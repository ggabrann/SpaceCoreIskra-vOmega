"""Quantum core orchestration utilities for Aethelgard-vΩ."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional


JOURNAL_FIELDS = [
    "timestamp",
    "mode",
    "query",
    "∆",
    "D",
    "Ω",
    "Λ",
    "pattern_density",
    "paradox_resolved",
    "quantum_entanglement",
    "ethics_check",
    "resonance_peaks",
    "context_weaving_score",
]


@dataclass(frozen=True)
class Manifest:
    """Representation of the core manifest file."""

    name: str
    version: str
    essence: str
    core_modules: List[str]
    modes: List[str]

    @classmethod
    def load(cls, manifest_path: Path) -> "Manifest":
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        return cls(
            name=data["name"],
            version=data["version"],
            essence=data["essence"],
            core_modules=list(data.get("core_modules", [])),
            modes=list(data.get("modes", [])),
        )


class QuantumCore:
    """Core engine that coordinates synthesis between Aethelgard modules."""

    def __init__(self, manifest_path: Path | str) -> None:
        path = Path(manifest_path)
        if not path.exists():
            raise FileNotFoundError(f"Manifest not found: {path}")
        self._manifest = Manifest.load(path)
        self._mode: Optional[str] = None

    @property
    def manifest(self) -> Manifest:
        return self._manifest

    @property
    def available_modes(self) -> List[str]:
        return list(self._manifest.modes)

    @property
    def mode(self) -> Optional[str]:
        return self._mode

    def set_mode(self, mode: str) -> None:
        if mode not in self._manifest.modes:
            raise ValueError(f"Unsupported mode '{mode}'. Available modes: {self._manifest.modes}")
        self._mode = mode

    def synthesize(self, query: str, components: Iterable[Mapping[str, object]]) -> Dict[str, object]:
        if self._mode is None:
            raise RuntimeError("Mode is not initialised. Call set_mode() before synthesize().")

        entry: Dict[str, object] = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "mode": self._mode,
            "query": query,
        }

        for component in components:
            for key, value in component.items():
                if key in JOURNAL_FIELDS:
                    entry[key] = value

        for field in JOURNAL_FIELDS:
            entry.setdefault(field, None)

        return entry
