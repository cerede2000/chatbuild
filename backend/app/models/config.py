"""Modèle persistant pour la configuration globale de l’application."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from .base import Base


class GlobalConfig(Base):
    __tablename__ = "global_config"

    id: int | None = Column(Integer, primary_key=True)
    currency: str = Column(String(3), nullable=False, default="EUR")
    timezone: str = Column(String(64), nullable=False, default="Europe/Paris")
    initialized: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<GlobalConfig currency={self.currency} timezone={self.timezone} initialized={self.initialized}>"