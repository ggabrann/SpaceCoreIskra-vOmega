"""Quantum core utilities for Aethelgard‑vΩ.

Quantum mechanics serve as a metaphor for states of uncertainty
within the Aethelgard layer.  Here we implement a trivial helper
that computes the arithmetic mean of a sequence of numeric values.
If the sequence is empty, zero is returned.  This can be used to
collapse multiple metric measurements into a single representative
value.
"""

from __future__ import annotations

from typing import Iterable


def compute_state(values: Iterable[float]) -> float:
    """Return the average of ``values`` or ``0.0`` if empty."""
    total = 0.0
    count = 0
    for v in values:
        total += float(v)
        count += 1
    return total / count if count else 0.0
