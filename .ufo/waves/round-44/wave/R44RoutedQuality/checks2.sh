C18='for pair in "carried_direction_diff:carried_vs_rederived" "sources_appendonly:sources_appendonly"; do p=${pair%%:*}; d=${pair##*:}; { test -f "plans/$p.py" && grep -qF "python3 plans/$p.py" corpus/QUALITY.md; } || grep -qF "python3 .ufo/waves/round-42/build/R42QualityDraft/$d.py ." corpus/QUALITY.md || exit 1; done; exit 0'
C19='for pair in "carried_direction_diff:carried_vs_rederived" "sources_appendonly:sources_appendonly"; do p=${pair%%:*}; d=${pair##*:}; if test -f "plans/$p.py" && grep -qF "python3 plans/$p.py" corpus/QUALITY.md; then python3 "plans/$p.py" --lane . 2>&1 | grep -qE "^(CARRIED-DIRECTIONS total=|SOURCES-COMMITS scanned=)" || exit 1; else grep -qF "python3 .ufo/waves/round-42/build/R42QualityDraft/$d.py ." corpus/QUALITY.md || exit 1; fi; done; exit 0'
C20='sed -n "/(b) restore the carried cells/,/(c) unpatched/p" corpus/QUALITY.md | grep -qF "development mode prints"'
C23='tr -s " \n" " " < corpus/QUALITY.md | grep -qF "No lane tool read it from committed history at this criterion'"'"'s creation"'
C31='sed -n "/Envelope note: under the v1/,/^$/p" SCORECARD.md | grep -qF "counter that drives the gate"'
C32='grep -qF "measure-final.txt:938" corpus/lessons/round-42.md'
for tree in pristine lane; do
  echo "== tree=$tree =="
  for n in 18 19 20 23 31 32; do v=C$n; cmd=${!v}; ( cd "$tree" && bash -c "$cmd" >/dev/null 2>&1 ); echo "  R42-R3-$n rc=$?"; done
done
