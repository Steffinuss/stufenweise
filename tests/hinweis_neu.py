import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        pg=await b.new_page(viewport={'width':1180,'height':820}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.click("[data-ctx='practice']"); await pg.wait_for_timeout(300)
        for lvl in ['G1','G2','G3','G4','U1','L4','H1']:
            r = await pg.evaluate(f"""(()=>{{leaveMode?.(); app.mode='read'; app.read.lvl='{lvl}'; app.read.item=null; render();
              const R=app.read, it=R.item; R.fb={{ok:true}}; setHint('Richtig!','ok'); renderRead();
              const before=$('#hint').textContent; document.querySelector('#btn-random').click();
              return before+' -> ['+$('#hint').textContent+']'}})()""")
            print(lvl, r)
        # other modes: money / add via randomAny
        for m in ['add','money','times','written','number']:
            r = await pg.evaluate(f"""(()=>{{leaveMode?.(); app.mode='{m}'; render(); setHint('Richtig!','ok'); const rb=document.querySelector('#btn-random'); if(rb.hidden) return 'hidden'; rb.click(); return '['+$('#hint').textContent+']'}})()""")
            print(m, r)
        print('ERR', errs); await b.close()
asyncio.run(main())
