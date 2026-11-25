"""Sätze legen mit Ziehen (Stefan, 25.11.2026): Satz-Baukasten an der Tafel und Schüttelsätze.
Aus dem Vorrat an eine Stelle ziehen, im Satz verschieben, herausziehen; Antippen eines gelegten Worts legt es zurück."""
import asyncio
from common import URL, launch, FOKUS_AUS
from playwright.async_api import async_playwright

RES = []
def chk(name, cond, info=''):
    RES.append(cond); print(('ok ' if cond else 'FEHLER ') + f' [{name}] {info}')


async def drag(pg, src, x, y):
    b = await src.bounding_box()
    await pg.mouse.move(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); await pg.mouse.down()
    for k in range(1, 9):
        await pg.mouse.move(b['x'] + b['width'] / 2 + (x - b['x'] - b['width'] / 2) * k / 8, b['y'] + b['height'] / 2 + (y - b['y'] - b['height'] / 2) * k / 8)
    await pg.mouse.up(); await pg.wait_for_timeout(450)


async def main():
    async with async_playwright() as p:
        b = await launch(p)
        pg = await b.new_page(viewport={'width': 1180, 'height': 820})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script(FOKUS_AUS)
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.click("[data-ctx='class']"); await pg.click(".wz-body [data-ctool='tsatz']"); await pg.wait_for_timeout(300)
        await pg.evaluate("tsSet('Mia stellt die Tassen und die Teller in den Schrank.'); renderTsatz()")
        line = lambda: pg.evaluate("app.ts.order.map(i => app.ts.words[i]).join(' ')")
        # antippen: Mia, stellt, die
        for i in [0, 1, 2]: await pg.click(f"[data-tsw='{i}']")
        chk('Antippen legt hinten an', await line() == 'Mia stellt die')
        # „Teller“ (Index 6) zwischen „Mia“ und „stellt“ ziehen
        mia = await pg.locator("[data-sdin='0']").bounding_box()
        await drag(pg, pg.locator("[data-tsw='6']"), mia['x'] + mia['width'] + 4, mia['y'] + mia['height'] / 2)
        chk('aus dem Vorrat an eine Stelle ziehen', await line() == 'Mia Teller stellt die', await line())
        # „Teller“ ans Ende verschieben
        last = await pg.locator("[data-sdin='3']").bounding_box()
        await drag(pg, pg.locator("[data-sdin='1']"), last['x'] + last['width'] + 30, last['y'] + last['height'] / 2)
        chk('im Satz verschieben', await line() == 'Mia stellt die Teller', await line())
        # Antippen eines gelegten Worts legt zurück
        await pg.click("[data-sdin='3']"); await pg.wait_for_timeout(200)
        chk('antippen legt zurück', await line() == 'Mia stellt die', await line())
        # herausziehen
        tiles = await pg.locator('.ts-tiles').bounding_box()
        await drag(pg, pg.locator("[data-sdin='2']"), tiles['x'] + 40, tiles['y'] + tiles['height'] / 2)
        chk('herausziehen legt zurück', await line() == 'Mia stellt', await line())
        chk('Wort wieder im Vorrat', await pg.locator("[data-tsw='2']:not(:disabled)").count() == 1)

        # Schüttelsatz beim Üben (Lesen LS)
        await pg.goto(URL); await pg.wait_for_timeout(400)
        ok = await pg.evaluate("""(()=>{ try{ app.ctx='practice'; app.mode='read'; const R = app.read; R.lvl='LS';
           R.item = {type:'sent', words:'Ben wäscht seine Hände mit Wasser und Seife.'.split(' '), tiles:[7,3,0,5,1,2,6,4], label:'Satz'}; R.r = {}; R.fb = null; render(); return !!document.querySelector('#stage [data-sdline]'); }catch(e){ return String(e); } })()""")
        chk('Schüttelsatz zeigt Satzzeile', ok is True, str(ok))
        if ok is True:
            sline = lambda: pg.evaluate("app.read.r.order.map(i => app.read.item.words[i]).join(' ')")
            for i in [0, 1, 2]: await pg.click(f"#stage [data-wword='{i}']")
            first = await pg.locator("#stage [data-sdin='0']").bounding_box()
            await drag(pg, pg.locator("#stage [data-sdin='2']"), first['x'] - 10, first['y'] + first['height'] / 2)
            chk('Schüttelsatz: verschieben', await sline() == 'seine Ben wäscht', await sline())
            await pg.click("#stage [data-sdin='0']"); await pg.wait_for_timeout(200)
            chk('Schüttelsatz: antippen legt zurück', await sline() == 'Ben wäscht', await sline())
        chk('keine Fehler', not errs, str(errs))
        await b.close()
    print('ERR', [] if all(RES) else ['siehe oben'])

asyncio.run(main())
