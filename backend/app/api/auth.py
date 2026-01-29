"""Routes d’authentification."""

from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models.user import User
from ..core.security import verify_password, get_password_hash, create_token
from ..core.config import settings
from ..schemas.token import Token


router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login", response_model=Token)
async def login(
    data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_session),
) -> Token:
    """Authentifie un utilisateur et renvoie un token JWT.

    Le token est également envoyé dans un cookie HttpOnly pour être
    automatiquement renvoyé par le client lors des requêtes suivantes.
    """
    result = await db.execute(
        User.__table__.select().where(User.username == data.username)
    )
    user: User | None = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(status_code=403, detail="User disabled")
    # Générer le token d’accès et le rafraîchissement
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_token({"sub": user.username}, expires_delta=access_token_expires)
    # Stocker dans un cookie HttpOnly
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.access_token_expire_minutes * 60,
        secure=False,
        samesite="lax",
    )
    return Token(access_token=access_token)