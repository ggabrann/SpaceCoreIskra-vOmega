"""Resonance detector for Aethelgard‑vΩ.

Resonance between two sequences is quantified here by computing the
ratio of the intersection over the union of their unique elements.
The resulting value lies in the ``[0.0, 1.0]`` interval and reflects
the degree of overlap.  A value of ``0.0`` indicates no shared
elements, while ``1.0`` implies both sequences contain the same
elements.
"""

from __future__ import annotations

from typing import Iterable


def detect(seq1: Iterable[str], seq2: Iterable[str]) -> float:
    """Return the Jaccard similarity between ``seq1`` and ``seq2``.

    Parameters
    ----------
    seq1, seq2:
        Sequences of hashable elements.

    Returns
    -------
    float
        The size of the intersection divided by the size of the union
        of the unique elements.
    """
    set1 = set(seq1)
    set2 = set(seq2)
    if not set1 and not set2:
        return 1.0
    union_size = len(set1 | set2)
    if union_size == 0:
        return 0.0
    return len(set1 & set2) / union_size
