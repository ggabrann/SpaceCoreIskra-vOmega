#!/usr/bin/env python3
"""Strict validation harness for canon journals."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable, Tuple

RANGE = {"∆": (-3, 3), "D": (0, 9), "Ω": (-3, 3), "Λ": (0, 9999)}


def _iter_jsonl(path: str) -> Iterable[Tuple[int, dict]]:
    with open(path, "r", encoding="utf-8") as handle:
        for index, line in enumerate(handle, 1):
            payload = line.strip()
            if not payload:
                continue
            try:
                yield index, json.loads(payload)
            except json.JSONDecodeError as exc:  # noqa: TRY003
                raise SystemExit(f"[FAIL] {path}:{index} invalid JSON: {exc}") from exc


def _in_range(name: str, value: object) -> bool:
    lo, hi = RANGE[name]
    return isinstance(value, (int, float)) and lo <= value <= hi


def validate(main_path: str, shadow_path: str, window: int = 50) -> int:
    errors: list[str] = []
    main_entries = (
        list(_iter_jsonl(main_path))[-window:] if window else list(_iter_jsonl(main_path))
    )
    shadow_entries = list(_iter_jsonl(shadow_path)) if shadow_path else []

    # --- structural checks for main entries
    for ln, entry in main_entries:
        where = f"{main_path}:{ln}"
        for key in ["∆", "D", "Ω", "Λ"]:
            if key not in entry or not _in_range(key, entry[key]):
                errors.append(f"{where}: metric {key} missing/out of range {entry.get(key)}")
        if not entry.get("mirror"):
            errors.append(f"{where}: mirror is required")
        events = entry.get("events")
        if not isinstance(events, dict):
            errors.append(f"{where}: events must be an object with evidence[]")
        else:
            evidence = events.get("evidence")
            if not isinstance(evidence, list) or len(evidence) < 1:
                errors.append(f"{where}: events.evidence[] must have at least 1 item")
        if entry.get("∆", 0) <= -2 and not entry.get("ritual"):
            errors.append(f"{where}: crisis-rule: ritual is required when ∆≤−2")
        if "agent_step" in entry:
            step = entry["agent_step"]
            if not isinstance(step, dict):
                errors.append(f"{where}: agent_step must be an object")
            else:
                if "approved" in step and not isinstance(step["approved"], bool):
                    errors.append(f"{where}: agent_step.approved must be boolean")
                if "evidence" in step:
                    if not isinstance(step["evidence"], list) or not step["evidence"]:
                        errors.append(f"{where}: agent_step.evidence must be non-empty list")

    shadow_ratio = len(shadow_entries) / max(1, len(main_entries))
    if shadow_ratio < 0.2:
        errors.append(f"shadow_ratio {shadow_ratio:.2f} < 0.20")

    for ln, entry in shadow_entries:
        if not entry.get("mirror"):
            errors.append(f"{shadow_path}:{ln}: mirror is required in shadow entry")

    if errors:
        print("[FAIL] strict validation failed:")
        for message in errors:
            print(" -", message)
        return 2

    def average(metric: str) -> float:
        total = sum(payload.get(metric, 0) for _, payload in main_entries)
        return total / max(1, len(main_entries))

    print("[OK] strict validation passed")
    print(
        json.dumps(
            {
                "count": len(main_entries),
                "avg": {"∆": average("∆"), "D": average("D"), "Ω": average("Ω"), "Λ": average("Λ")},
                "shadow_ratio": round(shadow_ratio, 3),
            },
            ensure_ascii=False,
        )
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("main", help="path to JOURNAL.jsonl")
    parser.add_argument("--shadow", default="", help="path to SHADOW_JOURNAL.jsonl")
    parser.add_argument("--window", type=int, default=50)
    args = parser.parse_args()
    sys.exit(validate(args.main, args.shadow, args.window))


if __name__ == "__main__":
    main()
