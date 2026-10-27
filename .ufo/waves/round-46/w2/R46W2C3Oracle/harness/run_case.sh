#!/bin/bash
# Per-case sandbox: a scratch-rooted mini root (so /app is writable inside), the state dir bound
# at /app, the harness+grader bound read-only at /work. Runs under envelope.sh, never alone.
set -u
S=/fast/scratch/hyaku/kengaku-r46/R46W2C3Oracle
CASE=$1
echo "LANE_CLONE_TOP $(git -C "$S/lane" rev-parse --show-toplevel)"
echo "LANE_CLONE_HEAD $(git -C "$S/lane" rev-parse HEAD)"
echo "GRADER_SHA256 $(sha256sum "$S/run/test_outputs.py" | cut -d' ' -f1)  (captured test_outputs.py)"
echo "SOLVE_SHA256 $(sha256sum "$S/run/solve.sh" | cut -d' ' -f1)  (captured solve.sh)"
echo "TOOLCHAIN $(python3 -V 2>&1) / $(gcc --version | head -1) / host, not the image's python 3.12.3 + gcc 13.2.0"
exec bwrap --bind "$S/root" / \
  --ro-bind /usr /usr --ro-bind /etc /etc \
  --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 \
  --ro-bind /sys /sys --dev /dev --proc /proc --tmpfs /tmp \
  --bind "$S/states/$CASE" /app \
  --ro-bind "$S/run" /work \
  --chdir /app \
  python3 /work/grade.py --work "$S" "$CASE"
