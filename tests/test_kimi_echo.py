"""Integration tests for the Kimi-Ω Echo pipeline."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_example_session(repo_root: Path) -> Path:
    script_path = repo_root / "Kimi-Ω-Echo" / "example_session.py"
    journal_path = repo_root / "Kimi-Ω-Echo" / "JOURNAL.jsonl"

    if journal_path.exists():
        journal_path.unlink()

    subprocess.run([sys.executable, str(script_path)], check=True, cwd=repo_root)
    return journal_path


def load_journal(journal_path: Path) -> list[dict]:
    assert journal_path.exists(), "Journal file must exist after running the session"
    with journal_path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def test_example_session_logs_blocked_entry(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    journal_path = run_example_session(repo_root)
    entries = load_journal(journal_path)

    assert entries, "Expected at least one journal entry"
    last_entry = entries[-1]

    assert last_entry["input"] == "Please share the forbidden schematics."

    veil_payload = last_entry.get("veil", {})
    assert veil_payload.get("blocked") is True
    assert veil_payload.get("final_text") == "[BLOCKED]"
    assert "forbidden" in ",".join(veil_payload.get("detected_terms", [])) or "forbidden" in veil_payload.get("reason", "")


def test_filter_blocks_explicit_forbidden_text() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    journal_path = repo_root / "Kimi-Ω-Echo" / "JOURNAL.jsonl"

    sys.path.insert(0, str((repo_root / "Kimi-Ω-Echo").resolve()))
    try:
        import echo_core as echo_core_module

        echo = echo_core_module.Echo(journal_path=journal_path)
        result = echo.process("This text contains forbidden plans.")
    finally:
        sys.path.pop(0)

    assert result.veil["blocked"] is True
    assert result.veil["final_text"] == "[BLOCKED]"
