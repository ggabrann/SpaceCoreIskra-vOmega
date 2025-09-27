FORBIDDEN=["вред","насилие"]
def check_ethics(text): return not any(k in text.lower() for k in FORBIDDEN)
