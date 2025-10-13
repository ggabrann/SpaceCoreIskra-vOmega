"""Ethics and veil enforcement utilities for Iskra Nexus."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

from common.ethics_core import is_allowed

from .veil import explain as veil_explain


@dataclass(frozen=True)
class ModerationDecision:
    """Represents the result of an ethics moderation pass."""

    allowed: bool
    reasons: Tuple[str, ...] = ()


class EthicsLayer:
    """Combine veil filters, ethics keywords, and project guardrails."""

    def __init__(self, guardrails: Iterable[str] | None = None) -> None:
        self._guardrails = tuple(guardrails or ())

    def review(self, text: str) -> ModerationDecision:
        reasons: list[str] = []

        veil_decision = veil_explain(text)
        if not veil_decision.allowed:
            reasons.extend(f"veil:{reason}" for reason in veil_decision.reasons)

        if not is_allowed(text):
            reasons.append("ethics:forbidden-keyword")

        lowered = (text or "").lower()
        for guardrail in self._guardrails:
            if guardrail.lower() in lowered:
                reasons.append(f"guardrail:{guardrail}")

        return ModerationDecision(allowed=not reasons, reasons=tuple(reasons))

    def require(self, text: str) -> None:
        decision = self.review(text)
        if not decision.allowed:
            raise ValueError("content rejected: " + ", ".join(decision.reasons))
