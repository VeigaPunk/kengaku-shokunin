#!/bin/bash
# F40CritCounterLimits counter runner. Every invocation is wrapped in the round-40 HOST-SAFETY sandbox.
# usage: run.sh <label> <counter-file> <battery-dir> <only|-> [path-prefix]
set -u
S=/fast/scratch/hyaku/kengaku-r40/F40CritCounterLimits
label=$1; counter=$2; bdir=$3; only=$4
export TMPDIR="$S/tmp/$label"
mkdir -p "$TMPDIR"
if [ "${5:-}" != "" ]; then export PATH="$5"; fi
args=(--lane "$S/lane" --work "$TMPDIR")
[ "$bdir" != "-" ] && args+=(--battery-dir "$bdir")
[ "$only" != "-" ] && args+=(--only "$only")
echo "# counter=$counter battery=$bdir only=$only"
echo "# PATH=${PATH}"
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
      bash -c 'cd "$0" && exec "$@"' "$S/lane" python3 "$S/lane/plans/$counter" "${args[@]}" 2>&1
echo "EXIT=$?"
