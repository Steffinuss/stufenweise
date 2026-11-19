"""Plus und Minus aufgeteilt (Backlog A, Stefan 19.11.2026).
Üben: sofort eine Zufallsaufgabe, keine eigene Eingabe, keine Darstellungs-Knöpfe unten; Darstellung kommt nacheinander
(bis 20 Material → Zwanzigerfeld → Zahlenstrahl, bis 100 Material → Hundertertafel → Zahlenstrahl, bis 1000 Material → Zahlenstrahl),
nach 8 auf Anhieb richtigen die nächste, nach 3 Fehlern in Folge zurück; Lehrkraft kann oben wählen (mit PIN gesperrt).
Rechenhilfe: eigener Eintrag (auch geführt), Plus/Minus wählbar, eigene Zahlen, Darstellung frei, keine Zufallsaufgabe."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

SOLVE = "(()=>{const t=task(); if(!document.querySelector('#guess')){ t.done=true; renderWork(); } const g=document.querySelector('#guess'); g.value=String(resultOf(app.mode,t.a,t.b)); t.tries=TRIES; checkGuess(); })()"


async def run(pg, n, tries=0):
    out = []
    for _ in range(n):
        out.append(await pg.evaluate("task().view"))
        await pg.evaluate(SOLVE.replace('TRIES', str(tries))); await pg.wait_for_timeout(20)
        await pg.click('#btn-random'); await pg.wait_for_timeout(30)
    return out


async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.evaluate("app.ctx='practice'; settings.subject='M'; app.range=20; app.mode='home'; render()")
        await pg.click('[data-mode="add"]'); await pg.wait_for_timeout(200)
        st = await pg.evaluate("[app.mode, !!app.calc, task().ready, task().view, !!document.querySelector('#in-a'), document.querySelectorAll('[data-view]').length, document.querySelectorAll('[data-pmv]').length, document.querySelector('#btn-random').textContent]")
        if st != ['add', False, True, 'material', False, 0, 3, 'Neue Aufgabe']: errs.append(f'Üben Start: {st}')
        v = await run(pg, 18)
        if v[:8] != ['material'] * 8 or v[8:16] != ['field'] * 8 or v[16:] != ['line'] * 2: errs.append(f'Reihenfolge bis 20: {v}')
        v = await run(pg, 3, tries=1)  # 3 Aufgaben nicht auf Anhieb → zurück
        if await pg.evaluate("task().view") != 'field': errs.append(f'nach 3 Fehlern nicht zurück: {await pg.evaluate("task().view")}')
        # bis 100: Material → Hundertertafel → Zahlenstrahl; bis 1000 ohne Tafel
        await pg.click('[data-range="100"]'); await pg.wait_for_timeout(150)
        if await pg.evaluate("pmViews().join()") != 'material,board,line': errs.append('Reihenfolge bis 100')
        await pg.click('[data-range="1000"]'); await pg.wait_for_timeout(150)
        if await pg.evaluate("pmViews().join()") != 'material,line': errs.append('Reihenfolge bis 1000')
        await pg.click('[data-range="20"]'); await pg.wait_for_timeout(150)
        # Lehrkraft wählt (ohne PIN erlaubt), mit PIN gesperrt
        await pg.click('[data-pmv="2"]'); await pg.wait_for_timeout(100)
        if await pg.evaluate("task().view") != 'line': errs.append('Lehrkraft-Wahl der Darstellung')
        await pg.evaluate("settings.pin='1234'; app.teacherUntil=0; render()")
        if not await pg.evaluate("document.querySelector('[data-pmv=\"0\"]').disabled"): errs.append('Darstellung mit PIN nicht gesperrt')
        await pg.evaluate("settings.pin=''; render()")
        # Rechenhilfe
        await pg.click('[data-calc]'); await pg.wait_for_timeout(200)
        st = await pg.evaluate("[app.mode, !!app.calc, task().ready, !!document.querySelector('#in-a'), !!document.querySelector('[data-calcop]'), document.querySelector('#btn-random').hidden, document.querySelector('[data-calc]').getAttribute('aria-pressed'), document.querySelector('[data-mode=\"add\"]').getAttribute('aria-pressed')]")
        if st != ['add', True, False, True, True, True, 'true', 'false']: errs.append(f'Rechenhilfe Start: {st}')
        await pg.fill('#in-a', '13'); await pg.fill('#in-b', '6'); await pg.click('[data-calcop="sub"]'); await pg.wait_for_timeout(150)
        await pg.click('#btn-commit'); await pg.wait_for_timeout(150)
        st = await pg.evaluate("[app.mode, task().a, task().b, document.querySelectorAll('[data-view]').length]")
        if st != ['sub', 13, 6, 3]: errs.append(f'Rechenhilfe eigene Aufgabe: {st}')
        await pg.click('[data-view="line"]'); await pg.wait_for_timeout(100)
        if await pg.evaluate("task().view") != 'line': errs.append('Rechenhilfe: Darstellung frei')
        # zurück zum Üben: neue Zufallsaufgabe, nicht die eigene
        await pg.click('[data-mode="sub"]'); await pg.wait_for_timeout(200)
        st = await pg.evaluate("[app.mode, !!app.calc, task().ready, task().a === 13 && task().b === 6]")
        if st != ['sub', False, True, False]: errs.append(f'zurück zum Üben: {st}')
        # Startseite: Kachel Rechenhilfe; geführte Oberfläche zeigt Rechenhilfe
        await pg.evaluate("app.mode='home'; app.wz={step:'area', subj:'M'}; render()")
        await pg.click('.wz-tile[data-wz-calc]'); await pg.wait_for_timeout(150)
        if await pg.evaluate("[app.mode, !!app.calc].join()") != 'add,true': errs.append('Kachel Rechenhilfe')
        await pg.close()
        # Handy
        pg = await b.new_page(viewport={'width': 390, 'height': 844}); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.evaluate("app.ctx='practice'; settings.subject='M'; app.range=20; app.mode='add'; render()"); await pg.wait_for_timeout(200)
        if await pg.evaluate("document.documentElement.scrollWidth") > 392: errs.append('Handy: zu breit')
        print('ERR', errs); await b.close()
asyncio.run(main())
