import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        pg=await b.new_page(viewport={'width':1180,'height':820}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        # Lesen L3: solve items by choosing correct
        await pg.evaluate("leaveMode(); settings.subject='D'; app.mode='read'; Object.assign(app.read,{lvl:'L3',item:null}); render();")
        for i in range(10):
            await pg.evaluate("(()=>{const R=app.read; if(R.item.type==='choice'){R.r.choice=R.item.correct; readCheck();} else { readControl({id:'r-show'}); } })()")
            if i<9: await pg.evaluate("readNew()")
        print('bar', await pg.evaluate("document.querySelectorAll('.workspace > .round-bar i.ok').length"))
        await pg.wait_for_timeout(1800)
        print('end', await pg.evaluate("document.querySelector('.round-end')?.innerText"))
        await pg.screenshot(path='round_end.png')
        await pg.click('[data-round="up"]'); await pg.wait_for_timeout(300)
        print('after up', await pg.evaluate("[app.read.lvl, app.round.res.length, !!document.querySelector('.round-end')]"))
        # Mathe Plus: use logAttempt direct sim
        await pg.evaluate("leaveMode(); settings.subject='M'; app.mode='add'; app.range=20; render(); startRandom();")
        for i in range(10): await pg.evaluate(f"logAttempt({{mode:'add', ok:{'true' if i%3 else 'false'}, tries:{1 if i%3 else 2}}})")
        await pg.wait_for_timeout(1800)
        print('end2', await pg.evaluate("document.querySelector('.round-end')?.innerText"))
        await pg.screenshot(path='round_end2.png')
        await pg.click('[data-round="again"]'); await pg.wait_for_timeout(300)
        print('again', await pg.evaluate("[app.round.res.length, document.querySelectorAll('.workspace > .round-bar i').length]"))
        await pg.screenshot(path='round_bar.png')
        await pg.evaluate("leaveMode(); settings.subject='D'; app.mode='read'; Object.assign(app.read,{lvl:'L9',item:null}); render();")
        await pg.evaluate("(()=>{for(let i=0;i<30;i++){ readNew(); if(qBelow(app.read.item)) return; } })()")
        await pg.screenshot(path='qbelow.png')
        print('ERR', errs); await b.close()
asyncio.run(main())
