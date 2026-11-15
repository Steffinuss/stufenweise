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
        topics = await pg.evaluate("[...document.querySelectorAll('#sh-topic option')].map(o=>o.value).filter(t=>!t.startsWith('K:'))")
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
              const got=String(sols[i]).split('; ').map(Number); if(want.join()!==got.join()) out.push(rows.join('|')+' = '+sols[i]);
              const o=x.querySelectorAll('.ab-opt'); if(o.length && ![...o].some(e=>+e.textContent===got[0])) out.push('Partner fehlt in Auswahl: '+rows);});}
            return out}""")
        print('Zehnerpartner falsch:', bad[:5])
        if bad: errs.append(f'Zehnerpartner: {len(bad)} falsch')

        # 4. Über die 10: Zerlegung stimmt, Beispiel ausgefüllt, nur das erste
        bad = await pg.evaluate("""()=>{const out=[];for(const wop of ['add','sub','both'])for(let k=0;k<20;k++){Object.assign(app.sheet,{topic:'M:ueber10',wop,draw:false,mat:true,n:8,sol:true});
            const d=new DOMParser().parseFromString(buildSheet().html,'text/html'); const ts=[...d.querySelectorAll('.ab-task')];
            ts.forEach((x,i)=>{const sp=[...x.querySelector('.ab-ast').children].filter(c=>c.tagName!=='svg').map(c=>c.textContent.trim());
              const [a,o,bb]=[+sp[0],sp[1],+sp[2]]; const ex=x.querySelectorAll('.bsp').length;
              if(i===0 && ex!==4) out.push('Beispiel nicht ausgefüllt'); if(i>0 && ex) out.push('Beispiel doppelt');
              if(o==='+' && !(a<10 && a+bb>10)) out.push('kein Übergang '+a+o+bb); if(o==='−' && !(a>10 && a-bb<10)) out.push('kein Übergang '+a+o+bb);
              if(wop==='add'&&o!=='+'||wop==='sub'&&o!=='−') out.push('falsche Rechenart');
              if(i===0){ const s=sp.slice(6).filter(v=>v!=='+'&&v!=='−'&&v!=='='); const [p,r,res]=s.map(Number); const ok=o==='+'?(a+p===10&&p+r===bb&&res===a+bb):(a-p===10&&p+r===bb&&res===a-bb); if(!ok) out.push('Beispiel falsch '+sp.join(' ')); }});}
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
        print('ERR', errs); await b.close()
asyncio.run(main())
