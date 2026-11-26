"""Fortschritt im Test (0.23.0): Abschnitte in fester Reihenfolge und ein Balken.
Der Balken läuft nur vorwärts – auch wenn die adaptive Suche eine Stufe zurückgeht –
und zeigt nie richtig/falsch an. Geprüft mit gemischten Antworten in allen Testarten."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        for subj, want in [('M1', ['Zahlen', 'Rechnen', 'Stellenwert']), ('M2', ['Uhr', 'Größen', 'Hundertertafel']), ('M', None), ('L', []), ('W', [])]:
            pg = await b.new_page(viewport={'width': 1180, 'height': 820}); pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(400)
            await pg.evaluate(f"diagStart('{subj}')"); await pg.wait_for_timeout(200); await pg.click('#d-start'); await pg.wait_for_timeout(200)
            progs, chips, k = [], None, 0
            while k < 80 and not await pg.evaluate("app.diag?.done ?? true"):
                st = await pg.evaluate("[app.diag.prog, [...document.querySelectorAll('.dg-sec')].map(e=>e.textContent), !!document.querySelector('.dg-bar'), document.querySelector('#equation').textContent]")
                progs.append(st[0]); chips = chips or st[1]
                if not st[2]: errs.append(f'{subj}: kein Balken')
                if any(w in st[3] for w in ['richtig', 'falsch', 'Richtig', 'Falsch']): errs.append(f'{subj}: Bewertung in der Kopfzeile')
                # abwechselnd richtig (Auswahl) und „Weiß ich nicht“ → die Suche geht auf und ab
                ok = await pg.evaluate("(()=>{const d=app.diag,it=d.items[d.idx]; if(it.type==='choice' && k%2===0){ d.resp={choice:it.correct}; return true;} return false;})()".replace('k%2', str(k % 2)))
                await pg.click('#d-next' if ok else '#d-skip'); await pg.wait_for_timeout(50); k += 1
            mono = all(b2 >= a2 for a2, b2 in zip(progs, progs[1:]))
            print(subj, 'Schritte', len(progs), 'Abschnitte', chips, 'monoton', mono, 'Ende', round(progs[-1]*100) if progs else None)
            if not mono: errs.append(f'{subj}: Balken läuft zurück')
            # Lese-Test: Erreicht das Kind L4 nicht, folgt der Teil „Hören“ (Backlog I); dann zeigt die Leiste „Lesen · Hören“.
            # Seit Q1 (3 von 3 bei Auswahlstufen) kommt dieser Ablauf mit den abwechselnden Antworten hier vor.
            if subj == 'L' and chips == ['Lesen', 'Hören']: pass
            elif want is not None and chips != want: errs.append(f'{subj}: Abschnitte {chips} statt {want}')
            await pg.close()
        # Abbrechen im laufenden Test braucht zwei Tipps; „Prüfen“ heißt im Test „Weiter“
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        await pg.evaluate("diagStart('M2')"); await pg.wait_for_timeout(150); await pg.click('#d-start')
        await pg.click('#d-close'); await pg.wait_for_timeout(150)
        if not await pg.evaluate("!!app.diag && app.mode==='diag'"): errs.append('Test nach einem Tipp auf Abbrechen beendet')
        if 'Wirklich' not in await pg.inner_text('#d-close'): errs.append('keine Rückfrage beim Abbrechen')
        await pg.click('#d-close'); await pg.wait_for_timeout(150)
        if await pg.evaluate("!!app.diag"): errs.append('Test nach zwei Tipps nicht beendet')
        await pg.evaluate("diagStart('M2')"); await pg.wait_for_timeout(150); await pg.click('#d-start')
        await pg.evaluate("(()=>{const d=app.diag; d.key='H|H6'; d.items=[H_ITEMS.H6[0]()]; d.idx=0; d.resp=null; renderDiag();})()")
        pr = await pg.inner_text('#prompt')
        if 'Prüfen' in pr or 'Weiter' not in pr: errs.append('Auftrag nennt im Test nicht „Weiter“: ' + pr)
        await pg.close()
        print('ERR', errs); await b.close()
asyncio.run(main())
