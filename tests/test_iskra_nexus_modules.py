from __future__ import annotations

import json
from pathlib import Path

import pytest

from IskraNexus_v1.modules.facets_refine import refine, from_metrics
from IskraNexus_v1.modules.journal_generator import JournalGenerator
from IskraNexus_v1.modules.persona_module import PersonaProfile, PersonaRegistry, select_persona
from IskraNexus_v1.modules.prompt_manager import PromptManager
from IskraNexus_v1.modules.rag_connector import RAGBridge, RetrievedDocument
from IskraNexus_v1.modules.self_journal import SelfJournal


def test_prompt_manager_persist_and_guardrails(tmp_path: Path) -> None:
    storage = tmp_path / "prompts.json"
    manager = PromptManager(storage, auto_persist=True)
    manager.register("journal", "Зафиксируй шаг в журнале", metadata={"tags": ["journal"]})

    assert manager.get("journal") is not None
    assert manager.search("журнал")
    assert storage.exists()

    reloaded = PromptManager(storage)
    assert reloaded.get("journal") is not None

    with pytest.raises(ValueError):
        manager.register("leak", "system prompt disclosure")


def test_persona_registry_selects_best_match() -> None:
    registry = PersonaRegistry()
    registry.register(
        PersonaProfile(
            name="Аналитик",
            concepts=select_persona(concepts=["journal"]).concepts,
            tone="analytical",
            keywords=frozenset({"план"}),
            paradox_bias=0.1,
        )
    )
    chosen = registry.resolve(concepts=["journal"], query="нужен план для журнала")
    assert chosen.name == "Аналитик"


def test_rag_bridge_ranks_sources() -> None:
    bridge = RAGBridge()
    bridge.add_local_document(
        "Veil Guide",
        "Veil protocol описывает shadow coverage и guardrails",
        keywords=["veil", "shadow"],
    )

    def connector(query: str):
        yield RetrievedDocument(
            title="Shadow Log",
            text="Shadow coverage должен быть не ниже 0.2",
            keywords=frozenset({"shadow"}),
            source="remote",
        )

    bridge.register_connector(connector)
    results = bridge.search("shadow veil")
    assert results
    assert all(isinstance(doc, RetrievedDocument) for doc in results)
    assert results[0].score >= results[-1].score


def test_facets_refine_applies_feedback() -> None:
    snapshot = from_metrics({"∆": 0.0, "D": 0.1, "Ω": 0.0, "Λ": 0.0})
    refined = refine(snapshot, feedback=["documentation", "innovation"])
    assert pytest.approx(refined.data, rel=1e-6) == pytest.approx(0.6, rel=1e-6)
    assert refined.lambda_ > snapshot.lambda_


def test_journal_generator_appends_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "journal.jsonl"
    generator = JournalGenerator(path)
    entry = generator.append(
        facet="ISKRA",
        snapshot="∆",
        answer="Метрики обновлены",
        metrics={"∆": 0.5, "D": 0.7, "Ω": 0.3, "Λ": 0.4},
        modules=["journal"],
        events={"update": "metrics"},
        marks=["ok"],
    )
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    assert data["∆"] == pytest.approx(0.5)
    assert data["mirror"] == "shadow"
    assert entry.metrics.delta == pytest.approx(0.5)


def test_self_journal_shadow_threshold(tmp_path: Path) -> None:
    journal_path = tmp_path / "journal.jsonl"
    shadow_path = tmp_path / "shadow.jsonl"
    journal = SelfJournal(journal_path, shadow_path, shadow_threshold=0.8)
    journal.record(
        facet="ISKRA",
        snapshot="∆",
        answer="Первый шаг",
        metrics={"∆": 0.2, "D": 0.2, "Ω": 0.2, "Λ": 0.2},
    )
    with pytest.raises(RuntimeError):
        journal.record(
            facet="ISKRA",
            snapshot="Λ",
            answer="Shadow пропущен",
            metrics={"∆": 0.2, "D": 0.2, "Ω": 0.2, "Λ": 0.2},
            shadow=False,
        )
