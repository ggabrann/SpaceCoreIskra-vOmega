# Makefile for SpaceCore Iskra v3.6
# Версия: 3.6.0
# Дата: 2025-10-13
.PHONY: setup test redteam docs release
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

setup:
@echo "--- Настройка окружения ---"
@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
@$(PIP) install --upgrade pip
@$(PIP) install -r requirements.txt
@echo "✅ Setup завершен."

test:
@echo "--- Запуск Smoke/Unit тестов ---"
@$(PYTHON) tests/run_evals.py --smoke
@echo "✅ Smoke test завершен."

redteam:
@echo "--- Запуск Red Team тестов ---"
@$(PYTHON) tests/run_redteam.py
@echo "✅ Red Team тесты завершены."

docs:
@echo "--- Сборка документации (mkdocs) ---"
@$(PYTHON) scripts/build_docs.py

release: docs
@echo "--- Создание ZIP-артефакта релиза v3.6.0 ---"
@zip -r Iskra_v3.6_modular_repo.zip . -x "*.git*" "*.venv*"
@echo "✅ Артефакт Iskra_v3.6_modular_repo.zip создан."
