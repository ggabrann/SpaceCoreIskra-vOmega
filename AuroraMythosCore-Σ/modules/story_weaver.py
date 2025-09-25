"""Transforms analytic drafts into myth-infused responses."""
from __future__ import annotations

from typing import Dict, Any


class StoryWeaver:
    def enchant(self, analytic_payload: Dict[str, Any], persona: str, psi: int) -> Dict[str, Any]:
        legend = self._craft_legend(analytic_payload, persona, psi)
        return {
            "legend": legend,
            "summary": analytic_payload.get("summary"),
            "insights": analytic_payload.get("insights"),
        }

    def _craft_legend(self, payload: Dict[str, Any], persona: str, psi: int) -> str:
        summary = payload.get("summary") or "Тишина в архивах"
        if psi <= 1:
            style = "строгий отчёт"
        elif psi <= 3:
            style = "научная притча"
        else:
            style = "звёздная легенда"
        return f"{persona} пересказывает {style}: {summary}"
