# Документация SpaceCore Iskra v3.6

**Версия: 3.6.0**
**Дата: 2025-10-13**

## Архитектура SpaceCore Iskra (Mermaid)

```mermaid
flowchart TD
    User[Пользователь] --> Veil[Veil/Guardrails]
    Veil --> Core[Ядро: 09_CODE_CORE.py]
    Core -->|Оркестрация| FacetA[Грань A] & FacetB[Грань B] & FacetC[Грань C]
    Core -->|Метрики ∆DΩΛ| Utilities[Утилиты: 10_CODE_UTILITIES.py]
    Core --> Memory[Контекст/Память/RAG]
    Utilities --> CLI[CLI/make]
    CLI --> User
```

## Начать за 2 минуты
1. Клонируйте репозиторий.
2. `make setup`
3. `make test`
