#!/usr/bin/env bash
# Cross-check receipt for R64-C3(b) seat IndexParity: gate admits / mistakes rows / verdict
# for corpus/lessons/round-{57..62}.md. Run from the lane root.
set -u
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
cd "$LANE" || exit 2
for n in 57 58 59 60 61 62; do
  f="corpus/lessons/round-$n.md"
  echo "===== $f  sha256=$(sha256sum "$f" | cut -d' ' -f1)"
  echo "-- header --"
  sed -n '1p' "$f"
  echo "-- gate S-rows admitted (table form) --"
  printf '  grep -c "^| S[0-9]" %s -> ' "$f"; grep -c "^| S[0-9]" "$f"
  echo "-- gate admits/rejects sentences --"
  grep -n "admit A\|All four admit\|no rejections\|Rejections this round\|Tier A\|supersed" "$f" | cut -c1-190 | sed 's/^/  /'
  echo "-- mistakes-section data rows (awk) --"
  awk '/^## Mistakes/{f=1;next} /^## /{f=0} f && /^\| /' "$f" | grep -v '^| *class ' | grep -v '^| *---' | wc -l | sed 's/^/  mistakes_rows_in_Mistakes_sections=/'
  echo "-- all lesson table data rows (4-cell, class-first) --"
  grep -c "^| " "$f" | sed 's/^/  all_pipe_rows=/'
  echo "-- verdict line (SCORECARD round verdict) --"
  grep -n "Round verdict" SCORECARD.md | sed -n "1,20p" >/dev/null
  awk -v n="$n" 'BEGIN{found=0} /^\*\*Round verdict/{print "  " NR ": " substr($0,1,400); found=1} ' SCORECARD.md | head -0
  echo
done
