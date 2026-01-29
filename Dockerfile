# syntax=docker/dockerfile:1

###############################################
# Étape frontend : construction des assets React
###############################################
FROM node:20-alpine AS frontend-builder
WORKDIR /frontend
# Copie uniquement package.json (le fichier lock peut ne pas exister dans l'arbre)
COPY frontend/package.json ./
RUN npm install --quiet
# Puis copie le reste du code source et construit l'application React
COPY frontend/ ./
RUN npm run build

###############################################
# Étape backend : installation des dépendances
###############################################
FROM python:3.12-slim AS python-base
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copie des fichiers de dépendances et installation
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

###############################################
# Étape finale : assemblage backend + frontend
###############################################
FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copie des dépendances depuis l’étape python-base
COPY --from=python-base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=python-base /usr/local/bin /usr/local/bin

# Copie du code backend
COPY backend/app/ ./app/
COPY backend/alembic/ ./alembic/
COPY backend/alembic.ini ./alembic.ini

# Copie des assets frontend compilés dans un répertoire statique servi par FastAPI
COPY --from=frontend-builder /frontend/dist ./static

# Copie du script d’entrée et le rend exécutable
COPY backend/entrypoint.sh ./entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Crée le répertoire de données (accessible en écriture par root)
RUN mkdir -p /app/data

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]