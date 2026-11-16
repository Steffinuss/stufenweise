"""Jede Testaufgabe passt auf kleinere iPads (0.24.0).
Safari auf einem 10,2-Zoll-iPad lässt etwa 1080 × 740 Pixel frei. Vorher lagen dort bei
46 Aufgaben Antworten unsichtbar unter dem Rand (z. B. Zehnerpartner: Auswahl ganz weg).
Jetzt verkleinert itFit() die Aufgabe; nur sehr lange Lesetexte (L9) dürfen scrollen und
zeigen dann „Weiter unten“. Am Handy (390 × 664) darf mehr scrollen, aber nie ohne Hinweis."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

LIST = r"""(()=>{const pools=[]; const add=(ax,o)=>{for(const k in o) if(Array.isArray(o[k])) o[k].forEach((g,i)=>pools.push(ax+'|'+k+'#'+i));};
add('S',STELL);add('L',READ);add('W',WRITE);add('U',CLOCK);add('G',G_ITEMS);add('H',H_ITEMS);add('R',R_ITEMS);add('Z',Z_ITEMS);
for(const l of ['I','II','III','IV','V']) for(const zr of [10,20,100,1000]) MATH[l](zr).forEach((g,i)=>pools.push('M|'+zr+'|'+l+'#'+i));
return pools.filter(p=>!/^[LW]\|[LW]X/.test(p));})()"""
GET = r"""(id)=>{const [key,gi]=id.split('#'); const [ax,a,b]=key.split('|'); const arr= ax==='M'?MATH[b](+a): ({S:STELL,L:READ,W:WRITE,U:CLOCK,G:G_ITEMS,H:H_ITEMS,R:R_ITEMS,Z:Z_ITEMS})[ax][a];
 const d=app.diag; d.key=key; d.items=[arr[+gi]()]; d.idx=0; d.resp=null; d.answers=[]; renderDiag();
 const w=document.querySelector('#stage .it-wrap'); const st=document.querySelector('#stage').getBoundingClientRect();
 const btns=[...document.querySelectorAll('#stage [data-dgc], #stage .dg-in, #stage [data-hb]')].filter(e=>e.getBoundingClientRect().bottom>st.bottom+2).length;
 return {more: !!w?.classList.contains('it-more'), hidden: btns};}"""

async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        for vw, vh in [(1080, 740), (810, 1010), (390, 664)]:
            pg = await b.new_page(viewport={'width': vw, 'height': vh}); pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(400)
            ids = await pg.evaluate(LIST); cur = None; bad = []
            for id_ in ids:
                subj = {'L': 'L', 'W': 'W'}.get(id_[0], 'M2')
                if subj != cur:
                    await pg.evaluate("app.diag=null"); await pg.evaluate(f"diagStart('{subj}', false)"); await pg.wait_for_timeout(120)
                    await pg.click('#d-start'); await pg.wait_for_timeout(80); cur = subj
                for rep in range(3):
                    r = await pg.evaluate(GET, id_)
                    if r['more'] and not id_.startswith('L|L9') and vw > 560: bad.append(f'{id_} scrollt')  # Handy: Scrollen mit Hinweis erlaubt
                    if r['hidden'] and not r['more']: bad.append(f'{id_}: {r["hidden"]} Antwortknöpfe unsichtbar')
            print(vw, vh, len(ids), 'Aufgaben, Probleme:', sorted(set(bad))[:8])
            errs += sorted(set(bad)); await pg.close()
        print('ERR', errs[:8]); await b.close()
asyncio.run(main())
