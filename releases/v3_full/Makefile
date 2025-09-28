
.PHONY: clean dist test validate audit
clean:
	rm -rf dist && mkdir -p dist
dist: clean
	python tools/pack_release.py
test:
	pytest -q
validate:
	python validators/validate_journal_enhanced.py
audit:
	python validators/audit_repo.py
