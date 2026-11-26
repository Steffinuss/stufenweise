"""„Große Aufgaben“ im Heft-Assistenten (Backlog N, Wunsch Stefan 26.11.2026):
- Häkchen „Große Aufgaben (mehr Platz zum Schreiben und Streichen)“, anfangs aus, gemerkt im Heft.
- Mit Häkchen: Übungsseiten, „Das kann ich schon“ und Wiederholung mit großen Aufgaben; die Seitenzahl bleibt.
- Ohne Häkchen: keine großen Aufgaben auf Übungsseiten, auch wenn das letzte Einzelblatt sie hatte.
- Das Heft nimmt feste Grundeinstellungen, nicht die Einstellungen des letzten Einzelblatts; diese bleiben danach erhalten.
- Passt groß nicht einmal eine Aufgabe (lange Texte), wird nur diese Seite normal groß."""
import asyncio
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

KID = """(z) => { const id = newId('p-'); data.profiles.push({id, name:z.name, created:1, updated:1, world:'HS'}); data.current = id;
  for(const k of z.ok) setCell(id, k, {status:'erreicht', quelle:'test', sum:''});
  for(const k of z.part) setCell(id, k, {status:'teilweise', quelle:'test', sum:''});
  saveData(); return id; }"""
MIA = {'name': 'Mia', 'ok': ['M|10|I', 'M|10|II', 'M|20|I', 'R|R1', 'R|R2'], 'part': ['M|20|II', 'R|R3']}
LIA = {'name': 'Lia', 'ok': ['L|L1', 'L|L2', 'L|L3', 'L|L4', 'L|L5', 'L|L6', 'L|L7', 'L|L8'], 'part': ['L|L9']}
STAT = """() => { const it = app.heft.items, g = i => i.html.includes('ab-grid gross');
  return {total: heftTotal(app.heft), N: app.heft.book?.N, over: it.filter(i => i.over).length,
    ueben: it.filter(i => i.kind === 'ueben').length, uebenG: it.filter(i => i.kind === 'ueben' && g(i)).length,
    kann: it.filter(i => i.kind === 'kann').length, kannG: it.filter(i => i.kind === 'kann' && g(i)).length,
    wdh: it.filter(i => i.kind === 'wdh').length, wdhG: it.filter(i => i.kind === 'wdh' && g(i)).length,
    sheet: [app.sheet.gross, app.sheet.mat, app.sheet.lcase, app.sheet.draw]}; }"""

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 900})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        mia = await pg.evaluate(KID, MIA)
        # letztes Einzelblatt: große Aufgaben, ohne Materialbilder, Kleinbuchstaben, zeichnen
        await pg.evaluate("Object.assign(app.sheet, {gross:true, mat:false, lcase:true, draw:true}); sheetSave()")
        await pg.evaluate("pid => { app.heft = {title:'Mein Arbeitsheft', pid, items:[], toc:true, fach:'M', pages:12, vor:'zone'}; saveHeft(); openHeftZone(pid); }", mia)
        await pg.wait_for_timeout(400)
        box = pg.locator('#hf-gross')
        check('Häkchen da und anfangs aus', await box.count() == 1 and not await box.is_checked())
        lab = await pg.evaluate("document.querySelector('#hf-gross').closest('label').textContent.trim()")
        check('Beschriftung wie beim Einzelblatt', lab == 'Große Aufgaben (mehr Platz zum Schreiben und Streichen)', lab)

        # ohne Häkchen: nichts vom letzten Einzelblatt übernehmen
        await pg.evaluate("async pid => { await heftMake(pid); }", mia)
        a = await pg.evaluate(STAT)
        print('ohne:', a)
        check('ohne Häkchen: Übungsseiten normal groß', a['uebenG'] == 0 and a['kannG'] == 0, str(a))
        check('ohne Häkchen: Seitenzahl stimmt', a['total'] == a['N'] == 12, f"{a['total']}/{a['N']}")
        mat = await pg.evaluate("app.heft.items.filter(i => i.kind === 'ueben' && /mit Bild/.test(i.title)).length")
        check('Feinstufe „mit Bild“ trotz Einzelblatt ohne Materialbilder', mat > 0)
        tasks0 = await pg.evaluate("""() => app.heft.items.filter(i => i.kind === 'ueben').map(i => (i.html.match(/class="ab-task/g) || []).length)""")
        check('Einstellungen des Einzelblatts bleiben erhalten', a['sheet'] == [True, False, True, True], str(a['sheet']))

        # mit Häkchen
        await box.check(); await pg.wait_for_timeout(300)
        check('Häkchen wird gemerkt', await pg.evaluate("JSON.parse(localStorage.getItem(HEFT_KEY)).gross === true"))
        await pg.evaluate("async pid => { await heftMake(pid); }", mia)
        b = await pg.evaluate(STAT)
        print('mit:', b)
        check('mit Häkchen: Übungsseiten groß', b['uebenG'] == b['ueben'] > 0, f"{b['uebenG']}/{b['ueben']}")
        check('mit Häkchen: „Das kann ich schon“ groß', b['kannG'] == b['kann'] > 0, f"{b['kannG']}/{b['kann']}")
        check('mit Häkchen: Seitenzahl bleibt', b['total'] == b['N'] == 12 and b['over'] == 0, f"{b['total']}/{b['N']}, über: {b['over']}")
        tasks = await pg.evaluate("""() => app.heft.items.filter(i => i.kind === 'ueben').map(i => (i.html.match(/class="ab-task/g) || []).length)""")
        check('große Aufgaben: weniger Aufgaben je Seite', sum(tasks) < sum(tasks0), f'normal {tasks0}, groß {tasks}')
        await pg.evaluate("app.heft.pages = 24; saveHeft()")
        await pg.evaluate("async pid => { await heftMake(pid); }", mia)
        c = await pg.evaluate(STAT)
        check('24 Seiten mit Wiederholung: groß, Seitenzahl stimmt', c['total'] == c['N'] == 24 and c['over'] == 0 and (c['wdh'] == 0 or c['wdhG'] >= 1), str(c))
        html = await pg.evaluate("buildHeft().html")
        doc = await br.new_page(); await doc.set_content(html); await doc.wait_for_timeout(1200)
        info = await doc.evaluate("[document.querySelectorAll('.page').length, [...document.querySelectorAll('.page')].filter(p => p.dataset.over).length]")
        await doc.close()
        check('Druck: keine Seite läuft über', info[1] == 0 and info[0] == 24, str(info))

        # lange Texte (L9): passt groß nicht, dann normal groß
        lia = await pg.evaluate(KID, LIA)
        await pg.evaluate("pid => { app.heft = {title:'Mein Arbeitsheft', pid, items:[], toc:true, fach:'D', pages:12, vor:'zone', gross:true, story:'aus'}; saveHeft(); }", lia)
        await pg.evaluate("async pid => { await heftMake(pid); }", lia)
        d = await pg.evaluate(STAT)
        print('lange Texte:', d)
        check('lange Texte: Heft passt', d['total'] == d['N'] == 12 and d['over'] == 0, str(d))
        await br.close()
    print('FEHLER:', ERR) if ERR else print('alles ok')

asyncio.run(main())
