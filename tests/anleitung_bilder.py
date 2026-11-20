import asyncio, sys
from simlib import answer, math_skill
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
OUT='anleitung/'
async def main():
    async with async_playwright() as p:
        b = await launch(p, args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width':1180,'height':820}, has_touch=True, device_scale_factor=1.5)
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(600)
        import json
        HL={}
        async def shot(n, wait=350, hl=None):
            await pg.wait_for_timeout(wait)
            if hl:
                bb = await pg.locator(hl).first.bounding_box(); HL[n]=bb
            await pg.screenshot(path=OUT+n+'.png')
        await shot('01_start')
        TB={}
        for sel,lab in [('#btn-home','Startseite'),('#btn-profile','Kind wählen'),('#btn-stats','Lernstand'),('#btn-sheet','Arbeitsblätter'),('#btn-fb','Rückmeldung'),('#btn-help','Anleitung'),('#btn-full','Vollbild'),('#btn-settings','Einstellungen')]:
            TB[lab]=await pg.locator(sel).bounding_box()
        HL['_toolbar']=TB
        # Einstellungen / PIN
        await pg.click('#btn-more'); await pg.click('#btn-settings'); await pg.wait_for_timeout(300)
        await pg.click('[data-stab="kids"]'); await pg.wait_for_timeout(200)
        await pg.evaluate("[...document.querySelectorAll('#dlg-settings legend')].find(l=>l.textContent.includes('PIN')).scrollIntoView({block:'center'})")
        await shot('02_pin', hl='#dlg-settings fieldset:has(legend:text("Lehrkraft-PIN"))')
        await pg.click('#dlg-settings [data-close]')
        # Kind anlegen
        await pg.click('#btn-profile'); await pg.wait_for_timeout(300)
        if await pg.locator('#privacy-ok').count(): await pg.click('#privacy-ok'); await pg.wait_for_timeout(200)
        await pg.fill('#pname', 'Testkind A')
        await shot('03_kind', hl='#padd')
        await pg.click('#padd button[type=submit]'); await pg.wait_for_timeout(300)
        await pg.click('#dlg-profile [data-close]'); await pg.wait_for_timeout(200)
        # Testen: Startseite → Testen → Kind → Test (seit 0.29.0 ein eigener Eingang)
        await pg.click('#btn-home'); await pg.wait_for_timeout(300)
        if await pg.locator('[data-ctx-reset]').count(): await pg.click('[data-ctx-reset]'); await pg.wait_for_timeout(300)
        await pg.click('[data-ctx-test]'); await pg.wait_for_timeout(300)
        await pg.click('[data-home-pick]'); await pg.wait_for_timeout(300)
        await shot('04_tests', hl='[data-tstart="M1"]')
        await pg.click('[data-tstart="M1"]'); await pg.wait_for_timeout(300)
        await shot('05_intro', hl='#d-start')
        await pg.click('#d-start')
        skill = math_skill({10:5,20:3,100:0,1000:0},0,2,2)
        took=False
        for step in range(80):
            if await pg.evaluate("app.diag.done"): break
            info = await pg.evaluate("(()=>{const d=app.diag,it=d.items[d.idx];return {key:d.key,type:it.type}})()")
            if not took and info['type'] in ('input','build','choice') and step>=1:
                took=True; await shot('06_aufgabe', 500, hl='#d-skip, button:has-text("Weiß ich nicht")')
            await answer(pg, skill(info['key'])); await pg.wait_for_timeout(80)
        await shot('07_fertig', 600, hl='button:has-text("Lernstand (Lehrkraft)")')
        await pg.click('#d-close'); await pg.wait_for_timeout(300)
        # Teil 2
        await pg.evaluate("diagStart('M2', false)"); await pg.wait_for_timeout(200); await pg.click('#d-start')
        for step in range(200):
            if await pg.evaluate("app.diag.done"): break
            info = await pg.evaluate("(()=>{const d=app.diag;return {key:d.key,type:d.items[d.idx].type}})()")
            if info['type'] in ('input','flash','scatter','seq','clockset','write','sent','choice','pairs','line','money','build'): await answer(pg, skill(info['key']))
            else: await pg.click('#d-skip')  # Aufgabenarten, die simlib nicht kennt (z. B. Hundertertafel): „Weiß ich nicht“
            await pg.wait_for_timeout(60)
        print('Teil 2 fertig:', await pg.evaluate("app.diag?.done"))
        await pg.click('#d-close'); await pg.wait_for_timeout(300)
        print('Modus:', await pg.evaluate("app.mode"))
        # Lernstand
        await pg.click('#btn-more'); await pg.click('#btn-stats'); await pg.wait_for_timeout(500)
        await shot('08_lernstand')
        print(await pg.evaluate("[...document.querySelectorAll('#dlg-stats *')].filter(e=>e.children.length===0 && /Förderzone|ILEB|Ganze Klasse|Bericht/.test(e.textContent)).slice(0,25).map(e=>e.tagName+'.'+e.className+': '+e.textContent.trim().slice(0,60))"))
        async def scrollto(rx):
            ok = await pg.evaluate("(rx)=>{const r=new RegExp(rx);const e=[...document.querySelectorAll('#dlg-stats h3,#dlg-stats h4,#dlg-stats summary,#dlg-stats b,#dlg-stats strong,#dlg-stats .zt,#dlg-stats legend')].find(e=>r.test(e.textContent));if(e){e.scrollIntoView({block:'start'});return e.tagName+':'+e.textContent.slice(0,50)}return null}", rx)
            print('scroll', rx, ok)
        await scrollto('^Förderzone'); await shot('09_foerderzone')
        await scrollto('ILEB'); await shot('10_ileb')
        await pg.click('#dlg-stats [data-close]'); await pg.wait_for_timeout(300)
        await pg.click('#btn-home'); await pg.wait_for_timeout(300)
        if await pg.locator("[data-ctx='practice']").count(): await pg.click("[data-ctx='practice']"); await pg.wait_for_timeout(300)
        if await pg.locator('[data-home-pick]').count(): await pg.click('[data-home-pick]'); await pg.wait_for_timeout(300)
        await shot('11_heute', 500, hl='.home-card')
        await pg.click('.home-card'); await shot('12_ueben', 600)
        await pg.click('#btn-more'); await pg.click('#btn-sheet'); await pg.wait_for_timeout(900)
        await pg.evaluate("const b=[...document.querySelectorAll('#dlg-sheet button')].find(b=>b.textContent.trim()==='Drucken'); b.id='hl-print'; b.scrollIntoView({block:'center', behavior:'instant'})"); await pg.wait_for_timeout(600)
        await shot('13_arbeitsblatt', 500, hl='#hl-print')
        await pg.click('#dlg-sheet [data-close]'); await pg.wait_for_timeout(300)
        await pg.click('#btn-more'); await pg.click('#btn-fb'); await pg.wait_for_timeout(300)
        await pg.click('[data-fbart]') if await pg.locator('[data-fbart]').count() else None
        await pg.evaluate("document.querySelector('#fb-gh').scrollIntoView({block:'center'})")
        await shot('14_rueckmeldung', 400, hl='#fb-gh')
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
        await pg.click('#btn-more'); await pg.click('#btn-help'); await pg.wait_for_timeout(300)
        await pg.evaluate("[...document.querySelectorAll('#dlg-help *')].filter(e=>e.textContent.trim().startsWith('Freie Software') && e.textContent.trim().length<20).pop().scrollIntoView({block:'start', behavior:'instant'})"); await pg.wait_for_timeout(500)
        await shot('15_lizenz')
        # Materialkiste (seit 0.30.0): Startseite → Materialkiste → Kind → Taschenrechner mit Ergebnis als Material
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
        await pg.click('#btn-home'); await pg.wait_for_timeout(300)
        if await pg.locator('[data-ctx-reset]').count(): await pg.click('[data-ctx-reset]'); await pg.wait_for_timeout(300)
        await pg.click('[data-ctx-kiste]'); await pg.wait_for_timeout(200)
        if await pg.locator('.home-names [data-home-pick]').count(): await pg.click('.home-names [data-home-pick]:not([data-home-pick=""])'); await pg.wait_for_timeout(200)
        await pg.click('.ct-tile[data-kiste="tcalc"]'); await pg.wait_for_timeout(200)
        for k in ['1', '2', '3', '4', '*', '3', '=']: await pg.click(f'[data-trk="{k}"]')
        await pg.mouse.move(5, 800)
        await shot('16_materialkiste', 400, hl='.rail [data-kiste="tcalc"]')
        json.dump(HL, open(OUT+'hl.json','w'))
        await b.close(); print('ERR', errs)
asyncio.run(main())
