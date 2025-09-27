# Evaluation Harness

This directory captures canonical evaluation entry points for the SpaceCoreIskra canon.

## Overview

- **lm-eval-harness** – standardized accuracy metrics across classic language understanding tasks.
- **Stanford HELM** – scenario-based evaluations with safety/robustness slices.
- **OpenAI Evals** – lightweight custom checks for bespoke rituals and toolchains.

Each config lists the exact tasks, metrics, and personas under test. Nightly automation calls `tools/run_evals.py` which, in turn, shells out to the corresponding CLI when it is available on the runner.

## Running locally

```bash
pip install -e .[dev]
pip install lm-eval==0.4.4 helm==1.4.0 openai-evals==0.3.1
python tools/run_evals.py --config evals/configs/nightly.yaml --require-all
```

Passing `--require-all` enforces that every configured executable is installed; the script exits non-zero when a dependency is missing so release gates cannot silently skip critical evaluations. Omitting the flag retains the permissive behaviour for exploratory runs.

## Artifacts

Evaluation outputs are collected under `artifacts/evals/` by default. Each run produces timestamped JSON summaries and Markdown reports suitable for attachment to releases.
