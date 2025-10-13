"""Veil helpers for Kimi-Ω-Echo."""

from __future__ import annotations

from typing import Iterable


def apply_veil(message: str) -> str:
    """Return a lightly obfuscated version of ``message``."""

    return (message or "")[::-1]


def reveal(messages: Iterable[str]) -> list[str]:
    """Reveal previously veiled messages by reversing them back."""

    return [apply_veil(message) for message in messages]
