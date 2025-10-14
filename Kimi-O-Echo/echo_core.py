"""Core echo processing primitives for Kimi-Ω-Echo."""

from __future__ import annotations

from typing import Iterable, List

from .ethics_echo import evaluate
from .veil_echo import apply_veil


def process_echo(messages: Iterable[str], window: int = 3, *, veil: bool = True) -> List[str]:
    """Return the recent echo messages after guardrail checks."""

    recent = list(messages or [])[-int(max(window, 0)) :]
    safe: list[str] = []
    for message in recent:
        verdict = evaluate(message)
        if not verdict.allowed:
            continue
        safe.append(apply_veil(message) if veil else message)
    return safe
