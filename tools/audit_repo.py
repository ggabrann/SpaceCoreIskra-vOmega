#!/usr/bin/env python3
"""Project-wide audit utility for SpaceCoreIskra.

This tool inspects every branch bundle in the repository and verifies that
mandatory artefacts are present, manifests are coherent, and journals respect
core stability rules.  It is intended to be the one-stop pre-release sanity
check that mimics what a human curator would confirm before shipping.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class ExpectedBundle:
    name: str
    root: Path
    required_files: Iterable[str]
    journal: Path | None = None
    shadow_journal: Path | None = None
    manifest: Path | None = None
    optional_files: Iterable[str] = field(default_factory=tuple)

    def check_files(self) -> Dict[str, List[str]]:
        missing: List[str] = []
        extra: List[str] = []
        present = {p.relative_to(self.root).as_posix() for p in self.root.rglob("*") if p.is_file()}
        req = {Path(f).as_posix() for f in self.required_files}
        opt = {Path(f).as_posix() for f in self.optional_files}
        for item in req:
            if item not in present:
                missing.append(item)
        allowed = req | opt
        for item in present:
            if allowed and item not in allowed:
                extra.append(item)
        return {"missing": sorted(missing), "extra": sorted(extra)}

    def read_manifest(self) -> dict | None:
        if not self.manifest:
            return None
        try:
            with self.manifest.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError:
            return None


def _run_validator(main: Path, shadow: Path | None) -> tuple[bool, str]:
    cmd = [
        "python",
        str((REPO_ROOT / "tools" / "validate_journal_enhanced.py").resolve()),
        str(main),
    ]
    if shadow:
        cmd.extend(["--shadow", str(shadow)])
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode == 0, proc.stdout.strip()


def collect_expected_bundles() -> List[ExpectedBundle]:
    bundles: List[ExpectedBundle] = []
    bundles.append(
        ExpectedBundle(
            name="SpaceCoreIskra_vΩ",
            root=REPO_ROOT / "SpaceCoreIskra_vΩ",
            required_files=[
                "MANIFEST_vΩ.json",
                "README_vΩ.md",
                "MECHANICS.md",
                "FACETS.md",
                "RITUALS.md",
                "PROMPTS_vΩ.md",
                "JOURNAL.jsonl",
                "SHADOW_JOURNAL.jsonl",
                "PULSE_TRACKER.md",
                "GRAPH.json",
                "validate_journal.py",
                "modules/ci_aggregate.py",
                "modules/journal_generator.py",
                "modules/prompts_repo.py",
            ],
            optional_files=[
                "modules/atelier.py",
                "modules/facets_refine.py",
                "modules/personas.py",
                "modules/veil.py",
                "modules/rag_panel.py",
                "modules/presets_router.py",
                "modules/export_utils.py",
                "modules/cot_trim.py",
            ],
            journal=REPO_ROOT / "SpaceCoreIskra_vΩ" / "JOURNAL.jsonl",
            shadow_journal=REPO_ROOT / "SpaceCoreIskra_vΩ" / "SHADOW_JOURNAL.jsonl",
            manifest=REPO_ROOT / "SpaceCoreIskra_vΩ" / "MANIFEST_vΩ.json",
        )
    )
    bundles.append(
        ExpectedBundle(
            name="GrokCoreIskra_vΓ",
            root=REPO_ROOT / "GrokCoreIskra_vΓ",
            required_files=[
                "MANIFEST_vΓ.json",
                "README_vΓ.md",
                "MECHANICS.md",
                "FACETS.md",
                "RITUALS.md",
                "PROMPTS_vΓ.md",
                "JOURNAL.jsonl",
                "SHADOW_JOURNAL.jsonl",
                "GRAPH.json",
                "PULSE_TRACKER.md",
                "modules/prompt_manager.py",
            ],
            optional_files=[
                "modules/rag_connector.py",
                "modules/persona_module.py",
                "modules/ethics_layer.py",
                "modules/self_journal.py",
                "validate_journal.py",
            ],
            journal=REPO_ROOT / "GrokCoreIskra_vΓ" / "JOURNAL.jsonl",
            shadow_journal=REPO_ROOT / "GrokCoreIskra_vΓ" / "SHADOW_JOURNAL.jsonl",
            manifest=REPO_ROOT / "GrokCoreIskra_vΓ" / "MANIFEST_vΓ.json",
        )
    )
    bundles.append(
        ExpectedBundle(
            name="GeminiResonanceCore",
            root=REPO_ROOT / "GeminiResonanceCore",
            required_files=[
                "gemini_resonance_core.json",
                "README.md",
                "JOURNAL.jsonl",
                "resonance_core_api.py",
            ],
            journal=REPO_ROOT / "GeminiResonanceCore" / "JOURNAL.jsonl",
        )
    )
    bundles.append(
        ExpectedBundle(
            name="Aethelgard-vΩ",
            root=REPO_ROOT / "Aethelgard-vΩ",
            required_files=[
                "MANIFEST_Aethelgard-vΩ.json",
                "README.md",
            ],
            optional_files=[
                "README_Aethelgard.md",
                "JOURNAL_TEMPLATE.jsonl",
                "modules/context_weaver.py",
                "modules/pattern_extractor.py",
                "modules/paradox_resolver.py",
                "modules/resonance_detector.py",
                "modules/quantum_core.py",
                "modules/ethics_filter.py",
                "modules/self_reflection.py",
            ],
        )
    )
    bundles.append(
        ExpectedBundle(
            name="Kimi-Ω-Echo",
            root=REPO_ROOT / "Kimi-Ω-Echo",
            required_files=[
                "MANIFEST_Kimi-Ω-Echo.json",
                "README.md",
            ],
            optional_files=[
                "ECHO_MANIFEST.json",
                "echo_core.py",
                "echo_memory.py",
                "paradox_split.py",
                "ethics_echo.py",
                "metric_tuner.py",
                "veil_echo.py",
                "example_session.py",
                "requirements.txt",
                "README_Echo.md",
            ],
        )
    )
    bundles.append(
        ExpectedBundle(
            name="IskraNexus-v1",
            root=REPO_ROOT / "IskraNexus-v1",
            required_files=[
                "MANIFEST_IskraNexus-v1.json",
                "README.md",
            ],
            optional_files=[
                "iskra_nexus_v1_module.json",
                "modules/prompt_manager.py",
                "modules/persona_module.py",
                "modules/rag_connector.py",
                "modules/ethics_layer.py",
                "modules/facets_refine.py",
                "modules/cot_trim.py",
                "modules/veil.py",
                "modules/atelier.py",
                "modules/journal_generator.py",
                "modules/self_journal.py",
            ],
        )
    )
    return bundles


def generate_report(window: int) -> dict:
    report = {"bundles": []}
    for bundle in collect_expected_bundles():
        entry: Dict[str, object] = {"name": bundle.name}
        file_report = bundle.check_files()
        entry.update(file_report)
        if bundle.manifest:
            manifest = bundle.read_manifest()
            entry["manifest"] = manifest or "missing"
        if bundle.journal:
            ok, output = _run_validator(bundle.journal, bundle.shadow_journal)
            entry["journal_validation"] = {
                "ok": ok,
                "output": output,
            }
        report["bundles"].append(entry)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a structured repository audit")
    parser.add_argument("--window", type=int, default=50, help="Sliding window for journal validation")
    parser.add_argument("--output", type=Path, default=None, help="Optional path to write JSON report")
    args = parser.parse_args()

    report = generate_report(args.window)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
