# Backlog

Geplante Entwicklungsaufgaben für Stufenweise. Begonnenes steht in `IN_PROGRESS.md`, Erledigtes in `CHANGELOG.md`.

Regeln (Stand 17.11.2026): Der Funktionsumfang von `main` ist eingefroren, weil die App an Schulen genutzt wird. Neues entsteht nur im Zweig `entwicklung`, wird in der Testversion gezeigt und erst nach Stefans OK freigegeben (`docs/entwicklung.md`). Didaktische Entscheidungen trifft Stefan.

Stand: 23.11.2026 (0.32.0)

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
| 7 | **H** Konzentrationsmodus für Kinder (+ Usability-Review) | klein bis mittel | gebaut in `entwicklung` (24.11.2026), wartet auf Stefans OK in der Testversion |

Alternative: B zuerst als schneller Gewinn, während Stefan den Basis-Test ausprobiert.

---

## H: Konzentrationsmodus für Kinder

**Status:** gebaut in `entwicklung` (24.11.2026), Testversion; wartet auf Stefans OK.
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
