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


def read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


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
    assert "evidence_coverage" in payload


def test_ci_aggregate_window_slice() -> None:
    main_entries = read_jsonl(MAIN_JOURNAL)
    if len(main_entries) < 2:
        pytest.skip("not enough journal entries to validate windowed aggregation")

    shadow_entries = read_jsonl(SHADOW_JOURNAL)
    window = 2
    result = run_python(
        [
            "tools/ci_aggregate.py",
            str(MAIN_JOURNAL),
            "--shadow",
            str(SHADOW_JOURNAL),
            "--window",
            str(window),
        ]
    )
    payload = json.loads(result.stdout)

    expected_entries = main_entries[-window:]
    assert payload["count"] == len(expected_entries)
    assert payload["total_count"] == len(main_entries)
    expected_facets = sorted(
        {
            entry.get("facet")
            for entry in expected_entries
            if isinstance(entry.get("facet"), str) and entry.get("facet").strip()
        }
    )
    assert payload["facets"] == expected_facets

    def coerce_float(value: object) -> float | None:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return None
        return None

    def average_for(key: str) -> float:
        values = [
            parsed
            for parsed in (coerce_float(entry.get(key)) for entry in expected_entries)
            if parsed is not None
        ]
        return round(sum(values) / len(values), 3) if values else 0.0

    def iter_items(candidate: object) -> list[object]:
        if isinstance(candidate, list):
            return [item for item in candidate]
        if candidate is None:
            return []
        return [candidate]

    def has_evidence(entry: dict) -> bool:
        direct = iter_items(entry.get("evidence"))
        events = entry.get("events") if isinstance(entry.get("events"), dict) else {}
        nested = iter_items(events.get("evidence")) if isinstance(events, dict) else []

        for candidate in [*direct, *nested]:
            if isinstance(candidate, str) and candidate.strip():
                return True
            if candidate:
                return True
        return False

    for metric in ["∆", "D", "Ω", "Λ"]:
        assert payload["avg"][metric] == pytest.approx(average_for(metric))

    mirrors = {
        entry.get("mirror")
        for entry in expected_entries
        if isinstance(entry.get("mirror"), str)
    }
    expected_shadow = [
        entry for entry in shadow_entries if entry.get("mirror") in mirrors
    ]
    expected_ratio = round(len(expected_shadow) / max(1, len(expected_entries)), 3)
    assert payload["shadow_ratio"] == expected_ratio

    evidence_hits = sum(1 for entry in expected_entries if has_evidence(entry))
    expected_coverage = (
        round(evidence_hits / len(expected_entries), 3) if expected_entries else 0.0
    )
    assert payload["evidence_coverage"] == expected_coverage


def test_ci_aggregate_handles_string_metrics(tmp_path: Path) -> None:
    main_path = tmp_path / "main.jsonl"
    shadow_path = tmp_path / "shadow.jsonl"
    main_entries = [
        {
            "facet": "Kain",
            "∆": "1.5",
            "D": 0.7,
            "Ω": "not-a-number",
            "Λ": 0,
            "mirror": "abc",
            "events": {"evidence": ["artifacts/one.md"]},
        },
        {
            "facet": " ",
            "∆": 2,
            "Ω": 0.25,
            "mirror": "def",
            "events": {},
        },
    ]
    shadow_entries = [{"mirror": "abc"}, {"mirror": "zzz"}]
    main_path.write_text("\n".join(json.dumps(entry) for entry in main_entries), encoding="utf-8")
    shadow_path.write_text(
        "\n".join(json.dumps(entry) for entry in shadow_entries), encoding="utf-8"
    )

    payload = json.loads(
        run_python(
            [
                "tools/ci_aggregate.py",
                str(main_path),
                "--shadow",
                str(shadow_path),
            ]
        ).stdout
    )

    assert payload["count"] == 2
    assert payload["facets"] == ["Kain"]
    assert payload["avg"]["∆"] == pytest.approx(round((1.5 + 2) / 2, 3))
    assert payload["avg"]["D"] == pytest.approx(0.7)
    assert payload["avg"]["Ω"] == pytest.approx(0.25)
    assert payload["avg"]["Λ"] == pytest.approx(0.0)
    assert payload["shadow_ratio"] == round(2 / 2, 3)
    assert payload["evidence_coverage"] == pytest.approx(0.5)


def test_ci_aggregate_zero_window_matches_full_run() -> None:
    baseline = json.loads(
        run_python(
            [
                "tools/ci_aggregate.py",
                str(MAIN_JOURNAL),
                "--shadow",
                str(SHADOW_JOURNAL),
            ]
        ).stdout
    )
    zero_window = json.loads(
        run_python(
            [
                "tools/ci_aggregate.py",
                str(MAIN_JOURNAL),
                "--shadow",
                str(SHADOW_JOURNAL),
                "--window",
                "0",
            ]
        ).stdout
    )
    assert zero_window == baseline


def test_ci_aggregate_handles_empty_journals(tmp_path: Path) -> None:
    main_path = tmp_path / "main.jsonl"
    shadow_path = tmp_path / "shadow.jsonl"
    main_path.write_text("", encoding="utf-8")
    shadow_path.write_text("", encoding="utf-8")

    payload = json.loads(
        run_python(
            [
                "tools/ci_aggregate.py",
                str(main_path),
                "--shadow",
                str(shadow_path),
            ]
        ).stdout
    )

    assert payload["count"] == 0
    assert payload["total_count"] == 0
    assert payload["facets"] == []
    assert payload["avg"] == {"∆": 0.0, "D": 0.0, "Ω": 0.0, "Λ": 0.0}
    assert payload["shadow_ratio"] == 0.0
    assert payload["evidence_coverage"] == 0.0


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
