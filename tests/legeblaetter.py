import asyncio, subprocess, sys
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
CASES = [('zehner','plus',None),('zehner','none',None),('zwanzig','plus',None),('zwanzig','ergaenz',None),('strahl20','zahl',None),('strahl20','abstand',None),('strahl100','plus',100),('strahl100','zahl',1000),
 ('hundert','zahl',None),('hundert','mal',None),('stellen','zahl',100),('stellen','plus',1000),('stellen','zahl',1000),('stellen','minus',100),('geld','zahl',20),('geld','zahl',100),('uhr','zeit',None),('uhrm','zeit',None),
 ('anlaut','zahl',None),('wort','zahl',None),('wortv','zahl',None),('wortm','zahl',None),('silben','zahl',None),('buchst','zahl',None)]
only = sys.argv[1:]
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        pg=await b.new_page(viewport={'width':1180,'height':820}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        for key,kt,zr in CASES:
            if only and key not in only: continue
            html = await pg.evaluate(f"(()=>{{app.sheet.topic='K:{key}'; app.sheet.kt='{kt}'; {'app.sheet.zr='+str(zr)+';' if zr else ''} app.sheet.sol=false; return buildSheet().html}})()")
            p2=await b.new_page(); await p2.set_content(html); await p2.wait_for_timeout(300)
            name=f"{key}-{kt}-{zr or ''}"
            # overflow check: in print media, the .q content height vs available
            await p2.emulate_media(media='print')
            ov = await p2.evaluate("(()=>{const q=document.querySelector('.page.lg .q'); const kids=[...q.children]; const last=kids[kids.length-1].getBoundingClientRect(); const top=q.getBoundingClientRect(); return {used:Math.round((last.bottom-top.top)/3.7795), avail:Math.round(q.getBoundingClientRect().height/3.7795), scroll:Math.round(q.scrollHeight/3.7795), w:Math.round(q.scrollWidth/3.7795)}})()")
            await p2.pdf(path=f'lege/{name}.pdf', format='A4', prefer_css_page_size=True)
            n = subprocess.run(['pdfinfo', f'lege/{name}.pdf'],capture_output=True,text=True).stdout
            pages=[l for l in n.splitlines() if l.startswith('Pages')][0].split()[-1]
            subprocess.run(['pdftoppm','-png','-r','45','-f','1','-l','1',f'lege/{name}.pdf',f'lege/{name}'])
            print(name, 'pages', pages, ov, flush=True)
            await p2.close()
        print('ERR', errs); await b.close()
asyncio.run(main())
