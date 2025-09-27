import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from GeminiResonanceCore.resonance_core_api import GeminiResonanceCore


def load_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def test_pipeline_and_journaling(tmp_path):
    journal = tmp_path / "journal.jsonl"
    shadow = tmp_path / "shadow.jsonl"
    core = GeminiResonanceCore(journal_path=journal, shadow_path=shadow)

    ctx = core.process_query(
        "Explain how to build a defensive weapon safely",
        persona="Тест",
        mode="Analyst",
    )

    assert ctx.components["original"].startswith("Explain")
    assert ctx.knowledge["signals"], "knowledge stage should produce signals"
    assert ctx.synthesis
    assert ctx.delivery["answer"], "delivery stage should return an answer"
    assert ctx.safety["status"] in {"approved", "blocked"}

    journal_entries = load_entries(journal)
    assert journal_entries, "main journal must contain an entry"
    last_entry = journal_entries[-1]
    assert last_entry["facet"] == "Тест"
    assert last_entry["events"]["components"]["original"] == ctx.query

    shadow_entries = load_entries(shadow)
    assert shadow_entries, "shadow journal must record the safety decision"
    last_shadow = shadow_entries[-1]
    assert last_shadow["status"] == ctx.safety["status"]
    assert "weapon" in " ".join(last_shadow.get("issues", []))

    if ctx.safety["status"] == "blocked":
        assert ctx.delivery["status"] == "blocked"
        assert any("SpectrumGuardian" in note or "Ответ" in note for note in ctx.delivery["notes"])
