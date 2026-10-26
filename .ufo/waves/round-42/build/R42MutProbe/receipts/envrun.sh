#!/usr/bin/env bash
# Q32 envelope (task line, verbatim) + timestamps + ~/.local/bin listing digest before/after
set -u
ENV=(/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent)
before=$(ls -A /home/vgpnk/.local/bin | sha256sum | cut -c1-16)
echo "ENVELOPE ${ENV[*]} -- $*"
echo "ENVELOPE start $(date +%T) cwd=$PWD"
"${ENV[@]}" "$@"
rc=$?
after=$(ls -A /home/vgpnk/.local/bin | sha256sum | cut -c1-16)
echo "ENVELOPE end $(date +%T) exit=$rc local_bin_before=$before after=$after $( [ "$before" = "$after" ] && echo unchanged || echo CHANGED)"
exit $rc
