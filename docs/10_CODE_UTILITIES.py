"""Вспомогательные утилиты Искры.

Основные вспомогательные модули:
- `common.logging_utils` — единый формат логов, уровни INFO/TRACE для граней.
- `common.formatting` — функции для красивых таблиц, подсветки символов, ∆DΩΛ.
- `common.metrics` — нормализация и зажим метрик в диапазоне [0, 1].
- `common.validation` — помощь в проверке схем JSON и ∆-структур.

Правила для новых утилит:
1. Не использовать глобальные состояния.
2. Покрывать unit-тестами в `tests/`.
3. Документировать публичные функции docstring-ами.
"""

from __future__ import annotations

UTILITY_MODULES = {
    "logging": "common/logging_utils.py",
    "formatting": "common/formatting.py",
    "metrics": "common/metrics.py",
    "validation": "common/validation.py",
}

