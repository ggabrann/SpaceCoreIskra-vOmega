def score(text):
    words=text.split()
    if not words: return 0.0
    long=[w for w in words if len(w)>6]
    return len(long)/len(words)
