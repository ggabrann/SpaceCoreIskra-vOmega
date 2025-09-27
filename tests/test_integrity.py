from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAIN_JOURNAL = REPO_ROOT / "SpaceCoreIskra_vΩ" / "JOURNAL.jsonl"
SHADOW_JOURNAL = REPO_ROOT / "SpaceCoreIskra_vΩ" / "SHADOW_JOURNAL.jsonl"


def run_python(args: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"Command {' '.join(args)} failed:\n{result.stdout}")
    return result


def test_json_schema_validation() -> None:
    run_python(["tools/validate_json_schemas.py"])


def test_strict_journal_validation() -> None:
    run_python(
        [
            "tools/validate_journal_enhanced.py",
            str(MAIN_JOURNAL),
            "--shadow",
            str(SHADOW_JOURNAL),
            "--window",
            "0",
        ]
    )


def test_ci_aggregate_output() -> None:
    result = run_python(
        [
            "tools/ci_aggregate.py",
            str(MAIN_JOURNAL),
            "--shadow",
            str(SHADOW_JOURNAL),
        ]
    )
    payload = json.loads(result.stdout)
    assert "count" in payload and payload["count"] >= 0


def test_unicode_ascii_parity() -> None:
    run_python(["tools/check_unicode_ascii_mirrors.py"])


def test_security_cases() -> None:
    run_python(["tools/run_security_checks.py"])


def test_rag_audit_smoke() -> None:
    dataset = REPO_ROOT / "tests" / "data" / "rag_sample.jsonl"
    result = run_python(
        [
            "tools/rag_audit.py",
            str(dataset),
            "--sample-size",
            "10",
            "--threshold",
            "0.35",
            "--seed",
            "7",
        ]
    )
    payload = json.loads(result.stdout)
    assert payload["documents_sampled"] == 2
    assert payload["chunk_pairs_evaluated"] == 3
    assert payload["anomalies"], "Expected at least one anomaly"
    assert payload["anomalies"][0]["doc_id"] == "doc-2"
