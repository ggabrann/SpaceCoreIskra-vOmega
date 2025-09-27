import json
def log_entry(entry):
    with open("JOURNAL.jsonl","a",encoding="utf-8") as f: f.write(json.dumps(entry, ensure_ascii=False)+"\n")
