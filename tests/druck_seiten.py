"""Druck = Vorschau (Stefan, 23.11.2026): Jedes Blatt im Arbeitsheft und auf Arbeitsblättern wird genau eine A4-Seite.
Bis 0.30 durfte ein Blatt in der Vorschau länger als A4 sein; im Druck rutschte der Rest (Inhaltsverzeichnis, Fußzeile,
lange Lesetexte) auf ein eigenes Blatt. Geprüft wird mit echtem Druck (Chrome → PDF) und Seitenzählung.
Zu hohe Blätter werden verkleinert (PAGE_FIT_JS), ein langes Inhaltsverzeichnis bekommt eine eigene Seite."""
import asyncio, re
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

KID = """() => { const id = newId('p-'); data.profiles.push({id, name:'Omer', created:1, updated:1, world:'HS'}); data.current = id;
  for(const k of ['M|10|I','M|10|II','M|20|I']) setCell(id, k, {status:'erreicht', quelle:'test', sum:''});
  for(const k of ['M|20|II','R|R3','Z|Z1','U|U1','G|G1','H|H3','L|L9']) setCell(id, k, {status:'teilweise', quelle:'test', sum:''});
  for(const k of ['L|L1','L|L2','L|L3','L|L4','L|L5','L|L6','L|L7','L|L8']) setCell(id, k, {status:'erreicht', quelle:'test', sum:''});
  saveData(); return id; }"""

async def printed(br, html):
    doc = await br.new_page(); await doc.set_content(html); await doc.wait_for_timeout(700)
    n = await doc.evaluate("document.querySelectorAll('.page').length")
    fit = await doc.evaluate("[...document.querySelectorAll('.page')].map(p => p.dataset.fit || '').filter(Boolean)")
    pdf = await doc.pdf(prefer_css_page_size=True, print_background=True)
    await doc.close()
    return n, len(re.findall(rb'/Type\s*/Page[^s]', pdf)), fit

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 820})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        pid = await pg.evaluate(KID)

        # 1. Heft zur Förderzone mit 2 Blättern je Zone: langes Inhaltsverzeichnis auf eigener Seite
        await pg.evaluate("async pid => { app.heft.toc = true; await heftFromZones(pid, 2); }", pid)
        items = await pg.evaluate("app.heft.items.length")
        html = await pg.evaluate("buildHeft().html")
        n, pr, fit = await printed(br, html)
        check('Heft: jede Seite ein Blatt', n == pr == items + 2, f'{items} Blätter, {n} Seiten im Heft, {pr} gedruckt, verkleinert {fit}')
        check('Inhaltsverzeichnis eigene Seite', 'class="page tocp"' in html)

        # 2. Ein viel zu hohes Blatt wird auf eine Seite verkleinert
        await pg.evaluate("""() => { const long = '<h2>Sehr langer Text</h2>' + Array.from({length: 22}, (_, i) => `<p style="font-size:14pt">Absatz ${i + 1}: Bienen fliegen von Blüte zu Blüte und sammeln Nektar.</p>`).join('') + '<p class="ab-foot ab-lic">Stufenweise</p>';
          app.heft.items = app.heft.items.slice(0, 3).concat([{title:'Zu lang', html: long}]); }""")
        n, pr, fit = await printed(br, await pg.evaluate("buildHeft().html"))
        check('zu hohes Blatt verkleinert', n == pr and len(fit) == 1 and 0.8 <= float(fit[0]) < 1, f'{n} Seiten, {pr} gedruckt, Faktor {fit}')
        await pg.evaluate("() => { app.heft.items[3].html = app.heft.items[3].html.repeat(3); }")
        n, pr, fit = await printed(br, await pg.evaluate("buildHeft().html"))
        check('viel zu hoch: nicht unter 80 %, läuft weiter', not fit and pr > n, f'{n} Seiten, {pr} gedruckt, verkleinert {fit}')

        await pg.evaluate("app.heft.items = app.heft.items.slice(0, 3)")
        # 3. Kurzes Heft: Inhaltsverzeichnis bleibt auf dem Deckblatt
        await pg.evaluate("app.heft.items = app.heft.items.slice(0, 3)")
        html = await pg.evaluate("buildHeft().html")
        n, pr, fit = await printed(br, html)
        check('kurzes Heft: Inhalt auf dem Deckblatt', 'class="page tocp"' not in html and n == pr == 4, f'{n} Seiten, {pr} gedruckt')

        # 4. Einzelnes Arbeitsblatt Lesen L9 (lange Texte), mit Lösungsblatt
        for topic in ['L:L9', 'M:plus']:
            ok = await pg.evaluate("""t => { const S = app.sheet; if(!sheetTopics().some(([, o]) => o.some(x => x[0] === t))) return false;
              Object.assign(S, {topic: t, n: 6, sol: true}); app.sheetDoc = buildSheet(); return true; }""", topic)
            if not ok: print(f'(Thema {topic} nicht gefunden, übersprungen)'); continue
            n, pr, fit = await printed(br, await pg.evaluate("app.sheetDoc.html"))
            check(f'Arbeitsblatt {topic}', all(float(f) >= 0.8 for f in fit) and pr >= n, f'{n} Seiten, {pr} gedruckt, verkleinert {fit}')
            if pr > n:   # läuft weiter: die Vorschau muss es sagen
                d = await br.new_page(); await d.set_content(await pg.evaluate("app.sheetDoc.html")); await d.wait_for_timeout(500)
                over = await d.evaluate("[...document.querySelectorAll('.page[data-over]')].map(p => p.dataset.over)")
                check(f'Vorschau-Hinweis {topic}', over and int(over[0]) >= 2, str(over)); await d.screenshot(path='druck_hinweis.png'); await d.close()

        # 5. „Große Aufgaben“ werden nie verkleinert (läuft dann weiter, Hinweis in der Vorschau)
        html = await pg.evaluate("() => { Object.assign(app.sheet, {topic:'L:L1', n:8, sol:false, gross:true}); const h = buildSheet().html; app.sheet.gross = false; return h; }")
        n, pr, fit = await printed(br, html)
        check('Große Aufgaben nicht verkleinert', not fit, f'{n} Seiten, {pr} gedruckt, verkleinert {fit}')
        # 6. Legeblätter bleiben unberührt
        html = await pg.evaluate("() => { const k = Object.keys(LEGE)[0]; return legeSheet(k).html; }")
        if html:
            n, pr, fit = await printed(br, html)
            check('Legeblatt unverändert', not fit and n == pr, f'{n} Seiten, {pr} gedruckt')
        await br.close()
    print('FERTIG', 'Fehler: ' + ', '.join(ERR) if ERR else 'alles ok')

asyncio.run(main())
