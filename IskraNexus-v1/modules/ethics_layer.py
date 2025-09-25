"""Minimal ethics filter used by the orchestrator."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List


DEFAULT_FORBIDDEN = [
    "насилие",
    "оружие",
    "пытка",
    "hate",
]


@dataclass
class EthicsLayer:
    forbidden: List[str] = field(default_factory=lambda: list(DEFAULT_FORBIDDEN))

    def is_allowed(self, text: str) -> bool:
        low = text.lower()
        return not any(term in low for term in self.forbidden)

    def enforce(self, text: str) -> str:
        if self.is_allowed(text):
            return text
        return "Ответ скрыт этическим фильтром."

    def update_terms(self, terms: Iterable[str]) -> None:
        self.forbidden = list(dict.fromkeys(term.lower() for term in terms))


__all__ = ["EthicsLayer", "DEFAULT_FORBIDDEN"]
