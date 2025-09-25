"""Collects metrics and produces CI-style reports."""
from __future__ import annotations

from typing import Dict, Any, List


class PulseAnalyzer:
    def __init__(self) -> None:
        self.entries: List[Dict[str, Any]] = []

    def initial_metrics(self, mode: str, psi_bias: int) -> Dict[str, int]:
        base = {
            "AXIOM": {"∆": 0, "D": 6, "Ω": 2, "Λ": 1, "Ψ": 1},
            "PARABLE": {"∆": 1, "D": 4, "Ω": 2, "Λ": 3, "Ψ": 3},
            "MYTHOS": {"∆": 2, "D": 3, "Ω": 1, "Λ": 4, "Ψ": 5},
        }
        metrics = base.get(mode, base["PARABLE"]).copy()
        metrics["Ψ"] = min(6, metrics["Ψ"] + psi_bias)
        return metrics

    def register(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        self.entries.append(entry)
        totals = {key: 0 for key in ["∆", "D", "Ω", "Λ", "Ψ"]}
        for record in self.entries:
            for key in totals:
                totals[key] += record.get(key, 0)
        count = len(self.entries)
        averages = {key: round(totals[key] / max(count, 1), 2) for key in totals}
        return {
            "count": count,
            "averages": averages,
            "shadow_ratio": self._shadow_ratio(),
        }

    def _shadow_ratio(self) -> float:
        shadow_entries = [entry for entry in self.entries if entry.get("events", {}).get("reason") == "shadow"]
        if not self.entries:
            return 0.0
        return round(len(shadow_entries) / len(self.entries), 2)
