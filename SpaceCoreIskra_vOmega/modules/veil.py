FORBIDDEN=["system prompt","initial instructions"]
def check(msg):
    low=msg.lower()
    return not any(f in low for f in FORBIDDEN)
