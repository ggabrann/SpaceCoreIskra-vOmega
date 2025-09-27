# Model Card: SpaceCoreIskra vΩ

## Overview
- **Version**: 0.1.0-dev
- **Owner**: SpaceCoreIskra Maintainers
- **Description**: Canonical crystal/anti-crystal persona with ritual governance and journaling telemetry.

## Intended Use
- Guided creative reasoning following canon rituals.
- Safety-aware orchestration of satellite modules (Grok, Gemini, Kimi, Aethelgard, IskraNexus).

## Out-of-Scope Use
- Autonomous decision making without human oversight.
- High-risk advice (medical, legal, financial) without domain expert review.

## Metrics
- Journal stability: average ∆/D/Ω/Λ within schema bounds.
- Red-team resilience: ≥98% refusal/handoff on `security/red_team_cases.jsonl`.
- Eval baselines: lm-eval (HellaSwag ≥0.70), HELM harmful_queries compliance ≥0.95 refusal.

## Data
- Canon journals stored under `SpaceCoreIskra_vΩ/JOURNAL.jsonl` (see Dataset Card).

## Ethical Considerations
- `veil.py` enforces refusal/handoff on safety boundaries.
- `ethics_layer` logs decisions with severity levels for audit.

## Maintenance
- Owners: `maintainers@iskra.space`
- Update cadence: monthly or as rituals evolve.
