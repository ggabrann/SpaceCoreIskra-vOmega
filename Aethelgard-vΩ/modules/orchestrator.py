"""High level orchestration for the Aethelgard-vΩ pipeline."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Optional

import context_weaver
import ethics_filter
import paradox_resolver
import pattern_extractor
import resonance_detector
import self_reflection

from quantum_core import JOURNAL_FIELDS, QuantumCore


class AethelgardOrchestrator:
    """Coordinate modules and persist journal entries."""

    def __init__(self, base_path: Optional[Path] = None) -> None:
        self._base_path = Path(base_path) if base_path is not None else Path(__file__).resolve().parent
        manifest_path = self._base_path.parent / "MANIFEST_Aethelgard-vΩ.json"
        self._core = QuantumCore(manifest_path)

    @property
    def core(self) -> QuantumCore:
        return self._core

    @property
    def available_modes(self) -> List[str]:
        return self._core.available_modes

    def _collect_components(self, query: str, mode: str) -> List[dict]:
        return [
            pattern_extractor.analyze(query, mode),
            paradox_resolver.resolve(query, mode),
            context_weaver.weave(query, mode),
            ethics_filter.evaluate(query, mode),
            self_reflection.reflect(query, mode),
            resonance_detector.detect(query, mode),
        ]

    def process(
        self,
        query: str,
        modes: Optional[Iterable[str]] = None,
        journal_path: Optional[Path] = None,
    ) -> List[dict]:
        modes_to_use = list(modes) if modes is not None else self.available_modes

        invalid_modes = [mode for mode in modes_to_use if mode not in self.available_modes]
        if invalid_modes:
            raise ValueError(f"Unsupported modes requested: {invalid_modes}")

        journal_entries: List[dict] = []
        writer = None
        if journal_path is not None:
            journal_path = Path(journal_path)
            journal_path.parent.mkdir(parents=True, exist_ok=True)
            writer = journal_path.open("w", encoding="utf-8")

        try:
            for mode in modes_to_use:
                self._core.set_mode(mode)
                components = self._collect_components(query, mode)
                entry = self._core.synthesize(query, components)
                if entry.get("ethics_check") == "rejected":
                    continue

                journal_entries.append(entry)
                if writer is not None:
                    writer.write(json.dumps(entry, ensure_ascii=False) + "\n")
        finally:
            if writer is not None:
                writer.close()

        for entry in journal_entries:
            for field in JOURNAL_FIELDS:
                entry.setdefault(field, None)

        return journal_entries
