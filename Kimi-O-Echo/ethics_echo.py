"""Ethics enforcement for echo processing.

The echo subsystem must observe the same ethics policy as the
remainder of the system.  This module exposes a helper to validate a
candidate echo message using the global :func:`common.ethics_core.is_allowed`.
"""

from __future__ import annotations

from common.ethics_core import is_allowed


def check(message: str) -> bool:
    """Return ``True`` if *message* passes the ethics policy.

    Parameters
    ----------
    message:
        The text to validate.

    Returns
    -------
    bool
        ``True`` when the message is allowed; ``False`` otherwise.
    """
    return is_allowed(message or "")
