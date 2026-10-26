#!/bin/bash
# $1=label $2=command  (cwd = clone root, TMPDIR = scratch)
S=/fast/scratch/hyaku/kengaku-r37/F37NoHarmSweep
D="$S/fx/lane"
export TMPDIR="$S/tmp/$1"; mkdir -p "$TMPDIR"
out="$S/out/$1"
cd "$D" || exit 99
t0=$(date +%s.%N)
bash -c "$2" >"$out.log" 2>&1
rc=$?
t1=$(date +%s.%N)
secs=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.1f", b-a}')
last=$(awk 'NF{l=$0} END{print l}' "$out.log" | cut -c1-200)
printf '%s\t%s\t%s\t%s\n' "$1" "$rc" "$secs" "$last" > "$out.meta"
