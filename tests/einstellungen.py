import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        pg=await b.new_page(viewport={'width':1180,'height':820}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.click('#btn-more'); await pg.click('#btn-settings'); await pg.wait_for_timeout(200)
        vis = await pg.evaluate("!!document.querySelector('[data-key=startCtx]') && document.querySelector('[data-key=startCtx]').offsetParent!==null")
        print('select visible', vis)
        if not vis:
            print(await pg.evaluate("document.querySelector('dialog[open]')?.innerText.slice(0,200)"))
        await pg.select_option('[data-key=startCtx]', 'class'); await pg.select_option('[data-key=roundLen]', '0'); await pg.click('[data-stab=german]'); await pg.select_option('[data-key=kbd]', 'abc')
        await pg.evaluate("document.querySelectorAll('dialog[open]').forEach(d=>d.close())")
        await pg.reload(); await pg.wait_for_timeout(400)
        print('after reload', await pg.evaluate("[app.ctx, app.mode, !!document.querySelector('.ct-tiles'), settings.roundLen, settings.kbd]"))
        await pg.evaluate("setCtx('practice'); leaveMode(); app.mode='add'; app.range=20; render(); startRandom();")
        print('bar with roundLen 0', await pg.evaluate("!!document.querySelector('.workspace > .round-bar')"))
        await pg.evaluate("leaveMode(); app.mode='read'; Object.assign(app.read,{lvl:'W3',item:null}); render()")
        print('abc keys', await pg.evaluate("document.querySelector('.w-keys').className"))
        print('ERR', errs); await b.close()
asyncio.run(main())
