#!/usr/bin/env bash
# R43RevSiteStable: site-stability matrix for the round-43 C1 counter on the frozen witness battery.
# Remaining 17 runs (pilot j16_s0_wa already recorded).
set -u
S=/fast/scratch/hyaku/kengaku-r43/R43RevSiteStable
ENVSH=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims/envelope.sh
COUNTER=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round43_c1_verify.py
WITNESS=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-43/claims/witness
mkdir -p "$S/logs" "$S/env" "$S/wa" "$S/wb"
: > "$S/logs/rc.txt"
for jobs in 1 8 16; do
  for seed in 0 1 42; do
    for root in wa wb; do
      tag="j${jobs}_s${seed}_${root}"
      [ -f "$S/logs/${tag}.log" ] && { echo "skip $tag"; continue; }
      TMPDIR="$S" "$ENVSH" "$S/env" env PYTHONHASHSEED="$seed" TMPDIR="$S" python3 "$COUNTER" \
        --lane "$S/lane" --battery-dir "$WITNESS" --work "$S/$root/$tag" --jobs "$jobs" \
        > "$S/logs/${tag}.log" 2>&1
      rc=$?
      echo "$tag rc=$rc" >> "$S/logs/rc.txt"
      echo "done $tag rc=$rc"
    done
  done
done
echo ALL-DONE
