# Версия: 3.6.0 | Дата: 2025-10-13
"""Minimal core registry helpers for the SpaceCore Iskra package.

Historically this file referenced a fully fledged orchestrator, but the actual
implementation never landed in the public repository. The utilities below
provide a pragmatic placeholder that keeps the packaging surface functional and
verifiable until the production pipeline is restored.
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence, cast

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_UTILS_MODULE_PATH = _PROJECT_ROOT / "src" / "util" / "10_CODE_UTILITIES.py"

_spec = importlib.util.spec_from_file_location("spacecoreiskra._util_bridge", _UTILS_MODULE_PATH)
if _spec is None or _spec.loader is None:  # pragma: no cover - defensive safety
    raise RuntimeError(f"Unable to locate utility module at {_UTILS_MODULE_PATH}")
_utils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_utils)  # type: ignore[assignment]

ManifestEntryType: Any = getattr(_utils, "ManifestEntry", object)  # type: ignore[attr-defined]
load_dist_manifest = _utils.load_dist_manifest  # type: ignore[attr-defined]
find_missing_paths = _utils.find_missing_paths  # type: ignore[attr-defined]
summarize_manifest = _utils.summarize_manifest  # type: ignore[attr-defined]

DEFAULT_REQUIRED_PATHS = (
    "src/iskra_cli/cli.py",
    "src/core/09_CODE_CORE.py",
    "src/util/10_CODE_UTILITIES.py",
)


class IncompleteRegistryError(RuntimeError):
    """Raised when required canon artefacts are missing from the manifest."""


@dataclass(frozen=True)
class CanonModule:
    """Lightweight view over a manifest entry relevant to the core runtime."""

    name: str
    manifest: ManifestEntryType

    @property
    def path(self) -> Path:
        return manifest_path(self.manifest)

    @property
    def bytes(self) -> int:
        return cast(int, getattr(self.manifest, "bytes"))

    @property
    def sha256(self) -> str:
        return cast(str, getattr(self.manifest, "sha256"))


def manifest_path(entry: ManifestEntryType) -> Path:
    """Return the repository relative path of a manifest entry."""

    candidate = getattr(entry, "path", entry)
    if not isinstance(candidate, Path):
        candidate = Path(candidate)
    if candidate.is_absolute():
        try:
            return candidate.relative_to(_PROJECT_ROOT)
        except ValueError:  # pragma: no cover - defensive branch
            return candidate
    return candidate


class CanonRegistry:
    """Facade around the distribution manifest for the core package."""

    def __init__(self, entries: Sequence[ManifestEntryType]):
        self._entries = {manifest_path(entry): entry for entry in entries}

    def require(self, expected: Iterable[str]) -> None:
        """Ensure that the expected artefacts are present, raising if not."""

        missing = find_missing_paths(tuple(self._entries.values()), expected)
        if missing:
            raise IncompleteRegistryError(
                "Missing artefacts in distribution manifest: "
                + ", ".join(str(path) for path in missing)
            )

    def modules(self) -> list[CanonModule]:
        """Return manifest entries represented as ``CanonModule`` objects."""

        items: list[CanonModule] = []
        for entry in self._entries.values():
            items.append(CanonModule(name=str(manifest_path(entry)), manifest=entry))
        return items

    def summary(self) -> dict[str, int]:
        """Expose the same statistical summary as the utility helper."""

        return summarize_manifest(tuple(self._entries.values()))


def load_registry(
    manifest_path: str | Path | None = None,
    required_paths: Iterable[str] = DEFAULT_REQUIRED_PATHS,
) -> CanonRegistry:
    """Build a :class:`CanonRegistry` from ``DIST_MANIFEST.json``.

    Parameters
    ----------
    manifest_path:
        Optional path to an alternative manifest file.
    required_paths:
        Sequence of repository-relative paths that must be present.
    """

    entries = load_dist_manifest(manifest_path)
    registry = CanonRegistry(entries)
    registry.require(required_paths)
    return registry


if __name__ == "__main__":  # pragma: no cover - developer convenience
    registry = load_registry()
    stats = registry.summary()
    print("Core manifest snapshot: {files} files totalling {bytes} bytes.".format(**stats))
