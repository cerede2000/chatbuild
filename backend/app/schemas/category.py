"""Schémas Pydantic pour les catégories."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    deleted: bool

    class Config:
        from_attributes = True