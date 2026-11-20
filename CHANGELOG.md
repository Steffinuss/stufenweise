# Änderungen

Abgeschlossene Änderungen, neueste oben. Geplantes steht in `BACKLOG.md`, Begonnenes in `IN_PROGRESS.md`.
Versionen: Hauptversion.Nebenversion.Korrektur (Korrektur = Fehlerbehebung, Nebenversion = neue Funktion). Ältere Versionen: siehe Git-Historie und GitHub-Releases.

## Unveröffentlicht (Zweig `entwicklung`, Testversion)

- noch nichts

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
