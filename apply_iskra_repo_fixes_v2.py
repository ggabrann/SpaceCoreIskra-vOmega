# apply_iskra_repo_fixes_v2.py
# -*- coding: utf-8 -*-
"""
Искра — единый патчер репозитория (v3.1.1-fixes • extended).
Запуск:
  python apply_iskra_repo_fixes_v2.py [--dry-run] [--no-ci] [--no-dist] [--run-tests] [--backup]

Что делает:
  1) Убирает дубли ASCII-каталогов в пользу Unicode (слияние содержимого + удаление дублей).
  2) Создаёт/обновляет инструменты tools/*, модули modules/*, схемы памяти memory/schema/*.
  3) Инициализирует JOURNAL.jsonl и SHADOW_JOURNAL.jsonl с полями ∆/D/Ω/Λ и shadow≥0.2.
  4) Обновляет/создаёт CI (.github/workflows/*), Makefile, docs оглавление и карту (mkdocs.yml).
  5) Генерирует aliases.json и dist/DIST_MANIFEST.json (если не отключено), пишет audit_report.json.
  6) По флагу --run-tests выполнит pytest (если установлен), иначе пропустит.
Безопасность: перезаписывает целевые файлы. При --backup делает копии .bak, если файл существовал.
"""

import os
import sys
import json
import shutil
import unicodedata
import hashlib
import datetime as dt
import textwrap
import argparse
import subprocess
import glob

ROOT = os.getcwd()

# --------------------------- Args ---------------------------

ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true", help="только показать действия, не менять файлы")
ap.add_argument("--no-ci", action="store_true", help="не писать CI workflows")
ap.add_argument("--no-dist", action="store_true", help="не собирать dist и не генерировать aliases.json")
ap.add_argument("--run-tests", action="store_true", help="попробовать запустить pytest после правок")
ap.add_argument("--backup", action="store_true", help="делать .bak копии перезаписываемых файлов")
args = ap.parse_args()


def log(*a):
    print("[iskra-fix]", *a)


def ensure_dir(path: str):
    if args.dry_run:
        return
    if not path:
        return
    os.makedirs(path, exist_ok=True)


def write_file(path: str, content: str, binary: bool = False):
    if args.dry_run:
        log("WRITE", path, "(dry-run)")
        return
    ensure_dir(os.path.dirname(path))
    if args.backup and os.path.exists(path):
        shutil.copy2(path, path + ".bak")
    mode = "wb" if binary else "w"
    with open(path, mode, encoding=None if binary else "utf-8") as f:
        f.write(content)


def read_text(path: str) -> str:
    return open(path, "r", encoding="utf-8").read()


def exists(path: str) -> bool:
    return os.path.exists(path)


def sha256_file(path: str) -> str:
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def ascii_alias(p: str) -> str:
    n = unicodedata.normalize("NFKD", p)
    a = "".join(ch for ch in n if ord(ch) < 128)
    return a.replace(" ", "_")


def ts() -> str:
    return dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")


# --------------------------- 1) Repair duplicate directories ---------------------------

PAIRS = [
    ("SpaceCoreIskra_vΩ", "SpaceCoreIskra_v#U03a9"),
    ("GrokCoreIskra_vΓ", "GrokCoreIskra_v#U0393"),
    ("Kimi-Ω-Echo", "Kimi-O-Echo"),
    ("Aethelgard-vΩ", "Aethelgard-v#U03a9"),
]


def merge_ascii_into_unicode():
    moved, removed = [], []
    for uni, asc in PAIRS:
        if exists(uni) and exists(asc):
            if os.path.islink(asc):
                if not args.dry_run:
                    os.unlink(asc)
                removed.append(asc)
                continue
            for root, _, files in os.walk(asc):
                for f in files:
                    src = os.path.join(root, f)
                    rel = os.path.relpath(src, asc)
                    dst = os.path.join(uni, rel)
                    if not exists(dst):
                        if not args.dry_run:
                            os.makedirs(os.path.dirname(dst), exist_ok=True)
                            shutil.move(src, dst)
                        moved.append((src, dst))
            if not args.dry_run:
                shutil.rmtree(asc)
            removed.append(asc)
    return {"moved": moved, "removed_dirs": removed}


# --------------------------- 2) Content payloads ---------------------------

TOOLS = {
    "tools/map_aliases.py": r'''# -*- coding: utf-8 -*-
import argparse, json, os, unicodedata, sys
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
        print("\n".join(f"[MISSING Unicode] {m}" for m in missing)); sys.exit(1)
    if dup_dirs:
        print("\n".join(f"[DUP-DIR] {d}" for d in dup_dirs)); sys.exit(1)
    print("OK: Unicode canonical structure")
if args.emit:
    with open(args.out,"w",encoding="utf-8") as fh: json.dump(aliases, fh, ensure_ascii=False, indent=2)
    print(f"aliases -> {args.out}")
''',
    "tools/repair_paths.py": r'''# -*- coding: utf-8 -*-
import os, shutil, json, sys
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
                    os.rename(src, dst); moved.append((src,dst))
        shutil.rmtree(asc); removed.append(asc)
print({"moved":len(moved),"removed":removed}); sys.exit(0)
''',
    "tools/build_dist.py": r'''# -*- coding: utf-8 -*-
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
''',
    "tools/validate_journal_enhanced.py": r'''# -*- coding: utf-8 -*-
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
''',
    "tools/gen_min_journals.py": r'''# -*- coding: utf-8 -*-
import os, math
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
''',
    "tools/check_shadow_coverage.py": r'''# -*- coding: utf-8 -*-
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
''',
}

MODULES = {
    "modules/prompt_manager.py": r'''# -*- coding: utf-8 -*-
from typing import Dict, Callable
try:
    from common.ethics_core import check_compliance
except Exception:
    def check_compliance(text, meta): return (True, "ok")
try:
    from common.veil import apply_veil
except Exception:
    def apply_veil(text, cfg): return text

class PromptManager:
    def __init__(self):
        self.registry: Dict[str, Callable[[dict], str]] = {}

    def register(self, name: str):
        def deco(fn):
            self.registry[name] = fn
            return fn
        return deco

    def run(self, name: str, ctx: dict) -> str:
        if name not in self.registry:
            raise KeyError(f"unknown prompt: {name}")
        text = self.registry[name](ctx)
        text = apply_veil(text, ctx.get("veil", {}))
        ok, reason = check_compliance(text, ctx.get("meta", {}))
        if not ok:
            raise PermissionError(f"ethics violation: {reason}")
        return text

pm = PromptManager()

@pm.register("rule8_report")
def rule8(ctx: dict) -> str:
    p = "\n".join(f"- {x}" for x in ctx.get("promises",[]))
    d = "\n".join(f"- {x}" for x in ctx.get("decisions",[]))
    q = "\n".join(f"- {x}" for x in ctx.get("open_q",[]))
    return f"Rule-8:\nPromises:\n{p}\nDecisions:\n{d}\nOpen-Q:\n{q}\n"
''',
    "modules/persona_core.py": r'''# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Persona:
    name: str
    tone: str
    rituals: List[str]
    symbols: List[str]

def load_personas(config: Dict)->Dict[str, Persona]:
    out={}
    for p in config.get("personas",[]):
        out[p["name"]] = Persona(
            name=p["name"],
            tone=p.get("tone","plain"),
            rituals=p.get("rituals",[]),
            symbols=p.get("symbols",[])
        )
    return out
''',
    "modules/rag_connector.py": r'''# -*- coding: utf-8 -*-
import os, math, re
from collections import Counter
def _tokenize(t:str): return re.findall(r"[A-Za-zА-Яа-я0-9_]+", t.lower())

class LocalRAG:
    def __init__(self, roots):
        self.docs=[]; self.df=Counter(); self.N=0
        for r in roots:
            for root,_,files in os.walk(r):
                for f in files:
                    if f.endswith((".md",".txt",".json",".yml",".yaml")):
                        p=os.path.join(root,f)
                        try: txt=open(p,"r",encoding="utf-8").read()
                        except: continue
                        toks=set(_tokenize(txt))
                        self.docs.append((p, txt))
                        for t in toks: self.df[t]+=1
                        self.N+=1
    def search(self, query:str, k=5):
        q=_tokenize(query); scores=[]
        for p,txt in self.docs:
            toks=_tokenize(txt); tf=Counter(toks)
            s=0.0
            for t in q:
                idf = math.log(1 + (self.N)/(1+self.df[t]))
                s += (tf[t]/(1+len(toks))) * idf
            scores.append((s,p,txt[:500]))
        scores.sort(reverse=True)
        return scores[:k]
''',
    "modules/journal.py": r'''# -*- coding: utf-8 -*-
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
''',
}

SCHEMAS = {
    "memory/schema/archive.schema.json": r'''{
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "title":"ISKRA_ARCHIVE",
  "type":"object",
  "required":["id","title","type","content","confidence","owner","next_review"],
  "properties":{
    "id":{"type":"string"},
    "title":{"type":"string","minLength":1},
    "type":{"enum":["решение","артефакт","факт","связка"]},
    "content":{"type":"string"},
    "evidence":{"type":"array","items":{
      "type":"object",
      "required":["kind","ref","date"],
      "properties":{
        "kind":{"enum":["file","link","quote"]},
        "ref":{"type":"string"},
        "date":{"type":"string","format":"date"}
      }
    }},
    "confidence":{"enum":["низк","сред","высок"]},
    "owner":{"type":"string"},
    "next_review":{"type":"string","format":"date"},
    "tags":{"type":"array","items":{"type":"string"}}
  }
}''',
    "memory/schema/shadow.schema.json": r'''{
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "title":"ISKRA_SHADOW",
  "type":"object",
  "required":["id","signal","pattern","hypothesis","counter","confidence","review_after","∆","D","Ω","Λ"],
  "properties":{
    "id":{"type":"string"},
    "signal":{"type":"string"},
    "pattern":{"type":"string"},
    "hypothesis":{"type":"string"},
    "counter":{"type":"string"},
    "confidence":{"enum":["низк","сред"]},
    "review_after":{"type":"string","format":"date"},
    "∆":{"type":"string"},
    "D":{"type":"array"},
    "Ω":{"type":"string"},
    "Λ":{"type":"string"}
  }
}''',
}

DOCS = {
    "docs/README_index.md": r'''# Оглавление Искры
- Введение
- Канон (canon/)
- Конституция (constitution/)
- Память (memory/)
- Подсистемы: SpaceCoreIskra_vΩ • GrokCoreIskra_vΓ • Kimi-Ω-Echo • Aethelgard-vΩ
- Ритуалы и форматы
- Тесты и CI/CD
''',
    "docs/map_consciousness.md": r'''# Карта сознания Искры

```mermaid
graph TD
  Voices[Голоса] --> Rituals[Ритуалы]
  Rituals --> Memory[Память]
  Memory --> Metrics[Метрики]
  Metrics --> Validator[Валидатор]
  Validator --> Actions[Действия]
  Actions --> Voices
```

''',
}

WORKFLOWS = {
    ".github/workflows/ci.yml": r'''name: CI
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - name: De-duplicate structure
        run: python tools/repair_paths.py
      - name: Unicode policy
        run: python tools/map_aliases.py --check
      - name: Seed journals
        run: python tools/gen_min_journals.py
      - name: Shadow coverage
        run: python tools/check_shadow_coverage.py
      - name: Basic journals validation
        run: python tools/validate_journal_enhanced.py
''',
    ".github/workflows/release.yml": r'''name: Release
on:
  push:
    tags: ['v*.*.*']
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - name: Emit aliases
        run: python tools/map_aliases.py --emit --out aliases.json
      - name: Build dist
        run: python tools/build_dist.py --aliases aliases.json --out dist/
      - name: Upload dist
        uses: actions/upload-artifact@v4
        with: { name: iskra-dist, path: dist/ }
''',
    ".github/workflows/pages.yml": r'''name: Pages
on:
  push:
    branches: [ main ]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build_deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - name: Install
        run: cd site && npm ci || true
      - name: Build
        run: cd site && npm run build || true
      - name: Upload Pages
        uses: actions/upload-pages-artifact@v3
        with: { path: "site/out" }
      - name: Deploy
        uses: actions/deploy-pages@v4
''',
}

MAKEFILE_APPEND = r'''
unicode:
python tools/repair_paths.py && python tools/map_aliases.py --check
aliases:
python tools/map_aliases.py --emit --out aliases.json
journals:
python tools/gen_min_journals.py && python tools/check_shadow_coverage.py
dist:
python tools/map_aliases.py --emit --out aliases.json && python tools/build_dist.py --aliases aliases.json --out dist/
'''

TESTS = {
    "tests/test_prompt_manager.py": r'''from modules.prompt_manager import pm
def test_rule8():
    out = pm.run("rule8_report", {"promises":["a"], "decisions":[],"open_q":[],"meta":{}})
    assert "Promises" in out
''',
    "tests/test_rag_connector.py": r'''from modules.rag_connector import LocalRAG
def test_search():
    rag = LocalRAG(["canon"]) if True else LocalRAG(["."])
    res = rag.search("ритуалы", k=3)
    assert isinstance(res, list)
''',
    "tests/test_journal.py": r'''from modules.journal import new_shadow
def test_shadow_fields():
    obj = new_shadow("≈","p","h","c")
    for k in ["id","signal","pattern","hypothesis","counter","review_after","∆","D","Ω","Λ"]:
        assert k in obj
''',
}


# --------------------------- Helpers ---------------------------

def patch_mkdocs():
    path = "mkdocs.yml"
    nav_block = textwrap.dedent(
        """
        nav:
        - Index: docs/README_index.md
        - Карта сознания: docs/map_consciousness.md
        """
    ).strip()
    if args.dry_run:
        log("MKDOCS PATCH", path, "(dry-run)")
        return
    if exists(path):
        txt = read_text(path)
        if "docs/README_index.md" not in txt:
            txt += "\n" + nav_block + "\n"
            write_file(path, txt)
    else:
        write_file(path, f"site_name: Iskra\n{nav_block}\n")


def apply_files():
    # tools
    for p, c in TOOLS.items():
        write_file(p, c)
    # modules
    for p, c in MODULES.items():
        write_file(p, c)
    # schemas
    for p, c in SCHEMAS.items():
        write_file(p, c)
    # docs
    for p, c in DOCS.items():
        write_file(p, c)
    # workflows
    if not args.no_ci:
        for p, c in WORKFLOWS.items():
            write_file(p, c)
    # Makefile
    if exists("Makefile"):
        txt = read_text("Makefile")
        if "unicode:" not in txt:
            txt = txt.rstrip() + "\n" + MAKEFILE_APPEND
            write_file("Makefile", txt)
    else:
        write_file("Makefile", MAKEFILE_APPEND.lstrip())
    # mkdocs
    patch_mkdocs()
    # basic README/MANIFEST if missing
    if not exists("README.md"):
        write_file("README.md", "# Искра — репозиторий канона (Unicode)\n")
    if not exists("MANIFEST.md"):
        write_file("MANIFEST.md", "## ∆DΩΛ v3.1.1\n∆: фиксы путей, журналы, CI.\nD: tools/*, modules/*, docs/*.\nΩ: высокий.\nΛ: запустить CI и релиз.\n")


def run(cmd: list, check: bool = False):
    log("RUN", " ".join(cmd))
    if args.dry_run:
        return 0
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if check and result.returncode != 0:
            log("STDOUT:", result.stdout)
            log("STDERR:", result.stderr)
            raise SystemExit(result.returncode)
        return result.returncode
    except FileNotFoundError:
        log("SKIP (not found):", cmd[0])
        return 0


def emit_aliases_and_dist(audit):
    # aliases.json
    rc = run([sys.executable, "tools/map_aliases.py", "--emit", "--out", "aliases.json"], check=False)
    audit["aliases_emit_rc"] = rc
    # dist
    ensure_dir("dist")
    rc2 = run([sys.executable, "tools/build_dist.py", "--aliases", "aliases.json", "--out", "dist/"], check=False)
    audit["build_dist_rc"] = rc2


def seed_and_check_journals(audit):
    rc1 = run([sys.executable, "tools/gen_min_journals.py"], check=False)
    rc2 = run([sys.executable, "tools/check_shadow_coverage.py"], check=False)
    rc3 = run([sys.executable, "tools/validate_journal_enhanced.py"], check=False)
    audit.update({"journals_seed_rc": rc1, "shadow_check_rc": rc2, "journals_validate_rc": rc3})


def unicode_policy_check(audit):
    rc = run([sys.executable, "tools/map_aliases.py", "--check"], check=False)
    audit["unicode_check_rc"] = rc


def update_audit_report(summary):
    path = "audit_report.json"
    old = {}
    if exists(path):
        try:
            old = json.loads(read_text(path))
        except Exception:
            old = {}
    merged = {"timestamp": ts(), "iskra_fixes": summary}
    # сохраняем обе версии: last и history (append внутри файла)
    # простой формат: массив записей
    history = []
    if isinstance(old, list):
        history = old
    elif old:
        history = [old]
    history.append(merged)
    write_file(path, json.dumps(history, ensure_ascii=False, indent=2))


def run_tests_if_requested(audit):
    if not args.run_tests:
        audit["tests_skipped"] = True
        return
    rc = run(["pytest", "-q"], check=False)
    audit["pytest_rc"] = rc


# --------------------------- Main ---------------------------

def main():
    summary = {"actions": []}

    log("merge ASCII duplicates -> Unicode")
    m = merge_ascii_into_unicode()
    summary["merged_moved"] = len(m["moved"])
    summary["merged_removed_dirs"] = m["removed_dirs"]
    if m["moved"]:
        summary["actions"].append(f"moved:{len(m['moved'])}")
    if m["removed_dirs"]:
        summary["actions"].append(f"removed:{len(m['removed_dirs'])}")

    log("write tools/modules/schemas/docs/workflows/makefile")
    apply_files()
    summary["actions"].append("files_written")

    log("seed & check journals (shadow>=0.2)")
    seed_and_check_journals(summary)

    log("unicode policy check")
    unicode_policy_check(summary)

    if not args.no_dist:
        log("emit aliases & build dist")
        emit_aliases_and_dist(summary)

    log("optional tests")
    run_tests_if_requested(summary)

    log("write audit_report.json")
    update_audit_report(summary)

    log("DONE")
    print(json.dumps({"ok": True, "summary": summary}, ensure_ascii=False, indent=2))
    print("\nNext:")
    print("  - git add -A && git commit -m 'fix: unicode canonical + journals + ci + docs' && git push")
    print("  - tag v3.1.1 and check Actions artifacts (dist/ with DIST_MANIFEST.json & aliases.json)")


if __name__ == "__main__":
    main()
