"""Persona graph with context-sensitive selection."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Persona:
    name: str
    keywords: List[str]
    psi_bias: int


class PersonaConstellation:
    def __init__(self) -> None:
        self._personas: List[Persona] = [
            Persona("Люминарий", ["анализ", "статистика", "исследование"], psi_bias=1),
            Persona("Проводник Мифа", ["история", "легенда", "миф"], psi_bias=4),
            Persona("Хронист Теней", ["риск", "уязвимость", "этика"], psi_bias=2),
            Persona("Архитектор Σ", ["архитектура", "код", "проект"], psi_bias=0),
        ]

    def select_persona(self, query: str) -> str:
        q = query.lower()
        for persona in self._personas:
            if any(token in q for token in persona.keywords):
                return persona.name
        return self._personas[0].name

    def get_bias(self, name: str) -> int:
        for persona in self._personas:
            if persona.name == name:
                return persona.psi_bias
        return 0
