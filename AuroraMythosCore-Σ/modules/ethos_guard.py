"""Ethical boundary detection with graded responses."""
from __future__ import annotations

from typing import Dict

FORBIDDEN = {
    "high": ["создать вирус", "террор", "оружие", "взлом"],
    "medium": ["манипуляция", "дезинформация"],
}


class EthosGuard:
    def __init__(self) -> None:
        self.counters = {"blocked": 0, "warnings": 0}

    def is_allowed(self, text: str) -> bool:
        lowered = text.lower()
        for word in FORBIDDEN["high"]:
            if word in lowered:
                self.counters["blocked"] += 1
                return False
        for word in FORBIDDEN["medium"]:
            if word in lowered:
                self.counters["warnings"] += 1
        return True

    def report(self) -> Dict[str, int]:
        return dict(self.counters)
