
import json, jsonschema, sys
from pathlib import Path
SCHEMA_J = json.loads((Path('schemas/journal_entry.schema.json')).read_text(encoding='utf-8'))
SCHEMA_S = json.loads((Path('schemas/shadow_journal_entry.schema.json')).read_text(encoding='utf-8'))
def validate(path, schema):
    ok=True
    for i,line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        obj=json.loads(line)
        try:
            jsonschema.validate(obj, schema)
        except jsonschema.ValidationError as e:
            print(f"Line {i}: {e.message}"); ok=False
    return ok
if __name__=='__main__':
    ok1=validate('memory/short_term.jsonl', SCHEMA_J)
    ok2=validate('memory/long_term.jsonl', SCHEMA_J)
    ok3=validate('memory/archive.jsonl', SCHEMA_S)
    sys.exit(0 if (ok1 and ok2 and ok3) else 1)
