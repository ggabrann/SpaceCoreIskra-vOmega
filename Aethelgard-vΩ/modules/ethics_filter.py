"""Ethical filter for Aethelgard-vΩ."""
from __future__ import annotations

from typing import Dict


SENSITIVE_KEYWORDS = {"запрещ", "разруш", "эксперимент"}


def evaluate(query: str, mode: str) -> Dict[str, str]:
    """Return the ethics status for the given query and mode."""
    lower_query = query.lower()

    if any(keyword in lower_query for keyword in SENSITIVE_KEYWORDS) and mode == "flux":
        decision = "rejected"
    elif "парадокс" in lower_query or mode == "quantum":
        decision = "conditional"
    else:
        decision = "passed"

    return {"ethics_check": decision}
