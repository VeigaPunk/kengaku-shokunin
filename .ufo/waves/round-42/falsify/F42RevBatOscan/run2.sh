#!/bin/bash
# F42RevBatOscan: corrected run — --lane points at the clone so PINS hash the clone's tool files
set -u
S=/fast/scratch/hyaku/kengaku-r42/F42RevBatOscan
export TMPDIR="$S"
echo "toplevel: $(git -C "$S/lane" rev-parse --show-toplevel)"
echo "head: $(git -C "$S/lane" rev-parse HEAD)"
echo "== Q32 pre =="
date +%T
ls -A /home/vgpnk/.local/bin | sha256sum
echo "== counter run (bwrap envelope) =="
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
  python3 "$S/lane/plans/round42_c1_verify.py" --lane "$S/lane" --battery-dir "$S/bat" --only XO5,XO6,XO7 --work "$S/work"
echo "RC=$?"
echo "== Q32 post =="
date +%T
ls -A /home/vgpnk/.local/bin | sha256sum
