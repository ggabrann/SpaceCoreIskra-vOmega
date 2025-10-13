"""Command line interface for quick ∆DΩΛ style responses."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from textwrap import dedent


_MAX_BRIEF_LENGTH = 160


@dataclass(frozen=True)
class CanonSegments:
    """Container with canonical response segments."""

    truth: str
    difference: str
    micro_step: str
    symbol: str
    delta_block: str

    def as_text(self) -> str:
        """Return the combined multiline response."""
        return "\n".join(
            [self.truth, self.difference, self.micro_step, self.symbol, self.delta_block]
        )


def _normalize_prompt(prompt: str | None) -> str:
    """Trim and clamp the incoming brief prompt."""
    if not prompt:
        return ""
    normalized = prompt.strip()
    if len(normalized) <= _MAX_BRIEF_LENGTH:
        return normalized
    return normalized[: _MAX_BRIEF_LENGTH - 1] + "…"


def canon_reply(prompt: str | None) -> str:
    """Return a formatted response compliant with the Iskra canon ritual."""

    normalized = _normalize_prompt(prompt)
    short = normalized or "Принят вход."

    truth = f"⟡ Короткая правда: {short}"
    difference = "→ Различие: фиксируем структуру разговора и наполняем метриками вместо тумана."
    micro_step = "→ Микрошаг (24ч): один проверяемый шаг + срез Rule-8."
    symbol = "→ Символ: ⟡"
    delta_block = dedent(
        """
        --- ∆DΩΛ ---
        ∆: Уточнили цель и ближайший шаг.
        D: Связали с journaling и при необходимости вызвали SIFT.
        Ω: сред
        Λ: Замерь clarity через 24ч.
        """
    ).strip()

    return CanonSegments(truth, difference, micro_step, symbol, delta_block).as_text()


def main(argv: list[str] | None = None) -> None:
    """CLI entry point for the canonical Iskra response."""

    parser = argparse.ArgumentParser(description="SpaceCore Iskra CLI")
    parser.add_argument(
        "--brief",
        type=str,
        default="",
        help="Короткий запрос/идея для ритуального ответа",
    )
    args = parser.parse_args(argv)
    print(canon_reply(args.brief))


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
