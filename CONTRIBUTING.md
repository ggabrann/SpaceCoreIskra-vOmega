## Contributing to SpaceCoreIskra-vΩ

### Validation checklist (must pass in CI)
1. Each journal entry has metrics in range (∆∈[-3,3], D∈[0,9], Ω∈[-3,3], Λ≥0).
2. `mirror` is **required** for every entry.
3. If `∆ ≤ -2` → `ritual` is **required** (crisis-rule).
4. `events.evidence[]` is present and non-empty (at least one artifact/link).
5. `shadow_ratio ≥ 0.2`.

Run locally:
```bash
python tools/validate_journal_enhanced.py SpaceCoreIskra_vΩ/JOURNAL.jsonl --shadow SpaceCoreIskra_vΩ/SHADOW_JOURNAL.jsonl --window 50
```
