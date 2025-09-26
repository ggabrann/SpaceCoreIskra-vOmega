"""Skill toolkit for Ния: контент, решения, ритуалы микро-шагов."""
from __future__ import annotations

from typing import Dict, Iterable, Tuple


CONTENT_TEMPLATES = {
    "light_post": ["разогрев (1 мин)", "каркас идеи (5 мин)", "черновик (7 мин)", "CTA (2 мин)"],
    "retreat_announcement": ["ключевая тема", "даты", "программа", "приглашение"],
    "partner_letter": ["приветствие", "ценность", "предложение шага"],
}


def decision_matrix(options: Iterable[Dict[str, float]], criteria: Dict[str, float]) -> Tuple[str, float]:
    """Return best option according to weighted criteria."""
    scores = {}
    for option in options:
        name = option.get("name", "option")
        total = 0.0
        for crit, weight in criteria.items():
            total += weight * option.get(crit, 0)
        scores[name] = total
    best = max(scores.items(), key=lambda item: item[1])
    return best


RITUALS = {
    "morning": ["чек-ин", "интенция дня", "микро-движение"],
    "evening": ["итог", "благодарность", "выбор мягкого шага"],
    "reset": ["дыхание 4-7-8", "вытяжение", "вода", "напоминание об опоре"],
}
