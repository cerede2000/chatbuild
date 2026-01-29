"""Modèle ORM pour les moyens de paiement."""

from __future__ import annotations

from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id: int | None = Column(Integer, primary_key=True)
    name: str = Column(String(100), unique=True, nullable=False)
    deleted: bool = Column(Boolean, default=False)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<PaymentMethod id={self.id} name={self.name}>"