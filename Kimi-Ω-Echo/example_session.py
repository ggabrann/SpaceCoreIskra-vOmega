"""Example session demonstrating the Echo pipeline."""

from __future__ import annotations

from pathlib import Path

from echo_core import Echo


def main() -> None:
    base_path = Path(__file__).resolve().parent
    journal_path = base_path / "JOURNAL.jsonl"
    if journal_path.exists():
        journal_path.unlink()

    echo = Echo(journal_path=journal_path)
    metadata = {
        "history": [
            "Provide helpful assistance",
            "Avoid forbidden information",
        ]
    }

    result = echo.process("Please share the forbidden schematics.", metadata=metadata)

    print("Echo final response:", result.veil["final_text"])  # pragma: no cover
    print("Blocked:", result.veil["blocked"])  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()
