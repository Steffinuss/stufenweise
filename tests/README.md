# Tests für Stufenweise

Automatische Tests, die die App in einem echten Chrome-Browser bedienen (mit [Playwright](https://playwright.dev/python/)). Sie klicken die Bereiche durch, prüfen auf JavaScript-Fehler, lassen simulierte Kinder üben und erzeugen Arbeitsblätter als PDF. Bildschirmfotos und PDFs landen in `tests/out/` (nicht im Repository).

## Voraussetzungen

- Python 3 mit `pip install playwright pillow`
- Chrome oder Chromium (sonst `playwright install chromium`)
- für die PDF-Prüfung der Legeblätter: `pdfinfo` und `pdftoppm` (Paket poppler-utils)

## Alles auf einmal

```sh
sh tests/run_all.sh                        # schnelle Tests (etwa 4 Minuten; nacheinander waren es 10½)
sh tests/run_all.sh lang                   # dazu alle Arbeitsblätter, simulierte Kinder, Zufallsklicks (etwa 7 Minuten; nacheinander 19)
sh tests/run_all.sh nur blatt_layout heft_gross   # nur diese Tests (Namen ohne „.py“; Zwanzigerfeld: zwanzigerfeld:1180x820)
STUFENWEISE_JOBS=1 sh tests/run_all.sh lang    # nacheinander wie früher
```

Die Tests laufen **gleichzeitig** (Standard: so viele wie Prozessorkerne, mindestens 2, höchstens 4; einstellbar mit `STUFENWEISE_JOBS`). Lange Tests starten zuerst. Das Skript startet selbst einen gemeinsamen Webserver auf Port 8766 (`STUFENWEISE_PORT`) und wartet, bis er antwortet; läuft dort schon einer, wird er benutzt. Jeder Test schreibt Bilder und PDFs in einen eigenen Ordner `tests/out/lauf/<Test>/` und seine Ausgabe nach `tests/out/lauf/<Test>.log`, so überschreibt kein Test die Dateien eines anderen. Während der Runde erscheint je fertigem Test eine Zeile mit der Dauer, am Ende die Liste in fester Reihenfolge: „ok“ heißt keine JavaScript-Fehler, kein Absturz und keine Zeile „ERR [...]“; bei „FEHLER“ stehen die letzten Zeilen der Ausgabe darunter. Viele Tests geben zusätzlich Messwerte aus; die stehen in der Logdatei.

## Gezielt testen

Bei kleinen Änderungen reicht oft ein Teil der Tests (`sh tests/run_all.sh nur …`). Vor einer Freigabe immer `lang`.

| Bereich der App | Tests |
| --- | --- |
| Start, Fehler allgemein | `fehler smoke einstellungen konzentrationsmodus handy` |
| Üben Mathe (Plus/Minus, Zwanzigerfeld, Zehnerpartner, Material) | `plusminus_ueben feld_ueben antwortfeld springen zehnerpartner_ueben mathe_material runden ueberspringen hinweis_neu gefuehrt` |
| Üben Deutsch (Lesen, Schreiben, Hören, Satz-Baukasten) | `deutsch_optimierung satz_ziehen tafel_rueckmeldung` |
| Basis | `basis_grundlagen basis_ueben basis_test basis_blaetter` |
| Test und Auswertung (Einstufung, Förderzone, Raten) | `test_fortschritt test_nie_haengen test_passt raten basis_test durchsicht_0_21` |
| Unterricht an der Tafel | `zwanzigerfeld:1180x820 zwanzigerfeld:390x844 zwanzigerfeld_zahl frei_stift satz_ziehen tafel_rueckmeldung` |
| Materialkiste | `materialkiste` |
| Arbeitsblätter (Layout, Optionen, Lineatur, Schwarz-Weiß, keine doppelten Aufgaben) | `blatt_layout keine_doppelten blatt_rueckmeldungen blatt_auswahl arbeitsblatt_optionen grosse_aufgaben hundertertafel_blaetter lineatur druck_seiten legeblaetter tausenderbuch_nachspuren` (lang: `arbeitsblaetter`) |
| Arbeitshefte, Heft-Assistent | `heft_assistent heft_gross heft_zone_optionen heft_scroll arbeitsheft lineatur plaene_sinnvoll` (lang: `heft_seiten_passen heft_seiten_gross`) |
| Lernstand, Berichte, Wochenübersicht | `lernort_material wochenuebersicht drittes_fach` |
| Daten: Speichern, Fenster, Sicherung, Umzug, Safari | `mehrere_fenster speicher_voll qr_umzug safari_tab update_hinweis` |
| Alle Aufgabentypen, Robustheit | (lang) `sweep zufallsklicks kinder_sim` |

## Einzelne Tests von Hand

Zuerst den Server starten: `python3 -m http.server 8766 --bind 127.0.0.1` im Repository-Ordner. Dann zum Beispiel `python3 tests/legeblaetter.py`.

| Test | Prüft |
| --- | --- |
| `fehler.py` | App lädt ohne JavaScript-Fehler |
| `smoke.py` | Startseite, PIN, Einstellungen, Schreiben: einmal durchklicken |
| `sweep.py` | alle Aufgabentypen aller Stufen erzeugen und darstellen (über 4.500) |
| `kinder_sim.py` (mit `simlib.py`) | 10 simulierte Kinder machen Tests und üben; Förderzonen plausibel |
| `zufallsklicks.py` | viele zufällige Klicks, die App darf nicht abstürzen |
| `arbeitsblaetter.py` | jedes Arbeitsblatt-Thema: passt auf die Seite, genug Aufgaben (`PRÜFEN` = ansehen) |
| `arbeitsblatt_optionen.py` | Materialbilder „1. Aufgabe vorgegeben, dann selbst zeichnen“, Zehnerpartner, Rechnen über die 10 (Beispiel ausgefüllt), Geld mit Cent, Einmaleins-Reihen |
| `basis_grundlagen.py` | Basis, Schritt 1: alle Bilder (Gegenstände, Farben, Größen, Formen, Pfeile, Spiegel-Zeichen, Punktbilder, Symbole) und vollständige Stufentexte V1–V8, O1–O5 |
| `basis_blaetter.py` | Basis, Schritt 2: alle Basis-Arbeitsblätter (V1–V7, O2–O4) in allen Varianten, Lösungen passend, Vorgemachtes nur in der ersten Aufgabe jeder Art, Schwarz-Weiß mit Mustern; Legeblätter Sortierunterlage, Zuordnungsleiste, Musterstreifen |
| `basis_ueben.py` | Basis, Schritt 3: alle Übungs-Generatoren V1–V8, O2–O4 (Lösung richtig, falsche Antwort falsch), jede Aufgabenart mit echten Klicks gelöst (Bild wählen, Sortieren, Verbinden, Reihenfolge, kurz zeigen), Fach für Gast sichtbar, für Kinder erst nach Einschalten, Statistik; Ablauf: Vormachen vor jeder neuen Aufgabenart, bei einer Art bleiben, nach 8 richtigen „Nächste Aufgabe“, nach 3 Fehlern leichter; Ziehen mit der Maus (in die Kiste, zurück in den Vorrat, unter das Bild, auf die Plätze 1, 2, 3) |
| `basis_test.py` | Basis-Test (Schritt 4): drei Teile (V1–V4, V5–V8, O2–O4), je Stufe Block a mit Vormachen (nicht gewertet, nichts antippbar), Block b nur nach a; Einstufung erreicht / teilweise / nicht, keine Ableitung; Förderzone in empfohlener Reihenfolge, ILEB, Lernstand mit Matrix und Hinweis bei Mathe I / L1, Elterninfo, Lernlandkarte, automatische Sichtbarkeit, „Heute für dich“ mit Basis zuerst, Re-Diagnose, Kurztest, Abbrechen |
| `blatt_auswahl.py` | Arbeitsblätter: Auswahl Fach → Bereich → Blatt, jedes Blatt genau einmal, Legeblätter beim Fach, zuletzt gewähltes Blatt beim Zurückwechseln, „Zuletzt benutzt“, Kind mit Förderzone stellt das Fach ein, Arbeitsheft über Fächer |
| `drittes_fach.py` | Mehr als zwei Fächer: ein Probe-Fach wird angemeldet und erscheint in Fachwahl, Startseite, Üben, Test, Lernstand, Klassenübersicht und Berichten; optional nur für eingeschaltete Kinder |
| `handy.py` | Handy hochkant: Startseite, Leiste, Aufgaben ohne Überlappung, Zifferntastatur unten; quer Hinweis zum Drehen; iPad unverändert |
| `test_passt.py` | Jede Testaufgabe passt auf kleinere iPads (1080 × 740 und Hochformat); nur lange Lesetexte scrollen mit Hinweis |
| `test_nie_haengen.py` | Jede Stufe hat mindestens 3 Aufgaben; Test läuft auch bei vielen falschen Antworten durch |
| `test_fortschritt.py` | Fortschritt im Test: Abschnitte in fester Reihenfolge, Balken läuft nur vorwärts, keine Bewertung |
| `oberflaeche_details.py` | Fachwahl Mathe/Deutsch mittig; Lineal-Gegenstände mit realistischen Längen |
| `durchsicht_0_21.py` | Randfälle: kaputte gemerkte Blatt-Einstellungen, geführte Oberfläche mit Zehnerpartnern, Ableitung aus R3, Klassenübersicht, Wiederholungstest |
| `zehnerpartner_ueben.py` | Üben „Zehnerpartner“ Z1–Z3 lösbar, Statistik; Blitzblick „Neue Aufgabe“ zählt als übersprungen |
| `grosse_aufgaben.py` | „Große Aufgaben“: nichts zu breit, alles größer; Minus „Umtausch schon im Bild zeigen“: Bild stimmt, Tausch reicht zum Wegstreichen |
| `doppelte_zeilen.py` | keine Zeile doppelt in einer Aufgabe (z. B. zweimal „7 = 4 + □“), keine gleichen Aufgaben direkt nacheinander |
| `legeblaetter.py` | alle Legeblätter als PDF: genau 1 Seite, nichts abgeschnitten (`scroll` ≤ verfügbare Höhe) |
| `arbeitsheft.py` | Arbeitsheft mit mehreren Blättern |
| `heft_assistent.py` | Arbeitshefte (Backlog J): Fach, 12/24/36/48 Seiten (gedruckt genau so viele), Vorgriff, Kapitel mit Einstieg/Üben/„Das kann ich schon“, Wiederholung, Hilfen, Lösungsheft, Mathe-Feinstufen, Fortsetzungsgeschichte, neue Deutsch-Formate, Broschürendruck, Layout B (Kopf- und Fußzeile auf jeder Seite, Seitenzahl gleich hoch, Aufgaben bis zur Fußzeile, keine Seite verkleinert), Deckblatt (Titel aus Kapiteln, Farbrand, Fachbild), Rückseite als Nachguckseite |
| `heft_seiten_passen.py` | (lang) Arbeitsheft: für jede Stufe Einstieg, Üben, „Das kann ich schon“ und Wiederholung bauen – keine Seite läuft über, gedruckt genau so viele Blätter, A5-Broschüre ohne abgeschnittene Seiten |
| `plaene_sinnvoll.py` | Erzeugte Inhalte ergeben Sinn: Stundenplan je Stufe (Fächer nach BP GENT, kein Fach jeden Tag in derselben Stunde), „Stimmt das?“-Sätze eindeutig, Stehendes nicht unter dem Tisch |
| `tausenderbuch_nachspuren.py` | Tausenderbuch-Seiten wählen, ganzes Buch, Nachspur-Buchstaben |
| `einstellungen.py` | Einstellungen mit Registerkarten |
| `runden.py`, `ueberspringen.py` | Übungsrunden; Überspringen zählt mit |
| `gefuehrt.py` | geführte Oberfläche zeigt die richtigen Bereiche |
| `antwortfeld.py`, `feld_ueben.py` | Antwortfeld in der Rechnung, Zwanzigerfeld beim Üben |
| `zwanzigerfeld.py BREITE HÖHE` | Tafelwerkzeug Zwanzigerfeld (Legen, Wegstreichen, Verdecken) |
| `springen.py` | nichts springt: Zwanzigerfeld bleibt beim ersten Tippen an seiner Stelle |
| `hinweis_neu.py` | „Richtig“ verschwindet bei der nächsten Aufgabe |
| `lernort_material.py` | Weg am Material für jede Stufe, Legeblatt-Knopf, ILEB-Maßnahmen |
| `materialkiste.py` | Materialkiste: Ablauf, alle Werkzeuge, Zählen, Taschenrechner, Lernstand/ILEB |
| `mehrere_fenster.py` | Zwei Fenster derselben App: nichts geht verloren, Löschen gilt weiter |
| `wochenuebersicht.py`, `update_hinweis.py` | Wochenübersicht; Update-Hinweis nur auf der Startseite |
| `blatt_layout.py` | Arbeitsblätter im Heft-Design (Backlog M): Kopf- und Fußzeile, Kästen bis zur Fußzeile, alle Blätter passen auf ihre Seiten, Schwarz-Weiß ohne bunte Farben, keine Aufgabe breiter als die Seite (auch große Aufgaben), Lochrand links 20 mm (Backlog S1/S8), Legeblätter unverändert, Heft mit genau einem Rahmen |
| `blatt_rueckmeldungen.py` | Stefans Rückmeldungen (Backlog S3–S7): Schwarz-Weiß-Material hellgrau, Pfeil schwarz, Kästchen zum Rechnen ab 1000, Umbruch nur zwischen Sätzen, Zehnerfeld als eine Reihe mit 10 (auch Tafel und Legeblatt) |
| `keine_doppelten.py` | Keine Aufgabe zweimal auf einer Seite (Backlog S9): alle Blätter mit „Seite füllen“, auch im Heft und in der Wiederholung |
| `lineatur.py` | Lineatur (Backlog L): Haus, zwei Linien, eine Linie; Standard nach Themenwelt; Auswahl bei Blättern mit Schreibzeilen und im Heft; Deckblatt-Zwanzigerfeld zeilenweise |
| `heft_gross.py` | „Große Aufgaben“ im Heft-Assistenten (Backlog N); Heft nimmt Grundeinstellungen statt der des letzten Einzelblatts |
| `heft_scroll.py` | Heft-Assistent: „+“ und „−“ springen nicht nach oben (iPad und Handy) |
| `heft_seiten_gross.py` | (lang) wie `heft_seiten_passen.py`, mit großen Aufgaben |
| `heft_zone_optionen.py` | Heft zur Förderzone: Schwarz-Weiß, Hundertertafel als Extraseite |
| `hundertertafel_blaetter.py` | Hundertertafel-Blätter H1–H6: Tafel im Titel, Extraseite auf Wunsch |
| `druck_seiten.py` | Druck = Vorschau: jedes Blatt im Heft und als Arbeitsblatt genau eine A4-Seite |
| `deutsch_optimierung.py` | Deutsch (Backlog I): eindeutige Bilder, „Kenne ich nicht“, Anhören, Silben, Hören P1–P4, Materialkiste und Unterricht Deutsch |
| `satz_ziehen.py` | Sätze legen mit Ziehen (Satz-Baukasten, Schüttelsätze) |
| `tafel_rueckmeldung.py` | Rückmeldungen aus dem Einsatz an der Tafel (vertauschte Satzteile, Zifferntastatur am Smartboard) |
| `frei_stift.py` | Stift beim „Frei legen“ an der Tafel |
| `zwanzigerfeld_zahl.py` | Unterricht → Zwanzigerfeld: Zahl vorgeben, Zufallszahl, verdecken |
| `plusminus_ueben.py` | Üben Plus und Minus (Backlog A): Zufallsaufgabe, Darstellung nacheinander |
| `mathe_material.py` | Test „mit Material“ (R1–R7), Üben bis „im Kopf“, Geld ziehen |
| `konzentrationsmodus.py` | Konzentrationsmodus (Backlog H) und Usability-Review |
| `qr_umzug.py` | Geräteumzug per QR-Code (große und kleine Codes, alte Formate) |
| `raten.py` | Raten im Test (Backlog Q1): Auswahlstufen erst bei 3 von 3; Simulation eines ratenden Kindes |
| `safari_tab.py` | Hinweis im Safari-Tab auf iPad/iPhone (Backlog P1) |
| `speicher_voll.py` | Voller Speicher wird gemeldet (Backlog O1), Sicherung mit ungespeichertem Stand |
| `shot.py BILD.png "js" "CLICK selektor" …` | Hilfsprogramm: Schritte ausführen und Bildschirmfoto speichern |

## Bilder für die Anleitung

```sh
python3 tests/anleitung_bilder.py                     # nimmt alle Bilder neu auf (Querformat 1180 × 820, „Testkind A“)
python3 tests/anleitung_markieren.py                  # umrandet den wichtigen Knopf orange
python3 tests/anleitung_markieren.py --uebernehmen    # kopiert die Bilder nach docs/bilder
```

Vorher die Bilder in `tests/out/anleitung/final/` ansehen. Ändert sich die Oberfläche stark, müssen die Klickschritte in `anleitung_bilder.py` angepasst werden.
