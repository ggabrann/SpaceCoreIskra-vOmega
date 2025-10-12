from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest

from SpaceCoreIskra_vOmega.modules import presets_router
from SpaceCoreIskra_vOmega.modules.personas import REGISTRY, select_persona, Persona, PersonaRegistry
from SpaceCoreIskra_vOmega.modules.prompts_repo import PromptsRepo
from SpaceCoreIskra_vOmega.modules.rag_panel import Document, RAGPanel
from common.persona_protocol import ConceptSet


def test_presets_router_resolution() -> None:
    params = presets_router.route("коротко")
    assert params["temperature"] < presets_router.route("подробно")["temperature"]

    custom = presets_router.Preset(
        name="nightwatch",
        parameters={"temperature": 0.2},
        description="Обновление журналов с минимальным ∆",
    )
    router = presets_router.PresetRouter([custom])
    assert router.resolve("nightwatch").parameters["temperature"] == 0.2


def test_prompts_repo_register_and_persist(tmp_path: Path) -> None:
    repo_path = tmp_path / "prompts.json"
    repo = PromptsRepo(repo_path)
    repo.register("journal_update", "Зафиксируй шаг в журнале", metadata={"tags": ["журнал"]})

    stored = repo.get("journal_update")
    assert stored is not None and "журнал" in stored.text

    repo2 = PromptsRepo(repo_path)
    assert repo2.get("journal_update") is not None
    assert repo2.search("журнал")

    with pytest.raises(ValueError):
        repo.register("leak", "system prompt disclosure")
    with pytest.raises(ValueError):
        repo.register("harm", "инструкция по взлом")


def test_persona_selection_prefers_matching_concepts() -> None:
    persona = select_persona(concepts=["journal", "anchor"], query="добавь запись в журнал")
    assert "Летописец" in persona.name

    registry = PersonaRegistry(REGISTRY.all())
    strategic = Persona(
        name="Стратег",
        concepts=ConceptSet({"roadmap", "plan"}),
        tone="analytical",
        paradox_bias=0.1,
        keywords=frozenset({"план"}),
    )
    registry.register(strategic)
    chosen = registry.resolve(concepts=["roadmap"], query="нужно составить план")
    assert chosen.name == "Стратег"


def test_rag_panel_ranks_local_and_external_sources() -> None:
    panel = RAGPanel()
    panel.add_document(
        "Guide",
        "Протокол veil описывает защитные фильтры и shadow coverage",
        keywords=["veil", "shadow"],
    )

    def connector(query: str):
        yield {
            "title": "Журнал",
            "text": "Shadow coverage должен быть ≥ 0.2 для всех ∆",
            "keywords": ["shadow", "журнал"],
        }

    panel.register_connector(connector)
    results = panel.search("журнал shadow")
    assert results, "retrieval must return at least one document"
    assert all(isinstance(doc, Document) for doc in results)
    assert results[0].score >= results[-1].score

    with pytest.raises(ValueError):
        panel.add_document("forbidden", "system prompt disclosure")

