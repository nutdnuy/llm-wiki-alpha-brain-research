import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from support import REPO, SKILL

spec = importlib.util.spec_from_file_location('export_skill', REPO / 'scripts/export_skill.py')
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)

class DistributionTests(unittest.TestCase):
    def test_allowlist_and_drift_detection(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp).resolve() / 'package'
            exporter.export(SKILL, out)
            exporter.export(SKILL, out, check=True)
            paths = {p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()}
            self.assertEqual(paths, set(exporter.FILES) | {'distribution.json'})
            (out / 'SKILL.md').write_text('changed')
            with self.assertRaisesRegex(ValueError, 'distribution drift'):
                exporter.export(SKILL, out, check=True)

    def test_checked_in_hashes_match(self):
        manifest = json.loads((SKILL / 'distribution.json').read_text())
        self.assertEqual(set(manifest), set(exporter.FILES))
        for name, expected in manifest.items():
            actual = exporter.hashlib.sha256((SKILL / name).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, name)

    def test_unexpected_file_and_check_do_not_write(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp).resolve() / 'package'
            exporter.export(SKILL, out)
            original = (out / 'SKILL.md').read_bytes()
            (out / 'extra.txt').write_text('unexpected')
            for check in (True, False):
                with self.assertRaisesRegex(ValueError, 'unexpected'):
                    exporter.export(SKILL, out, check=check)
            self.assertEqual((out / 'SKILL.md').read_bytes(), original)
            (out / 'extra.txt').unlink()
            (out / 'SKILL.md').write_text('drift')
            with self.assertRaisesRegex(ValueError, 'distribution drift'):
                exporter.export(SKILL, out, check=True)
            self.assertEqual((out / 'SKILL.md').read_text(), 'drift')

    def test_source_symlink_and_private_content_preflight(self):
        with tempfile.TemporaryDirectory() as temp:
            source, out = Path(temp).resolve() / 'source', Path(temp).resolve() / 'package'
            shutil.copytree(SKILL, source)
            # Last allowlisted file fails: earlier files must not be written.
            last = source / exporter.FILES[-1]
            original = last.read_bytes()
            for marker in ('/Users/private', '/home/private', 'BEGIN PRIVATE KEY',
                           '-----BEGIN OPENSSH PRIVATE KEY-----',
                           '-----BEGIN RSA PRIVATE KEY-----',
                           '-----BEGIN EC PRIVATE KEY-----',
                           '-----BEGIN DSA PRIVATE KEY-----',
                           '-----BEGIN ENCRYPTED PRIVATE KEY-----'):
                last.write_text(marker)
                with self.assertRaisesRegex(ValueError, 'nonportable/private'):
                    exporter.export(source, out)
                self.assertFalse(out.exists())
            last.write_bytes(original)
            last.unlink()
            last.symlink_to(SKILL / exporter.FILES[-1])
            with self.assertRaisesRegex(ValueError, 'symlink'):
                exporter.export(source, out)
            self.assertFalse(out.exists())

    def test_destination_symlinks_preflight(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            victim = root / 'victim'
            victim.mkdir()
            for name in ('SKILL.md', 'unexpected', 'scripts'):
                out = root / 'package'
                out.mkdir()
                (out / name).symlink_to(victim / 'missing')
                for check in (False, True):
                    with self.assertRaisesRegex(ValueError, 'symlink'):
                        exporter.export(SKILL, out, check=check)
                self.assertFalse((victim / 'missing').exists())
                self.assertEqual(list(out.iterdir()), [out / name])
                (out / name).unlink()
                out.rmdir()
            linked = root / 'linked'
            linked.symlink_to(victim, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'symlink'):
                exporter.export(SKILL, linked / 'package')
            self.assertFalse((victim / 'package').exists())

    def test_only_generated_python_cache_is_tolerated(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp).resolve() / 'package'
            exporter.export(SKILL, out)
            cache = out / 'scripts/__pycache__'
            cache.mkdir()
            (cache / 'model.cpython-311.pyc').write_bytes(b'cache')
            exporter.export(SKILL, out, check=True)
            for name in ('secret.txt', 'secret.pyc', 'unknown.cpython-311.pyc'):
                (cache / name).write_text('not a generated cache')
                with self.assertRaisesRegex(ValueError, 'unexpected'):
                    exporter.export(SKILL, out, check=True)
                (cache / name).unlink()
