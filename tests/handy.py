"""Handy-Ansicht (0.25.0): brauchbare Demo am Smartphone hochkant.
Startseite zeigt Üben und Unterricht ohne Scrollen, Leiste und Knöpfe oben überlappen nicht,
Aufgabe und Knöpfe liegen nicht übereinander, Zifferntastatur sitzt unten über die ganze Breite,
quer gehalten erscheint der Hinweis „Bitte das Handy hochkant halten“."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

VIS = "(s)=>{const e=document.querySelector(s); if(!e) return false; const r=e.getBoundingClientRect(); return r.top>=0 && r.bottom<=innerHeight && r.left>=0 && r.right<=innerWidth}"
OVER = """()=>{const st=document.querySelector('#stage').getBoundingClientRect(), h=document.querySelector('#hint').getBoundingClientRect(), c=document.querySelector('#controls').getBoundingClientRect();
  const kids=[...document.querySelectorAll('#stage *')].filter(e=>{const r=e.getBoundingClientRect(); return r.height>0 && getComputedStyle(e).visibility!=='hidden'});
  const low=Math.max(...kids.map(e=>e.getBoundingClientRect().bottom), st.bottom);
  return {stageOver: Math.round(low - st.bottom), hintBelow: h.top >= st.bottom - 1, ctlBelow: c.top >= h.bottom - 1, wide: document.documentElement.scrollWidth - innerWidth};}"""

async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        pg = await b.new_page(viewport={'width': 390, 'height': 664}, is_mobile=True, has_touch=True); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        for s in ['[data-ctx="practice"]', '[data-ctx="class"]']:
            if not await pg.evaluate(VIS, s): errs.append(f'Start: {s} nicht ganz sichtbar')
        await pg.click('[data-ctx="practice"]'); await pg.click('[data-home-subj="M"]'); await pg.wait_for_timeout(200)
        r = await pg.evaluate("(()=>{const a=document.querySelector('aside.rail').getBoundingClientRect(), t=document.querySelector('.top-tools').getBoundingClientRect(); return [a.right, t.left]})()")
        if r[0] > r[1] + 1: errs.append(f'Leiste reicht unter Gast/Menü ({r})')
        for m in ['number', 'add', 'sub', 'money', 'written', 'times', 'blitz', 'free']:
            await pg.goto(URL); await pg.wait_for_timeout(200); await pg.click('[data-ctx="practice"]'); await pg.click('[data-home-subj="M"]')
            await pg.click(f'.wz-tile[data-wz-mode="{m}"]'); await pg.wait_for_timeout(200)
            btn = await pg.query_selector('#btn-random')
            if btn and await btn.is_visible(): await btn.click(); await pg.wait_for_timeout(250)
            o = await pg.evaluate(OVER)
            if o['wide'] > 2: errs.append(f'{m}: Seite breiter als Handy ({o["wide"]} px)')
            if not (o['hintBelow'] and o['ctlBelow']): errs.append(f'{m}: Hinweis/Knöpfe liegen über der Aufgabe {o}')
        # Zifferntastatur unten über die ganze Breite
        await pg.goto(URL); await pg.wait_for_timeout(200); await pg.click('[data-ctx="practice"]'); await pg.click('[data-home-subj="M"]'); await pg.click('.wz-tile[data-wz-mode="add"]'); await pg.wait_for_timeout(200)
        await pg.click('#inputs input'); await pg.wait_for_timeout(200)
        np = await pg.evaluate("(()=>{const e=document.getElementById('numpad'); if(!e||e.hidden) return null; const r=e.getBoundingClientRect(); return [r.left, r.right, r.bottom]})()")
        if not np or np[0] > 1 or np[1] < 389 or np[2] < 663: errs.append(f'Zifferntastatur nicht unten über die ganze Breite: {np}')
        await pg.close()
        # quer: Hinweis
        pg = await b.new_page(viewport={'width': 844, 'height': 390}, is_mobile=True, has_touch=True)
        await pg.goto(URL); await pg.wait_for_timeout(300)
        if not await pg.evaluate("getComputedStyle(document.querySelector('.rotate-hint')).display!=='none'"): errs.append('quer: kein Hinweis zum Drehen')
        await pg.close()
        # iPad bleibt unverändert: kein Hinweis, kein Scrollen der Seite
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}, has_touch=True)
        await pg.goto(URL); await pg.wait_for_timeout(300)
        if await pg.evaluate("getComputedStyle(document.querySelector('.rotate-hint')).display!=='none'"): errs.append('iPad: Dreh-Hinweis sichtbar')
        if await pg.evaluate("document.documentElement.scrollHeight > innerHeight + 2"): errs.append('iPad: Seite scrollt')
        await pg.close()
        print('ERR', errs); await b.close()
asyncio.run(main())
