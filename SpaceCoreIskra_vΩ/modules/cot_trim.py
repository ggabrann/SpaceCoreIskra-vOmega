from typing import Tuple


def trim(text: str, max_len: int = 200) -> str:
    if not text:
        return text
    if len(text) <= max_len:
        return text
    return text[-max_len:]


def extract_answer(text: str) -> Tuple[str, str]:
    """Возвращает (reasoning, answer)."""
    if "Answer:" in text:
        reasoning, answer = text.split("Answer:", maxsplit=1)
        return reasoning.strip(), answer.strip()
    return text, ""
