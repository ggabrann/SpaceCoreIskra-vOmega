"""Append-only echo memory for Kimi-Ω-Echo."""

from __future__ import annotations

from collections import deque
from typing import Deque, Iterable, List

from .ethics_echo import evaluate


class EchoMemory:
    """Bounded echo memory that honours guardrail checks."""

    def __init__(self, *, capacity: int = 20) -> None:
        self.capacity = max(1, int(capacity))
        self._history: Deque[str] = deque(maxlen=self.capacity)

    def record(self, message: str) -> bool:
        """Record ``message`` when it passes guardrails."""

        verdict = evaluate(message)
        if not verdict.allowed:
            return False
        self._history.append(str(message))
        return True

    def extend(self, messages: Iterable[str]) -> int:
        """Record multiple messages, returning the number accepted."""

        accepted = 0
        for message in messages:
            accepted += int(self.record(message))
        return accepted

    def last(self, n: int = 3) -> List[str]:
        """Return the last ``n`` remembered messages."""

        n = max(0, int(n))
        if n == 0:
            return []
        return list(self._history)[-n:]
