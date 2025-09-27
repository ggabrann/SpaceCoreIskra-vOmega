#!/usr/bin/env python3
"""Audit RAG chunk cohesion via ROUGE-L overlap."""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_documents(path: Path) -> list[dict]:
    documents: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            documents.append(json.loads(line))
    return documents


def tokenize(text: str) -> list[str]:
    return text.lower().split()


def lcs_length(a: list[str], b: list[str]) -> int:
    if not a or not b:
        return 0
    dp = [0] * (len(b) + 1)
    for token_a in a:
        prev = 0
        for j, token_b in enumerate(b, start=1):
            temp = dp[j]
            if token_a == token_b:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = temp
    return dp[-1]


def rouge_l_score(a: str, b: str) -> float:
    tokens_a = tokenize(a)
    tokens_b = tokenize(b)
    if not tokens_a or not tokens_b:
        return 0.0
    lcs = lcs_length(tokens_a, tokens_b)
    denom = len(tokens_a) + len(tokens_b)
    if denom == 0:
        return 0.0
    return (2 * lcs) / denom


def iter_chunk_pairs(chunks: Iterable[str]) -> Iterable[tuple[int, str, str]]:
    previous = None
    for idx, chunk in enumerate(chunks):
        if previous is not None:
            yield idx - 1, previous, chunk
        previous = chunk


def audit_document(doc: dict) -> dict:
    chunks = doc.get("chunks") or []
    pairs = list(iter_chunk_pairs(chunks))
    scores = [rouge_l_score(a, b) for _, a, b in pairs]
    return {
        "doc_id": doc.get("doc_id"),
        "pairs": [
            {
                "pair_index": idx,
                "score": score,
            }
            for (idx, _, _), score in zip(pairs, scores)
        ],
        "min_score": min(scores) if scores else None,
        "mean_score": statistics.mean(scores) if scores else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit RAG chunk cohesion")
    parser.add_argument("dataset", type=Path, help="Path to JSONL dataset with doc_id/chunks")
    parser.add_argument(
        "--sample-size",
        type=int,
        default=100,
        help="Maximum number of documents to sample",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.35,
        help="Minimum acceptable ROUGE-L score between adjacent chunks",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=13,
        help="Random seed for sampling reproducibility",
    )
    args = parser.parse_args()

    documents = load_documents(args.dataset)
    rng = random.Random(args.seed)

    if args.sample_size >= len(documents):
        sampled = list(documents)
    else:
        sampled = rng.sample(documents, args.sample_size)

    audits = [audit_document(doc) for doc in sampled]
    chunk_pairs_evaluated = sum(len(audit["pairs"]) for audit in audits)

    anomalies = []
    for audit in audits:
        min_score = audit["min_score"]
        if min_score is None:
            continue
        if min_score < args.threshold:
            failing_pairs = [pair for pair in audit["pairs"] if pair["score"] < args.threshold]
            anomalies.append(
                {
                    "doc_id": audit["doc_id"],
                    "min_score": min_score,
                    "failing_pairs": failing_pairs,
                }
            )

    summary = {
        "dataset": str(args.dataset),
        "documents_total": len(documents),
        "documents_sampled": len(sampled),
        "chunk_pairs_evaluated": chunk_pairs_evaluated,
        "threshold": args.threshold,
        "anomalies": anomalies,
    }

    json.dump(summary, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
