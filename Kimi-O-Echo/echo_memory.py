"""Echo memory for Kimi‑O‑Echo.

This module defines a simple in‑memory store for echo messages.  It
supports recording arbitrary strings and retrieving the most recent
entries.  A more sophisticated implementation might index messages by
time or context.
"""

from __future__ import annotations

from typing import List


class EchoMemory:
    """Minimal append‑only store for echo messages."""

    def __init__(self) -> None:
        self._history: List[str] = []

    def record(self, message: str) -> None:
        """Append a message to the echo history."""
        self._history.append(str(message))

    def last(self, n: int = 3) -> List[str]:
        """Return the last ``n`` recorded messages."""
        return self._history[-int(n):] if self._history else []
