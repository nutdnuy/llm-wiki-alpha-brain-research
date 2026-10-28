import hashlib
import re
from pathlib import Path
import yaml

FOLDERS = {
    'source': 'Sources', 'hypothesis': 'Hypotheses',
    'candidate': 'Candidates', 'experiment': 'Experiments',
    'synthesis': 'Syntheses',
}
COMMON = {'id', 'type', 'title', 'status', 'sensitivity', 'created_by',
          'synthetic', 'created', 'updated'}
REQUIRED = {
    'source': {'origin', 'captured_at', 'raw_path', 'raw_sha256',
               'capture_method', 'capture_completeness', 'claims'},
    'hypothesis': {'sources', 'mechanism', 'expected_sign', 'horizon',
                   'data_requirements', 'leakage_checks', 'kill_criteria'},
    'candidate': {'hypothesis', 'source', 'family', 'expression', 'settings',
                  'expected_effect', 'static_checks', 'research_state',
                  'parent_candidate', 'repair_experiment', 'notes'},
    'experiment': {'candidate', 'evidence_kind', 'observed_at', 'expression',
                   'settings', 'artifacts', 'metrics', 'checks', 'decision',
                   'reason', 'next_action', 'test_scope', 'brain_alpha_id'},
    'synthesis': {'sources', 'experiments', 'limitations'},
}
SETTINGS = {'region', 'universe', 'delay', 'neutralization', 'decay',
            'truncation', 'pasteurization', 'nan_handling'}
STATES = {'draft', 'static-pass', 'queued', 'simulated', 'backtested', 'hard-pass',
          'near-pass', 'failed', 'archive'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def within(root, relative):
    root = Path(root).resolve()
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('artifact path must be relative without traversal')
    path = root / rel
    cursor = root
    for part in rel.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError('symlink is not an evidence artifact')
    if not path.resolve().is_relative_to(root):
        raise ValueError('artifact escapes wiki')
    return path

def read_note(path):
    text = Path(path).read_text(encoding='utf-8')
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        raise ValueError('missing YAML frontmatter')
    try:
        end = lines.index('---', 1)
    except ValueError:
        raise ValueError('unterminated YAML frontmatter') from None
    data = yaml.safe_load('\n'.join(lines[1:end]))
    if not isinstance(data, dict):
        raise ValueError('frontmatter must be a mapping')
    kind = data.get('type')
    if kind not in FOLDERS:
        raise ValueError('unknown note type')
    missing = sorted((COMMON | REQUIRED[kind]) - data.keys())
    if missing:
        raise ValueError('missing fields: ' + ', '.join(missing))
    if not re.fullmatch(r'[a-z][a-z0-9-]{2,79}', str(data['id'])):
        raise ValueError('invalid stable ID')
    if data['status'] not in {'draft', 'reviewed', 'conflicted'}:
        raise ValueError('invalid review status')
    if data['sensitivity'] not in {'public', 'personal', 'confidential', 'restricted'}:
        raise ValueError('invalid sensitivity')
    if not isinstance(data['synthetic'], bool):
        raise ValueError('synthetic must be boolean')
    for key in ('title', 'created_by', 'created', 'updated'):
        if not str(data[key] or '').strip():
            raise ValueError(key + ' must not be empty')
    body = '\n'.join(lines[end + 1:]).strip()
    if not body:
        raise ValueError('empty note body')
    return data, body
