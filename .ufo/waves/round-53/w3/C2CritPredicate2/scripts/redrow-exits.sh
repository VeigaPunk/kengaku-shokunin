#!/usr/bin/env bash
# For each genuinely-RED registry row: does the script have a --help / --selftest form
# that exits 0?  Those are the argv substitutions that could launder a red row to green.
cd /fast/scratch/hyaku/kengaku-r53/C2CritPredicate2/lane
for s in round51_surfaces gate_flip_check adoption_check anchor_digest_check \
         mutant_direction_check round28_census; do
  f="plans/${s}.py"; [ -f "$f" ] || continue
  for form in "--help" "--selftest"; do
    out=$(timeout 120 python3 "$f" $form 2>&1); rc=$?
    printf '%-26s %-11s rc=%s\n' "$s" "$form" "$rc"
  done
done
echo "=== other red-row scripts (find by ledger argv) ==="
python3 - <<'EOF'
import json, os
d = json.load(open('plans/round53-tipstate.json'))['rows']
for n, e in d.items():
    if e.get('state') == 'red':
        a = e.get('argv') or []
        script = a[1] if len(a) > 1 and a[0] == 'python3' else None
        print(f"{n:28s} {script}")
EOF
