import argparse
import hashlib
import json
import re
from pathlib import Path

FILES = (
    'SKILL.md', 'agents/openai.yaml', 'requirements.txt',
    'scripts/model.py', 'scripts/validate.py', 'scripts/storage.py',
    'scripts/handoff.py', 'scripts/brain_wiki.py', 'scripts/backends.py',
    'references/workflows.md', 'references/brain-handoff.md',
    'references/data-contract.md', 'references/backends.md',
    'references/research-playbook.md', 'references/review-and-delta.md',
    'references/upstream-design.md', 'references/usage.md',
    'assets/starter/AGENTS.md', 'assets/starter/05-Index/Home.md',
    'assets/starter/05-Index/Research.md', 'assets/starter/03-Logs/Log.md',
    'assets/starter/04-Schema/Contract.md',
    'assets/starter/04-Schema/Templates/Source.md',
    'assets/starter/04-Schema/Templates/Hypothesis.md',
    'assets/starter/04-Schema/Templates/Candidate-brain.md',
    'assets/starter/04-Schema/Templates/Candidate-python.md',
    'assets/starter/04-Schema/Templates/Experiment-brain.md',
    'assets/starter/04-Schema/Templates/Experiment-python.md',
    'assets/starter/04-Schema/Templates/Synthesis.md',
    'tests/test_backends.py',
)

def reject_symlinks(path):
    # Include ancestors: a safe leaf must not traverse a redirected parent.
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError('symlink refused: ' + str(part))


def export(source, destination, check=False):
    source, destination = Path(source).absolute(), Path(destination).absolute()
    reject_symlinks(source)
    reject_symlinks(destination)
    payload = {}
    for name in FILES:
        path = source / name
        reject_symlinks(path)
        path.resolve().relative_to(source.resolve())
        raw = path.read_bytes()
        text = raw.decode('utf-8')
        if (any(marker in text for marker in ('/Users/', '/home/'))
                or re.search(r'BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY', text)):
            raise ValueError('nonportable/private material in ' + name)
        payload[name] = raw
    manifest = {name: hashlib.sha256(raw).hexdigest() for name, raw in payload.items()}
    payload['distribution.json'] = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
    # Inspect every entry before writing, including unexpected dangling links.
    if destination.exists():
        for path in destination.rglob('*'):
            reject_symlinks(path)
            name = path.relative_to(destination).as_posix()
            if path.is_dir():
                continue
            match = re.fullmatch(r'([a-z_]+)\.cpython-[0-9]+(?:\.opt-[0-9]+)?\.pyc', path.name)
            cache = (path.parent.name == '__pycache__' and match is not None
                     and (path.parent.parent / (match[1] + '.py'))
                         .relative_to(destination).as_posix() in FILES)
            if name not in payload and not cache:
                raise ValueError('unexpected distribution files: ' + name)
    for name in payload:
        target = destination / name
        reject_symlinks(target)
        if target.exists() and not target.is_file():
            raise ValueError('distribution target is not a file: ' + name)
        for parent in target.parents:
            if parent.exists() and not parent.is_dir():
                raise ValueError('distribution parent is not a directory: ' + name)
    if check:
        for name, raw in payload.items():
            target = destination / name
            if not target.is_file() or target.read_bytes() != raw:
                raise ValueError('distribution drift: ' + name)
    else:
        for name, raw in payload.items():
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
    return len(FILES)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--destination', required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(export(args.source, args.destination, args.check))
