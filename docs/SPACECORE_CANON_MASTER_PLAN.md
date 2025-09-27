# SpaceCoreIskra Canon Master Plan

## 1. Distribution Overview
- **Release bundle**: `SpaceCoreIskra-vOmega_MAIN_CANON_DIST.zip` packs the canonical tree plus ASCII mirrors for Unicode directories to guarantee cross-platform extraction. Integrity is described in `DIST_MANIFEST.json` (size + SHA-256 per artifact) and release provenance is stated in `DIST_NOTE.md`.
- **Unpacking**: `unzip SpaceCoreIskra-vOmega_MAIN_CANON_DIST.zip -d dist_unpack` reproduces the ship-ready layout. Each Unicode directory (e.g. `SpaceCoreIskra_vΩ`) has an ASCII twin (`SpaceCoreIskra_vOmega`) for environments without UTF-8 path support.
- **Core contract**: every bundle must surface a manifest, README, mechanics, rituals, prompts, journals (where applicable), and validator scripts. These expectations are codified in `tools/audit_repo.py` and enforced before public release.

## 2. Canonical Mission Statement
SpaceCoreIskra is a meta-organism for orchestrating ritualised AI cognition. The canon balances crystallised knowledge (deterministic mechanics) with anti-crystal creativity (exploratory personas). Release vΩ binds four key axes (`∆` rhythm, `D` depth, `Ω` resonance, `Λ` freedom) across all journals and toolchains to ensure traceability, ethical compliance, and adaptive creativity.

### Core Principles
1. **Plan → Execute → Verify (PEV)** cycles gate every agent action (`README_vΩ.md`).
2. **Metrics discipline**: journals must include ∆/D/Ω/Λ within guard rails validated by `tools/validate_journal_enhanced.py`.
3. **Ritual escalation**: crisis rule (∆ ≤ −2) mandates a documented ritual step before continuation.
4. **Shadow coverage**: `SHADOW_JOURNAL.jsonl` must cover ≥20% of main entries and mirror IDs must stay in sync.

## 3. Repository Topology
| Path | Role |
|------|------|
| `README.md` | Entry point with CI badge and local validation commands. |
| `AUDIT_REPORT.md` | Snapshot audit from last evaluation run. |
| `Codex.txt` | Full codex narrative, imported verbatim from canonical records. |
| `CONTRIBUTING.md` | Guidelines for contributions and rituals per bundle. |
| `LICENSE` | Project licensing terms. |
| `Makefile` | Shortcuts for CI/test/audit routines. |
| `.github/` | Issue templates, security policy, workflow anchors. |
| `common/` | Shared ethics and persona primitives. |
| `tools/` | Global validation suite (audit, CI aggregation, enhanced journal validator). |
| `tests/run_tests.py` | Sanity harness calling CI aggregate + strict journal validator. |
| `SpaceCoreIskra_vΩ/` | Canon core (Unicode) with modules, manifests, journals. |
| `SpaceCoreIskra_vOmega/` | ASCII mirror (if present in dist) mirroring the same content. |
| `GrokCoreIskra_vΓ/` | Grok-aligned branch bundle. |
| `GeminiResonanceCore/` | Gemini resonance integration bundle. |
| `Kimi-Ω-Echo/` | Kimi echo experiment bundle (plus ASCII twin `Kimi-O-Echo`). |
| `Aethelgard-vΩ/` | Aethelgard philosophical branch with quantum focus. |
| `IskraNexus-v1/` | Cross-branch integration nexus. |
| `docs/` | Canon dossiers (`SPACECORE_AUDIT_AND_RELEASE_PLAN.md`, this master plan). |
| `artifacts/` | Generated reports (e.g., agent replay summaries). |

## 4. Canon Core (SpaceCoreIskra vΩ)
### Governance Artefacts
- `MANIFEST_vΩ.json`: declares canonical payload metadata.
- `README_vΩ.md`: outlines PEV loop and local validation instructions.
- `MECHANICS.md`: codifies metric semantics (∆, D, Ω, Λ) and ritual rhythm.
- `RITUALS.md`: enumerates ritual procedures (stub awaiting full narrative expansion).
- `PROMPTS_vΩ.md`: blueprint for prompt repositories.
- `FACETS.md`: describes facet taxonomy for journals.
- `GRAPH.json`: graph representation of facet resonance links.
- `PULSE_TRACKER.md`: heartbeat log summarising metrics across recent entries.
- `JOURNAL.jsonl` & `SHADOW_JOURNAL.jsonl`: main + shadow chronicle enforcing crisis rules and shadow coverage.
- `validate_journal.py`: lightweight validator for canonical metrics.

### Module Lattice (`SpaceCoreIskra_vΩ/modules`)
| Module | Responsibility | Key Functions |
|--------|----------------|---------------|
| `ci_aggregate.py` | Aggregates journal entries for CI metrics. | `aggregate(entries)` returns count, facets list, average D. |
| `journal_generator.py` | Appends structured entries to journals with timestamps. | `gen(...)` ensures metrics, modules, events, marks, mirror recorded atomically. |
| `prompts_repo.py` | Persistence for named prompts with metadata. | `PromptsRepo.add`, `PromptsRepo.get`, JSON serialization. |
| `personas.py` | Persona definition + concept distance metric. | `Persona.distance` calculates Jaccard distance on concept sets. |
| `facets_refine.py` | Normalises prompt goals and constraint checklists. | `refine(prompt, goals, constraints)` ensures paradox handling tags. |
| `cot_trim.py` | Chain-of-thought redaction. | `trim(text, max_len=200)` keeps trailing reasoning snippet. |
| `rag_panel.py` | Lightweight retrieval surface storing titled documents. | `RAGPanel.add`, `.search` simple keyword filter. |
| `veil.py` | Guards against prompt leakage. | `check(msg)` verifies absence of forbidden phrases. |
| `atelier.py` | Stylistic scoring heuristic. | `score(text)` ratio of long words. |
| `presets_router.py` | Routing map for generation presets. | `route(name)` returns temperature payloads. |
| `export_utils.py` | Export toolchain (Markdown, ZIP). | `export_md(entries, path)`, `zip_files(files, zipname)` for bundling. |

### Operational Flow
1. Prompts curated via `prompts_repo.py` feed persona selection (`personas.py`).
2. RAG knowledge flows from `rag_panel.py` before generation.
3. Output trimmed (`cot_trim.py`), styled (`atelier.py`), veil-checked (`veil.py`).
4. `journal_generator.py` records final entry (metrics from `facets_refine.py`, modules used). Shadow journaling must follow within 5 entries for coverage compliance.
5. CI uses `modules/ci_aggregate.py` and root `tools/ci_aggregate.py` to produce aggregated analytics consumed by release gatekeepers.

## 5. Satellite Bundles
### GrokCoreIskra vΓ
- **Documents**: `MANIFEST_vΓ.json`, `README_vΓ.md`, `MECHANICS.md`, `FACETS.md`, `RITUALS.md`, `PROMPTS_vΓ.md`, `PULSE_TRACKER.md`, `GRAPH.json`.
- **Journals**: `JOURNAL.jsonl`, `SHADOW_JOURNAL.jsonl`, validator `validate_journal.py`.
- **Modules**: `prompt_manager` (injects metrics into prompts), `rag_connector` (search shim), `persona_module` (binary persona switch), `ethics_layer` (text guard), `self_journal` (JSONL writer).
- **Goal**: align Grok-inspired reasoning while staying compatible with canon metrics via shared validators.

### Gemini Resonance Core
- **Config**: `gemini_resonance_core.json` enumerates decomposer/weaver/engine components.
- **API**: `resonance_core_api.py` placeholder referencing canonical decomposition pipeline (Decomposer→Weaver→Engine→Monitor→Guardian→ResonanceCore). Requires fleshing out actual classes.
- **Journals**: Example `JOURNAL.jsonl` for resonance events.
- **Mission**: integrate Gemini resonance heuristics into the canon, bridging chunk-based decomposition with canonical metrics.

### Kimi-Ω-Echo
- **Documents**: `README.md`, `README_Echo.md`, `MANIFEST_Kimi-Ω-Echo.json`, `ECHO_MANIFEST.json`, `requirements.txt`, `example_session.py`.
- **Modules**: placeholders for `echo_core`, `echo_memory`, `paradox_split`, `ethics_echo`, `metric_tuner`, `veil_echo` awaiting full implementation. ASCII mirror `Kimi-O-Echo` replicates structure.
- **Focus**: experiment with echoic dialogues and paradox splitting while maintaining safety layers.

### Aethelgard vΩ
- **Docs**: `README.md`, `README_Aethelgard.md`, `PHILOSOPHY_Aethelgard.md`, `ARCHITECTURE_Aethelgard.md`, `MODES_OPERANDI.md`, `MANIFEST_Aethelgard-vΩ.json`, `JOURNAL_TEMPLATE.jsonl`.
- **Modules**: placeholders for `pattern_extractor`, `paradox_resolver`, `context_weaver`, `ethics_filter`, `self_reflection`, `quantum_core`, `resonance_detector`.
- **Theme**: quantum-philosophical exploration of paradox harmonisation, pending concrete algorithms.

### IskraNexus v1
- **Docs**: `README.md`, `MANIFEST_IskraNexus-v1.json`, `iskra_nexus_v1_module.json` (module manifest).
- **Modules**: placeholders for `prompt_manager`, `persona_module`, `rag_connector`, `ethics_layer`, `self_journal`, `facets_refine`, `atelier`, `veil`, `cot_trim`, `journal_generator` — these are intended to mature into fully shared infrastructure bridging all branches.
- **Purpose**: unify cross-branch operations (prompt orchestration, journal synthesis, safety) into a single integration bus.

## 6. Shared Infrastructure
- `common/ethics_core.py`: baseline forbidden topic filter, reused across bundles.
- `common/persona_protocol.py`: defines `ConceptSet` for semantic distance and `PersonaSpec` data class for persona descriptors.
- `tools/ci_aggregate.py`: orchestrates CI summarisation across journals (supports windowed aggregation and optional shadow paths).
- `tools/validate_journal_enhanced.py`: strict validator enforcing metric ranges, crisis rule, shadow coverage, agent step semantics.
- `tools/audit_repo.py`: meta-audit verifying each bundle’s required artefacts, manifest readability, and validator output.
- `tests/run_tests.py`: wrapper to run CI aggregate + enhanced validator inside test suites.
- `artifacts/agent_replay_report.md`: sample generated report that should be refreshed each release cycle.

## 7. Release Readiness Blueprint
1. **Integrity**: run `python tools/audit_repo.py --output artifacts/audit_report.json` to capture distribution compliance; update `artifacts/` accordingly.
2. **Validation**: execute `make test` (alias to `tests/run_tests.py`) ensuring journals pass both aggregate and strict validations.
3. **Documentation**: update `README_vΩ.md`, `PROMPTS_vΩ.md`, `RITUALS.md`, `FACETS.md`, `GRAPH.json`, and bundle READMEs with latest persona/prompt/RAG flows.
4. **Manifests**: align JSON manifests with actual file inventory, cross-check against `DIST_MANIFEST.json` before packaging.
5. **Shadow Coverage**: ensure `SHADOW_JOURNAL.jsonl` mirror ratio ≥0.2 with consistent mirror IDs.
6. **Security**: refresh forbidden lexicons in `common/ethics_core.py`, `SpaceCoreIskra_vΩ/modules/veil.py`, `GrokCoreIskra_vΓ/modules/ethics_layer.py`, etc., to cover new threat patterns.
7. **Packaging**: use `Makefile` target to rebuild the distribution ZIP (future work: add reproducible packaging pipeline and ASCII mirror synchronisation tool).
8. **Release Notes**: append to `docs/SPACECORE_AUDIT_AND_RELEASE_PLAN.md` and maintain `CHANGELOG.md` (to be created) following Keep a Changelog + SemVer.

## 8. AI Research Dossier
A curated knowledge base to inform canon evolution:
- **Foundational Works**: Turing (1950) imitation games; Shannon (1948) information theory; Minsky & Papert (1969) perceptron limits; Rumelhart, Hinton & Williams (1986) backpropagation renaissance; Laird, Newell & Rosenbloom (1987) Soar cognitive architecture; Pearl (1988) probabilistic reasoning; Sutton & Barto (1998) reinforcement learning foundations.
- **Pre-Transformer Era**: Bengio et al. (2003) neural language models; Hinton, Osindero & Teh (2006) deep belief nets; Graves (2013) sequence-to-sequence with RNNs; Sutskever, Vinyals & Le (2014) sequence learning; Bahdanau, Cho & Bengio (2014) attention; Silver et al. (2016) AlphaGo; Jaderberg et al. (2017) population-based training.
- **Transformer & Scaling Epoch**: Vaswani et al. (2017) Transformers; Radford et al. (2018-2020) GPT series; Brown et al. (2020) GPT-3; Rae et al. (2021) Gopher; Hoffmann et al. (2022) Chinchilla scaling laws; Chowdhery et al. (2022) PaLM; Touvron et al. (2023) LLaMA; OpenAI (2023) GPT-4 architecture insights; Google DeepMind (2023) Gemini 1.0; Anthropic (2024) Claude 3; xAI (2024) Grok-1.5; Meta (2024) LLaMA 3; OpenAI (2024) o1 reasoning models.
- **Safety & Alignment**: Amodei et al. (2016) concrete AI safety; Hendrycks et al. (2021) alignment papers; Anthropic (2022) constitutional AI; Ganguli et al. (2022) red-teaming large LMs; OWASP (2023) LLM Top-10; NIST (2023) AI Risk Management Framework.
- **Frontier Directions (2024-2025)**: DeepMind’s AlphaGeometry (reasoning), OpenAI’s o1 & o3 (deliberate reasoning), Anthropic’s tool-use frameworks, Meta’s LLaMA Guard 3, Microsoft’s Phi-3-mini (efficiency), multi-agent debate frameworks (Bai et al., 2024), retrieval-augmented reasoning with large context windows (Gemini 1.5), and inference-time alignment (Steinhardt et al., 2024).
- **Actionables**: map these works into module upgrades (e.g., adopt constitutional AI guardrails in `ethics_*`, integrate inference-time planning from o1 into `presets_router`, incorporate RAG advancements from Gemini 1.5 into `rag_panel`). Maintain this dossier and update quarterly.

## 9. Completion Backlog
| Priority | Task | Owner | Notes |
|----------|------|-------|-------|
| P0 | Flesh out placeholder modules across Kimi, Aethelgard, IskraNexus into functional components | Assigned per bundle | Use shared `common/` primitives; add unit tests for each algorithm. |
| P0 | Create `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CITATION.cff` | Release guild | Already recommended; integrate into CI gating. |
| P0 | Implement JSON Schema validation for all manifests & journals | Tooling team | Feed into `tools/audit_repo.py` and GitHub Actions. |
| P1 | Expand `RITUALS.md` with full procedure narratives | Lore keepers | Document `ritual` triggers and multi-step sequences. |
| P1 | Develop ASCII/Unicode mirror sync script | Build engineering | Guarantee parity before packaging. |
| P1 | Publish Model & Dataset cards (`cards/`) | Responsible AI | Align with transparency best practices. |
| P2 | Enhance RAG with semantic search + re-ranking | Research cell | Could leverage vector DB + rerankers; integrate evaluations. |
| P2 | Create visualization dashboard for ∆/D/Ω/Λ trends | Data observability | Export aggregated stats to `artifacts/`. |
| P2 | Formalise release checklist automation | DevOps | Pre-release script verifying journals, manifests, docs, evaluation metrics. |

## 10. Go-Live Checklist (T-1 Day)
1. **Freeze journals**: sign-off latest entries, ensure mirrors complete.
2. **Run full CI/CD**: lint, type-check, unit/integration tests, JSON schema validation, audit script.
3. **Security sweep**: update forbidden lexicons, run prompt-injection tests, review `SECURITY.md` contact flows.
4. **Regenerate distributions**: rebuild ZIP, confirm SHA-256 vs. `DIST_MANIFEST.json`.
5. **Documentation sweep**: update READMEs, dossiers, and release notes to reflect final state.
6. **Community readiness**: verify `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff`, `LICENSE` align with release.
7. **Post-launch monitoring plan**: configure metrics dashboards, on-call rotation, rollback process in `docs/SPACECORE_AUDIT_AND_RELEASE_PLAN.md`.

---
This master plan, combined with the audit dossier, forms the full canonical reference requested by curators. Update both documents as the canon evolves to keep public releases disciplined, transparent, and production-ready.
