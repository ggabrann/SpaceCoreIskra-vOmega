"""Обзор ядра SpaceCoreIskra.

Этот документ описывает основные компоненты, отвечающие за ритуалы Искры. Он служит справкой для разработчиков и привязан к исходному коду в `SpaceCoreIskra_vOmega/`.
"""

from __future__ import annotations

COMPONENTS = {
    "ManifestValidator": {
        "module": "SpaceCoreIskra_vOmega.manifest",
        "responsibility": "проверяет структуру репозитория на соответствие Manifest vΩ, читает dependency graph и формирует отчёт",
    },
    "FacetActivationEngine": {
        "module": "SpaceCoreIskra_vOmega.modules.facets_refine",
        "responsibility": "преобразует метрики в активные грани, учитывая тон, парадокс и безопасность",
    },
    "ReasoningChain": {
        "module": "SpaceCoreIskra_vOmega.modules.personas",
        "responsibility": "генерирует мыслеформы от имени каждой грани и объединяет их в Совет",
    },
    "ReasoningPipeline": {
        "module": "SpaceCoreIskra_vOmega.modules.presets_router",
        "responsibility": "декомпозирует задачи, планирует шаги, проверяет контрпримеры и синхронизирует с журналами",
    },
    "ContextManager": {
        "module": "SpaceCoreIskra_vOmega.modules.personas",
        "responsibility": "ведёт память сеанса, pack_context и promise ledger",
    },
    "RAGSystem": {
        "module": "SpaceCoreIskra_vOmega.modules.rag_panel",
        "responsibility": "индексирует файлы проекта, выполняет ranked_search, комбинирует внутренние и внешние источники",
    },
    "RulesEnforcer": {
        "module": "SpaceCoreIskra_vOmega.modules.personas",
        "responsibility": "контролирует Rule 8/21/88, проверяет честность и наличие источников",
    },
    "IskraOrchestrator": {
        "module": "SpaceCoreIskra_vOmega.modules.atelier",
        "responsibility": "собирает всё во время ответа: выбирает персону, вызывает RAG, проверяет формат, обновляет журналы",
    },
}

WORKFLOW = """
1. ManifestValidator убеждается, что все обязательные документы и журналы на месте.
2. ContextManager собирает контекст и обновляет обещания.
3. FacetActivationEngine выбирает активные грани на основе метрик.
4. ReasoningPipeline строит план, ReasoningChain — голоса граней.
5. RAGSystem подбирает фрагменты знаний, RulesEnforcer проверяет соблюдение правил.
6. IskraOrchestrator синтезирует ответ, запускает валидаторы формата и ∆DΩΛ, логирует результат.
"""

__all__ = ["COMPONENTS", "WORKFLOW"]
