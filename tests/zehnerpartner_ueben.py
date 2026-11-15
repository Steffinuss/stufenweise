"""Üben „Zehnerpartner“ (Z1–Z3): Knopf in der Leiste, alle Stufen mit richtigen Antworten lösbar,
falsche Antwort wird erkannt, Statistik zeigt den Bereich. Dazu: Blitzblick und „Zahl suchen“ – „Neue Aufgabe“ zählt als übersprungen."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

async def main():
    async with async_playwright() as p:
        b = await launch(p); pg = await b.new_page(viewport={'width': 1180, 'height': 820}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.evaluate("settings.subject='M'; app.mode='number'; render()"); await pg.wait_for_timeout(300)
        if not await pg.locator('[data-tenpair]').count(): errs.append('Knopf Zehnerpartner fehlt')
        await pg.locator('[data-tenpair]').first.click(); await pg.wait_for_timeout(400)
        n = 0
        for lvl in ['Z1', 'Z2', 'Z3']:
            await pg.click(f'[data-rlvl="{lvl}"]'); await pg.wait_for_timeout(300)
            for k in range(8):
                it = await pg.evaluate("({t:app.read.item.type,f:app.read.item.fields,c:app.read.item.correct,label:app.read.item.label})")
                if it['t'] == 'input':
                    ins = pg.locator('#stage .dg-in'); m = await ins.count()
                    if m != len(it['f']): errs.append(f'{lvl}: {m} Felder statt {len(it["f"])}')
                    for i in range(m): await ins.nth(i).fill(str(it['f'][i]))
                    await ins.nth(m - 1).press('Enter')
                else:
                    await pg.locator('#stage .dg-choice button').nth(it['c']).click(); await pg.click('#r-check')
                await pg.wait_for_timeout(150)
                if not await pg.evaluate("app.read.fb?.ok"): errs.append(f'{lvl} {it["label"]}: richtige Antwort nicht erkannt')
                n += 1
                await pg.click('#r-next'); await pg.wait_for_timeout(150)
        while await pg.evaluate("app.read.item.type") != 'input': await pg.click('#btn-random'); await pg.wait_for_timeout(100)
        ins = pg.locator('#stage .dg-in')
        for i in range(await ins.count()): await ins.nth(i).fill('99')
        await pg.click('#r-check'); await pg.wait_for_timeout(200)
        if await pg.evaluate("app.read.fb?.ok") is not False: errs.append('falsche Antwort nicht erkannt')
        titles = await pg.evaluate("statsSections(data.current||'guest').map(s=>s.title)")
        print(n, 'Zehnerpartner-Aufgaben gelöst; Statistik:', titles)
        if 'Zehnerpartner' not in titles: errs.append('Statistik ohne Zehnerpartner')
        # Blitzblick: Neue Aufgabe oben = übersprungen
        await pg.evaluate("app.mode='blitz'; app.blitz.range=10; app.blitz.phase='idle'; render()"); await pg.wait_for_timeout(300)
        await pg.click('#b-go'); await pg.wait_for_timeout(300)
        before = await pg.evaluate("(data.skips?.[data.current||'guest']||[]).length")
        for i in range(2): await pg.click('#btn-random'); await pg.wait_for_timeout(250)
        after = await pg.evaluate("(data.skips?.[data.current||'guest']||[]).length")
        print('Blitzblick übersprungen:', after - before)
        if after - before != 2: errs.append(f'Blitzblick: {after - before} statt 2 übersprungen')
        # Zahlen: „Zahl suchen“ am Zahlenstrahl überspringen
        await pg.evaluate("app.mode='number'; app.range=100; render()"); await pg.wait_for_timeout(300)
        await pg.click('#btn-random'); await pg.wait_for_timeout(300)
        await pg.evaluate("task().view='line'; render()"); await pg.wait_for_timeout(300)
        await pg.click('#c-find'); await pg.wait_for_timeout(300)
        n0 = await pg.evaluate("(data.skips?.[data.current||'guest']||[]).length")
        await pg.click('#btn-random'); await pg.wait_for_timeout(300)
        last = await pg.evaluate("(data.skips?.[data.current||'guest']||[]).slice(-1)[0]?.task")
        print('Zahl suchen übersprungen:', last)
        if not (last or '').startswith('Zahl '): errs.append('Zahl suchen: Überspringen nicht gezählt')
        print('ERR', errs); await b.close()
asyncio.run(main())
