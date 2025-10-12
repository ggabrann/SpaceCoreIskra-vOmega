"""Generate repository-wide model card manifests."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON_PATH = ROOT / "model_cards" / "model_card.json"
DEFAULT_MD_PATH = ROOT / "docs" / "model_card.md"
IGNORE_DIRS = {
    ".git",
    ".github",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "site",
    "dist",
    "artifacts",
    "__pycache__",
}
IGNORE_FILES = {
    DEFAULT_JSON_PATH.name,
}


def discover_files(base: Path) -> Iterable[Path]:
    """Yield files inside *base* filtered by guardrails in deterministic order."""

    try:
        default_json_parent = DEFAULT_JSON_PATH.parent.relative_to(base)
    except ValueError:
        default_json_parent = None

    candidates: list[Path] = []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(base)
        if any(part in IGNORE_DIRS for part in rel.parts[:-1]):
            continue
        if (
            default_json_parent is not None
            and rel.name in IGNORE_FILES
            and rel.parent == default_json_parent
        ):
            continue
        if path.stat().st_size > 25_000_000:
            continue
        candidates.append(path)

    candidates.sort(key=lambda candidate: candidate.relative_to(base).as_posix())
    yield from candidates


def sha256sum(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest_seed() -> dict[str, object]:
    manifest_path = ROOT / "DIST_MANIFEST.json"
    if not manifest_path.exists():
        return {}
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {
        key: data.get(key)
        for key in ["generated_at", "files", "notes"]
        if data.get(key) is not None
    }


def build_card(limit: int | None = None, base: Path = ROOT) -> dict[str, object]:
    files = []
    for path in discover_files(base):
        files.append(
            {
                "path": str(path.relative_to(base)),
                "bytes": path.stat().st_size,
                "sha256": sha256sum(path),
            }
        )
        if limit is not None and len(files) >= limit:
            break

    manifest_seed = load_manifest_seed() if base == ROOT else {}
    generated_at = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    card = {
        "name": "SpaceCore Iskra Canon",
        "generated_at": generated_at,
        "file_count": len(files),
        "files": files,
    }
    if manifest_seed:
        card["dist_manifest_excerpt"] = manifest_seed
    return card


def render_markdown(card: dict[str, object]) -> str:
    header = ["# Model Card", ""]
    header.append(f"Сгенерировано: {card['generated_at']}")
    header.append("")
    header.append(f"Всего файлов (≤25 МБ): {card['file_count']}")
    header.append("")
    header.append("## Файлы")
    rows = [
        f"- `{entry['path']}` — {entry['bytes']} B — `{entry['sha256'][:12]}…`"
        for entry in card["files"][:2000]
    ]
    header.extend(rows or ["- (нет файлов)"])
    return "\n".join(header) + "\n"


def write_outputs(card: dict[str, object], json_path: Path, md_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(card), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate repository model card")
    parser.add_argument("--limit", type=int, default=None, help="Ограничить количество файлов")
    parser.add_argument(
        "--json-path",
        type=Path,
        default=DEFAULT_JSON_PATH,
        help="Путь для JSON-версии",
    )
    parser.add_argument(
        "--markdown-path",
        type=Path,
        default=DEFAULT_MD_PATH,
        help="Путь для Markdown-версии",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    card = build_card(limit=args.limit)
    write_outputs(card, args.json_path, args.markdown_path)
    print(f"Model card written to {args.json_path} and {args.markdown_path}")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
