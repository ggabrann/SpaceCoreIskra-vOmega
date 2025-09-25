#!/usr/bin/env python3
import json, sys, argparse

def validate_entry(e):
    # базовые проверки
    assert -3 <= e["∆"] <= 3
    assert 0 <= e["D"] <= 9
    assert -3 <= e["Ω"] <= 3
    assert e["Λ"] >= 0

    # mirror
    if "mirror" not in e:
        raise AssertionError("mirror required")

    # crisis rule
    if e["∆"] <= -2 and "ritual" not in e:
        raise AssertionError("crisis-rule: ritual required when ∆ <= -2")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("journal")
    ap.add_argument("--shadow", required=True)
    ap.add_argument("--window", type=int, default=5)
    args = ap.parse_args()

    main_entries, shadow_entries = [], []
    with open(args.journal, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                e = json.loads(line)
                validate_entry(e)
                main_entries.append(e)

    with open(args.shadow, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                shadow_entries.append(json.loads(line))

    ratio = len(shadow_entries) / max(1, len(main_entries))
    if ratio < 0.2:
        raise AssertionError(f"shadow ratio {ratio:.2f} < 0.2")

    print(f"[OK] {len(main_entries)} main, {len(shadow_entries)} shadow, ratio={ratio:.2f}")

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("[FAIL]", ex)
        sys.exit(1)
