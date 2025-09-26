#!/usr/bin/env python3
import sys, json, argparse

RANGE = {"∆": (-3, 3), "D": (0, 9), "Ω": (-3, 3), "Λ": (0, 9999)}

def _iter_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield i, json.loads(line)
            except Exception as ex:
                raise SystemExit(f"[FAIL] {path}:{i} invalid JSON: {ex}")

def _in_range(name, v):
    lo, hi = RANGE[name]
    return isinstance(v, (int, float)) and lo <= v <= hi

def validate(main_path: str, shadow_path: str, window: int = 50) -> int:
    errors = []
    main_entries = list(_iter_jsonl(main_path))[-window:] if window else list(_iter_jsonl(main_path))
    shadow_entries = list(_iter_jsonl(shadow_path)) if shadow_path else []

    # --- structural checks for main entries
    for ln, e in main_entries:
        where = f"{main_path}:{ln}"
        for k in ["∆", "D", "Ω", "Λ"]:
            if k not in e or not _in_range(k, e[k]):
                errors.append(f"{where}: metric {k} missing/out of range {e.get(k)}")
        if not e.get("mirror"):
            errors.append(f"{where}: mirror is required")
        ev = e.get("events")
        if not isinstance(ev, dict):
            errors.append(f"{where}: events must be an object with evidence[]")
        else:
            evid = ev.get("evidence")
            if not isinstance(evid, list) or len(evid) < 1:
                errors.append(f"{where}: events.evidence[] must have at least 1 item")
        # crisis rule
        if e.get("∆", 0) <= -2 and not e.get("ritual"):
            errors.append(f"{where}: crisis-rule: ritual is required when ∆≤−2")
        # agent_step (optional schema)
        if "agent_step" in e:
            s = e["agent_step"]
            if not isinstance(s, dict):
                errors.append(f"{where}: agent_step must be an object")
            else:
                if "approved" in s and not isinstance(s["approved"], bool):
                    errors.append(f"{where}: agent_step.approved must be boolean")
                if "evidence" in s:
                    if not isinstance(s["evidence"], list) or not s["evidence"]:
                        errors.append(f"{where}: agent_step.evidence must be non-empty list")

    # --- shadow coverage
    sr = len(shadow_entries) / max(1, len(main_entries))
    if sr < 0.2:
        errors.append(f"shadow_ratio {sr:.2f} < 0.20")

    # --- shadow mirror presence
    for ln, s in shadow_entries:
        if not s.get("mirror"):
            errors.append(f"{shadow_path}:{ln}: mirror is required in shadow entry")

    if errors:
        print("[FAIL] strict validation failed:")
        for msg in errors:
            print(" -", msg)
        return 2

    # summary
    avg = lambda k: sum(e.get(k, 0) for _, e in main_entries) / max(1, len(main_entries))
    print("[OK] strict validation passed")
    print(json.dumps({
        "count": len(main_entries),
        "avg": {"∆": avg("∆"), "D": avg("D"), "Ω": avg("Ω"), "Λ": avg("Λ")},
        "shadow_ratio": round(sr, 3),
    }, ensure_ascii=False))
    return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("main", help="path to JOURNAL.jsonl")
    ap.add_argument("--shadow", default="", help="path to SHADOW_JOURNAL.jsonl")
    ap.add_argument("--window", type=int, default=50)
    args = ap.parse_args()
    sys.exit(validate(args.main, args.shadow, args.window))

if __name__ == "__main__":
    main()
