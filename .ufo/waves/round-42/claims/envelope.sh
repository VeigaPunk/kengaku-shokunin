#!/usr/bin/env bash
# Round-42 L1 envelope (QUALITY Q32 forward leg): run one counter/battery/fixture command inside a sandbox that
# makes the host home (and with it every shared PATH dir under it) read-only, scratch the only writable tree
# besides /tmp, and print the envelope, timestamps and a post-run check of the forbidden target.
#   usage: envelope.sh <scratch dir> <command...>      (stdout is the receipt; redirect it outside)
set -u
SCR=$1; shift
mkdir -p "$SCR"
ENV=(/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind "$SCR" "$SCR"
     --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent)
before=$(ls -A /home/vgpnk/.local/bin | sha256sum | cut -c1-16)
echo "ENVELOPE ${ENV[*]} -- $*"
echo "ENVELOPE start $(date +%T) cwd=$PWD"
"${ENV[@]}" "$@"
rc=$?
after=$(ls -A /home/vgpnk/.local/bin | sha256sum | cut -c1-16)
echo "ENVELOPE end $(date +%T) exit=$rc local_bin_listing_before=$before after=$after $( [ "$before" = "$after" ] && echo unchanged || echo CHANGED)"
exit $rc
