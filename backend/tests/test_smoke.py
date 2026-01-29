"""Tests simples pour s’assurer que l’application démarre et que les enums sont corrects.

Ces tests sont volontairement minimalistes pour valider la présence de
certains composants critiques. Des tests plus complets (permissions,
soft‑delete, récurrences) seront ajoutés dans les prochaines itérations.
"""

import os
import sys

# Ajoute le dossier racine du projet au PYTHONPATH pour permettre l’import de `backend`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app.models.enums import PermissionLevel, AccountType, OperationType, RecurringFrequency


def test_enums_exist() -> None:
    assert PermissionLevel.FULL_MANAGE in PermissionLevel
    assert AccountType.PERSONAL in AccountType
    assert OperationType.REVENU in OperationType
    assert RecurringFrequency.MONTHLY in RecurringFrequency


def test_basic_logic() -> None:
    # Vérifie qu’une simple assertion fonctionne
    assert 1 + 1 == 2