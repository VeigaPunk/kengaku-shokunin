#!/usr/bin/env bash
# Round-38 wave 1, seat R38LedgerTip — replays every control quoted in
# .ufo/waves/round-38/build/R38LedgerTip.md. Reads the lane, writes only under $S (scratch, removed on
# exit). Expected values are in the comments; a line whose rc differs from the comment is a changed
# observation, not a style problem.
set -uo pipefail
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
SEAT=$(cd "$(dirname "$0")" && pwd)
DRAFT="$SEAT/ledger_tip.py"          # the fixed draft
COMMITTED="$SEAT/ledger_tip.committed.py"   # byte copy of the landed plans/ledger_tip.py (sha256 67cb3966…)
S=/fast/scratch/hyaku/kengaku-r38/R38LedgerTip-replay
mkdir -p "$S"; export TMPDIR="$S"; trap 'rm -rf -- "$S"' EXIT
git clone -q --shared "$LANE" "$S/lane" || exit 2
[ "$(git -C "$S/lane" rev-parse --show-toplevel)" = "$S/lane" ] || { echo "clone top mismatch"; exit 2; }
[ "$(git -C "$S/lane" status --porcelain | wc -l)" -eq 0 ] || { echo "clone not clean"; exit 2; }
cd "$S/lane" || exit 2
TIP=$(git -C "$S/lane" rev-parse HEAD)
OLD=$(git -C "$S/lane" rev-parse HEAD~1)

# --- fixtures ------------------------------------------------------------------------------------
# A: detached source at HEAD~1 while refs/heads/master stays at HEAD  => clone has no local master
git clone -q --shared "$S/lane" "$S/src-det"; git -C "$S/src-det" checkout -q "$OLD"
# B: source on master (operator path)
# C: reuse refusal (existing <work>/lane), D: non-git source, E: broken control tree
git clone -q --shared "$S/lane" "$S/ctl-nobranch"; git -C "$S/ctl-nobranch" checkout -q "$OLD"
git -C "$S/ctl-nobranch" update-ref -d refs/heads/master
echo '- **D4 correction (round 34 C2):** planted duplicate for the control' >> "$S/ctl-nobranch/SCORECARD.md"
mkdir -p "$S/notarepo" && echo x > "$S/notarepo/f.txt"

run() { local tag=$1 script=$2; shift 2; local log="$S/$tag.log"
  python3 "$script" "$@" >"$log" 2>&1; local rc=$?
  echo "## $tag rc=$rc"; grep -E '^(TIP|REF|REFUSE|rows=|LEDGER)' "$log" | cut -c1-200
  return $rc; }

# 1 detached clone: committed script false-reds (rc 1, 2 CRASHED pins) ...
run 01-before-det  "$COMMITTED" --source "$S/src-det" --work "$S/w1"; case $? in 1) ;; *) echo "  !! expected 1";; esac
# 2 ... the draft resolves the ref at the audited tip and reports it (rc 0, rows=9 … mismatches=0)
run 02-after-det   "$DRAFT"     --source "$S/src-det" --work "$S/w2"; case $? in 0) ;; *) echo "  !! expected 0";; esac
# 3/4 normal clone: unchanged bytes and exit code
run 03-before-norm "$COMMITTED" --source "$S/lane"    --work "$S/w3"
run 04-after-norm  "$DRAFT"     --source "$S/lane"    --work "$S/w4"
diff <(sed "s#$S/w3/#/W/#" "$S/03-before-norm.log") <(sed "s#$S/w4/#/W/#" "$S/04-after-norm.log") \
  && echo "## 05 normal-clone output IDENTICAL"
# 6/7 reuse refusal: the declared style-2 refusal used to exit 1
run 06-before-reuse "$COMMITTED" --source "$S/lane" --work "$S/w3"; case $? in 1) ;; *) echo "  !! expected 1";; esac
run 07-after-reuse  "$DRAFT"     --source "$S/lane" --work "$S/w4"; case $? in 2) ;; *) echo "  !! expected 2";; esac
# 8/9 a source that is not a git repository: traceback exit 1 -> one REFUSE line, exit 2
run 08-before-nonrepo "$COMMITTED" --source "$S/notarepo" --work "$S/w5"; case $? in 1) ;; *) echo "  !! expected 1";; esac
run 09-after-nonrepo  "$DRAFT"     --source "$S/notarepo" --work "$S/w6"; case $? in 2) ;; *) echo "  !! expected 2";; esac
# 10/11 control mode on a detached clone with no master ref: 3 mismatches -> only the planted one
run 10-before-ctl "$COMMITTED" --lane "$S/ctl-nobranch"; case $? in 1) ;; *) echo "  !! expected 1";; esac
run 11-after-ctl  "$DRAFT"     --lane "$S/ctl-nobranch"; case $? in 1) ;; *) echo "  !! expected 1";; esac
# 12 editing plans/defect_ledger.py instead: the gate's own genuine-package clause goes red
git clone -q --shared "$S/lane" "$S/editdg"
echo '# would resolve BRANCH at runtime' >> "$S/editdg/plans/defect_ledger.py"
python3 "$S/editdg/plans/pkg_gate.py" package --root "$S/editdg" --spec "$S/editdg/plans/pkg-spec-r35.json" \
  | grep -E '^P1' | cut -c1-140
echo "## tip=$TIP old=$OLD"
