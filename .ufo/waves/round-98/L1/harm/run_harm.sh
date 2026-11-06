#!/usr/bin/env bash
# Round-98 L1 harm battery: tree-reading standing checks at BASE and at REV, each in its own
# `git clone --shared` checkout under scratch (never the lane). Output: <out>/<rev8>/<check>.log with rc.
# Usage: run_harm.sh <rev> <out-dir>
set -u
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
REV=$1; OUT=$2
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r98/L1/harm-$$
mkdir -p "$S" "$OUT"
trap 'rm -rf -- "$S"' EXIT
declare -A CHECKS=(
  [grader]="python3 grader.py"
  [r52c2]="python3 plans/round52_c2_registry.py --lane ."
  [r63depth]="python3 plans/round63_gate_checks.py depth --skill SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root ."
  [r68cap]="python3 plans/round68_capability_table.py --lane ."
  [r72c2]="python3 plans/round72_c2_routed_defects.py --lane ."
  [r73c2]="python3 plans/round73_c2_registry_audit.py --lane ."
  [r74c1]="python3 plans/round74_c1_registry.py --lane ."
  [r74c2]="python3 plans/round74_c2_registry_audit.py --lane ."
  [r75c1]="python3 plans/round75_c1_index_parity.py --lane ."
  [r75c2]="python3 plans/round75_c2_registry_audit.py --lane ."
  [r76c1]="python3 plans/round76_c1_surface_resolver.py --lane ."
  [r77c1]="python3 plans/round77_c1_declared_surfaces.py --lane ."
  [r78c1]="python3 plans/round78_c1_class_member_ledger.py --lane ."
  [r79c1]="python3 plans/round79_c1_population_ledger.py --lane ."
  [r80c1]="python3 plans/round80_c1_located_replay.py --lane ."
  [r80c2]="python3 plans/round80_c2_spotcheck_debt.py --lane ."
  [r81c1]="python3 plans/round81_c1_new_members.py --lane ."
  [r81c2]="python3 plans/round81_c2_spotcheck_debt.py --lane ."
  [r82c1]="python3 plans/round82_c1_plans_registry.py --lane ."
  [r82c2]="python3 plans/round82_c2_closure_debt.py --lane ."
  [r82c3]="python3 plans/round82_c3_sweep.py --lane . --check"
  [anchor]="python3 plans/anchor_digest_check.py --lane ."
  [anchorline]="python3 plans/anchor_line_check.py --lane ."
)
for rev in 49a1c4f1097db7c923da56d4213cad75772ed1c0 "$REV"; do
  D=$S/${rev:0:8}
  git clone -q --shared --no-checkout "$L" "$D"
  git -C "$D" -c advice.detachedHead=false checkout -q "$rev"
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch" >&2; exit 3; }
  mkdir -p "$OUT/${rev:0:8}"
  for k in "${!CHECKS[@]}"; do
    ( cd "$D" && TMPDIR=$S timeout 900 ${CHECKS[$k]} > "$OUT/${rev:0:8}/$k.log" 2>&1; echo "rc=$?" >> "$OUT/${rev:0:8}/$k.log" ) &
  done
  wait
done
for k in $(printf '%s\n' "${!CHECKS[@]}" | sort); do
  b=$(tail -1 "$OUT/49a1c4f1/$k.log"); r=$(tail -1 "$OUT/${REV:0:8}/$k.log")
  nb=$(grep -c '^DEFECT\|FAIL\|MISMATCH' "$OUT/49a1c4f1/$k.log"); nr=$(grep -c '^DEFECT\|FAIL\|MISMATCH' "$OUT/${REV:0:8}/$k.log")
  echo "$k BASE $b findings=$nb | ${REV:0:8} $r findings=$nr"
done | tee "$OUT/summary-${REV:0:8}.txt"
