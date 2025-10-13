"""Aggregate journal entries with ethics and veil guardrails."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from statistics import mean
from typing import Iterable, Mapping, MutableMapping, Any

from common.ethics_core import is_allowed

from .veil import check as veil_check

_METRIC_KEYS = ("∆", "D", "Ω", "Λ")


@dataclass(slots=True)
class AggregateResult:
    """Container with summary information used in CI reports."""

    count: int
    facets: Mapping[str, int]
    avg: Mapping[str, float]
    flagged: int
    flagged_examples: tuple[Mapping[str, Any], ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "count": self.count,
            "facets": dict(self.facets),
            "avg": dict(self.avg),
            "flagged": self.flagged,
            "flagged_examples": [dict(example) for example in self.flagged_examples],
        }


def _safe_metric(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def aggregate(entries: Iterable[Mapping[str, Any]]) -> AggregateResult:
    """Return summary statistics for ``entries`` respecting guardrails.

    Any entry that fails the veil check or ethics policy is excluded from the
    aggregated metrics and reported separately in ``flagged_examples``.
    """

    facets: Counter[str] = Counter()
    sums: MutableMapping[str, list[float]] = {key: [] for key in _METRIC_KEYS}
    flagged: list[Mapping[str, Any]] = []
    valid_count = 0

    for entry in entries:
        facet = str(entry.get("facet", "")).strip()
        if facet:
            facets[facet] += 1

        answer = str(entry.get("answer", ""))
        veil_ok = veil_check(answer)
        ethics_ok = is_allowed(answer)
        if not (veil_ok and ethics_ok):
            flagged.append({
                "facet": entry.get("facet"),
                "mirror": entry.get("mirror"),
                "reason": "veil" if not veil_ok else "ethics",
            })
            continue

        for key in _METRIC_KEYS:
            sums[key].append(_safe_metric(entry.get(key)))
        valid_count += 1

    averages = {key: (mean(values) if values else 0.0) for key, values in sums.items()}

    return AggregateResult(
        count=valid_count,
        facets=facets,
        avg=averages,
        flagged=len(flagged),
        flagged_examples=tuple(flagged),
    )
