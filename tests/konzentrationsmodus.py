"""Konzentrationsmodus (Backlog H, Stefan 24.11.2026) und Punkte aus dem Usability-Review:
- Standard an: beim Üben keine Leiste, keine Einstellleiste, kein Name/Menü; oben Fortschritt, Pause, Zahnrad
- Startseite: keine Leiste, kurzer Satz; Bereich über die Kacheln
- „Weiter“ erst nach Lösung oder zwei Fehlversuchen (Plus, Geld, Einmaleins, Lesen); Pause → Startseite
- Zahnrad mit PIN: alles sichtbar bis zur Pause
- Geld: Auswahl Betrag legen/Wechselgeld als Kacheln; Wechselgeld: ein Satz, Rechnung erst nach dem Lösen, Tipp erst nach Fehlversuch
- Zahlen mit Material: Zählaufgabe, Zahl erst nach dem Zählen
- Rundenende: „Runde vorbei“ statt „Geschafft!“, wenn nichts gelöst wurde
- Einstellung „aus“: alles wie vorher"""
import asyncio
from common import URL, launch  # noqa: E402
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

KID = """() => { const id = newId('p-'); data.profiles.push({id, name:'Mia', created:1, updated:1, world:'HS'}); data.current = id; saveData(); }"""
VIS = """sel => { const e = document.querySelector(sel); if(!e) return false; const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).display !== 'none'; }"""

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 820}, has_touch=True)
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.evaluate(KID); await pg.evaluate("location.reload()"); await pg.wait_for_timeout(700)
        check('Standard an', await pg.evaluate("settings.fokus") == 'on')
        await pg.click("[data-ctx='practice']"); await pg.wait_for_timeout(300)
        if await pg.locator('[data-home-pick]').count(): await pg.locator('[data-home-pick]').first.click(); await pg.wait_for_timeout(300)
        check('Startseite ohne Leiste', not await pg.evaluate(VIS, '.rail'))
        check('Startseite: kurzer Satz', 'Lehrkraft' not in await pg.evaluate("$('#stage').innerText"))
        check('Startseite: Menü bleibt', await pg.evaluate(VIS, '#btn-more'))

        # Plus über die Kacheln
        await pg.click('[data-home-subj="M"]'); await pg.wait_for_timeout(300)
        await pg.click('[data-wz-mode="add"]'); await pg.wait_for_timeout(500)
        check('Plus: Aufgabe läuft', await pg.evaluate("task().ready"))
        check('Plus: Leiste, Einstellleiste, Menü weg', not any([await pg.evaluate(VIS, s) for s in ['.rail', '.toolbar', '#btn-more', '#btn-profile']]))
        bar = await pg.evaluate("$('#fokus-bar').innerText")
        check('Plus: Fortschritt und Pause', 'Aufgabe 1 von 10' in bar and 'Pause' in bar and 'Weiter' not in bar, bar.replace('\n', ' | '))
        # Material zusammenlegen, dann zweimal falsch
        await pg.evaluate("task().view !== 'material' || !$('#c-join') || $('#c-join').click()"); await pg.wait_for_timeout(300)
        res = await pg.evaluate("resultOf(app.mode, task().a, task().b)")
        for i in (1, 2):
            await pg.fill('#guess', str(res + i)); await pg.click('#c-check'); await pg.wait_for_timeout(200)
            bar = await pg.evaluate("$('#fokus-bar').innerText")
            check(f'Plus: nach {i} Fehlversuch(en) Weiter {"da" if i == 2 else "noch nicht"}', ('Weiter' in bar) == (i == 2), bar.replace('\n', ' | '))
        await pg.fill('#guess', str(res)); await pg.click('#c-check'); await pg.wait_for_timeout(300)
        check('Plus: gelöst, Weiter hervorgehoben', await pg.evaluate("$('#fk-next')?.classList.contains('primary')"))
        a0 = await pg.evaluate("[task().a, task().b]")
        await pg.click('#fk-next'); await pg.wait_for_timeout(300)
        check('Plus: Weiter gibt neue Aufgabe, Runde zählt', await pg.evaluate("[task().a, task().b]") != a0 and 'Aufgabe 2 von 10' in await pg.evaluate("$('#fokus-bar').innerText"))

        # Zahnrad: alles sichtbar bis zur Pause
        await pg.click('#fk-teacher'); await pg.wait_for_timeout(300)
        if await pg.locator('#dlg-pin[open]').count(): await pg.keyboard.press('Escape')
        check('Zahnrad ohne PIN: alles sichtbar', await pg.evaluate(VIS, '.toolbar') and await pg.evaluate(VIS, '.rail'))
        await pg.evaluate("goHome()"); await pg.wait_for_timeout(300)
        check('nach Pause wieder Konzentrationsmodus', await pg.evaluate("app.fokusAus") is False)

        # Geld: Wechselgeld
        await pg.click('[data-home-subj="M"]'); await pg.wait_for_timeout(300)
        await pg.click('[data-wz-mode="money"]'); await pg.wait_for_timeout(400)
        check('Geld: Kacheln Betrag legen/Wechselgeld', await pg.locator('[data-fk-money]').count() == 2)
        await pg.click('[data-fk-money="change"]'); await pg.wait_for_timeout(400)
        eq = await pg.evaluate("$('#equation').textContent")
        check('Wechselgeld: Auftrag statt Rechnung', eq == 'Lege das Wechselgeld.' and '−' not in eq, eq)
        check('Wechselgeld: kein zweiter Satz, kein Tipp', await pg.evaluate("$('#prompt').textContent") == '' and await pg.evaluate("$('#hint').textContent") == '')
        check('Wechselgeld: Feld heißt „Wechselgeld“', 'Lege hier hin' not in await pg.evaluate("$('#stage').innerHTML"))
        check('Wechselgeld: Weiter versteckt', await pg.evaluate("$('#m-next').hidden") and await pg.locator('#fk-next').count() == 0)
        tgt = await pg.evaluate("app.money.target")
        # einmal falsch: zu wenig (nichts geht nicht, also kleinste Münze, wenn sie nicht passt)
        await pg.evaluate("""t => { const m = app.money, d = moneyDenoms().filter(c => c !== t).sort((a, b) => a - b)[0]; m.items = [{id:1, c:d, x:300, y:150}]; m.check = null; renderMoney(); }""", tgt)
        await pg.click('#m-check'); await pg.wait_for_timeout(200)
        await pg.click('#m-clear'); await pg.wait_for_timeout(200)
        check('Wechselgeld: Tipp nach Fehlversuch', 'Tipp' in await pg.evaluate("$('#hint').textContent"))
        await pg.evaluate("""t => { const m = app.money; m.items = greedy(t, moneyDenoms()).map((c, i) => ({id:10 + i, c, x:200 + 60*i, y:150})); m.check = null; renderMoney(); }""", tgt)
        await pg.click('#m-check'); await pg.wait_for_timeout(300)
        eq = await pg.evaluate("$('#equation').textContent")
        check('Wechselgeld: Rechnung nach dem Lösen', '−' in eq and '=' in eq, eq)
        check('Wechselgeld: Weiter heißt „Weiter“', await pg.evaluate("!$('#m-next').hidden && $('#m-next').textContent.includes('Weiter')"))

        # Rundenende ohne Lösung
        await pg.evaluate("app.round = {key: roundKey(), res: Array(10).fill('skip')}; roundEnd()"); await pg.wait_for_timeout(300)
        check('Rundenende: „Runde vorbei“', await pg.evaluate("document.querySelector('.round-card h2')?.textContent") == 'Runde vorbei')
        await pg.click('[data-round="pause"]'); await pg.wait_for_timeout(300)
        check('Rundenende: Pause → Startseite', await pg.evaluate("app.mode") == 'home')

        # Einmaleins: „Nächste Aufgabe“ erst nach Lösung/Fehlversuchen
        await pg.click('[data-home-subj="M"]'); await pg.wait_for_timeout(300)
        await pg.click('[data-wz-mode="times"]'); await pg.wait_for_timeout(400)
        check('Einmaleins: Überspringen versteckt', await pg.evaluate("$('#t-next')?.hidden") is True)
        await pg.evaluate("goHome()"); await pg.wait_for_timeout(200)

        # Zahlen: Zählaufgabe
        await pg.click('[data-home-subj="M"]'); await pg.wait_for_timeout(300)
        await pg.click('[data-wz-mode="number"]'); await pg.wait_for_timeout(400)
        check('Zahlen: Zählaufgabe, Zahl verdeckt', await pg.evaluate("!!$('#equation #guess') && !showDigits() && $('#words').hidden"))
        a = await pg.evaluate("task().a")
        await pg.fill('#guess', str(a)); await pg.click('#c-check'); await pg.wait_for_timeout(300)
        check('Zahlen: gezählt, Zahl steht da', await pg.evaluate("task().check") == 'ok' and str(a) in await pg.evaluate("$('#equation').textContent"))
        check('Zahlen: Protokoll „count“', await pg.evaluate("data.log[data.current].at(-1).mode") == 'count')
        check('Zahlen: keine Darstellungswahl', not await pg.evaluate(VIS, '#controls .views'))

        # Lesen: Weiter erst nach zwei Fehlversuchen
        await pg.evaluate("goHome()"); await pg.wait_for_timeout(200)
        await pg.click('[data-home-subj="D"]'); await pg.wait_for_timeout(300)
        await pg.locator('[data-wz-lvl="L4"]').first.click(); await pg.wait_for_timeout(500)
        check('Lesen: Konzentrationsmodus', await pg.evaluate("document.body.classList.contains('fokus')"))
        for i in (1, 2):
            await pg.evaluate("""() => { const R = app.read, it = R.item; const ch = [...document.querySelectorAll('#stage [data-dgc]')]; const wrong = ch.find(b => { R.r.choice = +b.dataset.dgc; return !evalItem(it, R.r, [])?.ok; }); R.r.choice = null; wrong?.click(); }"""); await pg.wait_for_timeout(150)
            await pg.evaluate("$('#r-check')?.click()"); await pg.wait_for_timeout(250)
        check('Lesen: nach zwei Fehlversuchen Weiter', await pg.locator('#fk-next').count() == 1, str(await pg.evaluate("app.read.tries")))

        # Einstellung aus
        await pg.evaluate("settings.fokus = 'off'; saveSettings(); goHome()"); await pg.wait_for_timeout(200)
        check('aus: Startseite mit Leiste', await pg.evaluate(VIS, '.rail'))
        await pg.click('[data-home-subj="M"]'); await pg.wait_for_timeout(300)
        await pg.click('[data-wz-mode="add"]'); await pg.wait_for_timeout(400)
        check('aus: Einstellleiste da, kein Balken', await pg.evaluate(VIS, '.toolbar') and await pg.evaluate("$('#fokus-bar').hidden"))
        await pg.evaluate("settings.fokus = 'on'; saveSettings()")

        print('Fehler:', ERR or 'keine')
        await br.close()
        if ERR: raise SystemExit(1)

asyncio.run(main())
