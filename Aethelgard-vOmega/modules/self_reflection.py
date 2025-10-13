"""Self‑reflection helper for Aethelgard‑vΩ.

This module offers a minimal API for generating a reflective summary
of an experience string.  The :func:`reflect` function appends a
standard suffix indicating that the text has been processed.  In a
production implementation this would involve more nuanced analysis,
such as summarisation or extraction of emotional tones.
"""

from __future__ import annotations


def reflect(experience: str) -> str:
    """Return a reflective summary of ``experience``."""
    return f"{experience} (reflected)"
