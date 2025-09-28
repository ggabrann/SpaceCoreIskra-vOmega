import json, os
from datetime import datetime


def _append(path, obj):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False) + '\n')


def write_short_term(path='memory/short_term.jsonl', text='', tags=None, anchors=None):
    payload = {
        'ts': datetime.utcnow().isoformat(),
        'text': text,
        'tags': tags or [],
        'anchors': anchors or [],
    }
    _append(path, payload)
