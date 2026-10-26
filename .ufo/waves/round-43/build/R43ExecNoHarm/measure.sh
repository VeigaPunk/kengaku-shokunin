#!/usr/bin/env bash
# Round-43 wave-1 no-harm baseline (seat R43ExecNoHarm). Adapted from
# .ufo/waves/round-42/integrate/measure.sh: a clean `--no-local` clone of the lane at the recorded receipt
# commit (committed bytes only), then the round-43 counters first and the whole round-42 measured set.
# Run inside the Q32 envelope:
#   .ufo/waves/round-43/claims/envelope.sh <seat scratch>/env \
#     .ufo/waves/round-43/build/R43ExecNoHarm/measure.sh <tag>
# Nothing here writes inside the lane: only the clone and the --work dirs under this seat's scratch.
set -u
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
REC=6b49694d2ff533135fc238a8400f3e0dc1c82026
ROOT=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r43
SEAT=$ROOT/R43ExecNoHarm
S=$SEAT/measure-${1:-run}
grep -q 'kengaku r43 round root' "$ROOT/.ROUND-ROOT-SENTINEL" 2>/dev/null && echo "SENTINEL present" || { echo "SENTINEL MISSING"; exit 3; }
case "$S" in "$SEAT"/measure-*) rm -rf -- "$S" ;; *) echo "refusing rm outside $SEAT/measure-*"; exit 3 ;; esac
mkdir -p "$S"; export TMPDIR="$S"
trap 'rm -rf -- "$S"' EXIT
git clone -q --no-local "$L" "$S/lane" && git -C "$S/lane" checkout -q "$REC"
[ "$(git -C "$S/lane" rev-parse --show-toplevel)" = "$S/lane" ] || { echo "bad clone"; exit 2; }
cd "$S/lane"
echo "REC $REC"
echo "HEAD $(git rev-parse HEAD)"
echo "untracked_in_clone=$(git status --porcelain --untracked-files=all | wc -l)"
r() { echo "\$ $*"; "$@"; echo "exit=$?"; }
mkdir -p "$S/c1" "$S/c2" "$S/pr" "$S/lt" "$S/tr" "$S/w"
# --- round 43 first: expected red at the receipt commit (no plans/battery43, no corpus entry)
r python3 plans/round43_c1_verify.py --lane . --work "$S/c1"
r python3 plans/round43_c2_verify.py --lane . --work "$S/c2"
r python3 plans/order_check.py --lane . --claims plans/round-43-claims.md --receipt corpus/evidence/round43/feal-probe.txt
# --- round 42 measured set, same order as round-42 integrate/measure.sh
r python3 plans/round42_c1_verify.py --lane . --work "$S/c1"
r python3 plans/round42_c2_verify.py --lane . --work "$S/c2"
r python3 plans/order_check.py --lane . --claims plans/round-42-claims.md --receipt corpus/evidence/round42/fibsqrt-probe.txt
r python3 plans/round41_c1_verify.py --lane . --work "$S/w"
r python3 plans/round41_c2_verify.py --lane . --work "$S/w"
r python3 plans/order_check.py --lane . --claims plans/round-41-claims.md --receipt corpus/evidence/round41/constraints-probe.txt
r python3 plans/round40_c1_verify.py --lane . --work "$S/w"
r python3 plans/round40_c2_verify.py --lane . --work "$S/w"
r python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt
r python3 plans/order_check.py --lane . --claims plans/round-39-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt
r python3 plans/order_check.py --lane . --claims plans/round-38-claims.md --receipt corpus/evidence/round38/build-pmars-probe.txt
r python3 plans/round39_c1_verify.py --lane . --work "$S/w"
r python3 plans/round39_c2_verify.py --lane . --work "$S/w"
r python3 plans/round38_c1_verify.py --lane . --work "$S/w"
r python3 plans/round38_c2_verify.py --lane . --work "$S/w"
r python3 plans/round37_c1_verify.py --lane . --work "$S/w"
r python3 plans/round37_c2_verify.py --lane . --work "$S/w"
r python3 plans/round36_c2_verify.py --lane .
r python3 plans/anchor_digest_check.py --lane .
r /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md
r sha256sum -c .ufo/waves/round-43/claims/frozen-digests.txt
r sha256sum -c .ufo/waves/round-42/claims/frozen-digests.txt
r sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt
r sha256sum -c .ufo/waves/round-40/claims/frozen-digests.txt
r sha256sum -c .ufo/waves/round-39/claims/frozen-digests.txt
r python3 plans/ledger_tip.py --source "$S/lane" --work "$S/lt"
r python3 plans/tip_receipts.py --lane . --work "$S/tr"
r python3 plans/routed_open.py
r python3 plans/db_wal_probe.py --lane . --work "$S/pr"
python3 plans/constraints_probe.py --lane . --work "$S/pr" > "$S/csp.txt"; echo "constraints_probe exit=$? byte_equal=$(cmp -s "$S/csp.txt" corpus/evidence/round41/constraints-probe.txt && echo yes || echo NO)"
python3 plans/fibsqrt_probe.py --lane . --work "$S/pr" > "$S/fsp.txt"; echo "fibsqrt_probe exit=$? byte_equal=$(cmp -s "$S/fsp.txt" corpus/evidence/round42/fibsqrt-probe.txt && echo yes || echo NO)"
r python3 plans/round_close.py --lane . --round 42 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
r python3 plans/round_close.py --lane . --round 43 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
# --- EXTRA, not part of the round-42 baseline: the frozen round-43 package gate (read-only, P9/P10 skipped)
r python3 plans/pkg_gate.py package --root . --spec plans/pkg-spec-r43.json
echo "registry_rows=$(grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md) knowledge_files=$(ls corpus/knowledge/*.md | wc -l) index_rows=$(grep -cE '^\| `knowledge/[^`]+` \|' corpus/README.md)"
