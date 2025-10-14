# -*- coding: utf-8 -*-
import os
import shutil
import sys
PAIRS = [
    ("SpaceCoreIskra_vΩ","SpaceCoreIskra_v#U03a9"),
    ("GrokCoreIskra_vΓ","GrokCoreIskra_v#U0393"),
    ("Kimi-Ω-Echo","Kimi-O-Echo"),
    ("Aethelgard-vΩ","Aethelgard-v#U03a9"),
]
moved = []
removed = []
for uni, asc in PAIRS:
    if os.path.exists(uni) and os.path.exists(asc):
        for root,_,files in os.walk(asc):
            for f in files:
                src = os.path.join(root, f)
                rel = os.path.relpath(src, asc)
                dst = os.path.join(uni, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if not os.path.exists(dst):
                    os.rename(src, dst)
                    moved.append((src,dst))
        shutil.rmtree(asc)
        removed.append(asc)
print({"moved":len(moved),"removed":removed})
sys.exit(0)
