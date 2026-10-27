#!/usr/bin/env bash
# Replica of claims/envelope.sh for a scratch lab demo. Sole delta (marked DELTA):
# bindigest cd target parameterized via RDBIN (default unchanged: /home/vgpnk/.local/bin).
set -u
SCR=$1; shift
mkdir -p "$SCR/home-cache"
ENV=(/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind "$SCR" "$SCR"
     --bind "$SCR/home-cache" /home/vgpnk/.cache
     --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent)
bindigest() {
  ( cd "${RDBIN:-/home/vgpnk/.local/bin}" 2>/dev/null || exit 0
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
