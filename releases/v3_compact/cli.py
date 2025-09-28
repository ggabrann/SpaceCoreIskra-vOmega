import argparse
import glob
import json
from pathlib import Path

from src.nia_core import Nia
from src.nia_tasks import Tasks
from src.nia_vector import TfIdf


def cal_import(path):
    events = []
    current = None
    try:
        with open(path, encoding='utf-8') as handle:
            for raw in handle:
                line = raw.strip()
                if line == 'BEGIN:VEVENT':
                    current = {}
                elif line == 'END:VEVENT':
                    if current:
                        events.append(current)
                    current = None
                elif current is not None and ':' in line:
                    key, value = line.split(':', 1)
                    key = key.lower()
                    if key in {'dtstart', 'dtend', 'summary', 'location'}:
                        current[key] = value
    except FileNotFoundError:
        return []
    return events


def run_search(query):
    tf = TfIdf()
    store = Path('memory/short_term.jsonl')
    if store.exists():
        with store.open(encoding='utf-8') as handle:
            for idx, line in enumerate(handle):
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                text = record.get('text', '')
                if text:
                    tf.add(f'memory:{idx}', text)
    hits = [{'id': doc_id, 'score': score} for doc_id, score in tf.score(query)]
    return hits


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--say', default='Привет')
    parser.add_argument('--persona')
    parser.add_argument('--mode', choices=['practical', 'lyrical', 'guardian'])
    parser.add_argument('--facet')
    parser.add_argument('--search')
    parser.add_argument('--cal-import')
    parser.add_argument('--cal-list', action='store_true')
    parser.add_argument('--task-add')
    parser.add_argument('--due')
    args = parser.parse_args()

    nia = Nia()
    if args.mode:
        nia.set_mode(args.mode)
    if args.persona:
        nia.set_persona(args.persona)

    if args.search:
        print(json.dumps(run_search(args.search), ensure_ascii=False, indent=2))
        raise SystemExit

    if args.cal_import:
        print(json.dumps(cal_import(args.cal_import), ensure_ascii=False, indent=2))
        raise SystemExit

    if args.cal_list:
        for path in glob.glob('*.ics'):
            print(path)
        raise SystemExit

    if args.task_add:
        task = Tasks().add(args.task_add, due=args.due)
        print(json.dumps(task, ensure_ascii=False, indent=2))
        raise SystemExit

    result = nia.reply(args.say, facet=args.facet)
    print(json.dumps(result, ensure_ascii=False, indent=2))
