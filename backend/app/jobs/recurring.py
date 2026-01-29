"""Tâche de matérialisation des items récurrents en opérations."""

from __future__ import annotations

import asyncio
from datetime import date, timedelta
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models.recurring import RecurringItem
from ..models.operation import Operation


async def materialize_once(session: AsyncSession, target_date: date) -> None:
    """Matérialise les items récurrents pour une date donnée.

    Cette fonction crée une opération pour chaque item actif dont la date
    effective correspond à la date spécifiée et qui n’a pas encore été
    matérialisé pour ce jour. Les règles de calcul du jour effectif sont
    simplifiées et devront être raffinées dans une prochaine version.
    """
    # Récupérer les items actifs sans conditions de période (simplifié)
    result = await session.execute(select(RecurringItem).where(RecurringItem.active.is_(True)))
    items = result.scalars().all()
    for item in items:
        # Déterminer si l’item doit être exécuté aujourd’hui
        should_execute = False
        if item.frequency == "DAILY":
            should_execute = True
        elif item.frequency == "WEEKLY":
            # moment: 1=lundi…7=dimanche
            if target_date.isoweekday() == item.moment:
                should_execute = True
        else:
            # cas mensuel et autres : comparer le jour du mois (report si fin de mois manquant)
            day = item.moment
            # ajustement si le jour n’existe pas ce mois-ci
            last_day = (target_date.replace(day=28) + timedelta(days=4)).day
            effective_day = min(day, last_day)
            if target_date.day == effective_day:
                should_execute = True
        if not should_execute:
            continue
        # Vérifier que l’item est dans sa période (si définie)
        if item.start_date and target_date < item.start_date:
            continue
        if item.end_date and target_date > item.end_date:
            continue
        # Vérifier si déjà matérialisé
        res = await session.execute(
            select(Operation)
            .where(Operation.account_id == item.account_id)
            .where(Operation.date == target_date)
            .where(Operation.label == item.label)
        )
        if res.scalar_one_or_none():
            continue
        # Créer l’opération
        op = Operation(
            type=item.type,
            label=item.label,
            amount=item.amount,
            date=target_date,
            account_id=item.account_id,
            category_id=item.category_id,
            payment_method_id=item.payment_method_id,
            comment=item.comment,
        )
        session.add(op)
    await session.commit()


async def recurring_materializer_loop() -> None:
    """Boucle infinie qui matérialise quotidiennement les items récurrents."""
    while True:
        try:
            async for db in get_session():
                await materialize_once(db, date.today())
                break
        except Exception as exc:  # pragma: no cover
            # On logguerait l’erreur ici
            pass
        # Attendre jusqu’au lendemain (simplifié : 24 h)
        await asyncio.sleep(60 * 60 * 24)


def start_recurring_materializer() -> None:
    """Démarre la tâche de fond dans un thread asynchrone.

    À appeler depuis un événement de démarrage FastAPI. La fonction retourne
    immédiatement et laisse la boucle tourner en arrière‑plan.
    """
    asyncio.create_task(recurring_materializer_loop())