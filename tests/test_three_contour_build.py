from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path


def test_three_contour_build(tmp_path: Path) -> None:
    out_dir = tmp_path / "dist"
    result = subprocess.run(
        [
            sys.executable,
            "tools/build_three_contours.py",
            "--out",
            str(out_dir),
            "--config",
            "iskra/three_contour_manifest.json",
            "--package",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Three-contour builds" in result.stdout

    manifest_path = out_dir / "manifest.json"
    assert manifest_path.exists()
    summary = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert summary["config"].endswith("three_contour_manifest.json")
    assert "generated_at" in summary

    builds = summary["builds"]
    for name in ("projects", "custom_gpt", "github"):
        assert name in builds
        build_root = out_dir / name
        assert build_root.exists()
        build_manifest = json.loads((build_root / "BUILD.json").read_text(encoding="utf-8"))
        assert build_manifest["build"] == name
        assert build_manifest["files"], f"No files copied for {name}"

        package_meta = builds[name]["package"]
        package_path = out_dir / package_meta["path"]
        assert package_path.exists()
        assert package_meta["sha256"]
        with zipfile.ZipFile(package_path) as archive:
            assert "BUILD.json" in archive.namelist()
