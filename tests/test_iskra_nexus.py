import json
from pathlib import Path

from IskraNexus_v1.modules.orchestrator import Orchestrator


def test_orchestrator_pipeline():
    base_path = Path(__file__).resolve().parents[1] / "IskraNexus-v1"
    journal_path = base_path / "JOURNAL.jsonl"
    prompts_path = base_path / "prompts.json"
    if journal_path.exists():
        journal_path.unlink()
    if prompts_path.exists():
        prompts_path.unlink()

    orchestrator = Orchestrator(base_path=base_path)
    result = orchestrator.process("Расскажи о цели Iskra Nexus", mode="synthesis")

    assert result["response"], "Ответ должен быть непустым"
    assert result["mode"] == "synthesis"

    metrics = result["metrics"]
    for key in ("∆", "D", "Ω", "Λ"):
        assert key in metrics, f"Отсутствует метрика {key}"
        assert isinstance(metrics[key], int)
        assert metrics[key] >= 0

    shadow_log = result["shadow_log"]
    assert shadow_log, "Shadow-лог должен содержать шаги"
    assert any(entry["stage"] == "journal" for entry in shadow_log)

    journal_entry = result["journal_entry"]
    assert journal_entry["events"]["mode"] == "synthesis"
    assert journal_entry["mirror"] == "shadow-000"
    assert journal_entry["modules"] == orchestrator.components

    assert journal_path.exists()
    with journal_path.open("r", encoding="utf-8") as fh:
        lines = [line.strip() for line in fh if line.strip()]
    assert lines, "Журнал должен содержать запись"
    last_record = json.loads(lines[-1])
    assert last_record == journal_entry

    assert (metrics["D"] >= len(result["response"]))
