import sys
import os
from pathlib import Path
import yaml

REPO = Path(__file__).resolve().parents[1]
SKILL = Path(os.environ.get('BRAIN_WIKI_SKILL', REPO / 'skills' / 'llm-wiki-alpha-brain-research'))
sys.path.insert(0, str(SKILL / 'scripts'))
from model import FOLDERS, digest

SETTINGS = {'region': 'USA', 'universe': 'TOP3000', 'delay': 1,
            'neutralization': 'INDUSTRY', 'decay': 5, 'truncation': 0.08,
            'pasteurization': 'ON', 'nan_handling': 'OFF'}

def write(root, record, body='Synthetic research fixture. Not investment evidence.'):
    path = Path(root) / '02-Wiki' / FOLDERS[record['type']] / (record['id'] + '.md')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('---\n' + yaml.safe_dump(record, sort_keys=False)
                    + '---\n\n' + body + '\n', encoding='utf-8')
    return path

def fixture(root):
    root = Path(root)
    root.mkdir(exist_ok=True)
    (root / '.brain-wiki.json').write_text('{"schema_version": 1}\n')
    (root / '01-Raw').mkdir(exist_ok=True)
    raw = b'Synthetic premise: delayed response might create a testable signal.\n'
    artifact = {'path': '01-Raw/' + digest(raw) + '.bin', 'sha256': digest(raw)}
    (root / artifact['path']).write_bytes(raw)
    common = {'status': 'draft', 'sensitivity': 'public', 'created_by': 'fixture-author',
              'synthetic': True, 'created': '2026-10-15', 'updated': '2026-10-15'}
    citation = {'source': 'src-demo', 'claim': 'claim-01', 'locator': 'line 1'}
    source = dict(common, id='src-demo', type='source', title='Synthetic premise',
        origin='synthetic:demo', captured_at='2026-10-15T00:00:00Z',
        raw_path=artifact['path'], raw_sha256=artifact['sha256'],
        capture_method='authored synthetic text', capture_completeness='complete',
        claims=[{'id': 'claim-01', 'text': raw.decode().strip(), 'locator': 'line 1',
                 'kind': 'interpretation', 'verification': 'pending'}])
    hypothesis = dict(common, id='hyp-demo', type='hypothesis', title='Synthetic response hypothesis',
        sources=[citation], mechanism='Test whether delayed response persists.',
        expected_sign='positive conditional association', horizon='5 sessions',
        data_requirements=['point-in-time observations'],
        leakage_checks=['respect publication time'], kill_criteria=['effect absent out of sample'])
    candidate = dict(common, id='cand-demo', type='candidate', title='Synthetic expression',
        hypothesis='hyp-demo', source='src-demo', family='demo-response',
        expression='rank(ts_delta(close, 5))', settings=SETTINGS.copy(),
        expected_effect='untested illustrative relation', static_checks={'fields': 'unverified'},
        research_state='draft', parent_candidate=None, repair_experiment=None,
        notes='Illustrative syntax only; field availability is unverified.')
    experiment = dict(common, id='exp-demo', type='experiment', title='Synthetic planned experiment',
        candidate='cand-demo', evidence_kind='untested', observed_at=None,
        expression=candidate['expression'], settings=SETTINGS.copy(), artifacts=[],
        metrics={}, checks={}, decision='pending', reason='', next_action='Obtain authorized result',
        test_scope='not run', brain_alpha_id=None)
    synthesis = dict(common, id='syn-demo', type='synthesis', title='Synthetic evidence gap',
        sources=[citation], experiments=['exp-demo'], limitations=['No observed result exists.'])
    records = [source, hypothesis, candidate, experiment, synthesis]
    for record in records:
        write(root, record)
    return records
