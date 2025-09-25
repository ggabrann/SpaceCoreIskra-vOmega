"""Paradox resolution logic for Aethelgard-vΩ."""
from __future__ import annotations

from typing import Dict

KEYWORDS_RESOLVE = {"парадокс", "противоречие", "антиномия"}


def resolve(query: str, mode: str) -> Dict[str, object]:
    """Estimate paradox resolution confidence."""
    lower_query = query.lower()
    contains_paradox = any(keyword in lower_query for keyword in KEYWORDS_RESOLVE)

    omega = len(mode) - lower_query.count("а")
    resolved = contains_paradox or mode in {"lucid", "nexus"}

    return {
        "Ω": omega,
        "paradox_resolved": resolved,
    }
