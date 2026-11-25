"""Schlichte Formen für die Stufenfibel (Stefan, 25.11.2026).

- Großes I als einfacher Strich, ohne Querstriche oben und unten (wie in der Schule geschrieben).
  Vom kleinen l bleibt es klar verschieden, weil das l unten einen Bogen hat.
- Ziffer 1 ohne Querstrich unten (Anstrich oben bleibt).

Andika hat für das große I keine eigene Variante; die Formen werden deshalb hier umgezeichnet.
Wird von build-stufenfibel.py aufgerufen; kann auch direkt auf die fertigen WOFF-Dateien angewendet werden:
    python3 fonts/schlichte_formen.py   (ändert fonts/*.woff und bettet sie neu in index.html ein)
"""
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables import ttProgram


def _set(font, name, contours):
    glyf = font['glyf']
    pen = TTGlyphPen(None)
    for pts in contours:
        pen.moveTo(pts[0])
        for p in pts[1:]:
            pen.lineTo(p)
        pen.closePath()
    g = pen.glyph()
    g.program = ttProgram.Program(); g.program.fromBytecode(b'')  # Hinting der alten Form passt nicht mehr
    glyf[name] = g
    g.recalcBounds(glyf)
    return g


def _stem(coords):
    """Senkrechter Hauptstrich: die beiden x-Werte, die am häufigsten vorkommen (innen liegend)."""
    xs = sorted({x for x, _ in coords})
    return xs[1], xs[-2]


def schlicht(font):
    glyf, hmtx = font['glyf'], font['hmtx']
    cmap = font.getBestCmap()
    nI, n1 = cmap[ord('I')], cmap[ord('1')]

    # --- großes I: einfacher Strich, Strichstärke wie bisher, Abstände wie beim H ---
    old = glyf[nI]
    coords, _, _ = old.getCoordinates(glyf)
    if len(coords) == 4:
        return font  # schon schlicht
    l, r = _stem(list(coords))
    stem = r - l
    hb = glyf[cmap[ord('H')]]; hb.recalcBounds(glyf)
    side = hb.xMin
    top = max(y for _, y in coords)
    oldw = hmtx[nI][0]; oldc = (min(x for x, _ in coords) + max(x for x, _ in coords)) / 2
    _set(font, nI, [[(side, top), (side + stem, top), (side + stem, 0), (side, 0)]])
    neww = 2 * side + stem
    hmtx[nI] = (neww, side)
    shift = round((side + stem / 2) - oldc)
    # Í Î Ï Ì: Akzent mitschieben, Breite anpassen
    for ch in 'ÍÎÏÌ':
        n = cmap.get(ord(ch))
        if not n or not glyf[n].isComposite():
            continue
        g = glyf[n]
        for c in g.components:
            if c.glyphName != nI:
                c.x += shift
        g.recalcBounds(glyf)
        hmtx[n] = (neww, g.xMin)

    # --- Ziffer 1: ohne Querstrich unten ---
    one = glyf[n1]
    coords, ends, _ = one.getCoordinates(glyf)
    pts = list(coords)
    if min(y for _, y in pts) == 0 and any(y > 0 and y < 300 for _, y in pts):
        bar = max(y for _, y in pts if 0 < y < 300)          # Oberkante des Fußes
        l, r = _stem([p for p in pts if p[1] == bar])          # Hauptstrich (innere Punkte auf Fußhöhe)
        # Reihenfolge wie im Original: von unten links den Strich hinauf, über den Kopf, rechts hinunter
        start = (l, 0); end = (r, 0)
        seq = [p for p in pts if p[1] > bar]
        # Original beginnt je nach Schnitt an anderer Stelle: so drehen, dass es mit dem linken Strich beginnt
        i = next(k for k, p in enumerate(seq) if p[0] == l)
        seq = seq[i:] + seq[:i]
        if seq[-1][0] != r:
            seq = seq[::-1]
        _set(font, n1, [[start] + seq + [end]])
        g = glyf[n1]
        hmtx[n1] = (hmtx[n1][0], g.xMin)
    return font


if __name__ == '__main__':
    import base64, os, re
    from fontTools.ttLib import TTFont
    here = os.path.dirname(os.path.abspath(__file__))
    html = os.path.join(here, '..', 'index.html')
    s = open(html, encoding='utf-8').read()
    for style, weight in [('Regular', 400), ('Bold', 700)]:
        p = os.path.join(here, f'Stufenfibel-{style}.woff')
        f = TTFont(p); schlicht(f); f.flavor = 'woff'; f.save(p)
        b64 = base64.b64encode(open(p, 'rb').read()).decode()
        pat = re.compile(r'(font-family:"Stufenfibel";font-weight:%d[^;]*;[^}]*?src:url\(data:font/woff;base64,)[A-Za-z0-9+/=]+(\))' % weight)
        s, n = pat.subn(lambda m: m.group(1) + b64 + m.group(2), s)
        assert n == 1, (style, n)
        print(style, os.path.getsize(p))
    open(html, 'w', encoding='utf-8').write(s)
