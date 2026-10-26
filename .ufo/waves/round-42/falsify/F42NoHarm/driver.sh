#!/usr/bin/env bash
# F42NoHarm: measure.sh's command list, verbatim, pinned at 508434a instead of the live branch tip.
set -u
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
COMMIT=508434ad55c709337065611691c426f05875492d
S=/fast/scratch/hyaku/kengaku-r42/F42NoHarm/run-1
grep -q 'kengaku r42 round root' /fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL 2>/dev/null && echo "SENTINEL present" || { echo "SENTINEL MISSING"; exit 3; }
case "$S" in /fast/scratch/hyaku/kengaku-r42/F42NoHarm/*) rm -rf -- "$S" ;; *) echo "refusing rm outside F42NoHarm"; exit 3 ;; esac
mkdir -p "$S" "$S/home" "$S/tmp" "$S/cache"
export TMPDIR="$S/tmp"
export HOME="$S/home"
git clone -q --no-local "$L" "$S/lane" && git -C "$S/lane" checkout -q "$COMMIT"
[ "$(git -C "$S/lane" rev-parse --show-toplevel)" = "$S/lane" ] || { echo "bad clone"; exit 2; }
cd "$S/lane"
echo "TIP $COMMIT"
echo "untracked_in_clone=$(git status --porcelain --untracked-files=all | wc -l)"
r() { echo "\$ $*"; "$@"; echo "exit=$?"; }
mkdir -p "$S/c1" "$S/c2" "$S/pr" "$S/lt" "$S/tr" "$S/w"
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
r python3 plans/round_close.py --lane . --round 41 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
r python3 plans/round_close.py --lane . --round 42 --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
echo "registry_rows=$(grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md) knowledge_files=$(ls corpus/knowledge/*.md | wc -l) index_rows=$(grep -cE '^\| `knowledge/[^`]+` \|' corpus/README.md)"
