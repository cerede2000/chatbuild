"""Modèle ORM pour les catégories d’opérations."""

from __future__ import annotations

from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class Category(Base):
    __tablename__ = "categories"

    id: int | None = Column(Integer, primary_key=True)
    name: str = Column(String(100), unique=True, nullable=False)
    deleted: bool = Column(Boolean, default=False)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Category id={self.id} name={self.name}>"