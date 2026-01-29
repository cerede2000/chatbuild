"""Schémas Pydantic pour les utilisateurs."""

from __future__ import annotations

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    is_admin: bool = False


class UserUpdate(BaseModel):
    password: str | None = Field(default=None, min_length=6)
    disabled: bool | None = None


class UserRead(UserBase):
    id: int
    disabled: bool
    is_admin: bool

    class Config:
        from_attributes = True