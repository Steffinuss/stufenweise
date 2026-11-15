import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b=await launch(p); pg=await b.new_page(viewport={'width':1180,'height':820}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.click("[data-ctx='practice']"); await pg.click('[data-mode="add"]'); await pg.click('[data-range="20"]')
        await pg.evaluate("(()=>{const t=task(); Object.assign(t,{a:8,b:5,ready:true,draft:['8','5']}); setupRows(t); t.view='field'; renderWork();})()"); await pg.wait_for_timeout(200)
        pr = lambda: pg.evaluate("document.querySelector('#prompt').textContent")
        print('add start:', await pr())
        await pg.click('[data-tfi="11"]'); print('tap 12th:', await pr(), await pg.evaluate("task().fd.dots.join('')"))
        await pg.click('[data-fds="1"]'); print('+1:', await pr())
        await pg.click('[data-fds="1"]'); print('+1 over:', await pr())
        await pg.click('#c-fdundo'); print('undo:', await pr())
        await pg.fill('#guess','13'); await pg.click('#equation #c-check'); await pg.wait_for_timeout(200); print('check:', await pg.evaluate("document.querySelector('#hint').textContent"))
        await pg.screenshot(path='field_add.png')
        await pg.click('[data-mode="sub"]'); await pg.evaluate("(()=>{const t=task(); Object.assign(t,{a:15,b:7,ready:true,draft:['15','7']}); setupRows(t); t.view='field'; renderWork();})()"); await pg.wait_for_timeout(200)
        print('sub start:', await pr()); await pg.click('[data-tfi="8"]'); print('tap 9th:', await pr(), await pg.evaluate("task().fd.cross"))
        await pg.screenshot(path='field_sub.png')
        print('views:', await pg.evaluate("[...document.querySelectorAll('[data-view]')].map(b=>b.textContent.trim()).join(',')"))
        await pg.click('[data-range="100"]'); await pg.wait_for_timeout(200); print('100 views:', await pg.evaluate("[...document.querySelectorAll('[data-view]')].map(b=>b.textContent.trim()).join(',')"))
        print('ERR', errs); await b.close()
asyncio.run(main())
