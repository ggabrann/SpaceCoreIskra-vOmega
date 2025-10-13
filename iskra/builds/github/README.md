# Искра v3.1 — GitHub Build

GitHub-оболочка хранит канон, конституцию, память и инструменты CI/CD.
Используется как источник правды для Projects и Custom GPT.

## Структура
- `constitution/` — символы, ритуалы, форматы и валидатор.
- `canon/` — ключевые документы (подтягиваются из основного репозитория).
- `memory/` — Мантра, Архив (jsonl), Shadow (jsonl).
- `tools/` — вспомогательные скрипты (`map_aliases.py`).
- `tests/` — smoke-тесты и кейсы валидатора.
- `.github/` — CI/CD (CI и release workflow).
- `examples/` — сценарии и промпты.

## Политика путей
- Unicode-пути — канонические.
- ASCII-алиасы генерируются через `aliases.json` и не коммитятся в репозиторий.

## Быстрый старт
1. Склонируй репозиторий.
2. Запусти `python tools/map_aliases.py --check`.
3. Заполни `memory/ARCHIVE` и `memory/SHADOW` JSONL-записями согласно схемам.
4. Прогони smoke-тесты из `tests/`.
5. Сформируй дистрибутив через `python tools/build_dist.py`.
