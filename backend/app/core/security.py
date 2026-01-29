"""Fonctions utilitaires liées à la sécurité et aux JWT.

Ce module encapsule la logique de hachage des mots de passe et de création
et validation des tokens JWT. Les tokens sont signés avec la clé secrète
configurée dans `Settings`. Les durées de vie sont également configurables.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie qu’un mot de passe en clair correspond au haché stocké."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Calcule le haché d’un mot de passe pour stockage en base."""
    return pwd_context.hash(password)


def create_token(
    data: dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Génère un JWT signé contenant les données fournies.

    Args:
        data: dictionnaire de claims à inclure.
        expires_delta: durée avant expiration. Si `None`, la durée par défaut
            des tokens d’accès est utilisée.
    Returns:
        Un token JWT encodé en chaîne de caractères.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any] | None:
    """Vérifie la validité d’un token et retourne les données décodées.

    Returns `None` si le token est invalide ou expiré.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None