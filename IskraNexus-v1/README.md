# IskraNexus v1

IskraNexus v1 — автономный оркестратор, объединяющий ядро SpaceCore с локальными модулями. Система использует несколько специализированных компонентов:

- `prompt_manager` — версионируемое хранилище промптов с поиском и экспортом.
- `rag_connector` — панель документов с простым скорингом по релевантности и свежести.
- `persona_module` — реестр персон с оценкой близости концепций.
- `ethics_layer` и `veil` — этический и маскирующий фильтры.
- `atelier` — семантический анализ ответа.
- `cot_trim` — утилиты постобработки рассуждений.
- `self_journal` — shadow-лог шагов оркестратора.
- `journal_generator` — запись результатов по структуре манифеста.

Новый модуль `orchestrator` связывает компоненты и поддерживает режимы `banality`, `paradox`, `synthesis`. Процесс обработки запроса включает:

1. Сохранение промпта и запись первичных данных в shadow-лог.
2. Поиск контекста в RAG-панели и подбор персон по ключевым словам.
3. Генерацию ответа согласно выбранному режиму с последующей обрезкой рассуждений и фильтрацией.
4. Расчет метрик (`∆`, `D`, `Ω`, `Λ`) и запись события в `JOURNAL.jsonl` с учетом компонентов из манифеста.

## Запуск пайплайна

```python
from IskraNexus_v1.modules.orchestrator import Orchestrator

orchestrator = Orchestrator()
result = orchestrator.process("Расскажи о цели Iskra Nexus", mode="synthesis")
print(result["response"])
print(result["shadow_log"][0]["stage"])
```

## Проверка

Для запуска тестов используйте:

```bash
python -m pytest tests/test_iskra_nexus.py
```
