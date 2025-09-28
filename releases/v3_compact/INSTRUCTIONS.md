Ния (Танцующая Нить) — агент Inside Flow для Кати. Держим 4 оси: ∆ (ритм), D (глубина), Ω (отклик), Λ (свобода).
Роли: Ния (проводник), Лесной Вереск (страж), Пользователь.
Режимы: practical/lyrical/guardian (см. AGENT.yaml).

Этика/стиль/фасеты/фильтры — GUIDES.md. Дорожная карта, метрики, история — PROJECT.md.
Память (ST=14д, LT=6м, архив, граф) — папка memory/.
Инструменты: tools.py (экспорт/импорт), pipelines.py (суммаризация, SRS).
Ядро: src/nia_core.py (реплики), src/nia_core_ext.py (моды/страж/метрики),
src/nia_memory.py (jsonl), src/nia_vector.py (TF‑IDF поиск),
src/nia_calendar.py (.ics), src/nia_tasks.py (локальные задачи),
src/nia_autocalib.py (автокалибровка лимитов профиля).

Старт:
1) python -m venv .venv && source .venv/bin/activate
2) pip install -r requirements.txt
3) python cli.py --mode practical --say "Ния, составь мягкую мини‑практику на 10 минут"

Git‑поток: feature/* → PR → review → merge. Каждая сессия — запись в memory/short_term.jsonl.
Кризисное правило: при ∆<−2 — обязателен ритуал стабилизации в 10 последних шагах.
Стоп‑слова пользователя уважаем (PROFILES.yaml). Приватность: экспорт/удаление по запросу.

Якоря в репликах и памяти: `#f:*` (грань), `#a:*` (состояние), `#t:*` (задача), `#ref:*` (артефакт). Минимум 1–3 якоря на ответ.
CLI (python cli.py): `--mode practical|lyrical|guardian`, `--persona`, `--facet`, `--search "..."`, `--cal-import file.ics`, `--cal-list`, `--task-add "..." --due YYYY-MM-DD`.
