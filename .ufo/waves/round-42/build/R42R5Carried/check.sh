#!/bin/bash
# check.sh LANE [WORK] — red/green check for the round-41 R5 carried item:
#   round_close.py --selftest must be idempotent when --work names an existing directory.
# RED  (tip fda71ae, plans/round_close.py before the patch): run 2 exits 1 with a
#      CalledProcessError traceback from git commit "nothing to commit" (line 275 -> 241).
# GREEN (patch applied): run 1 rc 0, run 2 rc 0, run 2 stdout identical to run 1, no nested
#      corpus/knowledge/knowledge copy left by a second 'cp -a'.
# Always runs inside the host-safety bwrap envelope and prints the Q32 pre/post evidence.
set -u
lane=$(readlink -f "${1:?usage: check.sh LANE [WORK]}")
work=${2:-$(mktemp -d)}
census=${CENSUS:-/home/vgpnk/Projects/shokunin/scripts/sources-census.sh}
mkdir -p "$work"

q32_head() { date +%T; ls -A /home/vgpnk/.local/bin | sha256sum; }
run_selftest() {  # $1 = output file; rc in $?
  env HOME="${HOME_SCRATCH:-$work/home}" \
      PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    bwrap --dev-bind / / \
          --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
          --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent \
      python3 "$lane/plans/round_close.py" --lane "$lane" --census "$census" \
              --selftest --work "$work" >"$1" 2>&1
}

q32_head
run_selftest "$work/run1.out"; rc1=$?
run_selftest "$work/run2.out"; rc2=$?
q32_head

echo "CHECK lane=$lane work=$work"
echo "CHECK run1_rc=$rc1 run2_rc=$rc2"
echo "CHECK run1=$(grep -c '^SELFTEST case=' "$work/run1.out") cases; tail: $(tail -1 "$work/run1.out")"
echo "CHECK run2_tail: $(tail -1 "$work/run2.out")"

fail=0
[ "$rc1" -eq 0 ] || { echo "CHECK FAIL run 1 exit=$rc1"; fail=1; }
[ "$rc2" -eq 0 ] || { echo "CHECK FAIL run 2 exit=$rc2 (rerun on an existing --work)"; grep -m1 'CalledProcessError' "$work/run2.out"; fail=1; }
cmp -s "$work/run1.out" "$work/run2.out" || { echo "CHECK FAIL run 2 output differs from run 1"; diff "$work/run1.out" "$work/run2.out" | sed -n '1,20p'; fail=1; }
[ -d "$work/A-excused-p10/corpus/knowledge/knowledge" ] && { echo "CHECK FAIL nested corpus/knowledge/knowledge from a second 'cp -a'"; fail=1; }
[ "$fail" -eq 0 ] && echo "CHECK PASS rc=0 twice, identical output, no nested copy"
exit "$fail"
