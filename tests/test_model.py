import tempfile
import unittest
from pathlib import Path
from support import fixture, write
from model import read_note, within

class ModelTests(unittest.TestCase):
    def test_valid_note_and_missing_field(self):
        with tempfile.TemporaryDirectory() as temp:
            records = fixture(temp)
            for record in records:
                with self.subTest(kind=record['type']):
                    self.assertEqual(read_note(write(temp, record))[0], record)
            path = write(temp, records[0])
            self.assertEqual(read_note(path)[0]['id'], 'src-demo')
            del records[0]['claims']
            write(temp, records[0])
            with self.assertRaisesRegex(ValueError, 'missing fields: claims'):
                read_note(path)

    def test_traversal_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                within(temp, '../outside')
            with self.assertRaises(ValueError):
                within(temp, '/tmp/outside')
            self.assertEqual(within(temp, '01-Raw/file.bin'), Path(temp).resolve() / '01-Raw/file.bin')
            (Path(temp) / 'link').symlink_to('/tmp')
            with self.assertRaises(ValueError):
                within(temp, 'link/file')
