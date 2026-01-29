#!/usr/bin/env bash
set -euo pipefail

# Lancer les migrations Alembic (crée la base et les tables si nécessaire)
alembic upgrade head

# Démarrer l’application FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port 8000