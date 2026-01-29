"""Modèle ORM pour les opérations courantes."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from .base import Base
from .enums import OperationType


class Operation(Base):
    __tablename__ = "operations"

    id: int | None = Column(Integer, primary_key=True)
    type: OperationType = Column(SAEnum(OperationType), nullable=False)
    label: str = Column(String(255), nullable=False)
    amount: float = Column(Numeric(12, 2), nullable=False)
    date: date = Column(Date, nullable=False)
    account_id: int = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    category_id: int = Column(Integer, ForeignKey("categories.id"), nullable=False)
    payment_method_id: int | None = Column(Integer, ForeignKey("payment_methods.id"), nullable=True)
    comment: str | None = Column(String(255), nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    account = relationship("BankAccount", back_populates="operations")
    category = relationship("Category")
    payment_method = relationship("PaymentMethod")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Operation id={self.id} label={self.label} amount={self.amount}>"