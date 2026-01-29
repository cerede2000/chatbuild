"""Modèle ORM représentant un utilisateur de l’application."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: int | None = Column(Integer, primary_key=True)
    username: str = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(255), nullable=False)
    disabled: bool = Column(Boolean, default=False)
    is_admin: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    # Relations
    accounts = relationship("BankAccount", back_populates="owner", cascade="all, delete-orphan")
    shares = relationship("AccountShare", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User id={self.id} username={self.username}>"