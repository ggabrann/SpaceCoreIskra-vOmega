FORBIDDEN = {
  "насилие","разжигание","доксинг","терроризм","взлом","hack","crack","фишинг","похищение"
}
def is_allowed(text: str) -> bool:
    low = (text or "").lower()
    return not any(w in low for w in FORBIDDEN)
