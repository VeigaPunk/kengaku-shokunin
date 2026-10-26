#!/bin/bash
# usage: run_case.sh <variant.py> <fixture-dir> <tag>
# Runs one tool variant on one built fixture under the counter's tool-run conditions:
# fixed system PATH (no uv), HOME empty, git config neutralised, cwd = fixture dir,
# inside the mandated bwrap envelope. Tool writes only under --work (inside scratch).
S=/fast/scratch/hyaku/kengaku-r41/F41RevBatCtl
V="$1"; FX="$2"; TAG="$3"
LANE=$(ls -d "$FX"/lane-*) || exit 2
W="$S/wrun/$TAG"
case "$W" in "$S"|"$S"/*) ;; *) echo refuse; exit 1;; esac
rm -rf "$W"; mkdir -p "$W"
cd "$FX" || exit 2
env -i PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
  HOME="$S/home" LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  TMPDIR="$S/rtmp" GIT_CEILING_DIRECTORIES="$S" \
  GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_COUNT=2 \
  GIT_CONFIG_KEY_0=core.fsmonitor GIT_CONFIG_VALUE_0=false \
  GIT_CONFIG_KEY_1=core.hooksPath GIT_CONFIG_VALUE_1=/dev/null \
  bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
  /usr/bin/python3 "$V" --lane "$LANE" --work "$W" > "$S/out/$TAG.out" 2> "$S/out/$TAG.err"
rc=$?
echo "== $TAG rc=$rc lane=$(basename "$LANE") variant=$(basename "$V")"
