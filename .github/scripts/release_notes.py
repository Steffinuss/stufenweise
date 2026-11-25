"""Text für ein GitHub-Release aus CHANGELOG.md.

Aufruf: python3 .github/scripts/release_notes.py <neue Version> [<letzte veröffentlichte Version>]
Gibt alle Abschnitte aus CHANGELOG.md aus, die neuer als die letzte veröffentlichte Version sind
und höchstens die neue Version haben. So stehen übersprungene Versionen mit im Release.
"""
import re, sys
from pathlib import Path


def ver(s):
    return tuple(int(x) for x in s.split('.'))


def sections(text):
    """Liste von (Version, Abschnittstext) in der Reihenfolge der Datei."""
    out, cur, buf = [], None, []
    for line in text.splitlines():
        if line.startswith('## '):
            if cur:
                out.append((cur, '\n'.join(buf).strip()))
            m = re.match(r'## (\d+\.\d+\.\d+)', line)
            cur, buf = (m.group(1) if m else None), [line]
        elif cur:
            buf.append(line)
    if cur:
        out.append((cur, '\n'.join(buf).strip()))
    return out


def notes(new, last=None, path='CHANGELOG.md'):
    text = Path(path).read_text(encoding='utf-8')
    picked = [body for v, body in sections(text)
              if ver(v) <= ver(new) and (last is None or ver(v) > ver(last))]
    if not picked:
        picked = [f'## {new}\n\nSiehe CHANGELOG.md.']
    return '\n\n'.join(picked) + '\n'


if __name__ == '__main__':
    new = sys.argv[1].lstrip('v')
    last = sys.argv[2].lstrip('v') if len(sys.argv) > 2 and sys.argv[2] else None
    sys.stdout.write(notes(new, last))
