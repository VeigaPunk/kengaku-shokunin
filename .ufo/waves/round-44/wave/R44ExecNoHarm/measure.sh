#!/usr/bin/env bash
# Round-44 no-harm baseline (seat R44ExecNoHarm), adapted from round-43 `integrate/measure.sh`.
# Reads committed bytes only: run it on a clean `git clone --no-local` of the lane at the receipt commit
# 45dc0bc81e42e02ecd272712086c372c8844b108, inside .ufo/waves/round-44/claims/envelope.sh (home read-only,
# ~/.local/bin content digest bracketed). Round-44 counters come first; they are expected RED at that commit
# (no plans/battery44, no corpus/knowledge entry yet) and the script says which reds are expected.
#   usage: measure.sh <clone> --work <dir>
# <clone> must be the work-tree top of the clone; --work must lie outside it (the counters build sandboxes).
set -u

CLONE=${1:-}; shift || true
WORK=
while [ $# -gt 0 ]; do
  case "$1" in
    --work) WORK=${2:-}; shift 2 ;;
    *) echo "usage: measure.sh <clone> --work <dir>" >&2; exit 2 ;;
  esac
done
[ -n "$CLONE" ] && [ -n "$WORK" ] || { echo "usage: measure.sh <clone> --work <dir>" >&2; exit 2; }
CLONE=$(cd "$CLONE" 2>/dev/null && pwd) || { echo "SETUP clone unreadable: $CLONE" >&2; exit 2; }
mkdir -p "$WORK" || { echo "SETUP --work uncreatable: $WORK" >&2; exit 2; }
WORK=$(cd "$WORK" && pwd)
TOP=$(git -C "$CLONE" rev-parse --show-toplevel 2>/dev/null) || { echo "SETUP not a git work tree: $CLONE" >&2; exit 2; }
[ "$TOP" = "$CLONE" ] || { echo "SETUP clone top is $TOP, expected $CLONE" >&2; exit 2; }
case "$WORK/" in "$CLONE"/*) echo "SETUP --work must lie outside the clone ($CLONE)" >&2; exit 2 ;; esac
export TMPDIR="$WORK"
cd "$CLONE" || exit 2

echo "CLONE $CLONE"
echo "HEAD $(git -C "$CLONE" rev-parse HEAD)"
echo "untracked_in_clone=$(git -C "$CLONE" status --porcelain --untracked-files=all | wc -l)"
echo "python3=$(command -v python3) $(python3 -V 2>&1)"
echo "bwrap=$(command -v bwrap || echo MISSING)"
# Rounds 36-42 counters read --work but never create it (round 43 pre-created one shared dir); create each here.
mkdir -p "$WORK/c1" "$WORK/c2" "$WORK/probes" "$WORK/w-lt" "$WORK/w-tr" \
  "$WORK/w-r43c1" "$WORK/w-r43c2" "$WORK/w-r42c1" "$WORK/w-r42c2" \
  "$WORK/w-r41c1" "$WORK/w-r41c2" "$WORK/w-r40c1" "$WORK/w-r40c2" \
  "$WORK/w-r39c1" "$WORK/w-r39c2" "$WORK/w-r38c1" "$WORK/w-r38c2" \
  "$WORK/w-r37c1" "$WORK/w-r37c2"

TOTAL=0
GREEN=0
REDS=()

# Red classification at the receipt commit (all three classes are printed, never hidden):
#   expected-red  r44-c1, r44-c2  — the freeze's do-nothing controls say these must be red here
#                 (claims/control-c1-nothing.txt `killed=0 survived=5`; claims/control-c2-nothing.txt
#                 `checks=11 defects=8`). A green here would falsify the control and is flagged.
#   carried-red   r38-order (ORDER HIT control-c2-skip.txt@e0a378539a45:11 kind=gate-p10) and r38-c1
#                 (MUTANT N21 D5 silence SURVIVED, killed=21/22) — red byte-identically at the round-42
#                 (measure-tip3.txt) and round-43 (build/R43ExecNoHarm/measure-v1.txt:339, :577) baselines;
#                 round-38 routed work, outside this round's remit.
#   UNEXPECTED    anything else, or an expected red that came back green.

chk() {
  local name=$1; shift
  TOTAL=$((TOTAL + 1))
  echo "CHECK $name :: $*"
  "$@"
  local rc=$?
  echo "CHECK $name exit=$rc"
  if [ "$rc" -eq 0 ]; then GREEN=$((GREEN + 1)); else REDS+=("$name exit=$rc"); fi
  return 0
}

# probe output must be byte-equal to the committed receipt, and exit 0
probe_cmp() {
  local probe=$1 receipt=$2 out=$3
  python3 "$probe" --lane . --work "$WORK/probes" > "$out"
  local prc=$?
  if cmp -s "$out" "$receipt"; then
    echo "PROBE $probe exit=$prc byte_equal=yes receipt=$receipt"
    [ "$prc" -eq 0 ]
    return
  fi
  echo "PROBE $probe exit=$prc byte_equal=NO receipt=$receipt"
  return 1
}

echo "== round 44 first (expected RED at the receipt commit)"
chk r44-c1 python3 plans/round44_c1_verify.py --lane . --work "$WORK/c1"
chk r44-c2 python3 plans/round44_c2_verify.py --lane . --work "$WORK/c2"
chk r44-order python3 plans/order_check.py --lane . --claims plans/round-44-claims.md \
    --receipt corpus/evidence/round44/feal-linear-probe.txt

echo "== counters rounds 36-43 (the round-43 set)"
chk r43-c1 python3 plans/round43_c1_verify.py --lane . --work "$WORK/w-r43c1"
chk r43-c2 python3 plans/round43_c2_verify.py --lane . --work "$WORK/w-r43c2"
chk r43-order python3 plans/order_check.py --lane . --claims plans/round-43-claims.md \
    --receipt corpus/evidence/round43/feal-probe.txt
chk r42-c1 python3 plans/round42_c1_verify.py --lane . --work "$WORK/w-r42c1"
chk r42-c2 python3 plans/round42_c2_verify.py --lane . --work "$WORK/w-r42c2"
chk r42-order python3 plans/order_check.py --lane . --claims plans/round-42-claims.md \
    --receipt corpus/evidence/round42/fibsqrt-probe.txt
chk r41-c1 python3 plans/round41_c1_verify.py --lane . --work "$WORK/w-r41c1"
chk r41-c2 python3 plans/round41_c2_verify.py --lane . --work "$WORK/w-r41c2"
chk r41-order python3 plans/order_check.py --lane . --claims plans/round-41-claims.md \
    --receipt corpus/evidence/round41/constraints-probe.txt
chk r40-c1 python3 plans/round40_c1_verify.py --lane . --work "$WORK/w-r40c1"
chk r40-c2 python3 plans/round40_c2_verify.py --lane . --work "$WORK/w-r40c2"
chk r40-order python3 plans/order_check.py --lane . --claims plans/round-40-claims.md \
    --receipt corpus/evidence/round40/db-wal-probe.txt
chk r39-order python3 plans/order_check.py --lane . --claims plans/round-39-claims.md \
    --receipt corpus/evidence/round39/git-leak-probe.txt
chk r38-order python3 plans/order_check.py --lane . --claims plans/round-38-claims.md \
    --receipt corpus/evidence/round38/build-pmars-probe.txt
chk r39-c1 python3 plans/round39_c1_verify.py --lane . --work "$WORK/w-r39c1"
chk r39-c2 python3 plans/round39_c2_verify.py --lane . --work "$WORK/w-r39c2"
chk r38-c1 python3 plans/round38_c1_verify.py --lane . --work "$WORK/w-r38c1"
chk r38-c2 python3 plans/round38_c2_verify.py --lane . --work "$WORK/w-r38c2"
chk r37-c1 python3 plans/round37_c1_verify.py --lane . --work "$WORK/w-r37c1"
chk r37-c2 python3 plans/round37_c2_verify.py --lane . --work "$WORK/w-r37c2"
chk r36-c2 python3 plans/round36_c2_verify.py --lane .

echo "== tools, census, frozen digests r39-r44"
chk anchor-check python3 plans/anchor_digest_check.py --lane .
chk census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md
chk digests-r44 sha256sum -c .ufo/waves/round-44/claims/frozen-digests.txt
chk digests-r43 sha256sum -c .ufo/waves/round-43/claims/frozen-digests.txt
chk digests-r42 sha256sum -c .ufo/waves/round-42/claims/frozen-digests.txt
chk digests-r41 sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt
chk digests-r40 sha256sum -c .ufo/waves/round-40/claims/frozen-digests.txt
chk digests-r39 sha256sum -c .ufo/waves/round-39/claims/frozen-digests.txt

echo "== ledgers and probes"
chk ledger-tip python3 plans/ledger_tip.py --source "$CLONE" --work "$WORK/w-lt"
chk tip-receipts python3 plans/tip_receipts.py --lane . --work "$WORK/w-tr"
chk routed-open python3 plans/routed_open.py
chk db-wal-byte-equal probe_cmp plans/db_wal_probe.py corpus/evidence/round40/db-wal-probe.txt \
    "$WORK/probes/db-wal.txt"
chk constraints-byte-equal probe_cmp plans/constraints_probe.py corpus/evidence/round41/constraints-probe.txt \
    "$WORK/probes/constraints.txt"
chk fibsqrt-byte-equal probe_cmp plans/fibsqrt_probe.py corpus/evidence/round42/fibsqrt-probe.txt \
    "$WORK/probes/fibsqrt.txt"
chk feal-byte-equal probe_cmp plans/feal_probe.py corpus/evidence/round43/feal-probe.txt \
    "$WORK/probes/feal.txt"

echo "== round close and flip checks"
chk round-close-42 python3 plans/round_close.py --lane . --round 42 \
    --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
chk round-close-43 python3 plans/round_close.py --lane . --round 43 \
    --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
chk round-close-44 python3 plans/round_close.py --lane . --round 44 \
    --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
chk gate-flip-42 python3 plans/gate_flip_check.py --lesson corpus/lessons/round-42.md
chk gate-flip-43 python3 plans/gate_flip_check.py --lesson corpus/lessons/round-43.md

echo "registry_rows=$(grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md) knowledge_files=$(ls corpus/knowledge/*.md | wc -l) index_rows=$(grep -cE '^\| `knowledge/[^`]+` \|' corpus/README.md)"

UNEXPECTED=0
N_EXPECTED=0
N_CARRIED=0
echo "SUMMARY total=$TOTAL green=$GREEN red=$((TOTAL - GREEN))"
for entry in ${REDS[@]+"${REDS[@]}"}; do
  name=${entry%% *}
  case "$name" in
    r44-c1|r44-c2) tag=expected-red; N_EXPECTED=$((N_EXPECTED + 1)) ;;
    r38-order|r38-c1) tag=carried-red; N_CARRIED=$((N_CARRIED + 1)) ;;
    *) tag=UNEXPECTED-RED; UNEXPECTED=$((UNEXPECTED + 1)) ;;
  esac
  echo "RED $entry $tag"
done
for name in r44-c1 r44-c2; do
  seen=0
  for entry in ${REDS[@]+"${REDS[@]}"}; do [ "${entry%% *}" = "$name" ] && seen=1; done
  [ "$seen" -eq 1 ] || {
    echo "MISSING-RED $name: the freeze's do-nothing control says this is red at the receipt commit"
    UNEXPECTED=$((UNEXPECTED + 1))
  }
done
echo "NO-HARM-BASELINE ${GREEN}-green-of-${TOTAL} expected_red=$N_EXPECTED carried_red=$N_CARRIED unexpected_red=$UNEXPECTED"
[ "$UNEXPECTED" -eq 0 ] && exit 0 || exit 1
