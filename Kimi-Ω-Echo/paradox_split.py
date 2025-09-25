"""Paradox detection helpers for the Echo pipeline."""

from __future__ import annotations

from typing import Dict


def resolve_paradox(user_text: str, metrics: Dict[str, float]) -> Dict[str, object]:
    """Identify paradoxical instructions and attempt to stabilise them."""

    lowered = user_text.lower()
    paradox_detected = any(keyword in lowered for keyword in ("paradox", "contradiction"))
    stability = round(1.0 - 0.3 if paradox_detected else 0.0, 2)

    resolved_text = user_text
    if paradox_detected:
        resolved_text = f"Paradox noted. Clarify intent: {user_text}".strip()

    return {
        "paradox_detected": paradox_detected,
        "stability_penalty": abs(stability),
        "resolved_text": resolved_text,
    }


__all__ = ["resolve_paradox"]
