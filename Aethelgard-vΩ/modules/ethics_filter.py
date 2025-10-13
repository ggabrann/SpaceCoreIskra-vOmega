"""Ethics and veil coordination utilities for Aethelgard."""

from __future__ import annotations

from dataclasses import dataclass

from common.ethics_core import is_allowed
from SpaceCoreIskra_vΩ.modules.veil import check as veil_check


@dataclass(slots=True)
class EthicsReport:
    allowed: bool
    reasons: tuple[str, ...]


def evaluate(text: str) -> EthicsReport:
    """Return an :class:`EthicsReport` for ``text``."""

    reasons: list[str] = []
    if not veil_check(text or ""):
        reasons.append("veil")
    if not is_allowed(text or ""):
        reasons.append("ethics")
    return EthicsReport(allowed=not reasons, reasons=tuple(reasons))


def filter_text(text: str) -> bool:
    """Backward compatible boolean helper."""

    return evaluate(text).allowed
