from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
# usage: python3 -I shot.py out.png "js1" ["js2" ...]  (each js evaluated, then 600ms wait)
import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    out, js = sys.argv[1], sys.argv[2:]
    async with async_playwright() as p:
        b=await launch(p)
        W,H = (1180,820)
        if out.startswith('P'): W,H=(820,1180); out=out[1:]
        elif out.startswith('I'): W,H=(1080,810); out=out[1:]
        elif out.startswith('J'): W,H=(1148,802); out=out[1:]
        pg=await b.new_page(viewport={'width':W,'height':H}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        for j in js:
            if j.startswith('CLICK '): await pg.click(j[6:])
            elif j.startswith('FILL '): sel,val=j[5:].split('=',1); await pg.fill(sel,val)
            else:
                r = await pg.evaluate(j)
                if r is not None: print('=>', str(r)[:2000])
            await pg.wait_for_timeout(500)
        await pg.screenshot(path=out)
        print('ERR', errs); await b.close()
asyncio.run(main())
