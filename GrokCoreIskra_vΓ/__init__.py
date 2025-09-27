"""Utilities to access GrokCoreIskra vΓ modules as a Python package."""
from __future__ import annotations

from pathlib import Path

__all__ = ["package_root", "modules_path"]


def package_root() -> Path:
    return Path(__file__).resolve().parent


def modules_path() -> Path:
    return package_root() / "modules"
