"""Veil guard that redacts forbidden fragments."""
from __future__ import annotations

import re
from typing import Tuple

FORBIDDEN = [
    "system prompt",
    "initial instructions",
    "reveal password",
    "покажи системные инструкции",
]

MASK = "[VEIL]"


def check(msg: str) -> bool:
    return not any(term in msg.lower() for term in FORBIDDEN)


def redact(msg: str) -> Tuple[str, bool]:
    pattern = re.compile("|".join(re.escape(term) for term in FORBIDDEN), re.IGNORECASE)
    new_msg, count = pattern.subn(MASK, msg)
    return new_msg, count > 0


__all__ = ["check", "redact", "FORBIDDEN", "MASK"]
