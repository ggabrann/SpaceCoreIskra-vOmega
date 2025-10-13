# Версия: 3.6.0 | Дата: 2025-10-13
"""Utility helpers for working with SpaceCore Iskra distribution metadata.

The legacy codebase referenced this module in documentation, but the actual
implementation was missing. The functions below provide a minimal, well tested
API that downstream tooling can rely on while the full orchestrator is being
ported.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence, Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = PROJECT_ROOT / "DIST_MANIFEST.json"


class ManifestValidationError(RuntimeError):
    """Raised when a distribution manifest entry is malformed."""


@dataclass(frozen=True, slots=True)
class ManifestEntry:
    """Single entry from ``DIST_MANIFEST.json``."""

    path: Path
    bytes: int
    sha256: str

    @classmethod
    def from_json(cls, payload: Mapping[str, object] | Mapping[str, Any]) -> "ManifestEntry":
        if not isinstance(payload, Mapping):
            raise ManifestValidationError("Manifest entries must be mapping objects.")
        try:
            path_value = payload["path"]
            bytes_value = payload["bytes"]
            sha_value = payload["sha256"]
        except KeyError as missing:
            raise ManifestValidationError(
                f"Manifest entry is missing required field: {missing.args[0]}"
            ) from missing

        path = Path(str(path_value))
        if isinstance(bytes_value, (int, float, str)):
            byte_count = int(bytes_value)
        else:  # pragma: no cover - defensive branch
            raise ManifestValidationError("Manifest entry contains invalid byte count")
        sha = str(sha_value)
        return cls(path=path, bytes=byte_count, sha256=sha)


def load_dist_manifest(manifest_path: str | Path | None = None) -> list[ManifestEntry]:
    """Return the list of manifest entries from ``DIST_MANIFEST.json``.

    Parameters
    ----------
    manifest_path:
        Optional custom path to the manifest. When omitted the project level
        ``DIST_MANIFEST.json`` is used.
    """

    target = Path(manifest_path) if manifest_path else DEFAULT_MANIFEST
    if not target.exists():
        raise FileNotFoundError(f"Cannot locate distribution manifest at {target}")

    data = json.loads(target.read_text(encoding="utf-8"))
    raw_entries = data.get("files", [])
    if not isinstance(raw_entries, list):
        raise ManifestValidationError("The manifest payload must contain a list under 'files'.")

    entries: list[ManifestEntry] = []
    for item in raw_entries:
        if not isinstance(item, Mapping):
            raise ManifestValidationError("Manifest entries must be mapping objects.")
        entries.append(ManifestEntry.from_json(item))
    return entries


def resolve_project_path(*parts: str) -> Path:
    """Return an absolute path inside the repository root."""

    return PROJECT_ROOT.joinpath(*parts)


def find_missing_paths(entries: Sequence[ManifestEntry], required: Iterable[str]) -> list[Path]:
    """Return a list of expected paths that are absent from the manifest."""

    present = {entry.path for entry in entries}
    missing: list[Path] = []
    for raw in required:
        candidate = Path(raw)
        if candidate not in present:
            missing.append(candidate)
    return missing


def summarize_manifest(entries: Sequence[ManifestEntry]) -> dict[str, int]:
    """Provide a lightweight statistical overview of manifest entries."""

    total_size = sum(entry.bytes for entry in entries)
    return {
        "files": len(entries),
        "bytes": total_size,
    }


if __name__ == "__main__":  # pragma: no cover - developer convenience
    manifest = load_dist_manifest()
    summary = summarize_manifest(manifest)
    print("Manifest contains {files} files spanning {bytes} bytes.".format(**summary))
