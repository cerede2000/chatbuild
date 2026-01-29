"""Modèle ORM pour les items récurrents (templates d’opérations)."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base
from .enums import OperationType, RecurringFrequency


class RecurringItem(Base):
    __tablename__ = "recurring_items"

    id: int | None = Column(Integer, primary_key=True)
    type: OperationType = Column(SAEnum(OperationType), nullable=False)
    label: str = Column(String(255), nullable=False)
    amount: float = Column(Numeric(12, 2), nullable=False)
    account_id: int = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    frequency: RecurringFrequency = Column(SAEnum(RecurringFrequency), nullable=False)
    # Pour DAILY, moment est ignoré. Pour WEEKLY: 1=Monday…7=Sunday. Pour MONTHLY et autres: jour du mois 1..31.
    moment: int = Column(Integer, nullable=False)
    start_date: date | None = Column(Date, nullable=True)
    end_date: date | None = Column(Date, nullable=True)
    duration: int | None = Column(Integer, nullable=True)
    category_id: int = Column(Integer, ForeignKey("categories.id"), nullable=False)
    payment_method_id: int | None = Column(Integer, ForeignKey("payment_methods.id"), nullable=True)
    comment: str | None = Column(String(255), nullable=True)
    active: bool = Column(Boolean, default=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    account = relationship("BankAccount", back_populates="recurring_items")
    category = relationship("Category")
    payment_method = relationship("PaymentMethod")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<RecurringItem id={self.id} label={self.label} frequency={self.frequency}>"