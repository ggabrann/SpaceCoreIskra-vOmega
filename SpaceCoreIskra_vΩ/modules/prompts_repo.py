import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class PromptsRepo:
    """Хранилище промптов с версионированием и поиском."""

    def __init__(self, path: str = "prompts.json"):
        self.path = path
        self.prompts: Dict[str, List[dict]] = {}
        if os.path.exists(self.path):
            self._load()

    # ------------------------------------------------------------------
    # Persistence helpers
    def _load(self) -> None:
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            for name, versions in data.items():
                if isinstance(versions, list):
                    self.prompts[name] = versions
        except (json.JSONDecodeError, OSError):
            self.prompts = {}

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(self.prompts, fh, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Public API
    def add(self, name: str, prompt: str, meta: Optional[dict] = None) -> dict:
        meta = meta or {}
        record = {
            "text": prompt,
            "meta": meta,
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        self.prompts.setdefault(name, []).append(record)
        self.save()
        return record

    def get(self, name: str) -> Optional[dict]:
        versions = self.prompts.get(name)
        if not versions:
            return None
        return versions[-1]

    def history(self, name: str) -> List[dict]:
        return list(self.prompts.get(name, []))

    def search(self, query: str) -> List[dict]:
        """Простой полнотекстовый поиск по тексту и тегам."""
        q = query.lower()
        results = []
        for name, versions in self.prompts.items():
            for version in versions:
                text = version.get("text", "").lower()
                tags = " ".join(version.get("meta", {}).get("tags", [])).lower()
                if q in text or q in tags or q in name.lower():
                    enriched = dict(version)
                    enriched["name"] = name
                    results.append(enriched)
        return results

    def tagged(self, tag: str) -> List[dict]:
        tag_lower = tag.lower()
        return [
            dict(version, name=name)
            for name, versions in self.prompts.items()
            for version in versions
            if tag_lower in (t.lower() for t in version.get("meta", {}).get("tags", []))
        ]

    def export(self, path: str) -> None:
        """Экспорт репозитория в указанный путь без изменения основного файла."""
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.prompts, fh, ensure_ascii=False, indent=2)
