# SpaceCore Iskra vΩ — Initial Audit Notes

## 1. Goals, Guardrails, and Modules to Track
- **Repository charter** — SpaceCoreIskra orchestrates multi-persona rituals with built-in safety, evaluation, and governance layers; quick start includes `make ci`, `pytest`, security and eval scripts.【F:README.md†L1-L34】
- **Sprint guardrails** — Maintain Unicode↔ASCII parity, keep journals aligned with schemas and ≥0.2 shadow coverage, and ensure distribution artifacts are regenerated through `tools/build_dist.py` with manifest/note updates.【F:AGENTS.md†L5-L33】
- **Canonical module surface** — SpaceCore manifest enumerates required ritual docs, journal assets, and safety modules (prompt repository, personas, facets, rag panel, etc.), all governed by ∆/D/Ω/Λ bounds, mirror enforcement, and shadow coverage minima.【F:SpaceCoreIskra_vOmega/MANIFEST_vΩ.json†L1-L7】
- **Nexus integration scope** — IskraNexus manifest lists placeholder modules (prompt manager, persona module, rag connector, ethics layer, facets refine, etc.) that must satisfy identical metric and mirror constraints when activated.【F:IskraNexus-v1/MANIFEST_IskraNexus-v1.json†L1-L24】

## 2. Repository Audit Findings (`tools/audit_repo.py`)
- The audit cannot locate the Unicode-named `SpaceCoreIskra_vΩ` bundle, flagging every manifest file (journals, rituals, modules) as missing despite their presence under the ASCII mirror. This indicates the directory naming/parity mismatch described in the follow-up task list and requires renaming or mirroring adjustments so validation scripts resolve the canonical path.【F:audit_report.json†L1-L36】
- Gemini Resonance Core violates the mandated shadow coverage (ratio 0.00 < 0.20) and needs additional shadow entries before release tasks proceed.【F:audit_report.json†L37-L51】
- GrokCoreIskra passes structural validation, but further work is needed on shared modules to remove placeholders (see §4).【F:audit_report.json†L23-L36】

### Required Corrections Summarised
1. Restore Unicode directory structure for SpaceCore canon so manifests and validators operate without FileNotFound errors.【F:audit_report.json†L4-L20】
2. Augment Gemini Resonance Core with compliant shadow journal entries to lift coverage above 0.2.【F:audit_report.json†L37-L51】
3. Replace placeholder module implementations in SpaceCore/Grok/Iskra Nexus with safety-aware logic tied to `ethics_layer` and `veil` before enabling CI tasks (details in §4).

## 3. Journal Metric Spot Checks (`validate_journal.py`)
- Canon journal entries comply with ∆/D/Ω/Λ bounds, but the shadow mirror lacks the required metric fields, triggering `'∆'` key errors and confirming schema misalignment.【574173†L1-L2】【3ece0b†L1-L4】【F:SpaceCoreIskra_vOmega/SHADOW_JOURNAL.jsonl†L1-L4】
- GrokCore journal passes metric checks; its shadow log mirrors the same missing-metric defect and needs field augmentation.【93209b†L1-L2】【48229f†L1-L3】【F:GrokCoreIskra_vΓ/SHADOW_JOURNAL.jsonl†L1-L2】
- Gemini Resonance Core has no shadow log, matching the audit’s coverage failure and requiring new shadow entries alongside metric enforcement.【a5124c†L1-L2】【F:GeminiResonanceCore/JOURNAL.jsonl†L1-L12】

## 4. Placeholder Module Inventory
- **SpaceCore personas** — Current implementation only stores names/concepts and offers a naive Jaccard distance without persona registry, selection heuristics, or safety checks, necessitating expansion with persona catalogue and veil/ethics hooks.【F:SpaceCoreIskra_vOmega/modules/personas.py†L1-L7】
- **SpaceCore RAG panel** — Minimal keyword containment check; must grow to include relevance scoring, keyword boosts, and external integration guards per task brief.【F:SpaceCoreIskra_vOmega/modules/rag_panel.py†L1-L6】
- **GrokCore prompt manager / RAG connector / persona module** — Provide only stub responses and metric echoes, lacking storage policies, rate limiting, or persona selection logic compatible with Nexus orchestration.【F:GrokCoreIskra_vΓ/modules/prompt_manager.py†L1-L9】【F:GrokCoreIskra_vΓ/modules/rag_connector.py†L1-L2】【F:GrokCoreIskra_vΓ/modules/persona_module.py†L1-L2】
- **IskraNexus core modules** — Key integration files remain empty placeholders (prompt manager, persona module, rag connector, ethics layer, facets refine, journal generator, self journal). Each must be implemented with shared abstractions and test coverage before release.【F:IskraNexus-v1/modules/prompt_manager.py†L1-L1】【F:IskraNexus-v1/modules/persona_module.py†L1-L1】【F:IskraNexus-v1/modules/rag_connector.py†L1-L1】【F:IskraNexus-v1/modules/ethics_layer.py†L1-L1】【F:IskraNexus-v1/modules/facets_refine.py†L1-L1】【F:IskraNexus-v1/modules/journal_generator.py†L1-L1】【F:IskraNexus-v1/modules/self_journal.py†L1-L1】

## 5. Next Actions Overview
- Design a renaming/mirroring migration plan that preserves git history while aligning `SpaceCoreIskra_vΩ` paths for CI tools.
- Draft schema-compliant shadow journal templates and regenerate entries via `journal_generator.py` once implemented to reach coverage ≥0.2 across all bundles.
- Prioritise implementation of shared prompt/persona/RAG modules within Iskra Nexus, then propagate robust versions to SpaceCore and Grok satellites alongside unit tests and CI wiring.
- Extend `facets_refine.py` and persona catalogues with tone/paradox constraints, then integrate selection logic in Nexus to power downstream modules.
- Update README/manifests once foundational modules and journals are corrected to reflect new capabilities and maintenance workflows.
