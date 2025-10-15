#!/usr/bin/env python3
"""Health check utility for SpaceCoreIskra deployment.

Can be used as:
1. Standalone script: python tools/health_check.py
2. Docker healthcheck: CMD ["python", "tools/health_check.py"]
3. Kubernetes livenessProbe: exec command

Exit codes:
    0 - Healthy
    1 - Unhealthy (critical failure)
    2 - Degraded (warnings but functional)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent


class HealthStatus(NamedTuple):
    """Health check result."""

    healthy: bool
    degraded: bool
    checks: dict[str, bool]
    messages: list[str]

    @property
    def exit_code(self) -> int:
        """Return appropriate exit code."""
        if self.healthy:
            return 0
        if self.degraded:
            return 2
        return 1


def check_required_files() -> tuple[bool, str]:
    """Verify critical files exist."""
    required = [
        "pyproject.toml",
        "README.md",
        "AGENTS.md",
        "common/ethics_core.py",
        "veil_rules.txt",
    ]

    missing = [f for f in required if not (REPO_ROOT / f).exists()]

    if missing:
        return False, f"Missing critical files: {', '.join(missing)}"
    return True, "All critical files present"


def check_journal_integrity() -> tuple[bool, str]:
    """Check main journal exists and is valid."""
    journal_path = REPO_ROOT / "SpaceCoreIskra_vΩ" / "JOURNAL.jsonl"

    if not journal_path.exists():
        return False, "Main JOURNAL.jsonl not found"

    try:
        with journal_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            return False, "JOURNAL.jsonl is empty"

        # Validate last entry
        last_entry = json.loads(lines[-1])
        required_fields = ["facet", "snapshot", "answer", "∆", "D", "Ω", "Λ", "mirror", "events"]

        missing_fields = [field for field in required_fields if field not in last_entry]

        if missing_fields:
            return False, f"Last journal entry missing fields: {', '.join(missing_fields)}"

        return True, f"Journal healthy ({len(lines)} entries)"

    except json.JSONDecodeError as e:
        return False, f"Journal JSON invalid: {e}"
    except Exception as e:
        return False, f"Journal check failed: {e}"


def check_shadow_coverage() -> tuple[bool, str]:
    """Check shadow journal coverage."""
    journal_path = REPO_ROOT / "SpaceCoreIskra_vΩ" / "JOURNAL.jsonl"
    shadow_path = REPO_ROOT / "SpaceCoreIskra_vΩ" / "SHADOW_JOURNAL.jsonl"

    if not journal_path.exists() or not shadow_path.exists():
        return False, "Journal or shadow journal missing"

    try:
        with journal_path.open("r", encoding="utf-8") as f:
            journal_count = sum(1 for line in f if line.strip())

        with shadow_path.open("r", encoding="utf-8") as f:
            shadow_count = sum(1 for line in f if line.strip())

        if journal_count == 0:
            return True, "Journal empty (shadow coverage N/A)"

        ratio = shadow_count / max(1, journal_count)

        if ratio >= 0.2:
            return True, f"Shadow coverage: {ratio:.1%}"
        else:
            return False, f"Shadow coverage too low: {ratio:.1%} (< 20%)"

    except Exception as e:
        return False, f"Shadow coverage check failed: {e}"


def check_security_rules() -> tuple[bool, str]:
    """Check security rules are loaded."""
    veil_path = REPO_ROOT / "veil_rules.txt"
    ethics_path = REPO_ROOT / "common" / "ethics_core.py"

    if not veil_path.exists():
        return False, "veil_rules.txt missing"

    if not ethics_path.exists():
        return False, "ethics_core.py missing"

    try:
        with veil_path.open("r", encoding="utf-8") as f:
            veil_rules = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        if len(veil_rules) < 5:
            return False, f"Too few veil rules: {len(veil_rules)}"

        return True, f"Security rules loaded ({len(veil_rules)} veil patterns)"

    except Exception as e:
        return False, f"Security rules check failed: {e}"


def check_python_imports() -> tuple[bool, str]:
    """Check critical Python imports work."""
    try:
        # Add repo root to path for imports
        import sys

        if str(REPO_ROOT) not in sys.path:
            sys.path.insert(0, str(REPO_ROOT))

        import common.ethics_core  # noqa: F401
        from common.logging_config import get_logger  # noqa: F401

        return True, "Python imports OK"
    except ImportError as e:
        return False, f"Import failed: {e}"


def run_health_checks() -> HealthStatus:
    """Run all health checks."""
    checks = {
        "required_files": check_required_files,
        "journal_integrity": check_journal_integrity,
        "shadow_coverage": check_shadow_coverage,
        "security_rules": check_security_rules,
        "python_imports": check_python_imports,
    }

    results: dict[str, bool] = {}
    messages: list[str] = []

    for check_name, check_func in checks.items():
        success, message = check_func()
        results[check_name] = success
        messages.append(f"[{'✅' if success else '❌'}] {check_name}: {message}")

    # Determine overall health
    critical_checks = ["required_files", "python_imports", "journal_integrity"]
    degraded_checks = ["shadow_coverage", "security_rules"]

    critical_failures = [name for name in critical_checks if not results.get(name, False)]
    degraded_failures = [name for name in degraded_checks if not results.get(name, False)]

    healthy = len(critical_failures) == 0
    degraded = healthy and len(degraded_failures) > 0

    return HealthStatus(
        healthy=healthy,
        degraded=degraded,
        checks=results,
        messages=messages,
    )


def main() -> int:
    """Main health check entry point."""
    print("🏥 SpaceCoreIskra Health Check")
    print("=" * 60)

    status = run_health_checks()

    for message in status.messages:
        print(message)

    print("=" * 60)

    if status.healthy and not status.degraded:
        print("✅ System HEALTHY")
    elif status.degraded:
        print("⚠️  System DEGRADED (warnings present)")
    else:
        print("❌ System UNHEALTHY (critical failures)")

    return status.exit_code


if __name__ == "__main__":
    sys.exit(main())
