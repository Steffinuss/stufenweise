"""Heft zur Förderzone mit Optionen (Stefan, 23.11.):
- „Schwarz-Weiß-Drucker“ nur, wenn Basis-Blätter dabei sind; Basis-Blätter im Heft dann mit Mustern
- „Ausgefüllte Hundertertafel als Extraseite“ nur, wenn Hundertertafel-Blätter dabei sind; dann einmal hinten im Heft
- beide Häkchen werden gemerkt; ohne Häkchen keine Extraseite"""
import asyncio
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

KID = """(cells) => { const id = newId('p-'); data.profiles.push({id, name:'Mia', created:1, updated:1, world:'HS', basis:true}); data.current = id;
  for(const k of ['M|10|I','M|10|II','M|20|I']) setCell(id, k, {status:'erreicht', quelle:'test', sum:''});
  for(const k of cells) setCell(id, k, {status:'teilweise', quelle:'test', sum:''});
  saveData(); return id; }"""

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 820})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        a = await pg.evaluate(KID, ['M|20|II', 'H|H3', 'H|H5', 'V|V3'])
        b = await pg.evaluate(KID, ['M|20|II', 'U|U1'])
        print('Zonen a', await pg.evaluate("pid => heftZones(pid).map(z => z.key)", a))

        async def dialog(pid):
            await pg.evaluate("pid => { app.heft.items = []; openHeftZone(pid); }", pid); await pg.wait_for_timeout(300)
            return await pg.locator('#hf-bw').count(), await pg.locator('#hf-taf').count()
        bw, taf = await dialog(a)
        check('Kind mit Tafel und Basis: beide Häkchen', bw == 1 and taf == 1, f'{bw} {taf}')
        bw, taf = await dialog(b)
        check('Kind ohne Tafel und Basis: keine Häkchen', bw == 0 and taf == 0, f'{bw} {taf}')

        # ohne Häkchen
        await dialog(a)
        await pg.evaluate("async pid => { await heftFromZones(pid, 1); }", a)
        it = await pg.evaluate("app.heft.items.map(i => i.title)")
        check('ohne Häkchen keine Extraseite', not any('Nachschauen' in t for t in it), str(it))
        bwpat = await pg.evaluate("app.heft.items.some(i => /url\\(#bw|fill=\\\"url\\(#/.test(i.html))")
        check('ohne Häkchen farbig', not bwpat)

        # mit Häkchen (über die Oberfläche)
        await dialog(a)
        await pg.locator('#hf-bw').check(); await pg.wait_for_timeout(200)
        await pg.locator('#hf-taf').check(); await pg.wait_for_timeout(200)
        saved = await pg.evaluate("(h => [h.bw, h.taf])(JSON.parse(localStorage.getItem(HEFT_KEY)))")
        check('Häkchen gemerkt', saved == [True, True], str(saved))
        await pg.evaluate("async pid => { await heftFromZones(pid, 2); }", a)
        it = await pg.evaluate("app.heft.items.map(i => i.title + ' | ' + (i.cls || ''))")
        print(it)
        check('Extraseite einmal, ganz hinten', sum('Nachschauen' in t for t in it) == 1 and 'Nachschauen' in it[-1] and 'hilfe' in it[-1])
        cells = await pg.evaluate("app.heft.items.at(-1).html.match(/hb-c/g)?.length || 0")
        check('Tafel vollständig', cells >= 100, str(cells))
        bwpat = await pg.evaluate("app.heft.items.some(i => /url\\(#bw|fill=\\\"url\\(#/.test(i.html))")
        check('Basis-Blätter mit Mustern', bwpat)
        keep = await pg.evaluate("[app.sheet.bw, app.sheet.taf]")
        check('Einstellungen der Einzelblätter unverändert', keep == [False, False], str(keep))
        html = await pg.evaluate("buildHeft().html")
        check('Heft enthält Extraseite', 'page hilfe' in html and 'Hundertertafel zum Nachschauen' in html)

        # Kind ohne Tafel-Blätter: trotz gemerktem Häkchen keine Extraseite
        await pg.evaluate("async pid => { app.heft.taf = true; await heftFromZones(pid, 1); }", b)
        it = await pg.evaluate("app.heft.items.map(i => i.title)")
        check('ohne Tafel-Blätter keine Extraseite', not any('Nachschauen' in t for t in it), str(it))

        await pg.evaluate("app.heft.items = []; app.heft.bw = false; app.heft.taf = false; saveHeft()")
        print('Fehler:', ERR or 'keine')
        await br.close()
        if ERR: raise SystemExit(1)

asyncio.run(main())
