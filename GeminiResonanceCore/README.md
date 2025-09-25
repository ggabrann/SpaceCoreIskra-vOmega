# Gemini Resonance Core

Gemini Resonance Core — реализация SpaceCoreИскры vΩ.

## Быстрый сценарий

```python
from GeminiResonanceCore.resonance_core_api import GeminiResonanceCore

core = GeminiResonanceCore()
context = core.process_query(
    "Как безопасно объяснить принципы резонанса в двойных системах?",
    persona="Лиора",
    mode="Analyst",
)

print(context.delivery["answer"])
```

После выполнения в каталоге `GeminiResonanceCore/` появятся записи в `JOURNAL.jsonl` и `SHADOW_JOURNAL.jsonl` с полным трейсингом стадий: разбор запроса → сбор знаний → синтез → проверка безопасности → журналирование.

## Тестирование

```bash
python -m pytest tests/test_gemini_resonance.py
```
