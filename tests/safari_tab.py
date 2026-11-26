"""Hinweis im Safari-Tab auf iPad und iPhone (Backlog P1, Prüfung vom 22.11.2026, Stefan 26.11.2026):
Safari löscht die Daten einer Website nach 7 Tagen mit Safari-Nutzung ohne Besuch; Apps vom Home-Bildschirm sind ausgenommen.
- Im Safari-Tab (iPad, auch iPadOS als „Macintosh“ mit Touch, iPhone) erscheint der Hinweis im Lernstand und in den Einstellungen,
  auf dem Startbildschirm nur, wenn Kinder angelegt sind; dort „Ausblenden (30 Tage)“.
- Mit Kindern steht der Umzugsweg dabei (Sicherung speichern → in der App laden).
- Nicht als Home-Bildschirm-App, nicht in anderen Browsern, nicht beim Üben."""
import asyncio
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

IPAD = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'
IPHONE = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
KID = "() => { const id = newId('p-'); data.profiles.push({id, name:'Mia', created:1, updated:1, world:'HS'}); data.current = id; saveData(); }"

def stand(v):
    return "Object.defineProperty(Navigator.prototype, 'standalone', {get: () => %s, configurable: true});" % v

async def page(br, ua, standalone, touch=5, vp=(1180, 820)):
    ctx = await br.new_context(user_agent=ua, viewport={'width': vp[0], 'height': vp[1]}, has_touch=touch > 0)
    if standalone is not None: await ctx.add_init_script(stand('true' if standalone else 'false'))
    await ctx.add_init_script("Object.defineProperty(Navigator.prototype, 'maxTouchPoints', {get: () => %d, configurable: true});" % touch)
    pg = await ctx.new_page()
    pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
    await pg.goto(URL); await pg.wait_for_timeout(500)
    return ctx, pg

async def start_note(pg):
    await pg.evaluate("() => { app.ctx = null; app.mode = 'home'; render(); }"); await pg.wait_for_timeout(200)
    return await pg.locator('.home .safari-note').count()

async def main():
    async with async_playwright() as p:
        br = await launch(p)
        # iPad im Safari-Tab (meldet sich als Macintosh mit Touch)
        ctx, pg = await page(br, IPAD, False)
        check('iPad-Tab erkannt', await pg.evaluate("safariTab()"))
        check('Start ohne Kinder: kein Hinweis', await start_note(pg) == 0)
        await pg.evaluate(KID)
        check('Start mit Kindern: Hinweis', await start_note(pg) == 1)
        txt = await pg.locator('.home .safari-note').inner_text()
        check('Start: kurzer Text mit Verweis', all(w in txt for w in ['7 Tage', 'Home-Bildschirm', 'Einstellungen → Daten sichern']), txt)
        fits = await pg.evaluate("(() => { const n = document.querySelector('.home .safari-note').getBoundingClientRect(), l = document.querySelector('.home-legal').getBoundingClientRect(); const h = document.querySelector('.home').getBoundingClientRect(); return n.bottom <= h.bottom && l.bottom <= h.bottom + 1 && document.elementFromPoint(n.left + 30, n.bottom - 8)?.closest('.safari-note') != null; })()")
        check('Start: Hinweis ganz sichtbar', fits)
        await pg.screenshot(path='safari_start.png')
        # Lernstand
        n = await pg.evaluate("() => { openStats(); return document.querySelectorAll('#stats-body .safari-note').length; }")
        check('Lernstand: Hinweis', n == 1)
        await pg.evaluate("document.querySelectorAll('dialog[open]').forEach(d => d.close())")
        # Einstellungen
        n = await pg.evaluate("() => { pinSettingsHtml(); return document.querySelector('#safari-note-set .safari-note')?.textContent || ''; }")
        check('Einstellungen: Hinweis mit Umzugsweg', all(w in n for w in ['7 Tage', 'Zum Home-Bildschirm', 'Sicherung speichern', 'Sicherung laden']), n)
        # Ausblenden für 30 Tage, nur auf dem Startbildschirm
        await start_note(pg)
        await pg.click('[data-safari-hide]'); await pg.wait_for_timeout(200)
        check('Ausblenden: weg', await start_note(pg) == 0)
        days = await pg.evaluate("Math.round((settings.safariHide - Date.now())/864e5)")
        check('Ausblenden: 30 Tage', days == 30, str(days))
        n = await pg.evaluate("() => { openStats(); return document.querySelectorAll('#stats-body .safari-note').length; }")
        check('Lernstand zeigt den Hinweis trotzdem', n == 1)
        await pg.evaluate("document.querySelectorAll('dialog[open]').forEach(d => d.close())")
        # nicht beim Üben
        await pg.evaluate("() => { settings.safariHide = 0; app.ctx = 'practice'; app.mode = 'add'; render(); }"); await pg.wait_for_timeout(300)
        check('beim Üben kein Hinweis', await pg.locator('.safari-note:visible').count() == 0)
        await ctx.close()

        # iPhone im Tab
        ctx, pg = await page(br, IPHONE, False, vp=(390, 844))
        check('iPhone-Tab erkannt', await pg.evaluate("safariTab()"))
        await pg.evaluate(KID); await start_note(pg)
        await pg.evaluate("document.querySelector('.home').scrollTop = 1e5"); await pg.wait_for_timeout(100)
        vis = await pg.evaluate("(() => { const b = document.querySelector('[data-safari-hide]').getBoundingClientRect(); return document.elementFromPoint(b.left + b.width/2, b.top + b.height/2)?.closest('[data-safari-hide]') != null; })()")
        check('iPhone: Hinweis erreichbar', vis)
        await pg.screenshot(path='safari_handy.png')
        await ctx.close()
        # Home-Bildschirm-App
        ctx, pg = await page(br, IPAD, True)
        await pg.evaluate(KID)
        check('Home-Bildschirm: nicht erkannt', not await pg.evaluate("safariTab()"))
        check('Home-Bildschirm: kein Hinweis', await start_note(pg) == 0)
        await ctx.close()
        # echter Mac ohne Touch, Chrome auf dem Rechner
        ctx, pg = await page(br, IPAD, None, touch=0)
        check('Mac ohne Touch: nicht erkannt', not await pg.evaluate("safariTab()"))
        await ctx.close()
        ctx = await br.new_context(); pg = await ctx.new_page(); await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.evaluate(KID)
        check('Chrome: nicht erkannt, kein Hinweis', not await pg.evaluate("safariTab()") and await start_note(pg) == 0)
        await ctx.close()
        await br.close()
    print('FEHLER:', ERR) if ERR else print('alles ok')

asyncio.run(main())
