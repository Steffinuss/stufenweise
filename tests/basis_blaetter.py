"""Basis, Schritt 2 (0.27.0): Arbeitsblätter und Legeblätter.
Jedes Basis-Blatt (V1–V7, O2–O4) lässt sich in allen Varianten bauen (Anzahl, Große Aufgaben,
Schwarz-Weiß) ohne NaN/undefined; Lösungsblatt hat so viele Einträge wie Aufgaben; das Vorgemachte
(grau gestrichelt) steht nur in der ersten Aufgabe jeder Art. Schwarz-Weiß ersetzt Farben durch Muster
und stellt danach wieder auf Farbe. Die Basis-Legeblätter (Sortierunterlage, Zuordnungsleiste,
Musterstreifen) bauen sich in allen Varianten. Die Themen stehen im Generator, die Schwarz-Weiß-Option
erscheint nur bei Basis."""
import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

CHECK = r"""(()=>{ const bad=[], stat={};
  const topics = sheetTopics().flatMap(([, o]) => o.map(x => x[0]));
  for(const k in B_SHEETS){
    if(!topics.includes('B:'+k)) bad.push('Thema fehlt '+k);
    if(zoneToSheet(k[0]+'|'+k)?.topic !== 'B:'+k) bad.push('zoneToSheet '+k);
    for(let r = 0; r < 12; r++){
      const n = [6, 'fill', 4][r % 3], bw = r % 2 === 1, gross = r % 4 === 3;
      Object.assign(app.sheet, {topic:'B:'+k, n, sol:true, bw, gross});
      const d = buildSheet(), h = d.html;
      if(/NaN|undefined|§/.test(h)) bad.push(k+' kaputt '+(h.match(/.{30}(NaN|undefined|§).{10}/)||[''])[0]);
      if(B_BW) bad.push(k+' B_BW bleibt an');
      const doc = new DOMParser().parseFromString(h, 'text/html');
      const tasks = doc.querySelectorAll('.page:not(.sol) .ab-task').length, sols = doc.querySelectorAll('.sol li').length;
      if(!tasks || tasks !== sols) bad.push(`${k} Aufgaben ${tasks} / Lösungen ${sols}`);
      const exs = [...doc.querySelectorAll('.page:not(.sol) .ab-task')].filter(t => /bb-it (ring|weg|grau)|stroke="#888"|bb-box ring|bb-cb x|<b class="x"/.test(t.innerHTML)).length;
      if(exs < 1 || exs > B_SHEETS[k].gens.length) bad.push(`${k} Vorgemacht in ${exs} Aufgaben`);
      if(bw !== /id="bw-rot"/.test(h)) bad.push(k+' Muster-Defs '+bw);
      if(bw && /fill="#(c9414a|346bc3|e8b92e|2e8b57)"/.test(h.split('<div class="page sol"')[0].replace(/<defs>[\s\S]*?<\/defs>/g, '').replace(/<path d="M35 12q6-4 11 0-5 4-11 0z"[^>]*>/g, ''))) bad.push(k+' Farbe trotz Schwarz-Weiß');
      if(!bw && /url\(#bw-/.test(h)) bad.push(k+' Muster ohne Schwarz-Weiß');
      stat[k] = (stat[k] || 0) + tasks;
    }
  }
  for(const [k, v] of Object.entries(LEGE).filter(([, v]) => v.grp === 'B')){
    if(!topics.includes('K:'+k)) bad.push('Legeblatt fehlt '+k);
    for(const kt of v.kts) for(const bw of [false, true]){
      Object.assign(app.sheet, {topic:'K:'+k, kt, sol:true, bw});
      const h = buildSheet().html;
      if(/NaN|undefined/.test(h)) bad.push('Legeblatt kaputt '+k+kt);
      if(B_BW) bad.push(k+' B_BW bleibt an');
      if(k === 'muster' && kt !== 'none' && new DOMParser().parseFromString(h, 'text/html').querySelectorAll('.sol li').length !== 5) bad.push('Muster-Lösungen '+kt);
    }
  }
  for(const l of ['V3', 'V4', 'V7']) if(!/^K:/.test(MAT_WAY[l].lege || '')) bad.push(l+' ohne Legeblatt');
  return {bad, stat};
})()"""

async def main():
    async with async_playwright() as p:
        b = await launch(p); errs = []
        pg = await b.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        r = await pg.evaluate(CHECK)
        errs += r['bad']
        print('Aufgaben je Blatt (12 Durchläufe):', r['stat'])
        # Option im Generator: nur bei Basis
        ui = await pg.evaluate("""(()=>{ const out = {};
          for(const t of ['B:V1', 'M:plus', 'K:muster', 'K:zehner']){ app.sheet.topic = t; openSheets('none'); out[t] = !!document.querySelector('#sh-bw'); }
          return out; })()""")
        if ui != {'B:V1': True, 'M:plus': False, 'K:muster': True, 'K:zehner': False}: errs.append(f'Schwarz-Weiß-Option {ui}')
        print('Schwarz-Weiß-Option sichtbar:', ui)
        print('ERR', errs[:10]); await b.close()
asyncio.run(main())
