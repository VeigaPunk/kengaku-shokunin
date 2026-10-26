#!/bin/bash
# R42RevMutRows: re-run the frozen witness run inside the mandated Q32 envelope, in my clone.
set -u
S=/fast/scratch/hyaku/kengaku-r42/R42RevMutRows
LANE="$S/lane"
cd "$LANE" || exit 9
git -C "$LANE" rev-parse --show-toplevel >/dev/null || { echo "not a toplevel"; exit 9; }
ENVLINE='bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 plans/round42_c1_verify.py --lane . --battery-dir .ufo/waves/round-42/claims/witness --work '"$S"'/w'
echo "ENVELOPE $ENVLINE"
echo "ENVELOPE start $(date +%T) cwd=$LANE"
B4=$(ls -A /home/vgpnk/.local/bin | sha256sum | cut -d' ' -f1)
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 plans/round42_c1_verify.py --lane . --battery-dir .ufo/waves/round-42/claims/witness --work "$S/w" > "$S/rerun.txt" 2> "$S/rerun.err"
RC=$?
A4=$(ls -A /home/vgpnk/.local/bin | sha256sum | cut -d' ' -f1)
echo "ENVELOPE end $(date +%T) exit=$RC local_bin_before=$B4 after=$A4"
if [ "$B4" != "$A4" ]; then echo "LOCAL-BIN CHANGED"; fi
echo "--- stderr ---"
cat "$S/rerun.err"
echo "--- byte diff vs frozen witness-run.txt, ENVELOPE lines aside ---"
grep -v '^ENVELOPE' "$LANE/.ufo/waves/round-42/claims/witness-run.txt" > "$S/frozen.noenv"
grep -v '^ENVELOPE' "$S/rerun.txt" > "$S/rerun.noenv"
if diff -u "$S/frozen.noenv" "$S/rerun.noenv" > "$S/rerun.diff"; then
  echo "BYTE-IDENTICAL (ENVELOPE lines aside); diff empty"
else
  echo "DIFFERS:"; cat "$S/rerun.diff"
fi
echo "--- ENVELOPE lines: frozen vs mine ---"
grep '^ENVELOPE' "$LANE/.ufo/waves/round-42/claims/witness-run.txt"
grep '^ENVELOPE' "$S/rerun.txt"
