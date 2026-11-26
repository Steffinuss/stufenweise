#!/bin/sh
# Führt die Tests aus, mehrere gleichzeitig, mit einem gemeinsamen Webserver für die App.
# Aufruf aus dem Repository-Ordner:
#   sh tests/run_all.sh              schnelle Tests
#   sh tests/run_all.sh lang         dazu alle Arbeitsblätter, simulierte Kinder, Zufallsklicks
#   sh tests/run_all.sh nur NAME …   nur diese Tests (z. B. „nur blatt_layout heft_gross“; Liste: tests/README.md)
# Einstellbar:
#   STUFENWEISE_JOBS=n   so viele Tests gleichzeitig (Standard 4; STUFENWEISE_JOBS=1 = nacheinander wie früher)
#   STUFENWEISE_PORT     Port des Testservers (Standard 8766)
# Jeder Test schreibt seine Bilder und PDFs in einen eigenen Ordner tests/out/lauf/<Test>/, seine Ausgabe nach
# tests/out/lauf/<Test>.log. Am Ende steht je Test „ok“ oder „FEHLER“ (mit den letzten Zeilen der Ausgabe).
cd "$(dirname "$0")/.." || exit 1
SELF="$PWD/tests/$(basename "$0")"
PORT=${STUFENWEISE_PORT:-8766}
export STUFENWEISE_URL=${STUFENWEISE_URL:-http://localhost:$PORT/index.html}
LAUF=tests/out/lauf
TO=""; command -v timeout >/dev/null 2>&1 && TO="timeout 900"   # macOS hat „timeout“ nicht immer

# ---- ein einzelner Test (intern, von xargs aufgerufen) ----
if [ "$1" = "__eins" ]; then
  t=$2; name=$(echo "$t" | tr ':' '_'); file=${t%%:*}; args=""; [ "$file" != "$t" ] && args=$(echo "${t#*:}" | tr 'x' ' ')
  mkdir -p "$LAUF/$name"; a=$(date +%s)
  STUFENWEISE_OUT="$PWD/$LAUF/$name" $TO python3 "tests/$file.py" $args > "$LAUF/$name.log" 2>&1; rc=$?
  b=$(date +%s)
  if [ $rc -eq 124 ]; then echo "Zeitlimit überschritten" >> "$LAUF/$name.log"; st=FEHLER
  elif [ $rc -ne 0 ] || grep -q "Traceback\|Error:\|ERR \[.\+\]" "$LAUF/$name.log"; then st=FEHLER; else st=ok; fi   # Rückgabewert ≠ 0: z. B. Syntaxfehler (ohne „Traceback“)
  echo "$st $((b-a))" > "$LAUF/$name.st"
  printf '%-7s %-26s %4s s\n' "$st" "$name" "$((b-a))"
  exit 0
fi

# ---- Testlisten ----
FAST="fehler smoke einstellungen runden gefuehrt hinweis_neu springen antwortfeld feld_ueben ueberspringen update_hinweis wochenuebersicht lernort_material legeblaetter tausenderbuch_nachspuren arbeitsheft doppelte_zeilen grosse_aufgaben arbeitsblatt_optionen zehnerpartner_ueben durchsicht_0_21 oberflaeche_details test_fortschritt test_nie_haengen test_passt handy drittes_fach basis_grundlagen basis_blaetter basis_ueben basis_test zwanzigerfeld_zahl plusminus_ueben blatt_auswahl mehrere_fenster materialkiste qr_umzug druck_seiten hundertertafel_blaetter heft_zone_optionen konzentrationsmodus deutsch_optimierung mathe_material tafel_rueckmeldung satz_ziehen frei_stift heft_assistent plaene_sinnvoll speicher_voll raten safari_tab heft_gross blatt_layout lineatur heft_scroll zwanzigerfeld:1180x820 zwanzigerfeld:390x844 keine_doppelten blatt_rueckmeldungen"
SLOW="sweep zufallsklicks kinder_sim arbeitsblaetter heft_seiten_passen heft_seiten_gross"
# Lange Tests zuerst starten, dann laufen die kurzen nebenher und die Runde endet früher
LANGE="heft_seiten_passen heft_seiten_gross kinder_sim arbeitsblaetter sweep zufallsklicks heft_assistent test_nie_haengen blatt_layout basis_ueben druck_seiten"
case "$1" in
  lang) LIST="$FAST $SLOW" ;;
  nur) shift; LIST="$*"; [ -z "$LIST" ] && { echo "Bitte Testnamen angeben, z. B.: sh tests/run_all.sh nur blatt_layout"; exit 2; } ;;
  "") LIST="$FAST" ;;
  *) echo "Unbekannt: $1 (erlaubt: lang, nur NAME …)"; exit 2 ;;
esac
for t in $LIST; do [ -f "tests/${t%%:*}.py" ] || { echo "Test gibt es nicht: $t"; exit 2; }; done
ORDER=""; for t in $LANGE; do case " $LIST " in *" $t "*) ORDER="$ORDER $t" ;; esac; done
for t in $LIST; do case " $LANGE " in *" $t "*) ;; *) ORDER="$ORDER $t" ;; esac; done

CORES=$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)
JOBS=${STUFENWEISE_JOBS:-4}   # gemessen 26.11.2026 auf 2 Kernen: 4 gleichzeitig am schnellsten (viele Tests warten auf den Browser)

# ---- gemeinsamer Testserver: muss laufen, bevor der erste Test startet ----
if ! curl -s -o /dev/null "http://localhost:$PORT/version.json"; then
  python3 -m http.server "$PORT" --bind 127.0.0.1 --directory . >/dev/null 2>&1 &
  SERVER=$!
  for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do curl -s -o /dev/null "http://localhost:$PORT/version.json" && break; sleep 0.5; done
  curl -s -o /dev/null "http://localhost:$PORT/version.json" || { echo "Testserver auf Port $PORT startet nicht."; kill "$SERVER" 2>/dev/null; exit 2; }
fi

rm -rf "$LAUF"; mkdir -p "$LAUF"
N=$(echo $ORDER | wc -w | tr -d ' ')
echo "$N Tests, $JOBS gleichzeitig ($CORES Kerne) …"
T0=$(date +%s)
echo $ORDER | tr ' ' '\n' | grep -v '^$' | xargs -P "$JOBS" -I{} sh "$SELF" __eins {}
T1=$(date +%s)
[ -n "$SERVER" ] && kill "$SERVER"

# ---- Ergebnis in der gewohnten Reihenfolge ----
echo; echo "Ergebnis:"
FAIL=0; OK=0
for t in $LIST; do name=$(echo "$t" | tr ':' '_')
  if [ -f "$LAUF/$name.st" ]; then read st sec < "$LAUF/$name.st"; else st=FEHLER; sec=0; echo "(kein Ergebnis)" >> "$LAUF/$name.log"; fi
  if [ "$st" = ok ]; then OK=$((OK+1)); echo "ok      $name"; else FAIL=$((FAIL+1)); echo "FEHLER  $name"; tail -5 "$LAUF/$name.log" | sed 's/^/    /'; fi
done
S=$((T1-T0)); printf '\n%s ok, %s FEHLER, Dauer %d:%02d min (Ausgaben: %s)\n' "$OK" "$FAIL" $((S/60)) $((S%60)) "$LAUF/"
[ $FAIL -eq 0 ]
