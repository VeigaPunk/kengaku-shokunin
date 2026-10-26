#!/bin/bash
# F42MutBattery receipt wrapper: runs "$@" under the seat bwrap envelope, records
# envelope line, wall times and the PATH-dir hash before/after (QUALITY Q32).
# usage: receipt_run.sh <tag> <command...>
set -u
TAG="$1"; shift
R=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-42/falsify/F42MutBattery
mkdir -p "$R"
REC="$R/receipt-$TAG.txt"
{
  echo "ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- $*"
  echo "SEAT F42MutBattery tag=$TAG"
  echo "START $(date +%T)"
  echo "PATHDIR_BEFORE $(ls -A /home/vgpnk/.local/bin | sha256sum | cut -d' ' -f1)"
} > "$REC"
/usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
  --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- "$@" >> "$REC" 2>&1
RC=$?
{
  echo "PATHDIR_AFTER $(ls -A /home/vgpnk/.local/bin | sha256sum | cut -d' ' -f1)"
  echo "END $(date +%T)"
  echo "EXIT $RC"
} >> "$REC"
echo "receipt=$REC exit=$RC"
exit $RC
