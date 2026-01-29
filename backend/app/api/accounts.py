"""Routes pour la gestion des comptes bancaires et du partage."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models.account import BankAccount
from sqlalchemy import select
from ..models.share import AccountShare
from ..models.user import User
from ..models.enums import PermissionLevel
from ..schemas.account import AccountCreate, AccountRead, ShareCreate
from .deps import get_current_user


router = APIRouter()


@router.get("/accounts", response_model=list[AccountRead])
async def list_accounts(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)) -> list[BankAccount]:
    """Retourne la liste des comptes accessibles à l’utilisateur courant."""
    # Comptes dont l’utilisateur est propriétaire
    q1 = select(BankAccount).where(BankAccount.owner_id == current_user.id)
    result1 = await db.execute(q1)
    owned = result1.scalars().all()
    # Comptes partagés
    q2 = (
        BankAccount.__table__.join(AccountShare, BankAccount.id == AccountShare.account_id)
        .select()
        .where(AccountShare.user_id == current_user.id)
    )
    result2 = await db.execute(q2)
    shared = result2.scalars().all()
    accounts = list({a.id: a for a in owned + shared}.values())
    return accounts


@router.post("/accounts", response_model=AccountRead, status_code=201)
async def create_account(
    account_in: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> BankAccount:
    """Crée un nouveau compte bancaire pour l’utilisateur courant.

    Les administrateurs n’ont pas le droit de créer des comptes bancaires.
    """
    if current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin cannot own accounts")
    account = BankAccount(
        name=account_in.name,
        bank=account_in.bank,
        account_number=account_in.account_number,
        initial_balance=account_in.initial_balance,
        owner_id=current_user.id,
        type=account_in.type,
    )
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


def _get_account_or_404(db: AsyncSession, account_id: int) -> BankAccount:
    """Récupère un compte ou lève 404 (utilitaire interne synchronisé)."""
    raise NotImplementedError  # placeholder pour Mypy


# Retourne 201 (Created) pour refléter la création ou mise à jour d’un partage
@router.post("/accounts/{account_id}/shares", status_code=201)
async def share_account(
    account_id: int,
    share_in: ShareCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> None:
    """Partage un compte avec un autre utilisateur.

    Seul le propriétaire du compte peut partager ou modifier les partages.
    """
    # Vérifier l’existence du compte et la propriété
    result = await db.execute(
        select(BankAccount).where(BankAccount.id == account_id)
    )
    account = result.scalars().first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can share account")
    # Interdire de partager à soi-même
    if share_in.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot share account with yourself")
    # Vérifier que la permission est valide
    if share_in.permission not in PermissionLevel:
        raise HTTPException(status_code=400, detail="Invalid permission")
    # Vérifier si déjà partagé
    exists = await db.execute(
        select(AccountShare)
        .where(AccountShare.account_id == account_id)
        .where(AccountShare.user_id == share_in.user_id)
    )
    share = exists.scalars().first()
    if share:
        # Mise à jour de la permission
        share.permission = share_in.permission
        db.add(share)
    else:
        share = AccountShare(
            account_id=account_id,
            user_id=share_in.user_id,
            permission=share_in.permission,
        )
        db.add(share)
    await db.commit()
    return