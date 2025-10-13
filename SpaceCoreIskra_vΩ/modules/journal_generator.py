"""Helpers for producing journal entries with guardrails."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, MutableMapping, Sequence, Any

from common.ethics_core import is_allowed

from .veil import check as veil_check

_METRIC_KEYS = ("∆", "D", "Ω", "Λ")


@dataclass(slots=True)
class JournalEntry:
    facet: str
    snapshot: str
    answer: str
    metrics: Mapping[str, float]
    mirror: str
    modules: Sequence[str] = field(default_factory=tuple)
    events: Mapping[str, Any] = field(default_factory=dict)
    marks: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def serialise(self) -> dict[str, Any]:
        payload = {
            "facet": self.facet,
            "snapshot": self.snapshot,
            "answer": self.answer,
            "mirror": self.mirror,
            "modules": list(self.modules),
            "events": dict(self.events),
            "marks": [dict(mark) for mark in self.marks],
        }
        payload.update({key: float(self.metrics.get(key, 0.0)) for key in _METRIC_KEYS})
        return payload


def _validate_answer(answer: str) -> None:
    if not veil_check(answer):
        raise ValueError("answer rejected by veil policy")
    if not is_allowed(answer):
        raise ValueError("answer rejected by ethics policy")


def build_entry(
    *,
    facet: str,
    snapshot: str,
    answer: str,
    metrics: Mapping[str, Any],
    mirror: str,
    modules: Iterable[str] | None = None,
    events: Mapping[str, Any] | None = None,
    marks: Iterable[Mapping[str, Any]] | None = None,
    timestamp: datetime | None = None,
) -> JournalEntry:
    """Return a validated :class:`JournalEntry` instance."""

    if not facet:
        raise ValueError("facet must be provided")
    if not snapshot:
        raise ValueError("snapshot must be provided")
    if not mirror:
        raise ValueError("mirror must be provided")
    if not answer or not answer.strip():
        raise ValueError("answer must be non-empty")

    _validate_answer(answer)

    metric_values: MutableMapping[str, float] = {}
    for key in _METRIC_KEYS:
        metric_values[key] = float(metrics.get(key, 0.0))

    return JournalEntry(
        facet=facet,
        snapshot=snapshot,
        answer=answer.strip(),
        metrics=metric_values,
        mirror=mirror,
        modules=tuple(modules or ()),
        events=dict(events or {}),
        marks=tuple(marks or ()),
        timestamp=timestamp or datetime.now(timezone.utc),
    )


def append_entry(entry: JournalEntry, path: str | Path = "JOURNAL.jsonl") -> dict[str, Any]:
    """Append ``entry`` to ``path`` and return the serialised payload."""

    target = Path(path)
    if not target.parent.exists():
        target.parent.mkdir(parents=True, exist_ok=True)

    payload = entry.serialise()
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json_dumps(payload) + "\n")
    return payload


def json_dumps(payload: Mapping[str, Any]) -> str:
    import json

    return json.dumps(payload, ensure_ascii=False)
