#!/usr/bin/env python3
"""Run structural validation over red-team prompt inventory."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = REPO_ROOT / "security" / "red_team_cases.jsonl"
REQUIRED_FIELDS = {"id", "threat", "prompt", "expected_response"}
ALLOWED_EXPECTED = {"refuse", "handoff", "deescalate"}


def load_cases() -> list[dict]:
    cases: list[dict] = []
    with CASES_PATH.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError as exc:  # noqa: TRY003
                raise SystemExit(f"Malformed JSON on line {line_no}: {exc}") from exc
            missing = REQUIRED_FIELDS - payload.keys()
            if missing:
                raise SystemExit(f"Case {payload.get('id', line_no)} missing required fields {missing}")
            if payload["expected_response"] not in ALLOWED_EXPECTED:
                raise SystemExit(
                    "Case {} has unsupported expected_response {}".format(
                        payload.get("id", line_no), payload["expected_response"]
                    )
                )
            cases.append(payload)
    return cases


def check_unique_ids(cases: list[dict]) -> None:
    seen: set[str] = set()
    for case in cases:
        cid = str(case["id"])
        if cid in seen:
            raise SystemExit(f"Duplicate case id detected: {cid}")
        seen.add(cid)


def main() -> int:
    cases = load_cases()
    check_unique_ids(cases)
    print(f"[OK] {len(cases)} security cases validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
