#!/usr/bin/env bash
# Round-35 C2 cheapest skip-control: mark every ledger row `closed` without repairing anything.
# Scored by the frozen checker in (a) the live lane read-only via a temp ledger copy is NOT possible
# (the checker reads corpus/defects.jsonl in place), so it runs in a throwaway shared clone holding
# the frozen tree; the lane checkout is never written.
set -euo pipefail
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
D=$(mktemp -d /tmp/k35-c2ctl.XXXX)
git clone -q --no-checkout --shared "$L" "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone '/corpus/' '/plans/' '/SCORECARD.md' \
  '/.ufo/waves/round-34/assimilation/' '/.ufo/waves/round-34/build/*.md'
git -C "$D/lane" checkout -q master
[ "$(git -C "$D/lane" rev-parse --show-toplevel)" = "$D/lane" ] || { echo "fixture toplevel mismatch"; exit 3; }
C="$D/lane"
cp "$L/plans/defect_ledger.py" "$C/plans/"
sed 's/"status": "open", "closed_round": null/"status": "closed", "closed_round": 35/' "$L/corpus/defects.jsonl" > "$C/corpus/defects.jsonl"
set +e
python3 "$C/plans/defect_ledger.py" --lane "$C"
echo "exit=$?"
rm -rf "$D"
