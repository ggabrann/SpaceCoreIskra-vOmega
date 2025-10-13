"""Quantised metric helpers for Aethelgard."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(slots=True)
class QuantumState:
    value: float
    amplitudes: Sequence[float]


def collapse(values: Iterable[float]) -> QuantumState:
    """Collapse a sequence of values into a single state."""

    amplitudes = [float(v) for v in values]
    if not amplitudes:
        return QuantumState(value=0.0, amplitudes=())
    value = sum(amplitudes) / len(amplitudes)
    return QuantumState(value=value, amplitudes=tuple(amplitudes))


def compute_state(values: Iterable[float]) -> float:
    """Backward compatible helper returning the collapsed value."""

    return collapse(values).value
