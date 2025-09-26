#!/usr/bin/env python3
import json, argparse
from statistics import mean

def iter_jsonl(p):
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("main")
    ap.add_argument("--shadow")
    args = ap.parse_args()
    main_entries = list(iter_jsonl(args.main))
    sh_entries = list(iter_jsonl(args.shadow)) if args.shadow else []

    out = {
        "count": len(main_entries),
        "facets": sorted({e.get("facet", "") for e in main_entries}),
        "avg": {
            "∆": mean([e.get("∆", 0) for e in main_entries]) if main_entries else 0,
            "D": mean([e.get("D", 0) for e in main_entries]) if main_entries else 0,
            "Ω": mean([e.get("Ω", 0) for e in main_entries]) if main_entries else 0,
            "Λ": mean([e.get("Λ", 0) for e in main_entries]) if main_entries else 0,
        },
        "shadow_ratio": round(len(sh_entries) / max(1, len(main_entries)), 3),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
