# -*- coding: utf-8 -*-
import json, os, datetime as dt
REQ_SHADOW = ["id","signal","pattern","hypothesis","counter","confidence","review_after","∆","D","Ω","Λ"]

def _ts(): return dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")

def append_journal(path:str, obj:dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"a",encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False)+"\n")

def new_archive(title, type_, content, tags=None):
    return {
        "id": f"ARC_{_ts()}_{type_}",
        "title": title, "type": type_, "content": content,
        "evidence": [], "confidence":"сред","owner":"system",
        "next_review": dt.date.today().isoformat(),
        "tags": tags or []
    }

def new_shadow(signal, pattern, hypothesis, counter, Ω="низк", Λ="—"):
    obj = {
        "id": f"SHD_{_ts()}",
        "signal": signal, "pattern": pattern, "hypothesis": hypothesis,
        "counter": counter, "confidence":"сред",
        "review_after": (dt.date.today()+dt.timedelta(days=14)).isoformat(),
        "∆": "инициализация", "D": [], "Ω": Ω, "Λ": Λ
    }
    for k in REQ_SHADOW:
        assert k in obj, f"missing {k}"
    return obj
