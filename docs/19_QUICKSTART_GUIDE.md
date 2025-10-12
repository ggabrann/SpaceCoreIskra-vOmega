# Быстрый старт

## Предусловия

- Python 3.10+
- `pip install -e .[dev]`
- Доступ к GitHub и ChatGPT Projects (при необходимости).

## Установка

```bash
make setup
make ci
```

## Первый запуск

1. Прочитайте `README.md` и `docs/03_PHILOSOPHY_COMPLETE.md`.
2. Выполните `python tools/audit_repo.py --output audit_report.json`.
3. Прогоните `pytest tests/test_spacecore_modules.py`.
4. Создайте запись в JOURNAL с ∆DΩΛ.

## Работа с Искрой

- Формулируйте запросы чётко, добавляйте тон (символ) при необходимости.
- Проверяйте ответы через чек-лист в `docs/16_TESTS_AND_VALIDATION.md`.
- При ошибке фиксируйте shadow-запись и план восстановления.

