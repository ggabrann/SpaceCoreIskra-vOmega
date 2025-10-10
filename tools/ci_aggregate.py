#!/usr/bin/env python3
"""Aggregate canon journal metrics for quick CI summaries."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from statistics import mean
from typing import Any


def iter_jsonl(path: str) -> Iterable[dict]:
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            payload = line.strip()
            if payload:
                yield json.loads(payload)


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("window must be a positive integer")
    return parsed


def coerce_number(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("main", help="path to canonical JOURNAL.jsonl")
    parser.add_argument("--shadow", help="optional SHADOW_JOURNAL.jsonl path")
    parser.add_argument(
        "--window",
        type=positive_int,
        help="limit aggregation to the last N journal entries",
    )
    args = parser.parse_args()

    all_main_entries = list(iter_jsonl(args.main))
    if args.window is not None:
        main_entries = all_main_entries[-args.window :]
    else:
        main_entries = all_main_entries

    if args.shadow:
        raw_shadow_entries = list(iter_jsonl(args.shadow))
        if args.window is not None and main_entries:
            mirrors = {
                entry.get("mirror")
                for entry in main_entries
                if isinstance(entry.get("mirror"), str)
            }
            shadow_entries = [
                entry
                for entry in raw_shadow_entries
                if entry.get("mirror") in mirrors
            ]
        else:
            shadow_entries = raw_shadow_entries
    else:
        shadow_entries = []

    def average_for(key: str) -> float:
        values = [coerce_number(entry.get(key, 0)) for entry in main_entries]
        return mean(values) if values else 0.0

    averages = {key: average_for(key) for key in ["∆", "D", "Ω", "Λ"]}
    output = {
        "count": len(main_entries),
        "total_count": len(all_main_entries),
        "facets": sorted({entry.get("facet", "") for entry in main_entries}),
        "avg": averages,
        "shadow_ratio": round(len(shadow_entries) / max(1, len(main_entries)), 3),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
