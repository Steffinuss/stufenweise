import asyncio
from playwright.async_api import async_playwright
from common import URL, launch, FOKUS_AUS  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b=await launch(p); pg=await b.new_page(viewport={'width':1180,'height':820}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script(FOKUS_AUS); await pg.goto(URL); await pg.wait_for_timeout(300)
        bar = lambda: pg.locator('.upd-bar').count()
        await pg.evaluate("data.profiles.push({id:'k1',name:'Mia'}); saveData(); UPD.found={version:'9.9.9'}; render();"); await pg.wait_for_timeout(100)
        print('chooser:', await bar())
        await pg.click("[data-ctx='practice']"); await pg.wait_for_timeout(100); print('who step:', await bar())
        await pg.click("[data-home-pick='k1']"); await pg.wait_for_timeout(100); print('kid chosen (subject step):', await bar())
        await pg.click('[data-mode="add"]'); await pg.wait_for_timeout(100); print('practicing:', await bar())
        await pg.evaluate("checkUpdate=async()=>{}; "); 
        await pg.evaluate("setCtx(null)"); await pg.wait_for_timeout(100); print('back to chooser:', await bar())
        await pg.click("[data-ctx='class']"); await pg.wait_for_timeout(100); print('class home:', await bar())
        await pg.click(".wz-body [data-ctool='nline']"); await pg.wait_for_timeout(100); print('class tool:', await bar())
        print('ERR', errs); await b.close()
asyncio.run(main())
