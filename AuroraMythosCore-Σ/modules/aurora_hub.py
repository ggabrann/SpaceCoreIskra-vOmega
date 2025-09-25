"""Central orchestration layer for AuroraMythosCore Σ."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from .ethos_guard import EthosGuard
from .oracle_rag import OracleRAG
from .persona_constellation import PersonaConstellation
from .prompt_forge import PromptForge
from .story_weaver import StoryWeaver
from .mythic_atelier import MythicAtelier
from .journal_architect import JournalArchitect
from .pulse_analyzer import PulseAnalyzer


@dataclass
class AuroraConfig:
    mode: str = "PARABLE"
    enable_shadow: bool = True
    psi_bias: int = 2


@dataclass
class AuroraContext:
    query: str
    persona: str
    metrics: Dict[str, int]
    sources: List[str] = field(default_factory=list)
    mythic_overlay: Optional[str] = None
    events: Dict[str, Any] = field(default_factory=dict)


class AuroraHub:
    """Coordinates the mythic-analytic processing pipeline."""

    def __init__(self, config: Optional[AuroraConfig] = None, journal_path: str = "JOURNAL.jsonl", shadow_path: str = "SHADOW_JOURNAL.jsonl") -> None:
        self.config = config or AuroraConfig()
        self.ethos = EthosGuard()
        self.oracle = OracleRAG()
        self.personas = PersonaConstellation()
        self.prompts = PromptForge()
        self.weaver = StoryWeaver()
        self.atelier = MythicAtelier()
        self.journal = JournalArchitect(journal_path, shadow_path)
        self.pulse = PulseAnalyzer()

    # -- public API -------------------------------------------------
    def handle_query(self, query: str, preset: Optional[str] = None) -> Dict[str, Any]:
        persona = self.personas.select_persona(query)
        metrics = self.pulse.initial_metrics(mode=preset or self.config.mode, psi_bias=self.config.psi_bias)
        ctx = AuroraContext(query=query, persona=persona, metrics=metrics)

        if not self.ethos.is_allowed(query):
            entry = self.journal.log_blocked(ctx, reason="ethics")
            return {"status": "blocked", "reason": "ethics", "entry": entry}

        prompt = self.prompts.compose(persona=persona, query=query, mode=preset or self.config.mode)
        ctx.events["prompt"] = prompt

        knowledge = self.oracle.search(query, limit=5)
        ctx.sources.extend(src["title"] for src in knowledge)

        analytic_answer = self.atelier.analyze(query=query, prompt=prompt, knowledge=knowledge)
        mythic_answer = self.weaver.enchant(analytic_answer, persona=persona, psi=ctx.metrics.get("Ψ", 0))
        ctx.mythic_overlay = mythic_answer

        entry = self.journal.log_success(ctx)
        report = self.pulse.register(entry)

        return {
            "status": "ok",
            "persona": persona,
            "answer": mythic_answer,
            "metrics": ctx.metrics,
            "sources": knowledge,
            "journal_entry": entry,
            "pulse_report": report,
        }
