# NIA — Танцующая Нить v3 (Full, Expanded)

Этот пакет — полноценный релиз без заглушек:
- Constitutional AI: `src/ethics_veil.py` (мягкие/жёсткие стопы, конституция).
- Inference planning: `src/presets_router.py` — глубина размышления по сложности.
- RAG Rosette: `src/rag_panel.py` — шардинг и поиск, слияние результатов.
- Persona/Guardian: `src/persona_module.py` + `src/ethics_veil.py`.
- Ядро: `src/nia_core.py` — orchestrator (veil → route → RAG → ответы).
- Паттерны и парадоксы: `src/pattern_extractor.py`, `src/paradox_resolver.py`.
- Валидация журналов и аудит: `validators/validate_journal_enhanced.py`, `validators/audit_repo.py` + JSON Schemas.
- Поставка: `tools/pack_release.py` — манифест хэшей и zip-артефакт.
- CI: `.github/workflows/iskra-ci.yml`.