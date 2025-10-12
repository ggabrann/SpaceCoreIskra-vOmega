"""Persona management for SpaceCore Iskra vΩ.

The previous placeholder exposed only a bare ``distance`` helper.  The Nexus
stack requires richer metadata in order to select the best persona for a given
request.  This module introduces a registry with tone and paradox awareness plus
keyword heuristics that support the CRISIS protocol metrics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping, Sequence

from common.persona_protocol import ConceptSet


def _normalise_keywords(keywords: Iterable[str]) -> frozenset[str]:
    return frozenset(keyword.strip().lower() for keyword in keywords if keyword.strip())


@dataclass(frozen=True, slots=True)
class Persona:
    """Rich persona representation with similarity scoring."""

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
        """Return a normalised similarity score in the ``[0, 1]`` range."""

        score = 0.0

        if concepts is not None:
            concept_set = ConceptSet(concepts)
            score += 0.5 * (1 - self.concepts.distance(concept_set))

        if query:
            lowered = set(query.lower().split())
            if self.keywords:
                overlap = len(self.keywords & lowered) / len(self.keywords)
                score += 0.3 * overlap

        if tone:
            tone_score = 1.0 if tone.lower() == self.tone.lower() else 0.0
            score += 0.1 * tone_score

        if paradox is not None:
            # Treat paradox_bias as the preferred value in [-1, 1].
            delta = max(0.0, 1 - min(1.0, abs(paradox - self.paradox_bias)))
            score += 0.1 * delta

        return min(score, 1.0)


class PersonaRegistry:
    """Mutable registry used by routers and evaluators."""

    def __init__(self, personas: Sequence[Persona] | None = None) -> None:
        self._personas: list[Persona] = list(personas or [])

    def register(self, persona: Persona) -> None:
        self._personas = [p for p in self._personas if p.name != persona.name]
        self._personas.append(persona)

    def resolve(
        self,
        *,
        concepts: Iterable[str] | None = None,
        query: str | None = None,
        tone: str | None = None,
        paradox: float | None = None,
    ) -> Persona:
        if not self._personas:
            raise LookupError("persona registry is empty")

        scored = [
            (
                persona.score(
                    concepts=concepts,
                    query=query,
                    tone=tone,
                    paradox=paradox,
                ),
                persona,
            )
            for persona in self._personas
        ]

        scored.sort(key=lambda item: item[0], reverse=True)
        best_score, persona = scored[0]
        if best_score == 0:
            # When nothing matches, fall back to the first registered persona to
            # retain deterministic behaviour.
            return self._personas[0]
        return persona

    def all(self) -> Sequence[Persona]:
        return tuple(self._personas)


DEFAULT_PERSONAS = (
    Persona(
        name="Куратор Кристалла",
        concepts=ConceptSet({"safety", "veil", "ethics", "∆"}),
        tone="calm",
        paradox_bias=-0.2,
        keywords=_normalise_keywords(["безопасность", "этика", "guardrails"]),
        traits={"role": "safety", "focus": "stability"},
    ),
    Persona(
        name="Проводник Парадокса",
        concepts=ConceptSet({"paradox", "synthesis", "Ω", "Λ"}),
        tone="playful",
        paradox_bias=0.8,
        keywords=_normalise_keywords(["парадокс", "контрапункт", "синтез"]),
        traits={"role": "exploration", "focus": "innovation"},
    ),
    Persona(
        name="Летописец Искры",
        concepts=ConceptSet({"journal", "∆", "chronicle", "anchor"}),
        tone="reflective",
        paradox_bias=0.0,
        keywords=_normalise_keywords(["журнал", "запись", "shadow"]),
        traits={"role": "documentation", "focus": "traceability"},
    ),
    Persona(
        name="Архитектор Синтеза",
        concepts=ConceptSet({"analysis", "plan", "facets", "roadmap"}),
        tone="analytical",
        paradox_bias=0.3,
        keywords=_normalise_keywords(["план", "структура", "facets"]),
        traits={"role": "planning", "focus": "structure"},
    ),
)

REGISTRY = PersonaRegistry(DEFAULT_PERSONAS)


def select_persona(
    *,
    concepts: Iterable[str] | None = None,
    query: str | None = None,
    tone: str | None = None,
    paradox: float | None = None,
) -> Persona:
    """Convenience wrapper that proxies to :class:`PersonaRegistry`."""

    return REGISTRY.resolve(concepts=concepts, query=query, tone=tone, paradox=paradox)

