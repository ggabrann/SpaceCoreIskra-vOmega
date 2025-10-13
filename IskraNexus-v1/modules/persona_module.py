"""Persona registry for Iskra Nexus."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping, Sequence

from common.persona_protocol import ConceptSet


def _normalise_keywords(keywords: Iterable[str]) -> frozenset[str]:
    return frozenset(keyword.strip().lower() for keyword in keywords if keyword.strip())


@dataclass(frozen=True, slots=True)
class PersonaProfile:
    name: str
    concepts: ConceptSet
    tone: str = "neutral"
    paradox_bias: float = 0.0
    keywords: frozenset[str] = field(default_factory=frozenset)
    traits: Mapping[str, str] = field(default_factory=dict)

    def score(
        self,
        *,
        concepts: Iterable[str] | None = None,
        query: str | None = None,
        tone: str | None = None,
        paradox: float | None = None,
    ) -> float:
        score = 0.0

        if concepts is not None:
            target = ConceptSet(concepts)
            score += 0.5 * (1 - self.concepts.distance(target))

        if query:
            query_terms = set(query.lower().split())
            if self.keywords:
                overlap = len(self.keywords & query_terms) / max(len(self.keywords), 1)
                score += 0.3 * overlap

        if tone:
            score += 0.1 if tone.lower() == self.tone.lower() else 0.0

        if paradox is not None:
            delta = 1 - min(1.0, abs(paradox - self.paradox_bias))
            score += 0.1 * max(0.0, delta)

        return min(score, 1.0)


class PersonaRegistry:
    def __init__(self, personas: Sequence[PersonaProfile] | None = None) -> None:
        self._personas: list[PersonaProfile] = list(personas or [])

    def register(self, persona: PersonaProfile) -> None:
        self._personas = [existing for existing in self._personas if existing.name != persona.name]
        self._personas.append(persona)

    def resolve(
        self,
        *,
        concepts: Iterable[str] | None = None,
        query: str | None = None,
        tone: str | None = None,
        paradox: float | None = None,
    ) -> PersonaProfile:
        if not self._personas:
            raise LookupError("persona registry is empty")

        scored = [
            (
                persona.score(concepts=concepts, query=query, tone=tone, paradox=paradox),
                persona,
            )
            for persona in self._personas
        ]
        scored.sort(key=lambda item: item[0], reverse=True)
        best_score, persona = scored[0]
        return persona if best_score > 0 else self._personas[0]

    def all(self) -> Sequence[PersonaProfile]:
        return tuple(self._personas)


DEFAULT_PERSONAS = (
    PersonaProfile(
        name="Куратор", concepts=ConceptSet({"safety", "veil", "ethics"}), tone="calm", paradox_bias=-0.2,
        keywords=_normalise_keywords(["safety", "veil", "guardrails"]), traits={"role": "safety"},
    ),
    PersonaProfile(
        name="Хронист", concepts=ConceptSet({"journal", "anchor", "∆"}), tone="reflective", paradox_bias=0.0,
        keywords=_normalise_keywords(["журнал", "anchor", "shadow"]), traits={"role": "documentation"},
    ),
    PersonaProfile(
        name="Стратег", concepts=ConceptSet({"plan", "roadmap", "Λ"}), tone="analytical", paradox_bias=0.3,
        keywords=_normalise_keywords(["план", "roadmap", "milestone"]), traits={"role": "planning"},
    ),
)

REGISTRY = PersonaRegistry(DEFAULT_PERSONAS)


def select_persona(
    *,
    concepts: Iterable[str] | None = None,
    query: str | None = None,
    tone: str | None = None,
    paradox: float | None = None,
) -> PersonaProfile:
    return REGISTRY.resolve(concepts=concepts, query=query, tone=tone, paradox=paradox)
