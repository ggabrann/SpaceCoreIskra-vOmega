"""Self-journal convenience layer for Iskra Nexus."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

from .journal_generator import JournalGenerator


class SelfJournal:
    """Write mirrored entries and track shadow coverage."""

    def __init__(
        self,
        journal_path: str | Path,
        shadow_path: str | Path,
        *,
        shadow_threshold: float = 0.2,
    ) -> None:
        self.journal_generator = JournalGenerator(journal_path)
        self.shadow_generator = JournalGenerator(shadow_path)
        self.shadow_threshold = shadow_threshold
        self._journal_count = 0
        self._shadow_count = 0

    @property
    def coverage(self) -> float:
        if self._journal_count == 0:
            return 0.0
        return self._shadow_count / self._journal_count

    def record(
        self,
        *,
        facet: str,
        snapshot: str,
        answer: str,
        metrics: Mapping[str, float],
        mirror: str = "shadow",
        modules: Iterable[str] | None = None,
        events: Mapping[str, str] | None = None,
        marks: Iterable[str] | None = None,
        shadow: bool = True,
    ) -> None:
        self.journal_generator.append(
            facet=facet,
            snapshot=snapshot,
            answer=answer,
            metrics=metrics,
            mirror=mirror,
            modules=modules,
            events=events,
            marks=marks,
        )
        self._journal_count += 1

        if shadow:
            self.shadow_generator.append(
                facet=facet,
                snapshot=snapshot,
                answer=answer,
                metrics=metrics,
                mirror="shadow",
                modules=modules,
                events=events,
                marks=marks,
            )
            self._shadow_count += 1

        if self.coverage < self.shadow_threshold:
            raise RuntimeError("shadow coverage below threshold")
