#!/usr/bin/env python3
"""Coordinate external evaluation harnesses for nightly runs."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = REPO_ROOT / "artifacts" / "evals"


class EvalResult:
    def __init__(self, name: str, command: list[str], available: bool, returncode: int | None):
        self.name = name
        self.command = command
        self.available = available
        self.returncode = returncode

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "command": self.command,
            "available": self.available,
            "returncode": self.returncode,
        }


def load_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def cli_available(executable: str) -> bool:
    return shutil.which(executable) is not None


def run_subprocess(command: list[str], log_file: Path) -> int:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("w", encoding="utf-8") as handle:
        proc = subprocess.run(command, stdout=handle, stderr=subprocess.STDOUT, text=True)
    return proc.returncode


def plan_commands(cfg: dict) -> list[tuple[str, list[str]]]:
    plans: list[tuple[str, list[str]]] = []
    if data := cfg.get("lm_eval"):
        cmd = [
            "lm_eval",
            "--model",
            data.get("model", "gpt2"),
            "--tasks",
            ",".join(data.get("tasks", [])),
            "--num-fewshot",
            str(data.get("num_fewshot", 0)),
        ]
        plans.append(("lm_eval", cmd))
    if data := cfg.get("helm"):
        cmd = ["helm-run", "--scenarios", ",".join(data.get("scenarios", []))]
        plans.append(("helm", cmd))
    if data := cfg.get("openai_evals"):
        for registry in data.get("registry", []):
            cmd = ["oaieval", registry]
            plans.append((f"openai_evals::{registry}", cmd))
    return plans


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", type=Path, default=REPO_ROOT / "evals" / "configs" / "nightly.yaml"
    )
    parser.add_argument(
        "--require-all",
        action="store_true",
        help="Fail if any configured evaluation executable is missing",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    results: list[EvalResult] = []
    for label, command in plan_commands(config):
        executable = command[0]
        available = cli_available(executable)
        if not available:
            results.append(EvalResult(label, command, False, None))
            continue
        log_path = ARTIFACT_DIR / f"{timestamp}_{label.replace('::', '_')}.log"
        returncode = run_subprocess(command, log_path)
        results.append(EvalResult(label, command, True, returncode))

    summary_path = ARTIFACT_DIR / f"{timestamp}_summary.json"
    summary_payload = [res.as_dict() for res in results]
    summary_path.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    try:
        relative_summary = summary_path.relative_to(REPO_ROOT)
    except ValueError:
        relative_summary = summary_path
    print(f"[INFO] wrote eval summary to {relative_summary}")

    failed = [res for res in results if res.available and res.returncode not in (0, None)]
    if failed:
        for res in failed:
            print(f"[FAIL] {res.name} exit {res.returncode}")
        return 1

    missing = [res for res in results if not res.available]
    if missing:
        names = ", ".join(res.name for res in missing)
        if args.require_all:
            print(f"[ERROR] required executable missing for: {names}")
            return 2
        print("[WARN] skipped evaluations:", names)
    print("[OK] evaluation orchestration finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())
