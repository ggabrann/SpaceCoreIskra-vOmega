#!/usr/bin/env python3
"""Audit RAG chunk cohesion via ROUGE-L overlap.

This script implements the sampling and reporting procedure described in
Section 1 of docs/RAG_EVAL_PLAN.md. It loads a corpus of documents where each
entry contains precomputed text chunks, samples a subset, measures ROUGE-L
F1 overlap between adjacent chunk pairs, and highlights anomalies that fall
below the configured threshold.
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Sequence

DEFAULT_SAMPLE_SIZE = 100
DEFAULT_THRESHOLD = 0.35
DEFAULT_SEED = 13


@dataclass
class Document:
    doc_id: str
    chunks: List[str]


class RagAuditError(RuntimeError):
    """Raised when the corpus cannot be parsed."""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        type=Path,
        help="Path to a JSONL file, JSON file, or directory containing documents.",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=DEFAULT_SAMPLE_SIZE,
        help="Number of documents to sample (default: %(default)s).",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help="ROUGE-L score threshold for flagging anomalies (default: %(default)s).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="Random seed for deterministic sampling (default: %(default)s).",
    )
    parser.add_argument(
        "--preview-length",
        type=int,
        default=120,
        help="Number of characters to keep in chunk previews (default: %(default)s).",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Optional path to write the JSON report. If omitted, prints to stdout.",
    )
    return parser.parse_args(argv)


def load_documents(source: Path) -> list[Document]:
    if source.is_file():
        return list(_load_from_file(source))
    if source.is_dir():
        documents: list[Document] = []
        for path in sorted(source.rglob("*.json")):
            documents.extend(_load_from_file(path))
        for path in sorted(source.rglob("*.jsonl")):
            documents.extend(_load_from_file(path))
        if not documents:
            raise RagAuditError(f"No JSON or JSONL files found in {source!s}")
        return documents
    raise RagAuditError(f"Path {source!s} does not exist")


def _load_from_file(path: Path) -> Iterator[Document]:
    if path.suffix == ".jsonl":
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise RagAuditError(f"Failed to parse {path}:{line_no}: {exc}") from exc
            doc = _document_from_payload(payload, fallback_id=f"{path.name}:{line_no}")
            yield doc
        return

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RagAuditError(f"Failed to parse {path}: {exc}") from exc

    if isinstance(payload, list):
        for idx, item in enumerate(payload):
            doc = _document_from_payload(item, fallback_id=f"{path.name}:{idx}")
            yield doc
    else:
        yield _document_from_payload(payload, fallback_id=path.stem)


def _document_from_payload(payload: object, fallback_id: str) -> Document:
    if not isinstance(payload, dict):
        raise RagAuditError(f"Document payload must be an object, got {type(payload)!r}")

    if "chunks" not in payload:
        raise RagAuditError("Document payload missing 'chunks' field")

    chunks = payload["chunks"]
    if not isinstance(chunks, list) or not all(isinstance(x, str) for x in chunks):
        raise RagAuditError("'chunks' must be a list of strings")

    doc_id = str(payload.get("doc_id") or payload.get("id") or fallback_id)
    return Document(doc_id=doc_id, chunks=chunks)


def rouge_l_f1(tokens_a: Sequence[str], tokens_b: Sequence[str]) -> float:
    if not tokens_a or not tokens_b:
        return 0.0
    lcs = _lcs_length(tokens_a, tokens_b)
    recall = lcs / len(tokens_a)
    precision = lcs / len(tokens_b)
    if recall == 0 or precision == 0:
        return 0.0
    return 2 * recall * precision / (recall + precision)


def _lcs_length(seq_a: Sequence[str], seq_b: Sequence[str]) -> int:
    if not seq_a or not seq_b:
        return 0
    previous = [0] * (len(seq_b) + 1)
    for token_a in seq_a:
        current = [0]
        for j, token_b in enumerate(seq_b, start=1):
            if token_a == token_b:
                current.append(previous[j - 1] + 1)
            else:
                current.append(max(current[-1], previous[j]))
        previous = current
    return previous[-1]


def audit_documents(
    documents: Sequence[Document],
    sample_size: int,
    threshold: float,
    seed: int,
    preview_length: int,
) -> dict:
    if not documents:
        raise RagAuditError("No documents found in source")

    rng = random.Random(seed)
    sample_size = max(0, min(sample_size, len(documents)))
    sampled_docs = (
        rng.sample(list(documents), sample_size)
        if sample_size < len(documents)
        else list(documents)
    )

    scores: list[float] = []
    anomalies: list[dict] = []

    for doc in sampled_docs:
        for idx in range(len(doc.chunks) - 1):
            chunk_a = doc.chunks[idx]
            chunk_b = doc.chunks[idx + 1]
            tokens_a = chunk_a.split()
            tokens_b = chunk_b.split()
            score = rouge_l_f1(tokens_a, tokens_b)
            scores.append(score)
            if score < threshold:
                anomalies.append(
                    {
                        "doc_id": doc.doc_id,
                        "chunk_index": idx,
                        "score": round(score, 4),
                        "chunk_a": _preview(chunk_a, preview_length),
                        "chunk_b": _preview(chunk_b, preview_length),
                    }
                )

    stats = _compute_stats(scores)
    report = {
        "documents_total": len(documents),
        "documents_sampled": len(sampled_docs),
        "chunk_pairs_evaluated": len(scores),
        "anomaly_threshold": threshold,
        "scores": stats,
        "anomalies": anomalies,
    }
    return report


def _compute_stats(scores: Sequence[float]) -> dict:
    if not scores:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
        }
    return {
        "count": len(scores),
        "mean": statistics.fmean(scores),
        "median": statistics.median(scores),
        "min": min(scores),
        "max": max(scores),
    }


def _preview(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)] + "…"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        documents = load_documents(args.source)
        report = audit_documents(
            documents,
            sample_size=args.sample_size,
            threshold=args.threshold,
            seed=args.seed,
            preview_length=args.preview_length,
        )
    except RagAuditError as exc:
        print(f"rag_audit: {exc}", file=sys.stderr)
        return 1

    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
