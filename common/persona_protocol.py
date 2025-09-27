from __future__ import annotations

from collections.abc import Iterable


class ConceptSet:
    def __init__(self, items: Iterable[str] | None) -> None:
        self.items = set(items or [])

    def distance(self, other: "ConceptSet") -> float:
        union = len(self.items | other.items)
        intersection = len(self.items & other.items)
        return 0.0 if union == 0 else 1 - intersection / union


class PersonaSpec:
    def __init__(self, name: str, concepts: Iterable[str], traits: dict | None = None) -> None:
        self.name = name
        self.concepts = ConceptSet(concepts)
        self.traits = traits or {}
