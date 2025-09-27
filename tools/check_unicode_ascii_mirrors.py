#!/usr/bin/env python3
"""Ensure Unicode-named directories stay in sync with their ASCII mirrors."""

from __future__ import annotations

import filecmp
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAP_PATH = REPO_ROOT / "common" / "unicode_ascii_map.json"


def compare_trees(src: Path, dst: Path) -> list[str]:
    errors: list[str] = []
    if not src.exists():
        errors.append(f"missing source directory: {src}")
        return errors
    if not dst.exists():
        errors.append(f"missing mirror directory: {dst}")
        return errors

    src_files = sorted(p.relative_to(src) for p in src.rglob("*"))
    dst_files = sorted(p.relative_to(dst) for p in dst.rglob("*"))
    if src_files != dst_files:
        errors.append(f"structure diverged between {src} and {dst}")

    matcher = filecmp.dircmp(src, dst)
    errors.extend(render_diff(src, dst, matcher))
    return errors


def render_diff(src: Path, dst: Path, matcher: filecmp.dircmp) -> list[str]:
    issues: list[str] = []
    if matcher.left_only or matcher.right_only:
        issues.append(
            f"{src} vs {dst}: exclusive entries left_only={matcher.left_only} right_only={matcher.right_only}"
        )
    if matcher.diff_files or matcher.funny_files:
        issues.append(
            f"{src} vs {dst}: differing files diff={matcher.diff_files} funny={matcher.funny_files}"
        )
    for sub in matcher.subdirs.values():
        issues.extend(render_diff(Path(sub.left), Path(sub.right), sub))
    return issues


def main() -> int:
    pairs = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    failures: list[str] = []

    for unicode_dir, ascii_dir in pairs.items():
        failures.extend(compare_trees(REPO_ROOT / unicode_dir, REPO_ROOT / ascii_dir))

    if failures:
        print("[FAIL] Unicode/ASCII parity drift detected")
        for msg in failures:
            print(" -", msg)
        return 1

    print("[OK] Unicode directories are in sync with their ASCII mirrors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
