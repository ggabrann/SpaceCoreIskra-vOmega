"""Journal generation utilities used by Iskra Nexus."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, MutableMapping, Sequence

from .facets_refine import FacetSnapshot, from_metrics


@dataclass(slots=True)
class JournalEntry:
    facet: str
    snapshot: str
    answer: str
    metrics: FacetSnapshot
    mirror: str
    modules: Sequence[str]
    events: Mapping[str, str]
    marks: Sequence[str]
    timestamp: str

    def as_dict(self) -> MutableMapping[str, object]:
        payload = {
            "facet": self.facet,
            "snapshot": self.snapshot,
            "answer": self.answer,
            "mirror": self.mirror,
            "modules": list(self.modules),
            "events": dict(self.events),
            "marks": list(self.marks),
            "timestamp": self.timestamp,
        }
        payload.update(self.metrics.as_dict())
        return payload


class JournalGenerator:
    """Append JSONL entries while enforcing metric structure."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def append(
        self,
        *,
        facet: str,
        snapshot: str,
        answer: str,
        metrics: Mapping[str, float],
        mirror: str = "shadow",
        modules: Iterable[str] | None = None,
        events: Mapping[str, str] | None = None,
        marks: Iterable[str] | None = None,
    ) -> JournalEntry:
        entry = JournalEntry(
            facet=facet,
            snapshot=snapshot,
            answer=answer,
            metrics=from_metrics(metrics),
            mirror=mirror,
            modules=tuple(modules or ()),
            events=dict(events or {}),
            marks=tuple(marks or ()),
            timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        )
        self._write(entry)
        return entry

    def _write(self, entry: JournalEntry) -> None:
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry.as_dict(), ensure_ascii=False) + "\n")
