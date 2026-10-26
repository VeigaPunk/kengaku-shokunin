#!/usr/bin/env bash
# Round-37 landing measurement: a clean clone of the lane branch tip (committed bytes only), then every frozen
# counter and the no-harm set. Usage: measure.sh [OUT]  (default: print)
set -u
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r37/L1/measure
rm -rf "$S"; mkdir -p "$S"; export TMPDIR="$S"
trap 'rm -rf -- "$S"' EXIT
TIP=$(git -C "$L" rev-parse refs/heads/master)
git clone -q --no-local "$L" "$S/lane" && git -C "$S/lane" checkout -q "$TIP"
[ "$(git -C "$S/lane" rev-parse --show-toplevel)" = "$S/lane" ] || { echo "bad clone"; exit 2; }
cd "$S/lane"
echo "TIP $TIP"
echo "untracked_in_clone=$(git status --porcelain --untracked-files=all | wc -l)"
r() { echo "\$ $*"; "$@"; echo "exit=$?"; }
r python3 plans/round37_c1_verify.py --lane .
r python3 plans/round37_c2_verify.py --lane .
r python3 plans/anchor_digest_check.py --lane .
r python3 plans/round36_c1_verify.py --lane .
r python3 plans/round36_c2_verify.py --lane .
r /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md
