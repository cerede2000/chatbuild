"""Routes pour gérer les opérations courantes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models.operation import Operation
from ..models.account import BankAccount
from ..models.share import AccountShare
from ..models.enums import PermissionLevel, OperationType
from ..models.user import User
from ..schemas.operation import OperationCreate, OperationRead
from .deps import get_current_user


router = APIRouter()


def _has_permission_to_add(user: User, permission: PermissionLevel) -> bool:
    return permission in (
        PermissionLevel.VIEW_ADD_CURRENT,
        PermissionLevel.VIEW_ADD_CURRENT_AND_RECURRING,
        PermissionLevel.FULL_MANAGE,
    )


@router.get("/operations", response_model=list[OperationRead])
async def list_operations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
    account_id: int | None = None,
) -> list[Operation]:
    """Liste les opérations visibles par l’utilisateur. Optionnellement filtré par compte."""
    # Récupérer les comptes accessibles
    acc_ids = []
    from sqlalchemy import select
    # Récupérer les comptes dont l'utilisateur est propriétaire
    q_owned = select(BankAccount).where(BankAccount.owner_id == current_user.id)
    res_owned = await db.execute(q_owned)
    acc_ids += [acc.id for acc in res_owned.scalars().all()]
    # Récupérer les comptes partagés
    q_shared = (
        select(BankAccount)
        .join(AccountShare, BankAccount.id == AccountShare.account_id)
        .where(AccountShare.user_id == current_user.id)
    )
    res_shared = await db.execute(q_shared)
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
    result = await db.execute(select(Operation).where(Operation.account_id.in_(acc_filter)))
    return result.scalars().all()


@router.post("/operations", response_model=OperationRead, status_code=201)
async def create_operation(
    op_in: OperationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> Operation:
    """Crée une opération courante.

    L’utilisateur doit être propriétaire du compte ou disposer d’un droit suffisant.
    L’administrateur ne peut pas créer d’opération.
    """
    if current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin cannot create operations")
    # Vérifier que le compte existe
    from sqlalchemy import select
    result_acc = await db.execute(select(BankAccount).where(BankAccount.id == op_in.account_id))
    account = result_acc.scalars().first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    # Vérifier la propriété ou le partage
    allowed = False
    if account.owner_id == current_user.id:
        allowed = True
    else:
        # Vérifier le partage
        result_share = await db.execute(
            select(AccountShare)
            .where(AccountShare.account_id == op_in.account_id)
            .where(AccountShare.user_id == current_user.id)
        )
        share = result_share.scalars().first()
        if share and _has_permission_to_add(current_user, share.permission):
            allowed = True
    if not allowed:
        raise HTTPException(status_code=403, detail="Insufficient permission to add operation")
    operation = Operation(
        type=op_in.type,
        label=op_in.label,
        amount=op_in.amount,
        date=op_in.date,
        account_id=op_in.account_id,
        category_id=op_in.category_id,
        payment_method_id=op_in.payment_method_id,
        comment=op_in.comment,
    )
    db.add(operation)
    await db.commit()
    await db.refresh(operation)
    return operation