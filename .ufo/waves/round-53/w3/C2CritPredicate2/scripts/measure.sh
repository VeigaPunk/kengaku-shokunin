#!/usr/bin/env bash
cd /fast/scratch/hyaku/kengaku-r53/C2CritPredicate2/lane
for c in "python3 plans/stage_scan.py" "python3 plans/sources_adopt.py" "python3 plans/scratch_guard.py check" "python3 plans/scratch_guard.py" "python3 plans/round51_surfaces.py --help"; do
  out=$(timeout 300 bash -c "$c" 2>&1); rc=$?
  echo "=== [$c] rc=$rc ==="
  printf '%s\n' "$out" | tail -3
done
