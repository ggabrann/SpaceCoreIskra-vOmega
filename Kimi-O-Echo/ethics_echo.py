"""Ethics utilities for Kimi-Ω-Echo."""

from __future__ import annotations

from dataclasses import dataclass

from common.ethics_core import is_allowed
from SpaceCoreIskra_vΩ.modules.veil import check as veil_check


@dataclass(slots=True)
class Verdict:
    allowed: bool
    reasons: tuple[str, ...]


def evaluate(message: str) -> Verdict:
    """Return a :class:`Verdict` for ``message``."""

    reasons: list[str] = []
    if not veil_check(message or ""):
        reasons.append("veil")
    if not is_allowed(message or ""):
        reasons.append("ethics")
    return Verdict(allowed=not reasons, reasons=tuple(reasons))


def check(message: str) -> bool:
    """Backward compatible boolean helper."""

    return evaluate(message).allowed
