# -*- coding: utf-8 -*-
import os
SUBSYSTEMS = ["SpaceCoreIskra_vΩ","GrokCoreIskra_vΓ","Kimi-Ω-Echo","Aethelgard-vΩ","IskraNexus-v1"]
min_ratio = 0.20
bad=[]
for sub in SUBSYSTEMS:
    j = os.path.join(sub,"JOURNAL.jsonl")
    s = os.path.join(sub,"SHADOW_JOURNAL.jsonl")
    aj = sum(1 for _ in open(j,"r",encoding="utf-8")) if os.path.exists(j) else 0
    sj = sum(1 for _ in open(s,"r",encoding="utf-8")) if os.path.exists(s) else 0
    ratio = (sj/aj) if aj else 0
    if ratio < min_ratio:
        bad.append((sub, ratio))
if bad:
    for sub, r in bad:
        print(f"[SHADOW<0.2] {sub}: {r:.2f}")
    raise SystemExit(1)
print("shadow coverage OK")
