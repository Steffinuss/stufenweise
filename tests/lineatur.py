"""Lineatur zum Schreiben (Backlog L, Wunsch Stefan 26.11.2026):
- Drei Arten: Haus mit drei Stockwerken (Dach, Erdgeschoss, Keller), zwei Linien, eine Linie.
- Standard nach Themenwelt des Kindes: Grundstufe Haus, Hauptstufe und Berufsschulstufe eine Linie (Stefan).
- Auswahl „Lineatur“ nur bei Blättern mit Schreibzeilen; die Wahl wird gemerkt. Im Heft-Assistenten eigene Auswahl,
  sie gilt für die Blätter im Heft und die Schreiblinien der Fortsetzungsgeschichte.
- Dazu (Stefan 26.11.): Das Zwanzigerfeld auf dem Deckblatt ist zeilenweise gefüllt wie in der App."""
import asyncio
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

LINES = """([topic, pid, lin]) => { Object.assign(app.sheet, {...SHEET_BASE, pid, topic, zr:20, n:8, sol:false, lin}); const d = buildSheet();
  return [...new Set([...d.html.matchAll(/class="ab-wline ([^"]*)"/g)].map(m => m[1]))]; }"""
KID = """(z) => { const id = newId('p-'); data.profiles.push({id, name:z.name, created:1, updated:1, world:z.world}); data.current = id;
  for(const k of z.ok) setCell(id, k, {status:'erreicht', quelle:'test', sum:''});
  for(const k of z.part) setCell(id, k, {status:'teilweise', quelle:'test', sum:''});
  saveData(); return id; }"""

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 900})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        gs = await pg.evaluate(KID, {'name': 'Ali', 'world': 'GS', 'ok': ['L|L1', 'L|L2', 'L|L3', 'L|L4', 'L|L5', 'W|W1', 'W|W2', 'W|W3', 'W|W4'], 'part': ['L|L6', 'W|W5']})
        hs = await pg.evaluate(KID, {'name': 'Bea', 'world': 'HS', 'ok': [], 'part': []})
        bss = await pg.evaluate(KID, {'name': 'Cem', 'world': 'BSS', 'ok': [], 'part': []})

        check('Grundstufe: Haus', await pg.evaluate(LINES, ['W:W3', gs, 'auto']) == ['lin-haus'])
        check('Hauptstufe: eine Linie', await pg.evaluate(LINES, ['W:W3', hs, 'auto']) == ['lin-eins'])
        check('Berufsschulstufe: eine Linie', await pg.evaluate(LINES, ['W:W3', bss, 'auto']) == ['lin-eins'])
        for v in ['haus', 'zwei', 'eins']:
            check(f'gewählt: {v}', await pg.evaluate(LINES, ['W:W6', hs, v]) == [f'lin-{v}'])

        # Höhe: Haus braucht am meisten Platz, alle Blätter passen trotzdem
        h = await pg.evaluate("""() => { const d = document.createElement('div'); d.innerHTML = `<style>${SHEET_CSS}</style>` + ['haus', 'zwei', 'eins'].map(v => `<div class="ab-wline lin-${v}" style="width:50mm"></div>`).join(''); document.body.append(d);
          const r = [...d.querySelectorAll('.ab-wline')].map(e => Math.round(e.getBoundingClientRect().height/3.7795)); d.remove(); return r; }""")
        check('Höhen: Haus 16 mm, zwei Linien 13 mm, eine Linie 12 mm', h == [16, 13, 12], str(h))

        # Auswahl im Generator nur bei Blättern mit Schreibzeilen
        lt = await pg.evaluate("sheetTopics().flatMap(([, o]) => o).map(x => x[0]).filter(sheetHasLines)")
        check('Blätter mit Schreibzeilen erkannt', {'W:W3', 'W:W4', 'W:W6', 'U:U3'} <= set(lt) and not any(t.startswith('M:') or t.startswith('B:') for t in lt), str(lt))
        await pg.evaluate("pid => { app.sheet.topic = 'W:W3'; app.sheet.lin = 'auto'; openSheets(pid); }", gs); await pg.wait_for_timeout(500)
        opt = await pg.evaluate("[...document.querySelectorAll('#sh-lin option')].map(o => o.textContent)")
        check('Auswahl Lineatur bei W3, Standard nennt die Art', len(opt) == 4 and 'Haus' in opt[0], str(opt))
        await pg.select_option('#sh-lin', 'zwei'); await pg.wait_for_timeout(500)
        prev = await pg.evaluate("app.sheetDoc.html.includes('lin-zwei')")
        kept = await pg.evaluate("JSON.parse(localStorage.getItem(SHEET_KEY)).lin")
        check('Auswahl wirkt auf das Blatt und wird gemerkt', prev and kept == 'zwei', f'{prev} {kept}')
        await pg.evaluate("app.sheet.topic = 'M:plus'; renderSheets()"); await pg.wait_for_timeout(300)
        check('keine Auswahl bei Plus', await pg.locator('#sh-lin').count() == 0)
        await pg.evaluate("document.querySelectorAll('dialog[open]').forEach(d => d.close()); app.sheet.lin = 'auto'; sheetSave()")

        # Heft: eigene Auswahl, gilt für Blätter und Geschichte
        await pg.evaluate("pid => { app.heft = {title:'Mein Arbeitsheft', pid, items:[], toc:true, fach:'D', pages:24, vor:'zone'}; saveHeft(); openHeftZone(pid); }", gs)
        await pg.wait_for_timeout(400)
        check('Heft-Assistent: Auswahl Lineatur', await pg.locator('#hf-lin').count() == 1)
        await pg.select_option('#hf-lin', 'zwei'); await pg.wait_for_timeout(300)
        check('Heft: Auswahl gemerkt', await pg.evaluate("JSON.parse(localStorage.getItem(HEFT_KEY)).lin") == 'zwei')
        await pg.evaluate("async pid => { await heftMake(pid); }", gs)
        r = await pg.evaluate("""() => { const all = app.heft.items.map(i => i.html).join(''); return {zwei: (all.match(/lin-zwei/g) || []).length, andere: (all.match(/lin-(haus|eins)/g) || []).length,
          story: app.heft.items.some(i => i.kind === 'story' && i.html.includes('hf-lines lin-zwei')), over: app.heft.items.filter(i => i.over).length, total: heftTotal(app.heft), N: app.heft.book?.N}; }""")
        print(r)
        check('Heft: Blätter und Geschichte mit zwei Linien', r['zwei'] > 0 and r['andere'] == 0 and r['story'], str(r))
        check('Heft: Seitenzahl stimmt, nichts läuft über', r['total'] == r['N'] == 24 and r['over'] == 0, str(r))
        check('Einzelblatt danach wieder „passend zur Stufe“', await pg.evaluate("app.sheet.lin") == 'auto')

        # Deckblatt: Zwanzigerfeld zeilenweise (8 blau, dann 3 orange: oben 8 + 2, unten 1)
        f = await pg.evaluate("""() => { const d = document.createElement('div'); d.innerHTML = zfSvg(8, 3, '#b', '#o'); return [...d.querySelectorAll('circle')].map(c => c.getAttribute('fill')).map(x => x === '#b' ? 'b' : x === '#o' ? 'o' : '.').join(''); }""")
        check('Deckblatt: Zwanzigerfeld zeilenweise gefüllt', f == 'bbbbbbbboo' + 'o.........', f)
        await br.close()
    print('FEHLER:', ERR) if ERR else print('alles ok')

asyncio.run(main())
