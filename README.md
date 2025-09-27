# SpaceCoreIskra-vOmega

[![iskra-ci](https://github.com/ggabrann/SpaceCoreIskra-vOmega/actions/workflows/ci.yml/badge.svg)](../../actions)

SpaceCoreIskra is the crystallized canon for orchestrating multi-persona reasoning rituals with built-in safety, evaluation, and governance layers.

## Quick Start (≤60 seconds)

```bash
pip install -e .[dev]
make ci
pytest
python tools/run_security_checks.py
python tools/run_evals.py --config evals/configs/nightly.yaml
```

### Key Documentation

- Canon overview – `SpaceCoreIskra_vΩ/README_vΩ.md`
- Release checklist – `docs/RELEASE_PROCESS.md`
- Evaluation harness – `evals/README.md`
- Security policy – `SECURITY.md`

## Repository Topology

| Path | Purpose |
| ---- | ------- |
| `SpaceCoreIskra_vΩ/` + ASCII mirror | Core canon rituals, journals, mechanics. |
| `GrokCoreIskra_vΓ/` + ASCII mirror | Prompt/RAG governance satellite. |
| `GeminiResonanceCore/` | Resonance harmonizer module. |
| `Kimi-Ω-Echo/` + ASCII mirror | Echo reflection engine. |
| `Aethelgard-vΩ/` + ASCII mirror | Paradox synthesizer. |
| `IskraNexus-v1/` | Integration lattice for downstream apps. |
| `schemas/` | JSON Schema definitions for manifests and journals. |
| `tools/` | CI utilities, security harnesses, evaluation orchestrators. |
| `cards/` | Model and dataset cards for transparency. |

## Authoring a New Persona Module (5 Steps)

1. Scaffold Unicode and ASCII mirrors, then add a manifest JSON conforming to `schemas/module_profile.schema.json`.
2. Implement persona logic with explicit entry points and safety hooks (`ethics_*`, `veil_*`).
3. Register journals that match `schemas/journal_entry.schema.json` and `schemas/shadow_journal_entry.schema.json`.
4. Extend evaluation configs (`evals/configs/nightly.yaml`) with relevant scenarios and update the module’s Model Card.
5. Run the full release checklist in `docs/RELEASE_PROCESS.md` before opening a pull request.

## CI/CD Expectations

- GitHub Actions runs linting (ruff, black), static typing (mypy), schema validation, unicode/ascii parity checks, security case validation, and pytest.
- `CHANGELOG.md` follows Keep a Changelog format and Semantic Versioning for each release tag.
- Evaluation and security harnesses emit artifacts in `artifacts/` for release packaging.
