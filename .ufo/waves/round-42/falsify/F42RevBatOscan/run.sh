#!/bin/bash
# F42RevBatOscan: honesty run of round42_c1_verify.py restricted to o_scan.py / XO5,XO6,XO7
set -u
S=/fast/scratch/hyaku/kengaku-r42/F42RevBatOscan
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
export TMPDIR="$S"

echo "== clone =="
git clone -q --no-local "$LANE" "$S/lane" || exit 1
git -C "$S/lane" checkout -q 508434ad55c709337065611691c426f05875492d || exit 1
echo "toplevel: $(git -C "$S/lane" rev-parse --show-toplevel)"
echo "head: $(git -C "$S/lane" rev-parse HEAD)"
echo "== landing..docs diff restricted to plans/ =="
git -C "$S/lane" diff --stat ff14d76d32d662f7b7073a2acb049594cb740d84 508434ad55c709337065611691c426f05875492d -- plans/
echo "(empty above = counter+battery identical to landing)"

mkdir -p "$S/bat"
cp "$S/lane/plans/battery42/o_scan.py" "$S/bat/o_scan.py" || exit 1
echo "== battery dir contents (must hold only o_scan.py) =="
ls -A "$S/bat"
cmp "$S/bat/o_scan.py" "$S/lane/plans/battery42/o_scan.py" && echo "CLONE-COPY-OK"
cmp "$S/bat/o_scan.py" "$LANE/plans/battery42/o_scan.py" && echo "WORKTREE-EQUAL"
sha256sum "$S/bat/o_scan.py"

echo "== Q32 pre =="
date +%T
ls -A /home/vgpnk/.local/bin | sha256sum

echo "== counter run (bwrap envelope) =="
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
  python3 "$S/lane/plans/round42_c1_verify.py" --battery-dir "$S/bat" --only XO5,XO6,XO7 --work "$S/work"
echo "RC=$?"

echo "== Q32 post =="
date +%T
ls -A /home/vgpnk/.local/bin | sha256sum
