#!/bin/sh
set -u
S=/fast/scratch/hyaku/kengaku-r41/F41RevBatSrcModes
exec bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
  /usr/bin/python3 "$S/lane/plans/round41_c1_verify.py" --lane "$S/lane" \
  --battery-dir "$S/bat" --only S01,S04,S08,S09 --work "$S/w"
