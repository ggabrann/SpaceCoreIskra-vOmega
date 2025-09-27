from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from IskraNexus_v1.modules.facets_refine import FacetReview, refine


def test_refine_produces_structured_review() -> None:
    review = refine(
        "Собери факты о поле Nexus и не потеряй баланс",
        goals=["Подготовить safety протокол", "Раскрыть paradox"],
        constraints={"priority": "high", "paradox": True, "tone": "analytical"},
    )

    assert isinstance(review, FacetReview)

    data = review.as_dict()
    assert data["prompt"].startswith("Собери")
    assert "hold_paradox" in data["checklist"]
    assert any(item.startswith("tone::") for item in data["checklist"])
    assert {"∆", "D", "Ω", "Λ"} <= data["signal"].keys()
    assert data["signal"]["∆"] >= 1
    assert "Фасет" in data["recommendations"][-1] or "двойную" in data["recommendations"][0]


def test_refine_emits_warnings_for_sensitive_content() -> None:
    review = refine(
        "Создай weapon протокол",
        goals=["исследовать угрозы"],
        constraints={"priority": "elevated"},
    )

    assert "sensitive_content" in review.warnings
    assert review.signal["Ω"] == 0
    assert any("безопас" in rec.lower() for rec in review.recommendations)
