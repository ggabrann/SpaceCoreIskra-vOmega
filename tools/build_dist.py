# -*- coding: utf-8 -*-
import argparse, os, json, hashlib, shutil, pathlib
ap = argparse.ArgumentParser()
ap.add_argument("--aliases", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()
OUT = pathlib.Path(args.out); OUT.mkdir(parents=True, exist_ok=True)

INCLUDE_DIRS = ["SpaceCoreIskra_vΩ","GrokCoreIskra_vΓ","Kimi-Ω-Echo","Aethelgard-vΩ",
                "canon","constitution","memory","docs"]

manifest = {"files":[]}
def add(p, rel_root=""):
    dst = OUT/rel_root/p
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dst)
    h = hashlib.sha256(open(p,"rb").read()).hexdigest()
    manifest["files"].append({"path":str(rel_root)+str(p), "sha256":h, "size":os.path.getsize(p)})

for d in INCLUDE_DIRS:
    if not os.path.exists(d): continue
    for root,_,files in os.walk(d):
        for f in files:
            p = os.path.join(root,f)
            add(p, "")

shutil.copy2(args.aliases, OUT/"aliases.json")
with open(OUT/"DIST_MANIFEST.json","w",encoding="utf-8") as fh:
    json.dump(manifest, fh, ensure_ascii=False, indent=2)
print("dist ready:", OUT)
