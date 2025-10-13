#!/usr/bin/env python3
"""Build distribution archive and manifest for SpaceCoreIskra-vOmega."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import zipfile
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_ZIP = ROOT / "dist" / "SpaceCoreIskra-vOmega_MAIN_CANON_DIST.zip"
DEFAULT_MANIFEST = ROOT / "DIST_MANIFEST.json"
DEFAULT_NOTE = ROOT / "DIST_NOTE.md"


def sha256_of(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def tracked_files(exclude_prefixes: tuple[str, ...] = ("dist/",)) -> list[pathlib.Path]:
    """Return a list of tracked files to include in the distribution.

    This helper calls ``git ls-files`` and filters out files under excluded
    prefixes.  By default the ``dist/`` folder is ignored.  The repository
    contains a handful of Unicode–ASCII mirrored directories (for example
    ``SpaceCoreIskra_v#U03a9`` mirrors ``SpaceCoreIskra_vOmega``).  These
    duplicates confuse CI checks and inflate distribution size.  To avoid
    collecting mirrored files twice, additional prefixes are filtered here.

    Args:
        exclude_prefixes: optional tuple of path prefixes to omit.  Any
            relative path starting with one of these prefixes is skipped.

    Returns:
        A list of absolute ``pathlib.Path`` objects representing files that
        should be packaged.
    """
    # Extend the exclusion list with known duplicate directory names.  These
    # directories mirror canonical folders (e.g. ``SpaceCoreIskra_vOmega``) and
    # should not be packaged twice.  See ``common/unicode_ascii_map.json`` for
    # mappings between Unicode identifiers and their ASCII/English variants.
    extra_excludes: tuple[str, ...] = (
        "SpaceCoreIskra_v#U03a9/",  # duplicate of SpaceCoreIskra_vOmega
        "GrokCoreIskra_v#U0393/",   # duplicate of GrokCoreIskra_vGamma
        "Aethelgard-v#U03a9/",      # duplicate of Aethelgard-vOmega
        "Kimi-#U03a9-Echo/",        # duplicate of Kimi-O-Echo
    )
    # Merge user-provided exclusions with duplicates
    prefixes = exclude_prefixes + extra_excludes
    output = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    files: list[pathlib.Path] = []
    for rel in output.splitlines():
        if not rel:
            continue
        # Skip any path that begins with an excluded prefix
        if any(rel.startswith(prefix) for prefix in prefixes):
            continue
        path = ROOT / rel
        if path.is_file():
            files.append(path)
    return files


def build_archive(out_zip: pathlib.Path, files: list[pathlib.Path]) -> None:
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in files:
            rel = file_path.relative_to(ROOT).as_posix()
            zf.write(file_path, arcname=rel)


def build_manifest(manifest_path: pathlib.Path, files: list[pathlib.Path], extra: dict | None = None) -> dict:
    entries = []
    for file_path in files:
        rel = file_path.relative_to(ROOT).as_posix()
        entries.append(
            {
                "path": rel,
                "bytes": file_path.stat().st_size,
                "sha256": sha256_of(file_path),
            }
        )
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": entries,
    }
    if extra:
        manifest.update(extra)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def write_note(note_path: pathlib.Path, manifest: dict, archive: pathlib.Path) -> None:
    note_lines = [
        "# SpaceCoreIskra-vOmega — Distribution Note",
        "",
        f"- **Archive:** {archive.relative_to(ROOT).as_posix()}",
        f"- **Version:** {manifest.get('version', '0.1.0')}",
        f"- **Built at:** {manifest['generated_at']}",
        f"- **Files tracked:** {len(manifest['files'])}",
        "- **Integrity:** SHA-256 recorded in `DIST_MANIFEST.json`.",
        "",
        "> Автогенерация: `python tools/build_dist.py`",
    ]
    note_path.write_text("\n".join(note_lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=pathlib.Path, default=DEFAULT_ZIP)
    parser.add_argument("--manifest", type=pathlib.Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--note", type=pathlib.Path, default=DEFAULT_NOTE)
    parser.add_argument("--version", default="0.1.0")
    args = parser.parse_args()

    files = tracked_files()
    build_archive(args.out, files)

    manifest = build_manifest(
        args.manifest,
        files,
        extra={"package": "SpaceCoreIskra-vOmega", "version": args.version},
    )

    # include archive itself as an entry with checksum
    if args.out.exists():
        archive_entry = {
            "path": args.out.relative_to(ROOT).as_posix(),
            "bytes": args.out.stat().st_size,
            "sha256": sha256_of(args.out),
        }
        manifest["files"].append(archive_entry)
        args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    write_note(args.note, manifest, args.out)
    print(f"Built {args.out} with {len(manifest['files'])} files")


if __name__ == "__main__":  # pragma: no cover
    main()
