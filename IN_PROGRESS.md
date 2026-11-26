# In Arbeit

Was gerade begonnen ist. Erledigtes wandert nach `CHANGELOG.md`, Geplantes steht in `BACKLOG.md`.
Arbeitsweise mit zwei Zweigen: `docs/entwicklung.md`.

Stand: 26.11.2026

## Backlog J, Schritte 1–5: Arbeitshefte (gebaut in `entwicklung`, Testversion; Stefan: „erst alle Schritte bauen, dann freigeben“)

- Schritt 1 Heft-Assistent, 2 Kapitelaufbau (Einstieg, Üben, „Das kann ich schon“, Wiederholung, Hilfen hinten, Lösungsheft), 3 Mathe-Feinstufen, 4 Deutsch-Stoff (Texte, Geschichten, Papier-Formate), 5 Broschürendruck. Details: `CHANGELOG.md` „Unveröffentlicht“.
- **Texte freigegeben** (Stefan, 26.11.: „Die Texte sind gut. Bei den Fragen folge ich deinen Vorschlägen.“): Geschichte nur ab Förderzone L6/W5, neue Kurz- und Langtexte auch in der App, Themen und Namen bleiben. Texte in `TEXTS_NEU`, `TEXTS_MID`, `LONG_NEU`, `STORIES`; Prüfseite aus `node tests/texte_pruefseite.mjs`.
- **Offen vor der Freigabe:** Stefans Rückmeldung zur Testversion bzw. „freigeben“ (offen von Schritt 1: Seitenverteilung, Standard-Fach „Gemischt“).
- Seitenplanung (`heftPlan`): Gewicht Förderzone 3, nächste Stufe 2 (− halbiert, + verdoppelt); „bis voll“ nimmt reihum weitere Stufen, solange `(Summe Gewichte) × 2,5 ≤ Seiten`. Außerhalb der Kapitel: Deckblatt, eigene Inhaltsseite (> 8 Einträge), Wiederholung nach je zwei Kapiteln, Hilfen, 2 Seiten je Geschichtsteil (min(6, Seiten/8)). Kapitel ≥ 3 Seiten: Einstieg + Üben + „Das kann ich schon“; 2 Seiten: Einstieg + Üben; 1 Seite: Üben.
- Danach (später, Stefan): Heft merken und Folgeheft vorschlagen (Frage 8).

## Rückmeldung Stefan 26.11. (gebaut in `entwicklung`)

- Überlauf im Heft (54 statt 48 Seiten, abgeschnittene Seite in der Broschüre) behoben, siehe `CHANGELOG.md`. Menü „Material drucken“.
- Seiten gleichmäßig gefüllt, Seitenzahl fest unten, Stundenplan nach BP GENT, weitere Unstimmigkeiten (Sätze, Sachaufgaben) behoben. Frage an Stefan: Im BP GENT heißt das Fach „Wirtschaft und Berufsorientierung“ (WBO), Stefan schrieb „WBS“ (Name an der Gemeinschaftsschule) – im Stundenplan steht WBO.

## Heft-Layout B (Stefan, 26.11.2026, gebaut in `entwicklung`)

- Drei Vorschläge als Bilder gezeigt (A: Abstände verteilen, B: Aufgaben strecken, C: Platz zum Rechnen). Stefan: „Ich bin für Layout B. Gerne kannst du noch optimieren, dass es insgesamt weniger große Lücken gibt.“
- Gebaut: `heftFrame` (Kopf-/Fußzeile aus Band und Fußzeilen der Seite), CSS in `buildHeft` (Seite als Spalte, `.ab-grid` wächst), `PAGE_FIT_JS` lässt Kopf- und Fußzeile unverkleinert, Messen mit Rahmen, keine Verkleinerung im Heft (`tight`), größerer Aufgabenvorrat beim Füllen. Test: `heft_assistent.py` (Layout B: Kopf/Fuß, bis zur Fußzeile gefüllt, nichts verkleinert, Seitenzahl gleich hoch).

## Deckblatt C4 und Rückseite (Stefan, 26.11.2026, gebaut in `entwicklung`)

- Vorschläge A (Rahmen), B (Farbband), C (Stufen); Stefan: C, aber andere Mitte → C1 Lernweg, C2 Kapitelkarten, C3 Fachbild, C4 Fachbild mit Inhalt. Stefan: „Ich finde C4 auch gut. Den farbigen Rand finde ich super … Für das gemischte Heft würde ich halb-halb vorschlagen.“ Dazu Wunsch: Rand auf der Rückseite fortsetzen (Regal), Rückseite als Nachguckseite je nach Thema, Anlauttabelle letzte Zeile voll.
- Gebaut: `heftSubj`, `heftBand`, `heftTitleAuto`, `heftBild`, `FACH_COL`; Rückseite `it.back` (`heftBackFor`, `backOf` in `heftPlan`, `P.back`), neue Hilfen `zf`, `stw`, `merk`, `form` (nur als Rückseite); Broschüre: Leerseiten vor die Rückseite. Inhalt bleibt auf dem Deckblatt (Stefans Frage nach eigener Inhaltsseite: Empfehlung C4, Stefan einverstanden).

## Backlog K: Fußzeile ohne Namen (gebaut in `entwicklung`, 26.11.2026)

- Kommt mit Backlog J zusammen in die Freigabe (0.38.0). Anleitungsbilder dann neu aufnehmen (zeigen noch die alte Fußzeile).
