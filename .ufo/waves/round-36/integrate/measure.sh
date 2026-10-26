#!/bin/bash
# Round-36 landing measurement: both counters on a CLEAN sparse clone of the lane's master tip.
# Usage: measure.sh <lane> <out-file>
set -u
L=$1; O=$2
D=$(mktemp -d /tmp/k36-meas-XXXX)
git clone -q --no-checkout --shared "$L" "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone /corpus /plans /SCORECARD.md /.ufo/waves/round-34/assimilation /.ufo/waves/round-34/build
git -C "$D/lane" checkout -q master
[ "$(git -C "$D/lane" rev-parse --show-toplevel)" = "$D/lane" ] || { echo "bad fixture root"; exit 9; }
{
echo "# measured at master=$(git -C "$D/lane" rev-parse master) in a clean sparse clone"
echo "untracked_in_clone=$(git -C "$D/lane" ls-files --others --exclude-standard | wc -l)"
cd "$D/lane"
echo "## C1"; python3 plans/round36_c1_verify.py --lane . ; echo "exit=$?"
echo "## C2"; python3 plans/round36_c2_verify.py --lane . ; echo "exit=$?"
} > "$O" 2>&1
rm -rf "$D"
