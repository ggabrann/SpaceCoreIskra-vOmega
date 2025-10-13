"""Paradox resolver for Aethelgard‑vΩ.

In the Aethelgard layer, paradoxes are resolved by prioritising the
first query.  This simplistic resolver returns the first element
from the list of questions.  More advanced logic would perform
comparative analysis and synthesis across the paradox space.
"""

from __future__ import annotations

from typing import Iterable, Optional


def resolve(questions: Iterable[str]) -> Optional[str]:
    """Return the first element from ``questions`` or ``None`` if empty."""
    for q in questions:
        return q
    return None
