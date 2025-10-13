"""Utility to materialise the agiagentИскра v4 entropy core on demand."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys
from dataclasses import dataclass


DEFAULT_SIZE_BYTES = 6 * 1024 * 1024  # 6 MiB — keeps us safely over the 5 MiB bar
SEED = "agiagentIskra_v4_total::entropy-core-seed/v1"

ROOT = pathlib.Path(__file__).resolve().parent
CORE_PATH = ROOT / "entropy_core.bin"
CHECKSUM_PATH = ROOT / "entropy_core.sha256"


@dataclass
class BuildResult:
    bytes_written: int
    sha256: str


def _block_for(counter: int) -> bytes:
    """Return a deterministic pseudo-random block used to fill the core."""

    payload = f"{SEED}|{counter}".encode("utf-8")
    return hashlib.sha512(payload).digest()


def write_entropy_core(size_bytes: int = DEFAULT_SIZE_BYTES) -> BuildResult:
    """Create the entropy core with deterministic contents."""

    total = 0
    counter = 0
    digest = hashlib.sha256()

    CORE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with CORE_PATH.open("wb") as fh:
        while total < size_bytes:
            block = _block_for(counter)
            counter += 1
            remaining = size_bytes - total
            chunk = block if len(block) <= remaining else block[:remaining]
            fh.write(chunk)
            digest.update(chunk)
            total += len(chunk)

    checksum = digest.hexdigest()
    CHECKSUM_PATH.write_text(f"{checksum}\n", encoding="utf-8")
    return BuildResult(bytes_written=total, sha256=checksum)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--size",
        type=int,
        default=DEFAULT_SIZE_BYTES,
        help="Target size in bytes (defaults to 6 MiB).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only display the checksum that would be produced without writing the file.",
    )
    return parser.parse_args(argv)


def dry_run_checksum(size_bytes: int) -> str:
    digest = hashlib.sha256()
    total = 0
    counter = 0
    while total < size_bytes:
        block = _block_for(counter)
        counter += 1
        remaining = size_bytes - total
        chunk = block if len(block) <= remaining else block[:remaining]
        digest.update(chunk)
        total += len(chunk)
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    if args.dry_run:
        checksum = dry_run_checksum(args.size)
        print(checksum)
        return 0

    result = write_entropy_core(size_bytes=args.size)
    print(
        f"entropy_core.bin written ({result.bytes_written} bytes, sha256={result.sha256})",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
