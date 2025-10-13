"""Persistence layer for curated prompts.

The original implementation only exposed a bare dictionary without any
validation or guardrails.  This module keeps the persisted state compatible
with the simple JSON format (used across SpaceCore variants) while ensuring that
stored prompts respect veil and ethics policies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping

from common.ethics_core import is_allowed
from .veil import check as veil_check


@dataclass(slots=True)
class PromptRecord:
    """Single prompt entry with metadata."""

    name: str
    text: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "meta": dict(self.metadata)}


class PromptsRepo:
    """File-backed repository of prompts."""

    def __init__(self, path: str | Path = "prompts.json", *, auto_persist: bool = True) -> None:
        self.path = Path(path)
        self.auto_persist = auto_persist
        self._prompts: MutableMapping[str, PromptRecord] = {}
        if self.path.exists():
            self._load()

    def _load(self) -> None:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        for name, payload in raw.items():
            if not isinstance(payload, dict):
                raise ValueError(f"invalid payload for prompt '{name}'")
            text = payload.get("text", "")
            metadata = payload.get("meta", {})
            if not isinstance(metadata, dict):
                raise ValueError(f"invalid metadata for prompt '{name}'")
            self._prompts[name] = PromptRecord(name=name, text=text, metadata=metadata)

    def _serialize(self) -> Dict[str, Dict[str, Any]]:
        return {name: record.as_dict() for name, record in self._prompts.items()}

    def register(self, name: str, text: str, *, metadata: Mapping[str, Any] | None = None) -> PromptRecord:
        """Add or replace a prompt after running the safety filters."""

        if not name:
            raise ValueError("prompt name must be provided")
        if not text or not text.strip():
            raise ValueError("prompt text must be non-empty")
        if not veil_check(text):
            raise ValueError("prompt rejected by veil policy")
        if not is_allowed(text):
            raise ValueError("prompt rejected by ethics policy")

        safe_metadata = dict(metadata or {})
        record = PromptRecord(name=name, text=text.strip(), metadata=safe_metadata)
        self._prompts[name] = record
        if self.auto_persist:
            self.save()
        return record

    def get(self, name: str) -> PromptRecord | None:
        return self._prompts.get(name)

    def search(self, keyword: str) -> List[PromptRecord]:
        needle = keyword.lower()
        return [
            record
            for record in self._prompts.values()
            if needle in record.text.lower() or needle in " ".join(record.metadata.get("tags", [])).lower()
        ]

    def list_names(self) -> Iterable[str]:
        return sorted(self._prompts.keys())

    def save(self) -> None:
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._serialize(), ensure_ascii=False, indent=2), encoding="utf-8")

