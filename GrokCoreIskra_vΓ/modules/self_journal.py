"""Shadow journal helpers for GrokCoreIskra vΓ."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


@dataclass
class JournalEntry:
    timestamp: str
    stage: str
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {"timestamp": self.timestamp, "stage": self.stage, "payload": self.payload}


class SelfJournal:
    def __init__(self, *, path: Path | None = None) -> None:
        self.path = Path(path) if path else Path(__file__).resolve().parents[1] / "SHADOW_JOURNAL.jsonl"
        self.entries: List[JournalEntry] = []

    def log(self, stage: str, payload: Dict[str, Any]) -> JournalEntry:
        entry = JournalEntry(
            timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            stage=stage,
            payload=dict(payload),
        )
        self.entries.append(entry)
        return entry

    def persist(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            for entry in self.entries:
                fh.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")

    def extend(self, entries: Iterable[JournalEntry]) -> None:
        for entry in entries:
            self.entries.append(entry)

    def clear(self) -> None:
        self.entries.clear()


__all__ = ["JournalEntry", "SelfJournal"]
