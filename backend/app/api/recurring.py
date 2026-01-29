"""Routes pour gérer les items récurrents."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models.recurring import RecurringItem
from sqlalchemy import select
from ..models.account import BankAccount
from ..models.share import AccountShare
from ..models.enums import PermissionLevel
from ..models.user import User
from ..schemas.recurring import RecurringCreate, RecurringRead
from .deps import get_current_user


router = APIRouter()


def _has_permission_to_add_recurring(user: User, permission: PermissionLevel) -> bool:
    return permission in (
        PermissionLevel.VIEW_ADD_CURRENT_AND_RECURRING,
        PermissionLevel.FULL_MANAGE,
    )


@router.get("/recurring", response_model=list[RecurringRead])
async def list_recurring(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
    account_id: int | None = None,
) -> list[RecurringItem]:
    """Liste les items récurrents visibles par l’utilisateur."""
    # Déterminer les comptes accessibles
    acc_ids = []
    res_owned = await db.execute(
        select(BankAccount).where(BankAccount.owner_id == current_user.id)
    )
    acc_ids += [acc.id for acc in res_owned.scalars().all()]
    res_shared = await db.execute(
        (
            BankAccount.__table__.join(AccountShare, BankAccount.id == AccountShare.account_id)
            .select()
            .where(AccountShare.user_id == current_user.id)
        )
    )
    acc_ids += [acc.id for acc in res_shared.scalars().all()]
    acc_ids = list(set(acc_ids))
    if account_id:
        if account_id not in acc_ids:
            raise HTTPException(status_code=403, detail="Not authorized to view this account")
        acc_filter = [account_id]
    else:
        acc_filter = acc_ids
    if not acc_filter:
        return []
    result = await db.execute(
        select(RecurringItem).where(RecurringItem.account_id.in_(acc_filter))
    )
    return result.scalars().all()


@router.post("/recurring", response_model=RecurringRead, status_code=201)
async def create_recurring(
    rec_in: RecurringCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> RecurringItem:
    """Crée un item récurrent.

    L’utilisateur doit être propriétaire du compte ou disposer du droit approprié.
    L’administrateur ne peut pas créer d’items récurrents.
    """
    if current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin cannot create recurring items")
    # Vérifier que le compte existe
    res_acc = await db.execute(
        select(BankAccount).where(BankAccount.id == rec_in.account_id)
    )
    account = res_acc.scalars().first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    # Vérifier permission
    allowed = False
    if account.owner_id == current_user.id:
        allowed = True
    else:
        res_share = await db.execute(
            select(AccountShare)
            .where(AccountShare.account_id == rec_in.account_id)
            .where(AccountShare.user_id == current_user.id)
        )
        share = res_share.scalars().first()
        if share and _has_permission_to_add_recurring(current_user, share.permission):
            allowed = True
    if not allowed:
        raise HTTPException(status_code=403, detail="Insufficient permission to add recurring item")
    item = RecurringItem(
        type=rec_in.type,
        label=rec_in.label,
        amount=rec_in.amount,
        account_id=rec_in.account_id,
        frequency=rec_in.frequency,
        moment=rec_in.moment,
        start_date=rec_in.start_date,
        end_date=rec_in.end_date,
        duration=rec_in.duration,
        category_id=rec_in.category_id,
        payment_method_id=rec_in.payment_method_id,
        comment=rec_in.comment,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item