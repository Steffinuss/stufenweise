# Backlog

Geplante Entwicklungsaufgaben für Stufenweise. Begonnenes steht in `IN_PROGRESS.md`, Erledigtes in `CHANGELOG.md`.

Regeln (Stand 17.11.2026): Der Funktionsumfang von `main` ist eingefroren, weil die App an Schulen genutzt wird. Neues entsteht nur im Zweig `entwicklung`, wird in der Testversion gezeigt und erst nach Stefans OK freigegeben (`docs/entwicklung.md`). Didaktische Entscheidungen trifft Stefan.

Stand: 28.11.2026 (0.44.0 freigegeben mit V Drucken auf iPad/iPhone)

## Vorgeschlagene Reihenfolge

| Nr. | Aufgabe | Größe | Warum an dieser Stelle |
| --- | --- | --- | --- |
| 0 | Basis-Test abschließen (`IN_PROGRESS.md`) | klein | fertig gebaut, braucht nur Ausprobieren und Freigabe |
| 1 | ~~**C** Basis: bessere Progression~~ | mittel | freigegeben in 0.29.0 (20.11.2026), siehe `CHANGELOG.md` |
| 2 | ~~**B** Unterricht: Zahl im Zwanzigerfeld~~ | klein | freigegeben in 0.29.0 (20.11.2026), siehe `CHANGELOG.md` |
| 3 | ~~**A** Plus und Minus aufteilen~~ | groß | freigegeben in 0.29.0 (20.11.2026), siehe `CHANGELOG.md` | 
| 4 | ~~**D** Materialkiste (Hilfen für Schüler*innen)~~ | mittel | freigegeben in 0.30.0 (20.11.2026), siehe `CHANGELOG.md` |
| 5 | ~~**E** QR-Umzug schneller (+ Fehler F2)~~ | mittel | freigegeben in 0.31.0 (23.11.2026), zusammen mit F3 (Druck wie Vorschau), siehe `CHANGELOG.md` |
| 6 | ~~**G** Hundertertafel-Blätter: Bezug zur Tafel sichtbar (+ Heft zur Förderzone)~~ | klein | freigegeben in 0.32.0 (23.11.2026), siehe `CHANGELOG.md` |
| 7 | ~~**H** Konzentrationsmodus für Kinder (+ Usability-Review)~~ | klein bis mittel | freigegeben in 0.33.0 (24.11.2026), siehe `CHANGELOG.md` |
| 8 | ~~**I** Optimierung Deutsch (Bilder beim Schreiben, Anhören, Ausbau) + Hundertertafel verdeckt, Mathe mit Material~~ | groß | freigegeben in 0.34.0 (24.11.2026), siehe `CHANGELOG.md` |
| 9 | ~~**J** Arbeitshefte, die aufeinander aufbauen + **K** Fußzeile ohne Namen~~ | groß | freigegeben in 0.38.0 (26.11.2026), siehe `CHANGELOG.md` |
| 10 | ~~**O1** Voller Speicher melden, **P1** Safari-Tab auf dem iPad, **Q1** Raten im Test~~ | klein | Datensicherheit aus der Prüfung vom 22.11.; O1 freigegeben in 0.38.1, P1 und Q1 in 0.39.0 |
| 11 | ~~**N** Große Aufgaben im Heft-Assistenten~~ | klein | freigegeben in 0.39.0 (26.11.2026) |
| 12 | ~~**M** Blätter im Heft-Design~~, dann ~~**L** Lineatur~~ | klein bis mittel | M freigegeben in 0.40.0 (26.11.); L freigegeben in 0.41.0 (27.11.) |
| 13 | ~~**S** Rückmeldungen Blätter und Hefte~~ | klein bis mittel | freigegeben in 0.41.0 (27.11.2026) |
| 14 | ~~**U** Arbeitshefte stringenter (U1–U3)~~ | mittel | freigegeben in 0.42.0 (27.11.2026) |
| 15 | **T** Basis-Arbeitsblätter überarbeiten | mittel | **erledigt** in 0.43.0 (28.11.2026) |
| 16 | **V** Drucken auf iPad und iPhone | klein | **erledigt** in 0.44.0 (28.11.2026) |

Alternative: B zuerst als schneller Gewinn, während Stefan den Basis-Test ausprobiert.

---

## I: Optimierung Fach Deutsch

**Status:** erledigt, freigegeben in 0.34.0 (24.11.2026). Dokument „Stufenweise – Optimierung Deutsch“ (claude.ai/artifact/UWNJUi6e6cFP7h7W7ugtdx).
**Anlass (Stefan, 24.11.):** In Deutsch ist deutlich weniger als in Mathe. Beim Schreiben müssen Kinder Wörter schreiben, ohne sie zu kennen; manchmal erkennen sie die Bilder nicht. „Vielleicht wäre an dieser Stelle doch eine Sprachausgabe als Hilfe gut.“

**Befund (gezählt in 0.33.0):**
- Stufen mit Übungen: Mathe 51 (M 20, R 7, H 7, U 6, S 4, G 4, Z 3), Deutsch 15 (L 9, W 6) plus LX/WX. Arbeitsblätter 34 zu 16, Legeblätter 9 zu 6, Tafelwerkzeuge 7 zu 1 (`tword`), Materialkiste 7 zu 0.
- Hören P1–P4: `P_LEVELS`, `L_INFO.P1–P4`, `HEAR_RAIL` und eine Lernstandszeile gibt es, aber `PHON = {}` (keine Übungen, kein Test).
- Schreiben zeigt nur Bild + Kästchen + Tastatur (`writeStage`). Falsches Wort → „Noch nicht. Sprich das Wort langsam mit.“ und zählt wie ein Schreibfehler.
- 12 Schreibwörter nicht in `CLEAR`: `LAUT_SHORT` Lama, Rabe, Schal, Limo, Lupe, Dose; `LAUT_LONG` Kamel, Nudel, Melone; `MERK` Tonne, Decke, Pfanne. Der Schreib-Test (`writePlan`) nutzt dieselben Listen. `CLEAR` selbst enthält Tulpe/Rose/Blume und Tasse/Kanne.
- Sprachausgabe wurde entfernt (`speak()` leer, „Qualität der Gerätestimmen reicht nicht“); `germanVoices`, `bestVoice`, `settings.voice`, `#btn-say` und die Aufbereitung gesprochener Zahlen sind noch im Code. Feste Regel „Keine Sprachausgabe“ – nur Stefan kann sie ändern.

**Vorschläge (Details im Dokument):**
- Ohne Ton: H1 nur `CLEAR` beim Schreiben (Üben + Test); H2 Knopf „Kenne ich nicht“ (a: anderes Bild, zählt nicht; b: Wort kurz zeigen, dann aus dem Gedächtnis, zählt „mit Hilfe“), Lernstand sammelt nicht erkannte Bilder als Wortschatzliste, nie als Schreibfehler; H3 Bilder vor einer Runde kennenlernen + Blatt „Bildkarten mit Wort“; H4 Bilder für die Klasse abwählen.
- Mit Ton: Knopf „Anhören“ neben dem Bild, nur das Wort. A Gerätestimme nur mit `localService`-Stimmen (nichts ins Internet); B eigene Aufnahmen der ~110 Bildwörter als Teil der App (~1 MB, offline), evtl. zusätzlich in Silben; Mischung möglich (Gerätestimme nur für „Meine Wörter“). Lehrkraft schaltet ein (alle oder je Kind).
- Ausbau: D1 Hören P1–P4 mit Übungen, D2 Silben beim Schreiben (W4 Kästchen unter Silbenbögen, Silbenkarten legen), D3 Deutsch in der Materialkiste (Anlauttabelle, Bildwörterbuch, Wörter legen), D4 Deutsch im Unterricht (Anlauttabelle, Blitzlesen, Satz-Baukasten), D5 Schreiben im Alltag (Einkaufszettel, eigener Satz), D6 Arbeitsblätter (Silben zählen, Reime, Anlaut-Bilder, Bildkarten).

**Stefans Antworten (im Dokument, 24.11.):** 1 ja, Üben und Test · 2 wie vorgeschlagen „oder beides gelten lassen“ → herausgenommen · 3 b beim Üben, a im Test · 4 ja, Knopf für die Lehrkraft · 5 ganze Klasse · 6 „erstmal A testen, evtl. später eigene Aufnahmen“ · 7 im Test ja, je Kind · 8 D2, D1, D3, D6, D4, D5 · 9 „Ja, auch im Test prüfen“. Dazu (24.11.): Hundertertafel „Finde Zahl“ auch abgedeckt und teilabgedeckt.
**Damit geändert:** feste Regel „Keine Sprachausgabe“ gilt nicht mehr für „Anhören“ (nur das Wort, nur Gerätestimmen); Rückmeldungen werden weiter nicht vorgelesen.
**Umsetzung:** `W_AMBIG`, `wClear`, `wPool`, `wPick`, `W_POOLS`, `settings.wHide`, `wUnkOk` (`r-unk`, Test `d-unk` mit `unkFrom`, `d.unkK`), `unkWords` (Log-Feld `unk`), `wPreviewStart`/`app.read.wq`; Anhören `sayOn`/`sayWord`/`speechBtn`/`sayMini` (nur `localService`), `settings.anhoeren`, `p.say`; W4 `syl` (Kästchen `w-sylg`), `sylCardItem`, `WRITE_PRACTICE`; Hören `PHON` (P1–P4), `RHYME`, Lese-Test `readPlan` (Hören, wenn L4 nicht erreicht), `cap:40`; Kiste `abc`/`dict`/`tword` (`subj:'D'`, `kisteLine(pid, sj)`); Unterricht `abc`/`tblitz`/`tsatz`; Blätter `P_SHEETS`, Legeblatt `bildk`; W6 `shopItem`, `satzItem` (`check:'satz'`, `free`); Hundertertafel `hCover`, `hcovTrack`, `p.hcov`. Test `tests/deutsch_optimierung.py`.

---

## H: Konzentrationsmodus für Kinder

**Status:** erledigt, freigegeben in 0.33.0 (24.11.2026).
**Anlass (Stefan, 24.11.):** Beim Wechselgeld ist der Bildschirm sehr voll. Idee: eine Art „Fullscreen-Modus“, damit sich Kinder nur auf die Aufgabe konzentrieren.
**Befund (Usability-Review 24.11., Dokument „Stufenweise – Usability-Review“, claude.ai/artifact/AdqPQacwdjd3vDwH9zfaQx):** Wechselgeld auf dem iPad: 30 Knöpfe sichtbar, 7 gehören zur Aufgabe; vier Anweisungen gleichzeitig; Rechnung „10 € − 7 €“ zum Auftrag „Ergänze“.
**Vorschlag:** Bereichsleiste, Einstellleiste, Name und Menü ausblenden; ein Satz Auftrag, Tipp erst nach Fehlversuch; Fortschritt groß („3 von 10“); Knopf „Pause“ zurück zu „Heute für dich“; Einstellung wie „Geführte Oberfläche“ (alle oder einzelne Kinder), Lehrkraft mit PIN. Bausteine vorhanden (Leiste ausblenden, abgedunkelte Leiste im Test, PIN, Runden).
**Stefans Antworten (im Dokument, 24.11.):** für alle Kinder und automatisch an; „Weiter“ nach 2 Fehlversuchen; Wechselgeld-Rechnung erst nach dem Legen; keine Handys im Unterricht. „Bitte baue das alles ein“ (Empfehlungen 1–12).
**Umsetzung:** `settings.fokus` ('on'/'off', Standard 'on'), `fokusBase`/`fokusTask`/`fokusClass`/`fokusSync`, `#fokus-bar` (Punkte, `#fk-next`, `#fk-pause`, `#fk-teacher` mit `requireTeacher` → `app.fokusAus` bis `goHome`), `fkState()` je Bereich (gelöst, Fehlversuche), `#m-next/#w-next/#t-next` erst nach Lösung oder 2 Fehlversuchen („Weiter“), `body.fokus`/`body.fokus-home` blenden Leiste, Einstellleiste und Darstellungswahl aus. Willkommen: Aufgabe startet von selbst, Geld mit Kacheln (`data-fk-money`). Zählaufgabe `countOn`/`countCheck` (Protokoll `count`). Wechselgeld, Rundenende, Startseite, Uhr, Mathe/Deutsch, Materialkiste, Lernstand-Sprungmarken (`statsJump`), Druckhilfe (`details.sh-help`). Tests `tests/konzentrationsmodus.py`; Tests mit voller Oberfläche schalten den Modus über `FOKUS_AUS` (tests/common.py) aus.
**Nicht umgesetzt (Empfehlung 7):** Einerwürfel und Zehnerstangen lassen sich nicht sinnvoll größer antippen: Die Tippflächen füllen die Lücken schon aus (Würfel 25 px), mehr ginge nur mit größerem Material und damit weniger Platz.

---

## G: Hundertertafel-Blätter – Bezug zur Tafel sichtbar

**Status:** erledigt, freigegeben in 0.32.0 (23.11.2026). Schwarz-Weiß für Zwanzigerfeld-Blätter (Plus: hell- und dunkelgrau) hat Stefan am 23.11. bewusst nicht gewollt: „Hell und dunkelgrau klappt“.
**Anlass (Stefan, 23.11.):** Bei Blättern wie „Nachbarn und Lücken“ sieht man nicht, dass es um die Hundertertafel geht.
**Stefans Wahl:** Titel ergänzen, Hinweis mit Tafel-Bild, ausgefüllte Hundertertafel als Extraseite – nur auf Wunsch (Häkchen).

**Umsetzung:** Blätter H1–H6 (nicht Tausenderbuch, nicht Material-Blätter):
- Titel: „Hundertertafel und Material verbinden“, „Nachbarn und Lücken in der Hundertertafel“, „Ausschnitte aus der Hundertertafel ergänzen“, „Wege gehen: Plus und Minus an der Hundertertafel“, „Muster in der Hundertertafel erkennen“ (H1 hatte die Tafel schon im Titel). Die Namen der Stufen in der App und im Lernstand bleiben gleich.
- Über den Aufgaben steht vor den Zeichen-Erklärungen ein kleines Tafel-Bild mit „Hundertertafel“.
- Häkchen „Ausgefüllte Hundertertafel als Extraseite zum Nachschauen“ (aus, wird gemerkt): Seite „Hundertertafel zum Nachschauen“ nach dem Blatt, vor den Lösungen; „Ins Arbeitsheft“ übernimmt sie als eigene Heftseite.
- Test `tests/hundertertafel_blaetter.py`.

**Nachtrag (Stefan, 23.11.):** Auch beim automatisch erstellten **Heft zur Förderzone** sollen „Schwarz-Weiß-Druck“ und die Hundertertafel als Extraseite wählbar sein, die Tafel nur, wenn Hundertertafel-Aufgaben im Heft sind.
- Umsetzung: Häkchen im Kasten „Heft zur Förderzone“ (`app.heft.bw`, `app.heft.taf`, gemerkt). Schwarz-Weiß nur sichtbar, wenn Basis-Zonen dabei sind (wirkt nur auf Basis-Blätter). Tafel nur sichtbar und nur angehängt, wenn eine Zone zu H1–H6 dabei ist; einmal als letzte Heftseite (auch bei 2 Blättern je Stufe). Die Einstellungen des Einzelblatts bleiben unberührt. Test `tests/heft_zone_optionen.py`.

---

## D: Materialkiste – Hilfen für Schüler*innen als eigenes Modul

**Status:** erledigt 20.11.2026, freigegeben in 0.30.0 (Stefan: „Sieht gut aus“).
**Wunsch Stefan (20.11.):** Die Rechenhilfe soll kein Teil von Mathe/Plus-Minus sein, sondern ein ganz unabhängiges Modul, „quasi wie ein Taschenrechner, Materialvorrat usw.“ für Schüler*innen.

**Ausgangslage:**
- Rechenhilfe seit 0.29.0: `app.calc` innerhalb von Plus/Minus, eigener Eintrag in der Mathe-Leiste vor „Schriftlich“ (`homeAreasMath`), für alle Kinder sichtbar. Eigene Aufgabe eingeben, Plus/Minus und Darstellung frei wählen. Übungen werden protokolliert (`logAttempt`), aber ohne „Schwerer/Leichter“.
- „Frei legen“ (`free`) ist schon ein Materialvorrat und bleibt nach dem Test immer sichtbar.
- Für die Tafel gibt es acht Werkzeuge ohne Namen und ohne Speichern (`CLASS_TOOLS`: Zahlen, Zwanzigerfeld, Zahlenstrahl, Hundertertafel, Frei legen, Blitzblick, Uhr, Wörter mit Silben). Diese könnten für Schüler*innen wiederverwendet werden, ohne neue Architektur.

**Idee:** eigener Bereich mit Werkzeugen, die ein Kind nutzt, wenn es eine Aufgabe (z. B. vom Arbeitsblatt oder aus dem Alltag) hat: kein Lernstand, keine Tests, keine Förderzone.

**Entscheidungen Stefan (20.11.):**
- Ort: eigener Eingang auf der Startseite neben Üben und Testen, unabhängig vom Fach.
- Inhalt: Rechenhilfe Plus/Minus, Materialvorrat (Frei legen mit Material, Würfeln, Geld), Zwanzigerfeld, Hundertertafel, Zahlenstrahl, Uhr (wie an der Tafel) und neu ein einfacher Taschenrechner (große Tasten, Ergebnis wahlweise auch als Material).
- Speichern: nur die Nutzung zählen (z. B. „Rechenhilfe 5× genutzt“) für Lernstand und ILEB; keine einzelnen Aufgaben, keine Ergebnisse, keine Förderzone.
- Sichtbarkeit: für alle Kinder immer.

**Weitere Entscheidungen Stefan (20.11.):** Name „Materialkiste“; Rechenhilfe fällt in der Mathe-Leiste weg; Taschenrechner mit + − · : und Zahlen bis 10 000.

**Umsetzung:** vierte Kachel auf der Startseite → „Wer bist du?“ (mit Gast) → Werkzeugauswahl; in der Kiste eigene Leiste mit „Fertig“. Die Tafel-Werkzeuge laufen unverändert (`TOOL_MODES`), die Rechenhilfe wie bisher (`app.calc`). In der Kiste (`app.kiste`) keine Lenkung (`guideFix`), kein gesperrter Zahlenraum, keine Runden, kein `logAttempt`/`noteError`/`logSkip`. `kisteCount` zählt das Öffnen je Werkzeug in `data.kiste`. Taschenrechner `tcalc`: eine Rechnung nach der anderen, Weiterrechnen mit dem Ergebnis, geteilt mit Rest, Material nur für ganze Ergebnisse 0–10 000. Lernstand (`statsSections`, `kisteLine`) und ILEB Mathe (`zoneReport`). Test `tests/materialkiste.py`.

**Ursprüngliche Fragen:**
1. Ort: eigener Eingang auf der Startseite (neben Üben und Testen) oder eigene Gruppe in der Leiste, die in jedem Fach zu sehen ist.
2. Inhalt: Rechenhilfe (Plus/Minus), Materialvorrat, Zwanzigerfeld, Hundertertafel, Zahlenstrahl, Uhr, Geld, Wörter/Silben; ein echter Taschenrechner (große Tasten, Ergebnis wahlweise auch als Material)?
3. Speichern: ohne Ergebnisse wie an der Tafel, oder Nutzung mitschreiben (z. B. „hat die Rechenhilfe 5× genutzt“) für Lernstand/ILEB.
4. Sichtbarkeit: immer für alle Kinder, oder je Kind von der Lehrkraft ein- und ausschaltbar (wie das Basis-Häkchen).
5. Name für Kinder: „Hilfen“, „Werkzeugkiste“ o. Ä.
6. Rechenhilfe danach aus der Mathe-Leiste nehmen oder an beiden Stellen lassen.

---

## E: QR-Umzug schneller (mit Fehler F2)

**Status:** erledigt, freigegeben in 0.31.0 (23.11.2026). Stefan hat Mac → iPad getestet: „funktionieren hervorragend“. Umgesetzt wie unten vorgeschlagen; gemessen: 6 Kinder × 800 Übungen 25 statt 148 Codes, ≈ 10 statt 96 s je Durchlauf.
**Anlass (Stefan, 23.11.):** Umzug von 6 Kindern Mac → iPad braucht 109 QR-Codes; klappt gut, dauert aber. Frage: mehr Information pro Code oder schnelleres Wechseln?

**F2 – Fehler:** `qrPayload(…, keep)` kürzt die Übungen mit `l.slice(-keep)`. Bei `keep = 0` liefert `slice(-0)` die ganze Liste. Die App zeigt „von jedem Kind die letzten 0 Übungen“, überträgt aber alle Übungen; `maxParts: 60` greift dadurch nicht (bei Stefan 109 Teile). Nicht allein beheben: Dann gingen beim Umzug wirklich alle Übungen verloren. Gemeinsam mit E lösen.

**Messungen (23.11.):**
- Heute: 230 Bytes je Code, Fehlerkorrektur M (61 × 61 Module), Wechsel alle 650 ms. 109 Teile ≈ 25 KB ≈ 71 s je Durchlauf.
- Eigener QR-Leser (`QR.scan`) liest im Test (720 px, leichte Unschärfe, Rauschen) Codes bis 1.000 Bytes mit Fehlerkorrektur L (105 × 105 Module) sicher, auch bei nur 3 px je Modul, in 10–30 ms.
- Übungen spaltenweise statt als einzelne Objekte verpackt (Zeitabstände statt Zeitstempel, Rechenart als Nummer): nach Deflate 3,4 statt 6,4 Bytes je Eintrag (Faktor 1,9).

**Vorschlag:**
1. Mehr pro Code: etwa 700 Bytes mit Fehlerkorrektur L (≈ 3× heute). Schalter „Kleine Codes“ als Rückfall, falls eine Kamera nicht mitkommt.
2. Kompakter packen: Übungen spaltenweise (Format `v:2`; der Empfänger liest weiter auch `v:1`).
3. Schneller wechseln: etwa 400 ms statt 650 ms; Empfänger wertet Bilder mit 960 statt 720 px aus.
4. F2 beheben: Kürzen der Übungen erst, wenn es auch dann noch über der Grenze liegt, und dann ehrlich anzeigen.
Erwartung für Stefans Fall: etwa 20 statt 109 Codes, ein Durchlauf etwa 8 s statt 71 s. Muss auf echten Geräten (Mac-Bildschirm → iPad-Kamera) geprüft werden.

---

## F1: Fehler – Kinder weg nach „Jetzt aktualisieren“ (mehrere offene Fenster)

**Status:** erledigt 20.11.2026 in 0.29.1 (`main`), siehe `CHANGELOG.md`. Umgesetzt wurde nicht nur der Listener, sondern Zusammenführen beim Speichern (Stefans Einwand: Ein Listener allein würde auch einen leeren oder kaputten Stand an alle Fenster verteilen).
**Meldung Stefan (20.11.):** Beim Update auf 0.29.0 waren in der Chrome-App auf dem Mac die Kinder weg; Sicherung ließ sich importieren.

**Ursache (nachgestellt mit Playwright):** Jedes Fenster der App liest `stufenweise.data` nur einmal beim Start und schreibt bei `saveData()` immer den ganzen Stand aus seinem eigenen Speicher zurück. Es gibt keinen `storage`-Listener. Chrome-App und Browser-Tab (und mehrere Tabs) teilen sich denselben Speicher. Ein länger offenes, veraltetes Fenster überschreibt deshalb beim nächsten Speichern alles, was ein anderes Fenster inzwischen angelegt hat. `doUpdate()` ruft vor dem Neuladen ausdrücklich `saveData()` auf – „Jetzt aktualisieren“ im veralteten Fenster löscht so die Kinder. Der Hinweis erscheint in jedem offenen Fenster.
- Nachgestellt: Update 0.28.5 → 0.29.0 in einem Fenster: alle Kinder bleiben. Zwei Fenster, Kinder im zweiten angelegt, „Jetzt aktualisieren“ im ersten: alle Kinder weg. Beliebige Aktion im älteren Fenster: neuere Kinder weg.
- Nicht die Ursache: Testversion (hatte von Anfang an den Vorsatz `test:`), Datenumstellung (`migrateData`), Service Worker (speichert keine Daten).
- Fehler besteht seit Einführung der Profile, nicht erst seit 0.29.0; das Update macht ihn nur wahrscheinlich.

**Erster Vorschlag (ersetzt):** (1) `storage`-Ereignis abhören: ändert ein anderes Fenster `stufenweise.data` oder die Einstellungen, liest dieses Fenster den neuen Stand ein (auf der Startseite neu zeichnen, beim Üben ruhig weiterüben und erst danach übernehmen). (2) `saveData()` in `doUpdate()` streichen (gespeichert wird ohnehin nach jeder Änderung). (3) Test mit zwei Seiten im selben Browser-Kontext.

**Umsetzung 0.29.1:** `saveData()` vergleicht den gespeicherten Stand mit dem zuletzt gelesenen/geschriebenen (`dataBase`). Hat ein anderes Fenster gespeichert, Dreiwege-Abgleich (`merge3`, `mergeStores`): Kinder über ihre Kennung (Löschen gilt), Listen über ihre Einträge, Fehlerzähler addiert, Einstufungen je Feld. Sicherheitsnetz gegen Speichern ohne Kinder (`saveData({empty:true})` nur beim Löschen des letzten Kindes und beim Ersetzen durch eine Sicherung). Nicht lesbarer Stand → `stufenweise.data.defekt`. `storage`-Listener nur noch für die Anzeige. Test `tests/mehrere_fenster.py`.

---

## A: Modul Plus und Minus aufteilen

**Status:** erledigt 19.11.2026, freigegeben in 0.29.0 (20.11.2026). Umsetzung: `app.calc` (Rechenhilfe) statt neuem Modus; `pmPractice`, `pmViews`, `pmMem`, `pmTrack` (Leiter je Kind, Rechenart und Zahlenraum); Rail-Eintrag und Startseiten-Kachel „Rechenhilfe“; Test `tests/plusminus_ueben.py`.
**Entscheidungen Stefan (19.11.):** Darstellung wechselt automatisch wie bei Basis (nach 8 auf Anhieb richtigen die nächste, nach 3 Fehlern in Folge zurück; Lehrkraft kann oben jede wählen). Reihenfolge: bis 20 Material → Zwanzigerfeld → Zahlenstrahl; bis 100 Material → Hundertertafel → Zahlenstrahl; bis 1000 Material → Zahlenstrahl. Die Rechenhilfe sehen alle Kinder (eigener Eintrag bei Mathe).

**Ausgangslage:** Im Schülermodus bietet Plus/Minus zu viele Wahlmöglichkeiten: Zufallsaufgabe, eigene Aufgabe eingeben, Darstellung wählen (Zahlenstrahl, Material, Hundertertafel). Das kann Schüler*innen mit Förderschwerpunkt geistige Entwicklung überfordern.

**Wunsch:** zwei Bereiche.
- **A1 Rechenhilfe** (Arbeitsname, auch „Taschenrechner“ möglich): „Ich habe eine Aufgabe und brauche Unterstützung.“ Eigene Plus- und Minusaufgaben eingeben und mit Zahlenstrahl, Material oder Hundertertafel lösen.
- **A2 Üben:** „Ich möchte Plus und Minus trainieren und bekomme Aufgaben gestellt.“ Nur Zufallsaufgaben, keine eigene Eingabe. Die Darstellungen kommen nacheinander, ohne dass das Kind wählen muss: 1. Material, 2. Hundertertafel, 3. Zahlenstrahl.

**Heute im Code:** Plus/Minus läuft über `MODES` (`app.mode` `add`/`sub`). Die Ansicht wählt man mit `viewButtons()` (`data-view`): Material, Zahlenstrahl, Tafel (Hundertertafel, ab Zahlenraum 100; bei 1000 Tausenderbuch) und bis 20 Zehner-/Zwanzigerfeld. Knopf „Zufallsaufgabe“ und eigene Aufgaben (ins Feld tippen bzw. Zahlen eingeben) im selben Bildschirm; Einstellungen „Zufallsaufgaben (Plus und Minus)“. Die geführte Oberfläche und die Förderzonen R1–R6 führen ebenfalls dorthin.

**Vor der Umsetzung zu klären (Stefan):**
- Wann wechselt die Darstellung? Vorschlag: wie bei Basis nach einer Anzahl richtiger Aufgaben (z. B. 8), nach Fehlern zurück zur vorigen Darstellung.
- Reihenfolge je Zahlenraum: Die Hundertertafel gibt es erst ab dem Zahlenraum 100. Bis 20 also Material → Zwanzigerfeld → Zahlenstrahl? Bis 100 Material → Hundertertafel → Zahlenstrahl? Bis 1000 mit Tausenderbuch statt Hundertertafel?
- Folgt die Darstellung auch der Förderzone (z. B. R3 „über die 10“ zuerst am Zwanzigerfeld)?
- Wer sieht die Rechenhilfe: alle Kinder, nur auf Freigabe der Lehrkraft, oder nur im Unterrichtsmodus?
- Name und Symbol der beiden Bereiche in der Leiste; was passiert mit Lernständen und Statistik (Übungen bleiben unter „Plus“/„Minus“ gezählt?).
- Bleibt der heutige Bildschirm für Lehrkräfte erhalten (alle Wahlmöglichkeiten)?

**Risiko:** zentrales Modul, betrifft Startseite, geführte Oberfläche, „Heute für dich“, Förderzonen-Angebote, Arbeitsblatt-Verweise und viele Tests. Nur in `entwicklung`, mit vollständigem Testlauf.

---

## B: Unterricht – Zahlen im Zwanzigerfeld darstellen

**Status:** erledigt 19.11.2026, freigegeben in 0.29.0 (20.11.2026)

**Ausgangslage:** Das Zwanzigerfeld (Unterricht, Tafelwerkzeug) wird vor allem mit Rechnungen genutzt.

**Wunsch:** Zahlen als eigener Lerngegenstand, unabhängig von einer Rechnung.
- Die Lehrkraft gibt eine Zahl vor, z. B. 14; sie erscheint als Material im Zwanzigerfeld.
- Die Zahl kann unabhängig von einer Rechnung ein- und ausgeblendet werden.
- Die Schüler*innen erkennen und benennen die Menge.
- Die bisherigen Funktionen bleiben erhalten.

**Heute im Code** (`app.tf`, `renderTfield`, Abschnitt „Zehner- und Zwanzigerfeld (Unterricht)“): Plättchen werden zeilenweise gelegt, auch mit Schnellknöpfen (`data-tfk`). Liegt nur eine Farbe, steht oben die Anzahl (z. B. „14“) – immer sichtbar. Der Schalter „Ergebnis verdecken“ (`app.tf.hide`, `?` zum Aufdecken) wirkt nur auf das Ergebnis einer Rechnung. Eine Zahl direkt eingeben kann man nicht.

**Umsetzungsidee (zur Abstimmung):** Eingabe „Zahl legen“ (Zifferntastatur), die das Feld neu füllt; Verdecken gilt auch für die Anzahl allein („?“ antippen zeigt sie). Optional: Zahl kurz zeigen und abdecken (wie Blitzblick). Kleine Änderung, keine neue Architektur.

---

## C: Basis – bessere Progression der Schwierigkeitsstufen

**Status:** erledigt 19.11.2026, freigegeben in 0.29.0 (20.11.2026).
**Entscheidungen Stefan (19.11.):** Ähnlichkeit als Schritte innerhalb der Aufgabenart (nicht als eigene Arten); zuerst V1, V2, V3.
**Umsetzung:** Aufgabenarten mit `{sim:true}` haben st 0…5 = deutlich/ähnlich/fein × wenige/mehr Bilder (`bzSim`), „Nächste Aufgabe“ nach 12. Neue Bilder: Messer, Nagel, Schraubenschlüssel und Varianten (großer Hammer, Klauenhammer, Kreuz- und kurzer Schraubenzieher, Ringschlüssel, Teelöffel, Kochlöffel, Kuchengabel, Becher); Untergruppen `B_SUB`, Familien `B_FAM`; Varianten nur bei „fein“. Arbeitsblätter V1–V3 mit Auswahl „Ähnlichkeit“. Basis-Test unverändert (leichte Form = deutlich).

**Ausgangslage:** Die Stufen in Basis sollen systematischer aufeinander aufbauen. Heute steigt die Schwierigkeit innerhalb einer Aufgabenart vor allem über die Anzahl der Bilder (`st` 0–2: 2–3, dann mehr Bilder) und über den Wechsel zu einer anderen Aufgabenart.

**Wunsch:** zwei Dimensionen der Schwierigkeit.
1. **Quantitativ:** mehr Auswahl, mehr Elemente, größere Mengen.
2. **Qualitativ:** größere Ähnlichkeit, feinere Unterschiede, abstraktere Kategorien.

Möglichst dieselben Inhalte und Kategorien über mehrere Stufen, damit die Anforderung steigt und nicht der Lerngegenstand wechselt.

Beispiel „Was passt nicht?“:
- leicht: Hammer, Schraube, Mutter, Gabel (deutlich verschieden)
- mittel: Hammer, Schraubendreher, Schraubenschlüssel, Gabel (mehr Gemeinsamkeiten)
- schwer: verschiedene Hämmer, Schraubendreher, Schraubenschlüssel und ein Ding, das nicht passt (feine Unterschiede)

**Heute im Code:** 17 Alltagsgegenstände in `B_OBJ` (Gruppen `B_GRP`, z. B. Küche, Werkstatt), je in 4 Farben und beliebiger Größe; Aufgabenarten je Stufe in `AXES.V.arts` / `AXES.O.arts`, Schwierigkeit `st` 0–2. Es gibt keine Varianten eines Gegenstands (z. B. verschiedene Hämmer).

**Was es dafür braucht:**
- Ein Raster je Stufe: Zeilen = Ähnlichkeit (deutlich – ähnlich – fein), Spalten = Menge (wenige – mehr). Für jede Aufgabenart festlegen, welche Felder sinnvoll sind.
- Neue Bilder: Varianten innerhalb einer Art (Hammerarten, Schraubendreher, Schraubenschlüssel …) und vermutlich Ober- und Unterkategorien (Werkzeug → Schlagwerkzeug …). Das ist der größte Aufwand.
- Ähnlichkeit als Eigenschaft der Bilder (z. B. Gruppe, Untergruppe, Form), damit Generatoren gezielt „ähnlich“ oder „deutlich anders“ wählen können.

**Zusammenhang mit dem Basis-Test:** Der Test nutzt je Stufe eine leichte und eine schwerere Aufgabenart (`B_TEST`, `B_ST`). Ändert C die Aufgabenarten oder ihre Schwierigkeit, müssen Test, Lernstand-Texte und Arbeitsblätter nachgezogen werden. Mit Stefan klären, ob C vor oder nach der Freigabe des Basis-Tests kommt.

**Vor der Umsetzung zu klären (Stefan):** Welche Stufen zuerst (Vorschlag: V1 Gleiches, V2 Was passt nicht?, V3 Sortieren – dort wirkt Ähnlichkeit am stärksten)? Welche Gegenstände und Varianten? Soll „mittel“ eine eigene Aufgabenart werden oder eine weitere Schwierigkeit `st` innerhalb der Art? Gilt die neue Progression auch für die Arbeitsblätter?

## J. Arbeitshefte, die aufeinander aufbauen (Wunsch Stefan, 25.11.2026) – erledigt, freigegeben in 0.38.0

**Status:** erledigt, freigegeben in 0.38.0 (26.11.2026), siehe `CHANGELOG.md`. Mit Heft-Layout B, Deckblatt C4 und Rückseite als Nachguckseite.

Stefan: „Test machen → Arbeitsheft drucken → Schüler üben lassen.“ Heute ist das Heft oft an einem Tag durch (nur Förderzone, 1–2 Seiten je Stufe). Gewünscht: kommende Stufen vorwegnehmen, Heft nur für Mathe oder nur für Deutsch, für Deutsch mehr Texte und Aufgaben, zwischendurch längere Texte; Umfang wie ein Verlagsheft (Westermann „Fördern Inklusiv“, rund 48–64 Seiten).

Konzept mit 9 Fragen an Stefan: Dokument „Stufenweise – Arbeitshefte, die aufeinander aufbauen“ (claude.ai/artifact/Bay279priYyGDskCEixrv7). Kurz: Heft-Assistent (Fach, Seitenzahl, Vorgriff), Kapitel je Stufe (Einstieg → Üben, schwerer werdend → „Das kann ich schon“), Wiederholungsseiten, Hilfen hinten, Lösungsheft; Mathe-Feinstufen (Material → Bild → im Kopf); Deutsch: Texte in drei Längen (Ziel ~80/40/40), Fortsetzungsgeschichte, neue Papier-Formate; Broschürendruck. Umsetzung in 5 Schritten, erst nach Stefans Antworten.

**Stefans Antworten (25.11.2026, im Dokument):** alle 9 „wie vorgeschlagen“, also: 24 Seiten vorausgewählt, 48 wählbar; Vorgriff „bis das Heft voll ist“, Förderzone mit den meisten Seiten; gemischtes Heft als dritte Wahl; „Das kann ich schon“ mit drei Stufen in Worten und einfachem Zeichen; Lösungen als eigenes Heft; Fortsetzungsgeschichte (Praktikum, Klassenausflug, Wohnen); Folgeheft später; anfangen mit Schritt 1 (Heft-Assistent). Zu Frage 7 (Druck) zusätzlich: **auch A4-Broschüre aus A3-Blättern** (also A4-Seiten, zwei je A3-Bogen, in der Mitte geheftet) neben A5-Broschüre und A4 einseitig.

**Stand 25.11.2026 nachts:** Schritte 1–5 in `entwicklung` gebaut (Stefan: erst alle Schritte, dann freigeben), siehe `IN_PROGRESS.md`. Neue Texte von Stefan freigegeben (26.11.: „Die Texte sind gut. Bei den Fragen folge ich deinen Vorschlägen.“): Geschichte nur, wenn die Förderzone ab L6 bzw. W5 liegt; neue Kurz- und Langtexte auch beim Üben in der App (ist so gebaut); Themen und Namen bleiben. Prüfseite: claude.ai/artifact/VWhQbsUtqM9JendPLR8JKs. Später: Folgeheft vorschlagen (Frage 8).

---

## K: Name auf Arbeitsblättern durch Projektnamen ersetzen (Wunsch Stefan, 25.11.2026)

**Status:** erledigt, freigegeben in 0.38.0 (26.11.2026; gebaut 26.11., Stefan: „mach das noch“). Alle 6 Fußzeilen (`tafHelp`, Arbeitsblätter, Legeblätter, Heft-Deckblatt, `HEFT_LIC`) zeigen „Stufenweise · stufenweise.app · CC BY-SA 4.0“; Impressum, Lizenzseite, Kopfkommentar und `docs/anleitung.md` (Lizenzabschnitt) unverändert. Test in `tests/heft_assistent.py`.
**Anlass:** Unten auf Arbeitsblättern, Legeblättern und Hilfeseiten steht „© Stefan Hackl“ (5 Stellen in `index.html`, Klasse `ab-lic`, z. B. `tafHelp`, Legeblätter; dazu seit Backlog J `HEFT_LIC` für Heftseiten und Deckblatt in `buildHeft`). Blätter anderer Lehrkräfte tragen so Stefans Namen; der Name gehört nicht in Hefte und zu Eltern.
**Vorschlag:** Fußzeile „Stufenweise · stufenweise.app · CC BY-SA 4.0“. Das genügt der Namensnennung der Lizenz; Stefan bleibt als Urheber im Impressum, in `LICENSE`/`LIZENZ-INHALTE.md` und auf GitHub genannt. Impressum und Kopfkommentar in `index.html` unverändert lassen.
**Größe:** klein. Prüfen: `arbeitsblaetter.py`, `legeblaetter.py` (Fußzeile darf keine Seite verlängern).

## L: Lineatur zum freien Schreiben wählbar (Wunsch Stefan, 26.11.2026)

**Status:** erledigt, freigegeben in 0.41.0 (27.11.2026).
**Wunsch (Stefan):** „Beim freien Schreiben Arten von Lineatur aussuchen. Standard (dreiteilig → Dach/Erdgeschoss/Keller) Standard für 1./2. Klasse. Dann 2 Linien (3. Klasse) und 1 Linie (Standard 4. Klasse).“
**Idee:** Auswahl „Lineatur“ mit drei Arten:
- **Haus mit drei Stockwerken:** Dach, Erdgeschoss, Keller (Oberlänge, Mittelband, Unterlänge). Standard für Klasse 1/2.
- **Zwei Linien:** Grundlinie und Mittelband. Standard für Klasse 3.
- **Eine Linie:** Standard für Klasse 4.

Der Standard richtet sich nach der Klasse/Stufe des Kindes. Die Wahl wird gemerkt (`app.sheet`, `SHEET_KEEP`) und gilt auch im Heft.
**Entschieden (Stefan, 26.11.2026):** Die App kennt keine Klasse, nur die Themenwelt. Standard: **Grundstufe → Haus mit drei Stockwerken (3 Linien), Hauptstufe und Berufsschulstufe → eine Linie.** Zwei Linien bleibt zur Auswahl. Reihenfolge: erst M, dann L (die Schreibzeilen sitzen in den neuen Kästen).
**Betrifft:** nur Arbeitsblätter und Arbeitshefte (Stefan, 26.11.2026), also die Schreibzeilen `.ab-wline` und `.hf-lines` (W6 „Satz zum Bild“, „Satz abschreiben“, Aufgabenseiten der Fortsetzungsgeschichte). Nicht der Stift an der Tafel.
**Größe:** klein bis mittel. Schreibzeilen mit fester Höhe je Lineatur; prüfen mit `heft_seiten_passen.py` (Seiten dürfen nicht überlaufen).

## M: Arbeitsblätter im Design der Arbeitshefte (Wunsch Stefan, 26.11.2026)

**Status:** erledigt, freigegeben in 0.40.0 (26.11.2026). Danach L. Bekannt, nicht neu: Große Aufgaben bei L8/L9 und H:HL passen nicht auf ein Blatt (schon in 0.39.0, große Aufgaben werden nie verkleinert).
**Wunsch (Stefan):** „Passend zu den Arbeitsheften auch Arbeitsblätter im Design anpassen/aktualisieren.“
**Idee:** Einzelne Arbeitsblätter („Material drucken“) bekommen das Aussehen der Heftseiten, wie in 0.38.0 eingeführt:
- Kopfzeile wie im Heft, z. B. Fach und Stufe; Name und Datum bleiben.
- Fußzeile immer auf gleicher Höhe, mit Bildungsplan und Lizenz.
- Aufgabenkästen reichen bis zur Fußzeile (Layout B), keine großen Lücken.
- **Kein Farbrand** auf einzelnen Blättern (Stefan).
- **Schwarz-Weiß-Version für alle Blätter** anbieten (Stefan); bisher gibt es sie nur bei Basis-Blättern (`B_BW`). Farben durch Muster bzw. Graustufen ersetzen, z. B. bei Plättchen, Zwanzigerfeld, Bildern und Uhrzeigern.
- **Lösungsblätter** bleiben im Aufbau, passen sich aber im Grundsatz an (Schrift, Fußzeile) (Stefan).

Ein gemeinsamer Seitenrahmen für Blatt und Heft (`heftFrame` verallgemeinern) wäre sinnvoll, damit beide gleich bleiben.
**Entschieden (Stefan, 26.11.2026):** kein Farbrand; Schwarz-Weiß für alle Blätter; Lösungsblätter bleiben, nur angepasst. Bild-Vorschläge (zwei echte Blätter, heute und A/B/C) am 26.11. gezeigt:
- **Layout A „wie im Heft“:** schmale Kopfzeile mit Fach und Bereich („Mathe · Rechnen“), darunter Titel und Name/Datum wie heute; Kästen bis zur Fußzeile (Layout B des Hefts); Fußzeile auf fester Höhe mit Bildungsplan und Lizenz links, Fach rechts; keine Seitenzahl. Umsetzung über `heftFrame` (Blatt-Fassung ohne Seitenzahl).
- **Schwarz-Weiß wie gezeigt:** Blau wird schwarz, Orange schraffiert; Häkchen „Schwarz-Weiß-Drucker“ bei allen Blättern (bisher nur Basis, `B_BW`).
- **Legeblätter bleiben**, wie sie sind (genau bemaßt); höchstens die Fußzeile wird angeglichen.
**Größe:** mittel. Prüfen: `arbeitsblaetter.py`, `druck_seiten.py`, `grosse_aufgaben.py`, Anleitungsbilder neu.

## N: „Große Aufgaben“ auch im Heft-Assistenten (Wunsch Stefan, 26.11.2026)

**Status:** erledigt, freigegeben in 0.39.0 (26.11.2026). **Entschieden (Stefan, 26.11.):** Häkchen anfangs aus; das Heft nimmt feste Grundeinstellungen statt der Einstellungen des letzten Einzelblatts; passt groß nicht, wird nur diese Seite normal groß.
**Wunsch (Stefan):** „‚Große Aufgaben (mehr Platz zum Schreiben und Streichen)‘ auch bei Arbeitsheften anbieten als Option.“
**Ist-Stand:** Bei einzelnen Arbeitsblättern gibt es das Häkchen (`app.sheet.gross`, Zoom 1,35). Im Heft bekommen nur die Einstiegsseiten große Aufgaben, und nur wenn die Seite damit zu drei Vierteln voll wird (`fixed()`). Übungsseiten übernehmen sonst zufällig die Einstellung des letzten Einzelblatts (siehe Übergabe, offene Punkte).
**Idee:**
- Häkchen „Große Aufgaben (mehr Platz zum Schreiben und Streichen)“ im Heft-Assistenten (`H.gross`). Es gilt für alle Übungsseiten, „Das kann ich schon“ und die Wiederholung.
- Weniger Aufgaben je Seite. Die Seiten füllen sich weiter ganz (Layout B) und werden nicht verkleinert, große Aufgaben bleiben groß.
- Die Einstellung des letzten Einzelblatts wird im Heft nicht mehr übernommen.

**Zu bedenken:**
- Mehr Seiten für dieselbe Übungsmenge, die Seitenzahl bleibt aber fest.
- Sehr große Aufgaben (z. B. lange Texte) brauchen eventuell eine Ausnahme, damit sie auf eine Seite passen.

**Größe:** klein bis mittel. Prüfen: `heft_seiten_passen.py` (alle Stufen mit großen Aufgaben), `heft_assistent.py`.

## O: Voller Speicher wird nicht gemeldet (Prüfung vom 22.11.2026, Empfehlung „Speicher volllaufen lassen verhindern“)

**Status:** O1 erledigt, freigegeben in 0.38.1 (26.11.2026). **Entschieden (Stefan, 26.11.):** nur **O1 Melden**, als Fehlerbehebung direkt in `main`. O2, O3, O4 nicht (vorerst).
**Ist-Stand (geprüft 26.11. im Code und in Chrome gemessen):**
- Alles liegt in `localStorage` unter `stufenweise.data` (Kinder, Protokoll, Lernstand), dazu `stufenweise.settings`, `stufenweise.blatt` und `stufenweise.heft`.
- `saveData()` hat außen `try { … } catch {}`. Schlägt `localStorage.setItem` fehl, passiert nichts Sichtbares. Die App arbeitet mit dem Stand im Arbeitsspeicher weiter. Nach dem nächsten Neustart fehlt alles seit dem letzten gelungenen Speichern. Gemessen: Speicher aufgefüllt, dann 2000 neue Protokolleinträge und ein umbenanntes Kind → gespeichert blieb der alte Stand (2 712 Zeichen statt 178 767), ohne Meldung. `saveSettings()` und `sheetSave()` schweigen genauso; nur `saveHeft()` meldet „Das Heft ist zu groß zum Merken“.
- Platz: Chrome erlaubt je Adresse etwa 5 Mio. Zeichen. Safari erlaubt ebenfalls etwa 5 MB; wie viele Zeichen das sind, kann ich hier ohne iPad nicht messen (möglicherweise nur die Hälfte).
- Was Platz braucht: je Kind bis zu 3 000 Protokolleinträge (Kürzung in `logAttempt`, je etwa 70–90 Zeichen, also bis etwa 0,25 Mio. Zeichen), 500 übersprungene Aufgaben, Lernstand-Verlauf `mhist` (ohne Grenze). **Neu seit 0.38.0: Das gemerkte Arbeitsheft ist groß.** Ein Heft mit 24 Seiten braucht etwa 0,4 Mio. Zeichen, mit 48 Seiten etwa 0,8 Mio. Es bleibt gemerkt, bis es geleert wird.
- Testversion: Seit dem Umzug (0.34.1) liegt sie unter test.stufenweise.app, also unter einer eigenen Adresse mit eigenem Speicher. Sie teilt sich den Platz nicht mehr mit der App. Der Vorsatz `test:` bleibt als zweite Sicherung. Dieser Teil der Empfehlung ist erledigt.

**Vorschläge:**
- **O1 Melden (Kern):** `saveData()` erkennt den Fehler. Dann erscheint eine deutliche Leiste für die Lehrkraft, kein Kindertext: „Der Speicher ist voll. Neue Ergebnisse werden gerade nicht gespeichert. Bitte jetzt eine Sicherung speichern.“ Mit Knopf „Jetzt sichern“. Die Sicherung nimmt den Stand aus dem Arbeitsspeicher, also auch alles Ungespeicherte. Die Leiste bleibt, bis das Speichern wieder klappt. Dasselbe für Einstellungen und Blatt-Einstellungen, aber nur als kurzer Hinweis.
- **O2 Platz machen:** Ist der Speicher voll, gibt die App zuerst das gemerkte Arbeitsheft frei (es lässt sich mit dem Heft-Assistenten neu bauen) und versucht es dann noch einmal. Es kommt der Hinweis „Das gemerkte Arbeitsheft wurde entfernt, damit die Ergebnisse gespeichert werden können.“ Varianten: (a) Heft nur noch bis zum Schließen merken, (b) Heft nach dem Drucken nicht mehr merken.
- **O3 Früh warnen:** Beim Start prüft die App einmal am Tag mit einer Probe (etwa 0,5 Mio. Zeichen kurz schreiben und wieder löschen), ob noch Platz ist. Wenn nicht, kommt vorher der Hinweis „Speicher fast voll“. Das funktioniert in jedem Browser. `navigator.storage.estimate()` misst `localStorage` nicht zuverlässig.
- **O4 Später, nur bei Bedarf:** ältere Protokolleinträge zu Tageswerten verdichten. Das ist größer, weil Lernstand, Bericht und QR-Umzug das Protokoll lesen.

**Frage an Stefan:** Fehlerbehebung direkt in `main` (0.38.1) oder über `entwicklung`/Testversion?
**Größe:** O1 + O2 + O3 klein. Test: neuer `tests/speicher_voll.py` (Speicher künstlich füllen, Meldung prüfen, Sicherung enthält den ungespeicherten Stand, Heft wird freigegeben, nach Freigabe gespeichert).

## P: Safari-Tab auf dem iPad löscht Daten nach 7 Tagen (Prüfung vom 22.11.2026, Empfehlung „iPad nur als App vom Home-Bildschirm nutzen“)

**Status:** P1 erledigt, freigegeben in 0.39.0 (26.11.2026). **Entschieden (Stefan, 26.11.):** nur **P1 Hinweis im Safari-Tab**, über `entwicklung`/Testversion (auf dem iPad im Safari-Tab ansehen). P2 und P3 nicht (vorerst).
**Ist-Stand (geprüft 26.11.):**
- Safari löscht allen Speicher, den eine Website per Skript schreibt (auch `localStorage`), wenn die Website an 7 Tagen, an denen Safari benutzt wird, nicht angetippt wurde (Tracking-Schutz ITP, WebKit 2020). Apps vom Home-Bildschirm sind davon ausgenommen (WebKit, „Home Screen Web Application Domain Exempt From ITP“). Laut WebKit-Entwickler*innen (2024) gilt die Regel für alle Speicherarten. `navigator.storage.persist()` schützt vor dem Aufräumen bei Platzmangel, nach heutigem Wissen aber nicht vor dieser 7-Tage-Regel.
- Die App ruft `navigator.storage.persist()` beim Start schon auf (still, ohne Ergebnis anzuzeigen).
- Die App erkennt nicht, ob sie im Safari-Tab oder als Home-Bildschirm-App läuft (kein `navigator.standalone`, kein `display-mode`).
- Die Erinnerung an die Sicherung kommt nach 14 Tagen und nur im Lernstand (`backupBox`).
- Anleitung und README erklären den Home-Bildschirm und sagen schon, dass Tab und Home-Bildschirm-App getrennte Daten haben.
- Gefahr im Alltag: Ferien. Wird das iPad in den Ferien für anderes in Safari genutzt, ist der Klassensatz danach leer. Eine Warnung *nach* dem Löschen ist nicht möglich, weil dann auch jeder Merker gelöscht ist.

**Vorschläge:**
- **P1 Erkennen und deutlich hinweisen:** Auf iPad und iPhone (auch iPadOS im Desktop-Modus: „Macintosh“ mit Touch) im Safari-Tab (`navigator.standalone === false`) erscheint für die Lehrkraft ein Hinweis: „Im Safari-Tab kann das iPad die Ergebnisse nach 7 Tagen ohne Nutzung löschen, zum Beispiel in den Ferien. Lege Stufenweise als App auf den Home-Bildschirm.“ Mit kurzer Anleitung (Teilen → Zum Home-Bildschirm) und dem Hinweis zum Umzug: Sind schon Kinder angelegt, erst hier „Sicherung speichern“ und in der App „Sicherung laden“. Ort: Lernstand und Einstellungen (Daten sichern) immer. Dazu einmal je Tag auf dem Startbildschirm, wenn Kinder angelegt sind (wie der Update-Hinweis, nicht beim Üben). Ausblendbar für 30 Tage.
- **P2 Häufiger an die Sicherung erinnern, nur im Safari-Tab:** nach 7 statt 14 Tagen, und auch auf dem Startbildschirm statt nur im Lernstand. In der Home-Bildschirm-App und auf anderen Geräten bleibt es bei 14 Tagen.
- **P3 Leere App nach Wechsel:** Startet die Home-Bildschirm-App ohne Kinder, zeigt sie unter „Wer übt?“ einen Satz: „Kinder schon im Safari-Tab angelegt? Dort Sicherung speichern, hier laden.“
- Nicht möglich ohne Server: Daten vor dem Löschen retten. Eine Sicherungsdatei muss eine Person speichern.

**Frage an Stefan:** Fehlerbehebung direkt in `main` (0.38.x) oder über die Testversion? Prüfen lässt sich P nur auf einem echten iPad (in Chrome kann ich iPad-Safari nur nachahmen).
**Größe:** klein. Test: neuer `tests/safari_tab.py` (Erkennung mit nachgeahmtem iPad-Safari, Hinweis an den richtigen Stellen, nicht beim Üben, nicht in der App).

## Q: Raten bei Auswahlaufgaben im Test (Prüfung vom 22.11.2026, Empfehlung „Raten im Test begrenzen“)

**Status:** Q1 erledigt, freigegeben in 0.39.0 (26.11.2026). **Entschieden (Stefan, 26.11.):** nur **Q1** (3 von 3 bei Stufen, die nur aus Auswahlaufgaben bestehen), über `entwicklung`/Testversion. Q2, Q3, Q4 nicht; Basis-Test bleibt bei 2 von 2 oder 2 von 3 je Block.
**Ist-Stand (geprüft 26.11.; Simulation mit einem Kind, das nur rät, je 600–3 000 Durchläufe):**
- `cellDecision`: erreicht bei 2 von 2 oder 2 von 3, aber nicht, wenn die Kernaufgabe (die erste Aufgabe, `kern:true`) falsch ist. Wegen dieser Regel liegt der Wert je Stufe bei 3 Bildern bei etwa **19 %** und nicht bei 26 %. Bei 2 Antworten (z. B. „Stimmt das?“ in L6) sind es etwa 26 %.
- Betroffen sind fast alle Stufen in **Lesen L1–L9**, **Hören P1–P4**, **Uhr U1–U6** und **Größen G1–G4** (3 Antworten, je Stufe 11–26 % „erreicht“, 32–50 % mindestens „teilweise“). Zahlen, Rechnen, Stellenwert und Schreiben fast nicht (Zahlen eintippen).
- **Ganzer Test:** Der Lese-Test sucht ab L4 nach oben und unten (`binary`). Unter der höchsten erreichten Stufe trägt `inferCells` alle tieferen als „erreicht (abgeleitet)“ ein. Ergebnis für ein Kind, das nur rät: In **etwa 2 von 3 Lese-Tests** steht danach mindestens eine Stufe auf „erreicht“, im Mittel 2 Stufen. L1 in etwa 47 %, L4 in etwa 18 % der Tests. Mathe-Test Teil 2: in etwa der Hälfte (meist G1, U1, G2).
- **Basis-Test** ist schon besser geschützt (Block a und b nötig): Teil 1 etwa 6 %, Teil 2 etwa 22 % (V5 „Wo sind mehr?“ mit 2 Bildern), Teil 3 etwa 6 %.
- „Weiß ich nicht“ senkt das Raten, wenn Kinder es nutzen.

**Vorschläge (simuliert, Kind rät nur; Anteil Lese-Tests mit mindestens einer Stufe „erreicht“ / Mathe Teil 2):**
| | Lesen | Mathe Teil 2 |
| --- | --- | --- |
| heute | 69 % (im Mittel 2,0 Stufen) | 49 % |
| **Q1** Stufen nur mit Auswahlaufgaben: „erreicht“ erst bei 3 von 3 (nach 2 von 2 kommt eine dritte Aufgabe; 2 von 3 = „teilweise“) | 17 % (0,4 Stufen) | 30 % |
| **Q2** mindestens 4 Antworten statt 3 | 45 % | 30 % |
| Q1 + Q2 | 9 % | 16 % |
| **Q3** nichts ableiten aus Stufen, die nur mit Auswahlaufgaben erreicht wurden | 66 %, aber nur 1,0 Stufen | 47 % |
| Q1 + Q3 | 17 % (0,2 Stufen) | 28 % |

- **Q1** ist die stärkste Einzelmaßnahme und klein: Kinder, die es können, bekommen je solcher Stufe höchstens eine Aufgabe mehr. Der Lese-Test prüft meist 4 bis 6 Stufen, wird also um höchstens so viele Aufgaben länger.
- **Q2** ist mehr Arbeit: Für jede Aufgabenart braucht es eine vierte passende Antwort, und vier Bilder in einer Reihe werden auf dem iPad kleiner. Bei Silben zählen (1, 2, 3) und „Stimmt das?“ (ja/nein) geht es nicht.
- **Q4** Hinweis im Lernstand: Stufen, die nur mit Auswahlaufgaben erreicht wurden, bekommen ein Zeichen („durch Auswahl“, bitte beim Üben bestätigen). Das ändert nichts an der Einstufung.
- **Basis:** Stefans Regel (2 von 2 oder 2 von 3 je Block) bleibt, außer Stefan möchte Q1 auch für Block b.

**Fragen an Stefan:** welche Maßnahmen? Auch für den Basis-Test? Weg über `entwicklung`/Testversion (Änderung an der Testauswertung, kein Fehler im engeren Sinn).
**Größe:** Q1, Q3, Q4 klein; Q2 mittel. Test: `tests/test_fortschritt.py`, `tests/basis_test.py`, neuer `tests/raten.py` (die Simulation von oben als Test mit Obergrenzen).

## R: Tests schneller (Werkzeug, keine App-Funktion; Wunsch Stefan, 26.11.2026)

**Status:** erledigt (26.11.2026), in `main` und `entwicklung`.
**Wunsch (Stefan):** `sh tests/run_all.sh lang` dauert etwa 25 Minuten, weil die Tests nacheinander laufen. Tests parallel laufen lassen (3–4 gleichzeitig, Anzahl per Variable), ohne dass sie sich in `tests/out/` Dateien überschreiben; ein gemeinsamer Testserver auf Port 8766, der vor dem Start sicher läuft; Tests mit hoher Last notfalls einzeln; Ausgabe am Ende als Liste ok/FEHLER je Test. Prüfen, dass die parallele Runde dieselben Ergebnisse liefert wie die alte. Optional `sh tests/run_all.sh nur <name>` und eine Liste in `tests/README.md`, welcher Test welchen Bereich prüft. Bauen in `entwicklung`, danach nach `main` (betrifft nur `tests/`).
**Messung (26.11.2026, Umgebung mit 2 Prozessorkernen, 7 GB Speicher):** vorher nacheinander schnell 10:30 min, lang 18:57 min (63 Tests). Nachher mit 4 gleichzeitig: schnell 3:33 min, lang 6:37 min, dieselben Ergebnisse (alle ok). Mit 2 gleichzeitig: lang 10:26 min. Längste Tests: Zufallsklicks 133 s, Heftseiten passen / mit großen Aufgaben je 120 s, Arbeitsblätter 105 s, Heft-Assistent 69 s.
**Umsetzung:** `tests/run_all.sh` startet die Tests mit `xargs -P` (Standard 4, `STUFENWEISE_JOBS`), lange zuerst; ein gemeinsamer Server auf Port 8766 (wartet bis zu 10 s, bis er antwortet); jeder Test hat einen eigenen Ausgabeordner `tests/out/lauf/<Test>/` (`STUFENWEISE_OUT`) und eine Logdatei; am Ende Liste ok/FEHLER in fester Reihenfolge mit den letzten Zeilen bei Fehlern; `nur NAME …` für einzelne Tests; `timeout` nur, wenn vorhanden (macOS). `tests/README.md`: Tabelle „Gezielt testen“ (Bereich → Tests) und alle Tests beschrieben.
**Dabei gefunden:** `mehrere_fenster.py` schlug unter Last einmal fehl (Fehlerzähler 2 statt 3). Ursache ist Chrome: Ein Fenster sieht die localStorage-Änderung eines anderen Fensters erst nach kurzer Zeit; der Test ließ beide Fenster im selben Augenblick schreiben. Die App selbst zählt richtig (nachgestellt). Der Test wartet jetzt, bis das andere Fenster den neuen Stand sieht. `frei_stift.py` schrieb sein Bild an einen festen Pfad dieser Umgebung, jetzt in den Ausgabeordner.

## S: Rückmeldungen zu Arbeitsblättern und Heften (Stefan, 26.11.2026 abends)

**Status:** erledigt, S1–S9 freigegeben in 0.41.0 (27.11.2026). **Entschieden (Stefan, 26.11.):** S3/S4 Material in Schwarz-Weiß **hellgrau** gefüllt (nicht weiß), Pfeile deutlich; S5/S6 **Kästchen in jeder Aufgabe** (Aufgabe über die ganze Breite); S7 Zehnerfeld als eine Reihe mit 10 **überall** (Blätter, Üben, Test, Materialkiste, Tafel); Reihenfolge: S jetzt in `entwicklung`, in der Testversion zeigen, dann mit L als 0.41.0 freigeben; T danach als Konzept-Dokument.

Fehler:
- **S1 Schriftlich rechnen bis 1000 mit „Große Aufgaben“ läuft rechts über den Rand.** Das Blatt hat 3 Spalten (`schriftlich.cols`), große Aufgaben werden auf 135 % vergrößert (`AB_GROSS`). Vorschlag: Mit großen Aufgaben höchstens 2 Spalten, für alle Blätter mit 3 oder mehr Spalten. Test: jedes Blatt mit großen Aufgaben darf nicht breiter als die Seite sein.
  - **Erledigt (entwicklung):** Große Aufgaben höchstens 2 Spalten; Hundertertafel- und Basis-Blätter groß einspaltig; Materialblätter (leere Hundertertafel u. a.) bleiben normal groß; Lineal bleibt in echter Größe; Stundenplan-Tabellen passen in die Breite. Das Raster wächst nicht mehr über die Seite (`minmax(0,1fr)`). Dabei aufgefallen und mitbehoben: „Der Größe nach ordnen“ lief auch ohne große Aufgaben 5 mm über. Tests: `blatt_layout`, `grosse_aufgaben`.
- **S2 Einmal lief eine Heftseite über** („Das kann ich schon: Längere Texte verstehen“, Hinweis „Zu lang für ein Blatt“), nicht nachstellbar. Bekannt: Lange Texte (L9) mit Fragen sind sehr hoch; bei „Das kann ich schon“ kommt die Selbsteinschätzung dazu. Vorschlag: viele Hefte mit L8/L9 bauen und prüfen; passt eine solche Seite nicht, nur eine Aufgabe (ein Text) auf die Seite und notfalls ein kürzerer Text. Möglich auch: ein altes gemerktes Heft (vor 0.38) – das zeigt den Hinweis weiter, bis es neu erstellt wird.
  - **Erledigt (entwicklung):** In Chrome nicht nachstellbar (je 15 Hefte mit L6–L9 in Grundstufe, HS und BSS, normal und groß: keine Seite läuft über). Wahrscheinliche Ursache: Seiten mit großen Aufgaben wurden im fertigen Heft nie verkleinert; auf dem iPad ist die Schrift etwas anders, eine knapp passende Seite lief dann über. Jetzt bis 90 % verkleinert statt zweites Blatt; beim Bauen bleibt es streng.
- **S3 Schwarz-Weiß: Material (Hunderterplatten, Zehnerstangen, Einerwürfel) sieht komisch aus** (Plus bis 1000, Mengen erfassen und zerlegen bis 1000 u. a.). Heute: Hunderter mit Punktmuster, Zehner schwarz, Einer mit Gitter. Stefans Wunsch: „wie in Farbe, nur ohne farbige Füllung“. Vorschlag: Material in Schwarz-Weiß weiß gefüllt, mit dunklem Umriss und den Kästchenlinien wie in Farbe; Plättchen im Zwanzigerfeld bleiben schwarz und schraffiert (so freigegeben).
- **S4 Schwarz-Weiß: Pfeil am Zahlenstrahl undeutlich** (Zahlenstrahl und Nachbarzahlen bis 1000). Der rote Pfeil bekommt heute das Punktmuster der Hunderter. Vorschlag: Pfeile und Markierungen in Schwarz-Weiß schwarz gefüllt.
  - **Erledigt S3/S4 (entwicklung):** Material in Schwarz-Weiß hellgrau mit Umriss und Kästchenlinien (Stefans Wahl „Material hellgrau“), Plättchen bleiben schwarz bzw. schraffiert; Pfeile, Kreuze und Markierungen in Rot werden schwarz. Test `blatt_rueckmeldungen`.

Didaktik und Gestaltung:
- **S5 Unterschiede bestimmen bis 1000 braucht Platz zum Rechnen** („Solche Aufgaben kann ja ich noch nicht mal ohne weiteres im Kopf lösen.“). Vorschlag: ab Zahlenraum 1000 (oder schon ab 100) in jeder Aufgabe ein Feld zum Rechnen (kariert, z. B. 6 × 4 Kästchen oder Stellenwerttafel für schriftliches Rechnen); dafür eine Aufgabe je Zeile.
  - **Erledigt (entwicklung):** ab 1000 eine Aufgabe je Zeile, links ein Kästchenfeld (5-mm-Karos), rechts die Antwort.
- **S6 Ergänzen bis 1000: Platz für Nebenrechnungen und Text über die ganze Breite.** Heute bricht „In den Karton passen 1000. 640 sind schon drin.“ mitten im Satz um, die Zahl steht am Zeilenende. Vorschlag: Sachaufgaben (Text) über die ganze Seitenbreite; Umbruch nur zwischen Sätzen; unten auf der Seite ein kariertes Feld „Nebenrechnung“ (füllt den Rest der Seite).
  - **Erledigt (entwicklung):** ab 1000 eine Aufgabe je Zeile mit Kästchenfeld in jeder Aufgabe (wie S5); Sätze werden nur zwischen den Sätzen umbrochen (auch bei 2 Spalten und großen Aufgaben).
- **S7 Zehnerpartner: das Zehnerfeld als eine Reihe mit 10** („dass es immer 10 in einer Reihe sein sollen, auch wenn es nur bis 10 geht – bekannte Logik“). Heute 2 Reihen mit je 5 (`fieldSvg(n, 10)`). Offen: nur auf Arbeitsblättern oder überall (auch Üben, Test, Materialkiste, Tafel)?
  - **Erledigt (entwicklung), Stefans Wahl „Überall“:** Zehnerfeld als eine Reihe mit 10 in Üben und Test, Rechenhilfe, Tafel/Materialkiste, Blitzblick, Arbeitsblättern und Legeblatt (Legeblatt jetzt quer, 25-mm-Felder für Wendeplättchen). Zwanzigerfeld bleibt 2 × 10.
- **S8 Lochrand: Arbeitsblätter links mehr Rand** (werden gelocht). Heute 12 mm rundum. Vorschlag: links 20 mm (Lochung braucht etwa 12–15 mm), rechts 12 mm; Hefte bleiben.
  - **Erledigt (entwicklung):** einzelne Arbeitsblätter links 20 mm (auch Lösungs- und Hilfeseite), Hefte und Legeblätter unverändert. Bilder werden auf die schmalere Breite (178 mm) eingepasst.

- **S9 Gleiche Aufgaben mehrmals auf einer Seite** (Stefan 23:11, Bild: Heft, Einstieg „Ergänzen bis 10“ viermal „9 sind schon drin“, zweimal „8 + ☐ = 10“). Ursache: Mit Feinstufe (`app.sheet.stufe`) baut `buildSheet0` dreimal so viele Aufgaben und nimmt die leichtesten; gleiche Aufgaben wurden dabei nicht aussortiert, sobald es nach 12 Versuchen keine neue gab. Gilt auch für Blätter mit fester Aufgabenzahl.
  - **Erledigt (entwicklung):** Gibt es nach 20 Versuchen keine neue Aufgabe, bleibt die doppelte weg (die Seite hat dann eine Aufgabe weniger). Test `keine_doppelten` (alle Blätter, Heft, Wiederholung); der alte Stand hatte Doppelte bei Längen, Uhr und im Heft-Einstieg.

Nebenbei gefunden (26.11., Testlauf): Im Lese-Test L8 „Stundenplan“ steht im Protokoll bei manchen Fragen „(undefined)“ statt der Fragenart (Beschriftung in `READ`/`SERIES`, Frage „Wie oft ist BNT in der Woche?“). Nur die Beschriftung, die Aufgabe selbst ist richtig.

## T: Basis-Arbeitsblätter didaktisch überarbeiten (Stefan, 26.11.2026)

**Status:** Konzept mit Bildern und 7 Fragen (27.11.2026, Claude-Doc „Konzept: Basis-Arbeitsblätter überarbeiten (Backlog T)“, https://claude.ai/artifact/MUbTKabSxyXh9fofA3No2U); **Stefan hat am 27.11. abends alle Fragen beantwortet** (Tabelle „Stefans Entscheidungen“ im Doc und unten) und danach „Ja, so bauen“ gesagt. **Erledigt in 0.43.0** (freigegeben 28.11.2026; Bastelseite nach Rückmeldung mit Schere und Umriss je Teil).

**Entscheidungen (Stefan, 27.11.2026, per Auswahl im Chat):**
1. Eine Art je Blatt für alle zehn Blätter: Auswahl „Aufgabe“ im Blatt-Dialog, leichteste vorausgewählt, keine Mischung.
2. V2: eine Reihe mit 4 Bildern je Kasten, 2 Kästen nebeneinander.
3. V4: Gabeln zusammengeschoben unter den Tellern, Beispiel ganz verbunden; „Reicht es?“ = den Teller ohne Gabel einkreisen (es fehlt immer genau eine Gabel), kein ja/nein.
4. V5: drei Arten „Wo sind mehr?“, „Wo sind weniger?“, „Gleich viele“; „Gleich viele“ = drei Kästen, die zwei mit gleich vielen (anders verteilt) einkreisen.
5. V6 „Ordnen“: **ausschneiden und aufkleben** (nicht mit der Treppe verbinden); die Dinge zum Ausschneiden auf einer **eigenen Bastelseite hinter dem Blatt**.
6. Die Art steht im Titel („Der Größe nach ordnen: Das größte“), keine graue Zeile.
7. Heft-Assistent: eine Art je Seite; Einstieg = leichteste Art, Übungsseiten der Reihe nach (V1–V3 innerhalb der Art deutlich → ähnlich → fein), bei wenigen Seiten die leichteren zuerst; „Das kann ich schon“ und Wiederholung = schwerste geübte Art.
8. Beispiel: die erste Aufgabe ist ganz vorgemacht (ersetzt die Regel vom 19.11. „nur erster Schritt“).
9. O2 Form, O3 Richtung, V3 „Nach Art“ (Gruppe): eine je Blatt, zufällig, groß oben; keine weitere Auswahl.
10. Arten und Reihenfolge wie in der App (`AXES.V.arts`/`AXES.O.arts`): V1 einkreisen vor verbinden; V3 erst Farbe bei gleichen Dingen, „verschiedene Dinge“ als eigene, spätere Art.
11. Bastelseite (Nachfrage): darf nie auf der Rückseite bedruckt sein (Hefte werden teils beidseitig gedruckt). Heft-Broschüren: Bastelseite auf einer rechten Seite, Rückseite leer; Einzelblatt und Blattsammlung: Blatt, Leerseite, Bastelseite, Leerseite.

Geplante Arten je Blatt (leicht → schwer): V1 Gleiches Bild einkreisen · Gleiches Bild verbinden · Gleiche Farbe einkreisen · Gleiche Farbe verbinden; V2 Ganz anders · Andere Farbe · Andere Größe · Gehört nicht dazu; V3 Nach Farbe · Nach Größe · Nach Art · Farbe, verschiedene Dinge; V4 Jedem eins · Reicht es?; V5 Wo sind mehr? · Wo sind weniger? · Gleich viele; V6 Das größte · Das kleinste · Ordnen; V7 Was kommt dann? · Längere Muster · Weitermalen; O2 Form finden · Quadrat oder Rechteck; O3 Alle Pfeile nach … · Gleiches Zeichen; O4 Von links nach rechts · Was kommt zuerst?. „Ähnlichkeit“ nur bei Arten, die sie nutzen.

Beim Prüfen im Code gefunden (wird mit T erledigt): V2 „Andere Farbe/Größe“ wechselt heute zufällig innerhalb einer Art; V3 „Nach Art“, O2 und O3 wechseln Gruppe, Form bzw. Richtung von Aufgabe zu Aufgabe; „Andere Größe“ (V2) und „Gleiches Bild einkreisen“ (V1) gibt es auf Papier noch nicht. Doppelte-Aufgaben-Prüfung (`KT` vergleicht nur Text) erkennt bei Bildaufgaben nichts – mit einer Art je Blatt muss sie den Bildinhalt vergleichen, sonst bleiben Blätter halb leer. Kern: eine Aufgabenart je Blatt (Auswahl „Aufgabe“), eine Bildreihe je Kasten, Beispiel ganz vorgemacht, nichts zum Lesen ankreuzen; neuer Aufbau für V2, V4, V5, V6. Stefan: „Bei den Basis-Arbeitsblättern scheint mir didaktisch noch am meisten der Wurm drin zu sein … Vielleicht müssen wir uns extra nochmal darum kümmern.“
Rückmeldungen:
- **T1 V2 Was passt nicht?** Lieber nur eine Bildreihe je eingerahmter Aufgabe (heute zwei Reihen in einem Kasten).
- **T2 V4 Eins zu eins zuordnen:** Das Beispiel verbindet quer (erster Teller mit dritter Gabel); der Sinn fehlt. Gabeln stehen schon unter den Tellern.
- **T3 V5 Mehr, weniger, gleich viel:** nicht alle drei auf einem Blatt – Kinder, die nicht lesen, schaffen den Wechsel nicht, und man sitzt nicht ständig daneben.
- **T4 V6 Der Größe nach ordnen:** unklar, wie das Kind es machen soll.
Vorschlag: eigenes Konzept-Dokument „Basis-Arbeitsblätter“ wie bei den Arbeitsheften – je Blatt V1–V8, O2–O4: Ziel, was das Kind tut (ohne Lesen), Aufbau, Beispiel, Varianten; dazu Bild-Vorschläge zum Ansehen. Grundsätze aus Stefans Entscheidungen zum Basis-Test (nicht mischen, vor jeder neuen Art unübersehbar vormachen, eine Art je Blatt bzw. Kasten).

## U: Arbeitshefte stringenter – einzelne Blätter vs. fertige Hefte (Stefan, 27.11.2026)

**Status:** erledigt, freigegeben in 0.42.0 (27.11.2026). Stefan 27.11.2026 09:24: „Deine Vorschläge 1–3 finde ich super.“ Detailfragen per Auswahl beantwortet, danach „Ja, so bauen“.
**Entschieden (Stefan, 27.11.2026):**
- Alte gemerkte Hefte: **aufteilen** – ein Heft aus dem Assistenten bleibt Heft, angehängte Blätter wandern in die Blattsammlung; ein Heft ganz ohne Assistent wird ganz zur Blattsammlung.
- U1 Stufenwahl: **ein Bereich, von–bis** (zusammenhängend in Lernreihenfolge); Seiten: **alle Kapitel gleich viele**; Themenwelt: **Auswahl im Assistenten** (vorausgewählt die Einstellung der App).
- U2 Lösungen: **hinter jedem Blatt**.
- U3: **nur Übungsseiten** austauschen (neue Aufgaben oder anderes Blatt); ↑ ↓ ✕ fallen im Heft weg (bleiben in der Blattsammlung).
Stefan: „Wir haben ja immer noch die Möglichkeit, einzelne Arbeitsblätter in ein Arbeitsheft aufzunehmen. Das ist jetzt etwas unklar, da dort beliebige Seitenzahlen möglich werden. Vielleicht sollte es eher ohne Schülername/Test vorgefertigte Arbeitshefte zu gewissen Kompetenzbereichen geben. … Insgesamt ist das so zumindest wenig stringent.“
Ist-Stand: „Ins Arbeitsheft“ im Blatt-Dialog (`heftAdd`) hängt Seiten an das gemerkte Heft an, auch an ein Heft aus dem Heft-Assistenten. Dann stimmen Kapitel, Inhaltsseite und Seitenzahl nicht mehr; für die Broschüre werden Leerseiten bis zur Vierer-Zahl eingefügt.
Vorschlag:
- **U1 Hefte nur noch über den Assistenten**, mit zwei Wegen: „für ein Kind“ (wie heute, Förderzone) und **„für einen Bereich“** ohne Kind und Test: Bereich und Stufen wählen (z. B. Mathe „Zahlen bis 20“ Stufe I–III, Deutsch L4–L6), Umfang 12/24/36/48, Namenszeile auf dem Deckblatt leer. Gleicher Kapitelaufbau (Einstieg, Üben, „Das kann ich schon“), gleiche Optionen (groß, Lineatur, Schwarz-Weiß, Druck).
- **U2 „Ins Arbeitsheft“ wird „Zur Blattsammlung“:** beliebig viele lose Blätter sammeln und zusammen drucken (A4 einseitig, mit Lösungen), ohne Deckblatt, Kapitel und Broschüre. Kein Mischen mit Heften mehr.
- **U3 Seite im Heft austauschen** statt anhängen: im Assistenten bei einem Kapitel „andere Aufgaben“ oder ein Blatt aus dem Generator an die Stelle einer Übungsseite setzen; Seitenzahl bleibt.

## V: Drucken auf iPad und iPhone (Stefan, 28.11.2026, mit Bildschirmfoto)

Beobachtung (Stefan, 08:50): Am Computer mit Chrome druckt alles sauber. Auf iPad und iPhone:
- **Home-Bildschirm-App:** „Drucken“ tut nichts. iOS öffnet aus Web-Apps im Vollbild keinen Druckdialog; `print()` wirft keinen Fehler, deshalb kommt auch der Hinweis „Drucken geht hier nicht direkt“ nicht.
- **Safari:** erst die Meldung „Diese Website wurde für das automatische Drucken gesperrt“ (Ignorieren/Erlauben). Nach „Erlauben“ geht es, je Adresse (stufenweise.app und test.stufenweise.app getrennt).
- **Kopf- und Fußzeile:** Safari druckt sie auf iPad/iPhone immer; unsere Seiten sind genau A4 ohne Rand (`@page{margin:0}`), deshalb rutscht Inhalt auf eine zweite Seite. Bisher nur ein Satz in der Heft-Notiz.

**Entscheidungen (Stefan, 28.11.2026, per Auswahl):**
1. **Hinweis:** Kasten direkt am Druck-Knopf, **nur auf iPad/iPhone** (Erkennung wie `safariTab()`): in Safari beim ersten Mal „Erlauben“ tippen; Kopf- und Fußzeile lassen sich nicht abschalten → im Druckdialog die Skalierung verkleinern, bis jede Seite auf ein Blatt passt; das sauberste Ergebnis gibt es am Computer. Am Computer kein Kasten.
2. **Keine automatische Verkleinerung** auf iOS – nur informieren (Seiten bleiben genau A4).
3. **Home-Bildschirm-App:** Der Knopf heißt dort **„Teilen und drucken“** und gibt das Dokument als Datei an das Teilen-Menü von iOS (`navigator.share` mit Datei); dort „Drucken“ wählen. Gilt für Einzelblatt, Blattsammlung, Heft, Lösungsheft und Berichte. Klappt das Teilen nicht, Hinweis auf „Als Datei speichern“ → in „Dateien“ öffnen → Teilen → Drucken. Muss am iPad in der Testversion (als App vom Home-Bildschirm) erprobt werden.

**Status:** **Erledigt in 0.44.0** (freigegeben 28.11.2026 nach Stefans Prüfung der Testversion).

