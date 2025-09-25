import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .ci_aggregate import aggregate

BASE_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = BASE_DIR / "MANIFEST_vΩ.json"


def _load_bounds() -> Dict[str, List[int]]:
    if not MANIFEST_PATH.exists():
        return {}
    with MANIFEST_PATH.open("r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    return manifest.get("metrics_bounds", {})


METRIC_BOUNDS = _load_bounds()


def _clamp_metrics(metrics: Dict[str, int]) -> Dict[str, int]:
    clamped = {}
    for key, value in metrics.items():
        if key not in METRIC_BOUNDS:
            clamped[key] = value
            continue
        low, high = METRIC_BOUNDS[key]
        clamped[key] = max(low, min(high, value))
    return clamped


def gen(
    facet: str,
    snap: str,
    ans: str,
    metrics: Dict[str, int],
    mirror: str = "shadow-000",
    modules: Optional[List[str]] = None,
    events: Optional[Dict] = None,
    marks: Optional[List[Dict]] = None,
    path: str = "JOURNAL.jsonl",
) -> Dict:
    metrics = _clamp_metrics(metrics)
    entry = {
        "facet": facet,
        "snapshot": snap,
        "answer": ans,
        "∆": metrics.get("∆", 0),
        "D": metrics.get("D", 0),
        "Ω": metrics.get("Ω", 0),
        "Λ": metrics.get("Λ", 0),
        "mirror": mirror,
        "modules": modules or [],
        "events": events or {},
        "marks": marks or [],
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    with (BASE_DIR / path).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def stats(path: str = "JOURNAL.jsonl") -> Dict:
    journal_path = BASE_DIR / path
    if not journal_path.exists():
        return {}
    entries = []
    with journal_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                entries.append(json.loads(line))
    return aggregate(entries)
