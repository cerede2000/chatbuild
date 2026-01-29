"""Fonctions de dépendances pour FastAPI.

Les dépendances centralisent l’accès à la base de données et la récupération
de l’utilisateur courant à partir du cookie d’authentification.
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models.user import User
from ..core.security import decode_token


async def get_db() -> AsyncSession:
    """Dépendance pour obtenir une session de base de données."""
    async for session in get_session():
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    access_token: str | None = Cookie(default=None, alias="access_token"),
) -> User:
    """Récupère l’utilisateur courant à partir du cookie `access_token`.

    Lève une exception HTTP 401 si le token est absent ou invalide.
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(access_token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    result = await db.execute(
        User.__table__.select().where(User.username == username)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.disabled:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """S’assure que l’utilisateur n’est pas désactivé."""
    return current_user


async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Vérifie que l’utilisateur courant est administrateur."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user