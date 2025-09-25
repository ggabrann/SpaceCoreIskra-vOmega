"""Handles journaling for light and shadow records."""
from __future__ import annotations

import json
from datetime import datetime
from typing import Dict, Any


class JournalArchitect:
    def __init__(self, journal_path: str, shadow_path: str) -> None:
        self.journal_path = journal_path
        self.shadow_path = shadow_path

    def _timestamp(self) -> str:
        return datetime.utcnow().isoformat() + "Z"

    def log_success(self, ctx) -> Dict[str, Any]:
        entry = {
            "timestamp": self._timestamp(),
            "facet": ctx.persona,
            "snapshot": ctx.query,
            "answer": ctx.mythic_overlay,
            "∆": ctx.metrics.get("∆"),
            "D": ctx.metrics.get("D"),
            "Ω": ctx.metrics.get("Ω"),
            "Λ": ctx.metrics.get("Λ"),
            "Ψ": ctx.metrics.get("Ψ"),
            "events": {"prompt": ctx.events.get("prompt"), "sources": ctx.sources},
        }
        self._append(self.journal_path, entry)
        if ctx.mythic_overlay and ctx.mythic_overlay.get("legend"):
            self._log_shadow(ctx, reason="mythic embellishment")
        return entry

    def log_blocked(self, ctx, reason: str) -> Dict[str, Any]:
        entry = {
            "timestamp": self._timestamp(),
            "facet": ctx.persona,
            "snapshot": ctx.query,
            "answer": None,
            "∆": ctx.metrics.get("∆"),
            "D": ctx.metrics.get("D"),
            "Ω": ctx.metrics.get("Ω"),
            "Λ": ctx.metrics.get("Λ"),
            "Ψ": ctx.metrics.get("Ψ"),
            "events": {"reason": reason},
        }
        self._append(self.shadow_path, {**entry, "mirror": "blocked"})
        return entry

    def _log_shadow(self, ctx, reason: str) -> None:
        entry = {
            "timestamp": self._timestamp(),
            "facet": ctx.persona,
            "mirror": ctx.query,
            "reason": reason,
        }
        self._append(self.shadow_path, entry)

    def _append(self, path: str, data: Dict[str, Any]) -> None:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(data, ensure_ascii=False) + "\n")
