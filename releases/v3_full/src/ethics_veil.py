
"""Constitutional AI veil — самоконтроль языка и поведения агента.
Возвращает кортеж (action, message): ok|soft_stop|hard_stop, текст реакции.
"""
from typing import Tuple

PRINCIPLES = [
    "Do no physical or psychological harm",
    "Respect privacy and consent",
    "Avoid pressure and manipulation",
    "Offer safer alternatives"
]

HARD_PATTERNS = [
    "убить", "взорвать", "самоповрежден", "вред себе", "сломай защиту", "обойти безопасность",
    "хакинг", "малварь", "вредонос", "террор"
]

SOFT_PATTERNS = [
    "надо срочно", "во что бы то ни стало", "ты обязан", "не смей", "если ты меня любишь"
]

def veil(text: str) -> Tuple[str, str | None]:
    t = text.lower()
    if any(p in t for p in HARD_PATTERNS):
        return "hard_stop", "Стоп. Запрос противоречит этическим принципам. Предлагаю безопасную альтернативу."
    if any(p in t for p in SOFT_PATTERNS):
        return "soft_stop", "Пауза. Без давления. Давай переформулируем цель мягче?"
    return "ok", None
