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

## Backlog K: Fußzeile ohne Namen (gebaut in `entwicklung`, 26.11.2026)

- Kommt mit Backlog J zusammen in die Freigabe (0.38.0). Anleitungsbilder dann neu aufnehmen (zeigen noch die alte Fußzeile).
