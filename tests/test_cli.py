import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from support import SKILL, fixture

class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SKILL / 'scripts/brain_wiki.py'), *args],
                              capture_output=True, text=True)

    def test_offline_workflow_and_failure_exit(self):
        with tempfile.TemporaryDirectory() as temp:
            wiki = Path(temp) / 'wiki'
            result = self.run_cli('init', '--wiki', str(wiki))
            self.assertEqual(result.returncode, 0, result.stderr)
            fixture(wiki)
            result = self.run_cli('lint', '--wiki', str(wiki))
            self.assertEqual(result.returncode, 0, result.stderr)
            result = self.run_cli('index', '--wiki', str(wiki))
            self.assertEqual(result.returncode, 0, result.stderr)
            index = (wiki / '05-Index/Research.md').read_text()
            self.assertIn('02-Wiki/Experiments/exp-demo', index)
            (wiki / '02-Wiki/Sources/src-demo.md').unlink()
            result = self.run_cli('lint', '--wiki', str(wiki))
            self.assertEqual(result.returncode, 1)
            self.assertIn('unresolved reference', result.stderr)

    def test_capture_and_handoff_output(self):
        import json
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp).resolve()
            wiki = base / 'wiki'
            self.assertEqual(self.run_cli('init', '--wiki', str(wiki)).returncode, 0)
            source = base / 'source.txt'
            source.write_text('preserve original bytes')
            result = self.run_cli('capture', '--wiki', str(wiki), '--file', str(source))
            self.assertEqual(result.returncode, 0, result.stderr)
            captured = json.loads(result.stdout)
            self.assertEqual((wiki / captured['path']).read_bytes(), source.read_bytes())
            result = self.run_cli('capture', '--wiki', str(wiki), '--file', str(base / 'missing'))
            self.assertEqual(result.returncode, 1)
            self.assertNotIn('Traceback', result.stderr)
            fixture(wiki)
            result = self.run_cli('handoff', '--wiki', str(wiki), '--output', str(base / 'queue'))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('0 candidates exported; manual-only', result.stdout)
            self.assertTrue((base / 'queue/02_candidates.csv').is_file())
            result = self.run_cli('handoff', '--wiki', str(wiki), '--output', str(base / 'queue'))
            self.assertEqual(result.returncode, 1)
            self.assertNotIn('Traceback', result.stderr)

    def test_index_lint_gate_preserves_existing_navigation(self):
        with tempfile.TemporaryDirectory() as temp:
            wiki = Path(temp) / 'wiki'
            result = self.run_cli('init', '--wiki', str(wiki))
            self.assertEqual(result.returncode, 0, result.stderr)
            fixture(wiki)
            before = {p.relative_to(wiki): p.read_bytes() for p in wiki.rglob('*') if p.is_file()}
            result = self.run_cli('index', '--wiki', str(wiki))
            self.assertEqual(result.returncode, 0, result.stderr)
            after = {p.relative_to(wiki): p.read_bytes() for p in wiki.rglob('*') if p.is_file()}
            self.assertEqual({k: v for k, v in before.items() if str(k) != '05-Index/Research.md'},
                             {k: v for k, v in after.items() if str(k) != '05-Index/Research.md'})
            index = wiki / '05-Index/Research.md'
            for kind, identity in [('Sources', 'src'), ('Hypotheses', 'hyp'), ('Candidates', 'cand'), ('Experiments', 'exp'), ('Syntheses', 'syn')]:
                self.assertIn('[[02-Wiki/' + kind + '/' + identity + '-demo|', index.read_text())
            old_index = index.read_bytes()
            (wiki / '02-Wiki/Sources/src-demo.md').unlink()
            result = self.run_cli('index', '--wiki', str(wiki))
            self.assertEqual(result.returncode, 1)
            self.assertEqual(index.read_bytes(), old_index)

    def test_index_refuses_symlink_destination(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp).resolve()
            wiki = base / 'wiki'
            result = self.run_cli('init', '--wiki', str(wiki))
            self.assertEqual(result.returncode, 0, result.stderr)
            fixture(wiki)
            outside = base / 'outside.md'
            outside.write_text('keep')
            index = wiki / '05-Index/Research.md'
            index.unlink(missing_ok=True)
            index.symlink_to(outside)
            result = self.run_cli('index', '--wiki', str(wiki))
            self.assertEqual(result.returncode, 1)
            self.assertEqual(outside.read_text(), 'keep')
