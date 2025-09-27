#!/usr/bin/env python3
"""Aggregate canon journal metrics for quick CI summaries."""

from __future__ import annotations

import argparse
import json
from statistics import mean
from typing import Iterable


def iter_jsonl(path: str) -> Iterable[dict]:
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            payload = line.strip()
            if payload:
                yield json.loads(payload)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("main", help="path to canonical JOURNAL.jsonl")
    parser.add_argument("--shadow", help="optional SHADOW_JOURNAL.jsonl path")
    args = parser.parse_args()

    main_entries = list(iter_jsonl(args.main))
    shadow_entries = list(iter_jsonl(args.shadow)) if args.shadow else []

    averages = {
        key: mean([entry.get(key, 0) for entry in main_entries]) if main_entries else 0
        for key in ["∆", "D", "Ω", "Λ"]
    }
    output = {
        "count": len(main_entries),
        "facets": sorted({entry.get("facet", "") for entry in main_entries}),
        "avg": averages,
        "shadow_ratio": round(len(shadow_entries) / max(1, len(main_entries)), 3),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
