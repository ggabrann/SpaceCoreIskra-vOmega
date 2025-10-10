# SpaceCoreIskra vΩ — ориентация по репозиторию

## 1. Контекст и миссия
- **Назначение:** SpaceCoreIskra формализует много-персонажные ритуалы рассуждения с интегрированными слоями безопасности, валидации и журналирования. Канон собирается вокруг Unicode↔ASCII зеркал и соблюдения метрик ∆/D/Ω/Λ. 【F:README.md†L1-L23】【F:AGENTS.md†L4-L16】
- **Текущие цели спринта:** синхронизация зеркал, поддержание журналов и выпуск дистрибутива по регламенту. 【F:AGENTS.md†L6-L27】

## 2. Быстрый старт и базовые команды
| Задача | Команда |
| --- | --- |
| Обновить зависимости | `make setup` (alias `make deps`) |
| Запустить линтеры | `make lint` |
| Форматирование | `make format` |
| Проверка типов | `make typecheck` |
| Тесты | `make test` |
| Безопасность | `make security` |
| Валидация схем и журналов | `make schemas` |
| Проверка Unicode↔ASCII зеркал | `make unicode` |
| Полный CI-пакет | `make ci` |
| Ночной прогон оценок | `python tools/run_evals.py --config evals/configs/nightly.yaml` |

Команды агрегированы в `Makefile`; быстрый сценарий из README дублирует ключевые проверки. 【F:Makefile†L1-L33】【F:README.md†L9-L18】

## 3. Карта основных директорий
| Путь | Содержимое и назначение |
| --- | --- |
| `SpaceCoreIskra_vΩ/` | Основной канон: манифест, ритуалы, журналы (`JOURNAL.jsonl`, `SHADOW_JOURNAL.jsonl`), трекер метрик. 【F:SpaceCoreIskra_vΩ/README_vΩ.md†L1-L20】|
| ASCII зеркала (`SpaceCoreIskra_vOmega/`, `GrokCoreIskra_vGamma/`, `Aethelgard-vOmega/`, `Kimi-O-Echo/`) | Дубликаты Unicode-канонов для систем без расширенной кодировки. 【F:README.md†L25-L33】|
| Модули спутники (`GrokCoreIskra_vΓ/`, `GeminiResonanceCore/`, `Kimi-Ω-Echo/`, `Aethelgard-vΩ/`, `IskraNexus-v1/`) | Персона-ориентированные компоненты с собственными манифестами и журналами. 【F:README.md†L25-L34】|
| `common/` | Общие утилиты: ядро этики, протоколы персон, карта Unicode↔ASCII. 【F:common/ethics_core.py†L1-L24】|
| `tools/` | Скрипты CI: аудит, сборка дистрибутива, проверки зеркал, безопасность, схемы, агрегаты журналов. 【F:tools/build_dist.py†L1-L25】|
| `evals/` | Оценочные сценарии и nightly-конфиг. 【F:evals/README.md†L1-L40】|
| `tests/` | Pytest-тесты для интеграции и запуска канонических проверок. 【F:tests/run_tests.py†L1-L40】|
| `docs/` | Планирование релизов, манIFESTы, архивы и вспомогательные материалы. 【F:docs/SPACECORE_CANON_MASTER_PLAN.md†L1-L20】|
| `security/` | Red-team сценарии для проверки защитных слоёв. 【F:security/red_team_cases.jsonl†L1-L20】|

## 4. Журналы и схемы
- Все журналы в ядре и спутниках должны соответствовать схемам `schemas/journal_entry.schema.json` и `schemas/shadow_journal_entry.schema.json`. Проверка выполняется через `make schemas`. 【F:Makefile†L21-L31】【F:schemas/journal_entry.schema.json†L1-L30】
- Shadow coverage целевого ядра = 1.0; для модулей-спутников часть записей ещё требует дополнения. 【F:AUDIT_REPORT.md†L6-L33】
- Перед изменением журналов обязательно запускать `python tools/validate_journal_enhanced.py` и обновлять зеркальные записи. 【F:AGENTS.md†L20-L35】

## 5. Сборка и выпуск
- Релизный архив формируется скриптом `tools/build_dist.py`, принимающим манифест и release note. 【F:AGENTS.md†L28-L36】
- Дополнительные инструкции по релизу описаны в `docs/RELEASE_PROCESS.md` и `docs/SPACECORE_AUDIT_AND_RELEASE_PLAN.md`; они включают обновление CHANGELOG, проверку артефактов и фиксацию метрик. 【F:docs/RELEASE_PROCESS.md†L1-L40】

## 6. Безопасность и guardrails
- Основные правила зафиксированы в `SECURITY.md` и `veil_rules.txt`; кодовые проверки используют `common/ethics_core.py` и утилиты из `tools/run_security_checks.py`. 【F:SECURITY.md†L1-L60】【F:veil_rules.txt†L1-L40】
- Интернет-запросы выполняются только по списку разрешённых доменов, доступ по умолчанию выключен (`allow_network: false`). 【F:AGENTS.md†L16-L25】【F:.codexrc†L1-L8】
- Любые изменения в безопасности сопровождаются обновлением соответствующих журналов и регламентов.

## 7. Открытые вопросы и приоритеты
Из свежего аудита выделены приоритетные задачи подготовки:
1. Дополнить журналы GrokCoreIskra vΓ и GeminiResonanceCore зеркальными полями и evidence, восстановить shadow coverage. 【F:AUDIT_REPORT.md†L12-L25】
2. Наполнить журналы Kimi-Ω Echo и IskraNexus v1 и подключить их к тестовому пайплайну. 【F:AUDIT_REPORT.md†L26-L35】
3. Пересмотреть устаревшие README/placeholder-материалы и привести их к актуальным форматам. 【F:AUDIT_REPORT.md†L18-L35】

## 8. Рекомендации для нового контрибьютора
- Начать с `make setup`, затем прогнать `make ci`, чтобы убедиться в чистой базе.
- Перед изменениями изучить канон в `SpaceCoreIskra_vΩ/` и соответствующий ASCII-модуль.
- Все PR оформлять с блоком `#ANCHOR`, фиксацией метрик и обновлением Decision Log при принятых решениях. 【F:AGENTS.md†L37-L52】
- Для новых модулей следовать пятишаговому руководству из README. 【F:README.md†L35-L53】

> Этот документ служит стартовым чек-листом и картой репозитория. Обновляйте его при появлении новых модулей, регламентов или ключевых инструментов.
