#!/usr/bin/env python3
import argparse, json, sys, io
def iter_jsonl(p):
    try: f=io.open(p,"r",encoding="utf-8")
    except Exception: return []
    with f:
        for i,line in enumerate(f,1):
            line=line.strip()
            if not line: continue
            yield i, json.loads(line)
def validate(journal, shadow=None, window=5):
    errs, warns, items=[], [], list(iter_jsonl(journal))
    crisis=False; ritual=False
    for ln,e in items[-window:]:
        for k,lo,hi in (("∆",-3,3),("D",0,9),("Ω",-3,3)):
            if k not in e: errs.append(f"{journal}:{ln}: missing {k}"); continue
            if e[k]<lo or e[k]>hi: errs.append(f"{journal}:{ln}: {k} out of range")
        if e.get("Λ",0)<0: errs.append(f"{journal}:{ln}: Λ<0")
        if not e.get("mirror"): errs.append(f"{journal}:{ln}: mirror required")
        if e.get("∆",-99)<=-2: crisis=True
        if "ritual" in e: ritual=True
        if "Лиora" in json.dumps(e,ensure_ascii=False): warns.append(f"{journal}:{ln}: mixed alphabet: Лиora → Лиора")
    if crisis and not ritual: errs.append(f"{journal}: crisis-rule fail in last {window}")
    shadow_ratio=None
    if shadow:
        s=list(iter_jsonl(shadow)); shadow_ratio=len(s)/max(1,len(items))
        if shadow_ratio<0.2: warns.append(f"{shadow}: shadow_ratio {shadow_ratio:.2f} < 0.20")
    return errs,warns,{"entries":len(items),"shadow_ratio":shadow_ratio}
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("journal"); ap.add_argument("--shadow"); ap.add_argument("--window",type=int,default=5)
    a=ap.parse_args()
    errs,warns,stats=validate(a.journal,a.shadow,a.window)
    for w in warns: print("[WARN]",w)
    if errs:
        for e in errs: print("[FAIL]",e); sys.exit(1)
    print("[OK]",stats)
