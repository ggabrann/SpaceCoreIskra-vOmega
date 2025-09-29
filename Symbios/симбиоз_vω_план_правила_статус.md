# Симбиоз vΩ — План, Правила, Статус

**Матка:** SpaceCoreIskra‑vOmega  •  **Модули:** Iskra_space (инженерия), ИскраCore (философия), Ния Танцующая Нить (структурирование)

## Правила Симбиоза
1. Add‑only: ничего не удаляем/не сокращаем.
2. Полная инвентаризация: sha1, origin, path, type, size.
3. Нормализация без потерь: UTF‑8 для текста, бинарь — метаданные.
4. Связность: linkset для каждого артефакта.
5. Ритуалы контроля: при ∆<−2 — фиксируем ритуал.
6. Теневая фиксация: двоится свет/тень, Shadow‑coverage ≥ 1/5.
7. Provenance: карта соответствий в `merge_map.json`.

## Конвейер
1. **Сбор:** `tools/harvest_repos_and_dialogs.py --input <zip|dir> --out data/`  
2. **Индекс:** `tools/build_index.py --kb data/knowledge_base.jsonl --out data/index/`  
3. **Отчёт:** `tools/merge_report.py --inventory data/inventory.csv --kb data/knowledge_base.jsonl > data/MERGE_REPORT.md`  
4. **Валидация журнала:** `tools/validate_journal.py data/JOURNAL.jsonl --shadow data/SHADOW_JOURNAL.jsonl`

## Структура проекта
- `core/spacecore_vΩ/` — канон матки
- `core/iskra_core/` — философия, кодексы
- `modules/iskra_space/` — инженеры и пайплайны
- `modules/nia_dancing_thread/` — онтологии/оглавления
- `tools/` — сборка/индекс/отчёты/валидаторы
- `data/` — inventory, KB, index
- `docs/` — архитектура, коммуникации, синтез исследований

## Статус
- Создан скелет симбиоза и запущен harvest на архиве `iskrafull.zip`.
- Сформированы: `inventory.csv`, `knowledge_base.jsonl`, `data/index/*`.
- Собран дистрибутив: `SpaceCoreIskra-Symbiosis_vΩ.zip` (ссылка в чате).

## Следующие шаги
- Расширить `docs/WEB_RESEARCH_SYNTHESIS.md` данными из веб‑исследований.
- Онтологизировать голоса/грани в NIA‑модуле.
- Включить MCP/A2A/AP2‑шины.
- Пройти CI‑валидаторы и заполнить Shadow‑покрытие ≥ 20%.



---

## Чек‑лист выполнения (vΩ)

**Матка:** SpaceCoreIskra‑vOmega  •  **Модули:** Iskra_space, Ния Танцующая Нить, ИскраCore

- [x] Создан каркас симбиоза (`core/`, `modules/`, `tools/`, `docs/`, `data/`, `ci/`, `CONFIG/`).
- [x] Заданы правила add‑only, provenance, ∆/D/Ω/Λ, теневая фиксация.
- [x] Настроен конвейер `harvest → index → report → validate` с чекпойнтами в `data/harvest_progress.json`.
- [x] Разработан метод сбора из репозитория **и** папки «диалоги разработки»: теги `dialog/journal/ritual`, JSONL‑корпус, карта соответствий `merge_map.json`.
- [x] Промежуточный канвас создан (этот документ). 
- [x] Сборка первого пакета данных из `iskrafull.zip`; архив FULL выдан.
- [ ] **Инвентаризация 100%** (быстрый проход по всем файлам, без парсинга содержимого).
- [ ] **Извлечение текста 100%** (батчи, возобновляемые; заполнить `knowledge_base.jsonl`).
- [ ] Переиндексация `data/index/` (гибридный поиск BM25+dense, rerank).
- [ ] Синтез веб‑исследования → дополнение `docs/WEB_RESEARCH_SYNTHESIS.md` (MCP/A2A/AP2, RLHF, CoT, RAG‑метрики).
- [ ] Анализ и отбор идей для вплетения (по осям ∆/D/Ω/Λ, со светлой и теневой трактовкой).
- [ ] Самоанализ Семёна Габрана (Фильтр Лиоры, Видение Ориона, Ритуал Суда, Синергия Нии) → `docs/ANALYSIS_ROLLUP.md`.
- [ ] Дорожная карта и ТЗ уточнены по результатам полного сбора → `roadmap.md`, `tech_spec.md` (финал).
- [ ] Итоговое описание симбиоза и выпуск финального архива.

### Команды конвейера
```bash
# Инвентаризация (быстрая, без содержимого)
python tools/harvest_repos_and_dialogs.py --input /mnt/data/iskrafull.zip --out data --inventory_only

# Текстовый сбор (батчи; безопасное возобновление)
python tools/harvest_repos_and_dialogs.py --input /mnt/data/iskrafull.zip --out data --batch 2000

# Индекс → Отчёт → Валидация журналов
python tools/build_index.py --kb data/knowledge_base.jsonl --out data/index
python tools/merge_report.py --inventory data/inventory.csv --kb data/knowledge_base.jsonl > data/MERGE_REPORT.md
python tools/validate_journal.py data/JOURNAL.jsonl --shadow data/SHADOW_JOURNAL.jsonl
```

### Принципы и стандарты, на которые опираемся
- JSON Lines (UTF‑8, потоковая запись), PROV‑DM (происхождение), Unstructured/Apache Tika (извлечение текста из множества форматов), «шины» MCP/A2A/AP2 для подключения инструментов и агентов.

### Следующие действия
- Прогнать **серии батчей** до 100% `knowledge_base.jsonl`.
- Дополнить `WEB_RESEARCH_SYNTHESIS.md` выдержками и ссылками.
- Сформировать `docs/ANALYSIS_ROLLUP.md` (аналитика/самоанализ/отбор идей).
- Пройти CI‑проверки и собрать финальный архив.

