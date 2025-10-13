"""Runtime bridge for modules stored under the hyphenated package."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


_PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "IskraNexus-v1" / "modules"


def load(name: str) -> ModuleType:
    """Load ``name`` from the hyphenated modules directory."""

    module_path = _PACKAGE_ROOT / f"{name}.py"
    if not module_path.exists():
        raise ModuleNotFoundError(f"IskraNexus module '{name}' not found")

    spec = importlib.util.spec_from_file_location(f"IskraNexus_v1.modules.{name}", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load specification for '{module_path}'")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[call-arg]
    return module
