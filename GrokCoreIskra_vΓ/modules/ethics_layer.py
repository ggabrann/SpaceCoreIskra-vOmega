"""Lightweight ethics filtering utilities for GrokCoreIskra vΓ."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List

DEFAULT_TERMS = [
    "насилие",
    "вред",
    "weapon",
    "attack",
    "exploit",
]


@dataclass
class EthicsLayer:
    forbidden_terms: List[str] = field(default_factory=lambda: list(DEFAULT_TERMS))

    def update_terms(self, terms: Iterable[str]) -> None:
        self.forbidden_terms = [term.lower() for term in terms]

    def analyse(self, text: str) -> Dict[str, object]:
        lowered = text.lower()
        matched = [term for term in self.forbidden_terms if term in lowered]
        status = "allowed" if not matched else "blocked"
        return {
            "status": status,
            "matched": matched,
            "confidence": 1.0 if not matched else 0.2,
        }

    def enforce(self, text: str) -> str:
        report = self.analyse(text)
        if report["status"] == "allowed":
            return text
        return "Ответ скрыт фильтром этики."


__all__ = ["EthicsLayer", "DEFAULT_TERMS"]
