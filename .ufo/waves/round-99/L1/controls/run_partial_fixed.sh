#!/usr/bin/env bash
# R99 prefreeze controls (round 99, L1 KengakuR99). Every control is a fixture clone of the lane at the
# P1 commit under $S (never the lane). Each fixture first gets a fixture-only plans/round-99-claims.md
# carrying a frozen-instruments block of the P1 instrument bytes (so L4/L8/L11 and K1 resolve), then the
# control's bytes in one fixture commit; both counters run from the fixture root (they refuse other cwd).
# Usage: run_controls.sh <run-label> <P1-rev> <grader venv>
set -u
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
RUN=$1; P1=$2; G=$3
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r99/L1/ctl-$RUN
OUT=$L/.ufo/waves/round-99/L1/controls
CAND=$OUT/candidate
mkdir -p "$S" "$OUT"
trap 'rm -rf -- "$S"' EXIT
INSTR="plans/round99_bnfit_probe.py plans/round99-cases.json plans/round99_c1_replay.py plans/round99_c2_rowscoped_bind.py plans/round99_provenance_build.py plans/anchor_digest_check.py"

fixture() {
  local D=$S/$1
  rm -rf "$D"
  git clone -q --shared "$L" "$D"
  git -C "$D" -c advice.detachedHead=false checkout -q "$P1"
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch $D" >&2; exit 3; }
  { echo "# fixture-only freeze table (control $1, not the lane's claims file)"; echo; echo '```frozen-instruments'
    ( cd "$D" && sha256sum $INSTR ); echo '```'; } > "$D/plans/round-99-claims.md"
  commit "$D" "fixture freeze"
  echo "$D"
}
commit() {
  git -C "$1" add -A corpus plans SKILL.md
  git -C "$1" -c user.name=fixture -c user.email=fixture@fixture.invalid commit -qm "$2"
}
receipt() {
  ( cd "$1" && python3 plans/round99_bnfit_probe.py --lane . --work "$S/probe-$(basename "$1")" --grader-venv "$G" ) \
    > "$1/corpus/evidence/round99/bnfit-probe.txt"
}
c1cand() {
  cp "$CAND/SKILL.md" "$1/SKILL.md"; cp "$CAND/ledger.json" "$1/plans/grader-population-ledger.json"
  cp "$CAND/SOURCES.md" "$1/corpus/SOURCES.md"
}
c2cand() { cp -r "$CAND/prov/corpus/." "$1/corpus/"; }
m1() {
  ( cd "$2" && python3 plans/round99_c1_replay.py --lane . --rev HEAD --work "$S/w1-$1" --grader-venv "$G"; echo "rc=$?" ) \
    > "$OUT/c1-$1-$RUN.txt" 2>&1
  echo "c1 $1: $(grep -E '^LEGS|^PREDICATE|^rc=' "$OUT/c1-$1-$RUN.txt" | tr '\n' ' ')"
}
m2() {
  ( cd "$2" && python3 plans/round99_c2_rowscoped_bind.py --lane . --rev HEAD --work "$S/w2-$1"; echo "rc=$?" ) \
    > "$OUT/c2-$1-$RUN.txt" 2>&1
  echo "c2 $1: $(grep -E '^LEGS|^PREDICATE|^rc=' "$OUT/c2-$1-$RUN.txt" | tr '\n' ' ')"
}

# re-run of the C2 partial control only (runs 1-2 of run_controls.sh had a harness defect, lesson M2)
D=$(fixture partial-fixed); c2cand "$D"; rm -f "$D/corpus/evidence/round95/PROVENANCE.md"; commit "$D" partial-fixed; m2 partial-fixed "$D"
