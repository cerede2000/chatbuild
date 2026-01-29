"""Routes pour gérer les catégories d’opérations."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models.category import Category
from ..schemas.category import CategoryCreate, CategoryRead
from ..models.user import User
from .deps import get_current_user, require_admin


router = APIRouter()


@router.get("/categories", response_model=list[CategoryRead])
async def list_categories(db: AsyncSession = Depends(get_session)) -> list[Category]:
    """Liste toutes les catégories non supprimées."""
    result = await db.execute(Category.__table__.select().where(Category.deleted.is_(False)))
    return result.scalars().all()


@router.post("/categories", response_model=CategoryRead, status_code=201)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Category:
    """Crée une catégorie (accessible à tous les utilisateurs)."""
    exists = await db.execute(Category.__table__.select().where(Category.name == category_in.name))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Category already exists")
    cat = Category(name=category_in.name)
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin),
) -> None:
    """Supprime (soft-delete) une catégorie (admin uniquement)."""
    result = await db.execute(Category.__table__.select().where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    cat.deleted = True
    db.add(cat)
    await db.commit()
    return