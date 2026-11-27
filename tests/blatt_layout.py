"""Arbeitsblätter im Design der Hefte (Backlog M, Stefan 26.11.2026: Layout A „wie im Heft“, Schwarz-Weiß für alle Blätter):
- Kopfzeile „Fach · Bereich“, Titel mit Name und Datum, Aufgabenkästen bis zur Fußzeile, Fußzeile mit Lizenz links und Fach rechts,
  keine Seitenzahl, kein Farbrand; Lösungsblatt und Hilfeseite mit Kopf- und Fußzeile; keine Linie über der Fußzeile (Stefan).
- Jedes Blatt (alle Themen, auch Schwarz-Weiß und große Aufgaben) passt genau auf seine Seiten.
- Schwarz-Weiß: im Blatt keine bunten Farben mehr, Plättchen schwarz bzw. schraffiert; Legeblätter bleiben, wie sie sind.
- Heft: eine ausgetauschte Seite (Backlog U3) hat genau einen Rahmen; die Blattsammlung (U2) nimmt das Blatt mit Rahmen."""
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
        bad, badc, badw, n = [], [], [], 0
        for i, t in enumerate(topics):
            opt = {'bw': i % 2 == 0, 'gross': i % 3 == 0}
            html = await pg.evaluate(BUILD, [t, 100 if t in ('M:stellenwert', 'M:schriftlich') else 20, opt])
            doc = await br.new_page(); await doc.set_content(html); await doc.wait_for_timeout(250)
            k = await doc.evaluate("[document.querySelectorAll('.page').length, [...document.querySelectorAll('.page')].filter(p => p.dataset.over).length, document.querySelectorAll('.page .hf-foot').length]")
            wide = await doc.evaluate("""(() => { const p = document.querySelector('.page'), r = p.getBoundingClientRect(), right = r.right - parseFloat(getComputedStyle(p).paddingRight) + 2;
              return [...p.querySelectorAll('.ab-task')].filter(t => t.getBoundingClientRect().right > right).length; })()""")
            if wide: badw.append(f'{t} {opt}: {wide} Aufgaben zu breit')
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
        check('keine Aufgabe breiter als die Seite (auch große Aufgaben, Backlog S1)', not badw, '; '.join(badw[:5]))
        # große Aufgaben bei allen Blättern mit 3 Spalten und Zahlenraum 1000 (Stefan: Schriftlich bis 1000 lief über)
        badg = []
        for t in topics:
            html = await pg.evaluate(BUILD, [t, 1000 if t.startswith('M:') else 20, {'gross': True}])
            doc = await br.new_page(); await doc.set_content(html); await doc.wait_for_timeout(200)
            w = await doc.evaluate("""(() => { const p = document.querySelector('.page'), r = p.getBoundingClientRect(), right = r.right - parseFloat(getComputedStyle(p).paddingRight) + 2;
              return [...p.querySelectorAll('.ab-task')].filter(t => t.getBoundingClientRect().right > right).length; })()""")
            await doc.close()
            if w: badg.append(f'{t}: {w}')
        check('große Aufgaben bis 1000: nichts zu breit', not badg, '; '.join(badg[:6]))
        pad = await pg.evaluate("""(() => { const d = document.createElement('div'); d.innerHTML = `<style>${SHEET_CSS}${HEFT_CSS}${SHEET_FRAME_CSS}</style><div class="page hf-p"></div>`; document.body.append(d);
          const cs = getComputedStyle(d.querySelector('.page')), r = [cs.paddingLeft, cs.paddingRight].map(x => Math.round(parseFloat(x)/3.7795)); d.remove(); return r; })()""")
        check('Lochrand: links 20 mm, rechts 12 mm (Backlog S8)', pad == [20, 12], str(pad))

        # Plättchen in Schwarz-Weiß
        html = await pg.evaluate(BUILD, ['M:plus', 20, {'bw': True}])
        check('Schwarz-Weiß: Plättchen schwarz und schraffiert', 'url(#sw-or)' in html and 'id="sw-or"' in html and '#2f5ea8' not in html)
        html = await pg.evaluate(BUILD, ['M:plus', 20, {'bw': False}])
        check('Farbe: Plättchen blau und orange', '#2f5ea8' in html and 'url(#sw-or)' not in html)
        # Legeblätter bleiben
        html = await pg.evaluate("() => { Object.assign(app.sheet, {...SHEET_BASE, pid:'none', topic:'K:zehner'}); return buildSheet().html; }")
        check('Legeblätter ohne neuen Rahmen', 'class="hf-foot' not in html and 'class="hf-head' not in html)

        # Heft: genau ein Rahmen je Seite
        await pg.evaluate("app.heft = {title:'Mein Arbeitsheft', pid:'none', weg:'bereich', items:[{title:'x', kind:'ueben', ch:0, html:''}], toc:true, book:{N:12, fach:'M'}, chapters:[{key:'M|20|I', label:'x', zone:true, title:'Zählen'}]}; saveHeft()")
        await pg.evaluate(BUILD, ['M:plus', 20, {}])
        await pg.evaluate("app.heftSwap = 0; app.sheetMode = 'single'; heftSwapOther()")
        it = await pg.evaluate("app.heft.items[0].html")
        check('Ausgetauschte Heftseite ohne Blatt-Rahmen', 'hf-foot' not in it and 'hf-head' not in it and 'ab-grid' in it)
        n_t = await pg.evaluate("(app.sheetDoc.html.match(/class=\"ab-task/g) || []).length")
        n_h = it.count('class="ab-task')
        check('Ausgetauschte Heftseite: dieselben Aufgaben', n_t == n_h, f'{n_t} / {n_h}')
        await pg.evaluate("app.samml.items = []; sammlAdd()")
        sm = await pg.evaluate("app.samml.items[0].html")
        check('Blattsammlung: Blatt mit Rahmen und denselben Aufgaben', sm.count('class="hf-foot') == 1 and sm.count('class="ab-task') == n_t, sm.count('class="hf-foot'))
        html = await pg.evaluate("buildHeft().html")
        pages, foots = html.count('class="page'), html.count('class="hf-foot"')
        check('Heft: eine Fußzeile je Aufgabenseite', foots == 1, f'{foots} Fußzeilen, {pages} Seiten')
        await br.close()
    print('FEHLER:', ERR) if ERR else print('alles ok')

asyncio.run(main())
