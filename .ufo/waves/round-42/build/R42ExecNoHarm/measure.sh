#!/usr/bin/env bash
# Round-42 no-harm baseline (seat R42ExecNoHarm, wave 1). A clean `--shared` clone of the lane pinned to the
# round-42 first recorded probe run (523b27806be0df26d2235089d845265a29f8cedf), then every standing instrument
# of rounds 36-42 named by the seat task, run inside the ruled host-safety envelope. One `INSTRUMENT <name>`
# line per leg (start, end, pathdir hash before/after, exit) and one GREEN/RED line; a final tally.
#
#   usage: ./measure.sh [SCRATCH]        (scratch root; default /fast/scratch/hyaku/kengaku-r42/R42ExecNoHarm/run)
#   env:   LANE= COMMIT= LOGDIR= KEEP=1  (KEEP=1 leaves the scratch tree in place)
#
# Host-safety envelope (orchestrator, binding for every seat): every counter / battery / fixture build runs
# under bwrap with ~/.local/bin read-only, a private /run/user/1000 and pid namespace; nothing is written to a
# shared PATH dir, /usr, /etc, or $HOME outside scratch (each leg gets HOME=$TMPDIR/home).
set -u
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kengaku-shokunin}
COMMIT=${COMMIT:-523b27806be0df26d2235089d845265a29f8cedf}
S=${1:-${S:-/fast/scratch/hyaku/kengaku-r42/R42ExecNoHarm/run}}
LOGDIR=${LOGDIR:-/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-42/build/R42ExecNoHarm/logs}
BIN=/home/vgpnk/.local/bin
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
BW=(bwrap --dev-bind / / --ro-bind "$BIN" "$BIN" --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent)

# scratch guard (round-41 closure R2): delete only inside this round's own scratch root, never the root itself
case "$S" in
    /fast/scratch/hyaku/kengaku-r42/?*) ;;
    *) echo "SETUP refusing scratch outside /fast/scratch/hyaku/kengaku-r42/<seat>: $S"; exit 2 ;;
esac
command -v bwrap >/dev/null || { echo "SETUP no bwrap"; exit 2; }
rm -rf -- "$S"
mkdir -p "$S/tmp" "$S/w" "$LOGDIR" || exit 2
export TMPDIR="$S/tmp"
trap '[ "${KEEP:-0}" = 1 ] || rm -rf -- "$S"' EXIT

start_epoch=$(date +%s)
echo "ENVELOPE ${BW[*]} -- <command>"
echo "RUN start $(date +%T) scratch=$S logdir=$LOGDIR"
echo "LANE $LANE tip_before=$(git -C "$LANE" rev-parse HEAD)"
echo "pathdir=$BIN sha_before=$(ls -A "$BIN" | sha256sum) files_before=$(find "$BIN" -maxdepth 1 -type f | wc -l) git_entry_before=$([ -e "$BIN/git" ] && echo present || echo absent)"

git clone -q --shared "$LANE" "$S/lane" || { echo "SETUP clone failed"; exit 2; }
# a detached --shared clone would hand CHILD clones (every counter clones the lane) the source's master, not the
# measured commit; pin master to COMMIT so a child clone checks out the frozen bytes
git -C "$S/lane" checkout -q -B master "$COMMIT" || { echo "SETUP checkout failed"; exit 2; }
top=$(git -C "$S/lane" rev-parse --show-toplevel)
[ "$top" = "$S/lane" ] || { echo "SETUP bad clone top=$top"; exit 2; }
cd "$S/lane" || exit 2
echo "CLONE top=$top head=$(git -C "$S/lane" rev-parse HEAD) dirty_before=$(git -C "$S/lane" status --porcelain --untracked-files=all | wc -l)"

TOTAL=0; GREEN=0; REDS=""
RC=0
run() {  # run <name> <argv...>   (cwd = clone root; private TMPDIR/HOME/work dir per leg)
    local name=$1; shift
    local w="$S/w/$name"
    mkdir -p "$w" "$S/tmp/$name/home"
    local before; before=$(ls -A "$BIN" | sha256sum | cut -c1-16)
    echo "INSTRUMENT $name start=$(date +%T) pathdir_sha_before=$before cmd=$*"
    ( cd "$S/lane" && "${BW[@]}" env TMPDIR="$S/tmp/$name" HOME="$S/tmp/$name/home" \
        PYTHONDONTWRITEBYTECODE=1 "$@" >"$LOGDIR/$name.log" 2>&1 )
    RC=$?
    echo "INSTRUMENT $name end=$(date +%T) exit=$RC pathdir_sha_after=$(ls -A "$BIN" | sha256sum | cut -c1-16)"
    grep -aE '^(PINS|BATTERY|MUTANTS|MUTANTS-BY-TOOL|PREDICATE|rows=|checks=|receipts=|note |tip |ORDER |ROUND-CLOSE|REF |ROWS |routed_open=|CASE |regrade |cases=|SETUP)' "$LOGDIR/$name.log" | grep -av '^CASE ' | tail -8 | sed 's/^/    /'
}
check() {  # check <name> <pattern>  (uses $RC from the preceding run: exit 0 AND the verdict line)
    local name=$1 pat=$2
    TOTAL=$((TOTAL + 1))
    if [ "$RC" -eq 0 ] && grep -aqE "$pat" "$LOGDIR/$name.log"; then
        GREEN=$((GREEN + 1)); echo "GREEN $name rc=$RC"
    else
        REDS="$REDS $name"; echo "RED   $name rc=$RC pattern=$pat"
    fi
}
check_frozen() {  # check_frozen <name> <digest list rel path>  (every listed file OK, none FAILED, exit 0)
    local name=$1 list=$2 want ok failed
    want=$(wc -l <"$S/lane/$list"); ok=$(grep -ac ': OK$' "$LOGDIR/$name.log"); failed=$(grep -ac ': FAILED$' "$LOGDIR/$name.log")
    TOTAL=$((TOTAL + 1))
    echo "    frozen_ok=$ok want=$want failed=$failed"
    if [ "$RC" -eq 0 ] && [ "$ok" -eq "$want" ] && [ "$failed" -eq 0 ]; then
        GREEN=$((GREEN + 1)); echo "GREEN $name rc=$RC ok=$ok/$want"
    else
        REDS="$REDS $name"; echo "RED   $name rc=$RC ok=$ok/$want failed=$failed"
    fi
}
cmpcheck() {  # cmpcheck <name> <receipt rel path>   (stdout byte-compare with the committed receipt)
    local name=$1 receipt=$2
    shift 2
    local out="$LOGDIR/$name.out"
    mkdir -p "$S/w/$name" "$S/tmp/$name/home"
    echo "INSTRUMENT $name start=$(date +%T) pathdir_sha_before=$(ls -A "$BIN" | sha256sum | cut -c1-16) byte_compare=$receipt"
    ( cd "$S/lane" && "${BW[@]}" env TMPDIR="$S/tmp/$name" HOME="$S/tmp/$name/home" \
        PYTHONDONTWRITEBYTECODE=1 python3 "$@" >"$out" 2>"$LOGDIR/$name.err" )
    RC=$?
    local be=no; cmp -s "$out" "$S/lane/$receipt" && be=yes
    echo "INSTRUMENT $name end=$(date +%T) exit=$RC pathdir_sha_after=$(ls -A "$BIN" | sha256sum | cut -c1-16) byte_equal=$be receipt_sha256=$(sha256sum "$S/lane/$receipt" | cut -d' ' -f1) fresh_sha256=$(sha256sum "$out" | cut -d' ' -f1) fresh_bytes=$(wc -c <"$out")"
    tail -2 "$out" | sed 's/^/    /'
    TOTAL=$((TOTAL + 1))
    if [ "$RC" -eq 0 ] && [ "$be" = yes ]; then GREEN=$((GREEN + 1)); echo "GREEN $name rc=$RC byte_equal=yes"
    else REDS="$REDS $name"; echo "RED   $name rc=$RC byte_equal=$be"; fi
}

# ---- C1 counters (rounds 37-41; round 42's own C1 is the wave in flight, not a standing instrument) --------
run r41_c1 python3 plans/round41_c1_verify.py --lane . --work "$S/w/r41_c1";  check r41_c1 '^PREDICATE C1 pass$'
run r40_c1 python3 plans/round40_c1_verify.py --lane . --work "$S/w/r40_c1";  check r40_c1 '^PREDICATE C1 pass$'
run r39_c1 python3 plans/round39_c1_verify.py --lane . --work "$S/w/r39_c1";  check r39_c1 '^PREDICATE C1 pass$'
run r37_c1 python3 plans/round37_c1_verify.py --lane . --work "$S/w/r37_c1";  check r37_c1 '^PREDICATE C1 pass$'
# ---- C2 counters ----------------------------------------------------------------------------------------
run r41_c2 python3 plans/round41_c2_verify.py --lane . --work "$S/w/r41_c2";  check r41_c2 '^PREDICATE C2 pass$'
run r40_c2 python3 plans/round40_c2_verify.py --lane . --work "$S/w/r40_c2";  check r40_c2 '^PREDICATE C2 pass$'
run r39_c2 python3 plans/round39_c2_verify.py --lane . --work "$S/w/r39_c2";  check r39_c2 '^PREDICATE C2 pass$'
run r38_c2 python3 plans/round38_c2_verify.py --lane . --work "$S/w/r38_c2";  check r38_c2 '^PREDICATE C2 pass$'
run r37_c2 python3 plans/round37_c2_verify.py --lane . --work "$S/w/r37_c2";  check r37_c2 '^PREDICATE C2 pass$'
run r36_c2 python3 plans/round36_c2_verify.py --lane . --fleet /home/vgpnk/Projects/shokunin; check r36_c2 '^PREDICATE C2 pass$'
# ---- frozen tools and their consumers -------------------------------------------------------------------
run anchor python3 plans/anchor_digest_check.py --lane .;                        check anchor '^rows=[0-9]+ tokens=[0-9]+ defects=0$'
run ledger_tip python3 plans/ledger_tip.py --source "$S/lane" --work "$S/lt";   check ledger_tip '^rows=[0-9]+ closed=[0-9]+ observed_pass=[0-9]+ mismatches=0$'
run tip_receipts python3 plans/tip_receipts.py --lane . --work "$S/tr";         check tip_receipts '^receipts=[0-9]+ byte_equal=[0-9]+ differ=0 skipped=[0-9]+$'
run order39 python3 plans/order_check.py --lane . --claims plans/round-39-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt; check order39 '^ORDER RESULT PASS$'
run order40 python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt;   check order40 '^ORDER RESULT PASS$'
run order41 python3 plans/order_check.py --lane . --claims plans/round-41-claims.md --receipt corpus/evidence/round41/constraints-probe.txt; check order41 '^ORDER RESULT PASS$'
run order42 python3 plans/order_check.py --lane . --claims plans/round-42-claims.md --receipt corpus/evidence/round42/fibsqrt-probe.txt; check order42 '^ORDER RESULT PASS$'
run close41 python3 plans/round_close.py --lane . --round 41 --census "$CENSUS"; check close41 '^ROUND-CLOSE RESULT PASS exit=0$'
run close42 python3 plans/round_close.py --lane . --round 42 --census "$CENSUS"; check close42 '^ROUND-CLOSE RESULT PASS exit=0$'
# ---- the two probes, byte-compared with their committed receipts ----------------------------------------
cmpcheck constraints_probe corpus/evidence/round41/constraints-probe.txt plans/constraints_probe.py --lane . --work "$S/pr"
cmpcheck db_wal_probe       corpus/evidence/round40/db-wal-probe.txt       plans/db_wal_probe.py       --lane . --work "$S/pr"
# ---- routed-findings burn-down -------------------------------------------------------------------------
run routed_open python3 plans/routed_open.py --lane .;                          check routed_open '^routed_open=[0-9]+ oldest_round=([0-9]+|-)$'
# ---- frozen digests (round 42, and round 41 as the carried freeze) --------------------------------------
run frozen42 sha256sum -c .ufo/waves/round-42/claims/frozen-digests.txt; check_frozen frozen42 .ufo/waves/round-42/claims/frozen-digests.txt
run frozen41 sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt; check_frozen frozen41 .ufo/waves/round-41/claims/frozen-digests.txt

# ---- uncounted: the freeze state of the round-42 counters (wave 1 is still building them) --------------
echo "# UNCOUNTED freeze-state observation (not part of the tally): the round-42 counters are red at this"
echo "# commit by construction -- C1 has no battery42 yet (control-c1-nothing.txt: killed=0 survived=14)."
run r42_c1_observe python3 plans/round42_c1_verify.py --lane . --work "$S/w/r42_c1"
run r42_c2_observe python3 plans/round42_c2_verify.py --lane . --work "$S/w/r42_c2"

# ---- host-safety receipts ------------------------------------------------------------------------------
echo "pathdir_sha_after=$(ls -A "$BIN" | sha256sum) files_after=$(find "$BIN" -maxdepth 1 -type f | wc -l) git_entry_after=$([ -e "$BIN/git" ] && echo present || echo absent)"
echo "pathdir_new_entries=$(find "$BIN" -newermt "@$start_epoch" 2>/dev/null | wc -l)"
echo "lane_tip_after=$(git -C "$LANE" rev-parse HEAD) clone_head_after=$(git -C "$S/lane" rev-parse HEAD) clone_dirty_after=$(git -C "$S/lane" status --porcelain --untracked-files=all | wc -l)"
echo "frozen_digests_ok42=$(grep -ac ': OK$' "$LOGDIR/frozen42.log") of $(wc -l < .ufo/waves/round-42/claims/frozen-digests.txt) frozen_digests_ok41=$(grep -ac ': OK$' "$LOGDIR/frozen41.log") of $(wc -l < .ufo/waves/round-41/claims/frozen-digests.txt)"
echo "RUN end $(date +%T) elapsed=$(( $(date +%s) - start_epoch ))s"
echo "baseline green=$GREEN of $TOTAL reds=${REDS:- none}"
exit 0
