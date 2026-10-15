import tempfile
import unittest
from pathlib import Path
from support import SKILL
from storage import capture, initialize

class StorageTests(unittest.TestCase):
    def test_init_and_refuse_existing_destination(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'wiki'
            initialize(root)
            marker = (root / '.brain-wiki.json').read_bytes()
            with self.assertRaises(ValueError):
                initialize(root)
            self.assertEqual((root / '.brain-wiki.json').read_bytes(), marker)
            self.assertTrue((root / '05-Index/Home.md').is_file())

    def test_idempotent_capture_and_new_version(self):
        with tempfile.TemporaryDirectory() as temp:
            root = initialize(Path(temp) / 'wiki')
            source = Path(temp) / 'source.txt'
            source.write_text('one')
            first = capture(root, source)
            self.assertEqual(first, capture(root, source))
            source.write_text('two')
            second = capture(root, source)
            self.assertNotEqual(first['sha256'], second['sha256'])
            self.assertEqual((root / first['path']).read_text(), 'one')
            self.assertEqual(len(list((root / '01-Raw').iterdir())), 2)

    def test_empty_capture_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = initialize(Path(temp) / 'wiki')
            source = Path(temp) / 'empty'
            source.touch()
            with self.assertRaisesRegex(ValueError, 'empty source'):
                capture(root, source)

    def test_malformed_marker_rejected_without_writes(self):
        for marker in ('no json', '[]', '{}', '{"schema_version": true}',
                       '{"schema_version": 2}', '{"schema_version": 1.0}'):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as temp:
                root = initialize(Path(temp) / 'wiki')
                (root / '.brain-wiki.json').write_text(marker)
                source = Path(temp) / 'source'
                source.write_bytes(b'evidence')
                with self.assertRaises(ValueError):
                    capture(root, source)
                self.assertEqual(list((root / '01-Raw').iterdir()), [])

    def test_missing_research_folder_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = initialize(Path(temp) / 'wiki')
            (root / '02-Wiki/Sources').rmdir()
            source = Path(temp) / 'source'
            source.write_bytes(b'evidence')
            with self.assertRaises(ValueError):
                capture(root, source)

    def test_tampered_raw_object_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = initialize(Path(temp) / 'wiki')
            source = Path(temp) / 'source'
            source.write_bytes(b'evidence')
            artifact = capture(root, source)
            (root / artifact['path']).write_bytes(b'tampered')
            with self.assertRaisesRegex(ValueError, 'does not match'):
                capture(root, source)
            self.assertEqual((root / artifact['path']).read_bytes(), b'tampered')

    def test_symlink_raw_root_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = initialize(Path(temp) / 'wiki')
            outside = Path(temp) / 'outside'
            outside.mkdir()
            (root / '01-Raw').rmdir()
            (root / '01-Raw').symlink_to(outside, target_is_directory=True)
            source = Path(temp) / 'source'
            source.write_bytes(b'evidence')
            with self.assertRaises(ValueError):
                capture(root, source)
            self.assertEqual(list(outside.iterdir()), [])

    def test_existing_file_and_dangling_symlink_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'wiki'
            root.write_bytes(b'owner data')
            with self.assertRaises(ValueError):
                initialize(root)
            self.assertEqual(root.read_bytes(), b'owner data')
            link = Path(temp) / 'link'
            link.symlink_to(Path(temp) / 'missing')
            with self.assertRaises(ValueError):
                initialize(link)
            self.assertTrue(link.is_symlink())

    def test_failure_cleans_staging(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as temp:
            with patch('storage.shutil.copytree', side_effect=OSError('copy failed')):
                with self.assertRaises(OSError):
                    initialize(Path(temp) / 'wiki')
            self.assertEqual(list(Path(temp).iterdir()), [])
