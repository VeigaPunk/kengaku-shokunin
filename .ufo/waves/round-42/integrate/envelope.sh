#!/usr/bin/env bash
# Round-42 L1 envelope, v2 (integration runs). Same as .ufo/waves/round-42/claims/envelope.sh (QUALITY Q32: host home
# read-only, scratch writable, envelope line, start/end `date +%T`, `~/.local/bin` listing digest before/after) plus a
# scratch-backed overlay on /home/vgpnk/.cache. Why: under v1 the pkg gate's P10 runs `uv run --with biopython`, and
# uv cannot take its cache lock on a read-only home ("Could not acquire lock", integrate/measure-baseline-v1.txt), so
# every C2 counter and ledger row R35-D1 went red for an envelope reason, not a lane reason. The host's real cache is
# never written: the overlay lives in "$SCR/home-cache".
#   usage: envelope.sh <scratch dir> <command...>      (stdout is the receipt; redirect it outside)
set -u
SCR=$1; shift
mkdir -p "$SCR/home-cache"
ENV=(/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind "$SCR" "$SCR"
     --bind "$SCR/home-cache" /home/vgpnk/.cache
     --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent)
before=$(ls -A /home/vgpnk/.local/bin | sha256sum | cut -c1-16)
echo "ENVELOPE ${ENV[*]} -- $*"
echo "ENVELOPE start $(date +%T) cwd=$PWD"
"${ENV[@]}" "$@"
rc=$?
after=$(ls -A /home/vgpnk/.local/bin | sha256sum | cut -c1-16)
echo "ENVELOPE end $(date +%T) exit=$rc local_bin_listing_before=$before after=$after $( [ "$before" = "$after" ] && echo unchanged || echo CHANGED)"
exit $rc
