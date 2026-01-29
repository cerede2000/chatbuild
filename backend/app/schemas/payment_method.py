"""Schémas Pydantic pour les moyens de paiement."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PaymentMethodBase(BaseModel):
    name: str = Field(..., max_length=100)


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodRead(PaymentMethodBase):
    id: int
    deleted: bool

    class Config:
        from_attributes = True