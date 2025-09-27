"""Persona registry used by GrokCoreIskra vΓ."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple


@dataclass
class Persona:
    name: str
    keywords: List[str]
    tone: str = "neutral"

    def affinity(self, query_tokens: Iterable[str]) -> int:
        tokens = set(query_tokens)
        return sum(1 for keyword in self.keywords if keyword in tokens)


class PersonaRegistry:
    def __init__(self) -> None:
        self._personas: Dict[str, Persona] = {}

    def register(self, name: str, keywords: Iterable[str], *, tone: str = "neutral") -> Persona:
        persona = Persona(name=name, keywords=[kw.lower() for kw in keywords], tone=tone)
        self._personas[name] = persona
        return persona

    def match(self, query: str) -> List[Tuple[Persona, int]]:
        tokens = {token for token in query.lower().split() if token}
        scored = [
            (persona, persona.affinity(tokens))
            for persona in self._personas.values()
        ]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [item for item in scored if item[1] > 0] or scored[:1]


__all__ = ["Persona", "PersonaRegistry"]
