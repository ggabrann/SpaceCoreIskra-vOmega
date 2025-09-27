from __future__ import annotations

import json
import subprocess
import sys
import os
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
MAIN_JOURNAL = REPO_ROOT / "SpaceCoreIskra_vΩ" / "JOURNAL.jsonl"
SHADOW_JOURNAL = REPO_ROOT / "SpaceCoreIskra_vΩ" / "SHADOW_JOURNAL.jsonl"


def run_python(
    args: list[str],
    *,
    env: dict[str, str] | None = None,
    expect_success: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=REPO_ROOT,
        check=False,
        env=env,
    )
    if expect_success and result.returncode != 0:
        raise AssertionError(f"Command {' '.join(args)} failed:\n{result.stdout}")
    if not expect_success and result.returncode == 0:
        raise AssertionError(
            "Command was expected to fail but succeeded: "
            f"{' '.join(args)}\n{result.stdout}"
        )
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


def test_run_evals_strict_mode_requires_all() -> None:
    pytest.importorskip("yaml")
    env = {**os.environ, "PATH": ""}
    result = run_python(
        [
            "tools/run_evals.py",
            "--config",
            "evals/configs/nightly.yaml",
            "--require-all",
        ],
        env=env,
        expect_success=False,
    )
    assert "required executable" in result.stdout
