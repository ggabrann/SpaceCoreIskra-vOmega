
import re
def extract(text:str)->dict:
    lines=[l.strip() for l in text.splitlines() if l.strip()]
    motifs=[l for l in lines if re.search(r'(дыхани|ритм|волна|связк)', l, re.I)]
    return {"motifs": motifs[:20], "count": len(motifs)}
