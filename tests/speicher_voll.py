"""Voller Speicher wird gemeldet (Backlog O1, Prüfung vom 22.11.2026, Stefan 26.11.2026):
- Schlägt das Speichern fehl, erscheint oben eine Leiste „Der Speicher ist voll …“ mit „Jetzt sichern“.
- Die Sicherung enthält den Stand aus dem Arbeitsspeicher, also auch das noch nicht Gespeicherte.
- Klappt das Speichern wieder, verschwindet die Leiste und der Stand ist gespeichert.
- Einstellungen: nur ein kurzer Hinweis, einmal je Sitzung.
- Im normalen Betrieb erscheint keine Leiste."""
import asyncio, json
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

FILL = """() => { let s = 'x'.repeat(1 << 20), i = 0; try { for(;;){ localStorage.setItem('fill' + i, s); i++; } } catch(e){}
  let j = 0; for(const n of [1 << 12, 1 << 6, 1]){ const t = 'x'.repeat(n); try { for(;;){ localStorage.setItem('fs' + j, t); j++; } } catch(e){} } return i + j; }"""
FREE = "() => { for(const k of Object.keys(localStorage)) if(/^f(ill|s)\\d+$/.test(k)) localStorage.removeItem(k); }"

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 820})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.evaluate("() => { const id = newId('p-'); data.profiles.push({id, name:'Mia', created:1, updated:1, world:'HS'}); data.current = id; saveData(); }")
        await pg.wait_for_timeout(200)
        check('normal: keine Leiste', await pg.locator('.store-bar').count() == 0)

        await pg.evaluate(FILL)
        await pg.evaluate("() => { data.profiles[0].name = 'Mia neu'; for(let k = 0; k < 500; k++) (data.log[data.current] ??= []).push({ts: Date.now() + k, mode:'add', task:'7 + 5', ok:true, tries:1}); saveData(); }")
        await pg.wait_for_timeout(200)
        bar = pg.locator('.store-bar')
        check('voll: Leiste erscheint', await bar.count() == 1)
        txt = await bar.inner_text() if await bar.count() else ''
        check('Text der Leiste', 'Der Speicher ist voll. Neue Ergebnisse werden gerade nicht gespeichert. Bitte jetzt sichern.' in txt, txt)
        stored = await pg.evaluate("JSON.parse(localStorage.getItem(DATA_KEY)).profiles[0].name")
        check('gespeichert bleibt der alte Stand', stored == 'Mia', stored)

        # Leiste liegt über allem, auch im Konzentrationsmodus beim Üben
        vis = await pg.evaluate("(() => { const r = document.querySelector('.store-bar').getBoundingClientRect(); const e = document.elementFromPoint(r.left + 20, r.top + r.height/2); return !!e?.closest('.store-bar'); })()")
        check('Leiste ist sichtbar und obenauf', vis)

        # Jetzt sichern: Sicherung mit dem Stand aus dem Arbeitsspeicher
        await pg.evaluate("window.__saved = null; saveFile = async (n, t) => { window.__saved = t; }")
        await pg.click('.store-bar [data-backup-now]'); await pg.wait_for_timeout(300)
        saved = await pg.evaluate("window.__saved")
        d = json.loads(saved)['data'] if saved else {}
        pid = d.get('current')
        check('Sicherung enthält das Ungespeicherte', bool(saved) and d['profiles'][0]['name'] == 'Mia neu' and len(d['log'].get(pid, [])) >= 500,
              str(len(d.get('log', {}).get(pid, [])) if saved else 'keine Datei'))
        check('Leiste bleibt, solange nicht gespeichert wird', await bar.count() == 1)

        # Einstellungen: kurzer Hinweis, einmal
        await pg.evaluate("() => { document.querySelector('.toast')?.remove(); settings.roundLen = '5'; settings.fbName = 'x'.repeat(2000); saveSettings(); }")
        t1 = await pg.evaluate("document.querySelector('.toast')?.textContent || ''")
        check('Einstellung: Hinweis', 'Die Einstellung konnte nicht gespeichert werden: Der Speicher ist voll.' in t1 or 'Die Einstellung konnte nicht gespeichert werden' in t1, t1)
        await pg.evaluate("() => { document.querySelector('.toast')?.remove(); saveSettings(); }")
        check('Einstellung: Hinweis nur einmal', await pg.evaluate("!document.querySelector('.toast')"))

        # Platz frei: nächstes Speichern klappt, Leiste verschwindet
        await pg.evaluate(FREE)
        await pg.evaluate("saveData()"); await pg.wait_for_timeout(200)
        check('Platz frei: Leiste weg', await bar.count() == 0)
        stored = await pg.evaluate("(s => [s.profiles[0].name, s.log[s.current].length])(JSON.parse(localStorage.getItem(DATA_KEY)))")
        check('danach alles gespeichert', stored[0] == 'Mia neu' and stored[1] >= 500, str(stored))

        # anderer Fehler als „voll“: eigener Text
        await pg.evaluate("() => { const o = Storage.prototype.setItem; window.__o = o; Storage.prototype.setItem = function(){ throw new DOMException('nein', 'SecurityError'); }; saveData(); }")
        await pg.wait_for_timeout(100)
        txt = await bar.inner_text() if await bar.count() else ''
        check('anderer Fehler: eigener Text', 'Der Browser speichert gerade nicht' in txt, txt)
        await pg.evaluate("() => { Storage.prototype.setItem = window.__o; saveData(); }")
        check('anderer Fehler behoben: Leiste weg', await bar.count() == 0)

        # Neustart: Stand ist da
        await pg.reload(); await pg.wait_for_timeout(500)
        n = await pg.evaluate("data.profiles[0]?.name")
        check('nach Neustart: Stand da', n == 'Mia neu', str(n))
        await br.close()
    print('FEHLER:', ERR) if ERR else print('alles ok')

asyncio.run(main())
