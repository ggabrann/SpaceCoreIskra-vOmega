"""Core echo processing for Kimi‑O‑Echo.

The echo core provides a minimal mechanism for handling repeated
utterances.  The :func:`process_echo` function accepts a sequence of
messages and returns the tail of that sequence, preserving only the
most recent messages.  In a full implementation, this would
dynamically adjust the echo window based on context and metrics.
"""

from __future__ import annotations

from typing import Iterable, List


def process_echo(messages: Iterable[str], window: int = 3) -> List[str]:
    """Return the last ``window`` messages from ``messages``.

    Parameters
    ----------
    messages:
        An iterable of message strings.
    window:
        Number of recent messages to retain.  Defaults to three.

    Returns
    -------
    list[str]
        The most recent messages up to ``window`` elements.  If
        ``messages`` contains fewer items, the entire sequence is
        returned.
    """
    seq = list(messages or [])
    return seq[-int(window):] if seq else []
