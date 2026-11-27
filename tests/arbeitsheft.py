import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        pg=await b.new_page(viewport={'width':1180,'height':820}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.evaluate("data.profiles.push({id:'k1',name:'Lea'}); saveData();")
        await pg.evaluate("app.sheet.topic='M:plus'; app.sheet.zr=20; openSheets()"); await pg.wait_for_timeout(1500)
        await pg.click('#sh-samml'); await pg.wait_for_timeout(300)
        await pg.click('[data-shfach="D"]'); await pg.click('[data-sharea="0"]'); await pg.click('[data-shtopic="L:L2"]'); await pg.wait_for_timeout(1500)
        await pg.click('#sh-samml'); await pg.wait_for_timeout(300)
        await pg.click('[data-shfach="M"]'); await pg.click('[data-sharea="3"]'); await pg.click('[data-shtopic="U:U1"]'); await pg.wait_for_timeout(1500)
        await pg.click('#sh-samml'); await pg.wait_for_timeout(300)
        # Backlog U2: gesammelte Blätter landen in der Blattsammlung, nicht im Heft
        await pg.click('[data-shmode="samml"]'); await pg.wait_for_timeout(800)
        print('items', await pg.evaluate("app.samml.items.map(i=>i.title)"), 'heft', await pg.evaluate("app.heft.items.length"))
        d="document.querySelector('#sh-frame').contentDocument"
        print('pages', await pg.evaluate(f"{d}.querySelectorAll('.page').length"), 'meta', await pg.evaluate(f"{d}.querySelectorAll('.ab-meta').length"), 'sol', await pg.evaluate(f"{d}.querySelectorAll('.sol').length"))
        print('foot', await pg.evaluate(f"[...{d}.querySelectorAll('.ab-lic')].map(e=>e.textContent.slice(0,30))"))
        await pg.screenshot(path='blattsammlung.png')
        await pg.click('[data-sm-down="0"]'); await pg.wait_for_timeout(300)
        print('after move', await pg.evaluate("app.samml.items.map(i=>i.title)"))
        await pg.reload(); await pg.wait_for_timeout(400)
        print('persisted', await pg.evaluate("app.samml.items.length"))
        # print-page overflow check: measure page heights in a print-like iframe
        print('ERR',errs); await b.close()
asyncio.run(main())
