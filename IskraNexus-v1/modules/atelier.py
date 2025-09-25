"""Semantic atelier utilities."""
from __future__ import annotations

from typing import Dict


def score(text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    long_words = [w for w in words if len(w) > 6]
    return len(long_words) / len(words)


def critique(prompt: str, answer: str) -> Dict[str, float]:
    prompt_len = len(prompt.split())
    answer_len = len(answer.split())
    density = score(answer)
    balance = answer_len / prompt_len if prompt_len else 0
    return {
        "prompt_len": prompt_len,
        "answer_len": answer_len,
        "semantic_density": round(density, 3),
        "balance_ratio": round(balance, 3),
    }


def recommend(density: float) -> str:
    if density < 0.15:
        return "Добавить конкретики и фактов"
    if density > 0.35:
        return "Разбавить метафоры примерами"
    return "Баланс в норме"


__all__ = ["score", "critique", "recommend"]
