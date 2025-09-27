.PHONY: ci test

ci:
	python tools/ci_aggregate.py

test:
	python -m pytest -q
