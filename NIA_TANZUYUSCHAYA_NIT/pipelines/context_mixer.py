"""Context mixer for assembling prompts without перегруза."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, List
import yaml


PRIORITY_ORDER = ("goal", "state", "constraints", "risks", "resources")


def load_state(state_file: Path) -> Dict[str, Any]:
    return yaml.safe_load(state_file.read_text(encoding="utf-8"))


def build_context(goal: str, state: Dict[str, Any], extras: Dict[str, Any] | None = None) -> List[str]:
    """Compose context paragraphs following priority order."""
    context: List[str] = [f"Goal: {goal}"]
    if extras is None:
        extras = {}
    blocks = {
        "state": f"Energy={extras.get('energy')} Focus={extras.get('focus')}" if extras else "",
        "constraints": extras.get("constraints", ""),
        "risks": extras.get("risks", ""),
        "resources": extras.get("resources", ""),
    }
    for key in PRIORITY_ORDER[1:]:
        value = blocks.get(key, "")
        if value:
            context.append(f"{key.title()}: {value}")
    anchors = state.get("long_term", {}).get("anchors", [])
    if anchors:
        focus = "; ".join(anchor["statement"] for anchor in anchors)
        context.append(f"Anchors: {focus}")
    return context
