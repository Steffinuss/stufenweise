import asyncio, sys
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        for vw in [(1180,820),(820,1180),(390,844)]:
            pg=await b.new_page(viewport={'width':vw[0],'height':vw[1]}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(400)
            out=[]
            for m in ['tfield','nline']:
                ok = await pg.evaluate(f"TOOL_MODES.includes('{m}')")
                if not ok: out.append(m+':n/a'); continue
                await pg.evaluate(f"app.ctx='class'; leaveMode?.(); app.mode='{m}'; render()"); await pg.wait_for_timeout(150)
                y0 = await pg.evaluate("Math.round(document.querySelector('#stage').getBoundingClientRect().top)")
                if m=='tfield':
                    await pg.evaluate("document.querySelector('[data-tfk=\"1\"]').click()"); await pg.wait_for_timeout(100)
                    y1 = await pg.evaluate("Math.round(document.querySelector('#stage').getBoundingClientRect().top)")
                    await pg.evaluate("app.tf.hide=true; app.tf.shown=false; document.querySelector('[data-tft=\"o\"]').click(); document.querySelector('[data-tfk=\"5\"]').click()"); await pg.wait_for_timeout(100)
                    y2 = await pg.evaluate("Math.round(document.querySelector('#stage').getBoundingClientRect().top)")
                    out.append(f'tfield {y0} {y1} {y2}')
                else:
                    out.append(f'nline {y0}')
            print(vw, out, errs); await pg.close()
        await b.close()
asyncio.run(main())
