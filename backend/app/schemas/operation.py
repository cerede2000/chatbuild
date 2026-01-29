"""Schémas Pydantic pour les opérations courantes."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from ..models.enums import OperationType


class OperationBase(BaseModel):
    type: OperationType
    label: str = Field(..., max_length=255)
    amount: Decimal
    date: date
    category_id: int
    payment_method_id: Optional[int] = None
    comment: Optional[str] = Field(default=None, max_length=255)


class OperationCreate(OperationBase):
    account_id: int


class OperationRead(OperationBase):
    id: int
    account_id: int

    class Config:
        from_attributes = True