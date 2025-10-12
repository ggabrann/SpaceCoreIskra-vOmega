from __future__ import annotations

from pathlib import Path

from tools.generate_model_card import build_card, discover_files, render_markdown


def create_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_discover_files_returns_sorted_paths(tmp_path: Path) -> None:
    create_file(tmp_path / "zeta.txt", "z")
    create_file(tmp_path / "alpha" / "beta.txt", "b")
    create_file(tmp_path / "alpha" / "alpha.txt", "a")
    create_file(tmp_path / ".git" / "ignored.txt", "nope")

    discovered = [p.relative_to(tmp_path).as_posix() for p in discover_files(tmp_path)]

    assert discovered == ["alpha/alpha.txt", "alpha/beta.txt", "zeta.txt"]


def test_build_card_uses_limit_and_preserves_order(tmp_path: Path) -> None:
    create_file(tmp_path / "b.txt", "b")
    create_file(tmp_path / "a.txt", "a")

    card = build_card(limit=1, base=tmp_path)

    assert card["file_count"] == 1
    assert card["files"][0]["path"] == "a.txt"
    assert "dist_manifest_excerpt" not in card


def test_render_markdown_includes_entries(tmp_path: Path) -> None:
    create_file(tmp_path / "a.txt", "a")
    create_file(tmp_path / "b.txt", "b")
    card = build_card(base=tmp_path)

    markdown = render_markdown(card)

    assert "Всего файлов" in markdown
    assert "a.txt" in markdown and "b.txt" in markdown
