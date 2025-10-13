"""Paradox splitting helpers for Kimi-Ω-Echo."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence

from .ethics_echo import evaluate

_SPLIT_REGEX = re.compile(r"[.!?]+\s*", re.MULTILINE)


@dataclass(slots=True)
class SplitResult:
    fragments: Sequence[str]
    flagged: Sequence[str]


def split(text: str) -> SplitResult:
    """Split ``text`` while flagging unsafe fragments."""

    parts = [part.strip() for part in _SPLIT_REGEX.split(text or "") if part.strip()]
    fragments: list[str] = []
    flagged: list[str] = []
    for part in parts:
        verdict = evaluate(part)
        if verdict.allowed:
            fragments.append(part)
        else:
            flagged.append(part)
    return SplitResult(fragments=tuple(fragments), flagged=tuple(flagged))
