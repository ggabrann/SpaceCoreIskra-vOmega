"""Pattern discovery helpers for Aethelgard."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Sequence

from common.ethics_core import is_allowed
from SpaceCoreIskra_vΩ.modules.veil import check as veil_check

_TOKEN_RE = re.compile(r"[\w-]+", re.UNICODE)


@dataclass(slots=True)
class PatternSummary:
    keywords: Sequence[str]
    flagged: Sequence[str]


def extract(text: str | Iterable[str]) -> PatternSummary:
    """Extract keywords and highlight unsafe fragments."""

    if isinstance(text, str):
        stream = [text]
    else:
        stream = list(text)

    tokens: set[str] = set()
    flagged: list[str] = []
    for chunk in stream:
        snippet = chunk or ""
        for token in _TOKEN_RE.findall(snippet.lower()):
            if len(token) < 3:
                continue
            tokens.add(token)
        if not (veil_check(snippet) and is_allowed(snippet)):
            flagged.append(snippet)

    return PatternSummary(keywords=tuple(sorted(tokens)), flagged=tuple(flagged))
