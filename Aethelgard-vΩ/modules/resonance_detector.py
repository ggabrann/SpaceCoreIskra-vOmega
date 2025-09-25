"""Resonance detection utilities for Aethelgard-vΩ."""
from __future__ import annotations

from typing import Dict


def detect(query: str, mode: str) -> Dict[str, int]:
    """Calculate resonance peaks based on rhythmic patterns."""
    letters = [ch for ch in query.lower() if ch.isalpha()]
    syllabic_weight = sum(1 for ch in letters if ch in "аеёиоуыэюя")
    modulation = len(mode)

    peaks = max(1, (syllabic_weight // 2) + modulation // 2)

    return {"resonance_peaks": peaks}
