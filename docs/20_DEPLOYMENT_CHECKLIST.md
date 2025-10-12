# Чек-лист релиза

## Перед релизом

- [ ] Обновить версию в `pyproject.toml`, `DIST_NOTE.md`, `DIST_MANIFEST.json`.
- [ ] Прогнать `make ci` и убедиться в отсутствии ошибок.
- [ ] Обновить `CHANGELOG.md` (раздел `Unreleased`).
- [ ] Проверить журналы через `validate_journal.py` и shadow coverage ≥ 0.2.
- [ ] Запустить `python tools/run_evals.py --config evals/configs/nightly.yaml`.
- [ ] Выполнить `python tools/run_security_checks.py`.

## Сборка

- [ ] `python tools/build_dist.py --out dist/SpaceCoreIskra-vOmega_MAIN_CANON_DIST.zip --manifest DIST_MANIFEST.json --note DIST_NOTE.md`
- [ ] Проверить, что новые файлы указаны в `DIST_MANIFEST.json`.

## Публикация

- [ ] Создать git-тег и релиз на GitHub.
- [ ] Обновить Model Cards в `cards/`.
- [ ] Добавить релизную запись в JOURNAL/SHADOW_JOURNAL.

