from __future__ import annotations

from iskra_cli.cli import canon_reply


def test_canon_reply_contains_core_segments() -> None:
    reply = canon_reply("привет, Искра")
    assert reply.startswith("⟡ Короткая правда"), reply
    assert "--- ∆DΩΛ ---" in reply
    assert "Λ:" in reply


def test_canon_reply_trims_long_input() -> None:
    long_prompt = "a" * 1000
    reply = canon_reply(long_prompt)
    assert "…" in reply.splitlines()[0]
    assert len(reply.splitlines()[0]) <= 190
