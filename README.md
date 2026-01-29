# ChatBuild – Application de suivi de budget

## Présentation

ChatBuild est une application web de suivi de budget multicomptes. Elle permet aux utilisateurs de gérer des comptes bancaires, de saisir des opérations ponctuelles et récurrentes, de partager des comptes avec des droits granulaires et d’obtenir une vue synthétique de leurs finances. Cette première version (`v0.1`) met en place une base fonctionnelle et containerisée qui peut être exécutée facilement via Docker.

## Fonctionnalités principales (v0.1)

- **Initialisation one‑shot** : lors du premier démarrage, l’administrateur définit la devise et le fuseau horaire globaux via l’interface `/setup`.
- **Authentification JWT** : connexion et renouvellement de tokens via cookies HttpOnly. Un compte admin est généré automatiquement avec un mot de passe aléatoire affiché une seule fois dans les logs du conteneur.
- **Gestion des utilisateurs (admin)** : création, activation/désactivation et réinitialisation du mot de passe des utilisateurs.
- **Gestion des comptes bancaires** : un utilisateur peut créer des comptes, définir un solde initial et partager chaque compte à d’autres utilisateurs avec quatre niveaux de permission (lecture seule, ajout d’opérations courantes, ajout d’items récurrents ou gestion complète hors suppression).
- **Catégories et moyens de paiement globaux** : création par tous les utilisateurs, suppression (soft‑delete) uniquement par l’admin. Des valeurs par défaut sont préchargées lors de la première migration.
- **Opérations courantes** : revenu ou dépense avec libellé, montant, date, catégorie et moyen de paiement.
- **Items récurrents** : modèle d’opération récurrente avec fréquence (journalier, hebdomadaire, mensuel, etc.), période de validité et moment d’exécution. Un job asynchrone matérialise les occurrences en opérations réelles.
- **API REST JSON** : l’API est servie par FastAPI et documentée via OpenAPI accessible sur `/docs`.
- **Frontend React** : une interface minimale (login, tableau de bord et liste des comptes) construite avec Vite, TypeScript et Tailwind CSS.
- **CI/CD GitHub Actions** : lint et tests automatiques, build multi‑stage Docker et publication de l’image sur GitHub Container Registry (`ghcr.io/cerede2000/chatbuild`).

## Mise en route rapide

### Prérequis

- Docker >= 20.10 et Docker Compose >= 1.29

### Lancement en production

```bash
# Récupérer l’image construite par le CI
docker compose pull

# Démarrer les services (backend + frontend + base de données)
docker compose up -d

# Lors du premier lancement
# 1. Consulter les logs pour récupérer le mot de passe admin généré
docker compose logs app
# 2. Ouvrir http://localhost:8000/setup pour définir la devise et le fuseau horaire
#    (ces valeurs ne pourront plus être modifiées par la suite)
```

### Lancement en développement

```bash
# Construire et lancer l’application en mode développement
docker compose -f docker-compose.yml up --build

# L’API est accessible sur http://localhost:8000
# Le frontend React est disponible via le même port (servi en statique par FastAPI).
```

### Structure du dépôt

| Dossier                   | Rôle                                                               |
|---------------------------|---------------------------------------------------------------------|
| `backend/`                | Code Python (FastAPI, SQLAlchemy, Pydantic, Alembic, tests)         |
| `frontend/`               | Code React/TypeScript/Vite/Tailwind                                 |
| `docker-compose.yml`      | Composition des services : application et volume de données         |
| `Dockerfile`              | Construction multi‑stage pour le backend et le frontend             |
| `.github/workflows/`      | Workflows GitHub Actions (CI et publication d’image Docker)         |
| `.gitignore`              | Fichiers à ignorer par git                                          |

## Questions / TODO produit

Cette première itération fournit une base solide et fonctionnelle. Certaines parties sont volontairement simplifiées et feront l’objet d’itérations futures :

1. **Import CSV** : l’import de fichiers CSV et le mapping des colonnes seront implémentés dans la version 0.2.
2. **Graphiques et timeline** : les vues graphiques et l’évolution dans le temps sont prévues pour la version 0.2.
3. **Gestion avancée des récurrences** : le job de matérialisation est volontairement basique et devra être optimisé.
