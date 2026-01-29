"""Schémas Pydantic pour les items récurrents."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from ..models.enums import OperationType, RecurringFrequency


class RecurringBase(BaseModel):
    type: OperationType
    label: str = Field(..., max_length=255)
    amount: Decimal
    frequency: RecurringFrequency
    moment: int = Field(..., ge=0, le=31)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration: Optional[int] = None
    category_id: int
    payment_method_id: Optional[int] = None
    comment: Optional[str] = Field(default=None, max_length=255)


class RecurringCreate(RecurringBase):
    account_id: int


class RecurringRead(RecurringBase):
    id: int
    account_id: int
    active: bool

    class Config:
        from_attributes = True