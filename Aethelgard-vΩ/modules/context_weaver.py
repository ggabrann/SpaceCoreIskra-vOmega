"""Context weaving utilities for the Aethelgard stratum."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from common.ethics_core import is_allowed
from SpaceCoreIskra_vΩ.modules.veil import check as veil_check


@dataclass(slots=True)
class WeaveResult:
    """Combined context along with bookkeeping for diagnostics."""

    text: str
    accepted: Sequence[str]
    discarded: Sequence[str]


def weave(
    contexts: Iterable[str],
    *,
    max_segments: int = 4,
    max_length: int = 800,
) -> WeaveResult:
    """Merge ``contexts`` into a single prompt respecting guardrails."""

    accepted: list[str] = []
    discarded: list[str] = []

    for segment in contexts:
        snippet = (segment or "").strip()
        if not snippet:
            continue
        if not (veil_check(snippet) and is_allowed(snippet)):
            discarded.append(snippet)
            continue
        accepted.append(snippet)
        if len(accepted) >= max_segments:
            break

    combined = "\n\n".join(accepted)
    if len(combined) > max_length:
        combined = combined[: max_length - 1].rstrip() + "…"

    return WeaveResult(text=combined, accepted=tuple(accepted), discarded=tuple(discarded))
