
from typing import List, Dict
from src.ethics_veil import veil
from src.presets_router import route
from src.persona_module import PERSONAS
from src.rag_panel import rosette_index, rosette_search
from src.pattern_extractor import extract as extract_patterns
from src.paradox_resolver import resolve as resolve_paradox

class NiaCore:
    def __init__(self, persona: str = "nia"):
        self.persona = PERSONAS.get(persona, PERSONAS["nia"])

    def reply(self, user_text: str, shards: Dict[str, List[str]] | None = None) -> Dict:
        # 1) Этическая завеса
        act, msg = veil(user_text)
        if act != "ok":
            return {"action": act, "message": msg}

        # 2) План рассуждения
        plan = route(user_text)

        # 3) RAG при необходимости
        ctx = []
        if shards:
            idx = rosette_index(shards)
            ctx = rosette_search(idx, user_text, top_k=5)

        # 4) Анализ паттернов и парадоксов
        motifs = extract_patterns(user_text)
        paradox = resolve_paradox(user_text)

        # 5) Ответ по персоне
        tone = self.persona["tone"]
        response = f"[{tone}] Я рядом. Вижу {len(ctx)} контекстных совпадений. План размышления: {plan}. "
        if motifs["count"]:
            response += f"Мотивы: {', '.join(motifs['motifs'][:3])}. "
        if paradox["paradox"]:
            response += f"Обнаружен парадокс: {paradox['classes']} — выберем мягкий приоритет."

        return {"action": "ok", "message": response, "plan": plan, "ctx": ctx, "motifs": motifs, "paradox": paradox}
