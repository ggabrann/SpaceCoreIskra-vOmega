# Архитектурный обзор MkDocs/CLI/Model Card

```mermaid
flowchart TD
    CLI[CLI `iskra`] -->|форматирует ответ| Rituals[∆DΩΛ]
    Rituals --> Journals[Journals + Shadow]
    CLI --> Docs[Docs]
    Docs -->|MkDocs build| Pages[GitHub Pages]
    Docs --> Generator[Model Card Generator]
    Generator --> Card[model_cards/model_card.json]
    Generator --> ModelCardDoc[docs/model_card.md]
    Pages --> Readers[Читатель]
```

- **CLI `iskra`** — отдельный пакет `src/iskra_cli`, который можно установить через `pip install -e .`.
- **Документация** — `mkdocs.yml` собирает существующие материалы в навигацию и обеспечивает GitHub Pages.
- **Model Card** — `tools/generate_model_card.py` пересчитывает SHA256 и размеры файлов; workflow коммитит обновления по расписанию.

## Поток действий

1. Автор обновляет код/документы.
2. Запускает `python tools/generate_model_card.py`, затем `mkdocs build`.
3. GitHub Actions проверяют тесты (`ci.yml`), ссылки (`linkcheck.yml`), публикуют сайт (`pages.yml`) и обновляют карточку (`modelcard.yml`).
