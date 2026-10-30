#!/usr/bin/env bash
# baseline: run the counter on the real lane (clean clone) with the committed ledger
set -u
S=/fast/scratch/hyaku/kengaku-r53/C2CritPredicate2
export TMPDIR="$S/tmp"; mkdir -p "$TMPDIR"
cd "$S/lane"
start=$(date +%s)
python3 plans/round53_c2_tipstate.py --lane . --source "$S/source" --work "$S/work" --jobs 4 --timeout 900 \
  > "$S/out/baseline.txt" 2>&1
rc=$?
echo "rc=$rc elapsed=$(( $(date +%s) - start ))s" >> "$S/out/baseline.txt"
tail -40 "$S/out/baseline.txt"
