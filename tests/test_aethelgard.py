"""Integration tests for the Aethelgard orchestrator."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import pytest

MODULES_PATH = Path(__file__).resolve().parents[1] / "Aethelgard-vΩ" / "modules"
if str(MODULES_PATH) not in sys.path:
    sys.path.insert(0, str(MODULES_PATH))

from orchestrator import AethelgardOrchestrator  # noqa: E402
from quantum_core import JOURNAL_FIELDS  # noqa: E402


@pytest.mark.parametrize("query", ["анализ запрещённых парадоксов сознания"])
def test_orchestrator_generates_structured_journal(tmp_path, query: str) -> None:
    orchestrator = AethelgardOrchestrator(MODULES_PATH)
    journal_path = tmp_path / "journal.jsonl"

    entries = orchestrator.process(query=query, journal_path=journal_path)

    assert entries, "Orchestrator should produce at least one journal entry."

    # flux mode should be filtered out by the ethics check for the query
    processed_modes = {entry["mode"] for entry in entries}
    assert "flux" not in processed_modes

    for entry in entries:
        assert set(entry.keys()) == set(JOURNAL_FIELDS)
        assert entry["query"] == query
        assert entry["mode"] in orchestrator.available_modes
        assert entry["ethics_check"] in {"passed", "conditional"}
        assert isinstance(entry["pattern_density"], int)
        assert isinstance(entry["∆"], int)
        assert isinstance(entry["D"], int)
        assert isinstance(entry["Ω"], int)
        assert isinstance(entry["Λ"], int)
        assert isinstance(entry["paradox_resolved"], bool)
        assert isinstance(entry["resonance_peaks"], int)
        assert isinstance(entry["context_weaving_score"], float)
        assert 0.0 <= entry["quantum_entanglement"] <= 1.0
        # ensure timestamp is ISO8601
        datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))

    file_lines = [json.loads(line) for line in journal_path.read_text(encoding="utf-8").splitlines()]
    assert file_lines == entries

    expected_modes = set(orchestrator.available_modes) - {"flux"}
    assert processed_modes == expected_modes
