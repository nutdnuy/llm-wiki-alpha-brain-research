import json
import os
import shutil
import tempfile
from pathlib import Path
from model import FOLDERS, digest, within

def initialize(root):
    root = Path(root).absolute()
    if root.exists() or root.is_symlink():
        raise ValueError('destination already exists; choose a new wiki directory')
    if not root.parent.is_dir() or root.parent.is_symlink():
        raise ValueError('parent must be an existing real directory')
    starter = Path(__file__).resolve().parents[1] / 'assets' / 'starter'
    staging = Path(tempfile.mkdtemp(prefix='.brain-wiki-', dir=root.parent))
    try:
        shutil.copytree(starter, staging, dirs_exist_ok=True)
        for name in FOLDERS.values():
            (staging / '02-Wiki' / name).mkdir(parents=True, exist_ok=True)
        (staging / '01-Raw').mkdir(exist_ok=True)
        (staging / '.brain-wiki.json').write_text(
            json.dumps({'schema_version': 1}, indent=2) + '\n', encoding='utf-8')
        if root.exists() or root.is_symlink():
            raise ValueError('destination appeared during initialization')
        os.rename(staging, root)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return root

def capture(root, source):
    root = Path(root).resolve()
    marker = within(root, '.brain-wiki.json')
    try:
        metadata = json.loads(marker.read_text(encoding='utf-8'))
    except (OSError, ValueError, UnicodeError):
        raise ValueError('not a Brain Wiki: invalid marker') from None
    if (not isinstance(metadata, dict)
            or type(metadata.get('schema_version')) is not int
            or metadata['schema_version'] != 1):
        raise ValueError('not a Brain Wiki: unsupported schema version')
    for relative in ['01-Raw', '02-Wiki',
                     *('02-Wiki/' + name for name in FOLDERS.values())]:
        if not within(root, relative).is_dir():
            raise ValueError('not a Brain Wiki: missing directory ' + relative)
    data = Path(source).read_bytes()
    if not data:
        raise ValueError('empty source; obtain readable evidence before capture')
    sha = digest(data)
    relative = '01-Raw/' + sha + '.bin'
    destination = within(root, relative)
    try:
        with destination.open('xb') as handle:
            handle.write(data)
    except FileExistsError:
        if destination.read_bytes() != data:
            raise ValueError('existing raw content does not match its hash') from None
    return {'path': relative, 'sha256': sha, 'bytes': len(data)}
