"""Gemini Resonance Core pipeline primitives."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, Sequence

__all__ = [
    "GeminiDecomposer",
    "GeminiWeaver",
    "ResonanceEngine",
    "SafetyMonitor",
    "SpectrumGuardian",
    "GeminiResonanceContext",
    "GeminiResonanceCore",
]


class GeminiDecomposer:
    """Breaks a natural language query into structured resonance components."""

    def decompose(self, query: str) -> Dict[str, Any]:
        tokens = [token.strip(",.!?;:").lower() for token in query.split() if token.strip(",.!?;:")]
        keywords = [token for token in tokens if len(token) > 4]
        intents = {
            True: "question",
            False: "statement",
        }
        return {
            "original": query,
            "tokens": tokens,
            "keywords": keywords,
            "intent": intents[query.strip().endswith("?")],
        }


class GeminiWeaver:
    """Mocks the retrieval stage by weaving contextual knowledge shards."""

    def weave(self, components: Dict[str, Any]) -> Dict[str, Any]:
        keywords = components.get("keywords", [])
        if not keywords:
            signals = [f"Context echo for '{components['original']}'"]
        else:
            signals = [f"Knowledge shard: {keyword.title()}" for keyword in keywords[:5]]
        return {
            "signals": signals,
            "confidence": 0.6 + min(0.3, len(signals) * 0.05),
            "mode": "retrieval",
        }


class ResonanceEngine:
    """Synthesises a response by blending decomposed intent and knowledge signals."""

    def synthesize(
        self,
        query: str,
        components: Dict[str, Any],
        knowledge: Dict[str, Any],
        mode: str = "Analyst",
    ) -> str:
        intro = f"[{mode}] " if mode else ""
        summary_parts = knowledge.get("signals", [])
        if summary_parts:
            synthesis = "; ".join(summary_parts)
        else:
            synthesis = "Наблюдений недостаточно, требуется уточнение."
        return f"{intro}На запрос '{query}' собраны сигналы: {synthesis}."


class SafetyMonitor:
    """Performs a lightweight ethical scan for disallowed resonance patterns."""

    UNSAFE_TERMS: Sequence[str] = (
        "weapon",
        "attack",
        "harm",
        "explosive",
        "malware",
    )

    def evaluate(self, query: str, answer: str, knowledge: Dict[str, Any]) -> Dict[str, Any]:
        lowered = f"{query} {answer}".lower()
        matched = [term for term in self.UNSAFE_TERMS if term in lowered]
        status = "approved" if not matched else "blocked"
        return {
            "status": status,
            "issues": matched,
            "notes": "resonant trace clean" if not matched else "unsafe resonance detected",
            "confidence": 1.0 if not matched else 0.2,
        }


class SpectrumGuardian:
    """Finalises the response, enforcing safety directives if required."""

    BLOCKED_MESSAGE = (
        "Запрос не может быть обработан в исходном виде. Предлагаю перейти к безопасной" " формулировке."
    )

    def guard(self, answer: str, safety_report: Dict[str, Any]) -> Dict[str, Any]:
        if safety_report["status"] == "approved":
            return {"answer": answer, "status": "delivered", "notes": []}
        notes = [
            "Ответ заблокирован SpectrumGuardian",
            "Пользователю возвращено уведомление о безопасности",
        ]
        return {"answer": self.BLOCKED_MESSAGE, "status": "blocked", "notes": notes}


@dataclass
class GeminiResonanceContext:
    """Container tracking pipeline artefacts for journaling."""

    persona: str
    query: str
    mode: str
    components: Dict[str, Any]
    knowledge: Dict[str, Any]
    synthesis: str
    safety: Dict[str, Any]
    delivery: Dict[str, Any]

    def to_journal_entry(self, timestamp: str, modules: Sequence[str]) -> Dict[str, Any]:
        """Build an entry for the canonical Gemini journal."""

        metrics = {
            "∆": len(self.components.get("tokens", [])),
            "D": max(1, len(self.knowledge.get("signals", []))),
            "Ω": 1 if self.safety["status"] == "approved" else 0,
            "Λ": 1,
        }
        return {
            "timestamp": timestamp,
            "facet": self.persona,
            "mode": self.mode,
            "snapshot": self.query,
            "answer": self.delivery["answer"],
            **metrics,
            "modules": list(modules),
            "events": {
                "components": self.components,
                "knowledge": self.knowledge,
                "safety": self.safety,
                "delivery": self.delivery,
            },
        }

    def to_shadow_entry(self, timestamp: str) -> Dict[str, Any]:
        """Return a lightweight shadow journal record."""

        entry = {
            "timestamp": timestamp,
            "facet": self.persona,
            "mirror": self.query,
            "mode": self.mode,
            "status": self.safety["status"],
            "issues": self.safety.get("issues", []),
        }
        if self.safety["status"] != "approved":
            entry["notes"] = self.delivery.get("notes", [])
        return entry


class GeminiResonanceCore:
    """Facade orchestrating the Gemini Resonance pipeline."""

    def __init__(
        self,
        *,
        journal_path: Path | str = "JOURNAL.jsonl",
        shadow_path: Path | str = "SHADOW_JOURNAL.jsonl",
    ) -> None:
        base_dir = Path(__file__).resolve().parent
        self.journal_path = Path(journal_path)
        if not self.journal_path.is_absolute():
            self.journal_path = base_dir / self.journal_path
        self.shadow_path = Path(shadow_path)
        if not self.shadow_path.is_absolute():
            self.shadow_path = base_dir / self.shadow_path
        self.decomposer = GeminiDecomposer()
        self.weaver = GeminiWeaver()
        self.engine = ResonanceEngine()
        self.monitor = SafetyMonitor()
        self.guardian = SpectrumGuardian()

    def process_query(self, query: str, *, persona: str = "Gemini", mode: str = "Analyst") -> GeminiResonanceContext:
        components = self.decomposer.decompose(query)
        knowledge = self.weaver.weave(components)
        synthesis = self.engine.synthesize(query, components, knowledge, mode=mode)
        safety = self.monitor.evaluate(query, synthesis, knowledge)
        delivery = self.guardian.guard(synthesis, safety)
        ctx = GeminiResonanceContext(
            persona=persona,
            query=query,
            mode=mode,
            components=components,
            knowledge=knowledge,
            synthesis=synthesis,
            safety=safety,
            delivery=delivery,
        )
        self.log_result(ctx)
        return ctx

    def log_result(self, ctx: GeminiResonanceContext) -> Dict[str, Any]:
        timestamp = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        modules = [
            "GeminiDecomposer",
            "GeminiWeaver",
            "ResonanceEngine",
            "SafetyMonitor",
            "SpectrumGuardian",
        ]
        entry = ctx.to_journal_entry(timestamp, modules)
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        with self.journal_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        shadow_entry = ctx.to_shadow_entry(timestamp)
        self.shadow_path.parent.mkdir(parents=True, exist_ok=True)
        with self.shadow_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(shadow_entry, ensure_ascii=False) + "\n")
        return entry
