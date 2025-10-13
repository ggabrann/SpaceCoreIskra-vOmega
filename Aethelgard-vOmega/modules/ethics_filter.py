"""Ethics filter for Aethelgard‑vΩ.

This helper exposes a simple wrapper around the global
:func:`common.ethics_core.is_allowed` check.  It returns ``True`` if
the supplied text is permissible under the ethics policy.
"""

from __future__ import annotations

from common.ethics_core import is_allowed


def filter_text(text: str) -> bool:
    """Return ``True`` if ``text`` passes the ethics policy."""
    return is_allowed(text or "")
