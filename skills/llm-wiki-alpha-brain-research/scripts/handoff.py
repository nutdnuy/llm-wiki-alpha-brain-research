import csv
import json
from pathlib import Path
from model import read_note
from validate import lint

CANDIDATE_FIELDS = ['candidate_id', 'hypothesis_id', 'source_id', 'family',
                    'expression', 'settings_json', 'expected_effect',
                    'static_checks', 'status', 'notes']
QUEUE_FIELDS = ['queue_id', 'candidate_id', 'expression', 'settings_json',
                'priority', 'reason', 'run_policy', 'status']

def export_handoff(root, output) -> int:
    root, output = Path(root).resolve(), Path(output).absolute()
    errors = lint(root)
    if errors:
        raise ValueError('\n'.join(errors))
    if output.exists() or output.is_symlink():
        raise ValueError('handoff destination already exists')
    if any(parent.is_symlink() for parent in output.parents):
        raise ValueError('handoff destination has a symlink parent')
    rows, queue = [], []
    for path in sorted((root / '02-Wiki' / 'Candidates').glob('*.md')):
        note, _ = read_note(path)
        if note['synthetic'] or note['research_state'] not in {'static-pass', 'queued'}:
            continue
        settings = json.dumps(note['settings'], sort_keys=True, ensure_ascii=False)
        rows.append(dict(zip(CANDIDATE_FIELDS, [note['id'], note['hypothesis'],
            note['source'], note['family'], note['expression'], settings,
            note['expected_effect'], json.dumps(note['static_checks']),
            note['research_state'], note['notes']])))
        queue.append(dict(zip(QUEUE_FIELDS, ['q-' + note['id'], note['id'],
            note['expression'], settings, 'normal', note['expected_effect'],
            'manual-only', 'queued'])))
    output.mkdir(parents=False)
    for filename, fields, data in [('02_candidates.csv', CANDIDATE_FIELDS, rows),
                                   ('03_simulation_queue.csv', QUEUE_FIELDS, queue)]:
        with (output / filename).open('x', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
    return len(rows)
