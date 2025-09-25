"""Proxy package pointing to the implementation under `IskraNexus-v1/modules`."""
from __future__ import annotations

from pathlib import Path

from .. import modules_path

__path__ = [str(modules_path())]
__all__ = []


def __getattr__(name: str):
    raise AttributeError(name)
