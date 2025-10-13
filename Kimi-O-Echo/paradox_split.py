"""Paradox splitter for echo subsystem.

In certain echo scenarios the user may pose paradoxical or compound
queries.  This helper splits a text into segments using simple
sentence punctuation as boundaries.  A more advanced resolver would
perform logical analysis to separate contradictory clauses.
"""

from __future__ import annotations

import re
from typing import List


_SPLIT_REGEX = re.compile(r"[.!?]+\s*", re.MULTILINE)


def split(text: str) -> List[str]:
    """Split ``text`` into fragments on punctuation boundaries.

    Parameters
    ----------
    text:
        Input string to split.

    Returns
    -------
    list[str]
        List of non‑empty fragments after splitting on sentence end
        punctuation.
    """
    parts = _SPLIT_REGEX.split(text or "")
    return [part for part in parts if part.strip()]
