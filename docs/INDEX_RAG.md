# Индекс RAG (Что и как индексируем)

## 1. Данные → Вектор → Граф → Контекст ответа

### 1.1. Векторный слой (Evidence)
*   **Схема данных**: `evidence(id, source_uri, fragment_span, text, emb, checksum)`
*   **Индекс**: `pgvector` (`IVFFlat` или `HNSW`).
*   **Тюнинг**: `IVFFlat` (для роста корпуса) + `ANALYZE` после bulk-load; `HNSW` как альтернатива (другие компромиссы по вставкам/поиску).

### 1.2. Графовый слой (GraphRAG)
*   **Узлы (Nodes)**: `graph_node(id, type, title, description, aliases, metadata)`
    *   *Типы*: Research, Data/KG, Agents/Tools, Serve/Perf, Safety/Policy, Prod/Obs.
*   **Ребра (Edges)**: `graph_edge(source_id, target_id, type, weight, metadata)`
*   **Маппинг**: `evidence_graph_mapping(evidence_id, graph_node_id, confidence)`
*   **Применение**: Локальные и "комьюнити"-сводки для узлов/кластеров. MSR-подход для "глобальных" вопросов.

### 1.3. Оркестрация
*   **Фреймворк**: LangGraph.
*   **Особенность**: Возможность **обновлять `state` из `tools`** (для "памяти действий" и фактов, найденных в процессе работы).

## 2. Запросы (Шаблоны)
*   **Шаблон 1**: «Покажи все Evidence, поддерживающие Claim X, с цитатами по `frag_id` и similarity "e Д"». (Запрос на атрибуцию)
*   **Шаблон 2**: «Какие Requirements покрывает Component Y (дыры?)». (Запрос на покрытие/валидацию)
*   **Шаблон 3**: «Цепочка Evidence → Claim → Decision для baseline_report». (Запрос на трассировку)

## 3. Оценка RAG (RAGAS)
*   **Метрики**: `Faithfulness` (консистентность вывода с контекстом), `Answer Groundedness` и др.
*   **Фиксация**: Фиксировать версию/конфиг для сравнения.

## 4. Структура артефактов (Репозиторий)
*   **`/apps/rag`**: `GraphRAGManager` (вектор/гибрид), цитирование, сводки.
*   **`/apps/etl`**: Ingest pipeline (chunk, embed, insert to pgvector).
*   **`/ops/postgres`**: DDL для `evidence`, `graph_node`, `graph_edge`, `evidence_graph_mapping` и индексы.
*   **`/reports`**: `cd-index_v0.json` (CD-Index), `kappa_score.json`.
*   **`/docs/compliance`**: `compliance_map.md`.
*   **`/docs`**: `CANON_CHANGELOG.md` (с `traceability_link` на `cd-index_v0.json`).

