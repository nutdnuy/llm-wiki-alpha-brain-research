import csv
import json
import tempfile
import unittest
from pathlib import Path
from support import fixture, write
from handoff import export_handoff
from copy import deepcopy
from validate import lint

class HandoffTests(unittest.TestCase):
    def test_synthetic_is_excluded(self):
        with tempfile.TemporaryDirectory() as temp:
            wiki = Path(temp).resolve() / 'wiki'
            fixture(wiki)
            self.assertEqual(export_handoff(wiki, Path(temp).resolve() / 'queue'), 0)

    def test_csv_preserves_expression_settings_and_manual_policy(self):
        with tempfile.TemporaryDirectory() as temp:
            wiki = Path(temp).resolve() / 'wiki'
            records = fixture(wiki)
            # In-memory test mutation exercises the export boundary, not evidence promotion.
            for record in records:
                record['synthetic'] = False
                write(wiki, record)
            records[2].update(research_state='static-pass')
            records[2]['settings']['comment'] = 'comma, quote " and ไทย'
            records[3]['settings'] = records[2]['settings'].copy()
            write(wiki, records[3])
            write(wiki, records[2])
            out = Path(temp).resolve() / 'queue'
            self.assertEqual(export_handoff(wiki, out), 1)
            with (out / '02_candidates.csv').open(newline='') as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row['expression'], records[2]['expression'])
            self.assertEqual(json.loads(row['settings_json']), records[2]['settings'])
            with (out / '03_simulation_queue.csv').open(newline='') as handle:
                queued = next(csv.DictReader(handle))
            self.assertEqual(queued['run_policy'], 'manual-only')
            self.assertEqual(queued['candidate_id'], row['candidate_id'])
            with self.assertRaises(ValueError):
                export_handoff(wiki, out)

    def test_only_eligible_candidates_and_no_wiki_mutations(self):
        with tempfile.TemporaryDirectory() as temp:
            wiki = Path(temp).resolve() / 'wiki'
            records = fixture(wiki)
            for record in records:
                record['synthetic'] = False
                write(wiki, record)
            for state in ('draft', 'static-pass', 'queued', 'failed', 'archive'):
                candidate = deepcopy(records[2])
                candidate.update(id='cand-' + state, research_state=state)
                write(wiki, candidate)
            synthetic = deepcopy(records[2])
            synthetic.update(id='cand-synthetic', synthetic=True, research_state='queued')
            write(wiki, synthetic)
            self.assertEqual(lint(wiki), [])
            before = {p.relative_to(wiki): p.read_bytes() for p in wiki.rglob('*') if p.is_file()}
            output = Path(temp).resolve() / 'out'
            self.assertEqual(export_handoff(wiki, output), 2)
            with (output / '02_candidates.csv').open(newline='', encoding='utf-8') as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, 'candidate_id,hypothesis_id,source_id,family,expression,settings_json,expected_effect,static_checks,status,notes'.split(','))
                self.assertEqual({row['candidate_id'] for row in reader}, {'cand-static-pass', 'cand-queued'})
            with (output / '03_simulation_queue.csv').open(newline='', encoding='utf-8') as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, 'queue_id,candidate_id,expression,settings_json,priority,reason,run_policy,status'.split(','))
                rows = list(reader)
                self.assertEqual(len(rows), 2)
                self.assertTrue(all(row['run_policy'] == 'manual-only' and row['status'] == 'queued' for row in rows))
            self.assertEqual(before, {p.relative_to(wiki): p.read_bytes() for p in wiki.rglob('*') if p.is_file()})

    def test_invalid_wiki_is_refused_before_output_creation(self):
        with tempfile.TemporaryDirectory() as temp:
            wiki = Path(temp).resolve() / 'wiki'
            records = fixture(wiki)
            records[2]['hypothesis'] = 'hyp-missing'
            write(wiki, records[2])
            output = Path(temp).resolve() / 'out'
            with self.assertRaisesRegex(ValueError, 'unresolved reference'):
                export_handoff(wiki, output)
            self.assertFalse(output.exists())

    def test_existing_file_directory_and_symlink_destinations_are_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp).resolve()
            wiki = base / 'wiki'
            fixture(wiki)
            (base / 'file').write_text('keep')
            (base / 'directory').mkdir()
            (base / 'link').symlink_to(base / 'missing')
            (base / 'parent-link').symlink_to(base / 'directory', target_is_directory=True)
            for output in (base / 'file', base / 'directory', base / 'link', base / 'parent-link' / 'new'):
                with self.subTest(output=output), self.assertRaises(ValueError):
                    export_handoff(wiki, output)
            self.assertEqual((base / 'file').read_text(), 'keep')
            self.assertEqual(list((base / 'directory').iterdir()), [])
