# IskraNexus v1

IskraNexus v1 — автономный оркестратор, объединяющий ядро SpaceCore с локальными модулями. Система использует несколько специализированных компонентов:

- `prompt_manager` — версионируемое хранилище промптов.
- `rag_connector` — панель документов с простым поиском.
- `persona_module` — реестр персон с оценкой близости концепций.
- `ethics_layer` + `veil` — этический и маскирующий фильтр.
- `atelier` — семантический анализ ответа.
- `cot_trim` — утилиты постобработки рассуждений.
- `self_journal` — shadow-лог шагов оркестратора.
- `journal_generator` — запись результатов по структуре манифеста.

Новый модуль `orchestrator` связывает компоненты и поддерживает режимы `banality`, `paradox`, `synthesis`. На каждом шаге фиксируются метрики и события, которые сохраняются в `JOURNAL.jsonl` и shadow-лог.

## Запуск пайплайна

```python
from IskraNexus_v1.modules.orchestrator import Orchestrator

orchestrator = Orchestrator()
result = orchestrator.process("Расскажи о цели Iskra Nexus", mode="synthesis")
print(result["response"])
```

## Проверка

Для запуска тестов используйте:

```bash
python -m pytest tests/test_iskra_nexus.py
```
