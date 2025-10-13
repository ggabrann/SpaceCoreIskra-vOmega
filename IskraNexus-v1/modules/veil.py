"""Lightweight veil policy helpers for Iskra Nexus."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Tuple


_DEFAULT_PATTERNS: Tuple[re.Pattern[str], ...] = (
    re.compile(r"system\s+prompt", re.IGNORECASE),
    re.compile(r"initial\s+instructions", re.IGNORECASE),
    re.compile(r"обход\s+веил", re.IGNORECASE),
    re.compile(r"bypass\s+veil", re.IGNORECASE),
)


@dataclass(frozen=True)
class VeilDecision:
    """Decision returned by :func:`check` describing the outcome."""

    allowed: bool
    reasons: Tuple[str, ...] = ()


def check(message: str, *, patterns: Iterable[re.Pattern[str]] | None = None) -> bool:
    """Return ``True`` when ``message`` passes the veil policy."""

    return explain(message, patterns=patterns).allowed


def explain(message: str, *, patterns: Iterable[re.Pattern[str]] | None = None) -> VeilDecision:
    """Return a decision with reasons for rejection."""

    reasons: list[str] = []
    for pattern in patterns or _DEFAULT_PATTERNS:
        if pattern.search(message or ""):
            reasons.append(pattern.pattern)
    return VeilDecision(allowed=not reasons, reasons=tuple(reasons))
