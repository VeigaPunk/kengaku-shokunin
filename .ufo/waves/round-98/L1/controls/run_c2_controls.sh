#!/usr/bin/env bash
# R98-C2 prefreeze controls (round 98, L1 KengakuR98). Each control is a fixture clone of the lane at
# BASE under $S (never the lane), one fixture commit, then the counter from the lane. Receipts land in
# this directory as c2-<name>[-runN].txt with the counter's rc appended.
# Usage: run_c2_controls.sh <run-label> <provenance.md> <fixture-rev: the P1 commit>
set -u
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
BASE=49a1c4f1097db7c923da56d4213cad75772ed1c0
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r98/L1/c2ctl-$1
PROV=$2
FIXREV=$3
OUT=$L/.ufo/waves/round-98/L1/controls
mkdir -p "$S" "$OUT"
trap 'rm -rf -- "$S"' EXIT

fixture() {  # name -> prints fixture path, clean checkout of BASE
  local D=$S/$1
  rm -rf "$D"
  git clone -q --shared "$L" "$D"
  git -C "$D" -c advice.detachedHead=false checkout -q "$FIXREV"
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch $D" >&2; exit 3; }
  echo "$D"
}
commit() {  # dir msg
  git -C "$1" add -A corpus plans SKILL.md
  git -C "$1" -c user.name=fixture -c user.email=fixture@fixture.invalid commit -qm "$2"
}
measure() {  # name dir rev
  ( cd "$L" && python3 plans/round98_c2_nested_bind.py --lane "$2" --rev "$3" --work "$S/w-$1"; echo "rc=$?" ) \
    > "$OUT/c2-$1-$RUN.txt" 2>&1
  echo "$1: $(grep -E '^PREDICATE|^rc=' "$OUT/c2-$1-$RUN.txt" | tr '\n' ' ')"
}
RUN=$1

D=$(fixture do-nothing); measure do-nothing "$D" HEAD

D=$(fixture positive); cp "$PROV" "$D/corpus/evidence/PROVENANCE.md"; commit "$D" positive
measure positive "$D" HEAD

D=$(fixture partial); head -n -1 "$PROV" > "$D/corpus/evidence/PROVENANCE.md"; commit "$D" partial
measure partial "$D" HEAD

# row-edit forgery: every POP row's 64-hex token blanked out of SOURCES.md, no provenance file
D=$(fixture row-edit)
python3 - "$D" <<'EOF'
import importlib.util, sys
d = sys.argv[1]
spec = importlib.util.spec_from_file_location("c2", "/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round98_c2_nested_bind.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p = d + "/corpus/SOURCES.md"; t = open(p).read()
for tok, _ in m.POP.values():
    t = t.replace("sha256 " + tok, "sha256 elided").replace(tok, "elided")
open(p, "w").write(t)
EOF
commit "$D" row-edit; measure row-edit "$D" HEAD

# wrong-capture forgery: rows with a round-52 twin bound to the twin (same bytes, not the replay's capture)
D=$(fixture wrong-capture)
python3 - "$PROV" "$D" <<'EOF'
import os, re, sys
prov, d = sys.argv[1], sys.argv[2]
out = []
for line in open(prov):
    m = re.search(r"`(round(?:9\d)/graders/([^`]+))`", line)
    if m and os.path.isfile(f"{d}/corpus/evidence/round52/graders/{m.group(2)}"):
        line = line.replace(m.group(1), "round52/graders/" + m.group(2))
    out.append(line)
open(d + "/corpus/evidence/PROVENANCE.md", "w").write("".join(out))
EOF
commit "$D" wrong-capture; measure wrong-capture "$D" HEAD

# gate-edit forgery: provenance present (so only the gate bytes differ from positive), gate edited
D=$(fixture gate-edit); cp "$PROV" "$D/corpus/evidence/PROVENANCE.md"
python3 - "$D" <<'EOF'
import sys
p = sys.argv[1] + "/plans/anchor_digest_check.py"; t = open(p).read()
open(p, "w").write(t + "\n# forged: anchor-unbound silenced\n")
EOF
commit "$D" gate-edit; measure gate-edit "$D" HEAD

# capture-edit forgery: provenance present, one POP capture's bytes changed
D=$(fixture capture-edit); cp "$PROV" "$D/corpus/evidence/PROVENANCE.md"
printf '\n# forged\n' >> "$D/corpus/evidence/round97/graders/sparql-university/tests/test.sh"
commit "$D" capture-edit; measure capture-edit "$D" HEAD

# separability: C1 candidate bytes only (ledger, SKILL cells, SOURCES S326-S333, flat captures already at P0)
CAND=$(dirname "$PROV")
D=$(fixture c1only); cp "$CAND/SKILL.md" "$D/SKILL.md"; cp "$CAND/ledger.json" "$D/plans/grader-population-ledger.json"
cp "$CAND/SOURCES.md" "$D/corpus/SOURCES.md"; commit "$D" c1only; measure c1only "$D" HEAD

# both claims' candidate bytes
D=$(fixture both); cp "$CAND/SKILL.md" "$D/SKILL.md"; cp "$CAND/ledger.json" "$D/plans/grader-population-ledger.json"
cp "$CAND/SOURCES.md" "$D/corpus/SOURCES.md"; cp "$PROV" "$D/corpus/evidence/PROVENANCE.md"; commit "$D" both
measure both "$D" HEAD
