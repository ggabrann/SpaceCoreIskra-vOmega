#!/usr/bin/env python3
"""Validate canon JSON/JSONL artifacts against project schemas."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - fallback for slim CI images
    from dataclasses import dataclass

    @dataclass(slots=True)
    class _ValidationError:
        message: str

    class Draft202012Validator:  # type: ignore[override]
        def __init__(self, schema: dict) -> None:
            self.schema = schema

        def iter_errors(self, instance: object):
            for message in self._validate(self.schema, instance, "$"):
                yield _ValidationError(message)

        def validate(self, instance: object) -> None:
            errors = list(self.iter_errors(instance))
            if errors:
                raise ValueError(errors[0].message)

        def _validate(self, schema: dict, instance: object, path: str) -> list[str]:
            errors: list[str] = []
            schema_type = schema.get("type")
            if schema_type == "object":
                if not isinstance(instance, dict):
                    return [f"{path}: expected object"]
                required = schema.get("required", [])
                for key in required:
                    if key not in instance:
                        errors.append(f"{path}: missing required property '{key}'")
                properties = schema.get("properties", {})
                for key, subschema in properties.items():
                    if key in instance:
                        errors.extend(self._validate(subschema, instance[key], f"{path}.{key}"))
                if not schema.get("additionalProperties", True):
                    allowed = set(properties)
                    extras = set(instance) - allowed
                    for extra in extras:
                        errors.append(f"{path}: additional property '{extra}' is not allowed")
            elif schema_type == "array":
                if not isinstance(instance, list):
                    return [f"{path}: expected array"]
                min_items = schema.get("minItems")
                if isinstance(min_items, int) and len(instance) < min_items:
                    errors.append(f"{path}: expected at least {min_items} items")
                item_schema = schema.get("items")
                if isinstance(item_schema, dict):
                    for idx, item in enumerate(instance):
                        errors.extend(self._validate(item_schema, item, f"{path}[{idx}]"))
            elif schema_type == "string":
                if not isinstance(instance, str):
                    return [f"{path}: expected string"]
                min_length = schema.get("minLength")
                if isinstance(min_length, int) and len(instance) < min_length:
                    errors.append(f"{path}: string shorter than {min_length}")
            elif schema_type == "number":
                if not isinstance(instance, (int, float)):
                    return [f"{path}: expected number"]
                minimum = schema.get("minimum")
                maximum = schema.get("maximum")
                if minimum is not None and instance < minimum:
                    errors.append(f"{path}: value {instance} < {minimum}")
                if maximum is not None and instance > maximum:
                    errors.append(f"{path}: value {instance} > {maximum}")
            return errors

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schemas"
UNICODE_ASCII_MAP = json.loads((REPO_ROOT / "common" / "unicode_ascii_map.json").read_text(encoding="utf-8"))
ASCII_ALIASES = set(UNICODE_ASCII_MAP.values())

SCHEMAS = {
    "journal": SCHEMA_DIR / "journal_entry.schema.json",
    "shadow": SCHEMA_DIR / "shadow_journal_entry.schema.json",
    "canon_manifest": SCHEMA_DIR / "canon_manifest.schema.json",
    "module_profile": SCHEMA_DIR / "module_profile.schema.json",
}

CANON_MANIFESTS = [
    Path("SpaceCoreIskra_vΩ/MANIFEST_vΩ.json"),
    Path("GrokCoreIskra_vΓ/MANIFEST_vΓ.json"),
    Path("IskraNexus-v1/MANIFEST_IskraNexus-v1.json"),
    Path("Kimi-Ω-Echo/MANIFEST_Kimi-Ω-Echo.json"),
]

MODULE_PROFILES = [
    Path("GeminiResonanceCore/gemini_resonance_core.json"),
    Path("IskraNexus-v1/iskra_nexus_v1_module.json"),
    Path("Kimi-Ω-Echo/ECHO_MANIFEST.json"),
    Path("Aethelgard-vΩ/MANIFEST_Aethelgard-vΩ.json"),
]


def _expand_aliases(path: Path) -> set[Path]:
    if not path.parts:
        return {REPO_ROOT / path}
    top, *rest = path.parts
    expanded = {REPO_ROOT / path}
    alias = UNICODE_ASCII_MAP.get(top)
    if alias:
        expanded.add(REPO_ROOT / Path(alias, *rest))
    return expanded


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
        relative = journal.relative_to(REPO_ROOT)
        if relative.parts and relative.parts[0] in ASCII_ALIASES:
            continue
        issues.extend(validate_jsonl(journal, journal_validator))

    for shadow in sorted(REPO_ROOT.glob("**/SHADOW_JOURNAL.jsonl")):
        relative = shadow.relative_to(REPO_ROOT)
        if relative.parts and relative.parts[0] in ASCII_ALIASES:
            continue
        issues.extend(validate_jsonl(shadow, shadow_validator))

    for manifest in CANON_MANIFESTS:
        for candidate in _expand_aliases(manifest):
            if candidate.exists():
                issues.extend(validate_json(candidate, manifest_validator))

    for profile in MODULE_PROFILES:
        for candidate in _expand_aliases(profile):
            if candidate.exists():
                issues.extend(validate_json(candidate, module_validator))

    if issues:
        print("[FAIL] JSON schema validation")
        for msg in issues:
            print(" -", msg)
        return 1

    print("[OK] All JSON artifacts satisfy the registered schemas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
