import asyncio, subprocess
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        pg=await b.new_page(viewport={'width':1180,'height':820}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.evaluate("app.heft.items=[]; app.sheet.topic='H:HT'; openSheets('none')"); await pg.wait_for_timeout(1200)
        print(await pg.evaluate("app.sheetDoc.title+' '+(app.sheetDoc.html.match(/class=\"page\"/g)||[]).length+' sol:'+app.sheetDoc.html.includes('page sol')"))
        await pg.screenshot(path='ht_dlg.png')
        await pg.click('#sh-samml'); await pg.wait_for_timeout(300)
        print('Blattsammlung', await pg.evaluate("app.samml.items.map(i=>i.title+' '+(i.html.match(/class=\"page/g)||[]).length).join(' | ')"))
        await pg.select_option('#sh-htp','6'); await pg.wait_for_timeout(1200)
        print(await pg.evaluate("app.sheetDoc.title+' '+/701/.test(app.sheetDoc.html)"))
        await pg.select_option('#sh-htp','0'); await pg.wait_for_timeout(1200)
        print(await pg.evaluate("app.sheetDoc.title+' has1:'+/>1</.test(app.sheetDoc.html)"))
        html = await pg.evaluate("(app.sheet.htp='all', buildSheet().html)")
        p2=await b.new_page(); await p2.set_content(html); await p2.wait_for_timeout(300)
        await p2.pdf(path='tb.pdf', format='A4', prefer_css_page_size=True)
        print(subprocess.run(['pdfinfo','tb.pdf'],capture_output=True,text=True).stdout.split('Pages:')[1].split()[0])
        # trace sheet
        await pg.evaluate("$('#dlg-sheet').close(); app.sheet.topic='W:WX'; app.sheet.htp='all'; openSheets('none')"); await pg.wait_for_timeout(1800)
        html = await pg.evaluate("app.sheetDoc.html")
        p3=await b.new_page(viewport={'width':800,'height':500}); await p3.set_content(html.replace('Montag','Name')); await p3.wait_for_timeout(500)
        await p3.screenshot(path='trace.png')
        await p3.pdf(path='trace.pdf', format='A4', prefer_css_page_size=True)
        print('ERR', errs); await b.close()
asyncio.run(main())
