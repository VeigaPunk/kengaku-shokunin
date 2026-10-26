#!/usr/bin/env bash
# Round-41 no-harm baseline (seat R41ExecNoHarm, wave 1). A clean `--shared` clone of the lane at the frozen
# first-probe-run commit, then every standing instrument of rounds 36-41 run inside the ruled host-safety
# envelope. Prints one `INSTRUMENT <name> exit=<rc>` + summary lines per instrument, then a GREEN/RED tally.
#
#   usage: ./measure.sh [LOGDIR]          (KEEP=1 keeps the scratch tree; default removes it)
#   env:   LANE=, COMMIT=, S=, LOGDIR=
#
# Host-safety envelope (binding, orchestrator 2026-10-26): every counter / battery / fixture build writes only
# inside bwrap; ~/.local/bin stays read-only; PATH dirs, /usr, /etc and $HOME outside scratch are never written.
set -u
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kengaku-shokunin}
COMMIT=${COMMIT:-f774a87ad071122acd39ba02a9901b5b56d9910a}
S=${S:-/fast/scratch/hyaku/kengaku-r41/R41ExecNoHarm}
LOGDIR=${1:-${LOGDIR:-/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-41/build/R41ExecNoHarm/logs}}
BIN=/home/vgpnk/.local/bin
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
BW=(bwrap --dev-bind / / --ro-bind "$BIN" "$BIN" --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent)

command -v bwrap >/dev/null || { echo "SETUP no bwrap"; exit 2; }
mkdir -p "$S" "$LOGDIR" || exit 2
export TMPDIR="$S/tmp"; mkdir -p "$TMPDIR"
trap '[ "${KEEP:-0}" = 1 ] || rm -rf -- "$S"' EXIT

start=$(date +%s)
git clone -q --shared "$LANE" "$S/lane" || { echo "SETUP clone failed"; exit 2; }
# A detached `--shared` clone would hand CHILD clones (every counter clones the lane) the source's master, not
# the measured commit; pin master to COMMIT so a child clone of this clone checks out the frozen bytes.
git -C "$S/lane" checkout -q -B master "$COMMIT" || { echo "SETUP checkout failed"; exit 2; }
top=$(git -C "$S/lane" rev-parse --show-toplevel)
[ "$top" = "$S/lane" ] || { echo "SETUP bad clone top=$top"; exit 2; }
cd "$S/lane" || exit 2

echo "TIP $(git -C "$S/lane" rev-parse HEAD) source_tip $(git -C "$LANE" rev-parse HEAD)"
echo "clone_dirty_before=$(git status --porcelain --untracked-files=all | wc -l)"
echo "pathdir_git_entry=$([ -e "$BIN/git" ] && echo present || echo absent) pathdir_files=$(find "$BIN" -maxdepth 1 -type f | wc -l)"
echo "neutralized_modules=$(sha256sum .ufo/waves/round-40/build/R40CritC1Counter/crit_git_shim.py .ufo/waves/round-40/build/R40CritC1Counter/crit_ledger_selfread.py | awk '{print $1}' | tr '\n' ' ')"
echo "neutralized_banner_lines=$(grep -c NEUTRALIZED .ufo/waves/round-40/build/R40CritC1Counter/crit_git_shim.py .ufo/waves/round-40/build/R40CritC1Counter/crit_ledger_selfread.py | awk -F: '{s+=$2} END{print s}')"
echo "neutralized_referenced_by_plans=$(grep -rl 'crit_git_shim\|crit_ledger_selfread' plans 2>/dev/null | wc -l)"

TOTAL=0; GREEN=0
RC=0
run() {  # run <name> <argv...>   (cwd = clone root; private TMPDIR and --work dirs per instrument)
    local name=$1; shift
    local w="$S/w/$name"
    mkdir -p "$w" "$S/tmp/$name"
    ( cd "$S/lane" && "${BW[@]}" env TMPDIR="$S/tmp/$name" "$@" >"$LOGDIR/$name.log" 2>&1 )
    RC=$?
    echo "INSTRUMENT $name exit=$RC cmd=$*"
    grep -aE '^(PINS|BATTERY|MUTANTS|MUTANTS-BY-TOOL|ADVERTISED|PINS-AFTER|checks=|PREDICATE|rows=|tip |receipts=|note |ORDER RESULT|ORDER FAIL|ORDER ERROR|ROUND-CLOSE|ROUND-CLOSE RESULT|REF |REFUSE|cases=|regrade |EVIDENCE|USAGE|SETUP)' "$LOGDIR/$name.log" | sed 's/^/    /'
    grep -aE '(DEFECT|SURVIVED|WRONG|TAMPERED|NULL |differ)' "$LOGDIR/$name.log" | head -20 | sed 's/^/    ! /'
}
check() { # check <name> <pattern>   (uses $RC from the preceding run; a verdict needs exit 0 AND the line)
    local name=$1 pat=$2
    TOTAL=$((TOTAL + 1))
    if [ "$RC" -eq 0 ] && grep -aqE "$pat" "$LOGDIR/$name.log"; then
        GREEN=$((GREEN + 1)); echo "GREEN $name rc=$RC"
    else
        echo "RED   $name rc=$RC pattern=$pat"
    fi
}

run r40_c1 python3 plans/round40_c1_verify.py --lane . --work "$S/w/r40_c1";                 check r40_c1 '^PREDICATE C1 pass$'
run r40_c2 python3 plans/round40_c2_verify.py --lane . --work "$S/w/r40_c2";                 check r40_c2 '^PREDICATE C2 pass$'
run r39_c1 python3 plans/round39_c1_verify.py --lane . --work "$S/w/r39_c1";                 check r39_c1 '^PREDICATE C1 pass$'
run r39_c2 python3 plans/round39_c2_verify.py --lane . --work "$S/w/r39_c2";                 check r39_c2 '^PREDICATE C2 pass$'
run r38_c2 python3 plans/round38_c2_verify.py --lane . --work "$S/w/r38_c2";                 check r38_c2 '^PREDICATE C2 pass$'
run r37_c1 python3 plans/round37_c1_verify.py --lane . --work "$S/w/r37_c1";                 check r37_c1 '^PREDICATE C1 pass$'
run r37_c2 python3 plans/round37_c2_verify.py --lane . --work "$S/w/r37_c2";                 check r37_c2 '^PREDICATE C2 pass$'
run r36_c2 python3 plans/round36_c2_verify.py --lane . --fleet /home/vgpnk/Projects/shokunin; check r36_c2 '^PREDICATE C2 pass$'
run anchor python3 plans/anchor_digest_check.py --lane .;                                    check anchor '^rows=[0-9]+ tokens=[0-9]+ defects=0$'
run ledger_tip python3 plans/ledger_tip.py --source "$S/lane" --work "$S/lt";                check ledger_tip '^rows=[0-9]+ closed=[0-9]+ observed_pass=[0-9]+ mismatches=0$'
run tip_receipts python3 plans/tip_receipts.py --lane . --work "$S/tr";                      check tip_receipts '^receipts=[0-9]+ byte_equal=[0-9]+ differ=0 skipped=[0-9]+$'
run order39 python3 plans/order_check.py --lane . --claims plans/round-39-claims.md --receipt corpus/evidence/round39/git-leak-probe.txt; check order39 '^ORDER RESULT PASS$'
run order40 python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt;   check order40 '^ORDER RESULT PASS$'
run order41 python3 plans/order_check.py --lane . --claims plans/round-41-claims.md --receipt corpus/evidence/round41/constraints-probe.txt; check order41 '^ORDER RESULT PASS$'
run close40 python3 plans/round_close.py --lane . --round 40 --census "$CENSUS";              check close40 '^ROUND-CLOSE RESULT PASS exit=0$'
run close41 python3 plans/round_close.py --lane . --round 41 --census "$CENSUS";              check close41 '^ROUND-CLOSE RESULT PASS exit=0$'

# db_wal_probe: stdout only, byte-compared with its committed receipt (round-40 probe determinism)
mkdir -p "$S/w/dbwal" "$S/tmp/dbwal"
( cd "$S/lane" && "${BW[@]}" env TMPDIR="$S/tmp/dbwal" python3 plans/db_wal_probe.py --lane . --work "$S/w/dbwal" \
    >"$LOGDIR/db_wal_probe.out" 2>"$LOGDIR/db_wal_probe.err" )
RC=$?
if cmp -s "$LOGDIR/db_wal_probe.out" corpus/evidence/round40/db-wal-probe.txt; then be=yes; else be=no; fi
echo "INSTRUMENT db_wal_probe exit=$RC byte_equal=$be receipt_sha256=$(sha256sum corpus/evidence/round40/db-wal-probe.txt | awk '{print $1}') fresh_sha256=$(sha256sum "$LOGDIR/db_wal_probe.out" | awk '{print $1}')"
tail -2 "$LOGDIR/db_wal_probe.out" | sed 's/^/    /'
TOTAL=$((TOTAL + 1)); if [ "$RC" -eq 0 ] && [ "$be" = yes ]; then GREEN=$((GREEN + 1)); echo "GREEN db_wal_probe rc=$RC"; else echo "RED   db_wal_probe rc=$RC byte_equal=$be"; fi

# frozen digests of the round-41 freeze, verified from the clone root
( cd "$S/lane" && "${BW[@]}" sha256sum -c .ufo/waves/round-41/claims/frozen-digests.txt >"$LOGDIR/frozen_digests.log" 2>&1 )
RC=$?
echo "INSTRUMENT frozen_digests exit=$RC files=$(wc -l < .ufo/waves/round-41/claims/frozen-digests.txt) ok=$(grep -ac ': OK$' "$LOGDIR/frozen_digests.log") failed=$(grep -ac ': FAILED$' "$LOGDIR/frozen_digests.log")"
TOTAL=$((TOTAL + 1)); if [ "$RC" -eq 0 ] && [ "$(grep -ac ': OK$' "$LOGDIR/frozen_digests.log")" -eq 11 ]; then GREEN=$((GREEN + 1)); echo "GREEN frozen_digests rc=$RC"; else echo "RED   frozen_digests rc=$RC"; fi

echo "lane_head_after=$(git -C "$S/lane" rev-parse HEAD)"
echo "clone_dirty_after=$(git -C "$S/lane" status --porcelain --untracked-files=all | wc -l)"
echo "pathdir_new_entries=$(find "$BIN" -newermt "@$start" 2>/dev/null | wc -l)"
echo "pathdir_git_entry_after=$([ -e "$BIN/git" ] && echo present || echo absent) pathdir_files_after=$(find "$BIN" -maxdepth 1 -type f | wc -l)"
echo "baseline green=$GREEN of $TOTAL"
exit 0
