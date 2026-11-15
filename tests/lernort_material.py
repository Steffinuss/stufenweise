import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        pg=await b.new_page(viewport={'width':1180,'height':1400}); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.evaluate("""(()=>{data.profiles.push({id:'p1',name:'Ali'}); data.current='p1';
          const set=(k,st)=>setCell('p1',k,{status:st,quelle:'test',sum:''});
          set('M|20|I','erreicht'); set('M|20|II','erreicht'); set('M|20|III','nicht'); set('R|R1','erreicht'); set('R|R2','erreicht'); set('R|R3','teilweise'); set('S|S1','nicht'); set('L|L3','erreicht'); set('L|L4','teilweise'); set('W|W1','erreicht'); set('W|W2','erreicht'); set('W|W3','nicht'); set('U|U1','erreicht'); set('U|U2','nicht');
          data.errs={p1:{add:{uebertrag:5, eins:2}, sub:{kleingross:3}}};
          saveData(); })()""")
        # every cell key has a material way
        miss = await pg.evaluate("""(()=>{const ks=[...ZR.flatMap(z=>N_LEVELS.map(l=>`M|${z}|${l}`)),...R_LEVELS.map(l=>'R|'+l),...S_LEVELS.map(l=>'S|'+l),...U_LEVELS.map(l=>'U|'+l),...G_LEVELS.map(l=>'G|'+l),...H_LEVELS.map(l=>'H|'+l),...L_LEVELS.map(l=>'L|'+l),'L|LX',...P_LEVELS.map(l=>'P|'+l),...W_LEVELS.map(l=>'W|'+l),'W|WX'];
           const bad=[]; for(const k of ks){ const w=matWay(k); if(!w){bad.push(k+':none');continue;} if(w.lege){ const [sj,key]=w.lege.split(':'); const ok = sj==='K'?!!LEGE[key]: sj==='H'?!!H_SHEETS[key]: sj==='L'?!!R_SHEETS[key]: sj==='W'?!!W_SHEETS[key]: sj==='U'?!!U_SHEETS[key]: sj==='G'?!!G_SHEETS[key]:false; if(!ok) bad.push(k+':'+w.lege);} }
           return ks.length+' keys, bad: '+bad.join(',')})()""")
        print(miss)
        await pg.evaluate("statsId='p1'; renderStats(); document.querySelector('#dlg-stats').showModal()"); await pg.wait_for_timeout(400)
        await pg.evaluate("document.querySelector('.matway').scrollIntoView({block:'start'})"); await pg.wait_for_timeout(200)
        await pg.screenshot(path='mat_stats.png')
        print(await pg.evaluate("[...document.querySelectorAll('#stats-body fieldset')].map(f=>f.querySelector('legend')?.textContent).join(' | ')"))
        print(await pg.evaluate("(document.body.innerText.match(/Nächster Schritt am Material[^]*?\\n\\n/)||[''])[0].slice(0,400)"))
        print(await pg.evaluate("zoneReport('p1','M').ileb.massnahmen.slice(0,400)"))
        n = await pg.evaluate("document.querySelectorAll('[data-lege]').length")
        print('lege buttons', n)
        await pg.click('[data-lege]'); await pg.wait_for_timeout(1500)
        print(await pg.evaluate("app.sheet.topic+' '+app.sheet.zr+' '+app.sheetDoc.title"))
        await pg.screenshot(path='mat_sheetdlg.png')
        await pg.click('#sh-heft'); await pg.wait_for_timeout(300)
        print('heft cls', await pg.evaluate("app.heft.items.at(-1).cls"))
        wk = await pg.evaluate("weekReportHtml('p1', t=>'<h1>'+t+'</h1>').includes('Nächster Schritt am Material')"); print('week', wk)
        print('ERR', errs); await b.close()
asyncio.run(main())
