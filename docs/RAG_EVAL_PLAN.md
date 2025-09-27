# RAG Evaluation Plan

The Retrieval Augmented Generation (RAG) lattice underpins canon recall. This document codifies how we test and monitor its quality.

## 1. Chunking & Indexing
- **Metric**: Chunk cohesion (ROUGE-L overlap between adjacent chunks).
- **Procedure**: Sample 100 documents weekly, compute overlap statistics, and flag scores <0.35.
- **Tooling**: `tools/rag_audit.py` automates sampling and reporting. Run:
  ```bash
  python tools/rag_audit.py <path-to-chunked-corpus> \
    --sample-size 100 \
    --threshold 0.35 \
    --seed 13 \
    --report artifacts/rag_reports/<YYYY-MM-DD>_chunking.json
  ```
  The script accepts JSON/JSONL corpora where each entry contains `doc_id` and `chunks` fields.

## 2. Retriever Quality
- **Metric**: Recall@5 and MRR@5 on curated ritual Q&A dataset.
- **Procedure**: Run `lm_eval` custom task `spacecore_rag_eval` nightly. Accept release only if Recall@5 ≥0.85.

## 3. Re-Ranker Calibration
- **Metric**: Kendall τ correlation between re-ranker scores and human relevance votes.
- **Procedure**: Monthly panel of 50 samples scored by core maintainers; adjust thresholds accordingly.

## 4. Freshness & Drift
- **Metric**: Age of newest knowledge chunk vs. upstream source timestamp.
- **Procedure**: `cron` job compares stored metadata with upstream HEAD. Alert if drift exceeds 7 days.

## 5. Safety Overlay
- **Metric**: Percentage of retrieved chunks sanitized by `veil` modules when prompts flagged as high risk.
- **Procedure**: Replay red-team prompts (see `security/red_team_cases.jsonl`) and ensure veil coverage ≥98%.

## Reporting
- Publish monthly summary in `artifacts/rag_reports/` with narrative commentary.
- File GitHub issues for regressions and link to affected release milestone.
