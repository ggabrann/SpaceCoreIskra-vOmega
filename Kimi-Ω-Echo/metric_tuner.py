"""Metric tuning helpers for the Echo pipeline."""

from __future__ import annotations

from typing import Dict


def tune_metrics(user_text: str, memory_payload: Dict[str, object]) -> Dict[str, float]:
    """Return a deterministic set of metrics based on the input payload."""

    recalled = memory_payload.get("recalled", [])
    history_size = len(memory_payload.get("history", []))

    coherence = min(1.0, 0.55 + 0.1 * len(recalled))
    novelty = max(0.0, 0.9 - 0.05 * history_size)
    safety = max(0.0, min(1.0, 0.8 - 0.1 * len(recalled)))

    return {
        "coherence": round(coherence, 2),
        "novelty": round(novelty, 2),
        "safety": round(safety, 2),
    }


__all__ = ["tune_metrics"]
