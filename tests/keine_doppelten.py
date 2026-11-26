"""Keine gleiche Aufgabe zweimal auf einer Seite (Backlog S9, Stefan 26.11.2026: Heft-Einstieg „Ergänzen bis 10“ zeigte viermal
„In den Karton passen 10. 9 sind schon drin.“ und zweimal „8 + ☐ = 10“).
Geprüft: alle Blätter mit fester Aufgabenzahl und mit Feinstufe (leicht, mittel, schwer, wie im Heft) und zwei ganze Hefte."""
import asyncio, re
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

DUPS = r"""html => { const d = new DOMParser().parseFromString(html, 'text/html'), out = [];
  for(const pg of d.querySelectorAll('.page:not(.sol)')){ const seen = new Map();
    for(const t of pg.querySelectorAll('.ab-grid > .ab-task')){ const c = t.cloneNode(true); c.querySelector('.nr')?.remove(); c.querySelector('.ab-bsp-lab')?.remove(); c.querySelector('.ab-bsp-sol')?.remove();
      const k = c.innerHTML.replace(/\s+/g, ' '); if(seen.has(k)) out.push(t.textContent.replace(/\s+/g, ' ').trim().slice(0, 70)); seen.set(k, 1); } }
  return out; }"""

KID = """(z) => { const id = newId('p-'); data.profiles.push({id, name:z.name, created:1, updated:1, world:'HS'}); data.current = id;
  for(const k of z.ok) setCell(id, k, {status:'erreicht', quelle:'test', sum:''});
  for(const k of z.part) setCell(id, k, {status:'teilweise', quelle:'test', sum:''});
  saveData(); return id; }"""

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page(viewport={'width': 1180, 'height': 900})
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        topics = await pg.evaluate("sheetTopics().flatMap(([, o]) => o).map(x => x[0]).filter(t => !t.startsWith('K:'))")
        bad = []
        for t in topics:
            for zr in ([10, 20, 100, 1000] if t.startswith('M:') else [20]):
                for stufe in [None, 0, .5, 1]:
                    for rep in range(2):
                        html = await pg.evaluate("([t, zr, stufe]) => { Object.assign(app.sheet, {...SHEET_BASE, pid:'none', topic:t, zr, n:8, sol:false, stufe}); return buildSheet().html; }", [t, zr, stufe])
                        d = await pg.evaluate(DUPS, html)
                        if d: bad.append(f'{t} {zr} {stufe}: {d[0]}')
        check(f'{len(topics)} Blätter, 8 Aufgaben, mit und ohne Feinstufe: keine Aufgabe doppelt', not bad, '; '.join(sorted(set(bad))[:6]))

        for z in [{'name': 'Mia', 'ok': ['M|10|I'], 'part': ['M|10|II', 'R|R1', 'Z|Z1', 'U|U1']},
                  {'name': 'Ben', 'ok': ['L|L1', 'L|L2', 'L|L3', 'L|L4', 'L|L5', 'W|W1', 'W|W2', 'W|W3', 'W|W4'], 'part': ['L|L6', 'W|W5']}]:
            pid = await pg.evaluate(KID, z)
            await pg.evaluate("pid => { app.heft = {title:'Mein Arbeitsheft', pid, items:[], toc:true, pages:36, vor:'voll'}; }", pid)
            await pg.evaluate("async pid => { await heftMake(pid); }", pid)
            res = await pg.evaluate("""(D) => { const f = eval(D); return app.heft.items.flatMap(i => f(`<div class="page">${i.html}</div>`).map(x => i.title + ': ' + x)); }""", DUPS)
            check(f'Heft {z["name"]}: keine Aufgabe doppelt auf einer Seite', not res, '; '.join(res[:4]))
        await br.close()
    print('FEHLER:', ERR) if ERR else print('alles ok')

asyncio.run(main())
