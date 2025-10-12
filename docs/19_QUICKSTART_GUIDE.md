# Быстрый старт с Искрой

## Требования

- Python 3.11+
- pip + virtualenv
- Git, Make
- Доступ к репозиторию и права чтения журналов

## Установка

```bash
git clone git@github.com:project/SpaceCoreIskra-vOmega.git
cd SpaceCoreIskra-vOmega
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
make setup
```

## Проверка окружения

```bash
make ci
python tools/audit_repo.py --output audit_report.json
python SpaceCoreIskra_vOmega/validate_journal.py < SpaceCoreIskra_vOmega/JOURNAL.jsonl
```

## Первый запуск

1. Прочитайте `README.md` и `docs/README_index.md`.
2. Запустите `pytest tests/test_spacecore_modules.py`.
3. Создайте задачу с #ANCHOR в Issue или локально в `AGENTS.md`.
4. Используйте Codex CLI: `codex "собери план улучшения RAG"`.
5. Перед коммитом выполните `make ci`.

## Работа с Искрой (через Projects)

- Добавьте репозиторий в ChatGPT Projects.
- Включите инструменты: файлы, коннекторы (GitHub, Drive).
- Используйте символы для выбора тона (`[SAM]`, `⟡`, `⚑`).
- Фиксируйте ∆DΩΛ в конце каждого ответа.

## Решение проблем

| Симптом | Причина | Решение |
| --- | --- | --- |
| `make ci` падает на schemas | Необновлённые журналы | Запустить `make schemas` и `validate_journal` |
| shadow coverage <0.2 | Недостаточно shadow-записей | Использовать `journal_generator.py --shadow` |
| Codex просит доступ в сеть | Нужен внешний источник | Обсудить в PR и обновить allowlist |

## Следующие шаги

- Ознакомьтесь с `docs/15_WORKFLOWS_AND_CYCLES.md` для понимания ритуалов.
- Настройте Codex CLI/IDE по инструкции в `Codex.txt`.
- Присоединитесь к еженедельному аудиту (см. `AUDIT_REPORT.md`).
