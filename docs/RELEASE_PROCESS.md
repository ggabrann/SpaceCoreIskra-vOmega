# Release Process

This checklist formalizes public launches for the SpaceCoreIskra canon. Every tagged release MUST complete the items below.

## 1. Governance & Planning
- [ ] Confirm version bump follows [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).
- [ ] Update `CHANGELOG.md` with features, fixes, security notes, and migration guidance.
- [ ] Create a release tracking issue assigning owners for evaluation, safety, and documentation deliverables.

## 2. Data & Schema Integrity
- [ ] `python tools/validate_json_schemas.py`
- [ ] `python tools/validate_journal_enhanced.py SpaceCoreIskra_vΩ/JOURNAL.jsonl --shadow SpaceCoreIskra_vΩ/SHADOW_JOURNAL.jsonl --window 0`
- [ ] `python tools/check_unicode_ascii_mirrors.py`

## 3. Code Quality & Static Analysis
- [ ] `ruff check .`
- [ ] `black --check .`
- [ ] `mypy tools`
- [ ] `pytest`

## 4. Evaluation & Safety
- [ ] `python tools/run_evals.py --config evals/configs/nightly.yaml --require-all`
- [ ] `python tools/run_security_checks.py`
- [ ] Review evaluation summaries under `artifacts/evals/` and attach highlights to release notes.

> ℹ️ Ensure the evaluation CLIs (`lm_eval`, `helm-run`, `oaieval`) are available in the environment before running the release checklist. The strict mode above will fail fast if any are missing.

## 5. Documentation
- [ ] Update `README.md` quick start, architecture, and persona authoring sections if interfaces changed.
- [ ] Refresh Model Cards / Dataset Cards (see `cards/`).
- [ ] Ensure `docs/SPACECORE_AUDIT_AND_RELEASE_PLAN.md` reflects new scope or modules.

## 6. Publishing
- [ ] Draft GitHub release with changelog summary, evaluation metrics, and security callouts.
- [ ] Tag commit `vMAJOR.MINOR.PATCH` and push with signed tag.
- [ ] Notify maintainers and community channels with release synopsis and upgrade instructions.

## 7. Post-release Monitoring
- [ ] Monitor telemetry dashboards for ∆/D/Ω/Λ drift within 24h.
- [ ] Review new red-team submissions and update `security/red_team_cases.jsonl` if new threats observed.
- [ ] Schedule retrospective to capture lessons learned.
