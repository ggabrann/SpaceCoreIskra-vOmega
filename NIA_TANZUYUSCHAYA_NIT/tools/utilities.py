"""Utility helpers: export/import и реестр источников."""
from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Iterable

SOURCES = [
    "katya_journal",
    "instagram",
    "peer_reviewed",
]


def export_memory(files: Iterable[Path], archive: Path) -> None:
    with zipfile.ZipFile(archive, "w") as zf:
        for file in files:
            zf.write(file)


def import_memory(archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive, "r") as zf:
        zf.extractall(destination)


def save_sources(destination: Path) -> None:
    destination.write_text(json.dumps({"sources": SOURCES}, ensure_ascii=False, indent=2), encoding="utf-8")
