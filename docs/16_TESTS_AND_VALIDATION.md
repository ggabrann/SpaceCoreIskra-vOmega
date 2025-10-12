# Тесты и проверка качества

## Юнит-тесты

- `tests/test_spacecore_modules.py::test_persona_selection` — проверяет выбор персоны по метрикам.
- `tests/test_spacecore_modules.py::test_rag_ranked_search` — гарантирует ранжирование результатов RAG.
- `tests/test_spacecore_modules.py::test_delta_signature_validation` — проверяет корректность ∆DΩΛ.
- `tests/test_spacecore_modules.py::test_preset_resolution` — убеждается, что формат ответа соответствует пресету.

## Интеграционные проверки

- `make ci` — объединяет lint, форматирование, типизацию, тесты, проверки журналов и veil.
- `tools/run_evals.py --config evals/configs/nightly.yaml` — сценарии: свежие события, сложные расчёты, атаки.
- `tools/audit_repo.py` — анализирует структуру, Unicode↔ASCII, наличие обязательных файлов.

## Схемы и метрики

- `schemas/journal.schema.json` — валидация JOURNAL/SHADOW.
- `schemas/module_profile.schema.json` — профили модулей и manifest.
- `schemas/metrics_snapshot.schema.json` — значения метрик.

Запускайте `make schemas` после изменения структур данных.

## Пороговые значения

- Coverage shadow-журнала ≥ 0.2.
- Все тесты — зелёные на Python 3.11.
- Линтер ruff без предупреждений.
- Mypy без ошибок (strict режим).

## Порядок перед релизом

1. `make format && make lint`.
2. `make typecheck`.
3. `make test`.
4. `make schemas`.
5. `make security`.
6. `make ci` (объединяет проверки и экспортирует отчёт).

## Отчётность

Результаты тестов фиксируются в `DIST_NOTE.md` и при необходимости — в JOURNAL (`∆`=+тесты). Если тесты падают, создаётся запись в SHADOW и назначается восстановительный план.
