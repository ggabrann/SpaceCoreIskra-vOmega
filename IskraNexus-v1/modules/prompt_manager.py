"""Prompt management utilities for Iskra Nexus."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping

from .ethics_layer import EthicsLayer


@dataclass(slots=True)
class Prompt:
    key: str
    text: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "meta": dict(self.metadata)}


class PromptManager:
    """File-backed prompt catalogue with ethics enforcement."""

    def __init__(
        self,
        path: str | Path = "prompts.json",
        *,
        ethics: EthicsLayer | None = None,
        auto_persist: bool = True,
    ) -> None:
        self.path = Path(path)
        self.ethics = ethics or EthicsLayer()
        self.auto_persist = auto_persist
        self._prompts: MutableMapping[str, Prompt] = {}
        if self.path.exists():
            self._load()

    def _load(self) -> None:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        for key, payload in raw.items():
            if not isinstance(payload, dict):
                raise ValueError(f"invalid prompt payload for '{key}'")
            text = str(payload.get("text", ""))
            metadata = payload.get("meta", {})
            if not isinstance(metadata, dict):
                raise ValueError(f"invalid metadata for '{key}'")
            self._prompts[key] = Prompt(key, text, metadata)

    def _serialize(self) -> Dict[str, Dict[str, Any]]:
        return {key: prompt.as_dict() for key, prompt in self._prompts.items()}

    def save(self) -> None:
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._serialize(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def register(
        self,
        key: str,
        text: str,
        *,
        metadata: Mapping[str, Any] | None = None,
        overwrite: bool = True,
    ) -> Prompt:
        if not key:
            raise ValueError("prompt key must be provided")
        if not text or not text.strip():
            raise ValueError("prompt text must be non-empty")

        self.ethics.require(text)
        prompt = Prompt(key=key, text=text.strip(), metadata=dict(metadata or {}))
        if not overwrite and key in self._prompts:
            raise ValueError(f"prompt '{key}' already exists")
        self._prompts[key] = prompt
        if self.auto_persist:
            self.save()
        return prompt

    def get(self, key: str) -> Prompt | None:
        return self._prompts.get(key)

    def search(self, keyword: str) -> List[Prompt]:
        needle = keyword.lower()
        return [
            prompt
            for prompt in self._prompts.values()
            if needle in prompt.text.lower()
            or needle in " ".join(str(v) for v in prompt.metadata.values()).lower()
        ]

    def list_keys(self) -> Iterable[str]:
        return sorted(self._prompts.keys())

    def delete(self, key: str) -> None:
        self._prompts.pop(key, None)
        if self.auto_persist:
            self.save()
