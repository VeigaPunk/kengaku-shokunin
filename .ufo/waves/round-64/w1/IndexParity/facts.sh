#!/usr/bin/env bash
# Definitive per-lesson facts receipt for R64-C3(b) seat IndexParity.
# Every number below is produced by the command shown next to it. Read-only.
set -u
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
cd "$LANE" || exit 2
for n in 57 58 59 60 61 62; do
  f="corpus/lessons/round-$n.md"
  echo "######## $f"
  echo "\$ sha256sum $f"
  sha256sum "$f"
  echo "\$ sed -n '1p' $f"
  sed -n '1p' "$f"
  echo "\$ grep -c '^| S[0-9]' $f   # gate table source rows"
  grep -c '^| S[0-9]' "$f"
  echo "\$ awk '/^## Mistakes/{f=1;next} /^## /{f=0} f&&/^| /' $f | grep -vc '^| *class '   # rows under '## Mistakes'"
  awk '/^## Mistakes/{f=1;next} /^## /{f=0} f&&/^| /' "$f" | grep -vc '^| *class '
  echo "\$ awk '/^## Mistakes/{f=1;next} /^## /{f=0} f&&/^| /' $f | grep -v '^| *class ' | grep -c '^| '   # same, counted the other way"
  awk '/^## Mistakes/{f=1;next} /^## /{f=0} f&&/^| /' "$f" | grep -v '^| *class ' | grep -c '^| '
  echo "\$ grep -c '^| ' $f   # ALL table data lines in the lesson (header rows excluded by grep)"
  grep -c '^| ' "$f"
  echo "\$ grep -n 'admit A\|All four admit\|no rejections this round\|Rejections this round\|REJECT-equivalent' $f"
  grep -n "admit A\|All four admit\|no rejections this round\|Rejections this round\|REJECT-equivalent" "$f" | cut -c1-200
  echo "\$ grep -n 'Round verdict' SCORECARD.md (nearest above this round) + '## Round $n' heading"
  grep -n "^## Round $n " SCORECARD.md | cut -c1-160
  echo
done
