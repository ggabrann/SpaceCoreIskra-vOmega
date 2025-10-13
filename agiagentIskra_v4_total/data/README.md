# Data Core

`build_entropy_core.py` материализует искусственно созданное ядро высокой энтропии. Используется для:
- проверки пропускной способности пайплайнов и CI;
- обеспечения веса архива ≥ 5 МБ;
- стресс-тестов механизмов checksum и журналов.

Команды:

```bash
# создать ядро и обновить checksum
python agiagentIskra_v4_total/data/build_entropy_core.py

# сверить ожидаемую сумму без записи файла
python agiagentIskra_v4_total/data/build_entropy_core.py --dry-run
```

Файл `entropy_core.bin` не содержит пользовательских данных и может свободно распространяться после генерации.
