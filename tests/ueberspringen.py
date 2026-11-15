import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        pg=await b.new_page(viewport={'width':1180,'height':820}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.click("[data-ctx='practice']"); await pg.click('[data-board="1"]'); await pg.wait_for_timeout(300)
        res = lambda: pg.evaluate("JSON.stringify(app.round.res)")
        for _ in range(3): await pg.click('#btn-random'); await pg.wait_for_timeout(100)
        print('3 skips', await res())
        # switch level and back: round continues
        btns = pg.locator('#ranges button'); await btns.nth(2).click(); await pg.wait_for_timeout(150); await btns.nth(0).click(); await pg.wait_for_timeout(150)
        print('after level switch', await res())
        # solve one correctly via logAttempt path: use r-show? simulate correct: call logAttempt
        await pg.evaluate("logAttempt({mode:'board', task:'x', ok:true, tries:1})"); print('solved', await res())
        await pg.click('#btn-random'); print('next after solved (no skip)', await res())
        for _ in range(6): await pg.click('#btn-random'); await pg.wait_for_timeout(80)
        await pg.wait_for_timeout(1500)
        print('card', await pg.evaluate("document.querySelector('.round-card p')?.textContent"))
        await pg.screenshot(path='skipcard.png')
        # add mode: skip then correct
        await pg.click('[data-round="again"]'); await pg.wait_for_timeout(200)
        await pg.click('[data-mode="add"]'); await pg.wait_for_timeout(200); await pg.click('#btn-random'); print('add skip', await res())
        print('ERR', errs); await b.close()
asyncio.run(main())
