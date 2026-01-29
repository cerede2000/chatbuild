"""Schémas Pydantic pour les comptes bancaires et leur partage."""

from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from ..models.enums import AccountType, PermissionLevel


class AccountBase(BaseModel):
    name: str = Field(..., max_length=100)
    bank: Optional[str] = Field(default=None, max_length=100)
    account_number: Optional[str] = Field(default=None, max_length=100)
    initial_balance: Decimal = Field(default=0)
    type: AccountType = AccountType.PERSONAL


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class ShareCreate(BaseModel):
    user_id: int
    permission: PermissionLevel