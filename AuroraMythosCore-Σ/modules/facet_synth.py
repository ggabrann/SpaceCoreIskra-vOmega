"""Combines persona biases with prompt goals."""
from __future__ import annotations

from typing import Dict


def synthesize(persona: str, mode: str) -> Dict[str, int]:
    base = {
        "AXIOM": {"∆": 0, "D": 6, "Ω": 2, "Λ": 1, "Ψ": 1},
        "PARABLE": {"∆": 1, "D": 4, "Ω": 2, "Λ": 2, "Ψ": 3},
        "MYTHOS": {"∆": 2, "D": 3, "Ω": 1, "Λ": 4, "Ψ": 5},
    }
    metrics = base.get(mode, base["PARABLE"]).copy()
    if persona == "Проводник Мифа":
        metrics["Ψ"] = min(6, metrics["Ψ"] + 1)
    if persona == "Люминарий":
        metrics["D"] = min(9, metrics["D"] + 2)
    if persona == "Хронист Теней":
        metrics["Ω"] = max(-3, metrics["Ω"] - 1)
    return metrics
