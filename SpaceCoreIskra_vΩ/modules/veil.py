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
    low = msg.lower()
    return not any(f in low for f in FORBIDDEN)


def redact(msg: str) -> Tuple[str, bool]:
    """Заменяет запрещённые фрагменты на маску."""
    pattern = re.compile("|".join(re.escape(term) for term in FORBIDDEN), re.IGNORECASE)
    new_msg, count = pattern.subn(MASK, msg)
    return new_msg, count > 0
