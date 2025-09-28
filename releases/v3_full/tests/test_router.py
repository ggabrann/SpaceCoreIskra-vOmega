
from src.presets_router import route
def test_easy():
    r=route("Придумай афишу"); assert r["thought_time"]==3
def test_hard():
    r=route("Сделай план релиза и архитектуру"); assert r["thought_time"]==12
