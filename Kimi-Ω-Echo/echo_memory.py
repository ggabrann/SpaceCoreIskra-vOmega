"""Utility helpers for managing lightweight echo memory."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional


def _normalise_history(history: Optional[Iterable[str]]) -> List[str]:
    """Return a clean list representation of the provided history."""

    if history is None:
        return []
    if isinstance(history, list):
        return [str(item) for item in history]
    return [str(item) for item in list(history)]


def load_memory(user_text: str, metadata: Optional[Dict[str, object]] = None) -> Dict[str, object]:
    """Produce a deterministic memory payload for the echo pipeline.

    The implementation is intentionally lightweight.  It inspects an optional
    ``history`` collection present in ``metadata`` and selects the fragments
    that overlap with the current ``user_text``.
    """

    metadata = metadata or {}
    history = _normalise_history(metadata.get("history"))
    lowered_text = user_text.lower()

    recalled = [
        fragment
        for fragment in history
        if any(token and token in lowered_text for token in fragment.lower().split())
    ]

    return {
        "history": history,
        "recalled": recalled,
        "memory_score": round(min(1.0, 0.4 + 0.15 * len(recalled)), 2),
    }


__all__ = ["load_memory"]
