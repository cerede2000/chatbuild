"""Gestion de la configuration de l’application.

Les paramètres sont chargés depuis les variables d’environnement mais
disposent de valeurs par défaut raisonnables. Les valeurs de configuration
globales (devise, fuseau horaire) sont persistées en base via le modèle
`GlobalConfig` et ne doivent être définies qu’une seule fois lors de
l’initialisation de l’instance.
"""

from __future__ import annotations

import os
import secrets
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Objet de configuration principal.

    Les champs sont automatiquement alimentés à partir des variables
    d’environnement lorsqu’elles existent. Un secret aléatoire est
    généré par défaut pour la clé secrète si aucune valeur n’est fournie.
    """

    # URL de connexion à la base. Par défaut, SQLite dans un dossier `data/`.
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/db.sqlite3", env="DATABASE_URL"
    )

    # Clé secrète pour signer les JWT. Si non fournie, une valeur aléatoire est générée.
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32), env="SECRET_KEY")

    # Algorithme de signature pour les JWT.
    algorithm: str = Field(default="HS256")

    # Durées de vie des tokens (en minutes).
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_minutes: int = Field(default=60 * 24 * 7)

    # Nom et mot de passe de l’administrateur initial
    admin_username: str = Field(default="admin", env="ADMIN_USERNAME")
    admin_password: str | None = Field(default=None, env="ADMIN_PASSWORD")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instance globale de paramètres accessibles dans toute l’application.
settings = Settings()