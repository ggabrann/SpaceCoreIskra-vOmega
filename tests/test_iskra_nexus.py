import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from IskraNexus_v1.modules.orchestrator import Orchestrator


@pytest.fixture()
def prepared_base(tmp_path: Path) -> Path:
    manifest_src = Path("IskraNexus-v1") / "iskra_nexus_v1_module.json"
    manifest_dst = tmp_path / "iskra_nexus_v1_module.json"
    manifest_dst.write_text(manifest_src.read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path


@pytest.mark.parametrize("mode", ["banality", "paradox", "synthesis"])
def test_orchestrator_pipeline(prepared_base: Path, mode: str) -> None:
    orchestrator = Orchestrator(base_path=prepared_base)
    query = "Расскажи о предназначении Iskra Nexus"
    result = orchestrator.process(query, mode=mode)

    assert result["response"], "Ответ должен быть непустым"
    assert result["mode"] == mode
    assert result["rag_hits"] and isinstance(result["rag_hits"], list)
    assert result["atelier"]["prompt_len"] > 0

    metrics = result["metrics"]
    for key in ("∆", "D", "Ω", "Λ"):
        assert key in metrics, f"Отсутствует метрика {key}"
        assert isinstance(metrics[key], int)
        assert metrics[key] >= 0

    shadow_log = result["shadow_log"]
    assert shadow_log, "Shadow-лог должен содержать шаги"
    assert any(entry["stage"] == "metrics" for entry in shadow_log)
    assert shadow_log[-1]["stage"] == "journal"

    journal_entry = result["journal_entry"]
    assert journal_entry["facet"] == mode
    assert journal_entry["snapshot"] == query
    assert journal_entry["mirror"] == "shadow-000"
    assert journal_entry["modules"] == orchestrator.components
    assert journal_entry["events"]["mode"] == mode
    assert "atelier" in journal_entry["marks"][0]

    journal_path = prepared_base / "JOURNAL.jsonl"
    assert journal_path.exists()
    lines = [line.strip() for line in journal_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert lines, "Журнал должен содержать запись"
    stored_entries = [json.loads(line) for line in lines]
    assert journal_entry in stored_entries

    prompts_payload = json.loads((prepared_base / "prompts.json").read_text(encoding="utf-8"))
    assert f"query::{mode}" in prompts_payload
    assert prompts_payload[f"query::{mode}"][-1]["meta"]["mode"] == mode
