MAIN_JOURNAL=SpaceCoreIskra_vΩ/JOURNAL.jsonl
SHADOW_JOURNAL=SpaceCoreIskra_vΩ/SHADOW_JOURNAL.jsonl

ci:
	python tools/ci_aggregate.py $(MAIN_JOURNAL) --shadow $(SHADOW_JOURNAL)

test:
	python tests/run_tests.py
