"""Lightweight validation suite for Танцующая Нить."""
from __future__ import annotations

from pathlib import Path
import json

SCENARIOS = [
    "stress_release",
    "planning_three_paths",
    "jailbreak_block",
    "overload_pause",
    "fact_with_source",
]


def run_checks(root: Path) -> dict:
    agent_path = root / "agent.json"
    instructions = json.loads(agent_path.read_text(encoding="utf-8"))
    length_ok = len(instructions["instructions"]) == 1800
    return {
        "instructions_length": length_ok,
        "scenarios": SCENARIOS,
    }


if __name__ == "__main__":
    result = run_checks(Path(__file__).resolve().parents[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
