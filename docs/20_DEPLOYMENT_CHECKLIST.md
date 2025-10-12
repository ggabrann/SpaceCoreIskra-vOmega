# Чек-лист деплоя Искры

## Перед стартом

- [ ] Версия в `pyproject.toml` и `DIST_MANIFEST.json` обновлена.
- [ ] CHANGELOG содержит секцию для релиза.
- [ ] README и docs синхронизированы с функциональностью.

## Проверки

- [ ] `make ci`
- [ ] `python tools/run_evals.py --config evals/configs/nightly.yaml`
- [ ] `python tools/audit_repo.py --output audit_report.json`
- [ ] `python tools/validate_journal_enhanced.py --journal SpaceCoreIskra_vOmega/JOURNAL.jsonl --shadow SpaceCoreIskra_vOmega/SHADOW_JOURNAL.jsonl`
- [ ] `python tools/build_dist.py --out dist/SpaceCoreIskra-vOmega_MAIN_CANON_DIST.zip --manifest DIST_MANIFEST.json --note DIST_NOTE.md`

## Документация

- [ ] Обновлены `DIST_NOTE.md` и `AUDIT_STATUS.md`.
- [ ] JOURNAL и SHADOW содержат записи о релизе (∆ ≥ 0).
- [ ] Shadow coverage ≥ 0.2.

## Релиз

- [ ] Создан тег Git (`git tag vX.Y.Z` + `git push origin vX.Y.Z`).
- [ ] Создан релиз на GitHub с описанием изменений и ссылками на артефакты.
- [ ] Дистрибутив загружен в раздел Releases.
- [ ] Проведён ритуал Эхо: короткий отчёт о ходе релиза.

## После релиза

- [ ] Запланированы задачи по улучшениям (если были обнаружены риски).
- [ ] Обновлён `PULSE_TRACKER.md`.
- [ ] Проверено, что новые инструменты задокументированы.
