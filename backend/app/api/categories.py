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
    from sqlalchemy import select
    result = await db.execute(select(Category).where(Category.deleted.is_(False)))
    return result.scalars().all()


@router.post("/categories", response_model=CategoryRead, status_code=201)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Category:
    """Crée une catégorie (accessible à tous les utilisateurs)."""
    from sqlalchemy import select
    exists = await db.execute(select(Category).where(Category.name == category_in.name))
    if exists.scalars().first():
        raise HTTPException(status_code=400, detail="Category already exists")
    cat = Category(name=category_in.name)
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


# Retourne 200 (OK) car FastAPI refuse 204 avec un corps
@router.delete("/categories/{category_id}", status_code=200)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_session),
    current_admin: User = Depends(require_admin),
) -> None:
    """Supprime (soft-delete) une catégorie (admin uniquement)."""
    from sqlalchemy import select
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalars().first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    cat.deleted = True
    db.add(cat)
    await db.commit()
    return