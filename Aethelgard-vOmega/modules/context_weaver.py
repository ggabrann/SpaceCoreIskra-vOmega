"""Context weaver for Aethelgard‑vΩ.

The context weaver combines multiple messages into a coherent string.
It simply concatenates the messages with spaces.  This minimal
implementation does not perform semantic weaving or narrative
alignment.  It is intended to serve as a stub for more complex
context‑construction logic.
"""

from __future__ import annotations

from typing import Iterable


def weave_context(messages: Iterable[str]) -> str:
    """Concatenate messages into a single string.

    Parameters
    ----------
    messages:
        Iterable of message strings.  ``None`` values are ignored.

    Returns
    -------
    str
        Combined messages separated by a single space.
    """
    return " ".join(msg.strip() for msg in messages if msg)
