"""Context weaving utilities for Aethelgard-vΩ."""
from __future__ import annotations

from typing import Dict


def weave(query: str, mode: str) -> Dict[str, object]:
    """Evaluate the contextual resonance of the query."""
    words = [token for token in query.lower().split() if token]
    unique_words = len(set(words))
    complexity = len(query.split(","))

    lambda_shift = unique_words + complexity
    score = min(1.0, round(0.4 + unique_words / 25 + len(mode) / 20, 3))

    return {
        "Λ": lambda_shift,
        "context_weaving_score": score,
    }
