"""Point d’entrée principal de l’application FastAPI."""

from __future__ import annotations

import secrets
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .api.api import api_router
from .database import get_session
from .models.user import User
from .models.config import GlobalConfig
from .models.category import Category
from .models.payment_method import PaymentMethod
from .core.config import settings
from .core.security import get_password_hash
from .jobs import start_recurring_materializer

# Définitions des valeurs par défaut
DEFAULT_CATEGORIES = [
    "Salaire",
    "Crédit",
    "Loyer",
    "Nourriture",
    "Restaurant",
    "Loisir",
    "Carburant",
    "Enfant",
    "Vêtement",
    "Soins",
    "École",
    "Périscolaire",
    "Assurance",
    "Énergie",
]

DEFAULT_PAYMENT_METHODS = [
    "Carte Bancaire",
    "Chèque",
    "Virement",
    "Espèces",
]


app = FastAPI(title="ChatBuild Budget API")

# CORS (configurable si besoin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

# Monter les fichiers statiques du frontend si disponibles
static_path = Path(__file__).resolve().parents[2] / "static"
if static_path.exists():
    app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")


@app.on_event("startup")
async def startup_event():
    """Initialise l’administrateur, la configuration globale et les valeurs par défaut."""
    async for db in get_session():
        # Créer ou récupérer la configuration globale
        result = await db.execute(GlobalConfig.__table__.select())
        config = result.scalar_one_or_none()
        if not config:
            config = GlobalConfig(currency="EUR", timezone="Europe/Paris", initialized=False)
            db.add(config)
            await db.commit()
        # Créer l’utilisateur administrateur s’il n’existe pas
        res_admin = await db.execute(
            User.__table__.select().where(User.username == settings.admin_username)
        )
        admin = res_admin.scalar_one_or_none()
        if not admin:
            # Générer un mot de passe aléatoire si non fourni
            password = settings.admin_password or secrets.token_urlsafe(12)
            print(
                f"[INIT] Admin user created. Username: {settings.admin_username}, Password: {password}",
                flush=True,
            )
            admin = User(
                username=settings.admin_username,
                hashed_password=get_password_hash(password),
                is_admin=True,
            )
            db.add(admin)
            await db.commit()
        # Pré-charger les catégories par défaut
        for name in DEFAULT_CATEGORIES:
            res = await db.execute(Category.__table__.select().where(Category.name == name))
            if not res.scalar_one_or_none():
                db.add(Category(name=name))
        # Pré-charger les moyens de paiement par défaut
        for name in DEFAULT_PAYMENT_METHODS:
            res = await db.execute(
                PaymentMethod.__table__.select().where(PaymentMethod.name == name)
            )
            if not res.scalar_one_or_none():
                db.add(PaymentMethod(name=name))
        await db.commit()
        break  # on ne veut qu’une seule session

    # Démarrer la tâche de matérialisation des récurrences en arrière‑plan
    start_recurring_materializer()


@app.get("/ping")
async def ping() -> dict[str, str]:
    """Endpoint de santé simple."""
    return {"status": "ok"}