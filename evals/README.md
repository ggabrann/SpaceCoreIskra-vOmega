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
python tools/run_evals.py --config evals/configs/nightly.yaml
# Strict mode aborts if any of the evaluation CLIs are missing.
python tools/run_evals.py --config evals/configs/nightly.yaml --require-all
```

The script will skip frameworks that are not currently installed, emitting a warning but keeping the exit status zero so regular CI passes remain deterministic. Pass `--require-all` to enforce that `lm_eval`, `helm-run`, and `oaieval` are present before continuing.

## Artifacts

Evaluation outputs are collected under `artifacts/evals/` by default. Each run produces timestamped JSON summaries and Markdown reports suitable for attachment to releases.
