"""Veil helper for echo subsystem.

This module provides a basic mechanism for disguising the contents of
an echo message.  The :func:`apply_veil` function reverses the
characters in the message as a very simple obfuscation strategy.
While this does not provide cryptographic privacy, it deters naive
analysis of repeated content.  Full implementations should use a
robust veil consistent with the overall system design.
"""

from __future__ import annotations


def apply_veil(message: str) -> str:
    """Return a reversed copy of ``message`` to obscure its contents."""
    return (message or "")[::-1]
