"""Pattern extractor for Aethelgard‑vΩ.

This module defines a helper that identifies repeating words within a
text.  It lower‑cases and splits the input string on whitespace,
counts occurrences of each word and returns those words whose count
exceeds one.  Punctuation is not removed; a more advanced
implementation would perform tokenisation.
"""

from __future__ import annotations

from collections import Counter
from typing import List


def extract_patterns(text: str) -> List[str]:
    """Return a list of repeated words in ``text``.

    Parameters
    ----------
    text:
        The input string to analyse.

    Returns
    -------
    list[str]
        Unique words that occur more than once, in arbitrary order.
    """
    words = (text or "").lower().split()
    counts = Counter(words)
    return [word for word, count in counts.items() if count > 1]
