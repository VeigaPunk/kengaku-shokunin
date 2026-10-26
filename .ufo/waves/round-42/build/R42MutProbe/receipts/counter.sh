#!/usr/bin/env bash
# usage: counter.sh <out-file>  — runs the frozen C2 counter on the scratch clone inside the Q32 envelope
set -u
S=/fast/scratch/hyaku/kengaku-r42/R42MutProbe
OUT=$1
"$S/envrun.sh" /usr/bin/bash -c "cd $S/lane && export TMPDIR=$S/w && exec /usr/bin/python3 plans/round42_c2_verify.py --lane . --work $S/w" > "$OUT" 2>&1
rc=$?
echo "== counter exit=$rc out=$OUT"
cat "$OUT"
