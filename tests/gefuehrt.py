import asyncio, json
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        pg=await b.new_page(viewport={'width':1180,'height':820}); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.evaluate("""(()=>{data.profiles.push({id:'p1',name:'Ali'}); data.current='p1';
          const set=(k,st)=>setCell('p1',k,{status:st,quelle:'test',sum:''});
          ['M|10|I','M|10|II','M|10|III','M|10|IV','M|20|I','M|20|II'].forEach(k=>set(k,'erreicht')); set('M|20|III','nicht'); set('M|100|I','nicht');
          set('U|U1','erreicht'); set('U|U2','nicht');
          ['L|L1','L|L2','L|L3'].forEach(k=>set(k,'erreicht')); set('L|L4','teilweise'); set('W|W1','erreicht'); set('W|W2','nicht'); saveData(); })()""")
        rail = "[...document.querySelectorAll('#modes button')].map(b=>b.textContent.trim()).join(' | ')"
        rng = "[...document.querySelectorAll('#ranges button')].map(b=>b.textContent.trim()).join(',')"
        for gm in ['zone','plus','all']:
            await pg.evaluate(f"settings.guide='{gm}'; saveSettings(); setSubject('M')"); await pg.wait_for_timeout(200)
            print(gm,'M:', await pg.evaluate(rail)); 
            await pg.click('[data-mode="number"]') if await pg.locator('#modes [data-mode="number"]').count() else None
            await pg.wait_for_timeout(150); print('   ranges:', await pg.evaluate(rng))
            await pg.evaluate("setSubject('D')"); await pg.wait_for_timeout(200)
            print(gm,'D:', await pg.evaluate(rail))
            await pg.screenshot(path=f'gd_{gm}.png')
        await pg.evaluate("settings.guide='plus'; saveSettings(); setSubject('M')"); await pg.wait_for_timeout(200)
        await pg.screenshot(path='gd_M_plus.png')
        # teacher unlock (no pin)
        await pg.click('[data-guide-all]'); await pg.wait_for_timeout(200); print('teacher:', await pg.evaluate(rail))
        await pg.click('[data-guide-off]'); await pg.wait_for_timeout(200)
        # level-up: read L4 10 correct
        await pg.evaluate("setSubject('D')"); await pg.click('#modes [data-lvl="L4"]'); await pg.wait_for_timeout(200)
        for i in range(10):
            await pg.evaluate("logAttempt({mode:'read', task:'x', ok:true, tries:1})")
        await pg.wait_for_timeout(1700); await pg.screenshot(path='gd_lvlup.png')
        print('round-end', await pg.locator('.round-end').count(), await pg.evaluate("document.querySelector('.round-end')?.innerText.replace(/\\n+/g,' | ')"))
        await pg.click('[data-round="kurz"]'); await pg.wait_for_timeout(200); await pg.screenshot(path='gd_kurz0.png')
        await pg.click('#d-start'); await pg.wait_for_timeout(200)
        for i in range(3):
            if not await pg.evaluate("app.diag && !app.diag.done"): break
            t=await pg.evaluate("app.diag.items[app.diag.idx].type")
            if t=='choice':
                c=await pg.evaluate("app.diag.items[app.diag.idx].correct"); await pg.click(f'[data-dgc="{c}"]'); await pg.click('#d-next')
            else: print('type',t); break
            await pg.wait_for_timeout(200)
        await pg.screenshot(path='gd_kurz1.png')
        print('L4 now', await pg.evaluate("JSON.stringify(matrixOf('p1')['L|L4'])"))
        await pg.click('#d-close'); await pg.wait_for_timeout(150)
        if await pg.evaluate("!!app.diag && !app.diag.done && app.mode==='diag'"): await pg.click('#d-close'); await pg.wait_for_timeout(150)  # im laufenden Test: zweimal tippen
        print('after D:', await pg.evaluate(rail))
        print(errs); await b.close()
asyncio.run(main())
