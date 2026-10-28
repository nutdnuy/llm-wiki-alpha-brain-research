"""Offline contract tests. Fixtures are never evidence of financial performance."""
import copy
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from brain_wiki import rebuild_index
from handoff import export_handoff
from model import FOLDERS
from storage import capture, initialize
from validate import lint


class SharedWikiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.wiki = initialize(self.base / 'wiki')
        source = self.base / 'test-source.txt'
        source.write_text('UNIT TEST FIXTURE. Section 1: placeholder source assertion.\n')
        self.raw = capture(self.wiki, source)
        self.common = dict(status='draft', sensitivity='public', created_by='test-author',
                           synthetic=True, created='2026-01-01', updated='2026-01-01')
        self.brain_settings = dict(region='USA', universe='TEST-UNIVERSE', delay=1,
                                   neutralization='INDUSTRY', decay=0, truncation=0.01,
                                   pasteurization='ON', nan_handling='OFF')
        self.python_settings = dict(engine='qlib', engine_version='fixture-version',
                                    code_revision='fixture-code-hash', data_snapshot='fixture-data-hash',
                                    universe='fixture-point-in-time', sample_start='2020-01-01',
                                    sample_end='2021-12-31', signal_lag_bars=1, execution_lag_bars=1,
                                    rebalance='daily', execution_price='next-open',
                                    portfolio='fixture-long-short-equal-weight',
                                    costs=dict(commission_bps=1.0, slippage_bps=2.0, borrow_bps_per_year=100.0))
        self.notes = {}
        self.add('src-test', 'source', origin='unit-test-fixture', captured_at='2026-01-01',
                 raw_path=self.raw['path'], raw_sha256=self.raw['sha256'], capture_method='test',
                 capture_completeness='complete',
                 claims=[dict(id='claim-01', text='Test assertion only', locator='Section 1',
                              kind='fact', verification='pending')])
        self.add('hyp-test', 'hypothesis',
                 sources=[dict(source='src-test', claim='claim-01', locator='Section 1')],
                 mechanism='Test mechanism', expected_sign='positive', horizon='one month',
                 data_requirements=['timestamped data'], leakage_checks=['release cutoff'],
                 kill_criteria=['predeclared test fails'])
        for engine, settings in [('brain', self.brain_settings), ('python', self.python_settings)]:
            self.add('cand-' + engine, 'candidate', backend=engine, hypothesis='hyp-test',
                     source='src-test', family='test', expression='test-signal',
                     settings=copy.deepcopy(settings), expected_effect='test effect', static_checks={},
                     research_state='draft', parent_candidate=None, repair_experiment=None, notes='')
        self.save()

    def add(self, identity, kind, **fields):
        self.notes[identity] = self.common | dict(id=identity, type=kind, title=identity) | fields
        return self.notes[identity]

    def save(self):
        for note in self.notes.values():
            p = self.wiki / '02-Wiki' / FOLDERS[note['type']] / (note['id'] + '.md')
            p.write_text('---\n' + yaml.safe_dump(note, sort_keys=False) +
                         '---\n\nUNIT TEST FIXTURE; no empirical claim.\n')

    def experiment(self, engine, kind='untested', real_shape=False):
        # False synthetic flags exercise the imported-real-result schema branch
        # only inside this disposable test directory; they are not research data.
        if real_shape:
            for n in self.notes.values():
                n['synthetic'] = False
        candidate = self.notes['cand-' + engine]
        observed = kind != 'untested'
        return self.add('exp-' + engine, 'experiment', backend=engine,
                        synthetic=not real_shape, candidate=candidate['id'], evidence_kind=kind,
                        observed_at='2026-01-02' if observed else None,
                        expression=candidate['expression'], settings=copy.deepcopy(candidate['settings']),
                        artifacts=[dict(path=self.raw['path'], sha256=self.raw['sha256'])] if observed else [],
                        metrics={'turnover': {'value': 0, 'unit': 'fraction'}} if observed else {},
                        checks={}, decision='pending', reason='', next_action='',
                        test_scope={'fixture': 'IS only; not a real result'} if observed else {},
                        brain_alpha_id=None)

    def assertInvalid(self, phrase):
        self.save()
        errors = lint(self.wiki)
        self.assertTrue(any(phrase in e for e in errors), errors)

    def test_shared_hypothesis_and_separate_backend_records(self):
        self.experiment('brain')
        self.experiment('python')
        self.save()
        self.assertEqual(lint(self.wiki), [])
        rebuild_index(self.wiki)
        content = (self.wiki / '05-Index/Research.md').read_text()
        self.assertIn('02-Wiki/Candidates/cand-brain', content)
        self.assertIn('02-Wiki/Candidates/cand-python', content)

    def test_legacy_brain_record_still_valid(self):
        self.notes['cand-brain'].pop('backend')
        exp = self.experiment('brain')
        exp.pop('backend')
        self.save()
        self.assertEqual(lint(self.wiki), [])

    def test_brain_export_excludes_python_and_preserves_settings(self):
        for n in self.notes.values():
            n['synthetic'] = False
        for key in ['cand-brain', 'cand-python']:
            self.notes[key]['research_state'] = 'static-pass'
        self.notes['cand-brain'].pop('backend')
        self.save()
        before = {p: p.read_bytes() for p in self.wiki.rglob('*') if p.is_file()}
        out = self.base / 'handoff'
        self.assertEqual(export_handoff(self.wiki, out), 1)
        with (out / '02_candidates.csv').open() as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([r['candidate_id'] for r in rows], ['cand-brain'])
        self.assertEqual(json.loads(rows[0]['settings_json']), self.brain_settings)
        with (out / '03_simulation_queue.csv').open() as handle:
            queue = list(csv.DictReader(handle))
        self.assertEqual(queue[0]['run_policy'], 'manual-only')
        self.assertEqual(before, {p: p.read_bytes() for p in self.wiki.rglob('*') if p.is_file()})

    def test_unknown_backend_rejected(self):
        self.notes['cand-python']['backend'] = 'unknown'
        self.assertInvalid('backend must be')

    def test_cross_backend_snapshot_rejected(self):
        exp = self.experiment('python')
        exp['candidate'] = 'cand-brain'
        self.assertInvalid('tested snapshot differs')

    def test_local_result_cannot_claim_brain_evidence(self):
        self.experiment('python', 'live_brain')
        self.assertInvalid('evidence kind does not match')

    def test_brain_result_cannot_claim_local_evidence(self):
        self.experiment('brain', 'local_backtest')
        self.assertInvalid('evidence kind does not match')

    def test_extra_setting_change_needs_new_candidate(self):
        exp = self.experiment('python')
        exp['settings']['seed'] = 7
        self.assertInvalid('tested snapshot differs')

    def test_python_missing_costs_rejected(self):
        del self.notes['cand-python']['settings']['costs']
        self.assertInvalid('missing Python reproduction settings')

    def test_cost_units_unknown_and_invalid_values_rejected(self):
        for bad in [None, -1, True, float('nan')]:
            with self.subTest(value=bad):
                self.notes['cand-python']['settings']['costs']['slippage_bps'] = bad
                self.save()
                self.assertTrue(lint(self.wiki))

    def test_python_sample_order_rejected(self):
        self.notes['cand-python']['settings']['sample_start'] = '2022-01-01'
        self.assertInvalid('sample_start must not follow')

    def test_actual_backend_artifacts_allow_execution_state(self):
        for engine, kind, state in [('brain', 'live_brain', 'simulated'),
                                    ('python', 'local_backtest', 'backtested')]:
            self.experiment(engine, kind, real_shape=True)
            self.notes['cand-' + engine]['research_state'] = state
        self.save()
        self.assertEqual(lint(self.wiki), [])

    def test_untested_cannot_claim_backtested(self):
        self.notes['cand-python']['research_state'] = 'backtested'
        self.assertInvalid('state requires real matching-backend evidence')

    def test_python_cannot_use_brain_candidate_state(self):
        self.notes['cand-python']['research_state'] = 'simulated'
        self.assertInvalid('Python candidates use backtested')

    def test_proxy_cannot_pass(self):
        exp = self.experiment('python', 'offline_proxy', real_shape=True)
        exp['decision'] = 'pass'
        self.assertInvalid('pass requires non-synthetic matching-backend evidence')

    def test_pass_requires_dated_complete_policy(self):
        exp = self.experiment('python', 'local_backtest', real_shape=True)
        exp.update(decision='pass', reason='fixture criteria', next_action='fixture review')
        self.assertInvalid('complete recorded check set')
        exp['checks'] = dict(required_checks_complete=True, items={'fixture-oos': 'PASS'},
                             policy_source='fixture-predeclared-plan', as_of='2026-01-01')
        self.notes['cand-python']['research_state'] = 'hard-pass'
        self.save()
        self.assertEqual(lint(self.wiki), [])
        del exp['checks']['policy_source']
        self.assertInvalid('dated backend evaluation policy')

    def test_synthetic_result_cannot_pass(self):
        exp = self.experiment('python', 'local_backtest')
        exp['decision'] = 'pass'
        self.assertInvalid('pass requires non-synthetic matching-backend evidence')

    def test_synthetic_source_cannot_become_real_candidate(self):
        self.notes['cand-python']['synthetic'] = False
        self.assertInvalid('synthetic lineage cannot become a real candidate')

    def test_repair_cannot_cross_backends(self):
        self.experiment('brain')
        self.notes['cand-python'].update(parent_candidate='cand-brain', repair_experiment='exp-brain')
        self.assertInvalid('repair cannot cross backends')

    def test_raw_tamper_detected(self):
        (self.wiki / self.raw['path']).write_text('changed')
        self.assertInvalid('artifact hash mismatch')

    def test_templates_copied_and_reinit_preserves_files(self):
        self.assertEqual(len(list((self.wiki / '04-Schema/Templates').glob('*.md'))), 7)
        before = (self.wiki / '05-Index/Home.md').read_bytes()
        with self.assertRaises(ValueError):
            initialize(self.wiki)
        self.assertEqual(before, (self.wiki / '05-Index/Home.md').read_bytes())


if __name__ == '__main__':
    unittest.main()
