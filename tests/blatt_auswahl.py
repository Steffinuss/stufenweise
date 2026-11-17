"""Arbeitsblätter: Auswahl in drei Schritten (0.28.4, Wunsch Stefan: „langsam sehr unübersichtlich“).
Fach (Basis, Mathe, Deutsch) → Bereich (Legeblätter beim jeweiligen Fach) → Blatt. Jedes Blatt aus sheetTopics()
steht genau einmal im Baum, kein Bereich hat mehr als 12 Blätter. Fach- und Bereichswechsel wählen ein Blatt
(beim Zurückwechseln das zuletzt gewählte). „Zuletzt benutzt“ nach Drucken/Heft. Ein Kind mit Förderzone stellt
das passende Fach ein. Das Arbeitsheft nimmt Blätter aus allen Fächern auf."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        r = await pg.evaluate("""(()=>{ const all = sheetTopics().flatMap(([, o]) => o.map(x => x[0])), tree = sheetTree(), flat = tree.flatMap(f => f.areas.flatMap(a => a.items.map(x => x[0])));
          return {fach: tree.map(f => f.id).join(), miss: all.filter(t => !flat.includes(t)), dup: flat.filter((t, i) => flat.indexOf(t) !== i), big: tree.flatMap(f => f.areas.filter(a => a.items.length > 12).map(a => f.name + ' ' + a.name)),
            areas: tree.map(f => f.name + ': ' + f.areas.map(a => a.name + ' ' + a.items.length).join(', '))}; })()""")
        for x in r['areas']: print(x)
        if r['fach'] != 'B,M,D': errs.append(f"Fächer: {r['fach']}")
        if r['miss'] or r['dup'] or r['big']: errs.append(f"Baum: fehlt {r['miss']}, doppelt {r['dup']}, zu groß {r['big']}")
        if any('Legeblätter' not in a for a in r['areas']): errs.append('Legeblätter fehlen bei einem Fach')
        await pg.evaluate("app.sheet.recent = []; openSheets('none')"); await pg.wait_for_timeout(400)
        if await pg.query_selector('#sh-topic'): errs.append('altes Auswahlfeld noch da')
        await pg.click('[data-shfach="B"]'); await pg.wait_for_timeout(200)
        if not (await pg.evaluate("app.sheet.topic")).startswith('B:'): errs.append('Fach Basis wählt kein Basis-Blatt')
        await pg.click('[data-sharea="2"]'); await pg.wait_for_timeout(200)
        if not (await pg.evaluate("app.sheet.topic")).startswith('K:'): errs.append('Bereich Legeblätter wählt kein Legeblatt')
        await pg.click('[data-shtopic="K:muster"]'); await pg.wait_for_timeout(200)
        await pg.click('#sh-heft'); await pg.wait_for_timeout(200)
        await pg.click('[data-shfach="D"]'); await pg.wait_for_timeout(200); await pg.click('[data-sharea="1"]'); await pg.click('[data-shtopic="W:W1"]'); await pg.wait_for_timeout(300)
        await pg.click('#sh-heft'); await pg.wait_for_timeout(200)
        await pg.click('[data-shfach="B"]'); await pg.wait_for_timeout(200)
        if await pg.evaluate("app.sheet.topic") != 'K:muster': errs.append('Zurück ins Fach: zuletzt gewähltes Blatt nicht wieder da')
        rec = await pg.evaluate("[...document.querySelectorAll('.sh-recent [data-shtopic]')].map(b=>b.dataset.shtopic).join()")
        if rec != 'W:W1': errs.append(f'Zuletzt benutzt: {rec}')
        heft = await pg.evaluate("app.heft.items.map(i=>i.title).join(' | ')")
        if 'Musterstreifen' not in heft and 'Muster' not in heft or 'abschreiben' not in heft.lower(): errs.append(f'Heft über Fächer: {heft}')
        print('Heft:', heft)
        # Kind mit Förderzone in Lesen: Fach Deutsch voreingestellt
        await pg.evaluate("""(()=>{ const p={id:'kz',name:'Zoe',created:1}; data.profiles.push(p); setCell('kz','L|L3',{status:'nicht', source:'test', ts:Date.now()}); setCell('kz','L|L2',{status:'erreicht', source:'test', ts:Date.now()}); app.sheet.topic='M:plus'; renderSheets(); })()""")
        await pg.select_option('#sh-kid', 'kz'); await pg.wait_for_timeout(300)
        t = await pg.evaluate("[app.sheet.topic, sheetPlace(app.sheet.topic)?.fach]")
        if t[1] != 'D': errs.append(f'Kind mit Lese-Förderzone: {t}')
        print('ERR', errs[:10]); await b.close()
asyncio.run(main())
