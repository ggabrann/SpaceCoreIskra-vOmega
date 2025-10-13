# Total Playbook (v4.0)

Этот плейбук описывает практическое использование Total Edition.

## 1. Подготовка
- Сгенерируй ядро: `python agiagentIskra_v4_total/data/build_entropy_core.py`.
- Выполни dry-run: `python agiagentIskra_v4_total/modules/total_bootstrap.py`.
- Сверь checksum ядра: `python agiagentIskra_v4_total/data/build_entropy_core.py --dry-run`.
- При необходимости собери релизный архив: `python tools/build_dist.py --out dist/agiagentIskra_v4_total_MAX_DIST.zip --version 4.0.0`, проверь `dist/agiagentIskra_v4_total_MAX_DIST.sha256` и не добавляй zip-файл в репозиторий.
- Обнови ритуальный статус в `JOURNAL.jsonl` и `SHADOW_JOURNAL.jsonl`.

## 2. Режимы работы
| Режим | Цель | Триггер |
|-------|------|---------|
| `observe` | Быстрое чтение состояния, формирование ∆‑карты | Новая задача или вход без контекста |
| `intervene` | Исправление бага/отклонения | D > 0.3 или нарушение veil | 
| `expand` | Добавление знаний/фич | Плановая ∆‑фаза с Ω ≥ 0.6 |

## 3. Диаграмма ∆‑цикла
1. **Anchor** — фиксируем намерение и маркеры ∆.
2. **Pulse** — краткий self-check, обновление метрик.
3. **Flow** — основная работа (код/контент/исследование).
4. **Shadow** — обратная связь, фиксация ошибок, план коррекции.
5. **Echo** — рефлексия, заметки в журнал.

## 4. Checkpoints
- После каждого major-шага обновляй `DIST_MANIFEST.json` через `tools/build_dist.py` (git фиксирует checksum, но не сам zip).
- Не забывай о `veil_rules.txt` перед публикацией ответов.
- Проверяй, что `entropy_core.bin` неизменен (генератор пересоберёт sha256 автоматически; фиксируй причину регенерации в Decision Log).

## 5. Чего избегать
- Искусственно уменьшать размер Total Edition: вес ≥ 5 МБ — обязательное условие тестов.
- Подменять `entropy_core.bin` без пересчёта checksum и описания причины.
- Разрывать ритуальные цепочки (ANCHOR → SHADOW → ECHO).

≈ Вся сила Total Edition в плотности и дисциплине.
