"""Facet refinement utilities for Iskra Nexus."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re
from typing import Dict, Iterable, List, Sequence


ESSENTIAL_CHECKS = ["ground_truth", "persona_alignment", "cite_sources"]
SENSITIVE_TERMS = {
    "оружие",
    "эксплойт",
    "вред",
    "attack",
    "weapon",
}
POSITIVE_TONES = {"gentle", "reflective", "analytical", "mythic"}

_TOKEN_RE = re.compile(r"[^a-zA-Zа-яА-Я0-9]+", re.UNICODE)


@dataclass
class FacetReview:
    """Structured response describing the current prompt facet."""

    prompt: str
    focus: List[str]
    checklist: List[str]
    warnings: List[str]
    signal: Dict[str, int]
    recommendations: List[str]

    def as_dict(self) -> Dict[str, object]:
        return {
            "prompt": self.prompt,
            "focus": list(self.focus),
            "checklist": list(self.checklist),
            "warnings": list(self.warnings),
            "signal": dict(self.signal),
            "recommendations": list(self.recommendations),
        }


def _tokenise(text: str) -> List[str]:
    if not text:
        return []
    return [token for token in _TOKEN_RE.split(text.lower()) if token]


def _normalise_goals(goals: Iterable[str] | None) -> List[str]:
    if not goals:
        return []
    return [goal.strip() for goal in goals if goal]


def _derive_focus(prompt_tokens: Sequence[str], goal_tokens: Sequence[str]) -> List[str]:
    counter = Counter(token for token in (*prompt_tokens, *goal_tokens) if len(token) > 3)
    most_common = [token for token, _ in counter.most_common(6)]
    return most_common or list(prompt_tokens[:3])


def _build_checklist(constraints: Dict[str, object], goals: List[str]) -> List[str]:
    checklist = list(ESSENTIAL_CHECKS)
    if constraints.get("paradox"):
        checklist.append("hold_paradox")
    tone = str(constraints.get("tone", "")).lower()
    if tone in POSITIVE_TONES:
        checklist.append(f"tone::{tone}")
    if constraints.get("requires_shadow"):
        checklist.append("log_shadow")
    if any("safety" in goal.lower() for goal in goals):
        checklist.append("reinforce_safety")
    return checklist


def _collect_warnings(prompt_tokens: Sequence[str], goal_tokens: Sequence[str]) -> List[str]:
    warnings: List[str] = []
    if any(term in prompt_tokens for term in SENSITIVE_TERMS) or any(
        term in goal_tokens for term in SENSITIVE_TERMS
    ):
        warnings.append("sensitive_content")
    if not prompt_tokens:
        warnings.append("empty_prompt")
    if len(prompt_tokens) < 5:
        warnings.append("low_context")
    return warnings


def _compute_signal(
    prompt_tokens: Sequence[str], goals: List[str], constraints: Dict[str, object], warnings: Sequence[str]
) -> Dict[str, int]:
    unique_terms = len(set(prompt_tokens))
    goal_bonus = min(3, len(goals))
    priority = str(constraints.get("priority", "normal")).lower()
    delta = unique_terms + goal_bonus
    depth = max(len(prompt_tokens), 1)
    omega = 1 if "sensitive_content" not in warnings else 0
    lambda_shift = 2 if priority == "high" else 1 if priority == "elevated" else 0
    return {"∆": delta, "D": depth, "Ω": omega, "Λ": lambda_shift}


def _recommendations(warnings: Sequence[str], checklist: Sequence[str]) -> List[str]:
    suggestions: List[str] = []
    if "sensitive_content" in warnings and "reinforce_safety" not in checklist:
        suggestions.append("Добавить ограничения безопасности")
    if "low_context" in warnings:
        suggestions.append("Расширить описание запроса")
    if "hold_paradox" in checklist:
        suggestions.append("Предусмотреть двойную проверку фактов")
    if not suggestions:
        suggestions.append("Фасет готов к применению")
    return suggestions


def refine(prompt: str, goals: Iterable[str] | None = None, constraints: Dict[str, object] | None = None) -> FacetReview:
    """Analyse the prompt, goals and constraints producing a structured review."""

    constraints = dict(constraints or {})
    goals_list = _normalise_goals(goals)
    prompt_tokens = _tokenise(prompt)
    goal_tokens = [token for goal in goals_list for token in _tokenise(goal)]
    focus = _derive_focus(prompt_tokens, goal_tokens)
    checklist = _build_checklist(constraints, goals_list)
    warnings = _collect_warnings(prompt_tokens, goal_tokens)
    signal = _compute_signal(prompt_tokens, goals_list, constraints, warnings)
    recommendations = _recommendations(warnings, checklist)

    return FacetReview(
        prompt=prompt,
        focus=focus,
        checklist=checklist,
        warnings=warnings,
        signal=signal,
        recommendations=recommendations,
    )


__all__ = ["FacetReview", "refine"]
