"""Modèle ORM pour le partage des comptes bancaires entre utilisateurs."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Enum as SAEnum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base
from .enums import PermissionLevel


class AccountShare(Base):
    __tablename__ = "account_shares"

    id: int | None = Column(Integer, primary_key=True)
    account_id: int = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission: PermissionLevel = Column(SAEnum(PermissionLevel), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("account_id", "user_id", name="uq_account_user"),
    )

    account = relationship("BankAccount", back_populates="shares")
    user = relationship("User", back_populates="shares")

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<AccountShare account_id={self.account_id} user_id={self.user_id}"
            f" permission={self.permission}>"
        )