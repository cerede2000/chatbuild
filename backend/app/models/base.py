"""Exports la base déclarative pour simplifier l’importation dans les modèles.

L’utilisation de ce fichier permet d’éviter les imports en cascade circulaires
entre les modèles et le gestionnaire de base.
"""

from ..database import Base  # noqa: F401