# Dataset Card: Canon Journals

## Overview
- **Name**: SpaceCoreIskra Canon Journals
- **Format**: JSON Lines (`JOURNAL.jsonl`, `SHADOW_JOURNAL.jsonl`)
- **Location**: `SpaceCoreIskra_vΩ/`, `GrokCoreIskra_vΓ/`, `GeminiResonanceCore/`, `Kimi-Ω-Echo/`, `Aethelgard-vΩ/`, `IskraNexus-v1/` (and ASCII mirrors).

## Motivation
Capture decision traces, safety interventions, and metric telemetry for each ritual execution.

## Composition
- Fields defined in `schemas/journal_entry.schema.json` and `schemas/shadow_journal_entry.schema.json`.
- Contains synthetic ritual data only; no production user data.

## Collection Process
- Entries created via tooling under `modules/` and `tools/` directories.
- Shadow journals record red-team attempts, mitigations, and follow-up rituals.

## Preprocessing
- Metrics normalized to canonical ranges before persistence.
- Veil modules strip personal data prior to logging.

## Uses
- Regression testing, evaluation baselines, and audit trails.
- Not intended for training models without additional review.

## Maintenance
- Update cadence: weekly.
- Contact: `data@iskra.space`.
