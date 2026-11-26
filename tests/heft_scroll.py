"""Heft-Assistent: „+“ und „−“ bei den Kapiteln springen nicht nach oben (Rückmeldung Stefan, 26.11.2026).
Der Dialog „Material drucken“ wird bei jeder Änderung neu gezeichnet; die Scrollposition bleibt erhalten.
Beim Öffnen des Dialogs beginnt er oben. Geprüft auf iPad-Größe und Handy-Größe."""
import asyncio
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

KID = """() => { const id = newId('p-'); data.profiles.push({id, name:'Mia', created:1, updated:1, world:'HS'}); data.current = id;
  for(const k of ['M|10|I', 'R|R1', 'R|R2', 'U|U1', 'G|G1', 'H|H1', 'L|L1', 'L|L2', 'L|L3', 'L|L4', 'L|L5', 'L|L6', 'L|L7', 'L|L8']) setCell(id, k, {status:'erreicht', quelle:'test', sum:''});
  for(const k of ['M|10|II', 'R|R3', 'Z|Z1', 'U|U2', 'G|G2', 'H|H2', 'L|L9']) setCell(id, k, {status:'teilweise', quelle:'test', sum:''});
  saveData(); return id; }"""
SCROLLER = """() => { for(const e of [document.querySelector('.sheet-form'), document.querySelector('#sheet-body'), document.querySelector('#dlg-sheet')]) if(e && e.scrollHeight > e.clientHeight + 5 && getComputedStyle(e).overflowY !== 'visible') return e === document.querySelector('.sheet-form') ? '.sheet-form' : '#' + e.id; return null; }"""

async def main():
    async with async_playwright() as p:
        br = await launch(p)
        for w, h in [(1180, 820), (390, 844)]:
            pg = await br.new_page(viewport={'width': w, 'height': h})
            pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
            await pg.goto(URL); await pg.wait_for_timeout(500)
            pid = await pg.evaluate(KID)
            await pg.evaluate("pid => { app.heft = {title:'Mein Arbeitsheft', pid, items:[], toc:true, fach:'mix', pages:48}; saveHeft(); openHeftZone(pid); }", pid)
            await pg.wait_for_timeout(500)
            sc = await pg.evaluate(SCROLLER)
            check(f'{w}: Dialog scrollt', sc is not None, str(sc))
            if not sc: continue
            last = pg.locator('[data-hfadj][data-d="1"]:not([disabled])').last
            await last.scroll_into_view_if_needed(); await pg.wait_for_timeout(200)
            before = await pg.evaluate(f"document.querySelector('{sc}').scrollTop")
            key = await last.get_attribute('data-hfadj')
            y0 = (await last.bounding_box())['y']
            await last.click(); await pg.wait_for_timeout(400)
            after = await pg.evaluate(f"document.querySelector('{sc}').scrollTop")
            y1 = (await pg.locator(f'[data-hfadj="{key}"][data-d="1"]').bounding_box())['y']
            check(f'{w}: „+“ springt nicht nach oben', before > 50 and abs(after - before) < 5 and abs(y1 - y0) < 40, f'Scroll {before} → {after}, Knopf y {y0:.0f} → {y1:.0f}')
            minus = pg.locator(f'[data-hfadj="{key}"][data-d="-1"]')
            await minus.click(); await pg.wait_for_timeout(400)
            after2 = await pg.evaluate(f"document.querySelector('{sc}').scrollTop")
            check(f'{w}: „−“ springt nicht nach oben', abs(after2 - before) < 5, f'{before} → {after2}')
            await pg.evaluate("document.querySelector('#dlg-sheet').close()")
            await pg.evaluate("pid => openHeftZone(pid)", pid); await pg.wait_for_timeout(400)
            top = await pg.evaluate(f"document.querySelector('{sc}').scrollTop")
            check(f'{w}: neu geöffnet beginnt oben', top == 0, str(top))
            await pg.close()
        await br.close()
    print('FEHLER:', ERR) if ERR else print('alles ok')

asyncio.run(main())
