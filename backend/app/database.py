"""Gestion de la connexion à la base de données et de la session.

Ce module configure le moteur SQLAlchemy asynchrone pour SQLite et
expose un générateur de session utilisable comme dépendance FastAPI.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .core.config import settings


class Base(DeclarativeBase):
    """Base déclarative pour l’ensemble des modèles ORM."""


# Création du moteur asynchrone. L’option « future=True » active l’API 2.0.
engine = create_async_engine(settings.database_url, echo=False, future=True)

# Création d’un fabriquant de sessions asynchrones.
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    """Dépendance FastAPI fournissant une session de base de données.

    Usage :
        async with get_session() as session:
            ...
    """
    async with async_session() as session:
        yield session