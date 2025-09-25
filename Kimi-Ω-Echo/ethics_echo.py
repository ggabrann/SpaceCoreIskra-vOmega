"""Ethical evaluation helpers for the Echo pipeline."""

from __future__ import annotations

from typing import Dict, List

_BANNED_TERMS = {"forbidden", "weapon", "harm"}


def evaluate_ethics(resolved_text: str, metrics: Dict[str, float]) -> Dict[str, object]:
    """Analyse text for ethical concerns and return the assessment payload."""

    lowered = resolved_text.lower()
    triggered_terms: List[str] = sorted(term for term in _BANNED_TERMS if term in lowered)
    safety = metrics.get("safety", 0.0)

    ethical = not triggered_terms and safety >= 0.5

    return {
        "ethical": ethical,
        "issues": triggered_terms,
        "safety_margin": round(safety, 2),
    }


__all__ = ["evaluate_ethics"]
