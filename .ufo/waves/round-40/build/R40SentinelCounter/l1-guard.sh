#!/bin/sh
# Read-only post-run guard for the C1 counter (round 40). The frozen counter cannot see writes outside a
# fixture tree (see R40SentinelCounter.md F1/F2). Run after every `plans/round40_c1_verify.py` run.
set -eu
LANE=${1:-/home/vgpnk/Projects/shokunin/kengaku-shokunin}
cd "$LANE"
echo "# tree status (non-empty = the run wrote into the lane)"
git status --porcelain
echo "# frozen digests (anything but ': OK' is a defect)"
sha256sum -c .ufo/waves/round-40/claims/frozen-digests.txt 2>&1 | grep -v ': OK$' || true
echo "# home persistence paths touched today"
for f in "$HOME/.ssh/authorized_keys" "$HOME/.bashrc" "$HOME/.config/systemd/user"; do
  [ -e "$f" ] && ls -ld --time-style=full-iso "$f"
done
