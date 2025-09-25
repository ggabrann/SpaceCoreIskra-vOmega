"""Prompt manager with persistent storage and search capabilities."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class PromptRecord:
    """Single prompt version stored in the repository."""

    text: str
    meta: Dict[str, object]
    created_at: str


class PromptManager:
    """Repository that keeps prompt revisions on disk."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = Path(path or "prompts.json")
        self.prompts: Dict[str, List[PromptRecord]] = {}
        if self.path.exists():
            self._load()

    # ------------------------------------------------------------------
    def _load(self) -> None:
        try:
            with self.path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            data = {}
        for name, versions in data.items():
            records: List[PromptRecord] = []
            if isinstance(versions, list):
                for raw in versions:
                    if not isinstance(raw, dict):
                        continue
                    records.append(
                        PromptRecord(
                            text=raw.get("text", ""),
                            meta=dict(raw.get("meta", {})),
                            created_at=raw.get("created_at", ""),
                        )
                    )
            if records:
                self.prompts[name] = records

    def _save(self) -> None:
        payload = {
            name: [record.__dict__ for record in versions]
            for name, versions in self.prompts.items()
        }
        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    def add(self, name: str, prompt: str, meta: Optional[Dict[str, object]] = None) -> PromptRecord:
        record = PromptRecord(
            text=prompt,
            meta=dict(meta or {}),
            created_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        )
        self.prompts.setdefault(name, []).append(record)
        self._save()
        return record

    def get(self, name: str) -> Optional[PromptRecord]:
        versions = self.prompts.get(name)
        if not versions:
            return None
        return versions[-1]

    def history(self, name: str) -> List[PromptRecord]:
        return list(self.prompts.get(name, []))

    def search(self, query: str) -> List[PromptRecord]:
        q = query.lower()
        matches: List[PromptRecord] = []
        for versions in self.prompts.values():
            for record in versions:
                haystack = " ".join([record.text, json.dumps(record.meta, ensure_ascii=False)]).lower()
                if q in haystack:
                    matches.append(record)
        return matches

    def tagged(self, tag: str) -> List[PromptRecord]:
        tag_lower = tag.lower()
        results: List[PromptRecord] = []
        for versions in self.prompts.values():
            for record in versions:
                tags = [str(t).lower() for t in record.meta.get("tags", [])]
                if tag_lower in tags:
                    results.append(record)
        return results


__all__ = ["PromptManager", "PromptRecord"]
