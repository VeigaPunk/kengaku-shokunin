#!/usr/bin/env bash
# R98-C1 prefreeze controls (round 98, L1 KengakuR98). Fixture clones of the lane at the P1 commit
# under $S (never the lane). Each fixture gets a fixture-only plans/round-98-claims.md carrying the
# frozen-instruments block of the P1 bytes (so L4/L8 can resolve), then the control's bytes, then the
# counter is run from the fixture root (the counter refuses any other cwd).
# Usage: run_c1_controls.sh <run-label> <P1-rev> <candidate dir with SKILL.md ledger.json SOURCES.md PROVENANCE.md> <grader venv>
set -u
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
RUN=$1; P1=$2; CAND=$3; G=$4
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r98/L1/c1ctl-$RUN
OUT=$L/.ufo/waves/round-98/L1/controls
mkdir -p "$S" "$OUT"
trap 'rm -rf -- "$S"' EXIT
INSTR="plans/round98_regexchess_probe.py plans/round98-cases.json plans/round98_c1_replay.py plans/round98_c2_nested_bind.py plans/round98_provenance_build.py"

fixture() {
  local D=$S/$1
  rm -rf "$D"
  git clone -q --shared "$L" "$D"
  git -C "$D" -c advice.detachedHead=false checkout -q "$P1"
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch $D" >&2; exit 3; }
  { echo "# fixture-only freeze table (control $1, not the lane's claims file)"; echo; echo '```frozen-instruments'
    ( cd "$D" && sha256sum $INSTR ); echo '```'; } > "$D/plans/round-98-claims.md"
  commit "$D" "fixture freeze"
  echo "$D"
}
commit() {
  git -C "$1" add -A corpus plans SKILL.md
  git -C "$1" -c user.name=fixture -c user.email=fixture@fixture.invalid commit -qm "$2"
}
receipt() {  # dir: official-style probe run at the fixture's freeze commit
  ( cd "$1" && python3 plans/round98_regexchess_probe.py --lane . --work "$S/probe-$(basename "$1")" --grader-venv "$G" ) \
    > "$1/corpus/evidence/round98/regexchess-probe.txt"
}
c1cand() {  # dir: C1 candidate bytes
  cp "$CAND/SKILL.md" "$1/SKILL.md"; cp "$CAND/ledger.json" "$1/plans/grader-population-ledger.json"
  cp "$CAND/SOURCES.md" "$1/corpus/SOURCES.md"
}
measure() {  # name dir
  ( cd "$2" && python3 plans/round98_c1_replay.py --lane . --rev HEAD --work "$S/w-$1" --grader-venv "$G"; echo "rc=$?" ) \
    > "$OUT/c1-$1-$RUN.txt" 2>&1
  echo "$1: $(grep -E '^LEGS|^PREDICATE|^rc=' "$OUT/c1-$1-$RUN.txt" | tr '\n' ' ')"
}

D=$(fixture do-nothing); measure do-nothing "$D"

D=$(fixture positive); receipt "$D"; c1cand "$D"; commit "$D" positive; measure positive "$D"
POS=$D

# extra unearned member: positive plus one more ledger member flipped to executed (round-97 MutC1)
D=$(fixture extra-member); receipt "$D"; c1cand "$D"
python3 - "$D/plans/grader-population-ledger.json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
d["members"]["crack-7z-hash"].update(status="executed", reason="replayed", round=98)
json.dump(d, open(p, "w"), indent=1)
EOF
commit "$D" extra-member; measure extra-member "$D"

# forged receipt: the positive receipt with one DETAIL line's digest altered (observations not reproduced)
D=$(fixture forged-receipt); cp "$POS/corpus/evidence/round98/regexchess-probe.txt" "$D/corpus/evidence/round98/"
sed -i '0,/^DETAIL C09 /s/sha=[0-9a-f]*/sha=0000000000000000/' "$D/corpus/evidence/round98/regexchess-probe.txt"
c1cand "$D"; commit "$D" forged-receipt; measure forged-receipt "$D"

# separability: only the C2 candidate (PROVENANCE.md) on top of the freeze
D=$(fixture c2only); cp "$CAND/PROVENANCE.md" "$D/corpus/evidence/PROVENANCE.md"; commit "$D" c2only; measure c2only "$D"

# both claims: C1 candidate + receipt + C2 candidate
D=$(fixture both); receipt "$D"; c1cand "$D"; cp "$CAND/PROVENANCE.md" "$D/corpus/evidence/PROVENANCE.md"
commit "$D" both; measure both "$D"
