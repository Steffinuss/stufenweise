import asyncio, json
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        pg = await b.new_page(viewport={'width':1180,'height':820}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        topics = await pg.evaluate("sheetTopics().flatMap(([g,o])=>o.map(x=>x[0])).filter(t=>!t.startsWith('K:'))")
        p2 = await b.new_page(viewport={'width':794,'height':1123})
        out=[]
        for t in topics:
            zrs = [10,20,100,1000] if t.startswith('M:') and t not in ('M:einmaleins','M:schriftlich') else [None]
            for zr in zrs:
                for mat in ([True, False] if t in ('M:plus','M:minus','M:ergaenzen','M:stellenwert') and zr in (20,100,1000) else [True]):
                    try:
                        await pg.evaluate(f"Object.assign(app.sheet, {{topic:'{t}', zr:{zr or 20}, n:'fill', mat:{str(mat).lower()}}}); openSheets()")
                        await pg.wait_for_timeout(700)
                        info = await pg.evaluate("({n: app.sheetDoc.n, cols: app.sheetGen?.cols, title: app.sheetDoc.title})")
                        html = await pg.evaluate("app.sheetDoc.html")
                        await p2.emulate_media(media='print'); await p2.set_content(html); await p2.wait_for_timeout(50)
                        r = await p2.evaluate("""(()=>{const pg=document.querySelector('.page'); const mm=pg.getBoundingClientRect().width/186; const h=pg.scrollHeight/mm;
                           const over=[...document.querySelectorAll('.page:first-child .ab-task')].filter(t=>t.scrollWidth>t.clientWidth+2).length;
                           const und=(document.body.innerText.match(/undefined|NaN|\\[object/g)||[]).length; return {h:Math.round(h), over, und}})()""")
                        name=f"{t.replace(':','_')}_{zr}_{'m' if mat else 'o'}"
                        await p2.emulate_media(media='screen'); await p2.set_content(html); await p2.wait_for_timeout(40)
                        await p2.screenshot(path=f'sheets/all_{name}.png', clip={'x':0,'y':0,'width':794,'height':1123})
                        flag = ' <-- PRÜFEN' if r['h']>275 or r['over'] or r['und'] or info['n']<2 else ''
                        out.append(f"{name}: n={info['n']} cols={info['cols']} h={r['h']}mm over={r['over']} und={r['und']} | {info['title']}{flag}")
                        await pg.evaluate("$('#dlg-sheet').close()")
                    except Exception as e:
                        out.append(f"{t} {zr}: EXC {e}")
        print('\n'.join(out)); print('ERR', errs); await b.close()
asyncio.run(main())
