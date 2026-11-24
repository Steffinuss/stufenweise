"""Stefan 24.11.: Test „mit Material“ (Rechnen R1–R7), Plus/Minus und Einmaleins beim Üben bis „im Kopf“,
Geld im Test auch ziehen, Runden-Punkte bei „Mengen legen und abzählen“."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch

def check(ok, msg):
    if not ok: raise AssertionError(msg)
    print('ok', msg)

async def main():
    async with async_playwright() as p:
        b = await launch(p); ctx = await b.new_context(viewport={'width':1180, 'height':820})
        pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        # Test: ohne Material falsch, mit Material richtig → teilweise, mat erreicht
        for key in ['R|R1', 'R|R5', 'R|R7']:
            await pg.evaluate(f"diagStart('M'); const d=app.diag; d.started=true; d.key='{key}'; d.items=itemsFor('{key}').map(g=>g()); d.idx=0; d.answers=[]; d.resp=null; d.gen=(function*(){{}})(); renderDiag()")
            await pg.evaluate("diagAnswer(true)"); await pg.evaluate("diagAnswer(true)")
            check(await pg.evaluate("!!app.diag.items[app.diag.idx].mat"), f'{key}: danach Aufgaben mit Material')
            for k in range(3):
                it = await pg.evaluate("app.diag.done || !app.diag.items[app.diag.idx]?.mat ? null : app.diag.items[app.diag.idx]")
                if not it: break
                if it['type'] == 'build':
                    t = it['target']; await pg.evaluate(f"app.diag.resp={{mat:[{t//10},{t%10}]}}; diagAnswer(false)")
                else:
                    await pg.evaluate(f"document.querySelector('#stage .dg-in').value='{it['fields'][0]}'; diagAnswer(false)")
            c = await pg.evaluate(f"matrixOf('guest')['{key}']")
            check(c['status'] == 'teilweise' and c.get('mat') == 'erreicht', f'{key}: „mit Material erreicht“')
        # Geld im Test ziehen
        await pg.evaluate("diagStart('M'); app.diag.started=true; app.diag.key='M|20|I'; app.diag.items=[{type:'money', target:1300, denoms:[1000,500,200,100], prompt:'Lege 13 €.', label:'13 € legen'}]; app.diag.idx=0; app.diag.resp=null; renderDiag()")
        bb = await pg.locator('[data-dgden="1000"]').bounding_box(); tb = await pg.locator('#stage .mtable').bounding_box()
        await pg.mouse.move(bb['x'] + 20, bb['y'] + 20); await pg.mouse.down()
        for i in range(8): await pg.mouse.move(bb['x'] + 20, bb['y'] - i*25)
        await pg.mouse.move(tb['x'] + tb['width']/2, tb['y'] + tb['height']/2); await pg.mouse.up(); await pg.wait_for_timeout(200)
        check(await pg.evaluate("app.diag.resp.items.join()") == '1000', 'Test: Geldschein ziehen legt ihn hin')
        await pg.evaluate("app.diag = null; goHome()")
        # Plus/Minus: letzte Darstellung „im Kopf“
        await pg.evaluate("app.ctx='practice'; settings.subject='M'; app.range=20; app.mode='add'; app.calc=false; pmMem().v = pmViews().length - 1; app.tasks.add = blankTask(); render()")
        await pg.evaluate("document.querySelector('#btn-random')?.click()"); await pg.wait_for_timeout(200)
        check(await pg.evaluate("task().view === 'none' && !!document.querySelector('#stage .pm-none') && !!document.querySelector('#guess')"), 'Plus/Minus: Stufe „Im Kopf“ ohne Bild')
        # Einmaleins: nach 8 richtigen im Kopf
        await pg.evaluate("app.mode='times'; timesRandom()")
        for i in range(8):
            await pg.evaluate("const t=app.times; document.querySelector('#guess').value=String(t.a*t.b); timesCheck(); timesRandom()")
        check(await pg.evaluate("tmKopf() && !!document.querySelector('#stage .pm-none')"), 'Einmaleins: nach 8 richtigen im Kopf')
        await pg.evaluate("document.querySelector('#t-pic').click()")
        check(await pg.evaluate("!document.querySelector('#stage .pm-none')"), 'Einmaleins: „Bild zeigen“ zeigt das Punktebild')
        # Runden-Punkte bei der Zählaufgabe
        await pg.evaluate("app.mode='number'; app.range=10; render()"); await pg.wait_for_timeout(200)
        if await pg.evaluate("!task().ready"): await pg.evaluate("document.querySelector('#btn-random')?.click()")
        await pg.wait_for_timeout(200)
        check(await pg.evaluate("countOn(task()) && roundOn() && /Aufgabe \\d+ von/.test(document.querySelector('#fokus-bar').innerText)"), 'Zählaufgabe: „Aufgabe … von …“ oben')
        print('ERR', errs)
        await b.close()

asyncio.run(main())
