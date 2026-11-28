# Änderungen

Abgeschlossene Änderungen, neueste oben. Geplantes steht in `BACKLOG.md`, Begonnenes in `IN_PROGRESS.md`.
Versionen: Hauptversion.Nebenversion.Korrektur (Korrektur = Fehlerbehebung, Nebenversion = neue Funktion). Ältere Versionen: siehe Git-Historie und GitHub-Releases.

## Unveröffentlicht (Zweig `entwicklung`, Testversion)

## 0.44.0 – 28.11.2026

Freigegeben von Stefan am 28.11.2026 nach Prüfung der Testversion („Super. Du kannst erst mal alles freigeben.“): Drucken auf iPad und iPhone (Backlog V). Anleitung ergänzt (Abschnitt „Drucken auf iPad und iPhone“), Anleitungsbilder neu aufgenommen.

- **Drucken auf iPad und iPhone** (Backlog V, Stefan 28.11.2026, Entscheidungen per Auswahl, danach „Ja, so bauen“): Nur auf iPad/iPhone steht unter den Druck-Knöpfen (Einzelblatt, Blattsammlung, Heft, Bericht) ein Hinweiskasten (`printHint`, `.note.print-ios`): in Safari beim ersten Mal „Erlauben“, Kopf- und Fußzeile lassen sich nicht abschalten → im Druckdialog die Skalierung verkleinern, Legeblätter nicht, am saubersten am Computer. Keine automatische Verkleinerung (Stefans Wahl). In der **App vom Home-Bildschirm** heißen die Knöpfe „Teilen und drucken“ (`prLabel`) und geben das Dokument als HTML-Datei ans Teilen-Menü (`shareDoc`, `navigator.share`); geht Teilen nicht, Hinweis auf „Als Datei speichern“. Erkennung `iosDevice`/`iosApp` (für Tests `window.STUFENWEISE_IOS`). Der Satz „Auf dem iPad lässt sich die Fußzeile nicht abschalten …“ in den Notizen entfällt (steht jetzt im Kasten). Anleitung: Abschnitt „Drucken auf iPad und iPhone“. Test `drucken_ios.py`.
## 0.43.0 – 28.11.2026

Freigegeben von Stefan am 28.11.2026 nach Durchsicht der Testversion („Super gib alles frei“): Basis-Arbeitsblätter mit einer Aufgabenart je Blatt (Backlog T) und aufklappbare Seitenliste im Heft-Assistenten. Anleitung ergänzt (Basis-Blätter: Aufgabe, Bastelseite; Basis im Arbeitsheft), Anleitungsbilder neu aufgenommen.

- **Seitenliste im Heft-Assistenten ausblendbar** (Stefan 27.11.2026, 17:54: „Detailauswahl im Heftassistenten ausblendbar machen und standardmäßig ausgeblendet“; danach „Ja, so bauen“): Die Liste der Kapitel und Seiten mit „Austauschen“ steht jetzt in der aufklappbaren Zeile „Seiten im Heft (n) – zum Austauschen aufklappen“ (`details.hf-pages`), anfangs zu. Auf/zu gilt, solange der Dialog offen ist (`app.heftListOpen`, z. B. nach einem Austausch); beim nächsten Öffnen (`openSheets`, `openHeftZone`) ist sie wieder zu. Test: `heft_stringent.py`.
- **Basis-Arbeitsblätter: eine Aufgabenart je Blatt** (Backlog T, Stefan 27.11.2026, alle Entscheidungen per Auswahl, danach „Ja, so bauen“; Konzept im Claude-Doc „Konzept: Basis-Arbeitsblätter überarbeiten (Backlog T)“):
  - Neue Auswahl **„Aufgabe“** im Blatt-Dialog bei allen zehn Basis-Blättern, Arten von leicht nach schwer wie in der App (V1 einkreisen vor verbinden, V3 erst Farbe bei gleichen Dingen). Je Blatt gemerkt (`app.sheet.bart`, in `SHEET_KEEP`). Keine Mischung mehr: auf dem ganzen Blatt ein Auftragssatz. Die Art steht im Titel („Der Größe nach ordnen: Das größte“). „Ähnlichkeit“ erscheint nur bei Arten, die sie nutzen.
  - **Erste Aufgabe ganz vorgemacht** (alle Linien, alle Kreise; ersetzt „nur der erste Schritt“ vom 19.11.). Nichts zum Lesen ankreuzen (kein „ja/nein“, kein „☐ gleich viele“).
  - **V2** eine Bildreihe je Kasten, zwei Kästen nebeneinander, bis 12 Aufgaben; „Andere Farbe“ und „Andere Größe“ getrennt (vorher zufällig gemischt). **V4** Gabeln stehen zusammengeschoben (links, mittig oder rechts) statt schon unter den Tellern, je Blatt dasselbe Paar; „Reicht es?“ = verbinden und den Teller ohne Gabel einkreisen (es fehlt immer genau eine). **V5** drei Arten; „Gleich viele“ mit drei Kästen, die zwei gleichen (anders verteilt) einkreisen. **V6 „Ordnen“** zum Ausschneiden und Aufkleben auf eine Treppe (klein unten, groß oben); die Teile stehen auf einer **Bastelseite mit leerer Rückseite**: Blatt, Leerseite, Bastelseite, Leerseite (Stefans Wahl). Treppe und Teile in echter Größe, auch bei „Große Aufgaben“. Auf der Bastelseite (Stefan, 28.11.): jedes Teil mit eigener gestrichelter Schnittlinie und Scheren-Symbol, kleine Aufgabennummer auf jedem Teil, die Teile einer Aufgabe in einem Rahmen mit großer Nummer.
  - **O2, O3, V3 „Nach Art“**: gesuchte Form, Richtung bzw. Gruppe je Blatt fest (zufällig) und groß oben auf dem Blatt (`bb-ziel`, `B_FIX`).
  - **Heft-Assistent**: eine Art je Seite – Einstieg die leichteste, Übungsseiten der Reihe nach (bei wenigen Seiten die leichteren, innerhalb einer Art deutlich → ähnlich → fein), „Das kann ich schon“ die schwerste geübte Art, Wiederholung mit nur einem Basis-Kapitel. „Ordnen“ höchstens einmal als Übungsseite, die Bastelseite zählt im Umfang mit. In den Broschüren steht jede Bastelseite auf einer rechten Seite mit leerer Rückseite (Leerseiten setzt `heftNorm`; dadurch kann eine Broschüre einige Seiten länger werden). „Austauschen“ nimmt die Bastelseite mit; „Anderes Blatt wählen“ geht jetzt auch mit „Ordnen“.
  - Doppelte Aufgaben werden bei Basis-Blättern am Bild erkannt (vorher nur am Text, mit einer Art je Blatt wären Blätter halb leer geblieben).
  - Bei „Große Aufgaben“ bleiben Verbinde-Aufgaben kompakter, damit mindestens zwei aufs Blatt passen; die Linien im Beispiel blähen die Aufgabe beim Messen nicht mehr auf.
  - Tests: neu `basis_eine_art.py` (in `run_all.sh`); angepasst `basis_blaetter.py` (Beispiel ganz vorgemacht). `run_all.sh lang`: 67 × ok.

## 0.42.0 – 27.11.2026

Freigegeben von Stefan am 27.11.2026 nach Durchsicht der Testversion („Kannst du alles freigeben ist jetzt super“), auch der Broschüre-Fix auf dem iPad. Anleitungsbilder neu aufgenommen.

- **Broschüre lief auf Handy und altem iPad über** (Rückmeldung Stefan 27.11.2026, 12:39: „Zu lang für ein Blatt“ auf Einstiegs- und „Das kann ich schon“-Seiten, auf dem Smartboard passte es): Vermutete Ursache ist die automatische Schriftvergrößerung von Safari (iOS) bei sehr kleiner Darstellung – in der A5-Broschüre ist die Vorschau auf kleinen Bildschirmen stark verkleinert, Safari vergrößert dann die Schrift, die Seiten werden beim Messen zu lang. Alle Druckdokumente (Blätter, Hefte, Broschüre, Blattsammlung, Legeblätter) haben jetzt `html{-webkit-text-size-adjust:100%;text-size-adjust:100%}` in `SHEET_CSS` (die App selbst hatte das schon). In Chrome nicht nachstellbar (auch nicht mit Handy-Nachbildung und altem Zoom-Verhalten); Stefan hat die Testversion danach geprüft („ist jetzt super“). Test: `heft_stringent.py` prüft die Angabe.
- **Arbeitshefte stringenter** (Backlog U, Stefan 27.11.2026: „Deine Vorschläge 1–3 finde ich super.“; Details per Auswahl):
  - **Heft für einen Bereich** (U1): Im Arbeitsheft wählt man oben „Für ein Kind“ (wie bisher, Förderzone) oder „Für einen Bereich“ – ohne Kind und ohne Test. Dort: Fach, Bereich (z. B. Zahlen bis 20, Rechnen, Uhrzeit, Lesen, Schreiben, Vergleichen und Ordnen), Stufen von … bis … und Themenwelt (Grundstufe, Hauptstufe, Berufsschulstufe; bestimmt Bilder, Texte und die Lineatur „passend zur Stufe“). Jede Stufe wird ein Kapitel, alle Kapitel bekommen gleich viele Seiten (mit − und + änderbar). Die Namenszeile auf dem Deckblatt bleibt leer. Sonst wie beim Heft für ein Kind: Umfang 12/24/36/48, Einstieg, Üben, „Das kann ich schon“, Wiederholung, Geschichte, Große Aufgaben, Schwarz-Weiß, Broschüre, Lösungsheft. Hefte entstehen nur noch im Heft-Assistenten. Code: `heftWeg`, `heftKid`, `heftBereiche`, `heftBer`, `heftPlan` (Bereich: gewählte Stufen, gleich gewichtet), `app.sheetWorld` (Themenwelt beim Bauen), Heft-Daten `H.weg`, `H.bfach`, `H.ber`, `H.von`, `H.bis`, `H.welt`.
  - **Blattsammlung statt „Ins Arbeitsheft“** (U2): „Zur Blattsammlung“ sammelt beliebig viele lose Blätter genau wie in der Vorschau (mit Name, Datum, Rahmen und Lochrand), auch für verschiedene Kinder. „Alle drucken“ druckt sie zusammen, hinter jedem Blatt sein Lösungsblatt (Stefans Wahl). Kein Deckblatt, keine Kapitel, keine Broschüre, kein Mischen mit Heften; ↑ ↓ ✕ zum Ordnen. Gemerkt getrennt vom Heft (`stufenweise.sammlung`, `app.samml`, `sammlAdd`, `buildSamml`, `renderSamml`). Ältere Hefte werden beim ersten Öffnen aufgeteilt (Stefans Wahl): Ein Heft aus dem Assistenten bleibt Heft, früher angehängte Blätter wandern in die Blattsammlung; ein Heft ganz ohne Assistent wird ganz zur Blattsammlung (`heftSplitOld`).
  - **Übungsseite austauschen** (U3): In der Seitenliste hat jede Übungsseite „Austauschen“: „Neue Aufgaben“ würfelt die Seite mit demselben Bauplan neu (`it.spec`), „Anderes Blatt wählen“ führt zum Einzelblatt mit der Leiste „Seite n im Heft austauschen“; „An Seite n setzen“ übernimmt genau diese Aufgaben ohne Namenszeile, mit Lösungen fürs Lösungsheft. Kapitel und Seitenzahl bleiben; Legeblätter und Blätter mit mehreren Seiten gehen nicht. Seiten verschieben oder löschen (↑ ↓ ✕) gibt es im Heft nicht mehr, damit Seitenzahl, Inhalt und Broschüre immer stimmen.
  - Tests: neu `heft_stringent.py`; angepasst `arbeitsheft`, `blatt_auswahl`, `lernort_material`, `tausenderbuch_nachspuren`, `hundertertafel_blaetter`, `blatt_layout` (Blattsammlung bzw. Austausch statt „Ins Arbeitsheft“). Anleitung: neue Abschnitte „Blattsammlung“ und „Arbeitsheft“.

## 0.41.0 – 27.11.2026

Freigegeben von Stefan am 27.11.2026 nach Durchsicht der Testversion („Ich hab alles durchgesehen und will freigeben.“). Anleitungsbilder neu aufgenommen.

- **Rückmeldungen zu Arbeitsblättern und Heften** (Backlog S, Stefan 26.11.2026 abends; Entscheidungen von Stefan per Auswahl):
  - **Große Aufgaben passen in die Breite** (S1: „Schriftlich bis 1000“ lief rechts über): Mit großen Aufgaben höchstens 2 Spalten, Hundertertafel- und Basis-Blätter einspaltig. Materialblätter (z. B. leere Hundertertafel) bleiben normal groß, das Lineal bei „Länge messen“ bleibt in echter Größe (1 cm = 1 cm), Stundenpläne passen in die Breite. Das Aufgabenraster wächst nicht mehr über die Seite hinaus; dabei behoben: „Der Größe nach ordnen“ lief auch ohne große Aufgaben 5 mm über.
  - **Heftseite lief über** (S2, „Das kann ich schon: Längere Texte verstehen“, nicht nachstellbar): In Chrome passt jede solche Seite (je 15 Hefte in Grundstufe, HS und BSS, normal und groß geprüft). Seiten mit großen Aufgaben wurden im fertigen Heft bisher nie verkleinert; ein anderer Browser (iPad) mit etwas anderer Schrift ließ sie dann auf ein zweites Blatt laufen. Jetzt dürfen sie im Heft bis 90 % verkleinert werden; beim Bauen bleibt es streng wie bisher.
  - **Schwarz-Weiß: Material hellgrau** (S3, Stefans Wahl „Material hellgrau“): Hunderterplatten, Zehnerstangen und Einer sind hellgrau mit Umriss und Kästchenlinien, „wie in Farbe, nur ohne farbige Füllung“. Plättchen bleiben schwarz bzw. schraffiert.
  - **Schwarz-Weiß: Pfeil deutlich** (S4): Pfeile, Kreuze und Markierungen, die in Farbe rot sind, werden schwarz (vorher Punktmuster).
  - **Kästchen zum Rechnen ab 1000** (S5/S6, Stefans Wahl „Kästchen in jeder Aufgabe“): „Unterschiede bestimmen“ und „Ergänzen“ bis 1000 haben eine Aufgabe je Zeile, links ein Kästchenfeld (5-mm-Karos), rechts die Antwort. Sachaufgaben brechen nur zwischen den Sätzen um (vorher stand „640“ allein am Zeilenende).
  - **Zehnerfeld als eine Reihe mit 10** (S7, Stefans Wahl „Überall“): in Üben und Test, in der Rechenhilfe und auf der Tafel, im Blitzblick, auf Arbeitsblättern und auf dem Legeblatt (jetzt quer, Felder 25 mm für Wendeplättchen). Das Zwanzigerfeld bleibt 2 × 10.
  - **Lochrand** (S8): Einzelne Arbeitsblätter haben links 20 mm Rand (rechts 12 mm), auch Lösungs- und Hilfeseite. Hefte und Legeblätter bleiben, wie sie sind.
  - **Keine Aufgabe doppelt auf einer Seite** (S9, Rückmeldung 23:11: Heft-Einstieg „Ergänzen bis 10“ mit viermal „9 sind schon drin“): Findet sich nach 20 Versuchen keine neue Aufgabe, bleibt die doppelte weg. Gilt für Blätter, Heftseiten und Wiederholungen.
  - Tests: neu `keine_doppelten.py`, `blatt_rueckmeldungen.py`; `blatt_layout.py` prüft jetzt auch die Breite (alle Blätter, groß bis 1000) und den Lochrand. `run_all.sh` wertet auch den Rückgabewert eines Tests aus (z. B. Syntaxfehler); dabei kamen zwei Tests mit veralteten Erwartungen ans Licht (`hundertertafel_blaetter`, `arbeitsblaetter`, Seitenklassen seit 0.40.0), angepasst.

- **Werkzeug: Tests laufen gleichzeitig** (Backlog R, Wunsch Stefan 26.11.2026; betrifft nur `tests/`, keine App-Änderung): `sh tests/run_all.sh` startet bis zu 4 Tests gleichzeitig (`STUFENWEISE_JOBS`), mit gemeinsamem Server und eigenem Ausgabeordner je Test; `sh tests/run_all.sh nur NAME …` für einzelne Tests; `tests/README.md` mit „Gezielt testen“. Gemessen auf 2 Kernen: schnell 3:33 statt 10:30 min, lang 6:37 statt 18:57 min, gleiche Ergebnisse. `mehrere_fenster.py` wartet, bis das andere Fenster den Stand sieht (unter Last sonst unzuverlässig), `frei_stift.py` ohne festen Pfad.

- **Behoben: Heft-Assistent sprang nach oben** (Rückmeldung Stefan, 26.11.2026): „+“ und „−“ bei den Kapiteln (und jede andere Änderung im Dialog „Material drucken“) zeichneten den Dialog neu, die Liste sprang dabei ganz nach oben. Jetzt bleibt die Scrollposition erhalten (`sheetBodySet`); nur beim Öffnen beginnt der Dialog oben. Test `tests/heft_scroll.py` (iPad- und Handygröße).

- **Lineatur wählbar** (Backlog L, Wunsch Stefan 26.11.2026): Blätter mit Schreibzeilen (Wörter abschreiben, kurze und lange Wörter, Merkstellen, Sätze, Meine Wörter, Uhr in Worten, Kalender, Einkaufen) haben die Auswahl „Lineatur“: **Haus** mit drei Stockwerken (Dach, Erdgeschoss, Keller), **zwei Linien** (Mittel- und Grundlinie) oder **eine Linie**. Standard „passend zur Stufe“ nach Themenwelt des Kindes (Stefan): Grundstufe Haus, Hauptstufe und Berufsschulstufe eine Linie. Nach Stefans Durchsicht (26.11. abends, mit Beispielbildern): Das Haus ist ein eigener Kasten mit Rand und zwei Linien innen, ohne Grau, Erdgeschoss etwas höher als Dach und Keller, mit Abstand zur nächsten Zeile – so sieht man auch bei vielen Zeilen untereinander, wo es langgeht. Eine Linie und zwei Linien sind dünner und liegen tiefer (mehr Platz zum Schreiben über der Linie). Die Wahl wird gemerkt (`app.sheet.lin`, `SHEET_KEEP`). Im Heft-Assistenten gibt es eine eigene Auswahl (`H.lin`); sie gilt für alle Blätter im Heft und die Schreiblinien der Fortsetzungsgeschichte. Nicht für die Tafel. Code: `LIN`, `linFor`, `linSelect`, `sheetHasLines`, CSS `.ab-wline.lin-…`, `.hf-lines.lin-…`. Test `tests/lineatur.py`; alle Heftseiten passen auch mit dem Haus (Grundstufe).
- **Deckblatt: Zwanzigerfeld wie in der App gefüllt** (Rückmeldung Stefan, 26.11.2026: „eine ‚unmögliche‘ Füllung nach unseren Regeln“): Das Bild auf dem Deckblatt zeigte 8 Plättchen oben und 3 unten, nach Fünfern gefärbt. Jetzt wird zeilenweise gelegt wie in der App: oben 8 blaue und 2 orange, unten 1 orange (8 + 3). `zfSvg` legt Farbe 1, dann Farbe 2 in Lesereihenfolge.

## 0.40.0 – 26.11.2026

Freigegeben von Stefan am 26.11.2026 nach Durchsicht der Testversion („Perfekt, kannst du freigeben.“).

- **Testversion: neue Stände werden erkannt** (Rückmeldung Stefan, 26.11.2026): Bisher hatte jede Testversion dieselbe Nummer (z. B. 0.40.0), „Nach neuer Version suchen“ fand einen neueren Stand erst, wenn sich die Nebenversion änderte. `tests/testversion.sh` hängt jetzt den Zeitpunkt als vierte Stelle an (z. B. „0.41.0.2611262110“), in `version.json` und in der Anzeige. Die richtige App ist nicht betroffen.

- **Arbeitsblätter im Design der Arbeitshefte** (Backlog M; Stefan hat am 26.11.2026 aus drei Bild-Vorschlägen „Layout A: wie im Heft“ gewählt): Einzelne Arbeitsblätter haben oben eine schmale Kopfzeile mit Fach und Bereich (z. B. „Mathe · Rechnen“), darunter Titel, Name und Datum wie bisher. Die Aufgabenkästen reichen bis zur Fußzeile. Die Fußzeile steht auf fester Höhe, mit Bildungsplan und Lizenz links und dem Fach rechts; keine Seitenzahl, kein Farbrand. Lösungsblatt („Lösungen“) und Hundertertafel zum Nachschauen haben dieselbe Kopf- und Fußzeile, ihr Aufbau bleibt. Legeblätter bleiben, wie sie sind (Stefan). Umsetzung: `sheetFramed()` mit `heftFrame()` (neu: ohne Seitenzahl, Text rechts), `SHEET_FRAME_CSS`; „Blatt füllen“ misst ohne gestreckte Kästen (`sheetFit` mit `ab-measure`). Heftseiten werden weiter ohne Blatt-Rahmen gebaut (`sheetRaw`), auch bei „Ins Arbeitsheft“. Nebenbei: L8/L9-Blätter („Längere Texte“) laufen ohne große Aufgaben nicht mehr über.
- **Schwarz-Weiß für alle Blätter** (Backlog M, Stefan: „Ja, so“): Das Häkchen „Schwarz-Weiß-Drucker (Muster statt Farben)“ gibt es jetzt bei allen Arbeitsblättern und im Heft-Assistenten immer. Blaue Plättchen und Zehnerstangen werden schwarz, orange Plättchen schraffiert, grüne Einer bekommen ein Gitter, rote Hunderter Punkte; alle übrigen Farben (Bilder, Uhren, Geld, Markierungen) werden Grau gleicher Helligkeit (`swHtml`, `SW_MAP`, Muster `sw-or`/`sw-gr`/`sw-rot` in `B_BW_DEFS`). Basis-Blätter behalten ihre eigenen Muster.
- **Keine Linie mehr über der Fußzeile** (Rückmeldung Stefan, 26.11.2026: „unten die Linie überflüssig, so sieht es komisch aus“): Seit die Kästen bis zur Fußzeile reichen, lag die Linie direkt unter den Kästen. Gilt für Heftseiten und Arbeitsblätter.
- Tests: neu `tests/blatt_layout.py` (Aufbau, alle 64 Blätter passen auf ihre Seiten, Schwarz-Weiß ohne bunte Farben, Legeblätter unverändert, Heft mit genau einem Rahmen); angepasst `basis_blaetter.py`, `heft_zone_optionen.py` (Schwarz-Weiß jetzt überall).

## 0.39.0 – 26.11.2026

Freigegeben von Stefan am 26.11.2026 nach Durchsicht der Testversion („Ich hab in Testversion alles überprüft.“).

- **Hinweis im Safari-Tab** (Backlog P1, aus der Prüfung vom 22.11.2026; Stefan 26.11.2026): Im Safari-Tab löscht Safari die Daten einer Website, wenn sie 7 Tage lang nicht geöffnet wurde (gezählt werden Tage mit Safari-Nutzung), zum Beispiel in den Ferien. Für Apps vom Home-Bildschirm gilt das nicht. Läuft Stufenweise auf iPad oder iPhone im Safari-Tab (`safariTab()`: `navigator.standalone === false`, iPadOS auch als „Macintosh“ mit Touch), steht im Lernstand und unter Einstellungen → Daten sichern ein Hinweis mit dem Weg zum Home-Bildschirm und, wenn schon Kinder angelegt sind, dem Umzug (hier „Sicherung speichern“, in der App „Sicherung laden“). Auf dem Startbildschirm („Was machen wir?“) steht eine kurze Fassung, nur wenn Kinder angelegt sind; sie lässt sich für 30 Tage ausblenden (`settings.safariHide`). Nicht in der Home-Bildschirm-App, nicht in anderen Browsern, nicht beim Üben. Test `tests/safari_tab.py`.
- **Raten im Test begrenzt** (Backlog Q1, aus der Prüfung vom 22.11.2026; Stefan 26.11.2026): Sind die ersten beiden Aufgaben einer Stufe Auswahlaufgaben (ein Bild, Wort oder eine Uhrzeit antippen), gilt die Stufe erst bei 3 von 3 als erreicht. Nach 2 von 2 kommt eine dritte Aufgabe, 2 von 3 ist „teilweise“. Betrifft vor allem Lesen L1–L9, Hören P1–P4, Uhr und Größen. Simulation mit einem Kind, das nur rät: Im Lese-Test steht danach in etwa 20 % statt 69 % der Tests mindestens eine Stufe auf „erreicht“ (im Mittel 0,4 statt 2 Stufen), im Mathe-Test Teil 2 in etwa 20 % statt 49 %. Andere Stufen und der Basis-Test (Blöcke a und b) bleiben, wie sie sind. Anleitung ergänzt. Test `tests/raten.py`.
- **Große Aufgaben im Heft-Assistenten** (Backlog N, Wunsch Stefan 26.11.2026): Neues Häkchen „Große Aufgaben (mehr Platz zum Schreiben und Streichen)“, anfangs aus, im Heft gemerkt (`H.gross`). Damit bekommen Übungsseiten, „Das kann ich schon“ und die Wiederholung große Aufgaben, also weniger Aufgaben je Seite; die Seitenzahl bleibt, große Aufgaben werden nie verkleinert. Passt groß nicht einmal eine Aufgabe (z. B. lange Texte), wird nur diese Seite normal groß (Stefan). Das Heft übernimmt keine Einstellungen des letzten Einzelblatts mehr (große Aufgaben, Materialbilder, Zeichnen, Kleinbuchstaben, Rechenart …), sondern nimmt feste Grundeinstellungen (`SHEET_BASE`); die Einstellungen der Einzelblätter bleiben dabei erhalten. Tests `tests/heft_gross.py`, `tests/heft_seiten_gross.py` (alle Stufen mit großen Aufgaben).

## 0.38.1 – 26.11.2026

- **Voller Speicher wird gemeldet** (Backlog O1, aus der Prüfung vom 22.11.2026; Stefan 26.11.2026): Bisher fing `saveData()` einen Fehler beim Schreiben still ab. Die App arbeitete mit dem Stand im Arbeitsspeicher weiter, und nach einem Neustart fehlte alles Neue. Jetzt erscheint oben eine rote Leiste für die Lehrkraft: „Der Speicher ist voll. Neue Ergebnisse werden gerade nicht gespeichert. Bitte jetzt sichern.“ mit Knopf „Jetzt sichern“. Die Sicherung enthält den Stand aus dem Arbeitsspeicher, also auch das noch nicht Gespeicherte. Die Leiste verschwindet, sobald wieder gespeichert wird. Speichert der Browser aus einem anderen Grund nicht, steht dort „Der Browser speichert gerade nicht …“. Einstellungen und Blatt-Einstellungen melden einen Fehler einmal je Sitzung kurz. Anleitung: wie man Platz schafft (gemerktes Arbeitsheft leeren, Kinder löschen, alte Daten löschen). Test `tests/speicher_voll.py`.

## 0.38.0 – 26.11.2026

- **Heft-Assistent** (Backlog J, Schritt 1; Wunsch Stefan, 25.11.2026): Das „Heft zur Förderzone“ wird zum Heft-Assistenten. Wählbar sind Fach (Mathe, Deutsch, Basis oder gemischt), Umfang (12, 24, 36 oder 48 Seiten, 24 vorausgewählt; Deckblatt und Inhalt zählen mit, das gedruckte Heft hat genau so viele Seiten) und wie weit das Heft vorgreift (nur Förderzone, je eine Stufe weiter, bis das Heft voll ist – Standard). Jede Stufe ist ein Kapitel, zuerst die Förderzone mit den meisten Seiten, dann die nächsten noch nicht erreichten Stufen in Lernreihenfolge (`heftRow`). Jede Seite hat neue Aufgaben. Kapitel lassen sich abwählen, kürzer oder länger machen. Deckblatt mit Fach, Inhalt mit Kapiteln und Seitenzahl, unten „Seite n · Kapitel k“ (Seiten wie gedruckt gezählt). Bisher „Blätter je Stufe 1/2“ entfällt. Funktionen `heftPlan`, `heftMake`, `heftPages`, `heftAssistHtml`; Test `tests/heft_assistent.py`.
- **Kapitelaufbau** (Backlog J, Schritt 2): Jedes Kapitel hat eine Einstiegsseite (große Aufgaben, die erste als Beispiel mit Lösung), Übungsseiten und zum Schluss „Das kann ich schon“ (gemischte Aufgaben, Selbsteinschätzung in drei Stufen mit Worten und Zeichen ●/◐/○ zum Ankreuzen). Nach je zwei Kapiteln eine Wiederholung. Hilfen hinten je nach Inhalt: Hundertertafel, Anlauttabelle (neu als Druckseite), Einmaleins-Tafel (neu). Lösungsheft für die Lehrkraft (drucken oder speichern), mit denselben Seitenzahlen.
- **Mathe-Feinstufen** (Schritt 3): Die Übungsseiten eines Kapitels werden schwerer – mit Bild → Bild selbst zeichnen (bzw. Minus selbst wegstreichen) → im Kopf; dazu wählt `app.sheet.stufe` (0…1, nur im Heft) Aufgaben von leicht nach schwer. Basis V1–V3: Ähnlichkeit deutlich → ähnlich → fein.
- **Deutsch-Stoff** (Schritt 4; Texte von Stefan durchgesehen und freigegeben, 26.11.2026: „Die Texte sind gut“): 42 neue Kurztexte (zusammen 79), 39 mittlere Texte (auf den schwereren Seiten von „Texte lesen und verstehen“), 14 neue längere Texte (zusammen 40), drei Fortsetzungsgeschichten mit je 6 Teilen (Praktikum im Supermarkt, Klassenausflug, Trainingswohnung) – im Deutsch-Heft je Teil eine Seite Text und eine Seite Aufgaben, wenn die Förderzone ab L6 bzw. W5 liegt. Neue Papier-Formate: Lesen und malen (L4, L6), Wörter im Text unterstreichen und Sätze ordnen (L7), Lückenwort (W3), Silben zusammensetzen (W4), Satz zum Bild und Satz abschreiben (W6), Anlaut ankreuzen (P4).
- **Broschürendruck** (Schritt 5): „Drucken als“ A4 einseitig, A5-Heft aus A4-Bögen oder A4-Heft aus A3-Bögen; Seiten in Falt-Reihenfolge, leere Seiten bis zur durch 4 teilbaren Zahl, Hinweis zum beidseitigen Druck.
- Behoben: Merkstellen-Blatt (W5) zeigte bei Puppe, Löffel u. ä. keine Lücke (pp, ff, rr fehlten).
- **Heftseiten laufen nicht mehr über** (Rückmeldung Stefan, 26.11.2026: Testheft 54 statt 48 Seiten, in der Broschüre war eine Seite abgeschnitten): Die Einstiegsseite „Kalender und Termine“ war mit großen Aufgaben länger als ein Blatt. Ursache auch: Mit Feinstufe kamen bei Blättern mit höchstens 2 Aufgaben mehr Aufgaben als gewählt. Jetzt: erst weniger Aufgaben, dann normale statt großer Aufgaben, bei der Wiederholung notfalls nur das neuere Kapitel, zuletzt Verkleinern bis 60 % (`fitlow`). Neuer Test `tests/heft_seiten_passen.py` baut alle Seitenarten für alle 77 Stufen mit Blatt.
- **Seiten gleichmäßig gefüllt** (Stefan, 26.11.): Einstieg, „Das kann ich schon“ und Wiederholung werden einmal mit vielen Aufgaben gebaut und dann auf ganze Reihen gekürzt, bis die Seite gerade voll ist (keine einzelne Aufgabe mehr allein in der letzten Reihe). Große Aufgaben beim Einstieg nur, wenn die Seite damit mindestens zu drei Vierteln voll wird. Geschichte: Textseite mit Feld „Male ein Bild zu diesem Teil“, Aufgabenseite mit Schreiblinien bis unten. Seitenzahl im Heft fest unten in der Mitte (vorher je nach Inhalt unterschiedlich hoch), Kapitel weiter in der Fußzeile.
- **Einheitliches Seitenlayout im Heft** (Stefan hat aus drei Vorschlägen „Layout B: Aufgaben strecken“ gewählt, 26.11.2026): Jede Heftseite hat oben eine schmale Kopfzeile („Kapitel 2 · Üben“, „Einstieg“, „Das kann ich schon“, „Wiederholung“, „Geschichte · Teil 1“, „Zum Nachschauen“) und unten eine Fußzeile auf immer gleicher Höhe (Bildungsplan und Lizenz links, Seitenzahl im Kreis in der Mitte, Kapitel rechts). Die Aufgabenkästen wachsen bis zur Fußzeile, statt unten Platz frei zu lassen. Heftseiten werden nicht mehr verkleinert („Das kann ich schon“ und Wiederholung waren auf etwa 85 %); lieber eine Reihe weniger. Gemessen wird beim Zusammenstellen mit Kopf- und Fußzeile (`heftFrame`, `HEFT_RESERVE`). Ältere, im Browser gemerkte Hefte bekommen den neuen Rahmen beim Drucken.
- **Neues Deckblatt** (Stefan hat Entwurf „C4“ gewählt, 26.11.2026): Farbrand links je Fach (Mathe blau, Deutsch rot, Basis grün; gemischtes Heft halb blau, halb rot). Den Titel bildet die App aus den Kapiteln, z. B. „Rechnen bis 20“, „Lesen und Schreiben“ oder „Rechnen, Lesen und Schreiben“. Darunter stehen klein die Kapitel (`heftTitleAuto`); ein selbst eingetragener Titel bleibt. In der Mitte ein Fachbild (Zwanzigerfeld bzw. ab Zahlenraum 100 Hunderter, Zehner und Einer; Buchstabenkarten; Formen), darunter der Inhalt mit Kapitelnummern. Unten steht „Dieses Heft gehört ____“. Bei mehr als 8 Einträgen hat der Inhalt wie bisher eine eigene Seite (ohne Farbrand, Stefan).
- **Rückseite als Nachguckseite** (Wunsch Stefan): Die letzte Seite ist immer eine Nachguckseite passend zum ersten Kapitel: Zwanzigerfeld mit Zahlenstrahl und Zehnerfreunden (bis 20), Hundertertafel (bis 100), Stellenwerttafel mit Zahlenstrahlen (ab 1000), Einmaleins-Tafel, Anlauttabelle (Anfangsunterricht), Merkwörter (ab „Sätze verstehen“ bzw. W5/W6) oder Formen und Farben (Basis). Ist eine Hilfe angekreuzt, wird sie zur Rückseite. Der Farbrand steht rechts, so läuft er in der Broschüre vom Deckblatt über den Falz weiter: Das Heft lässt sich ins Regal stellen, und die Farbe zeigt das Fach. Leere Seiten in der Broschüre kommen vor die Rückseite.
- **Anlauttabelle:** 7 Spalten mit „Pf“ (Pfanne) dazu, damit die letzte Reihe voll ist (Stefan: unterste Zeile war nicht voll).
- Behoben: Ragte eine Aufgabe ein paar Pixel über die Seite (z. B. „Anfangsbuchstaben schreiben“), verkleinerte Chrome das ganze Heft-PDF minimal. Seiten schneiden jetzt seitlich ab (`overflow-x:clip`).
- **Weniger große Lücken:** Beim Füllen eines Blatts durften bisher keine zwei Aufgaben dasselbe Ergebnis haben. Bei „Plus/Minus bis 20 mit Zehnerübergang“ gibt es nur wenige Ergebnisse, die Seite hatte dann oft nur 4–8 Aufgaben. Jetzt kommen, wenn die Ergebnisse ausgehen, weitere verschiedene Aufgaben mit gleichem Ergebnis dazu (z. B. 7 + 5 und 8 + 4). Gilt auch für „Blatt füllen“ bei einzelnen Arbeitsblättern.
- **Stundenplan neu** (Stefan, 26.11.): gemischter Plan statt „1. Stunde immer Deutsch, 2. Stunde immer Mathe“; Klassen und Fächer passend zur Stufe nach Bildungsplan 2022 GENT (Grundstufe: Deutsch, Mathe, Sachunterricht, Musik, Kunst, Sport, Religion; Hauptstufe zusätzlich AES, Technik, WBO, BNT, Geschichte; Klassen 6–9), Sport und AES/Technik/Kunst als Doppelstunden, Fragen zählen richtig.
- **Weitere Unstimmigkeiten behoben:** „Stimmt das?“-Sätze, die als falsch galten, aber stimmen („Mit dem Messer kann man Papier schneiden“, „Mit dem Handy kann man Fotos machen“, „Die Mütze ist nass“, „Die Pizza ist eckig“, „Die Kerze ist hell“); Kerze, Tasse, Glas „stehen unter dem Tisch“; Sachaufgaben mit unrealistischen Preisen (Helm und Schloss bis 390 €, Strom und Internet bis 390 €); drei neue Texte mit Klassen 7–9 nur noch für Haupt-/Berufsschulstufe. Test `tests/plaene_sinnvoll.py`.
- **Menü „Material drucken“** statt „Arbeitsblätter“ (Wunsch Stefan, 26.11.2026), ebenso die Überschrift des Fensters.
- **Fußzeile ohne Namen** (Backlog K, Wunsch Stefan): Arbeitsblätter, Legeblätter, Hilfeseiten, Heft und Lösungsheft tragen unten „Stufenweise · stufenweise.app · CC BY-SA 4.0“ statt „© Stefan Hackl“. Stefan bleibt im Impressum, in der Lizenz und auf GitHub als Urheber genannt.
- Anleitungsbilder neu aufgenommen (neue Fußzeile, Menü „Material drucken“, Zifferntastatur mit 1 2 3 oben). Testhilfe `tests/simlib.py` setzt Ziffern per JS (Felder sind seit 0.35.1 bei offener Zifferntastatur schreibgeschützt).

## 0.37.0 – 25.11.2026

- **Mehr Sätze zum Legen:** 105 statt 37 (kurz 40, mittel 40, lang 25), Alltag aus Schule, Küche, Werkstatt, Einkaufen, Weg und Freizeit; erlaubte Umstellungen im Satz geprüft (`SATZ_ALT`). An der Tafel kommt jeder Satz einer Länge einmal dran, bevor sich einer wiederholt (`tsGen` mit Warteschlange). Schüttelsätze: in der zweiten Hälfte einer Runde auch lange Sätze (Wunsch Stefan, 25.11.2026).
- **Testversion mit eigenem Symbol und Namen** auf dem Home-Bildschirm: rotes Band „TEST“, Name „SW Test“ (`tests/test_icons.py`, von `tests/testversion.sh` aufgerufen; die richtige App bleibt unverändert).

## 0.36.1 – 25.11.2026

- **Sätze legen: Großbuchstabe vorne, Punkt hinten bleiben fest** (Stefan: „als Anfangs- und End-Symbol … und auch nur so gelten“). Richtig sind nur Umstellungen im Satz, z. B. „Mia stellt die Teller und die Tassen in den Schrank.“ oder „Morgen fahren wir früh mit dem Zug in die Stadt.“. Fassungen mit anderem Satzanfang (aus 0.36.0) gelten nicht mehr; verglichen werden die Karten wieder genau so, wie sie sind.

## 0.36.0 – 25.11.2026

- **Frei legen an der Tafel: gelegte Zahl einblenden.** Im Unterricht gibt es jetzt immer den Knopf „Zahl zeigen“ (bisher nur mit der Einstellung „Ergebnisse und Mengen anzeigen erlauben“). Die Zahl erscheint groß und farbig nach Stellen, dazu H/Z/E; beim Geld die Summe. „Verdecken“ blendet sie wieder aus (Wunsch Stefan, 25.11.2026).
- **Sätze legen mit Ziehen** (Satz-Baukasten an der Tafel, Schüttelsätze, Sätze im Lesen und im Test): Wortkarten lassen sich an eine Stelle im Satz ziehen und im Satz verschieben; ein gelegtes Wort antippen oder nach unten ziehen legt es zurück. Ein orangefarbener Strich zeigt beim Ziehen, wo das Wort landet. Antippen der Reihe nach geht wie bisher (Wunsch Stefan, 25.11.2026). Test `tests/satz_ziehen.py`.
- **Stift beim Frei legen an der Tafel:** Knopf „Stift“ schaltet zwischen Legen und Schreiben um; vier Farben, Radierer, „Strich zurück“, „Schrift weg“ (als Symbole). Die Schrift gehört zur Legefläche (Würfel und Geld), bleibt beim Legen stehen und passt sich der Größe an; „Alles weg“ löscht auch die Schrift. Nur im Unterricht (Wunsch Stefan, 25.11.2026). Test `tests/frei_stift.py`.
- **Sätze legen: weitere richtige Wortstellungen.** Alle Sätze des Satz-Baukastens und der Schüttelsätze geprüft; sinnvolle Umstellungen gelten jetzt als richtig, z. B. „Morgen fahren wir früh mit dem Zug in die Stadt.“, „Ich nehme eine Jacke mit, wenn es regnet.“, „Hunger hat Lea.“, „Gelb ist die Banane.“ (`SATZ_ALT`, `sentMatch`). Verglichen wird ohne Groß-/Kleinschreibung und Satzzeichen (die Karten behalten sie als Hilfe); stimmt der Satz, zeigt die Zeile ihn richtig geschrieben. Auch „Tomate und Gurke.“ am Satzende zählt jetzt.


## 0.35.2 – 25.11.2026

- **Zifferntastatur wie am Telefon:** 1 2 3 oben, 7 8 9 unten, darunter ⌫ 0 ✓ (bisher wie am Taschenrechner mit 7 8 9 oben). So kennen es die Kinder von Handy, Tablet und Smartboard (Rückmeldung Stefan). Der Taschenrechner in der Materialkiste bleibt wie ein echter Taschenrechner.

## 0.35.1 – 25.11.2026

Behoben (Rückmeldung aus dem Einsatz an der Tafel):
- **Satz legen:** Vertauschte Teile bei „und“/„oder“ gelten jetzt als richtig, z. B. „Mia stellt die Teller und die Tassen in den Schrank.“ statt „… die Tassen und die Teller …“ (Satz-Baukasten an der Tafel und Schüttelsätze). Bei Aufzählungen ist jede Reihenfolge richtig, solange die Satzzeichen stimmen. Falsche Tausche wie „Ich koche und Tom spült.“ → „Ich Tom und koche spült.“ bleiben falsch (`sentVariants`, `sentOk`).
- **Smartboard: keine Systemtastatur mehr** neben der eigenen Zifferntastatur. Manche Geräte zeigen ihre Tastatur trotz `inputmode="none"`; solange die Zifferntastatur offen ist, sind Ziffernfelder jetzt schreibgeschützt (eine echte Tastatur geht trotzdem). Eingerollt („▾“) kann man wieder mit der Systemtastatur tippen.
- Test `tests/tafel_rueckmeldung.py`.

## 0.35.0 – 25.11.2026

- Schrift Stufenfibel: großes I als einfacher Strich (ohne Querstriche oben und unten), Ziffer 1 ohne Querstrich unten (Stefan, 25.11.2026). `fonts/schlichte_formen.py`, Í/Î/Ï/Ì mit angepasst.

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
