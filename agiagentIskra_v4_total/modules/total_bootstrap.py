"""Total bootstrap validator for agiagentИскра v4.0."""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_CORE = ROOT / "data" / "entropy_core.bin"
CHECKSUM_FILE = ROOT / "data" / "entropy_core.sha256"
MIN_BYTES = 6 * 1024 * 1024
REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "architecture" / "system_landscape.md",
    ROOT / "docs" / "total_playbook.md",
    ROOT / "rituals" / "anchor_checklist.md",
    ROOT / "rituals" / "shadow_protocol.md",
]


@dataclass
class BootstrapReport:
    """Structured report describing validation result."""

    ok: bool
    issues: list[str]
    checksum: str | None = None
    size_bytes: int | None = None

    def to_json(self) -> str:
        payload = {
            "ok": self.ok,
            "issues": self.issues,
            "checksum": self.checksum,
            "size_bytes": self.size_bytes,
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)


def sha256_of(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def validate_required_files() -> list[str]:
    issues: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            issues.append(f"missing required file: {path.relative_to(ROOT)}")
    return issues


def validate_entropy_core(min_bytes: int = MIN_BYTES) -> BootstrapReport:
    issues = validate_required_files()

    if not DATA_CORE.exists():
        command_hint = "python agiagentIskra_v4_total/data/build_entropy_core.py"
        issues.append(
            "entropy_core.bin is missing. Run the generator via: "
            f"{command_hint}"
        )
        return BootstrapReport(ok=False, issues=issues)

    size = DATA_CORE.stat().st_size
    if size < min_bytes:
        issues.append(
            f"entropy_core.bin is too small: {size} bytes (expected ≥ {min_bytes})"
        )

    checksum = sha256_of(DATA_CORE)

    if CHECKSUM_FILE.exists():
        expected = CHECKSUM_FILE.read_text(encoding="utf-8").strip()
        if expected and expected != checksum:
            issues.append("entropy_core checksum mismatch")
    else:
        issues.append(
            "entropy_core.sha256 is missing. Re-run the generator to refresh it."
        )

    ok = not issues
    return BootstrapReport(ok=ok, issues=issues, checksum=checksum, size_bytes=size)


def main() -> int:
    report = validate_entropy_core()
    print(report.to_json())
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
