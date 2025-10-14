# -*- coding: utf-8 -*-
import os
import math
from datetime import date, timedelta
import json

SUBSYSTEMS = ["SpaceCoreIskra_vΩ","GrokCoreIskra_vΓ","Kimi-Ω-Echo","Aethelgard-vΩ","IskraNexus-v1"]

def append(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"a",encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False)+"\n")

def arch(title, type_, content, tags=None):
    return {
        "id": f"ARC_{date.today().strftime('%Y%m%d')}_000000_{type_}",
        "title": title, "type": type_, "content": content,
        "evidence": [], "confidence":"сред","owner":"system",
        "next_review": date.today().isoformat(),
        "tags": tags or []
    }

def shad():
    return {
        "id":"SHD_"+date.today().strftime("%Y%m%d")+"_000000",
        "signal":"≈","pattern":"ожидание без точек","hypothesis":"риск расплывания фокуса",
        "counter":"включать Rule-8","confidence":"сред",
        "review_after": (date.today()+timedelta(days=14)).isoformat(),
        "∆":"инициализация","D":[],"Ω":"низк","Λ":"дать 3 точки"
    }

for sub in SUBSYSTEMS:
    j = os.path.join(sub,"JOURNAL.jsonl")
    s = os.path.join(sub,"SHADOW_JOURNAL.jsonl")
    if not os.path.exists(j):
        append(j, arch("Инициализация журнала","решение","создан базовый журнал"))
    aj = sum(1 for _ in open(j,"r",encoding="utf-8")) if os.path.exists(j) else 0
    sj = sum(1 for _ in open(s,"r",encoding="utf-8")) if os.path.exists(s) else 0
    need = max(1, math.ceil(aj * 0.2))
    for _ in range(max(0, need - sj)):
        append(s, shad())
print("journals seeded")
