"""Обзор ядра SpaceCoreIskra.

Этот документ в формате `.py` описывает ключевые компоненты:

- `ManifestValidator` — проверяет наличие файлов и согласованность с Manifest vΩ.
- `FacetActivationEngine` — переводит метрики в активные грани.
- `ReasoningChain` — генерирует мысли от имени каждой грани.
- `ReasoningPipeline` — декомпозирует задачи, планирует и проверяет контрпримеры.
- `ContextManager` — поддерживает память и обрезает историю.
- `RAGSystem` — индексирует проектные файлы и извлекает фрагменты.
- `RulesEnforcer` — реализует Rule 8/21/88 и дополнительные проверки.
- `IskraOrchestrator` — связывает всё во время одного ответа.

См. исходный код в `SpaceCoreIskra_vOmega/` для реализаций. Этот файл служит справкой и синхронизируется с README.
"""

from __future__ import annotations

COMPONENTS = [
    "ManifestValidator",
    "FacetActivationEngine",
    "ReasoningChain",
    "ReasoningPipeline",
    "ContextManager",
    "RAGSystem",
    "RulesEnforcer",
    "IskraOrchestrator",
]

