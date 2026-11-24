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
# Die eigene Adresse (CNAME, stufenweise.app) gehört nur zur richtigen App, nie zur Testversion
rm -f "$ZIEL/CNAME"
{ printf '> **Testversion von Stufenweise** – Stand aus [Steffinuss/stufenweise](https://github.com/Steffinuss/stufenweise), Zweig `entwicklung` (%s). Nicht für den Unterricht. Hier nicht direkt arbeiten.\n\n' "$STAND"; cat "$ZIEL/README.md"; } > "$ZIEL/README.tmp" && mv "$ZIEL/README.tmp" "$ZIEL/README.md"
# Eigene Kennung, damit man die Testversion von der richtigen App unterscheidet: nächste Nebenversion + Stand
CUR=$(grep -o "APP_VERSION = '[0-9.]*" "$ZIEL/index.html" | grep -o "[0-9.]*$")
NEXT=$(echo "$CUR" | awk -F. '{print $1"."$2+1".0"}'); HEUTE=$(TZ=Europe/Berlin date +%d.%m.%Y)
sed -i "s/APP_VERSION = '[^']*'/APP_VERSION = '$NEXT · Testversion $STAND · $HEUTE'/" "$ZIEL/index.html"
printf '{"version": "%s", "date": "%s"}\n' "$NEXT" "$HEUTE" > "$ZIEL/version.json"
git -C "$ZIEL" add -A
git -C "$ZIEL" diff --cached --quiet && { echo "Keine Änderung."; exit 0; }
echo "Bereit zum Commit: Testversion aus entwicklung ($STAND)"
