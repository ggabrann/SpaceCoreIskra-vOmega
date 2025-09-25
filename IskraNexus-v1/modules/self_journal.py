"""Shadow logging facility for the orchestrator."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class ShadowEntry:
    timestamp: str
    stage: str
    payload: Dict[str, Any]


class SelfJournal:
    def __init__(self) -> None:
        self._entries: List[ShadowEntry] = []

    def log(self, stage: str, payload: Dict[str, Any]) -> ShadowEntry:
        entry = ShadowEntry(
            timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            stage=stage,
            payload=dict(payload),
        )
        self._entries.append(entry)
        return entry

    @property
    def entries(self) -> List[Dict[str, Any]]:
        return [
            {"timestamp": entry.timestamp, "stage": entry.stage, "payload": entry.payload}
            for entry in self._entries
        ]

    def clear(self) -> None:
        self._entries.clear()


__all__ = ["SelfJournal", "ShadowEntry"]
