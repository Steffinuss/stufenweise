"""Stift an der Tafel in „Frei legen“ (Stefan, 25.11.2026): schreiben, Farben, Radierer, Strich zurück, Schrift weg,
Schrift bleibt beim Legen stehen; beim Üben (nicht Tafel) kein Stift."""
import asyncio
from common import URL, launch, FOKUS_AUS
from playwright.async_api import async_playwright

RES = []
def chk(name, cond, info=''):
    RES.append(cond); print(('ok ' if cond else 'FEHLER ') + f' [{name}] {info}')

async def stroke(pg, pts):
    await pg.mouse.move(*pts[0]); await pg.mouse.down()
    for p in pts[1:]: await pg.mouse.move(*p, steps=4)
    await pg.mouse.up(); await pg.wait_for_timeout(150)

async def main():
    async with async_playwright() as p:
        b = await launch(p)
        pg = await b.new_page(viewport={'width': 1180, 'height': 820})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script(FOKUS_AUS)
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.click("[data-ctx='class']"); await pg.click(".wz-body [data-ctool='free']"); await pg.wait_for_timeout(300)
        await pg.click("[data-kind='z']"); await pg.click("[data-kind='e']")
        n = lambda: pg.evaluate("board().ink.length")
        chk('Stift-Knopf an der Tafel', await pg.locator('#ink-pen').count() == 1)
        await pg.click('#ink-pen'); await pg.wait_for_timeout(200)
        chk('Stift an: Leiste mit Farben', await pg.locator('.ink-bar [data-inkc]').count() == 4)
        r = await pg.locator('#stage .board-wrap').bounding_box()
        x0, y0 = r['x'] + 300, r['y'] + 300
        await stroke(pg, [(x0, y0), (x0 + 80, y0 + 10), (x0 + 120, y0 + 60)])
        chk('Strich gezeichnet', await n() == 1 and await pg.locator('#stage svg.ink path').count() == 1)
        await pg.click(".ink-bar [data-inkc='1']")
        await stroke(pg, [(x0, y0 + 150), (x0 + 100, y0 + 150)])
        chk('zweiter Strich rot', await pg.evaluate("board().ink[1].c") == '#c9414a')
        pieces = await pg.evaluate("board().pieces.length")
        chk('Zeichnen legt kein Material', pieces == 2, str(pieces))
        await pg.click(".ink-bar [data-inkt='erase']"); await stroke(pg, [(x0 + 40, y0 + 150), (x0 + 60, y0 + 150)])
        chk('Radierer löscht Strich', await n() == 1)
        await pg.click(".ink-bar [data-inkt='undo']"); await pg.wait_for_timeout(100)
        chk('Strich zurück', await n() == 0)
        await pg.click(".ink-bar [data-inkc='2']"); await stroke(pg, [(x0, y0), (x0 + 50, y0 + 50)])
        await pg.click('#ink-pen'); await pg.wait_for_timeout(200)
        chk('Stift aus: Leiste weg, Schrift bleibt', await pg.locator('.ink-bar').count() == 0 and await pg.locator('#stage svg.ink path').count() == 1)
        await pg.click("[data-kind='e']"); await pg.wait_for_timeout(200)
        chk('Legen geht wieder, Schrift bleibt', await pg.evaluate("board().pieces.length") == 3 and await n() == 1)
        await pg.click('#f-all'); await pg.wait_for_timeout(200)
        chk('Alles weg löscht auch Schrift', await n() == 0)
        await pg.screenshot(path='/home/claude/stufenweise/tests/out/frei_stift.png')
        # Geld
        await pg.click('#ink-pen'); await stroke(pg, [(x0, y0), (x0 + 60, y0 + 20)]); await pg.click('#ink-pen')
        if await pg.locator("[data-fmat='money']").count():
            await pg.click("[data-fmat='money']"); await pg.wait_for_timeout(300)
            chk('Geld: Stift-Knopf und Schrift da', await pg.locator('#ink-pen').count() == 1 and await pg.locator('#stage svg.ink path').count() == 1)
        # Üben: kein Stift
        await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.evaluate("app.ctx='practice'; app.mode='free'; render()"); await pg.wait_for_timeout(300)
        chk('Üben: kein Stift', await pg.locator('#ink-pen').count() == 0)
        chk('keine Fehler', not errs, str(errs))
        await b.close()
    print('ERR', [] if all(RES) else ['siehe oben'])

asyncio.run(main())
