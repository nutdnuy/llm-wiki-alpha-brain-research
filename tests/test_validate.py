import tempfile
import unittest
from pathlib import Path
from support import fixture, write
from validate import lint

class ValidationTests(unittest.TestCase):
    def test_valid_chain(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture(temp)
            self.assertEqual(lint(temp), [])

    def test_broken_claim_and_raw_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            records[1]['sources'][0]['claim'] = 'claim-missing'
            write(temp, records[1])
            (Path(temp) / records[0]['raw_path']).write_bytes(b'changed')
            errors = '\n'.join(lint(temp))
            self.assertIn('unresolved claim', errors)
            self.assertIn('artifact hash mismatch', errors)

    def test_synthetic_hard_pass_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            records[2]['research_state'] = 'hard-pass'
            write(temp, records[2])
            self.assertIn('state requires real BRAIN evidence', '\n'.join(lint(temp)))

    def test_snapshot_and_repair_lineage(self):
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            records[3]['expression'] = 'different_expression'
            write(temp, records[3])
            records[2]['parent_candidate'] = 'cand-demo'
            records[2]['repair_experiment'] = 'exp-demo'
            write(temp, records[2])
            errors = '\n'.join(lint(temp))
            self.assertIn('candidate lineage cycle', errors)
            self.assertIn('tested snapshot differs', errors)

    def test_untested_cannot_contain_metrics(self):
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            records[3]['metrics'] = {'sharpe': 0}
            write(temp, records[3])
            self.assertIn('untested record cannot', '\n'.join(lint(temp)))

    def test_failed_proxy_preserves_zero_and_null(self):
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            records[3].update(evidence_kind='offline_proxy', observed_at='2026-10-15T00:00:00Z',
                artifacts=[{'path': records[0]['raw_path'], 'sha256': records[0]['raw_sha256']}],
                test_scope='synthetic test artifact; no actual model run',
                metrics={'sharpe': 0, 'fitness': None}, checks={'sample': 'FAIL'},
                decision='fail', reason='Synthetic negative case', next_action='Keep failure')
            write(temp, records[3])
            self.assertEqual(lint(temp), [])

    def test_duplicate_id_and_independent_review(self):
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            source = write(temp, records[0])
            source.with_name('duplicate.md').write_bytes(source.read_bytes())
            records[1].update(status='reviewed', reviewed_by='fixture-author', review_evidence='self')
            write(temp, records[1])
            errors = '\n'.join(lint(temp))
            self.assertTrue('duplicate ID' in errors or 'filename/folder' in errors)
            self.assertIn('independent reviewer', errors)

    def test_synthetic_ancestry_cannot_be_exported_as_real(self):
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            records[2]['synthetic'] = False
            write(temp, records[2])
            self.assertIn('synthetic lineage cannot become a real candidate', '\n'.join(lint(temp)))

    def test_marker_and_research_root_are_required(self):
        for marker in ('{}', '[]', '{bad', '{"schema_version": 2}', '{"schema_version": true}'):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as temp:
                fixture(temp)
                (Path(temp) / '.brain-wiki.json').write_text(marker)
                self.assertTrue(lint(temp))
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / '.brain-wiki.json').write_text('{"schema_version": 1}')
            self.assertIn('missing 02-Wiki', '\n'.join(lint(temp)))

    def test_citation_locator_may_refine_source_claim(self):
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            records[1]['sources'][0]['locator'] = 'invented page 99'
            write(temp, records[1])
            self.assertEqual(lint(temp), [])

    def test_malformed_yaml_and_container_types_return_errors(self):
        import yaml
        cases = [(0, 'type', []), (0, 'claims', [None]),
                 (0, 'capture_completeness', []), (1, 'sources', [None]),
                 (1, 'data_requirements', 'not a list'), (4, 'limitations', 'not a list'),
                 (2, 'settings', []), (2, 'research_state', []),
                 (3, 'evidence_kind', []), (4, 'experiments', None)]
        for index, key, value in cases:
            with self.subTest(key=key), tempfile.TemporaryDirectory() as temp:
                records = fixture(temp)
                path = write(temp, records[index])
                records[index][key] = value
                path.write_text('---\n' + yaml.safe_dump(records[index]) + '---\n\nBody\n')
                self.assertTrue(lint(temp))
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            write(temp, records[0]).write_text('---\nid: [\n---\nBody')
            self.assertTrue(lint(temp))

    def test_real_child_cannot_hide_synthetic_parent(self):
        import copy
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            child = copy.deepcopy(records[2])
            child.update(id='cand-child', synthetic=False, parent_candidate='cand-demo', repair_experiment='exp-demo')
            for record in records[:2]:
                record['synthetic'] = False
                write(temp, record)
            write(temp, child)
            self.assertIn('synthetic lineage cannot become a real candidate', '\n'.join(lint(temp)))

    def test_real_experiment_cannot_hide_synthetic_candidate(self):
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            records[3]['synthetic'] = False
            write(temp, records[3])
            self.assertIn('synthetic candidate cannot produce a real experiment', '\n'.join(lint(temp)))

    def test_live_pass_and_matching_candidate_promotion(self):
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            for record in records:
                record['synthetic'] = False
            records[2]['research_state'] = 'hard-pass'
            records[3].update(evidence_kind='live_brain', observed_at='2026-10-15T00:00:00Z',
                artifacts=[{'path': records[0]['raw_path'], 'sha256': records[0]['raw_sha256']}],
                test_scope='Recorded result snapshot fixture', metrics={'sharpe': 0, 'fitness': None},
                checks={'required_checks_complete': True, 'items': {'sample': 'PASS'},
                        'policy_source': 'recorded-policy', 'as_of': '2026-10-15'},
                decision='pass', reason='Fixture checks complete', next_action='Review')
            for record in records:
                write(temp, record)
            self.assertEqual(lint(temp), [])
            records[3]['checks']['items'] = ['PASS']
            write(temp, records[3])
            self.assertIn('all recorded checks', '\n'.join(lint(temp)))

    def test_artifact_paths_reject_traversal_and_symlinks(self):
        for raw_path in ('01-Raw/../outside.bin', '/tmp/outside.bin', '01-Raw/link.bin'):
            with self.subTest(raw_path=raw_path), tempfile.TemporaryDirectory() as temp:
                records = fixture(temp)
                (Path(temp) / '01-Raw/link.bin').symlink_to(Path(temp) / records[0]['raw_path'])
                records[0]['raw_path'] = raw_path
                write(temp, records[0])
                self.assertTrue(lint(temp))

    def test_claim_and_citation_locators_require_nonblank_strings(self):
        for boundary in ('claim', 'citation'):
            for locator in ('   ', ['invalid locator container']):
                with self.subTest(boundary=boundary, locator=locator), tempfile.TemporaryDirectory() as temp:
                    records = fixture(temp)
                    if boundary == 'claim':
                        records[0]['claims'][0]['locator'] = locator
                        write(temp, records[0])
                        expected = 'claim needs text and locator'
                    else:
                        records[1]['sources'][0]['locator'] = locator
                        write(temp, records[1])
                        expected = 'citation needs locator'
                    self.assertIn(expected, '\n'.join(lint(temp)))
