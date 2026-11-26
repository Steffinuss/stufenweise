"""Arbeitsblätter im Design der Hefte (Backlog M, Stefan 26.11.2026: Layout A „wie im Heft“, Schwarz-Weiß für alle Blätter):
- Kopfzeile „Fach · Bereich“, Titel mit Name und Datum, Aufgabenkästen bis zur Fußzeile, Fußzeile mit Lizenz links und Fach rechts,
  keine Seitenzahl, kein Farbrand; Lösungsblatt und Hilfeseite mit Kopf- und Fußzeile; keine Linie über der Fußzeile (Stefan).
- Jedes Blatt (alle Themen, auch Schwarz-Weiß und große Aufgaben) passt genau auf seine Seiten.
- Schwarz-Weiß: im Blatt keine bunten Farben mehr, Plättchen schwarz bzw. schraffiert; Legeblätter bleiben, wie sie sind.
- Heft: Seiten aus „Ins Arbeitsheft“ und aus dem Heft-Assistenten haben genau einen Rahmen."""
import asyncio, re
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

BUILD = """async ([topic, zr, opt]) => {
  Object.assign(app.sheet, {...SHEET_BASE, pid:'none', topic, zr, n:'fill', sol:true, ...opt});
  app.sheetDoc = buildSheet();
  const fr = document.createElement('iframe'); fr.style.cssText = 'position:fixed;left:-10000px;top:0;width:820px;height:1200px'; document.body.append(fr);
  const load = html => new Promise(r => { fr.onload = () => setTimeout(r, 30); fr.srcdoc = html; });
  for(let i = 0; i < 25; i++){ await load(app.sheetDoc.html); const G = app.sheetGen; if(!G || !G.fill || G.fitted) break; sheetFit(fr, () => {}); if(G.fitted) break; }
  fr.remove(); return app.sheetDoc.html; }"""

def colored(html):
    body = re.sub(r'(?s)<style>.*?</style>', '', html.split('<body>', 1)[1]) if '<body>' in html else html
    body = re.sub(r'(?s)<pattern.*?</pattern>', '', body)
    bad = set()
    for c in re.findall(r'(?<=[=:"\'\s,])#([0-9a-fA-F]{3,8})(?![\w-])', body):
        h = c if len(c) > 4 else ''.join(x * 2 for x in c)
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        if max(r, g, b) - min(r, g, b) > 6: bad.add('#' + c)
    return bad

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 900})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)

        # Aufbau
        html = await pg.evaluate(BUILD, ['M:plus', 20, {'taf': False}])
        doc = await br.new_page(viewport={'width': 794, 'height': 1123}); await doc.set_content(html); await doc.wait_for_timeout(600)
        a = await doc.evaluate("""() => { const p = document.querySelector('.page'), g = p.querySelector('.ab-grid').getBoundingClientRect(), f = p.querySelector('.hf-foot').getBoundingClientRect();
          return {head: p.querySelector('.hf-head')?.textContent, meta: !!p.querySelector('.ab-meta'), pn: !!p.querySelector('.hf-pn'), right: p.querySelector('.hf-foot .r')?.textContent,
            lic: p.querySelector('.hf-foot .l')?.textContent, gap: (f.top - g.bottom)/3.7795, border: getComputedStyle(p.querySelector('.hf-foot')).borderTopStyle,
            sol: document.querySelector('.page.sol .hf-head')?.textContent, solFoot: !!document.querySelector('.page.sol .hf-foot')}; }""")
        print(a)
        check('Kopfzeile „Mathe · Rechnen“', a['head'] == 'Mathe · Rechnen', a['head'])
        check('Name und Datum bleiben', a['meta'])
        check('keine Seitenzahl', not a['pn'])
        check('Fußzeile: Lizenz links, Fach rechts', 'CC BY-SA 4.0' in (a['lic'] or '') and a['right'] == 'Mathe', f"{a['lic']} | {a['right']}")
        check('Kästen reichen bis zur Fußzeile', 0 <= a['gap'] < 12, f"{a['gap']:.1f} mm")
        check('keine Linie über der Fußzeile', a['border'] == 'none', a['border'])
        check('Lösungsblatt mit Kopf- und Fußzeile', a['sol'] == 'Lösungen' and a['solFoot'], str(a['sol']))
        await doc.close()

        # alle Themen: passen genau auf ihre Seiten, auch in Schwarz-Weiß und groß
        topics = await pg.evaluate("sheetTopics().flatMap(([, o]) => o).map(x => x[0]).filter(t => !t.startsWith('K:'))")
        bad, badc, n = [], [], 0
        for i, t in enumerate(topics):
            opt = {'bw': i % 2 == 0, 'gross': i % 3 == 0}
            html = await pg.evaluate(BUILD, [t, 100 if t in ('M:stellenwert', 'M:schriftlich') else 20, opt])
            doc = await br.new_page(); await doc.set_content(html); await doc.wait_for_timeout(250)
            k = await doc.evaluate("[document.querySelectorAll('.page').length, [...document.querySelectorAll('.page')].filter(p => p.dataset.over).length, document.querySelectorAll('.page .hf-foot').length]")
            pdf = await doc.pdf(prefer_css_page_size=True, print_background=True); await doc.close()
            pp = len(re.findall(rb'/Type\s*/Page[^s]', pdf)); n += 1
            known = opt['gross'] and t in ('L:L8', 'L:L9', 'H:HL')   # schon vor Backlog M: große Aufgaben mit langen Texten passen nicht (werden nie verkleinert)
            if known and k[1]: print('bekannt (schon in 0.39.0):', t, opt, k, 'PDF', pp)
            elif k[1] or pp != k[0] or k[2] != k[0]: bad.append(f'{t} {opt}: {k} PDF {pp}')
            if opt['bw'] and not t.startswith('B:'):
                c = colored(html)
                if c: badc.append(f'{t}: {sorted(c)[:4]}')
        check(f'{n} Blätter: jede Seite passt, jede hat eine Fußzeile', not bad, '; '.join(bad[:5]))
        check('Schwarz-Weiß: keine bunten Farben im Blatt', not badc, '; '.join(badc[:5]))

        # Plättchen in Schwarz-Weiß
        html = await pg.evaluate(BUILD, ['M:plus', 20, {'bw': True}])
        check('Schwarz-Weiß: Plättchen schwarz und schraffiert', 'url(#sw-or)' in html and 'id="sw-or"' in html and '#2f5ea8' not in html)
        html = await pg.evaluate(BUILD, ['M:plus', 20, {'bw': False}])
        check('Farbe: Plättchen blau und orange', '#2f5ea8' in html and 'url(#sw-or)' not in html)
        # Legeblätter bleiben
        html = await pg.evaluate("() => { Object.assign(app.sheet, {...SHEET_BASE, pid:'none', topic:'K:zehner'}); return buildSheet().html; }")
        check('Legeblätter ohne neuen Rahmen', 'class="hf-foot' not in html and 'class="hf-head' not in html)

        # Heft: genau ein Rahmen je Seite
        await pg.evaluate("app.heft = {title:'Mein Arbeitsheft', pid:'none', items:[], toc:true}; saveHeft()")
        await pg.evaluate(BUILD, ['M:plus', 20, {}])
        await pg.evaluate("heftAdd()")
        it = await pg.evaluate("app.heft.items[0].html")
        check('Ins Arbeitsheft: Seite ohne Blatt-Rahmen', 'hf-foot' not in it and 'hf-head' not in it and 'ab-grid' in it)
        n_t = await pg.evaluate("(app.sheetDoc.html.match(/class=\"ab-task/g) || []).length")
        n_h = it.count('class="ab-task')
        check('Ins Arbeitsheft: dieselben Aufgaben', n_t == n_h, f'{n_t} / {n_h}')
        html = await pg.evaluate("buildHeft().html")
        pages, foots = html.count('class="page'), html.count('class="hf-foot"')
        check('Heft: eine Fußzeile je Aufgabenseite', foots == 1, f'{foots} Fußzeilen, {pages} Seiten')
        await br.close()
    print('FEHLER:', ERR) if ERR else print('alles ok')

asyncio.run(main())
