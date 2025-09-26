"""Memory pipeline utilities for Танцующая Нить."""
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Iterable, List, Dict, Any


def summarize_entries(entries: Iterable[Dict[str, Any]]) -> List[str]:
    """Return distilled insights: first sentence + energy/focus markers."""
    insights: List[str] = []
    for entry in entries:
        text = entry.get("note", "").strip()
        if not text:
            continue
        head = text.split(".")[0]
        energy = entry.get("energy")
        focus = entry.get("focus")
        markers = []
        if energy is not None:
            markers.append(f"E{energy}")
        if focus is not None:
            markers.append(f"F{focus}")
        tail = f" [{' '.join(markers)}]" if markers else ""
        insights.append(f"{head}{tail}")
    return insights


def schedule_reviews(entry_date: str) -> List[str]:
    """Return spaced repetition checkpoints (ISO dates)."""
    base = datetime.fromisoformat(entry_date)
    return [(base + timedelta(days=delta)).date().isoformat() for delta in (3, 7, 21)]


def run_pipeline(source: Path, destination: Path) -> None:
    """Load JSONL entries, summarise, and export review schedule."""
    with source.open(encoding="utf-8") as handle:
        entries = [json.loads(line) for line in handle if line.strip()]
    summary = summarize_entries(entries)
    schedule_map = {
        item.get("date"): schedule_reviews(item["date"]) for item in entries if "date" in item
    }
    payload = {"summary": summary, "schedule": schedule_map}
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
