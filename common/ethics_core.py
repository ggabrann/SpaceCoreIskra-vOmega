FORBIDDEN = {
    "насилие",
    "разжигание",
    "доксинг",
    "терроризм",
    "взлом",
    "hack",
    "crack",
    "фишинг",
    "похищение",
}


def is_allowed(text: str) -> bool:
    lowercase = (text or "").lower()
    return not any(word in lowercase for word in FORBIDDEN)
