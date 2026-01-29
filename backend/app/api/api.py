"""Assemblage des différentes routes de l’API."""

from __future__ import annotations

from fastapi import APIRouter

from . import setup, auth, users, accounts, categories, operations, recurring


api_router = APIRouter()

api_router.include_router(setup.router, tags=["setup"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(operations.router, prefix="/operations", tags=["operations"])
api_router.include_router(recurring.router, prefix="/recurring", tags=["recurring"])