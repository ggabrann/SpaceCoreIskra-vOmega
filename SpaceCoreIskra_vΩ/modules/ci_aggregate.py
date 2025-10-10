"""Aggregate journal metrics for SpaceCore Искра modules."""

from __future__ import annotations

from collections.abc import Iterable
from statistics import mean
from typing import Sequence

JournalEntry = dict[str, object]


def _coerce_float(value: object) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _iter_items(candidate: object) -> Iterable[object]:
    if isinstance(candidate, list):
        yield from candidate
    elif candidate is not None:
        yield candidate


def _has_evidence(entry: JournalEntry) -> bool:
    direct = entry.get("evidence")
    events = entry.get("events") if isinstance(entry.get("events"), dict) else {}
    nested = events.get("evidence") if isinstance(events, dict) else None

    for candidate in _iter_items(direct):
        if isinstance(candidate, str) and candidate.strip():
            return True
        if candidate:
            return True
    for candidate in _iter_items(nested):
        if isinstance(candidate, str) and candidate.strip():
            return True
        if candidate:
            return True
    return False


def aggregate(
    main_entries: Sequence[JournalEntry],
    shadow_entries: Sequence[JournalEntry] | None = None,
) -> dict[str, object]:
    """Return summary statistics for canon journal slices."""

    main_entries = list(main_entries)
    shadow_entries = list(shadow_entries or [])

    averages: dict[str, float] = {}
    for key in ("∆", "D", "Ω", "Λ"):
        values = [
            parsed
            for parsed in (_coerce_float(entry.get(key)) for entry in main_entries)
            if parsed is not None
        ]
        averages[key] = round(mean(values), 3) if values else 0.0

    facets = sorted(
        {
            entry.get("facet")
            for entry in main_entries
            if isinstance(entry.get("facet"), str) and entry.get("facet").strip()
        }
    )

    mirrors = {
        entry.get("mirror")
        for entry in main_entries
        if isinstance(entry.get("mirror"), str)
    }
    relevant_shadow = [
        entry for entry in shadow_entries if entry.get("mirror") in mirrors
    ]

    evidence_hits = sum(1 for entry in main_entries if _has_evidence(entry))

    return {
        "count": len(main_entries),
        "facets": facets,
        "avg": averages,
        "shadow_ratio": (
            round(len(relevant_shadow) / len(main_entries), 3)
            if main_entries
            else 0.0
        ),
        "evidence_coverage": (
            round(evidence_hits / len(main_entries), 3) if main_entries else 0.0
        ),
    }


__all__ = ["aggregate"]
