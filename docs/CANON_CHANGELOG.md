# CANON_CHANGELOG (Журнал Изменений Канона)

## 2025-10-25 - Инициализация проекта ТЕ́ЛОС-Δ (Фаза-0 PoC)

*   **Добавлено**: Инициализирована архитектура ТЕ́ЛОС-Δ (TEL̄OS-Delta) с фокусом на гибридном ядре (Attention/SSM), GraphRAG памяти и LangGraph оркестрации.
*   **Добавлено**: Внедрена концепция **Строгой Атрибуции** (каждый вывод связан с источником) и **Canon Review** (гейт качества).
*   **Добавлено**: Определена структура артефактов и папок для PoC (apps/etl, apps/rag, apps/orchestrator, ops/postgres).
*   **Добавлено**: Инициализированы DDL для pgvector (evidence, graph_node, graph_edge) в `AgiAgentIskra/ops/postgres/`.
*   **Добавлено**: Создана Карта Соответствия `compliance_map.md` с учетом EU AI Act (GPAI) и GPAI Code of Practice.
*   **Добавлено**: Создан базовый отчет метрик **CD-Index v0** для Фазы-0.

**Traceability Link**: `reports/cd-index_v0.json` (Report ID: cd-index_v0_20251025)

