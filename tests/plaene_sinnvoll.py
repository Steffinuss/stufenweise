"""Erzeugte Inhalte ergeben Sinn (Stefan, 26.11.2026: Stundenplan „Montag nur Deutsch, Dienstag nur Mathe“, „Klasse 2a“ in der Hauptstufe).
- Stundenplan: nicht jeden Tag dasselbe Fach in derselben Stunde, Klasse und Fächer passend zur Stufe (Hauptstufe: AES, Technik, WBO …),
  Sport als Doppelstunde, Antwort „Wie oft ist … in der Woche?“ stimmt
- „Stimmt das?“: als falsch gemeinte Sätze sind wirklich falsch (nicht „Mit dem Messer kann man Papier schneiden“)
- Was steht (Kerze, Tasse, Glas …), steht nicht unter dem Tisch"""
import asyncio
from common import URL, launch
from playwright.async_api import async_playwright

ERR = []
def check(name, ok, info=''):
    print(('ok  ' if ok else 'ERR ') + f'[{name}] {info}')
    if not ok: ERR.append(name)

async def main():
    async with async_playwright() as p:
        br = await launch(p); pg = await br.new_page()
        pg.on('pageerror', lambda e: (ERR.append('pageerror'), print('ERR [pageerror]', e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        r = await pg.evaluate("""() => { const out = {}, keep = settings.world;
            for(const w of ['GS', 'HS']){ settings.world = w; const res = [];
              for(let k = 0; k < 40; k++){ const d = docTimetable(), doc = new DOMParser().parseFromString(d.html, 'text/html');
                const rows = [...doc.querySelectorAll('tbody tr')].map(tr => [...tr.querySelectorAll('td')].map(td => td.textContent));
                const cls = doc.querySelector('.dc-h').textContent, cols = rows[0].length;
                const sameCol = [...Array(cols).keys()].some(h => rows.every(r => r[h] === rows[0][h]));
                const sport = rows.filter(r => r.join(',').includes('Sport,Sport')).length === 1;
                const q = d.qs.find(x => /Wie oft ist/.test(x[1])), f = q[1].match(/Wie oft ist (\\S+)/)[1], c = rows.flat().filter(x => x === f).length;
                res.push({sameCol, cls, sport, countOk: q[2][0] === `${c}-mal`, subj: [...new Set(rows.flat())]}); }
              out[w] = res; }
            settings.world = keep;
            const yn = []; for(let k = 0; k < 400; k++){ const [s, yes, n] = factSentence(); if(!yes) yn.push([s, n]); }
            const badYn = yn.filter(([s, n]) => (TOOL_ALSO[n] || []).some(a => s.includes(`kann man ${a}.`)) || /(Mütze ist nass|Kerze ist dunkel|Pizza ist eckig)/.test(s)).map(x => x[0]);
            const steht = Object.keys(SCENE_OBJ).filter(o => SCENE_OBJ[o] === 'steht'), under = [];
            for(const o of steht) for(let k = 0; k < 30; k++) if(scenePos(o) === 'unter') under.push(o);
            return {out, badYn: [...new Set(badYn)], under: [...new Set(under)]}; }""")
        for w in ['GS', 'HS']:
            res = r['out'][w]
            check(f'{w}: kein Fach jeden Tag in derselben Stunde', not any(x['sameCol'] for x in res), str(sum(x['sameCol'] for x in res)))
            check(f'{w}: Sport als Doppelstunde an einem Tag', all(x['sport'] for x in res))
            check(f'{w}: „Wie oft …?“ richtig gezählt', all(x['countOk'] for x in res))
            nums = {int(''.join(ch for ch in x['cls'] if ch.isdigit())) for x in res}
            subj = set().union(*[set(x['subj']) for x in res])
            if w == 'GS':
                check('GS: Klassen 1–4', nums <= {1, 2, 3, 4}, str(nums))
                check('GS: Fächer der Grundstufe', subj <= {'Deutsch', 'Mathe', 'Sachunterricht', 'Musik', 'Kunst', 'Sport', 'Religion'}, str(subj))
            else:
                check('HS: Klassen 5–9', nums <= {5, 6, 7, 8, 9}, str(nums))
                check('HS: Fächer der Hauptstufe (mit AES, Technik, WBO)', {'AES', 'Technik', 'WBO'} <= subj and 'Sachunterricht' not in subj, str(subj))
        check('„Stimmt das?“: falsche Sätze sind wirklich falsch', not r['badYn'], str(r['badYn'][:5]))
        check('Was steht, steht nicht unter dem Tisch', not r['under'], str(r['under']))
        print('Fehler:', ERR or 'keine')
        await br.close()
        if ERR: raise SystemExit(1)

asyncio.run(main())
