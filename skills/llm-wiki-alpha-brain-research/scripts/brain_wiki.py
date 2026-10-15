import argparse
import json
import sys
from pathlib import Path
from handoff import export_handoff
from model import read_note, within
from storage import capture, initialize
from validate import lint

def rebuild_index(root):
    errors = lint(root)
    if errors:
        raise ValueError('\n'.join(errors))
    root = Path(root).resolve()
    lines = ['# Research Index', '', 'Generated navigation; status is not evidence quality.', '']
    for path in sorted((root / '02-Wiki').rglob('*.md')):
        note, _ = read_note(path)
        target = path.relative_to(root).with_suffix('').as_posix()
        lines.append(f"- [[{target}|{note['id']}]] — {note['title']} ({note['status']})")
    path = within(root, '05-Index/Research.md')
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

def main(argv=None):
    parser = argparse.ArgumentParser(description='Offline BRAIN research memory utilities')
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init')
    init.add_argument('--wiki', required=True)
    ingest = commands.add_parser('capture')
    ingest.add_argument('--wiki', required=True)
    ingest.add_argument('--file', required=True)
    for name in ('lint', 'index'):
        command = commands.add_parser(name)
        command.add_argument('--wiki', required=True)
    handoff = commands.add_parser('handoff')
    handoff.add_argument('--wiki', required=True)
    handoff.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'init':
            print(initialize(args.wiki))
        elif args.command == 'capture':
            print(json.dumps(capture(args.wiki, args.file), sort_keys=True))
        elif args.command == 'lint':
            errors = lint(args.wiki)
            for error in errors:
                print(error, file=sys.stderr)
            print(f'{len(errors)} structural errors; evidence requires separate review')
            return bool(errors)
        elif args.command == 'index':
            rebuild_index(args.wiki)
            print('index updated')
        else:
            print(f'{export_handoff(args.wiki, args.output)} candidates exported; manual-only')
        return 0
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
