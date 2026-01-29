"""Route d’initialisation de l’application (one‑shot)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from ..database import get_session
from ..models.config import GlobalConfig


router = APIRouter()


class SetupRequest(BaseModel):
    currency: str = Field(..., max_length=3, min_length=3, description="Devise ISO 4217, ex : EUR")
    timezone: str = Field(..., max_length=64, description="Identifiant de fuseau horaire, ex : Europe/Paris")


# Utilise un code 201 (Created) pour éviter l'assertion de FastAPI (204 sans corps)
@router.post("/setup", status_code=201)
async def setup_app(data: SetupRequest, db: AsyncSession = Depends(get_session)) -> None:
    """Initialise la devise et le fuseau horaire globaux.

    Cette route doit être appelée une seule fois immédiatement après le premier
    démarrage. Elle devient inaccessible dès que la configuration est
    verrouillée.
    """
    # Récupérer la configuration (il n’y a qu’une seule ligne)
    result = await db.execute(GlobalConfig.__table__.select())
    config = result.scalar_one_or_none()
    if not config:
        # Si aucune config, en créer une
        config = GlobalConfig(currency=data.currency.upper(), timezone=data.timezone, initialized=True)
        db.add(config)
        await db.commit()
        return
    if config.initialized:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Application already initialized")
    # Mettre à jour et verrouiller
    config.currency = data.currency.upper()
    config.timezone = data.timezone
    config.initialized = True
    db.add(config)
    await db.commit()
    return