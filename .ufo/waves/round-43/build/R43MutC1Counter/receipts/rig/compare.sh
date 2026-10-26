#!/usr/bin/env bash
# R43MutC1Counter: diff one mutant's control outputs against the pristine baseline.
# ENVELOPE lines (timestamps) are stripped for the comparison but stay in the receipt files.
# usage: compare.sh <mutant-outdir>
set -u
B=/fast/scratch/hyaku/kengaku-r43/R43MutC1Counter/out-base
M=$1
for f in "$B"/*.txt; do
  n=$(basename "$f")
  norm() { grep -v '^ENVELOPE' "$1" | sed -E 's/k43-c1-[A-Za-z0-9_]{8}/k43-c1-X/g'; }
  if ! diff -q <(norm "$f") <(norm "$M/$n") >/dev/null 2>&1; then
    echo "== DIFFERS: $n"
    diff <(norm "$f") <(norm "$M/$n")
  else
    echo "== same: $n"
  fi
done
