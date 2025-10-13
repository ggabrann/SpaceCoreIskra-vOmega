"""Resonance detection utilities for Aethelgard."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Iterable, Sequence


@dataclass(slots=True)
class ResonanceReport:
    score: float
    baseline: float
    anomalies: Sequence[tuple[int, float]]
    safe: bool


def detect(signals: Iterable[float], *, threshold: float = 1.5) -> ResonanceReport:
    """Analyse ``signals`` and flag anomalies."""

    values = [float(value) for value in signals]
    if not values:
        return ResonanceReport(score=0.0, baseline=0.0, anomalies=(), safe=True)

    baseline = mean(values)
    deviation = pstdev(values) if len(values) > 1 else 0.0

    anomalies: list[tuple[int, float]] = []
    for idx, value in enumerate(values):
        if deviation and abs(value - baseline) > threshold * deviation:
            anomalies.append((idx, value))

    score = baseline - len(anomalies) * 0.5
    safe = score >= 0 and not anomalies
    return ResonanceReport(score=score, baseline=baseline, anomalies=tuple(anomalies), safe=safe)
