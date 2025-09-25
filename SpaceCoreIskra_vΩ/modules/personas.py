from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set, Tuple


@dataclass
class Persona:
    name: str
    concepts: Set[str]
    tone: str = "neutral"
    focus: Optional[str] = None

    def distance(self, other: "Persona") -> float:
        union = self.concepts | other.concepts
        if not union:
            return 0.0
        return 1.0 - len(self.concepts & other.concepts) / len(union)


@dataclass
class PersonaRegistry:
    personas: Dict[str, Persona] = field(default_factory=dict)

    def register(self, name: str, concepts: Iterable[str], tone: str = "neutral", focus: Optional[str] = None) -> Persona:
        persona = Persona(name=name, concepts=set(concepts), tone=tone, focus=focus)
        self.personas[name] = persona
        return persona

    def get(self, name: str) -> Optional[Persona]:
        return self.personas.get(name)

    def match(self, concepts: Iterable[str], top_k: int = 3) -> List[Tuple[Persona, float]]:
        query = Persona(name="__query__", concepts=set(concepts))
        scored = [
            (persona, persona.distance(query))
            for persona in self.personas.values()
        ]
        scored.sort(key=lambda item: item[1])
        return scored[:top_k]

    def complementary_pairs(self, threshold: float = 0.5) -> List[Tuple[Persona, Persona, float]]:
        pairs: List[Tuple[Persona, Persona, float]] = []
        items = list(self.personas.values())
        for idx, persona in enumerate(items):
            for other in items[idx + 1 :]:
                dist = persona.distance(other)
                if dist >= threshold:
                    pairs.append((persona, other, dist))
        return pairs
