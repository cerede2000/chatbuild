"""Environnement Alembic pour gérer les migrations."""

from __future__ import annotations

import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy import engine_from_config
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

import os
import sys

# Ajouter le chemin de l’application pour importer les modèles
sys.path.append(str((context.config.config_file_name or "").split("/alembic.ini")[0]))
sys.path.append(str(os.path.abspath(os.path.join(__file__, "../.."))))

from app.database import Base  # noqa: E402
from app.models import user, config as config_model, category, payment_method, account, share, operation, recurring  # noqa: F401,E402

config = context.config

# Interprétez le fichier de configuration pour les logs Python.
fileConfig(config.config_file_name)

# Cible de métadonnées pour l’auto‑génération des migrations
target_metadata = Base.metadata


def get_url():
    return os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/db.sqlite3")


def run_migrations_offline() -> None:
    """Exécute les migrations en mode hors ligne.

    Ce mode ne requiert pas de connexion DB. Les instructions SQL sont
    énumérées directement dans le log/terminal.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Exécute les migrations en mode en ligne via un moteur asynchrone."""
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())