from collections import Counter
from statistics import mean
from typing import Dict, Iterable


def aggregate(entries: Iterable[dict]) -> Dict[str, object]:
    entries = list(entries)
    if not entries:
        return {"count": 0, "facets": [], "avg_D": 0.0}

    facets = [e.get("facet") for e in entries]
    avg_d = mean(e.get("D", 0) for e in entries)
    veil_hits = sum(1 for e in entries if e.get("events", {}).get("veil_triggered"))

    return {
        "count": len(entries),
        "facets": sorted(set(facets)),
        "avg_D": round(avg_d, 3),
        "veil_trigger_rate": round(veil_hits / len(entries), 3),
        "top_modules": Counter(mod for e in entries for mod in e.get("modules", []))
        .most_common(5),
    }
