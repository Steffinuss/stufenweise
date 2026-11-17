"""Basis, Schritt 1 (0.26.1): Bilder und Grundgerüst.
Alle Gegenstände in allen Farben und Größen, Formen mit Mustern, Pfeile, Spiegel-Zeichen,
Punktbilder und Bildsymbole lassen sich zeichnen (ohne NaN/undefined). Die Achsen V und O
haben zu jeder Stufe alle Texte und einen Weg am Material. Seit 0.28.0 ist das Fach „Basis“ zum Üben
angemeldet; der Basis-Test fehlt noch, solange BASIS_ON aus ist."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

CHECK = r"""(()=>{ const bad=[]; const chk=(n,h)=>{ if(!/^<svg/.test(h) || /NaN|undefined/.test(h)) bad.push(n); };
  for(const k in B_OBJ){ for(const c of [null, ...Object.keys(B_COL)]) for(const sc of [.4, .7, 1]) chk(k+c+sc, bObj(k, c, 64, sc)); }
  for(const f in B_FORM) for(const m of ['voll','leer','streifen','punkte']) chk(f+m, bShape(f, 'rot', 64, m));
  for(const d in B_DIR) chk(d, bArrow(d));
  for(const g in B_GLYPH) for(const l of [0,1,2,3]) chk(g+l, bGlyph(g, l));
  for(const n of [1,2,3,4]) B_DOTS[n].forEach((_, v) => chk('dots'+n+v, bDots(n, v)));
  for(const l of [...V_LEVELS, ...O_LEVELS]){
    if(!B_SYM[l]) bad.push('Symbol '+l);
    const i = (V_INFO[l] || O_INFO[l]); for(const f of ['name','short','a','b','kann','ziel','analog','ich','bp']) if(!i[f]) bad.push(l+' ohne '+f);
    if(i.offer?.set?.lvl !== l) bad.push(l+' Angebot');
    const w = MAT_WAY[l]; if(!w?.hand || !w?.bild || !w?.need?.length) bad.push(l+' ohne Weg am Material');
    const ci = cellInfo((l[0])+'|'+l); if(ci.name !== i.name || !ci.place) bad.push(l+' cellInfo');
    if(!/Vergleichen und Ordnen|Sehen und Orientieren/.test(cellLabel(l[0]+'|'+l))) bad.push(l+' cellLabel');
  }
  if(new Set(Object.values(B_COL)).size !== Object.keys(B_COL).length) bad.push('Farben doppelt');
  return {bad, subj: SUBJ_IDS.join(), tests: TEST_IDS.join(), on: BASIS_ON};
})()"""

async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        pg = await b.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        r = await pg.evaluate(CHECK)
        errs += r['bad']
        if not r['on'] and (r['subj'] != 'B,M,D' or r['tests'] != 'M,L,W'): errs.append(f'Fach Basis (Üben) fehlt oder Test schon da: {r}')
        print('Fächer', r['subj'], 'Tests', r['tests'], 'BASIS_ON', r['on'])
        print('ERR', errs[:10]); await b.close()
asyncio.run(main())
