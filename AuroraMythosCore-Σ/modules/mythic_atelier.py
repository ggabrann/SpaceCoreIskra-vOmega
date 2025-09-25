"""Hybrid analytic engine producing structured drafts."""
from __future__ import annotations

from typing import List, Dict, Any


class MythicAtelier:
    def analyze(self, query: str, prompt: str, knowledge: List[Dict[str, str]]) -> Dict[str, Any]:
        facts = [doc["text"] for doc in knowledge]
        return {
            "query": query,
            "prompt": prompt,
            "facts": facts,
            "summary": self._summarize(facts),
            "insights": self._derive_insights(facts),
        }

    def _summarize(self, facts: List[str]) -> str:
        if not facts:
            return "Недостаточно данных — требуется внешнее подключение."
        return " | ".join(facts[:3])

    def _derive_insights(self, facts: List[str]) -> List[str]:
        return [f"Insight #{idx + 1}: {fact[:120]}" for idx, fact in enumerate(facts[:3])]
