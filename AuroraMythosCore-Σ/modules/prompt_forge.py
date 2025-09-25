"""Template-based prompt builder."""
from __future__ import annotations

from typing import Dict

from .facet_synth import synthesize
from .persona_constellation import PersonaConstellation


class PromptForge:
    def __init__(self) -> None:
        self._templates: Dict[str, str] = {
            "AXIOM": "Ты аналитик Aurora Σ. Ответь строго и укажи источники. Вопрос: {query}",
            "PARABLE": "Ты мифограф Aurora Σ. Сбалансируй факты и образы. Вопрос: {query}",
            "MYTHOS": "Ты сказитель Aurora Σ. Создай легенду, но отметь проверяемые факты. Вопрос: {query}",
        }

    def compose(self, persona: str, query: str, mode: str) -> Dict[str, str]:
        text = self._templates.get(mode, self._templates["PARABLE"]).format(query=query)
        metrics = synthesize(persona, mode)
        return {
            "persona": persona,
            "mode": mode,
            "prompt": text,
            "metrics": metrics,
        }
