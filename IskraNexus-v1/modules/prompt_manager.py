"""Prompt manager mirroring the SpaceCore repository behaviour."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional


class PromptManager:
    """Хранилище промптов с версионированием и поиском."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = Path(path or "prompts.json")
        self.prompts: Dict[str, List[Dict[str, object]]] = {}
        if self.path.exists():
            self._load()

    # ------------------------------------------------------------------
    def _load(self) -> None:
        try:
            with self.path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            for name, versions in data.items():
                if isinstance(versions, list):
                    self.prompts[name] = [dict(version) for version in versions if isinstance(version, dict)]
        except (json.JSONDecodeError, OSError):
            self.prompts = {}

    def _save(self) -> None:
        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(self.prompts, fh, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    def add(self, name: str, prompt: str, meta: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        record: Dict[str, object] = {
            "text": prompt,
            "meta": dict(meta or {}),
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        self.prompts.setdefault(name, []).append(record)
        self._save()
        return record

    def get(self, name: str) -> Optional[Dict[str, object]]:
        versions = self.prompts.get(name)
        if not versions:
            return None
        return dict(versions[-1])

    def history(self, name: str) -> List[Dict[str, object]]:
        return [dict(version) for version in self.prompts.get(name, [])]

    def search(self, query: str) -> List[Dict[str, object]]:
        """Простой полнотекстовый поиск по тексту, тегам и имени."""
        q = query.lower()
        results: List[Dict[str, object]] = []
        for name, versions in self.prompts.items():
            for version in versions:
                text = str(version.get("text", "")).lower()
                tags = " ".join(str(tag) for tag in version.get("meta", {}).get("tags", [])).lower()
                if q in text or q in tags or q in name.lower():
                    enriched = dict(version)
                    enriched["name"] = name
                    results.append(enriched)
        return results

    def tagged(self, tag: str) -> List[Dict[str, object]]:
        tag_lower = tag.lower()
        return [
            dict(version, name=name)
            for name, versions in self.prompts.items()
            for version in versions
            if tag_lower in (str(t).lower() for t in version.get("meta", {}).get("tags", []))
        ]

    def export(self, path: Path) -> None:
        """Экспорт репозитория без изменения основного файла."""
        export_path = Path(path)
        with export_path.open("w", encoding="utf-8") as fh:
            json.dump(self.prompts, fh, ensure_ascii=False, indent=2)

    def extend(self, name: str, versions: Iterable[Dict[str, object]]) -> None:
        """Импортирует версии в существующую запись без дублирования."""
        existing = {json.dumps(v, sort_keys=True, ensure_ascii=False) for v in self.prompts.get(name, [])}
        for version in versions:
            payload = dict(version)
            marker = json.dumps(payload, sort_keys=True, ensure_ascii=False)
            if marker not in existing:
                self.prompts.setdefault(name, []).append(payload)
                existing.add(marker)
        self._save()


__all__ = ["PromptManager"]
