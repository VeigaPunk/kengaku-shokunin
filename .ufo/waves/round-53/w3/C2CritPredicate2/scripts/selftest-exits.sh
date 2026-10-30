#!/usr/bin/env bash
# Do the 12 genuinely-red rows have a --selftest form that exits 0?
cd /fast/scratch/hyaku/kengaku-r53/C2CritPredicate2/lane
for s in round51_surfaces state_assertion_check round28_census round35_c1_coverage \
         round38_c1_mutants round40_c1_mutants round46_c3 round52_c1 \
         anchor_digest_check gate_flip_check mutant_direction_check adoption_check; do
  f="plans/${s}.py"
  [ -f "$f" ] || { echo "$s: MISSING $f"; continue; }
  out=$(timeout 300 python3 "$f" --selftest 2>&1); rc=$?
  printf '%-28s --selftest rc=%s   %s\n' "$s" "$rc" "$(printf '%s' "$out" | tail -1 | cut -c1-70)"
done
