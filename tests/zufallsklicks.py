import asyncio, random
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    random.seed(41)
    async with async_playwright() as p:
        b=await launch(p)
        for vp in [(1180,820),(820,1180),(1920,1080)]:
            pg=await b.new_page(viewport={'width':vp[0],'height':vp[1]}); errs=[]
            last=['']; pg.on('pageerror', lambda e: errs.append((last[0], (e.stack or str(e))[:500]))); pg.on('dialog', lambda d: asyncio.ensure_future(d.dismiss()))
            await pg.goto(URL); await pg.wait_for_timeout(400); await pg.evaluate("data.profiles=[{id:'g',name:'Gina',world:'GS',sym:'Fisch',pic:true},{id:'b',name:'Bea',world:'BSS'}]; data.current='g'; app.ctx='practice'; render()")
            n=0
            for i in range(700):
                # close open dialogs sometimes
                if await pg.evaluate("!!document.querySelector('dialog[open]')"):
                    await pg.evaluate("document.querySelectorAll('dialog[open]').forEach(d=>d.close())")
                sel = await pg.evaluate("""(()=>{const bs=[...document.querySelectorAll('button:not([disabled]), [data-hb2], [data-wkey], .mden, [data-dgden], [data-dgc]')].filter(b=>{const r=b.getBoundingClientRect(); return r.width>0&&r.height>0&&r.top>=0&&r.bottom<=innerHeight && !b.closest('dialog') && !/btn-fb|btn-help|btn-sheet|btn-full|data-legal|b-backup|btn-settings|btn-profile|btn-stats/.test(b.outerHTML.slice(0,120))});
                  if(!bs.length) return null; const b=bs[Math.floor(Math.random()*bs.length)]; b.setAttribute('data-mk','1'); return b.textContent.trim().slice(0,20)||b.getAttribute('aria-label')})()""")
                if sel is None: continue
                last[0]=f'{sel} @ ' + await pg.evaluate("app.mode+'/'+(app.read&&app.read.lvl)")
                try:
                    await pg.click('[data-mk="1"]', timeout=1500); n+=1
                except Exception: pass
                await pg.evaluate("document.querySelectorAll('[data-mk]').forEach(e=>e.removeAttribute('data-mk'))")
                if i%50==0:
                    # tap randomly on svg stage areas too
                    st = await pg.locator('#stage').bounding_box()
                    if st: await pg.mouse.click(st['x']+random.random()*st['width'], st['y']+random.random()*st['height'])
                if i%120==119: await pg.evaluate("goHome()")
            print(vp, 'clicks', n, 'mode', await pg.evaluate("app.mode+'/'+app.ctx"), 'ERR', errs[:2])
            await pg.close()
        await b.close()
asyncio.run(main())
