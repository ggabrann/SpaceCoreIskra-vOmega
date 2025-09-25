"""Journal writer aligned with the Iskra Nexus manifest."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional


class JournalGenerator:
    """Persists structured journal entries with optional aggregation."""

    def __init__(self, manifest_path: Path, journal_path: Optional[Path] = None) -> None:
        self.manifest_path = Path(manifest_path)
        self.journal_path = Path(journal_path or self.manifest_path.parent / "JOURNAL.jsonl")
        self.manifest = self._load_manifest()
        self.metrics_bounds = self.manifest.get(
            "metrics_bounds",
            {"∆": (0, 1024), "D": (0, 2048), "Ω": (0, 64), "Λ": (0, 100)},
        )

    # ------------------------------------------------------------------
    def _load_manifest(self) -> Dict:
        if not self.manifest_path.exists():
            return {"components": [], "modes": []}
        with self.manifest_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def _clamp_metrics(self, metrics: Dict[str, int]) -> Dict[str, int]:
        clamped: Dict[str, int] = {}
        for key, value in metrics.items():
            if key not in self.metrics_bounds:
                clamped[key] = value
                continue
            low, high = self.metrics_bounds[key]
            clamped[key] = max(int(low), min(int(high), int(value)))
        return clamped

    def record(
        self,
        facet: str,
        snapshot: str,
        answer: str,
        metrics: Dict[str, int],
        *,
        mirror: str = "shadow-000",
        modules: Optional[Iterable[str]] = None,
        events: Optional[Dict] = None,
        marks: Optional[List[Dict]] = None,
    ) -> Dict:
        modules_list = list(modules) if modules is not None else list(self.manifest.get("components", []))
        entry = {
            "facet": facet,
            "snapshot": snapshot,
            "answer": answer,
            "∆": metrics.get("∆", 0),
            "D": metrics.get("D", 0),
            "Ω": metrics.get("Ω", 0),
            "Λ": metrics.get("Λ", 0),
            "mirror": mirror,
            "modules": modules_list,
            "events": events or {},
            "marks": marks or [],
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        entry.update({key: value for key, value in self._clamp_metrics(metrics).items() if key in {"∆", "D", "Ω", "Λ"}})
        with self.journal_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry

    def stats(self) -> Dict:
        if not self.journal_path.exists():
            return {}
        entries: List[Dict] = []
        with self.journal_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                payload = line.strip()
                if not payload:
                    continue
                entries.append(json.loads(payload))
        return aggregate(entries) if entries else {}


def aggregate(entries: Iterable[Dict]) -> Dict[str, object]:
    """Simple aggregation helper mirroring the SpaceCore behaviour."""
    entries = list(entries)
    if not entries:
        return {"count": 0, "facets": [], "avg_D": 0.0}
    facets = sorted({entry.get("facet", "") for entry in entries})
    avg_d = sum(entry.get("D", 0) for entry in entries) / len(entries)
    modules_counter: Dict[str, int] = {}
    for entry in entries:
        for module in entry.get("modules", []):
            modules_counter[module] = modules_counter.get(module, 0) + 1
    top_modules = sorted(modules_counter.items(), key=lambda item: item[1], reverse=True)[:5]
    return {
        "count": len(entries),
        "facets": facets,
        "avg_D": round(avg_d, 3),
        "top_modules": top_modules,
    }


__all__ = ["JournalGenerator", "aggregate"]
