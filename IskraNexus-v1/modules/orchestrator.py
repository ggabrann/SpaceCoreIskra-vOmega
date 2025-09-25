"""Central orchestrator wiring together the Iskra Nexus modules."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from . import atelier, cot_trim, veil
from .ethics_layer import EthicsLayer
from .journal_generator import JournalGenerator
from .persona_module import PersonaRegistry
from .prompt_manager import PromptManager
from .rag_connector import RAGConnector
from .self_journal import SelfJournal


class Orchestrator:
    def __init__(self, base_path: Optional[Path] = None) -> None:
        self.base_path = Path(base_path or Path(__file__).resolve().parents[1])
        self.manifest_path = self.base_path / "iskra_nexus_v1_module.json"
        self.manifest = self._load_manifest()
        self.prompt_manager = PromptManager(self.base_path / "prompts.json")
        self.rag = RAGConnector()
        self.personas = PersonaRegistry()
        self.ethics = EthicsLayer()
        self.self_journal = SelfJournal()
        self.journal = JournalGenerator(self.manifest_path, self.base_path / "JOURNAL.jsonl")
        self._bootstrap_components()

    # ------------------------------------------------------------------
    def _load_manifest(self) -> Dict:
        if not self.manifest_path.exists():
            return {"modes": ["banality", "paradox", "synthesis"], "components": []}
        with self.manifest_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def _bootstrap_components(self) -> None:
        self.rag.add(
            "Манифест Iskra Nexus",
            "Iskra Nexus соединяет кристалл и антикристалл, создавая поле синтеза между банальностью и парадоксом.",
            relevance=0.9,
            recency=0.5,
        )
        self.rag.add(
            "Техническая матрица",
            "Оркестратор управляет модулями prompt, rag, persona и journal, фиксируя результаты в shadow-логе.",
            relevance=0.7,
            recency=0.6,
        )
        self.personas.register("Archivist", {"искра", "nexus", "манифест"}, tone="reflective", focus="история")
        self.personas.register("Synthesist", {"синтез", "анализ", "структура"}, tone="analytical", focus="соединение")

    # ------------------------------------------------------------------
    @property
    def modes(self) -> List[str]:
        return list(self.manifest.get("modes", [])) or ["banality", "paradox", "synthesis"]

    @property
    def components(self) -> List[str]:
        return list(self.manifest.get("components", []))

    # ------------------------------------------------------------------
    def _compose_answer(self, query: str, rag_hits: List[Dict], persona_tone: str, mode: str) -> str:
        context = rag_hits[0]["snippet"] if rag_hits else "Система размышляет над вопросом без внешних материалов."
        if mode == "banality":
            return f"Ответ в духе банальности ({persona_tone}): {context}"
        if mode == "paradox":
            return (
                f"Парадоксальный ответ ({persona_tone}): {context} — но одновременно это и вызов привычной логике."
            )
        return (
            f"Синтетический ответ ({persona_tone}): {context} Он объединяет факты и образы для целостного понимания."
        )

    def _keywords(self, text: str) -> Iterable[str]:
        return {token.strip(".,!?;:" ).lower() for token in text.split() if token.strip(".,!?;:" )}

    def process(self, query: str, *, mode: str = "banality", context: Optional[Dict] = None) -> Dict:
        if mode not in self.modes:
            raise ValueError(f"Mode '{mode}' is not supported by the manifest")
        context = context or {}
        self.self_journal.clear()
        self.self_journal.log("mode", {"selected": mode})

        prompt_record = self.prompt_manager.add(
            f"query::{mode}",
            query,
            meta={"mode": mode, "tags": ["runtime"]},
        )
        self.self_journal.log("prompt_stored", {"created_at": prompt_record.created_at})

        rag_hits = self.rag.search(query)
        self.self_journal.log("rag_search", {"hits": rag_hits})

        matches = self.personas.match(self._keywords(query) or {mode})
        persona_names = [persona.name for persona, _ in matches]
        persona_tone = matches[0][0].tone if matches else "neutral"
        self.self_journal.log("persona_match", {"personas": persona_names})

        raw_answer = self._compose_answer(query, rag_hits, persona_tone, mode)
        reasoning, final_answer = cot_trim.extract_answer(raw_answer)
        if not final_answer:
            final_answer = raw_answer
        safe_answer = self.ethics.enforce(final_answer)
        safe_answer, veiled = veil.redact(safe_answer)
        self.self_journal.log("safety", {"ethics_passed": safe_answer != "Ответ скрыт этическим фильтром.", "veiled": veiled})

        atelier_metrics = atelier.critique(query, safe_answer)
        metrics = {
            "∆": len(query),
            "D": len(safe_answer),
            "Ω": max(1, len(rag_hits)),
            "Λ": int(round(atelier_metrics.get("semantic_density", 0.0) * 100)),
        }
        self.self_journal.log("metrics", metrics)

        events = {
            "mode": mode,
            "persona": persona_names,
            "veiled": veiled,
            "reasoning_length": len(reasoning),
        }
        journal_entry = self.journal.record(
            facet=mode,
            snapshot=query,
            answer=safe_answer,
            metrics=metrics,
            mirror=context.get("mirror", "shadow-000"),
            modules=self.components,
            events=events,
            marks=[{"atelier": atelier_metrics}],
        )
        self.self_journal.log("journal", {"timestamp": journal_entry["timestamp"]})

        return {
            "response": safe_answer,
            "mode": mode,
            "metrics": metrics,
            "rag_hits": rag_hits,
            "personas": persona_names,
            "atelier": atelier_metrics,
            "shadow_log": self.self_journal.entries,
            "journal_entry": journal_entry,
        }


__all__ = ["Orchestrator"]
