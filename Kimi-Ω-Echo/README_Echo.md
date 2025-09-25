# Kimi-Ω Echo — README

## Requirements

* Python 3.10+
* Virtual environment (optional but recommended)

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Запуск примерной сессии

```bash
python Kimi-Ω-Echo/example_session.py
```

Скрипт создаст файл `Kimi-Ω-Echo/JOURNAL.jsonl` с журнальной записью о конвейере.

## Тестирование

```bash
python -m pytest tests/test_kimi_echo.py
```

Тест запускает примерную сессию и проверяет, что фильтр блокирует запрещённые запросы.
