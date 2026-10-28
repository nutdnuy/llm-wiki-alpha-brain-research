"""Render this repository's editable Excalidraw scenes as lightweight SVG previews.

This renderer supports the shapes used here; it is not the official Excalidraw
exporter. The .excalidraw scenes remain the diagram source of truth.
"""
import base64
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'docs/assets'


def render(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    canvas = data['customData']['canvas']
    width, height = canvas['width'], canvas['height']
    css = []
    for weight in (400, 500):
        raw = (ASSETS / f'fonts/roboto-latin-{weight}-normal.woff2').read_bytes()
        url = 'data:font/woff2;base64,' + base64.b64encode(raw).decode()
        css.append(f"@font-face{{font-family:Roboto;font-weight:{weight};src:url('{url}') format('woff2')}}")
    esc = html.escape
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
             f'<title id="title">{esc(path.stem.replace("-", " "))}</title>',
             '<desc id="desc">Alpha Research Wiki workflow. Editable Excalidraw source is provided alongside this preview.</desc>',
             '<defs><style>' + ''.join(css) + '</style></defs>',
             f'<rect width="{width}" height="{height}" fill="{data["appState"]["viewBackgroundColor"]}"/>']
    for e in data['elements']:
        if e.get('isDeleted'):
            continue
        x, y, w, h = (e[k] for k in ('x', 'y', 'width', 'height'))
        color = e['strokeColor']
        if e['type'] == 'rectangle':
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
                         f'fill="{e["backgroundColor"]}" stroke="{color}" stroke-width="{e["strokeWidth"]}"/>')
        elif e['type'] == 'text':
            align = e.get('textAlign', 'left')
            anchor = {'left': 'start', 'center': 'middle', 'right': 'end'}[align]
            tx = x + (w/2 if align == 'center' else w if align == 'right' else 0)
            size = e['fontSize']
            weight = e.get('customData', {}).get('previewWeight', 400)
            lines = e['text'].splitlines()
            content = ''.join(f'<tspan x="{tx}" dy="{0 if i == 0 else size*1.25}">{esc(line)}</tspan>'
                              for i, line in enumerate(lines))
            parts.append(f'<text x="{tx}" y="{y+size}" fill="{color}" font-family="Roboto,Arial,sans-serif" '
                         f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{content}</text>')
        elif e['type'] in ('arrow', 'line'):
            points = [(x+p[0], y+p[1]) for p in e['points']]
            coords = ' '.join(f'{px},{py}' for px, py in points)
            dash = ' stroke-dasharray="8 7"' if e.get('strokeStyle') == 'dashed' else ''
            parts.append(f'<polyline points="{coords}" fill="none" stroke="{color}" '
                         f'stroke-width="{e["strokeWidth"]}" stroke-linecap="round" stroke-linejoin="round"{dash}/>')
            if e.get('endArrowhead'):
                import math
                (a,b),(c,d) = points[-2:]
                angle = math.atan2(d-b,c-a)
                length, spread = 11, 0.55
                wings = [(c-length*math.cos(angle+s),d-length*math.sin(angle+s)) for s in (-spread,spread)]
                parts.append(f'<polyline points="{wings[0][0]},{wings[0][1]} {c},{d} '
                             f'{wings[1][0]},{wings[1][1]}" fill="none" stroke="{color}" '
                             f'stroke-width="{e["strokeWidth"]}" stroke-linecap="round" stroke-linejoin="round"/>')
        elif e['type'] == 'image':
            image = data['files'][e['fileId']]['dataURL']
            parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{esc(image)}" preserveAspectRatio="xMidYMid meet"/>')
        else:
            raise ValueError('Unsupported scene element: ' + e['type'])
    parts.append('</svg>')
    out = ASSETS / (path.stem + '.svg')
    out.write_text('\n'.join(parts)+'\n', encoding='utf-8')
    print(out.relative_to(ROOT))


if __name__ == '__main__':
    for path in sorted(Path(__file__).parent.glob('flow-*.excalidraw')):
        render(path)
