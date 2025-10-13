"""Atelier module for IskraNexus‑v1.

This minimal implementation exposes a single function that prepares
user input before it is passed further down the pipeline.  The
preparation step trims leading and trailing whitespace and enforces
the system’s ethics policy via :func:`common.ethics_core.is_allowed`.

If the supplied text contains content that violates the ethics
policy, a :class:`ValueError` will be raised.
"""

from __future__ import annotations

from common.ethics_core import is_allowed


def workshop(text: str) -> str:
    """Return a cleaned version of ``text`` if it passes the ethics policy.

    Parameters
    ----------
    text:
        Arbitrary user input.  Whitespace at the start and end will be
        removed.  If the text contains any forbidden terms (see
        :mod:`common.ethics_core`), this function raises a
        :class:`ValueError` instead of returning.

    Returns
    -------
    str
        The trimmed input, ready for further processing.
    """
    cleaned = (text or "").strip()
    if not is_allowed(cleaned):
        raise ValueError("Input text violates ethics policy")
    return cleaned
