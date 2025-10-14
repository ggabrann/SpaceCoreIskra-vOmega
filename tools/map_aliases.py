# -*- coding: utf-8 -*-
import argparse
import json
import os
import unicodedata
import sys
ap = argparse.ArgumentParser()
ap.add_argument("--check", action="store_true")
ap.add_argument("--emit", action="store_true")
ap.add_argument("--out", default="aliases.json")
args = ap.parse_args()

def ascii_alias(p:str)->str:
    n = unicodedata.normalize("NFKD", p)
    a = "".join(ch for ch in n if ord(ch) < 128)
    return a.replace(" ", "_")

aliases = {}
for root,_,files in os.walk("."):
    rp = root.replace("\\","/")
    if "/.git" in rp or "/dist" in rp or "/node_modules" in rp:
        continue
    for f in files:
        p = os.path.join(rp, f).replace("\\","/")
        a = ascii_alias(p)
        if a != p:
            aliases[p] = a

if args.check:
    missing = [u for u in aliases if not os.path.exists(u)]
    dup_dirs = [d for d in os.listdir(".") if d.endswith("#U03a9") or d.endswith("#U0393") or d=="Kimi-O-Echo"]
    if missing:
        print("\n".join(f"[MISSING Unicode] {m}" for m in missing))
        sys.exit(1)
    if dup_dirs:
        print("\n".join(f"[DUP-DIR] {d}" for d in dup_dirs))
        sys.exit(1)
    print("OK: Unicode canonical structure")
if args.emit:
    with open(args.out,"w",encoding="utf-8") as fh:
        json.dump(aliases, fh, ensure_ascii=False, indent=2)
    print(f"aliases -> {args.out}")
