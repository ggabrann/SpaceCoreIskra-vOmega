"""Assemble the Iskra three-contour builds (Projects / Custom GPT / GitHub)."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Dict, Iterable, List

DEFAULT_CONFIG = Path("iskra/three_contour_manifest.json")
DEFAULT_OUT = Path("dist/three_contours")


class BuildError(RuntimeError):
    """Raised when a build configuration cannot be satisfied."""


def _copy_entry(source: Path, destination: Path) -> None:
    if not source.exists():
        raise BuildError(f"Source path does not exist: {source}")
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def _materialize_build(name: str, build_spec: Dict[str, object], root: Path, out_dir: Path) -> Dict[str, object]:
    description = str(build_spec.get("description", ""))
    include_entries: Iterable[Dict[str, str]] = build_spec.get("include", [])  # type: ignore[assignment]

    build_root = out_dir / name
    build_root.mkdir(parents=True, exist_ok=True)

    copied: List[Dict[str, str]] = []
    for entry in include_entries:
        source_rel = entry["source"]
        target_rel = entry.get("target", source_rel)
        source_path = root / source_rel
        destination_path = build_root / target_rel
        _copy_entry(source_path, destination_path)
        copied.append({"source": source_rel, "target": target_rel})

    metadata = {
        "build": name,
        "description": description,
        "files": copied,
    }
    metadata_path = build_root / "BUILD.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return metadata


def build_three_contours(config_path: Path, out_dir: Path) -> Dict[str, object]:
    if not config_path.exists():
        raise BuildError(f"Missing config: {config_path}")
    data = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise BuildError("Manifest must be a JSON object")

    manifest: Dict[str, object] = {}
    for name, spec in data.items():
        if not isinstance(spec, dict):
            raise BuildError(f"Invalid spec for build '{name}'")
        manifest[name] = _materialize_build(name, spec, config_path.parent.parent.resolve(), out_dir)
    summary_path = out_dir / "manifest.json"
    summary_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--clean", action="store_true", help="remove existing output directory before building")
    args = parser.parse_args()

    out_dir = args.out.resolve()
    if args.clean and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        build_three_contours(args.config, out_dir)
    except BuildError as error:
        print(f"Error: {error}")
        return 1
    print(f"Three-contour builds written to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
