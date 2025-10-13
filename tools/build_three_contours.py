"""Assemble the Iskra three-contour builds (Projects / Custom GPT / GitHub)."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

DEFAULT_CONFIG = Path("iskra/three_contour_manifest.json")
DEFAULT_OUT = Path("dist/three_contours")


class BuildError(RuntimeError):
    """Raised when a build configuration cannot be satisfied."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _ensure_relative_path(value: str, *, field: str, build: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        raise BuildError(f"{field} path must be relative in build '{build}': {value}")
    if any(part == ".." for part in candidate.parts):
        raise BuildError(f"{field} path may not escape build root in '{build}': {value}")
    return candidate


def _copy_entry(source: Path, destination: Path) -> None:
    if not source.exists():
        raise BuildError(f"Source path does not exist: {source}")
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def _materialize_build(
    name: str,
    build_spec: Dict[str, object],
    root: Path,
    out_dir: Path,
    timestamp: str,
) -> Dict[str, object]:
    description = str(build_spec.get("description", ""))
    include_entries: Iterable[Dict[str, str]] = build_spec.get("include", [])  # type: ignore[assignment]

    build_root = out_dir / name
    build_root.mkdir(parents=True, exist_ok=True)

    copied: List[Dict[str, str]] = []
    for entry in include_entries:
        if "source" not in entry:
            raise BuildError(f"Missing 'source' in manifest entry for build '{name}'")
        source_rel_raw = entry["source"]
        target_rel_raw = entry.get("target", source_rel_raw)

        source_rel = _ensure_relative_path(source_rel_raw, field="source", build=name)
        target_rel = _ensure_relative_path(target_rel_raw or ".", field="target", build=name)

        source_path = root / source_rel
        destination_path = (build_root / target_rel).resolve()
        build_root_resolved = build_root.resolve()
        try:
            destination_path.relative_to(build_root_resolved)
        except ValueError as exc:  # pragma: no cover - defensive guard
            raise BuildError(
                f"Target path escapes build root for '{name}': {target_rel_raw}"
            ) from exc

        _copy_entry(source_path.resolve(), destination_path)
        copied.append({"source": source_rel.as_posix(), "target": target_rel.as_posix()})

    metadata = {
        "build": name,
        "description": description,
        "generated_at": timestamp,
        "files": copied,
    }
    metadata_path = build_root / "BUILD.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return metadata


def _package_build(build_root: Path, package_path: Path, manifest_root: Path) -> Dict[str, object]:
    package_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(build_root.rglob("*")):
            if not path.is_file():
                continue
            arcname = path.relative_to(build_root).as_posix()
            archive.write(path, arcname=arcname)
    package_rel = package_path.relative_to(manifest_root)
    return {
        "path": package_rel.as_posix(),
        "bytes": package_path.stat().st_size,
        "sha256": _sha256(package_path),
    }


def build_three_contours(config_path: Path, out_dir: Path, *, package: bool = False) -> Dict[str, object]:
    config_path = config_path.resolve()
    if not config_path.exists():
        raise BuildError(f"Missing config: {config_path}")
    data = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise BuildError("Manifest must be a JSON object")

    root = config_path.parent.parent.resolve()
    timestamp = datetime.now(timezone.utc).isoformat()
    manifest: Dict[str, object] = {}

    for name, spec in data.items():
        if not isinstance(spec, dict):
            raise BuildError(f"Invalid spec for build '{name}'")
        build_metadata = _materialize_build(name, spec, root, out_dir, timestamp)
        if package:
            package_path = out_dir / f"{name}.zip"
            build_metadata["package"] = _package_build(out_dir / name, package_path, out_dir)
        manifest[name] = build_metadata

    summary = {
        "config": config_path.relative_to(root).as_posix(),
        "generated_at": timestamp,
        "builds": manifest,
    }
    summary_path = out_dir / "manifest.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--clean", action="store_true", help="remove existing output directory before building")
    parser.add_argument("--package", action="store_true", help="also emit zipped archives for each build")
    args = parser.parse_args()

    out_dir = args.out.resolve()
    if args.clean and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        build_three_contours(args.config, out_dir, package=args.package)
    except BuildError as error:
        print(f"Error: {error}")
        return 1
    package_note = " with packages" if args.package else ""
    print(f"Three-contour builds written to {out_dir}{package_note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
