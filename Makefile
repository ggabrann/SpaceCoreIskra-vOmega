# Makefile for SpaceCore Iskra v3.6
# Версия: 3.6.0
# Дата: 2025-10-13

.PHONY: setup deps lint format format-check typecheck test schemas unicode security docs release ci three-contours clean

VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
DIST_OUT := dist/SpaceCoreIskra-vOmega_MAIN_CANON_DIST.zip
FORMAT_PATHS := src/core src/util src/iskra_cli
LINT_PATHS := $(FORMAT_PATHS) tools common
TYPECHECK_PATHS := src/core src/util src/iskra_cli

setup: $(PYTHON)
	@echo "✅ Setup завершен."

deps: setup

$(PYTHON):
	@echo "--- Настройка окружения ---"
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements-dev.txt

lint: $(PYTHON)
	@echo "--- Ruff lint ---"
	@$(PYTHON) -m ruff check $(LINT_PATHS)

format: $(PYTHON)
	@echo "--- Black format ---"
	@$(PYTHON) -m black $(FORMAT_PATHS)

format-check: $(PYTHON)
	@echo "--- Black format check ---"
	@$(PYTHON) -m black --check $(FORMAT_PATHS)

typecheck: $(PYTHON)
	@echo "--- Mypy typecheck ---"
	@$(PYTHON) -m mypy $(TYPECHECK_PATHS)

test: $(PYTHON)
	@echo "--- Pytest ---"
	@$(PYTHON) -m pytest
	@echo "--- Journaling integrity suite ---"
	@$(PYTHON) tests/run_tests.py

schemas: $(PYTHON)
	@echo "--- JSON schema validation ---"
	@$(PYTHON) tools/validate_json_schemas.py

unicode: $(PYTHON)
	@echo "--- Unicode ↔ ASCII mirror check ---"
	@$(PYTHON) tools/check_unicode_ascii_mirrors.py

security: $(PYTHON)
	@echo "--- Security guardrails suite ---"
	@$(PYTHON) tools/run_security_checks.py

docs: $(PYTHON)
	@echo "--- Сборка документации (mkdocs) ---"
	@$(PYTHON) scripts/build_docs.py

release: docs
	@echo "--- Создание ZIP-артефакта релиза ---"
	@mkdir -p dist
	@$(PYTHON) tools/build_dist.py \
		--out $(DIST_OUT) \
		--manifest DIST_MANIFEST.json \
		--note DIST_NOTE.md
	@echo "✅ Артефакт $(DIST_OUT) создан."

ci: format-check lint typecheck test schemas unicode security
	@echo "✅ Все проверки пройдены."

three-contours: $(PYTHON)
	@echo "--- Сборка трёхконтурных пакетов ---"
	@$(PYTHON) tools/build_three_contours.py --clean
	@echo "✅ Папка dist/three_contours готова."

clean:
	@echo "--- Очистка окружения и артефактов ---"
	@rm -rf $(VENV_DIR) dist $(DIST_OUT)
