# SpaceCoreIskra — Release Sync Report (2025-09-27)

This report weaves the full "простыня" release sync performed on 2025-09-27 into the repository. It consolidates the
manual verification of the `main` snapshot, the canonical distribution archive, and the merged release bundle
`SpaceCoreIskra_FULL_RELEASE.zip` referenced during the audit.

## Actions Completed
- Unpacked both source archives supplied during the audit cycle:
  - `/mnt/data/SpaceCoreIskra-vOmega-main.zip` → `extract_main_zip/SpaceCoreIskra-vOmega-main/...`
  - `/mnt/data/SpaceCoreIskra-vOmega_MAIN_CANON_DIST (1).zip` → `extract_dist_zip/...`
- Read the bundled `DIST_MANIFEST.json`; generated a fresh `DIST_NOTE.md` for the merged release because it was
  missing from the provided archives.
- Inspected the public GitHub repository `ggabrann/SpaceCoreIskra-vOmega` (branch `main`) to confirm the visible root
  layout and the presence of the published `artifacts/` directory.
- Compared canonical (`dist`) and development (`main`) bundles:
  - `dist` contains expanded artefacts (model/dataset cards, schemas, tools, tests, devcontainer, pre-commit hooks,
    ASCII mirrors for Unicode paths).
  - `main` holds the Unicode-first layout (e.g. `Aethelgard-vΩ/`, `Kimi-Ω-Echo/`, `GrokCoreIskra_vΓ/`) that the
    distribution mirrors via ASCII duplicates.
- Built a combined release directory that preserves the canonical structure, populates missing notes, records an
  audit narrative, and regenerates manifests with SHA-256 hashes and byte sizes.
- Produced the consolidated archive **`SpaceCoreIskra_FULL_RELEASE.zip`**, containing:
  - Canonical dist content with both Unicode and ASCII directory mirrors.
  - `AUDIT_ANALYSIS.md` enumerating divergences between `main` and `dist`.
  - Fresh `DIST_NOTE.md`, integrity manifest `DIST_MANIFEST_v2.json`, and `FULL_STACK.txt` (full concatenation of all
    files in the bundle).

## Snapshot Metrics
- Files in `main` snapshot: **218**.
- Files in canonical `dist` snapshot: **179**.
- Key extras in `dist` vs `main`: `cards/`, `schemas/`, `tools/`, `tests/`, `.devcontainer/`, `.pre-commit-config.yaml`,
  ASCII clones such as `SpaceCoreIskra_vOmega/`.
- Key extras in `main` vs `dist`: Unicode-first directories (e.g. `Aethelgard-vΩ/`, `Kimi-Ω-Echo/`,
  `GrokCoreIskra_vΓ/`) and development-only artefacts recorded in `AUDIT_ANALYSIS.md`.

## Verification Notes
- `DIST_MANIFEST.json` inside the supplied distribution archive was sampled against on-disk hashes – checksums
  matched.
- `DIST_NOTE.md` was regenerated for the combined release bundle and is now captured alongside this report.
- The merged archive retains ASCII duplicates (e.g. `vΩ → vOmega`, `vΓ → vGamma`, `Kimi-Ω → Kimi-O`) to guarantee
  cross-platform extraction fidelity.

## Integration Guidance
- The curated ZIP can be retrieved from the sandbox path exposed during the audit session:
  `sandbox:/mnt/data/SpaceCoreIskra_FULL_RELEASE.zip`.
- Keep `AUDIT_ANALYSIS.md`, `DIST_MANIFEST_v2.json`, and `FULL_STACK.txt` under version control when promoting future
  release bundles so reproducibility data remains auditable.
- Use this report as the canonical reference when aligning `main` and `dist` snapshots or when rebuilding the
  distribution via `tools/build_dist.py`.

