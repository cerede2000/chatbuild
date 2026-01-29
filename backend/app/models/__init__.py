"""Expose les modèles ORM pour un import plus facile.

Importer ce module permet de s’assurer que toutes les classes sont
chargées et que SQLAlchemy connaît leurs métadonnées.
"""

from .user import User  # noqa: F401
from .config import GlobalConfig  # noqa: F401
from .category import Category  # noqa: F401
from .payment_method import PaymentMethod  # noqa: F401
from .account import BankAccount  # noqa: F401
from .share import AccountShare  # noqa: F401
from .operation import Operation  # noqa: F401
from .recurring import RecurringItem  # noqa: F401
from .enums import AccountType, PermissionLevel, OperationType, RecurringFrequency  # noqa: F401