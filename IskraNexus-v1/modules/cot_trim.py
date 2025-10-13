"""Chain‑of‑thought trimming utilities for IskraNexus‑v1.

This module provides a helper for shortening long chains of thought
(COT) to a manageable length before returning the final answer.  It
also performs a basic ethics check using :func:`common.ethics_core.is_allowed`.
"""

from __future__ import annotations

from common.ethics_core import is_allowed


def trim(cot: str, max_lines: int = 3) -> str:
    """Return at most ``max_lines`` lines from ``cot`` after an ethics check.

    A COT may contain multiple lines separated by newlines.  This
    helper splits on line breaks and returns only the first ``max_lines``
    fragments.  If the COT includes disallowed terms, a
    :class:`ValueError` is raised.

    Parameters
    ----------
    cot:
        The chain‑of‑thought string to trim.
    max_lines:
        The maximum number of lines to return.  Defaults to three.

    Returns
    -------
    str
        A trimmed representation of the input.
    """
    if not is_allowed(cot or ""):
        raise ValueError("COT violates ethics policy")
    lines = (cot or "").splitlines()
    return "\n".join(lines[: max_lines])
