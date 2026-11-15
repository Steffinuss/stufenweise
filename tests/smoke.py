import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b = await launch(p, args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width':1280,'height':800})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.wait_for_timeout(300)
        if await pg.locator("[data-ctx='practice']").count(): await pg.click("[data-ctx='practice']")
        await pg.screenshot(path='h1.png')
        await pg.evaluate("data.profiles.push({id:'pA',name:'Ali'},{id:'pB',name:'Bea'}); saveData(); render()")
        await pg.screenshot(path='h2.png')
        await pg.click('[data-home-pick="pA"]'); await pg.wait_for_timeout(200); await pg.screenshot(path='h3.png')
        await pg.click('[data-home-subj="D"]'); await pg.wait_for_timeout(200)
        await pg.click('[data-wz-lvl="W3"]'); await pg.wait_for_timeout(200); await pg.screenshot(path='w3.png')
        t = await pg.evaluate("app.read.item.target")
        await pg.keyboard.type(t.lower()[:-1]); await pg.wait_for_timeout(100)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200); await pg.screenshot(path='w3b.png')
        await pg.click('[data-lvl="W1"]'); await pg.wait_for_timeout(200); await pg.screenshot(path='w1.png')
        await pg.click('[data-lvl="W6"]'); await pg.wait_for_timeout(200)
        for i in range(4):
            if await pg.evaluate("app.read.item.type")=='sent': break
            await pg.click('#r-show') if await pg.locator('#r-show').count() else None
            await pg.evaluate("app.read.item=null; renderRead()")
        await pg.screenshot(path='w6.png')
        # PIN
        await pg.evaluate("settings.pin=pinHash('1234'); app.teacherUntil=0; saveSettings()")
        await pg.click('#btn-more'); await pg.click('#btn-stats'); await pg.wait_for_timeout(200); await pg.screenshot(path='pin.png')
        for d in '1235': await pg.click(f'[data-pin="{d}"]')
        await pg.wait_for_timeout(300)
        for d in '1234': await pg.click(f'[data-pin="{d}"]')
        await pg.wait_for_timeout(300)
        print('stats open', await pg.evaluate("$('#dlg-stats').open"))
        await pg.keyboard.press('Escape')
        await pg.click('#btn-more'); await pg.click('#btn-settings'); await pg.wait_for_timeout(200)
        await pg.evaluate("$('#dlg-settings').scrollTop=9999"); await pg.screenshot(path='set.png')
        print('ERR', errs)
        await b.close()
asyncio.run(main())
