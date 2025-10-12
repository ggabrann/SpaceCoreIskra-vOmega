# Интеграции и инструменты

## IskraNexus

- `connector_registry.json` — список доступных коннекторов (GitHub, Google Drive, Box, Gmail).
- `prompt_manager` — маршрутизатор подсказок между SpaceCore и внешними приложениями.
- `rag_connector` — проксирует запросы к внешним базам знаний.
- Все коннекторы уважают allowlist доменов и ограничения сети.

## Рабочие инструменты

| Инструмент | Назначение | Команда |
| --- | --- | --- |
| Codex CLI | Быстрые задачи | `codex "fix lint"` |
| Makefile | Сборка и проверки | `make ci`, `make security` |
| Audit Script | Проверка структуры | `python tools/audit_repo.py --output audit_report.json` |
| Journal Generator | Создание тестовых записей | `python SpaceCoreIskra_vOmega/modules/journal_generator.py --shadow 5` |
| Dist Builder | Сборка релиза | `python tools/build_dist.py ...` |

## API взаимодействия

- `SpaceCoreIskra_vOmega.modules.atelier.respond` — основной вход для генерации ответа.
- `IskraNexus_v1.api.call_connector(name, payload)` — доступ к внешним сервисам.
- `GrokCoreIskra_vGamma.prompts_repo.load_prompt(preset)` — загрузка шаблонов.

## Безопасность интеграций

- Каждая интеграция проходит через veil и ethics.
- Внешние API требуют явного разрешения в PR и обновления allowlist.
- Логи интеграций сохраняются в `logs/integrations/` (игнорируются git, но доступны в CI-артефактах).

## Расширение

1. Добавьте коннектор в `IskraNexus-v1` и задокументируйте его параметры.
2. Создайте тест, проверяющий успешный вызов и обработку ошибок.
3. Обновите README и данный документ.
4. Настройте мониторинг (например, health-check скрипт).
