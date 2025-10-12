"""Вспомогательные утилиты Искры.

Этот файл перечисляет ключевые вспомогательные модули и правила их развития.
"""

from __future__ import annotations

UTILITY_MODULES = {
    "logging": {
        "path": "common/logging_utils.py",
        "description": "единый формат логов, уровни INFO/TRACE для граней, экспорт в journals",
    },
    "formatting": {
        "path": "common/formatting.py",
        "description": "рендер символов, таблиц, секций ∆DΩΛ, преобразование markdown ↔ текст",
    },
    "metrics": {
        "path": "common/metrics.py",
        "description": "нормализация метрик, clamp значений, поддержка производных индексов",
    },
    "validation": {
        "path": "common/validation.py",
        "description": "проверка JSON-схем, валидация ∆DΩΛ и журналов перед коммитом",
    },
    "security": {
        "path": "security/veil.py",
        "description": "утилиты veil для фильтрации вредного контента и ведения журнала отказов",
    },
}

GUIDELINES = [
    "Не использовать глобальные состояния: все конфигурации передаются параметрами.",
    "Каждая новая утилита получает unit-тест в каталоге `tests/`.",
    "Документируйте публичные функции docstring-ами на русском языке.",
    "Проверяйте инструменты командой `make ci` перед публикацией.",
]

__all__ = ["UTILITY_MODULES", "GUIDELINES"]
