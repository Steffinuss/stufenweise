"""Rückmeldungen zu Arbeitsblättern (Backlog S, Stefan 26.11.2026):
- S3 Schwarz-Weiß: Material (Hunderterplatten, Zehnerstangen, Einer) hellgrau mit Umriss und Kästchen, Plättchen bleiben schwarz.
- S4 Schwarz-Weiß: Pfeil am Zahlenstrahl schwarz (kein Punktmuster mehr).
- S5/S6 Unterschiede bestimmen und Ergänzen ab 1000: eine Aufgabe je Zeile mit Kästchen zum Rechnen; Umbruch nur zwischen Sätzen.
- S7 Zehnerfeld als eine Reihe mit 10: Üben/Test, Tafel und Rechenhilfe, Arbeitsblatt, Legeblatt (quer)."""
import asyncio, re
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

BUILD = """([t, zr, opt]) => { Object.assign(app.sheet, {...SHEET_BASE, pid:'none', topic:t, zr, n:6, sol:false, ...opt}); return buildSheet().html; }"""

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 900})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)

        # S3: Material in Schwarz-Weiß hellgrau, Plättchen schwarz
        h = await pg.evaluate(BUILD, ['M:plus', 1000, {'bw': True, 'mat': True}])
        body = h.split('<body>', 1)[1]
        check('S3 Material hellgrau', 'fill="#dedede"' in body and 'url(#sw-rot)' not in body, str(body.count('#dedede')))
        h = await pg.evaluate(BUILD, ['M:plus', 20, {'bw': True, 'mat': True}])
        body = h.split('<body>', 1)[1]
        check('S3 Plättchen bleiben schwarz bzw. schraffiert', 'fill="#222"' in body and '#dedede' not in body)
        # S4: Pfeil am Zahlenstrahl schwarz
        h = await pg.evaluate(BUILD, ['M:zahlenstrahl', 1000, {'bw': True}])
        body = h.split('<body>', 1)[1]
        check('S4 Pfeil schwarz', 'url(#sw-rot)' not in body and not re.search(r'#c9414a', body, re.I), '')

        # S5/S6: ab 1000 einspaltig mit Kästchen, darunter ohne
        for t in ('M:ergaenzen', 'M:unterschied'):
            for zr, want in ((1000, True), (100, False)):
                h = await pg.evaluate(BUILD, [t, zr, {}])
                n = h.count('class="ab-task"'); k = h.count('class="ab-karo"')
                cols = re.search(r'grid-template-columns:repeat\((\d+)', h.split('<body>', 1)[1]).group(1)
                ok = (k == n and cols == '1') if want else (k == 0 and cols == '2')
                check(f'S5/S6 {t} bis {zr}: {"Kästchen, einspaltig" if want else "ohne Kästchen, zweispaltig"}', ok, f'{n} Aufgaben, {k} Kästchen, {cols} Spalten')
        h = await pg.evaluate(BUILD, ['M:ergaenzen', 1000, {}])
        doc = await br.new_page(viewport={'width': 820, 'height': 1160}); await doc.set_content(h); await doc.wait_for_timeout(150)
        r = await doc.evaluate("""(() => { const s = [...document.querySelectorAll('.ab-ins .ab-s')]; if(!s.length) return null;
          const lines = s.map(x => x.getClientRects().length); return {n: s.length, broken: lines.filter(l => l > 1).length}; })()""")
        await doc.close()
        check('S6 Sätze brechen nicht mitten im Satz um', r and r['n'] >= 3 and r['broken'] == 0, str(r))

        # S7: Zehnerfeld eine Reihe mit 10
        r = await pg.evaluate("""() => {
          const vb = s => s.match(/viewBox="([^"]+)"/)[1].split(' ').map(Number), cx = s => new Set([...s.matchAll(/<circle cx="([\\d.]+)"/g)].map(m => m[1])).size, cy = s => new Set([...s.matchAll(/<circle cx="[\\d.]+" cy="([\\d.]+)"/g)].map(m => m[1])).size;
          const f = fieldSvg(10, 10), a = abField(10, 0, '+', 10), q = drawQty(10, 10), t = tfSvg({cap:10, dots:Array(10).fill('b'), cross:0});
          const f20 = fieldSvg(20, 20), a20 = abField(20, 0, '+', 20);
          return {f:[cx(f), cy(f)], a:[cx(a), cy(a)], q:[cx(q), cy(q)], t:[cx(t), cy(t)], f20:[cx(f20), cy(f20)], a20:[cx(a20), cy(a20)], fw: vb(f)[2] > 3*vb(f)[3]}; }""")
        check('S7 Zehnerfeld 1 × 10 (Üben/Test, Arbeitsblatt, Blitzblick, Tafel)', all(r[k] == [10, 1] for k in 'faqt') and r['fw'], str(r))
        check('S7 Zwanzigerfeld bleibt 2 × 10', r['f20'] == [10, 2] and r['a20'] == [10, 2], str(r))
        h = await pg.evaluate("() => { Object.assign(app.sheet, {...SHEET_BASE, pid:'none', topic:'K:zehner', kt:'plus'}); return buildSheet().html; }")
        doc = await br.new_page(); await doc.set_content(h); await doc.wait_for_timeout(150)
        r = await doc.evaluate("""(() => { const s = document.querySelector('.lg-svg'), quer = !!document.querySelector('.page.lg.quer');
          const pages = [...document.querySelectorAll('.page')].filter(p => !p.classList.contains('sol')), over = pages.filter(p => p.scrollHeight > p.clientHeight + 2).length;
          return {w: s && s.getAttribute('width'), h: s && s.getAttribute('height'), n: document.querySelectorAll('.lg-svg').length, quer, over}; })()""")
        await doc.close()
        check('S7 Legeblatt Zehnerfeld: eine Reihe mit 10, quer, passt', r['w'] == '250mm' and r['h'] == '25mm' and r['quer'] and not r['over'], str(r))
        # S2: Heftseite mit großen Aufgaben darf im fertigen Heft ein wenig (bis 90 %) verkleinert werden, statt überzulaufen
        res = []
        for hmm in (300, 360):
            h = await pg.evaluate("""(hmm) => `<!DOCTYPE html><html><head><style>${HEFT_CSS}</style>${PAGE_FIT_JS}</head><body><div class="page"><div class="ab-grid gross"><div style="height:${hmm}mm"></div></div></div></body></html>`""", hmm)
            doc = await br.new_page(); await doc.set_content(h); await doc.wait_for_timeout(400)
            res.append(await doc.evaluate("(() => { const p = document.querySelector('.page'); return [p.dataset.fit || '', p.dataset.over || '']; })()")); await doc.close()
        check('S2 große Aufgaben: knapp zu lang → leicht verkleinert, viel zu lang → zweites Blatt', res[0][1] == '' and res[0][0] and float(res[0][0]) >= .9 and res[1][1] != '', str(res))
        await br.close()
    print('FEHLER:', ERR) if ERR else print('alles ok')
    if ERR: raise SystemExit(1)

asyncio.run(main())
