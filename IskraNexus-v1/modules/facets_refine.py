"""Facet refinement helpers for ∆/D/Ω/Λ metrics."""
from __future__ import annotations


from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class FacetSnapshot:
    delta: float
    data: float
    omega: float
    lambda_: float

    def clamp(self, min_value: float = -3.0, max_value: float = 3.0) -> "FacetSnapshot":
        return FacetSnapshot(
            delta=_clamp(self.delta, min_value, max_value),
            data=_clamp(self.data, min_value, max_value),
            omega=_clamp(self.omega, min_value, max_value),
            lambda_=_clamp(self.lambda_, min_value, max_value),
        )

    def as_dict(self) -> Mapping[str, float]:
        return {"∆": self.delta, "D": self.data, "Ω": self.omega, "Λ": self.lambda_}


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))



DEFAULT_RULES: Mapping[str, Mapping[str, float]] = {
    "stability": {"∆": 0.2, "Λ": 0.1},
    "risk": {"∆": -0.3, "Ω": -0.2},
    "innovation": {"Ω": 0.3, "D": 0.2},
    "documentation": {"D": 0.3, "Λ": 0.2},
}


def refine(snapshot: FacetSnapshot, *, feedback: Sequence[str] | None = None) -> FacetSnapshot:
    """Apply keyword-driven adjustments and clamp the result."""

    adjustments = {"∆": 0.0, "D": 0.0, "Ω": 0.0, "Λ": 0.0}
    tokens = feedback or []
    for token in tokens:
        deltas = DEFAULT_RULES.get(token.lower())
        if not deltas:
            continue
        for key, delta in deltas.items():
            adjustments[key] += delta

    refined = FacetSnapshot(
        delta=snapshot.delta + adjustments["∆"],
        data=snapshot.data + adjustments["D"],
        omega=snapshot.omega + adjustments["Ω"],
        lambda_=snapshot.lambda_ + adjustments["Λ"],
    )
    return refined.clamp()


def from_metrics(metrics: Mapping[str, float]) -> FacetSnapshot:
    return FacetSnapshot(
        delta=float(metrics.get("∆", 0.0)),
        data=float(metrics.get("D", 0.0)),
        omega=float(metrics.get("Ω", 0.0)),
        lambda_=float(metrics.get("Λ", 0.0)),
    )
