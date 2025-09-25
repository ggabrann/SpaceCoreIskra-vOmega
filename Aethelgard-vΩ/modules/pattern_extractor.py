"""Pattern extraction heuristics for Aethelgard-vΩ."""
from __future__ import annotations

from collections import Counter
from typing import Dict


def analyze(query: str, mode: str) -> Dict[str, int]:
    """Extract structural metrics from the query for the given mode."""
    tokens = [token for token in query.lower().split() if token]
    token_lengths = [len(token) for token in tokens] or [0]

    unique_chars = {ch for ch in query.lower() if ch.isalpha()}
    char_counts = Counter(ch for ch in query.lower() if ch.isalpha())

    density = len(unique_chars) + len(mode)
    delta = max(char_counts.values(), default=0) - len(tokens)
    depth = len(tokens) + sum(1 for length in token_lengths if length > 5)

    return {
        "pattern_density": density,
        "∆": delta,
        "D": depth,
    }
