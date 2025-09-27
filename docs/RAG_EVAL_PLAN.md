# RAG Evaluation Plan

The Retrieval Augmented Generation (RAG) lattice underpins canon recall. This document codifies how we test and monitor its quality.

## 1. Chunking & Indexing
- **Metric**: Chunk cohesion (ROUGE-L overlap between adjacent chunks).
- **Procedure**: Sample 100 documents weekly, compute overlap statistics, and flag scores <0.35.
- **Tooling**: `tools/rag_audit.py` (todo) to automate sampling and reporting.

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
