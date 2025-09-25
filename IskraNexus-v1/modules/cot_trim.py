"""Utilities to post-process chain-of-thought outputs."""
from __future__ import annotations

from typing import Tuple


def trim(text: str, max_len: int = 200) -> str:
    if not text or len(text) <= max_len:
        return text
    return text[-max_len:]


def extract_answer(text: str) -> Tuple[str, str]:
    if "Answer:" in text:
        reasoning, answer = text.split("Answer:", maxsplit=1)
        return reasoning.strip(), answer.strip()
    return text, ""


__all__ = ["trim", "extract_answer"]
