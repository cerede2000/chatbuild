"""Modèle ORM pour les comptes bancaires."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from .base import Base
from .enums import AccountType


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id: int | None = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False)
    bank: str | None = Column(String(100), nullable=True)
    account_number: str | None = Column(String(100), nullable=True)
    initial_balance: float = Column(Numeric(12, 2), nullable=False, default=0)
    owner_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    type: AccountType = Column(SAEnum(AccountType), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="accounts")
    operations = relationship(
        "Operation", back_populates="account", cascade="all, delete-orphan"
    )
    recurring_items = relationship(
        "RecurringItem", back_populates="account", cascade="all, delete-orphan"
    )
    shares = relationship(
        "AccountShare", back_populates="account", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<BankAccount id={self.id} name={self.name}>"