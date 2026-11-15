import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
SEED = """(()=>{data.profiles.push({id:'k1',name:'Mia'}); data.current='k1'; const L=data.log.k1=[]; const now=Date.now();
for(let d=6; d>=0; d--){ if(d===3) continue; let t=now-d*864e5-3*3600e3; for(let i=0;i<8+d*2;i++){ t+=40000+Math.random()*60000; const m=['add','sub','read','times'][i%4]; L.push({ts:t, mode:m, range:20, lvl: m==='read'?'L4':undefined, task:'x'+i, ok: Math.random()<(m==='sub'?.45:.9), tries:1}); } }
data.skips={k1:[{ts:now-864e5, mode:'sub', task:'32 − 7'},{ts:now-2*864e5, mode:'read', task:'Tafel: 45 finden'}]}; saveData(); return L.length})()"""
async def main():
    async with async_playwright() as p:
        b=await launch(p); pg=await b.new_page(viewport={'width':1180,'height':820}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        print(await pg.evaluate(SEED))
        html = await pg.evaluate("buildReport('k1','week').html")
        p2 = await b.new_page(viewport={'width':820,'height':1160}); await p2.set_content(html); await p2.wait_for_timeout(200); await p2.screenshot(path='week.png', full_page=True)
        print(await pg.evaluate("statsSections('k1').map(s=>s.title+': '+s.lines.join(' / ')).filter(x=>x.startsWith('Übersp')).join('\\n')"))
        await pg.evaluate("openReport('k1')"); await pg.wait_for_timeout(300); await pg.click('[data-rk="week"]'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='week_dlg.png')
        print('ERR', errs); await b.close()
asyncio.run(main())
