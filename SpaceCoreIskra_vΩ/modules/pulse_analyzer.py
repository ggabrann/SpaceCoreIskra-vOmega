from statistics import mean, pstdev
from typing import Dict, Iterable


class PulseAnalyzer:
    def summarize(self, entries: Iterable[dict]) -> Dict[str, Dict[str, float]]:
        entries = list(entries)
        if not entries:
            return {}
        result: Dict[str, Dict[str, float]] = {}
        for key in ("∆", "D", "Ω", "Λ"):
            values = [entry.get(key, 0) for entry in entries]
            if not values:
                continue
            result[key] = {
                "avg": round(mean(values), 3),
                "min": min(values),
                "max": max(values),
                "stdev": round(pstdev(values), 3) if len(values) > 1 else 0.0,
            }
        return result

    def stability_flag(self, summary: Dict[str, Dict[str, float]], bounds: Dict[str, tuple]) -> bool:
        for key, metrics in summary.items():
            low, high = bounds.get(key, (-999, 999))
            if not (low <= metrics["avg"] <= high):
                return False
        return True
