"""Self reflection helpers for Aethelgard."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from common.ethics_core import is_allowed
from SpaceCoreIskra_vΩ.modules.veil import check as veil_check


@dataclass(slots=True)
class Reflection:
    insights: Sequence[str]
    discarded: Sequence[str]


def reflect(notes: Iterable[str]) -> Reflection:
    """Filter ``notes`` through guardrails and return safe insights."""

    insights: list[str] = []
    discarded: list[str] = []
    for note in notes:
        snippet = (note or "").strip()
        if not snippet:
            continue
        if veil_check(snippet) and is_allowed(snippet):
            insights.append(snippet)
        else:
            discarded.append(snippet)
    return Reflection(insights=tuple(insights), discarded=tuple(discarded))
