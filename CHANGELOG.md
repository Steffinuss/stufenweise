# Änderungen

Abgeschlossene Änderungen, neueste oben. Geplantes steht in `BACKLOG.md`, Begonnenes in `IN_PROGRESS.md`.
Versionen: Hauptversion.Nebenversion.Korrektur (Korrektur = Fehlerbehebung, Nebenversion = neue Funktion). Ältere Versionen: siehe Git-Historie und GitHub-Releases.

## Unveröffentlicht (Zweig `entwicklung`, Testversion)

- noch nichts

## 0.34.1 – 25.11.2026

- Testversion zieht nach test.stufenweise.app um: Sie erkennt sich jetzt auch an der Adresse (beginnt mit `test.`) und hält ihre Daten weiter getrennt (Vorsatz `test:`). `tests/testversion.sh` schreibt dafür die Datei `CNAME` mit `test.stufenweise.app`.

## 0.34.0 – 24.11.2026

Neu (Backlog I „Optimierung Deutsch“, Stefans Antworten im Dokument vom 24.11.2026):
- **Bilder beim Schreiben:** nur eindeutige Bilder (Üben, Test, Anfangsbuchstaben, Arbeitsblätter W2–W5); Tulpe, Rose und Kanne weggelassen. **Kenne ich nicht** beim Üben: Wort mit Bild zeigen, abdecken, aus dem Gedächtnis schreiben (zählt „mit Hilfe“); im Schreib-Test ein anderes Bild (höchstens zweimal je Stufe). Lernstand: „Bilder, die nicht erkannt wurden (Wortschatz)“. **Bilder vorher ansehen** (Knopf für die Lehrkraft): die Bilder der nächsten Runde mit Wort. **Bilder abwählen** für die Klasse (Einstellungen → Deutsch).
- **Anhören (Sprachausgabe, zum Ausprobieren):** Lautsprecher-Knopf liest nur das Wort vor (Schreiben, Schreib-Test, Hören, Bildwörterbuch). Nur Stimmen auf dem Gerät, nichts übers Internet. Einstellungen → Deutsch: Standard für alle Kinder, je Kind abweichend, Stimme, Tempo, Probe.
- **W4 Silben:** Kästchen unter Silbenbögen; beim Üben zusätzlich Silbenkarten legen.
- **Hören P1–P4** mit Übungen (Silben zählen, Silben verbinden, Reime, Anlaute) und im Lese-Test, wenn L4 noch nicht erreicht ist; Arbeitsblätter „Hören“.
- **Materialkiste Deutsch:** Anlauttabelle, Bildwörterbuch, Wörter. Die Nutzung steht im ILEB-Vorschlag Lesen/Schreiben.
- **Unterricht Deutsch:** Anlauttabelle, Blitzlesen, Satz-Baukasten.
- **W6 Sätze schreiben** (nur Üben): nur echte Sätze – eigener Satz zum Bild und „Satz merken und aufschreiben“ (Großschreibung und Punkt werden geprüft). Der W6-Test bleibt wie bisher.
- **Schüttelsätze** (neuer Punkt unter Lesen, nur Üben, kein Test): Wortkarten zu einem Satz ordnen, mit und ohne Bild.
- **Einkaufszettel** (neuer Punkt unter Schreiben, nur Üben, kein Test): die Wörter einer Liste kommen nacheinander.
- **Legeblatt „Bildkarten mit Wort“** (Wortschatz, Memory; für ein Kind zuerst seine unbekannten Bilder).
- **Mathe, Hundertertafel „Finden“:** auch teilweise verdeckt (erste Zeile und Zehnerzahlen) und verdeckt; wechselt von selbst (8 richtig → weiter, 3 Fehler → zurück), Lehrkraft wählt oben. Nicht im Test.
- **Mathe-Test „mit Material“** (Stefan 24.11.): Klappt eine Rechenstufe (R1–R7) ohne Material nicht sicher, kommen zwei bis drei Aufgaben derselben Art mit Material: Punktefeld (bis 20), Zehnerstangen und Einer zum Legen mit Tauschen (bis 100), Hunderterplatten (bis 1000), Punktebild (Einmaleins). Gelingt es damit, steht im Lernstand „teilweise – mit Material“ (½ᴹ, im ILEB „Mit Material gelingt: …“). Die Suche im Test springt wie bisher.
- **Mathe-Test, Geld legen:** Scheine und Münzen lassen sich auch ziehen (auf den Tisch und wieder weg).
- **Üben im Kopf:** Plus und Minus haben als letzte Darstellung „Im Kopf“ (nur die Rechnung); Einmaleins wechselt nach 8 auf Anhieb richtigen von „mit Punktebild“ zu „im Kopf“ (3 Fehler → zurück, „Bild zeigen“ hilft).
- **Mengen legen und abzählen** (Zahlen im Konzentrationsmodus): oben „Aufgabe … von 10“ wie bei den anderen Übungen.
- Test `tests/mathe_material.py`; `tests/plusminus_ueben.py` kennt die Stufe „Im Kopf“.
- Test `tests/deutsch_optimierung.py`; `tests/materialkiste.py` zählt jetzt 10 Werkzeuge.

Nach Stefans Rückmeldung zur Testversion (24.11.2026):
- **Satz-Baukasten:** „Neuer Satz“ erzeugt Sätze aus dem Alltag (kurz, mittel, lang); der Satz steht nicht mehr oben sichtbar. „Eigener Satz“ öffnet ein kleines Feld, das Getipptes als Punkte zeigt.
- **Anlauttabelle:** Bilder für alle Buchstaben (neu: Computer, Qualle, Vogel, Xylofon, Yoga, Ähre, Öl, Überraschungsei (ohne Marke gezeichnet), Eule bei Eu). Selbstlaute mit langem (Strich) und kurzem (Punkt) Laut: Ameise/Apfel, Esel/Ente, Igel/Insel, Ofen/Ordner, Uhr/Unterhose; beim Buchstaben getrennt nach „lang gesprochen“ und „kurz gesprochen“. „Anlaute hören“ (P4) nutzt deshalb nur Mitlaute.
- **Bilder neu gezeichnet:** Ente (Stockente statt Badeente), Esel und Kamel ohne Linien an den Übergängen von Kopf, Hals und Körper.

## 0.33.0 – 24.11.2026

Neu (Backlog H, Usability-Review vom 24.11.2026, Stefans Antworten im Dokument):
- **Konzentrationsmodus** für alle Kinder, Standard an (Einstellungen → Kinder): Beim Üben sind Leiste, Einstellleiste, Name und Menü ausgeblendet. Oben stehen „Aufgabe 3 von 10“ mit Punkten, „Weiter“ (erst nach der Lösung oder nach zwei Fehlversuchen) und „Pause“ (zurück zur Startseite). Das Zahnrad zeigt mit der PIN alles bis zur Pause. Auch auf der Startseite keine Leiste. Nicht im Unterricht, im Test und in der Materialkiste.
- **Zahlen mit Material im Konzentrationsmodus = Zählaufgabe:** Die Zahl und die Ziffern erscheinen erst, wenn das Kind richtig gezählt hat (vorher stand bei „Wie viele sind es? Zähle nach.“ die Zahl schon da). Im Lernstand als „Zahlen: Mengen abzählen“.
- **Geld im Konzentrationsmodus:** Auswahl „Betrag legen“ oder „Wechselgeld“ als große Kacheln.

Geändert:
- **Wechselgeld:** oben nur „Lege das Wechselgeld.“, das Feld heißt „Wechselgeld“; die Rechnung (10 € − 7 € = 3 €) erscheint erst nach dem Lösen. Der Tipp (auch bei „Betrag legen“) kommt erst nach einem Fehlversuch.
- **Rundenende:** „Runde vorbei“ statt „Geschafft!“, wenn nichts gelöst oder mindestens die Hälfte übersprungen wurde.
- Startseite: kürzerer Satz („Was möchtest du üben?“); auf dem iPad bleibt nach dem Antippen keine Kachel hell hinterlegt.
- Uhr: „Volle Stunden“ und „Halbe Stunden“ ausgeschrieben; der Pfeil oben heißt „Neue Aufgabe“.
- Umschalter Mathe/Deutsch 44 px hoch; Materialkiste: „Kiste zu“ statt „Fertig“, Taschenrechner ohne Material in der Mitte.
- Lernstand: Sprungmarken je Fach oben; Arbeitsblätter: Druckhilfe aufklappbar („Probleme beim Drucken?“).
- Anleitung: Abschnitt „Konzentrationsmodus“, Bilder neu.

## 0.32.0 – 23.11.2026

Geändert:
- **Hundertertafel-Arbeitsblätter** (Backlog G, Stefan): Die Blätter H1–H6 nennen die Hundertertafel im Titel (zum Beispiel „Nachbarn und Lücken in der Hundertertafel“), und über den Aufgaben steht ein kleines Tafel-Bild mit „Hundertertafel“. Neues Häkchen „Ausgefüllte Hundertertafel als Extraseite zum Nachschauen“ (aus, wird gemerkt): eine Seite mit der Tafel 1 bis 100 nach dem Blatt; kommt auch ins Arbeitsheft.
- **Heft zur Förderzone mit Optionen** (Backlog G, Stefan): Häkchen „Schwarz-Weiß-Drucker“ (nur wenn Basis-Blätter dabei sind) und „Ausgefüllte Hundertertafel als Extraseite zum Nachschauen“ (nur wenn Hundertertafel-Blätter dabei sind; die Tafel kommt einmal hinten ins Heft). Beide werden gemerkt. Bisher übernahm das Heft zur Förderzone die Schwarz-Weiß-Einstellung unsichtbar vom zuletzt gedruckten Basis-Blatt.

## 0.31.0 – 23.11.2026

Geändert:
- **QR-Umzug viel schneller** (Backlog E, Stefan): größere Codes (700 statt 230 Bytes je Code), Übungen kompakter verpackt (etwa halb so viele Daten) und schnellerer Wechsel (0,4 statt 0,65 s). Beispiel 6 Kinder mit je 800 Übungen: 25 statt 148 Codes, ein Durchlauf etwa 10 statt 96 Sekunden. Das empfangende Gerät wertet das Kamerabild genauer aus. Schalter **Kleine Codes** unter den Codes als Rückfall, falls eine Kamera nicht mitkommt (wird gemerkt).
- Beide Geräte brauchen dieselbe Version: Ältere Versionen übergehen die neuen Codes; eine neuere Version meldet am empfangenden Gerät „bitte aktualisieren“. Codes älterer Versionen werden weiter gelesen.

Fehlerbehebung:
- **F3: Druck wie Vorschau** (Stefan, 23.11.): Im Arbeitsheft rutschten das Inhaltsverzeichnis und lange Deutsch-Aufgaben (z. B. „Längere Texte verstehen“) im Druck auf ein weiteres Blatt, oft nur mit der Fußzeile; in der Vorschau sah alles passend aus, weil ein Blatt dort länger als A4 sein durfte. Jetzt wird jedes Blatt, das etwas zu hoch ist, im Druckdokument selbst auf eine Seite verkleinert (höchstens auf 80 %, in allen Browsern, auch in einer gespeicherten Datei). Passt es so nicht, zeigt die Vorschau „wird auf 2 Blätter gedruckt“. Das Deckblatt hatte im Druck andere Maße als in der Vorschau (das ist entfernt); bei mehr als 8 Seiten steht das Inhaltsverzeichnis auf einer eigenen Seite. Legeblätter und Berichte sind unverändert.
- **F2:** Bei sehr vielen Daten zeigte die App „von jedem Kind die letzten 0 Übungen“, übertrug aber alle Übungen (daher z. B. 109 Codes bei 6 Kindern). Jetzt wird nur gekürzt, wenn es auch mit großen Codes nicht passt, und die Anzeige stimmt („mit allen Übungen“, „die letzten …“ oder „ohne Übungen“).

Für Entwickler*innen: Format 2 (`v:2`, Kopfbyte 2), `colPack`/`colUnpack` (verlustfrei, Zeitstempel als Abstände, Schlüsselreihenfolge über Formen), `QR_MODES`, `settings.qrSmall`; neuer Test `tests/qr_umzug.py` (echter Umzug zwischen zwei Browsern über Bilder und den eingebauten Leser). Druck: `PAGE_FIT_JS` (im Kopf von Arbeitsblatt, Legeblatt und Heft; `window.__fitPages`, `.fitz` nur beim Verkleinern, `data-fit`, `data-over`), `sheetFit` misst ohne Verkleinerung; neuer Test `tests/druck_seiten.py` (Chrome-Druck als PDF, Seiten gezählt).

## 0.30.1 – 20.11.2026

Geändert:
- Die Zählung der Materialkiste steht nur noch im Lernstand (auch beim Kopieren) und im ILEB-Vorschlag Mathe, nicht mehr in der Elterninfo (Stefan).

## 0.30.0 – 20.11.2026

Neu:
- **Materialkiste** (Backlog D): vierte Kachel auf der Startseite neben Üben, Unterricht und Testen. Hilfen für Kinder, die eine Aufgabe haben (z. B. vom Arbeitsblatt): Rechenhilfe, Taschenrechner, Frei legen, Zwanzigerfeld, Hundertertafel, Zahlenstrahl, Uhr. Für alle Kinder, auch in der geführten Oberfläche; keine Bewertung, keine Runden, kein „Schwerer/Leichter“, freier Zahlenraum.
- **Taschenrechner** in der Materialkiste: plus, minus, mal (·), geteilt (:) mit Zahlen bis 10 000, große Tasten, auch mit der Tastatur; geteilt mit Rest; Ergebnis wahlweise als Material (Tausender, Hunderter, Zehner, Einer).
- Gezählt wird nur, wie oft ein Kind welches Werkzeug öffnet (Gast: nichts): im Lernstand „Materialkiste (selbst genutzt)“ (auch beim Kopieren und in der Elterninfo; ab 0.30.1 nicht mehr in der Elterninfo) und im ILEB-Vorschlag Mathe als Satz unter „Lernstand“.

Geändert:
- Die Rechenhilfe ist aus der Mathe-Leiste und den Mathe-Kacheln in die Materialkiste umgezogen. Aufgaben in der Rechenhilfe werden nicht mehr protokolliert.
- Hilfe in der App und Anleitung beschreiben die Materialkiste; Bildschirmfotos der Anleitung erneuert.

Für Entwickler*innen: `app.kiste`, `KISTE_TOOLS`, `kisteGo`, `kisteCount`, `data.kiste[pid][werkzeug]` (beim Zusammenführen mehrerer Fenster addiert wie `errs`), Taschenrechner `app.tr`/`renderTcalc` als Werkzeug in `TOOL_MODES` (`tcalc`); neuer Test `tests/materialkiste.py`.

## 0.29.1 – 20.11.2026

Fehlerbehebung:
- **Kinder gingen verloren, wenn die App in mehreren Fenstern offen war** (z. B. installierte App und Browser-Tab, gemeldet von Stefan nach dem Update auf 0.29.0). Jedes Fenster schrieb beim Speichern seinen ganzen eigenen Stand zurück; ein länger offenes Fenster überschrieb so neuere Kinder und Ergebnisse, besonders über „Jetzt aktualisieren“. Jetzt führt jedes Fenster beim Speichern zusammen statt zu überschreiben: Neues aus allen Fenstern bleibt, entfernt wird nur, was ein Fenster wirklich gelöscht hat (Kind löschen, „Daten löschen“, Einstufung entfernen). Fehlerzähler aus beiden Fenstern werden addiert.
- Offene Fenster übernehmen Änderungen anderer Fenster sofort (auf der Startseite gleich sichtbar), auch die Einstellungen.
- Sicherheitsnetz: Ein Stand ohne Kinder wird nie über einen Stand mit Kindern gespeichert, außer beim Löschen des letzten Kindes oder beim Ersetzen durch eine Sicherung.
- „Jetzt aktualisieren“ speichert vor dem Neuladen nicht mehr extra.
- Ein nicht lesbarer gespeicherter Stand wird vor dem Überschreiben unter `stufenweise.data.defekt` im Browser aufgehoben.

Für Entwickler*innen: `saveData()` mit Dreiwege-Abgleich (`dataBase`, `merge3`, `mergeStores`, `adoptStore`), `storage`-Listener; neuer Test `tests/mehrere_fenster.py` (16 Prüfungen, auch im schnellen Testlauf).

## 0.29.0 – 20.11.2026

Neu:
- **Basis-Test** in drei kurzen Teilen (V1–V4, V5–V8, O2–O4): Vormachen vor jeder neuen Aufgabenart, je Stufe leichte und schwerere Form, Kompetenzmatrix mit zwei Bereichszeilen, Förderzone, ILEB-Vorschläge, Elterninfo, Lernlandkarte; Hinweis im Lernstand, wenn Mathe „Zahlen bis 10, Stufe I“ oder Lesen L1 nicht erreicht ist.
- **Eingang „Testen“** auf der Startseite (Testen → Wer? → Welcher Test?), nach Fach geordnet mit Stand und Wiederholung. Die Test-Knöpfe im Fenster „Wer übt?“ sind weg; dort gibt es das Häkchen Basis pro Kind.
- **Plus und Minus aufgeteilt** (Backlog A): Üben mit Zufallsaufgaben, die Darstellung kommt von selbst nacheinander (bis 20 Material → Zwanzigerfeld → Zahlenstrahl, bis 100 Material → Hundertertafel → Zahlenstrahl, bis 1000 Material → Zahlenstrahl; nach 8 richtigen weiter, nach 3 Fehlern zurück); neue **Rechenhilfe** für eigene Aufgaben mit freier Darstellung, für alle Kinder.
- **Basis: schwerer durch Ähnlichkeit** (Backlog C): V1–V3 steigen in zwei Richtungen, mehr Bilder und deutlich → ähnlich → fein; 12 neue Bilder; Arbeitsblätter V1–V3 mit Auswahl „Ähnlichkeit“.
- **Unterricht, Zwanzigerfeld: Zahl vorgeben** (Backlog B): Zahl eingeben oder „Zufallszahl“; „Zahl verdecken“ wirkt auch auf die Anzahl allein.

Geändert:
- Basis „Jedem eins“: frei hinlegen mit mehr im Vorrat, damit man auch etwas falsch machen kann.
- Basis-Arbeitsblätter: Das Beispiel zeigt nur den ersten Schritt; Kuchengabel mit 3 Zinken.
- Texte V3 und V6 passen zu dem, was der Test prüft.
- Anleitung und Hilfe in der App beschreiben Testen, Basis-Test, Rechenhilfe und Ähnlichkeit; Bildschirmfotos erneuert.

Durchsicht vor der Freigabe (20.11.2026):
- Rechenhilfe schlägt kein „Schwerer/Leichter“ mehr vor (sonst wurde aus der eigenen Aufgabe eine Zufallsaufgabe).
- Rechenhilfe endet sauber, wenn man über die Startseite in eine andere Übung geht.
- Toter Knopf-Code der alten Test-Knöpfe entfernt; `tests/anleitung_bilder.py` läuft wieder (über „Testen“).

Für Entwickler*innen: Testversion mit eigenem Speicher (`TEST_BUILD`, Vorsatz `test:`) und Skript `tests/testversion.sh`; Arbeitsweise mit zwei Zweigen in `docs/entwicklung.md`; `BACKLOG.md`, `IN_PROGRESS.md`, `CHANGELOG.md`; neue Test-Haken in `docs/neues-fach.md`.

## 0.28.5 – 17.11.2026 (Release v0.28.5, eingefrorener Stand für Schulen)

- Basis: Aufgabe springt und schrumpft nicht mehr beim Vormachen; kein Zahlenstrahl-Symbol mehr bei „Dazulegen“.

## 0.28.4 – 17.11.2026

- Arbeitsblätter: Auswahl in drei Schritten (Fach → Bereich → Blatt), „Zuletzt benutzt“.

## 0.28.0 – 0.28.3 – 17.11.2026

- Basis üben in der App: Bild wählen, Sortieren, Dazulegen, der Reihe nach legen, kurz zeigen; Fach pro Kind einschaltbar.
- Eine Aufgabenart nach der anderen, Vormachen vor jeder neuen Art, Schieben statt Linien, Vorgabe und Auswahl gleich groß, Basis zuerst in der Fachwahl (Rückmeldungen Stefan).

## 0.27.0 – 17.11.2026

- Basis-Arbeitsblätter V1–V7, O2–O4 (auch schwarz-weiß) und Legeblätter Sortierunterlage, Zuordnungsleiste, Musterstreifen.

## 0.26.0 – 0.26.2 – 17.11.2026

- App für mehr als zwei Fächer umgebaut (`SUBJECTS`, `TESTS`, `AXES`; `docs/neues-fach.md`).
- Basis: Bilder (Alltagsgegenstände, Formen, Pfeile, Spiegelzeichen, Punktbilder) und Stufentexte.

## 0.25.0 und älter

- Handy-Ansicht (0.25.0), Durchsicht aller Tests vor dem Einsatz mit Kindern (0.24.0), Fortschrittsanzeige im Test (0.23.0), Zehnerpartner, Arbeitsblatt-Optionen und vieles mehr: siehe Git-Historie.
