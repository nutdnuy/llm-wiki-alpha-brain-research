import json
import os
from pathlib import Path
import yaml
from model import FOLDERS, SETTINGS, STATES, digest, read_note, within

def _validate(root):
    root = Path(root).resolve()
    errors, notes = [], {}
    if not (root / '.brain-wiki.json').is_file():
        return ['missing .brain-wiki.json marker'], notes
    try:
        marker = json.loads((root / '.brain-wiki.json').read_text(encoding='utf-8'))
        if not isinstance(marker, dict) or type(marker.get('schema_version')) is not int or marker['schema_version'] != 1:
            return ['unsupported .brain-wiki.json schema_version; expected 1'], notes
    except (OSError, ValueError) as exc:
        return ['invalid .brain-wiki.json marker: ' + str(exc)], notes
    # Preflight every research entry before reading records. rglob/glob disagree
    # on directory symlinks; even empty or dangling links must fail closed.
    paths = []
    try:
        research = within(root, '02-Wiki')
        if not research.is_dir():
            return ['missing 02-Wiki research root'], notes

        def walk_error(exc):
            raise exc

        for directory, folders, files in os.walk(research, followlinks=False, onerror=walk_error):
            for name in sorted(folders + files):
                path = within(root, (Path(directory) / name).relative_to(root))
                if path.is_file() and path.suffix == '.md':
                    paths.append(path)
    except (ValueError, OSError) as exc:
        return ['research tree: ' + str(exc)], notes
    for path in sorted(paths):
        try:
            within(root, path.relative_to(root))
            note, body = read_note(path)
            identity = note['id']
            if identity in notes:
                raise ValueError('duplicate ID: ' + identity)
            expected = root / '02-Wiki' / FOLDERS[note['type']] / (identity + '.md')
            if path != expected:
                raise ValueError('filename/folder does not match ID/type')
            notes[identity] = (note, body)
        except (KeyError, ValueError, TypeError, OSError, yaml.YAMLError) as exc:
            errors.append(str(path.relative_to(root)) + ': ' + str(exc))

    def need(ok, message):
        if not ok:
            raise ValueError(message)

    def ref(identity, kind):
        need(isinstance(identity, str) and identity in notes,
             'unresolved reference: ' + str(identity))
        target = notes[identity][0]
        need(target['type'] == kind, 'wrong reference type: ' + identity)
        return target

    def hypothesis_has_synthetic_sources(hypothesis):
        need(isinstance(hypothesis['sources'], list), 'hypothesis sources must be a list')
        synthetic = False
        for citation in hypothesis['sources']:
            need(isinstance(citation, dict), 'citation must be a mapping')
            source = ref(citation['source'], 'source')
            synthetic = synthetic or source['synthetic']
        return synthetic

    def artifact(item):
        need(isinstance(item, dict), 'artifact must be a mapping')
        need(str(item['path']).startswith('01-Raw/'), 'evidence must be in 01-Raw')
        path = within(root, item['path'])
        need(path.is_file(), 'missing artifact: ' + item['path'])
        need(digest(path.read_bytes()) == item['sha256'], 'artifact hash mismatch')

    def setting(value):
        need(isinstance(value, dict), 'settings must be a mapping')
        need(SETTINGS <= value.keys(), 'missing reproduction settings')
        need(all(value[k] is not None for k in SETTINGS), 'null reproduction setting')
        need(type(value['delay']) is int and value['delay'] >= 0, 'invalid delay')
        json.dumps(value, allow_nan=False)

    def same_run(a, b):
        return a['expression'] == b['expression'] and a['settings'] == b['settings']

    for identity, (note, body) in notes.items():
        try:
            kind = note['type']
            if note['status'] == 'reviewed':
                need(note.get('reviewed_by') and note['reviewed_by'] != note['created_by'],
                     'reviewed requires an independent reviewer')
                need(note.get('review_evidence'), 'reviewed requires review evidence')
            if kind == 'source':
                artifact({'path': note['raw_path'], 'sha256': note['raw_sha256']})
                need(note['capture_completeness'] in {'complete', 'partial', 'unknown'},
                     'invalid capture completeness')
                need(note['origin'] and note['captured_at'] and note['capture_method'],
                     'source provenance is incomplete')
                need(isinstance(note['claims'], list) and note['claims'], 'claims are required')
                claim_ids = set()
                for claim in note['claims']:
                    need(isinstance(claim, dict), 'claim must be a mapping')
                    need(isinstance(claim.get('id'), str) and claim['id'].strip() and claim['id'] not in claim_ids, 'duplicate/empty claim ID')
                    claim_ids.add(claim['id'])
                    need(claim.get('text') and isinstance(claim.get('locator'), str)
                         and claim['locator'].strip(), 'claim needs text and locator')
                    need(claim.get('kind') in {'fact', 'interpretation', 'question'}, 'invalid claim kind')
                    need(claim.get('verification') in {'pending', 'verified', 'contradicted'},
                         'invalid claim verification')
            if kind in {'hypothesis', 'synthesis'}:
                need(isinstance(note['sources'], list) and note['sources'], 'sources are required')
                for item in note['sources']:
                    need(isinstance(item, dict), 'citation must be a mapping')
                    source = ref(item['source'], 'source')
                    need(item['claim'] in {c['id'] for c in source['claims']}, 'unresolved claim')
                    need(isinstance(item.get('locator'), str) and item['locator'].strip(),
                         'citation needs locator')
            if kind == 'hypothesis':
                for key in ('mechanism', 'expected_sign', 'horizon', 'data_requirements',
                            'leakage_checks', 'kill_criteria'):
                    need(bool(note[key]), 'hypothesis needs ' + key)
                for key in ('data_requirements', 'leakage_checks', 'kill_criteria'):
                    need(isinstance(note[key], list) and
                         all(isinstance(item, str) and item.strip() for item in note[key]),
                         'hypothesis ' + key + ' must be a list of nonempty strings')
            if kind == 'candidate':
                hypothesis = ref(note['hypothesis'], 'hypothesis')
                source = ref(note['source'], 'source')
                need(note['synthetic'] or not (source['synthetic'] or hypothesis['synthetic']
                                                 or hypothesis_has_synthetic_sources(hypothesis)),
                     'synthetic lineage cannot become a real candidate')
                need(note['source'] in {x['source'] for x in hypothesis['sources']},
                     'candidate source is outside its hypothesis')
                need(note['expression'].strip(), 'empty expression')
                setting(note['settings'])
                need(note['research_state'] in STATES, 'invalid candidate research state')
                need(bool(note['parent_candidate']) == bool(note['repair_experiment']),
                     'repair requires both parent and experiment')
                if note['parent_candidate']:
                    parent = ref(note['parent_candidate'], 'candidate')
                    repair = ref(note['repair_experiment'], 'experiment')
                    need(repair['candidate'] == parent['id'], 'repair experiment is not for parent')
                seen, current = {identity}, note
                while current.get('parent_candidate'):
                    parent_id = current['parent_candidate']
                    need(parent_id not in seen, 'candidate lineage cycle')
                    seen.add(parent_id)
                    current = ref(parent_id, 'candidate')
                    ancestor_source = ref(current['source'], 'source')
                    ancestor_hypothesis = ref(current['hypothesis'], 'hypothesis')
                    need(note['synthetic'] or not (current['synthetic'] or ancestor_source['synthetic']
                                                 or ancestor_hypothesis['synthetic']
                                                 or hypothesis_has_synthetic_sources(ancestor_hypothesis)),
                         'synthetic lineage cannot become a real candidate')
                evaluations = [x for x, _ in notes.values()
                               if x['type'] == 'experiment' and x['candidate'] == identity
                               and same_run(x, note) and x['evidence_kind'] == 'live_brain'
                               and not x['synthetic'] and x['artifacts']]
                if note['research_state'] in {'simulated', 'near-pass', 'hard-pass'}:
                    need(evaluations and not note['synthetic'], 'state requires real BRAIN evidence')
                if note['research_state'] == 'hard-pass':
                    need(any(x['decision'] == 'pass' for x in evaluations),
                         'hard-pass requires an evidenced pass decision')
                if note['research_state'] == 'failed':
                    need(note['notes'].strip(), 'failed candidate requires reason')
            if kind == 'experiment':
                candidate = ref(note['candidate'], 'candidate')
                need(note['synthetic'] or not candidate['synthetic'],
                     'synthetic candidate cannot produce a real experiment')
                setting(note['settings'])
                need(same_run(note, candidate), 'tested snapshot differs; create a new candidate')
                need(note['evidence_kind'] in {'untested', 'offline_proxy', 'live_brain'},
                     'invalid evidence kind')
                need(isinstance(note['metrics'], dict) and isinstance(note['checks'], dict),
                     'metrics/checks must be mappings')
                need(isinstance(note['artifacts'], list), 'artifacts must be a list')
                need(note['decision'] in {'pending', 'pass', 'near-pass', 'fail', 'archive'},
                     'invalid experiment decision')
                for item in note['artifacts']:
                    artifact(item)
                if note['evidence_kind'] == 'untested':
                    need(not note['metrics'] and not note['checks'] and not note['observed_at']
                         and not note['brain_alpha_id'] and note['decision'] == 'pending',
                         'untested record cannot contain observed results')
                else:
                    need(note['artifacts'] and note['observed_at'] and note['test_scope'],
                         'observed result needs artifacts, observation time and test scope')
                if note['decision'] == 'pass':
                    need(note['evidence_kind'] == 'live_brain' and not note['synthetic'],
                         'pass requires non-synthetic live evidence')
                    need(note['checks'].get('required_checks_complete') is True,
                         'pass requires a complete recorded check set')
                    need(isinstance(note['checks'].get('items'), dict) and note['checks']['items'] and
                         all(x == 'PASS' for x in note['checks']['items'].values()),
                         'pass requires all recorded checks to pass')
                    need(note['checks'].get('policy_source') and note['checks'].get('as_of'),
                         'pass requires dated platform policy source')
                if note['decision'] != 'pending':
                    need(note['reason'] and note['next_action'], 'decision needs reason and next action')
            if kind == 'synthesis':
                need(isinstance(note['limitations'], list) and note['limitations'],
                     'synthesis requires a limitations list')
                need(isinstance(note['experiments'], list), 'synthesis experiments must be a list')
                for item in note['experiments']:
                    ref(item, 'experiment')
        except (KeyError, ValueError, TypeError, AttributeError, OSError) as exc:
            errors.append(identity + ': ' + str(exc))
    return sorted(errors), notes


def lint(root):
    return _validate(root)[0]


def validated_records(root):
    """Return only containment-checked records from a successful validation."""
    errors, notes = _validate(root)
    if errors:
        raise ValueError('\n'.join(errors))
    return [note for note, _ in notes.values()]
