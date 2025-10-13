"""Paradox resolution helpers for Aethelgard."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .ethics_filter import evaluate


@dataclass(slots=True)
class Resolution:
    choice: str | None
    discarded: Sequence[str]
    reasons: Sequence[str]


def resolve(questions: Iterable[str]) -> Resolution:
    """Pick the first ethically safe question."""

    discarded: list[str] = []
    reasons: list[str] = []
    for question in questions:
        candidate = (question or "").strip()
        if not candidate:
            continue
        verdict = evaluate(candidate)
        if verdict.allowed:
            return Resolution(choice=candidate, discarded=tuple(discarded), reasons=tuple(reasons))
        discarded.append(candidate)
        reasons.append(", ".join(verdict.reasons) or "rejected")
    return Resolution(choice=None, discarded=tuple(discarded), reasons=tuple(reasons))
