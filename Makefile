MAIN_JOURNAL=SpaceCoreIskra_vΩ/JOURNAL.jsonl
SHADOW_JOURNAL=SpaceCoreIskra_vΩ/SHADOW_JOURNAL.jsonl

.PHONY: ci test lint format typecheck security evals schemas unicode setup deps

ci: lint typecheck test security schemas unicode

lint:
	ruff check .
	black --check .

setup: deps

deps:
	python -m pip install --upgrade pip
	python -m pip install -r requirements-dev.txt

format:
	black .

typecheck:
	mypy tools

test:
	pytest

security:
	python tools/run_security_checks.py

evals:
	python tools/run_evals.py --config evals/configs/nightly.yaml

schemas:
	python tools/validate_json_schemas.py
	python tools/validate_journal_enhanced.py $(MAIN_JOURNAL) --shadow $(SHADOW_JOURNAL) --window 0
	python tools/ci_aggregate.py $(MAIN_JOURNAL) --shadow $(SHADOW_JOURNAL)

unicode:
	python tools/check_unicode_ascii_mirrors.py
