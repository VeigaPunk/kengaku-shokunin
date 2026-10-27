#!/usr/bin/env bash
# Round-43 L1 envelope (QUALITY Q32 forward leg; round-42 v2 + closure R6/D5). Host home read-only, scratch the only
# writable tree besides /tmp, a scratch-backed overlay on ~/.cache (uv's lock), the envelope line and start/end
# `date +%T`. New in round 43 (round-42 closure R6, D5: the names-only listing let a content rewrite pass unseen):
# the PATH-dir digest covers every entry's name, type, target and CONTENT bytes; a `CHANGED` digest marks the
# measurement it brackets invalid (the script then exits 4 whatever the command returned).
#   usage: envelope.sh <scratch dir> <command...>      (stdout is the receipt; redirect it outside)
set -u
SCR=$1; shift
mkdir -p "$SCR/home-cache"
ENV=(/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind "$SCR" "$SCR"
     --bind "$SCR/home-cache" /home/vgpnk/.cache
     --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent)
bindigest() {
  ( cd /home/vgpnk/.local/bin 2>/dev/null || exit 0
    find . -mindepth 1 -maxdepth 1 -printf '%f %y %l\n' | LC_ALL=C sort
    find -L . -mindepth 1 -maxdepth 1 -type f -print0 2>/dev/null | LC_ALL=C sort -z | xargs -0 -r sha256sum 2>/dev/null
  ) | sha256sum | cut -c1-16
}
before=$(bindigest)
echo "ENVELOPE ${ENV[*]} -- $*"
echo "ENVELOPE start $(date +%T) cwd=$PWD"
"${ENV[@]}" "$@"
rc=$?
after=$(bindigest)
if [ "$before" = "$after" ]; then st=unchanged; else st=CHANGED; fi
echo "ENVELOPE end $(date +%T) exit=$rc local_bin_content_before=$before after=$after $st"
[ "$st" = CHANGED ] && { echo "ENVELOPE measurement INVALID (PATH dir content changed while it ran)"; exit 4; }
exit $rc
