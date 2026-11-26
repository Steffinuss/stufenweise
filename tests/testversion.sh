#!/bin/sh
# Überträgt den Stand des Zweigs „entwicklung“ in das Schaufenster-Repository stufenweise-test.
# Aufruf: sh tests/testversion.sh /pfad/zur/kopie/von/stufenweise-test
# Dort wird nie direkt gearbeitet: Jeder Aufruf ersetzt alle Dateien durch den Stand von „entwicklung“
# und macht daraus einen neuen Commit (die Geschichte bleibt im Haupt-Repository).
set -e
ZIEL="$1"; QUELLE="$(cd "$(dirname "$0")/.." && pwd)"
[ -d "$ZIEL/.git" ] || { echo "Keine Git-Kopie: $ZIEL"; exit 1; }
STAND=$(git -C "$QUELLE" rev-parse --short entwicklung)
find "$ZIEL" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
git -C "$QUELLE" archive entwicklung | tar -x -C "$ZIEL"
# Eigene Adresse der Testversion (die richtige App hat stufenweise.app)
printf 'test.stufenweise.app\n' > "$ZIEL/CNAME"
# Automatische Releases nur im Haupt-Repository
rm -rf "$ZIEL/.github"
# Eigenes Symbol und eigener Name auf dem Home-Bildschirm (rotes Band „TEST“, Name „SW Test“)
python3 "$QUELLE/tests/test_icons.py" "$ZIEL"
sed -i 's/"name": "Stufenweise"/"name": "Stufenweise – Testversion"/; s/"short_name": "Stufenweise"/"short_name": "SW Test"/' "$ZIEL/manifest.webmanifest"
sed -i 's#<title>Stufenweise</title>#<title>Stufenweise – Testversion</title>#; s#<meta name="apple-mobile-web-app-title" content="Stufenweise">#<meta name="apple-mobile-web-app-title" content="SW Test">#' "$ZIEL/index.html"
{ printf '> **Testversion von Stufenweise** – Stand aus [Steffinuss/stufenweise](https://github.com/Steffinuss/stufenweise), Zweig `entwicklung` (%s). Nicht für den Unterricht. Hier nicht direkt arbeiten.\n\n' "$STAND"; cat "$ZIEL/README.md"; } > "$ZIEL/README.tmp" && mv "$ZIEL/README.tmp" "$ZIEL/README.md"
# Eigene Kennung, damit man die Testversion von der richtigen App unterscheidet: nächste Nebenversion + Stand
CUR=$(grep -o "APP_VERSION = '[0-9.]*" "$ZIEL/index.html" | grep -o "[0-9.]*$")
# Vierte Stelle = Zeitpunkt (JJMMTTHHMM): Sonst hätte jede Testversion dieselbe Nummer (z. B. 0.40.0), und „Nach neuer Version suchen“
# fände eine neuere Testversion erst, wenn sich die Nebenversion ändert (Rückmeldung Stefan, 26.11.2026).
NEXT=$(echo "$CUR" | awk -F. '{print $1"."$2+1".0"}').$(TZ=Europe/Berlin date +%y%m%d%H%M); HEUTE=$(TZ=Europe/Berlin date +%d.%m.%Y)
sed -i "s/APP_VERSION = '[^']*'/APP_VERSION = '$NEXT · Testversion $STAND · $HEUTE'/" "$ZIEL/index.html"
printf '{"version": "%s", "date": "%s"}\n' "$NEXT" "$HEUTE" > "$ZIEL/version.json"
git -C "$ZIEL" add -A
git -C "$ZIEL" diff --cached --quiet && { echo "Keine Änderung."; exit 0; }
echo "Bereit zum Commit: Testversion aus entwicklung ($STAND)"
