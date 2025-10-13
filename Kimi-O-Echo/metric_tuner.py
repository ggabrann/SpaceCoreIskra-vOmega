"""Metric tuning for echo scenarios.

Echo feedback can influence certain metrics (e.g. echo level, drift).
This module provides a simple scaling function that multiplies each
numeric metric by a specified factor.  Non‑numeric values are left
unchanged.
"""

from __future__ import annotations

from typing import Any, Dict


def adjust(metrics: Dict[str, Any], factor: float) -> Dict[str, Any]:
    """Return a new metrics mapping with numeric values scaled by ``factor``.

    Parameters
    ----------
    metrics:
        Mapping of metric names to arbitrary values.  Numeric values
        (ints and floats) are multiplied by the given factor.  Other
        values are copied unchanged.
    factor:
        Scaling factor applied to numeric metrics.

    Returns
    -------
    dict
        A new dictionary containing the scaled metrics.
    """
    result: Dict[str, Any] = {}
    for key, value in (metrics or {}).items():
        if isinstance(value, (int, float)):
            result[key] = value * factor
        else:
            result[key] = value
    return result
