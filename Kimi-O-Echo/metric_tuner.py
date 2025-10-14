"""Metric adjustment helpers for Kimi-Ω-Echo."""

from __future__ import annotations

from typing import Any, Dict, Mapping


def adjust(metrics: Mapping[str, Any], factor: float) -> Dict[str, Any]:
    """Return scaled metrics while leaving non-numeric values untouched."""

    result: Dict[str, Any] = {}
    for key, value in (metrics or {}).items():
        if isinstance(value, (int, float)):
            result[key] = float(value) * float(factor)
        else:
            result[key] = value
    return result
