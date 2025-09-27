#!/usr/bin/env python3
"""Validate canon JSON/JSONL artifacts against project schemas."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schemas"

SCHEMAS = {
    "journal": SCHEMA_DIR / "journal_entry.schema.json",
    "shadow": SCHEMA_DIR / "shadow_journal_entry.schema.json",
    "canon_manifest": SCHEMA_DIR / "canon_manifest.schema.json",
    "module_profile": SCHEMA_DIR / "module_profile.schema.json",
}

CANON_MANIFESTS = [
    REPO_ROOT / "SpaceCoreIskra_vΩ" / "MANIFEST_vΩ.json",
    REPO_ROOT / "SpaceCoreIskra_vOmega" / "MANIFEST_vΩ.json",
    REPO_ROOT / "GrokCoreIskra_vΓ" / "MANIFEST_vΓ.json",
    REPO_ROOT / "GrokCoreIskra_vGamma" / "MANIFEST_vΓ.json",
    REPO_ROOT / "IskraNexus-v1" / "MANIFEST_IskraNexus-v1.json",
    REPO_ROOT / "Kimi-Ω-Echo" / "MANIFEST_Kimi-Ω-Echo.json",
    REPO_ROOT / "Kimi-O-Echo" / "MANIFEST_Kimi-Ω-Echo.json",
]

MODULE_PROFILES = [
    REPO_ROOT / "GeminiResonanceCore" / "gemini_resonance_core.json",
    REPO_ROOT / "IskraNexus-v1" / "iskra_nexus_v1_module.json",
    REPO_ROOT / "Kimi-Ω-Echo" / "ECHO_MANIFEST.json",
    REPO_ROOT / "Kimi-O-Echo" / "ECHO_MANIFEST.json",
    REPO_ROOT / "Aethelgard-vΩ" / "MANIFEST_Aethelgard-vΩ.json",
    REPO_ROOT / "Aethelgard-vOmega" / "MANIFEST_Aethelgard-vΩ.json",
]


def load_schema(path: Path) -> Draft202012Validator:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Draft202012Validator(data)


def iter_json_lines(path: Path) -> Iterable[tuple[int, dict]]:
    with path.open("r", encoding="utf-8") as handle:
        for idx, raw in enumerate(handle, 1):
            raw = raw.strip()
            if not raw:
                continue
            yield idx, json.loads(raw)


def validate_json(path: Path, validator: Draft202012Validator) -> list[str]:
    errors: list[str] = []
    try:
        validator.validate(json.loads(path.read_text(encoding="utf-8")))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{path}: {exc}")
    return errors


def validate_jsonl(path: Path, validator: Draft202012Validator) -> list[str]:
    errors: list[str] = []
    for line_no, payload in iter_json_lines(path):
        for err in validator.iter_errors(payload):
            errors.append(f"{path}:{line_no}: {err.message}")
    return errors


def main() -> int:
    issues: list[str] = []

    journal_validator = load_schema(SCHEMAS["journal"])
    shadow_validator = load_schema(SCHEMAS["shadow"])
    manifest_validator = load_schema(SCHEMAS["canon_manifest"])
    module_validator = load_schema(SCHEMAS["module_profile"])

    for journal in sorted(REPO_ROOT.glob("**/JOURNAL.jsonl")):
        issues.extend(validate_jsonl(journal, journal_validator))

    for shadow in sorted(REPO_ROOT.glob("**/SHADOW_JOURNAL.jsonl")):
        issues.extend(validate_jsonl(shadow, shadow_validator))

    for manifest in CANON_MANIFESTS:
        if manifest.exists():
            issues.extend(validate_json(manifest, manifest_validator))

    for profile in MODULE_PROFILES:
        if profile.exists():
            issues.extend(validate_json(profile, module_validator))

    if issues:
        print("[FAIL] JSON schema validation")
        for msg in issues:
            print(" -", msg)
        return 1

    print("[OK] All JSON artifacts satisfy the registered schemas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
