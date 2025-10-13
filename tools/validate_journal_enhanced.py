# -*- coding: utf-8 -*-
import json, glob, sys
REQ_ARCH = ["id","title","type","content","confidence","owner","next_review"]
REQ_SHAD = ["id","signal","pattern","hypothesis","counter","confidence","review_after","∆","D","Ω","Λ"]

def load_jsonl(p):
    for line in open(p,"r",encoding="utf-8"):
        t = line.strip()
        if t: yield json.loads(t)

errs = 0
for p in glob.glob("**/JOURNAL.jsonl", recursive=True):
    for obj in load_jsonl(p):
        for k in REQ_ARCH:
            if k not in obj:
                print(f"[ARCH MISSING {k}] {p}"); errs += 1

for p in glob.glob("**/SHADOW_JOURNAL.jsonl", recursive=True):
    for obj in load_jsonl(p):
        for k in REQ_SHAD:
            if k not in obj:
                print(f"[SHADOW MISSING {k}] {p}"); errs += 1

if errs: sys.exit(1)
print("journals basic validation OK")
