"""Définition des énumérations partagées par plusieurs modèles."""

from enum import Enum


class AccountType(str, Enum):
    """Type de compte bancaire."""

    PERSONAL = "PERSONAL"
    JOINT = "JOINT"


class PermissionLevel(str, Enum):
    """Niveaux de permission pour le partage des comptes."""

    VIEW_ONLY = "VIEW_ONLY"
    VIEW_ADD_CURRENT = "VIEW_ADD_CURRENT"
    VIEW_ADD_CURRENT_AND_RECURRING = "VIEW_ADD_CURRENT_AND_RECURRING"
    FULL_MANAGE = "FULL_MANAGE"


class OperationType(str, Enum):
    """Type d’opération (revenu ou dépense)."""

    REVENU = "REVENU"
    DEPENSE = "DEPENSE"


class RecurringFrequency(str, Enum):
    """Fréquence des items récurrents."""

    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    EVERY_2_MONTHS = "EVERY_2_MONTHS"
    EVERY_3_MONTHS = "EVERY_3_MONTHS"
    EVERY_6_MONTHS = "EVERY_6_MONTHS"
    YEARLY = "YEARLY"