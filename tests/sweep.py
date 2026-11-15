import asyncio
from playwright.async_api import async_playwright
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
JS = r"""()=>{const keys=[]; for(const zr of [10,20,100,1000]) for(const lv of Object.keys(MATH)) keys.push(`M|${zr}|${lv}`);
for(const [ax,o] of [['S',STELL],['L',READ],['W',WRITE],['U',CLOCK],['G',G_ITEMS],['R',R_ITEMS],['P',PHON]]) for(const k of Object.keys(o)) keys.push(`${ax}|${k}`);
const strip=s=>String(s??'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim(); const bad=[]; let n=0;
for(const k of keys){ let fs; try{fs=itemsFor(k);}catch(e){bad.push(k+' itemsFor EXC '+e);continue;} if(!fs){bad.push(k+' none');continue;}
 const arr=Array.isArray(fs)?fs:Object.values(fs);
 for(let i=0;i<arr.length*25;i++){ let it; try{ const f=arr[i%arr.length]; it=typeof f==='function'?f():f; }catch(e){bad.push(k+' gen EXC '+String(e).slice(0,80)); continue;} n++;
  const all=JSON.stringify(it); if(/undefined|NaN/.test(all)) bad.push(k+' UNDEF '+strip(it.label));
  if(it.type==='choice'){ const t=it.options.map(o=>strip(o.h)+'|'+String(o.a)); if(new Set(t).size!==t.length) bad.push(k+' DUP '+strip(it.label)+' :: '+t.join(' / ').slice(0,150)); if(it.correct<0||it.correct>=it.options.length) bad.push(k+' BADCORRECT '+strip(it.label)); if(it.options.length<2) bad.push(k+' FEWOPT '+strip(it.label));
   for(const o of it.options){ const m=strip(o.h).match(/\b\d{1,2}:(\d\d)\b/g); if(m) for(const x of m) if(+x.split(':')[1]>59) bad.push(k+' BADTIME '+x+' '+strip(it.label)); } }
  if(it.fields) for(const f of it.fields) if(typeof f==='number' && (f<0||!isFinite(f))) bad.push(k+' NEGFIELD '+strip(it.label)+' '+JSON.stringify(it.fields));
 }}
return [n, [...new Set(bad)]];}"""
async def main():
    async with async_playwright() as p:
        b=await launch(p); pg=await b.new_page()
        await pg.goto(URL); await pg.wait_for_timeout(300)
        n,bad=await pg.evaluate(JS); print('items',n,'issues',len(bad))
        for x in bad[:80]: print(' ',x)
        await b.close()
asyncio.run(main())
