"""Routes pour la gestion des utilisateurs (admin uniquement)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models.user import User
from ..core.security import get_password_hash
from ..schemas.user import UserCreate, UserRead, UserUpdate
from .deps import require_admin


router = APIRouter()


@router.get("/users", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_session), current_admin: User = Depends(require_admin)) -> list[UserRead]:
    """Renvoie la liste de tous les utilisateurs."""
    from sqlalchemy import select
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.post("/users", response_model=UserRead, status_code=201)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin),
) -> User:
    """Crée un nouvel utilisateur (admin uniquement)."""
    # Vérifier l’unicité du nom
    from sqlalchemy import select
    exists = await db.execute(select(User).where(User.username == user_in.username))
    if exists.scalars().first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_admin=user_in.is_admin,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin),
) -> User:
    """Met à jour les informations d’un utilisateur (admin uniquement)."""
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.password:
        user.hashed_password = get_password_hash(user_in.password)
    if user_in.disabled is not None:
        user.disabled = user_in.disabled
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user