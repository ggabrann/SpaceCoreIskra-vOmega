"""Filtering helpers for the Echo pipeline."""

from __future__ import annotations

from typing import Dict, Iterable, List

DEFAULT_FORBIDDEN_TERMS = {"forbidden", "classified", "bypass"}


def apply_filter(resolved_text: str, ethics_payload: Dict[str, object], *,
                 forbidden_terms: Iterable[str] = DEFAULT_FORBIDDEN_TERMS) -> Dict[str, object]:
    """Apply the final veil filter to the resolved text."""

    lowered = resolved_text.lower()
    forbidden_terms = set(forbidden_terms)
    detected: List[str] = sorted(term for term in forbidden_terms if term in lowered)

    blocked = bool(detected) or not ethics_payload.get("ethical", False)
    reason = ""
    if detected:
        reason = f"detected forbidden terms: {', '.join(detected)}"
    elif not ethics_payload.get("ethical", False):
        issues = ethics_payload.get("issues") or []
        if issues:
            reason = f"ethical issues: {', '.join(issues)}"
        else:
            reason = "ethical safety margin too low"

    final_text = "[BLOCKED]" if blocked else resolved_text

    return {
        "blocked": blocked,
        "final_text": final_text,
        "reason": reason,
        "detected_terms": detected,
    }


__all__ = ["apply_filter"]
