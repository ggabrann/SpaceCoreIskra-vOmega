"""Echo core pipeline orchestrating helper modules."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

from echo_memory import load_memory
from ethics_echo import evaluate_ethics
from metric_tuner import tune_metrics
from paradox_split import resolve_paradox
from veil_echo import apply_filter


@dataclass
class EchoResult:
    """Container that holds the pipeline output for convenience."""

    input_text: str
    memory: Dict[str, object]
    metrics: Dict[str, float]
    paradox: Dict[str, object]
    ethics: Dict[str, object]
    veil: Dict[str, object]

    def as_dict(self) -> Dict[str, object]:
        return {
            "input": self.input_text,
            "memory": self.memory,
            "metrics": self.metrics,
            "paradox": self.paradox,
            "ethics": self.ethics,
            "veil": self.veil,
        }


class Echo:
    """High level façade that executes the Echo moderation pipeline."""

    def __init__(self, journal_path: Optional[Path] = None) -> None:
        base_path = Path(__file__).resolve().parent
        self.journal_path = Path(journal_path) if journal_path else base_path / "JOURNAL.jsonl"
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)

    def _write_journal_entry(self, entry: Dict[str, object]) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        journal_entry = {"timestamp": timestamp, **entry}
        with self.journal_path.open("a", encoding="utf-8") as journal:
            journal.write(json.dumps(journal_entry, ensure_ascii=False) + "\n")

    def process(self, user_text: str, metadata: Optional[Dict[str, object]] = None) -> EchoResult:
        """Process ``user_text`` through the Echo pipeline."""

        metadata = metadata or {}

        memory_payload = load_memory(user_text, metadata)
        metrics_payload = tune_metrics(user_text, memory_payload)
        paradox_payload = resolve_paradox(user_text, metrics_payload)
        ethics_payload = evaluate_ethics(paradox_payload["resolved_text"], metrics_payload)
        veil_payload = apply_filter(paradox_payload["resolved_text"], ethics_payload)

        result = EchoResult(
            input_text=user_text,
            memory=memory_payload,
            metrics=metrics_payload,
            paradox=paradox_payload,
            ethics=ethics_payload,
            veil=veil_payload,
        )

        self._write_journal_entry(result.as_dict())
        return result


__all__ = ["Echo", "EchoResult"]
