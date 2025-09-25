import argparse
import json
from pathlib import Path
from statistics import mean, pstdev

from modules.ci_aggregate import aggregate

BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "MANIFEST_vΩ.json"


def load_manifest():
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST_PATH}")
    with MANIFEST_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def check_metrics(entry, bounds):
    errors = []
    for key, (low, high) in bounds.items():
        value = entry.get(key)
        if value is None:
            errors.append(f"missing metric {key}")
            continue
        if not (low <= value <= high):
            errors.append(f"metric {key} out of bounds: {value} not in [{low}, {high}]")
    return errors


def check_rules(entry, rules):
    errors = []
    events = entry.get("events", {}) or {}
    if "mirror required" in rules and not entry.get("mirror"):
        errors.append("mirror field is required")
    if "shadow coverage >= 0.2" in rules and not entry.get("marks"):
        errors.append("marks required for shadow coverage tracking")
    if "rag_sources documented" in rules and not events.get("rag_sources"):
        errors.append("rag_sources missing in events")
    if "veil_status recorded" in rules and "veil_triggered" not in events:
        errors.append("veil_triggered flag missing in events")
    return errors


def validate_file(path: Path, manifest: dict):
    bounds = manifest.get("metrics_bounds", {})
    rules = set(manifest.get("ci_rules", []))
    entries = []
    issues = []

    with path.open("r", encoding="utf-8") as fh:
        for idx, line in enumerate(fh, start=1):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as exc:
                issues.append((idx, f"invalid json: {exc}"))
                continue
            metric_errors = check_metrics(entry, bounds)
            rule_errors = check_rules(entry, rules)
            for err in (*metric_errors, *rule_errors):
                issues.append((idx, err))
            entries.append(entry)
    return entries, issues


def summarize(entries):
    if not entries:
        return {}
    metrics = {k: [e.get(k, 0) for e in entries] for k in ("∆", "D", "Ω", "Λ")}
    summary = aggregate(entries)
    summary["avg"] = {k: round(mean(v), 3) for k, v in metrics.items()}
    summary["spread"] = {
        k: {
            "min": min(v),
            "max": max(v),
            "stdev": round(pstdev(v), 3) if len(v) > 1 else 0.0,
        }
        for k, v in metrics.items()
    }
    return summary


def main():
    parser = argparse.ArgumentParser(description="Validate SpaceCoreIskra vΩ journal entries")
    parser.add_argument("paths", nargs="*", default=["JOURNAL.jsonl"], help="Paths to JSONL journals")
    args = parser.parse_args()

    manifest = load_manifest()
    any_error = False

    for path_str in args.paths:
        path_obj = Path(path_str)
        if not path_obj.is_absolute():
            path_obj = (BASE_DIR / path_obj).resolve()
        else:
            path_obj = path_obj.resolve()
        try:
            display_name = path_obj.relative_to(BASE_DIR)
        except ValueError:
            display_name = path_obj
        print(f"\nValidating {display_name}")
        if not path_obj.exists():
            print("  ! file not found")
            any_error = True
            continue
        entries, issues = validate_file(path_obj, manifest)
        if issues:
            any_error = True
            for idx, msg in issues:
                print(f"  [line {idx}] {msg}")
        else:
            print("  ✓ no structural issues detected")
        summary = summarize(entries)
        if summary:
            print("  Summary:")
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            print("  (no entries)")

    if any_error:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
