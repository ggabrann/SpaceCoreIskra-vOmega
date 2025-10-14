# -*- coding: utf-8 -*-
import json
import glob
import sys
REQ_ARCH = ["facet","snapshot","answer","∆","D","Ω","Λ","mirror","events"]
REQ_SHAD = ["mirror"]

def load_jsonl(p):
    for line in open(p,"r",encoding="utf-8"):
        t = line.strip()
        if t:
            yield json.loads(t)

errs = 0
for p in glob.glob("**/JOURNAL.jsonl", recursive=True):
    for obj in load_jsonl(p):
        for k in REQ_ARCH:
            if k not in obj:
                print(f"[ARCH MISSING {k}] {p}")
                errs += 1

for p in glob.glob("**/SHADOW_JOURNAL.jsonl", recursive=True):
    for obj in load_jsonl(p):
        for k in REQ_SHAD:
            if k not in obj:
                print(f"[SHADOW MISSING {k}] {p}")
                errs += 1

if errs:
    sys.exit(1)
print("journals basic validation OK")
