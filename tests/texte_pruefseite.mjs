import fs from 'fs'; import vm from 'vm';
const ctx = {}; vm.createContext(ctx);
/* Prüfseite für neue Texte (Backlog J, Schritt 4) aus index.html erzeugen: node tests/texte_pruefseite.mjs ZIELDATEI.html */
const app = fs.readFileSync(new URL('../index.html', import.meta.url), 'utf8');
for(const [name, end] of [['TEXTS_NEU', '\n];'], ['TEXTS_MID', '\n];'], ['LONG_NEU', '\n];'], ['STORIES', '\n};']]){ const i = app.indexOf(`const ${name} =`), j = app.indexOf(end, i) + end.length; vm.runInContext(app.slice(i, j).replace(`const ${name} =`, `this.${name} =`), ctx); }
const {TEXTS_NEU, TEXTS_MID, LONG_NEU, STORIES} = ctx;
const e = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const words = t => t.split(/\s+/).filter(Boolean).length;
const qMc = qs => `<ol class="qs">${qs.map(([q, o]) => `<li><b>${e(q)}</b> <span class="ok">✓ ${e(o[0])}</span>${o.slice(1).map(x => `<span class="no">${e(x)}</span>`).join('')}</li>`).join('')}</ol>`;
const qLong = qs => `<ol class="qs">${qs.map(([k, p, q, r, ...w]) => `<li><b>${e(q)}</b> <span class="ok">✓ ${e(r)}</span>${w.map(x => `<span class="no">${e(x)}</span>`).join('')} <small>${e(k)}${p ? `, Absatz ${p}` : ''}</small></li>`).join('')}</ol>`;
const world = w => w ? '<small class="tag">Hauptstufe/Berufsschulstufe</small>' : '';
const stories = Object.values(STORIES).map(S => `<section class="story"><h3>${e(S.t)}</h3>${S.parts.map((p, i) => `<article><h4>Teil ${i + 1}: ${e(p.t)} <small>${words(p.p.join(' '))} Wörter</small></h4>${p.p.map(x => `<p>${e(x)}</p>`).join('')}<div class="tasks"><p class="lab">Fragen</p>${qMc(p.q.map(([q, ...o]) => [q, o]))}<p class="lab">Richtig oder falsch?</p><ul class="rf">${p.rf.map(([x, ok]) => `<li>${e(x)} <span class="${ok ? 'ok' : 'no2'}">${ok ? 'richtig' : 'falsch'}</span></li>`).join('')}</ul><p class="lab">Schreiben</p><p>${e(p.schreib)}</p></div></article>`).join('')}</section>`).join('');
const kurz = TEXTS_NEU.map((t, i) => `<article class="k"><p class="nr">K${i + 1} ${world(t.w)}</p><p class="tx">${e(t.text)}</p>${qMc(t.qs)}</article>`).join('');
const mid = TEXTS_MID.map((t, i) => `<article><h4>M${i + 1}: ${e(t.t)} ${world(t.w)} <small>${words(t.text)} Wörter</small></h4><p class="tx">${e(t.text)}</p>${qMc(t.qs)}</article>`).join('');
const lang = LONG_NEU.map((t, i) => `<article><h4>L${i + 1}: ${e(t.t)} <small>${e(t.g)}</small> ${world(t.w)}</h4>${t.head ? `<p class="head">${e(t.head)}</p>` : ''}${t.p ? t.p.map(x => `<p>${e(x)}</p>`).join('') : `<div class="chat">${t.chat.map(([w, x, r]) => `<p class="${r ? 'r' : ''}"><b>${e(w)}:</b> ${e(x)}</p>`).join('')}</div>`}${qLong(t.q)}</article>`).join('');
const nStory = Object.values(STORIES).reduce((s, S) => s + S.parts.length, 0);
const html = `<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neue Texte zum Durchsehen</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Spectral:wght@500;600&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
/* VOICE: ruhiges Prüfdokument für eine Lehrkraft, sachlich.
   IDEA: ein Korrekturbogen – Texte wie im Heft, Antworten markiert.
   PICTURE: die Texte selbst, als Seiten mit Randnotizen (Fragen).
   COLOUR and TYPE: Weiß, Tinte, Ultramarin als Akzent; Spectral + Inter.
   LAYOUT: eine Lesespalte, Abschnittslinks oben, Fragen eingerückt. */
:root{color-scheme:light dark;--bg:light-dark(#fff,#0d0e18);--ink:light-dark(#14110f,#e9e7f2);--mut:light-dark(#5d5a66,#a3a0b4);--acc:light-dark(#1d2bd8,#8f99ff);--line:light-dark(#e2e0ea,#262840);--soft:light-dark(#f4f4fb,#161828);--ok:light-dark(#1f6b3d,#7fd3a0)}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,sans-serif;overflow-x:clip}
main{max-width:860px;margin:0 auto;padding:clamp(24px,4vw,56px) max(5vw,16px)}
h1,h2,h3,h4{font-family:Spectral,Georgia,serif;font-weight:600;line-height:1.15;text-wrap:balance}h1{font-size:clamp(32px,5vw,46px);margin:0 0 12px}h2{font-size:30px;margin:56px 0 8px;padding-top:12px;border-top:2px solid var(--ink)}h3{font-size:24px;margin:32px 0 8px;color:var(--acc)}h4{font-size:19px;margin:0 0 6px}
small{font:400 13px Inter,sans-serif;color:var(--mut);margin-left:6px}.tag{border:1px solid var(--line);border-radius:10px;padding:1px 7px}
.lead{font-size:18px;max-width:68ch}.nav{display:flex;flex-wrap:wrap;gap:8px 18px;margin:18px 0 0;padding:12px 0;border-block:1px solid var(--line)}.nav a{color:var(--acc);font-weight:600;text-decoration:none}
article{padding:18px 0;border-bottom:1px solid var(--line)}article p{margin:0 0 8px;max-width:70ch}.tx{font-size:17px}
.qs{margin:6px 0 0;padding-left:22px;font-size:14.5px;color:var(--ink)}.qs li{margin:3px 0}.qs span{display:inline-block;margin:0 8px 0 4px}.ok{color:var(--ok);font-weight:600}.no{color:var(--mut)}.no2{color:#b3261e;font-weight:600}
.tasks{background:var(--soft);border-radius:8px;padding:10px 14px;margin-top:10px}.lab{font-weight:600;font-size:13px;color:var(--mut);margin:8px 0 2px!important}.rf{margin:0;padding-left:20px;font-size:14.5px}
.k{display:grid;grid-template-columns:52px minmax(0,1fr);gap:0 12px}.k .nr{grid-row:span 2;font:600 15px Spectral,serif;color:var(--acc)}.k .nr small{display:block;margin:4px 0 0;font-size:10px}
.chat p{background:var(--soft);border-radius:10px;padding:6px 10px;max-width:80%}.chat p.r{margin-left:auto}.head{font-size:13px;color:var(--mut)}
table{border-collapse:collapse;width:100%;font-size:15px}td,th{border-bottom:1px solid var(--line);padding:10px 8px;text-align:left;vertical-align:top}th{font-size:13px;color:var(--mut)}td.ans{width:30%;background:var(--soft)}
@media(max-width:600px){.k{grid-template-columns:1fr}.k .nr{grid-row:auto}}
</style></head><body><main>
<h1>Neue Texte für die Arbeitshefte</h1>
<p class="lead"><b>Für Backlog J, Schritt 4.</b> ${nStory} Teile Fortsetzungsgeschichte, ${TEXTS_NEU.length} neue Kurztexte, ${TEXTS_MID.length} mittlere Texte und ${LONG_NEU.length} neue längere Texte, jeweils mit Fragen. Die richtige Antwort ist grün mit ✓ markiert. Von Stefan durchgesehen und freigegeben am 26.11.2026.</p>
<p>So kannst du antworten: Kommentare direkt hier auf der Seite, oder im Chat zum Beispiel „K12: Satz 2 ändern in …“. Ein „Passt“ genügt auch.</p>
<nav class="nav"><a href="#geschichten">Geschichten</a><a href="#kurz">Kurztexte</a><a href="#mittel">Mittlere Texte</a><a href="#lang">Längere Texte</a><a href="#fragen">Fragen an dich</a></nav>
<h2 id="geschichten">Fortsetzungsgeschichten</h2><p>Im Deutsch-Heft (und im gemischten Heft) kommt etwa alle 6–8 Seiten ein Teil: eine Seite Text, eine Seite Aufgaben (Fragen, richtig/falsch, ein Satz schreiben). Bei 24 Seiten sind es 3 Teile, bei 48 Seiten alle 6. Die Lehrkraft wählt die Geschichte im Heft-Assistenten.</p>${stories}
<h2 id="kurz">Kurztexte (2–4 Sätze)</h2><p>Für „Texte lesen und verstehen“ (L7), auch beim Üben in der App. Dazu kommen dort zwei neue Aufgabenarten mit denselben Texten: Wörter im Text unterstreichen und Sätze in die richtige Reihenfolge bringen.</p>${kurz}
<h2 id="mittel">Mittlere Texte (5–8 Sätze)</h2><p>Auf den schwereren Seiten eines Kapitels „Texte lesen und verstehen“ (Feinstufe ab der Mitte) statt der Kurztexte.</p>${mid}
<h2 id="lang">Längere Texte</h2><p>Für „Längere Texte verstehen“ (L9), zusätzlich zu den 26 vorhandenen. Hinter jeder Frage steht die Frageart (Information finden, Warum, Schlussfolgern, Thema) und der Absatz.</p>${lang}
<h2 id="fragen">Fragen an dich</h2>
<table><tr><th>#</th><th>Frage</th><th>Mein Vorschlag</th><th>Deine Antwort</th></tr>
<tr><td>1</td><td>Ab welcher Stufe soll die Fortsetzungsgeschichte ins Heft?</td><td>nur wenn die Förderzone bei Lesen L6 (Sätze verstehen) oder höher bzw. Schreiben W5/W6 liegt; darunter keine Geschichte</td><td class="ans">wie vorgeschlagen</td></tr>
<tr><td>2</td><td>Sollen die neuen Texte auch beim Üben in der App vorkommen (nicht nur im Heft)?</td><td>ja, Kurztexte und längere Texte auch in der App</td><td class="ans">wie vorgeschlagen</td></tr>
<tr><td>3</td><td>Passen Themen und Namen zu deiner Lerngruppe? Gibt es Themen, die fehlen oder nicht passen?</td><td>–</td><td class="ans">Die Texte sind gut.</td></tr>
</table>
<p><small>Stufenweise · Entwurf vom 25.11.2026, freigegeben von Stefan am 26.11.2026</small></p>
</main></body></html>`;
fs.writeFileSync(process.argv[2] || 'texte_pruefseite.html', html);
console.log(html.length, TEXTS_NEU.length, TEXTS_MID.length, LONG_NEU.length, nStory);
