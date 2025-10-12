# SpaceCoreIskra vΩ

Мета-организм идей. Баланс Кристалла и Антикристалла.  
Новые модули vΩ: prompts_repo, personas, rag_panel, presets_router.  
Процесс: огранка граней → CI-агрегация.

## Agent mode (PEV)
- **Plan → Execute → Verify** с ручными подтверждениями для действий с последствиями.
- Метрики в каждом шаге: ∆/D/Ω/Λ; crisis-rule (при ∆≤−2 требуется `ritual`).
- Артефакты и ссылки добавляются в `events.evidence[]`.

Проверка локально:
```bash
python tools/validate_journal_enhanced.py SpaceCoreIskra_vΩ/JOURNAL.jsonl --shadow SpaceCoreIskra_vΩ/SHADOW_JOURNAL.jsonl --window 50
```
