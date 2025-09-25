import json
import sys
from typing import Dict, Any

BOUNDS = {
    "∆": (-3, 3),
    "D": (0, 9),
    "Ω": (-3, 3),
    "Λ": (0, 9),
    "Ψ": (0, 6),
}

REQUIRED_KEYS = {"facet", "snapshot", "answer", "∆", "D", "Ω", "Λ", "Ψ"}


def _check_bounds(entry: Dict[str, Any]) -> None:
    for key, (lo, hi) in BOUNDS.items():
        if key not in entry:
            raise ValueError(f"Missing metric {key}")
        value = entry[key]
        if not (lo <= value <= hi):
            raise ValueError(f"Metric {key} out of bounds: {value}")


def _check_required(entry: Dict[str, Any]) -> None:
    missing = REQUIRED_KEYS - set(entry.keys())
    if missing:
        raise ValueError(f"Missing keys: {missing}")


def validate_stream(stream) -> int:
    valid = 0
    for line_no, line in enumerate(stream, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Line {line_no}: invalid JSON: {exc}") from exc
        _check_required(entry)
        _check_bounds(entry)
        valid += 1
    return valid


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python validate_journal.py JOURNAL.jsonl")
        raise SystemExit(1)
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as fh:
        count = validate_stream(fh)
    print(f"Validated entries: {count}")


if __name__ == "__main__":
    main()
