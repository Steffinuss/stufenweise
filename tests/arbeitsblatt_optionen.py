"""Arbeitsblatt-Optionen (0.20.0):
- Materialbilder „1. Aufgabe vorgegeben, dann selbst zeichnen“: keine Marker übrig, Beispiel mit Bild, sonst leere Felder
- Zehnerpartner und Rechnen über die 10: Lösungen stimmen, Beispiel ist ausgefüllt
- Geld: nur Euro / Euro und Cent / auf den Cent
- Einmaleins: nur die gewählten Reihen"""
import asyncio, re
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402

async def main():
    async with async_playwright() as p:
        b = await launch(p)
        pg = await b.new_page(viewport={'width': 1180, 'height': 820}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        await pg.evaluate("openSheets()"); await pg.wait_for_timeout(400)

        # 1. keine Marker übrig, bei allen Themen, mit und ohne Zeichnen
        topics = await pg.evaluate("sheetTree().flatMap(f=>f.areas.flatMap(a=>a.items.map(x=>x[0]))).filter(t=>!t.startsWith('K:'))")
        left = await pg.evaluate("""(topics)=>{const out=[];for(const t of topics)for(const d of [false,true])for(const zr of (t.startsWith('M:')?[10,20,100]:[null])){
            Object.assign(app.sheet,{topic:t,draw:d,mat:true,n:8,gcent:'euro',rows:null}); if(zr) app.sheet.zr=zr;
            const h=buildSheet().html; if(/§/.test(h)) out.push(t+' '+d+' '+zr);} return out}""", topics)
        print('Marker übrig:', left)
        if left: errs.append(f'Marker übrig: {left[:3]}')

        # 2. Zeichnen: erste Aufgabe mit Bild, die anderen leer
        for t, zr, pic, empty in [('M:plus', 20, 'circle', None), ('M:minus', 100, 'svg.matp', '.ab-draw'), ('M:einmaleins', 20, 'svg.dots', '.ab-draw'), ('M:ergaenzen', 10, 'circle', None)]:
            r = await pg.evaluate("""([t,zr,pic,empty])=>{Object.assign(app.sheet,{topic:t,zr,draw:true,mat:true,n:6}); const d=new DOMParser().parseFromString(buildSheet().html,'text/html');
                const ts=[...d.querySelectorAll('.ab-task')]; const seen=new Set(); let bad=0, ex=0;
                for(const x of ts){ const has=!!x.querySelector(pic), em=empty?!!x.querySelector(empty):!x.querySelector(pic); if(has) ex++; else if(!em) bad++; }
                return {n:ts.length, ex, bad, first: !!ts[0].querySelector(pic)}}""", [t, zr, pic, empty])
            print('Zeichnen', t, r)
            if not r['first'] or r['bad'] or r['ex'] > 2: errs.append(f'Zeichnen {t}: {r}')

        # 3. Zehnerpartner: Aufgaben und Lösungen
        bad = await pg.evaluate("""()=>{const out=[];for(let k=0;k<30;k++){Object.assign(app.sheet,{topic:'M:zehnerpartner',draw:false,mat:true,n:12,sol:true});
            const d=new DOMParser().parseFromString(buildSheet().html,'text/html'); const sols=[...d.querySelectorAll('.sol li')].map(l=>l.textContent);
            [...d.querySelectorAll('.ab-task')].forEach((x,i)=>{ const rows=[...x.querySelectorAll('.ab-row')].map(r=>r.textContent.replace(/\\s+/g,' ').trim());
              const want=rows.map(r=>{let m; if(m=r.match(/^(\\d+) \\+ = 10$/)) return 10-m[1]; if(m=r.match(/^\\+ (\\d+) = 10$/)) return 10-m[1]; if(m=r.match(/^10 = (\\d+) \\+$/)) return 10-m[1]; if(m=r.match(/^10 − (\\d+) =$/)) return 10-m[1]; if(m=r.match(/^(\\d+)→/)) return 10-m[1]; return 'X'+r;});
              const got=String(sols[i]).split('; ').map(Number);
              const mt=x.querySelector('.ab-match'); if(mt){ const L=[...mt.querySelectorAll('.l')].map(e=>+e.textContent), R=[...mt.querySelectorAll('.r')].map(e=>+e.textContent);
                if(L.length!==3 || L.some(l=>!R.includes(10-l)) || String(sols[i])!==L.map(l=>l+' – '+(10-l)).join('; ')) out.push('Verbinden falsch: '+L+' / '+R+' = '+sols[i]); return; }
              if(want.join()!==got.join()) out.push(rows.join('|')+' = '+sols[i]);});}
            return out}""")
        print('Zehnerpartner falsch:', bad[:5])
        if bad: errs.append(f'Zehnerpartner: {len(bad)} falsch')

        # 4. Über die 10: Zerlegung stimmt, Beispiel ausgefüllt: je Rechenart genau die erste Aufgabe
        bad = await pg.evaluate("""()=>{const out=[];for(const wop of ['add','sub','both'])for(let k=0;k<20;k++){Object.assign(app.sheet,{topic:'M:ueber10',wop,draw:false,mat:true,n:8,sol:true});
            const d=new DOMParser().parseFromString(buildSheet().html,'text/html'); const ts=[...d.querySelectorAll('.ab-task')]; const seenOp=new Set();
            ts.forEach((x,i)=>{const sp=[...x.querySelector('.ab-ast').children].filter(c=>c.tagName!=='svg').map(c=>c.textContent.trim());
              const [a,o,bb]=[+sp[0],sp[1],+sp[2]]; const ex=x.querySelectorAll('.bsp').length;
              const firstOp=!seenOp.has(o); seenOp.add(o); if(firstOp && ex!==4) out.push('Beispiel nicht ausgefüllt'); if(!firstOp && ex) out.push('Beispiel doppelt');
              if(o==='+' && !(a<10 && a+bb>10)) out.push('kein Übergang '+a+o+bb); if(o==='−' && !(a>10 && a-bb<10)) out.push('kein Übergang '+a+o+bb);
              if(wop==='add'&&o!=='+'||wop==='sub'&&o!=='−') out.push('falsche Rechenart');
              if(ex){ const s=sp.slice(6).filter(v=>v!=='+'&&v!=='−'&&v!=='='); const [p,r,res]=s.map(Number); const ok=o==='+'?(a+p===10&&p+r===bb&&res===a+bb):(a-p===10&&p+r===bb&&res===a-bb); if(!ok) out.push('Beispiel falsch '+sp.join(' ')); }});}
            return out}""")
        print('Über die 10 falsch:', bad[:5])
        if bad: errs.append(f'Über die 10: {len(bad)} Fehler')

        # 5. Geld
        for gc, rx in [('euro', r'^\d+ €$'), ('cent10', r'^\d+,\d0 €$'), ('exact', r'^\d+,\d\d €$')]:
            r = await pg.evaluate("""(gc)=>{const out=[];for(let k=0;k<20;k++){Object.assign(app.sheet,{topic:'M:geld',zr:20,gcent:gc,n:8,sol:true}); const d=new DOMParser().parseFromString(buildSheet().html,'text/html'); out.push(...[...d.querySelectorAll('.sol li')].map(l=>l.textContent)); } return out}""", gc)
            wrong = [x for x in r if not re.match(rx, x)]
            small = sum(1 for x in r if re.search(r',\d[1-9] €$', x))
            print('Geld', gc, len(r), 'falsches Format:', wrong[:3], 'mit 1/2/5 Cent:', small)
            if wrong or (gc == 'exact' and not small) or (gc == 'cent10' and small): errs.append(f'Geld {gc}: {wrong[:3]} / {small}')

        # 6. Einmaleins: nur gewählte Reihen, Schalter im Dialog
        await pg.evaluate("app.sheet.topic='M:einmaleins'; app.sheet.rows=[3]; renderSheets()"); await pg.wait_for_timeout(300)
        await pg.check('[data-shrow="7"]'); await pg.wait_for_timeout(300)
        rows = await pg.evaluate("app.sheet.rows")
        r = await pg.evaluate("""()=>{const out=new Set();for(let k=0;k<20;k++){const d=new DOMParser().parseFromString(buildSheet().html,'text/html'); d.querySelectorAll('.ab-row.big').forEach(x=>{const m=x.textContent.match(/(\\d+) · (\\d+)/); if(m) out.add(+m[2]);});} return [...out].sort((a,b)=>a-b)}""")
        title = await pg.evaluate("buildSheet().title")
        print('Einmaleins Reihen', rows, r, title)
        if sorted(rows) != [3, 7] or r != [3, 7]: errs.append(f'Einmaleins Reihen: {rows} {r}')
        await pg.uncheck('[data-shrow="3"]'); await pg.wait_for_timeout(300); await pg.click('[data-shrow="7"]'); await pg.wait_for_timeout(300)  # letzte Reihe bleibt
        if not await pg.evaluate("app.sheet.rows.length"): errs.append('Einmaleins: alle Reihen abwählbar')

        # 7. Auswahl Materialbilder im Dialog
        await pg.evaluate("app.sheet.topic='M:plus'; app.sheet.rows=null; renderSheets()"); await pg.wait_for_timeout(300)
        await pg.select_option('#sh-matm', 'zeichnen'); await pg.wait_for_timeout(300)
        st = await pg.evaluate("[app.sheet.mat, app.sheet.draw]")
        await pg.select_option('#sh-matm', 'ohne'); await pg.wait_for_timeout(300)
        st2 = await pg.evaluate("[app.sheet.mat, app.sheet.draw]")
        print('Auswahl Materialbilder', st, st2)
        if st != [True, True] or st2[0]: errs.append(f'Auswahl Materialbilder: {st} {st2}')
        await pg.evaluate("app.sheet.mat=true; app.sheet.draw=false")

        # 7b. Minus im Bild: Wegstreichen eingezeichnet oder nur Ausgangsmenge
        for t, zr, wop in [('M:minus', 20, 'both'), ('M:ueber10', 20, 'sub')]:
            r = await pg.evaluate("""([t,zr,wop])=>{const out={};for(const ms of ['gezeigt','selbst']){Object.assign(app.sheet,{topic:t,zr,wop,mstrich:ms,mat:true,draw:false,n:8,sol:false});
                const d=new DOMParser().parseFromString(buildSheet().html,'text/html'); const ts=[...d.querySelectorAll('.ab-task')];
                out[ms]={n:ts.length, kreuz:ts.filter(x=>x.innerHTML.includes('#c9414a')).length, streiche:ts.filter(x=>/Streiche \d+ weg/.test(x.textContent)).length,
                  menge:ts.every(x=>{const a=x.querySelector('.ab-ast') ? +x.querySelector('.ab-ast').children[0].textContent : +x.querySelector('.ab-row.big').textContent.match(/(\d+)/)[1]; return x.querySelectorAll('svg.ab-svg circle').length===a;})};} return out}""", [t, zr, wop])
            print('Minus im Bild', t, r)
            g, sb = r['gezeigt'], r['selbst']
            if g['kreuz'] != g['n'] or sb['kreuz'] or sb['streiche'] != sb['n'] or not sb['menge'] or not g['menge']: errs.append(f'Minus im Bild {t}: {r}')
        await pg.evaluate("app.sheet.topic='M:ueber10'; app.sheet.wop='both'; app.sheet.mstrich='gezeigt'; renderSheets()"); await pg.wait_for_timeout(300)
        if not await pg.locator('#sh-mstrich').count(): errs.append('Auswahl „Minus im Bild“ fehlt')
        await pg.select_option('#sh-mstrich', 'selbst'); await pg.wait_for_timeout(300)
        if await pg.evaluate("app.sheet.mstrich") != 'selbst': errs.append('Auswahl „Minus im Bild“ wirkt nicht')
        await pg.evaluate("app.sheet.wop='add'; renderSheets()"); await pg.wait_for_timeout(300)
        if await pg.locator('#sh-mstrich').count(): errs.append('„Minus im Bild“ bei nur Plus sichtbar')
        await pg.evaluate("app.sheet.mstrich='gezeigt'; app.sheet.wop='both'")

        # 8. Einstellungen bleiben nach dem Neuladen
        await pg.evaluate("app.sheet.topic='M:minus'; renderSheets()"); await pg.wait_for_timeout(300)
        await pg.check('#sh-gross'); await pg.select_option('#sh-matm', 'zeichnen'); await pg.wait_for_timeout(300)
        await pg.reload(); await pg.wait_for_timeout(600)
        st = await pg.evaluate("[app.sheet.topic, app.sheet.gross, app.sheet.draw, app.sheet.pid]")
        print('nach Neuladen', st)
        if st[:3] != ['M:minus', True, True]: errs.append(f'Einstellungen nicht gemerkt: {st}')
        await pg.evaluate("localStorage.removeItem('stufenweise.blatt')")

        # 9. Förderzone R3: Chips Zehnerpartner und Rechnen über die 10
        await pg.evaluate("""(()=>{const p={id:'p_z',name:'Ida',created:Date.now()};data.profiles.push(p);selectProfile(p.id);
            for(const [k,s] of [['R|R2','erreicht'],['R|R3','nicht'],['Z|Z1','erreicht'],['Z|Z2','erreicht'],['Z|Z3','nicht']]) setCell(p.id,k,{status:s,quelle:'test',sum:'x'}); inferCells(p.id,'M'); openSheets('p_z');})()""")
        await pg.wait_for_timeout(500)
        chips = await pg.evaluate("[...document.querySelectorAll('.sh-zones button')].map(b=>[b.textContent, b.dataset.shtopic || zoneToSheet(b.dataset.shzone).topic])")
        print('Chips', chips)
        tops = [c[1] for c in chips]
        for want in ['M:zehnerpartner', 'M:ueber10']:
            if tops.count(want) != 1: errs.append(f'Chip {want}: {tops.count(want)}-mal')
        await pg.click('.sh-zones [data-shtopic="M:zehnerpartner"]'); await pg.wait_for_timeout(300)
        if await pg.evaluate("app.sheet.topic") != 'M:zehnerpartner': errs.append('Chip wirkt nicht')
        print('ERR', errs); await b.close()
asyncio.run(main())
