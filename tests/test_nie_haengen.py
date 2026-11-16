"""Test darf nie hängen bleiben (0.23.1): Jede Stufe hat mindestens 3 Aufgaben,
und bei vielen falschen Antworten läuft der Test bis zum Ende durch.
Anlass: Zehnerpartner Z1 hatte nur 2 Aufgaben; nach „1 richtig, 1 falsch“ ging nichts mehr."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

POOLS = """(()=>{const out=[]; const chk=(n,o)=>{for(const k in o){const v=o[k]; if(Array.isArray(v) && v.length<3) out.push(n+'.'+k+'='+v.length);}};
  chk('STELL',STELL);chk('READ',READ);chk('WRITE',WRITE);chk('CLOCK',CLOCK);chk('G',G_ITEMS);chk('H',H_ITEMS);chk('R',R_ITEMS);chk('Z',Z_ITEMS);chk('PHON',PHON);
  for(const l of ['I','II','III','IV','V']) for(const zr of [10,20,100,1000]){ try{const a=MATH[l](zr); if(a.length<3) out.push('M.'+zr+'.'+l+'='+a.length);}catch(e){} }
  return out;})()"""

async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        pg = await b.new_page(); await pg.goto(URL); await pg.wait_for_timeout(400)
        short = await pg.evaluate(POOLS)
        if short: errs.append('zu wenige Aufgaben: ' + ', '.join(short))
        await pg.close()
        for subj in ['M1'] * 12 + ['M2'] * 4 + ['L'] * 3 + ['W'] * 3:
            pg = await b.new_page(viewport={'width': 1180, 'height': 820}); pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(300)
            await pg.evaluate(f"diagStart('{subj}')"); await pg.wait_for_timeout(150); await pg.click('#d-start')
            k, last, same = 0, None, 0
            while k < 90 and not await pg.evaluate("app.diag?.done ?? true"):
                st = await pg.evaluate("[app.diag.key, app.diag.idx, app.diag.nItems, app.diag.items[app.diag.idx]?.type]")
                same = same + 1 if st == last else 0; last = st
                if same >= 2: errs.append(f'{subj} hängt bei {st}'); break
                t = st[3]
                if t == 'choice':  # meist falsch, manchmal richtig
                    await pg.evaluate(f"(()=>{{const it=app.diag.items[app.diag.idx]; app.diag.resp={{choice:{'it.correct' if k % 3 == 0 else '(it.correct+1)%it.options.length'}}};}})()")
                    await pg.click('#d-next')
                elif t == 'input':
                    for f in await pg.query_selector_all('.dg-in, #stage input'):
                        try: await f.fill('1')
                        except Exception: pass
                    await pg.click('#d-next')
                else:
                    await pg.click('#d-skip')
                await pg.wait_for_timeout(40); k += 1
            await pg.close()
        print('ERR', errs[:5]); await b.close()
asyncio.run(main())
