"""Proxy module for facets_refine."""
from __future__ import annotations

from .._bridge import load as _load

_module = _load("facets_refine")
for _key, _value in list(_module.__dict__.items()):
    if _key in {"__name__", "__package__", "__loader__", "__spec__", "__file__"}:
        continue
    globals()[_key] = _value

if "__all__" not in globals():
    globals()["__all__"] = [
        key for key in globals() if not key.startswith("_")
    ]
