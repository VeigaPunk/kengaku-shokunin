#!/usr/bin/env bash
# R100 prefreeze controls (round 100, L1 KengakuR100). Every control is a fixture clone of the lane at the
# P1 commit under $S (never the lane). Each fixture first commits a fixture-only plans/round-100-claims.md
# carrying a frozen-instruments block of the P1 instrument bytes and a candidate-bytes block of the
# candidate files (so L3/L4/L8/L11/L12 and K1/K9/K10 resolve), then the control's bytes in one fixture
# commit; both counters run from the fixture root (they refuse another cwd).
# Q85 (round-99 lesson M2): every forgery prints `TREE-DIFF <name> vs <positive>: <n> paths` and the battery
# aborts unless n > 0; every step's exit status is checked (set -euo pipefail; counters' rc captured explicitly).
# Usage: run_controls.sh <run-label> <P1-rev> <grader venv>
set -euo pipefail
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
RUN=$1; P1=$2; G=$3
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/kengaku-r100/L1/ctl-$RUN
OUT=$L/.ufo/waves/round-100/L1/controls
CAND=$OUT/candidate
mkdir -p "$S" "$OUT"
trap 'rm -rf -- "$S"' EXIT
INSTR="plans/round100_fdp_probe.py plans/round100-cases.json plans/round100_c1_replay.py plans/round100_c2_rowcensus_bind.py plans/round100_provenance_build.py plans/round100_prefreeze_check.py plans/anchor_digest_check.py .ufo/waves/round-100/L1/c2-live-refetch.txt"
PROV="corpus/evidence/round52/PROVENANCE.md corpus/evidence/round58/PROVENANCE.md corpus/evidence/round94/PROVENANCE.md"

fixture() {
  local D=$S/$1
  rm -rf "$D"
  git clone -q --shared "$L" "$D"
  git -C "$D" -c advice.detachedHead=false checkout -q "$P1"
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch $D" >&2; exit 3; }
  { echo "# fixture-only freeze table (control $1, not the lane's claims file)"; echo; echo '```frozen-instruments'
    ( cd "$D" && sha256sum $INSTR ); echo '```'; echo; echo '```candidate-bytes'
    ( cd "$CAND" && printf '%s  SKILL.md\n' "$(sha256sum SKILL.md | cut -c1-64)"
      printf '%s  plans/grader-population-ledger.json\n' "$(sha256sum ledger.json | cut -c1-64)"
      printf '%s  corpus/SOURCES.md\n' "$(sha256sum SOURCES.md | cut -c1-64)"
      cd prov && sha256sum $PROV ); echo '```'; } > "$D/plans/round-100-claims.md"
  commit "$D" "fixture freeze"
  echo "$D"
}
commit() {
  git -C "$1" add -A corpus plans SKILL.md
  git -C "$1" -c user.name=fixture -c user.email=fixture@fixture.invalid commit -qm "$2"
}
treediff() {   # Q85: forgery $1 (dir) must differ from positive $2 (dir)
  git -C "$1" fetch -q "$2" HEAD
  local n; n=$(git -C "$1" diff --name-only FETCH_HEAD HEAD | wc -l)
  echo "TREE-DIFF $(basename "$1") vs $(basename "$2"): $n paths"
  [ "$n" -gt 0 ] || { echo "ABORT forgery $(basename "$1") equals $(basename "$2")" >&2; exit 4; }
}
receipt() {
  ( cd "$1" && python3 plans/round100_fdp_probe.py --lane . --work "$S/probe-$(basename "$1")" --grader-venv "$G" ) \
    > "$1/corpus/evidence/round100/fdp-probe.txt"
}
c1cand() {
  cp "$CAND/SKILL.md" "$1/SKILL.md"; cp "$CAND/ledger.json" "$1/plans/grader-population-ledger.json"
  cp "$CAND/SOURCES.md" "$1/corpus/SOURCES.md"
}
c2cand() { cp -r "$CAND/prov/corpus/." "$1/corpus/"; }
m1() {
  local rc=0
  ( cd "$2" && python3 plans/round100_c1_replay.py --lane . --rev HEAD --work "$S/w1-$1" --grader-venv "$G" ) \
    > "$OUT/c1-$1-$RUN.txt" 2>&1 || rc=$?
  echo "rc=$rc" >> "$OUT/c1-$1-$RUN.txt"
  echo "c1 $1: $(grep -E '^LEGS|^PREDICATE|^rc=' "$OUT/c1-$1-$RUN.txt" | tr '\n' ' ')"
}
m2() {
  local rc=0
  ( cd "$2" && python3 plans/round100_c2_rowcensus_bind.py --lane . --rev HEAD --work "$S/w2-$1" ) \
    > "$OUT/c2-$1-$RUN.txt" 2>&1 || rc=$?
  echo "rc=$rc" >> "$OUT/c2-$1-$RUN.txt"
  echo "c2 $1: $(grep -E '^LEGS|^PREDICATE|^rc=' "$OUT/c2-$1-$RUN.txt" | tr '\n' ' ')"
}

# ---------------- shared: do-nothing, c1only, c2only, both (each measured by both counters)
D=$(fixture do-nothing); m1 do-nothing "$D"; m2 do-nothing "$D"
D=$(fixture c1only); receipt "$D"; c1cand "$D"; commit "$D" c1only; m1 positive "$D"; m2 c1only "$D"; POS1=$D
D=$(fixture c2only); c2cand "$D"; commit "$D" c2only; m2 positive "$D"; m1 c2only "$D"; POS2=$D
D=$(fixture both); receipt "$D"; c1cand "$D"; c2cand "$D"; commit "$D" both; m1 both "$D"; m2 both "$D"
rc=0; ( cd "$D" && python3 plans/round100_prefreeze_check.py --lane . --base 7846037679de77d050141c785996471801e5a19a \
  --cand HEAD --work "$S/pf" ) > "$OUT/prefreeze-both-$RUN.txt" 2>&1 || rc=$?
echo "rc=$rc" >> "$OUT/prefreeze-both-$RUN.txt"; echo "prefreeze both: $(tail -2 "$OUT/prefreeze-both-$RUN.txt" | tr '\n' ' ')"

# ---------------- C1 forgeries (positive = c1only)
D=$(fixture extra-member); receipt "$D"; c1cand "$D"
python3 - "$D/plans/grader-population-ledger.json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
d["members"]["winning-avg-corewars"].update(status="executed", reason="replayed", round=100)
open(p, "w").write(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
EOF
commit "$D" extra-member; treediff "$D" "$POS1"; m1 extra-member "$D"

D=$(fixture forged-receipt); cp "$POS1/corpus/evidence/round100/fdp-probe.txt" "$D/corpus/evidence/round100/"
sed -i '0,/^DETAIL C03 /s/summary=[0-9a-f]*/summary=0000000000000000/' "$D/corpus/evidence/round100/fdp-probe.txt"
c1cand "$D"; commit "$D" forged-receipt; treediff "$D" "$POS1"; m1 forged-receipt "$D"

D=$(fixture receipt-identity); receipt "$D"
sed -i 's/^LANE_TIP .*/LANE_TIP 7846037679de77d050141c785996471801e5a19a/' "$D/corpus/evidence/round100/fdp-probe.txt"
c1cand "$D"; commit "$D" receipt-identity; treediff "$D" "$POS1"; m1 receipt-identity "$D"

D=$(fixture counter-edit); receipt "$D"; c1cand "$D"
printf '\n# forged after freeze\n' >> "$D/plans/round100_c1_replay.py"
commit "$D" counter-edit; treediff "$D" "$POS1"; m1 counter-edit "$D"

D=$(fixture extra-file); receipt "$D"; c1cand "$D"
mkdir -p "$D/corpus/knowledge"; printf 'not in the candidate table\n' > "$D/corpus/knowledge/zz-extra.md"
commit "$D" extra-file; treediff "$D" "$POS1"; m1 extra-file "$D"

D=$(fixture skill-cell); receipt "$D"; c1cand "$D"
sed -i 's/executed 35 of 76 (round 100 adds/executed 36 of 76 (round 100 adds/' "$D/SKILL.md"
commit "$D" skill-cell; treediff "$D" "$POS1"; m1 skill-cell "$D"

D=$(fixture extra-row); receipt "$D"; c1cand "$D"
python3 - "$D/corpus/SOURCES.md" <<'EOF'
import sys
p = sys.argv[1]; t = open(p).read()
row = [l for l in t.split("\n") if l.startswith("| S348 ")][0]
t = t.replace(row, row + "\n" + row.replace("| S348 ", "| S350 ", 1), 1)
open(p, "w").write(t)
EOF
commit "$D" extra-row; treediff "$D" "$POS1"; m1 extra-row "$D"

D=$(fixture typed-words); receipt "$D"; c1cand "$D"
sed -i '/^| S343 /s/(2 words)/(3 words)/' "$D/corpus/SOURCES.md"
commit "$D" typed-words; treediff "$D" "$POS1"; m1 typed-words "$D"

# ---------------- C2 forgeries (positive = c2only)
D=$(fixture partial); c2cand "$D"; rm -f "$D/corpus/evidence/round58/PROVENANCE.md"; commit "$D" partial
treediff "$D" "$POS2"; m2 partial "$D"

D=$(fixture url-channel); c2cand "$D"
printf '| S180 | `sources/tb2-readme.md` | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md |\n' \
  >> "$D/corpus/evidence/round52/PROVENANCE.md"
commit "$D" url-channel; treediff "$D" "$POS2"; m2 url-channel "$D"

D=$(fixture duplicate-line); c2cand "$D"
printf '| S210 | `graders/distribution-search/tests/test_outputs.py` | `02bca54db4849b7c911253fb92f941e21db8b1eea13261a7e5a9871fca68b4ed` |\n' \
  >> "$D/corpus/evidence/round52/PROVENANCE.md"
commit "$D" duplicate-line; treediff "$D" "$POS2"; m2 duplicate-line "$D"

D=$(fixture sha-column); c2cand "$D"
sed -i 's/`02bca54db4849b7c911253fb92f941e21db8b1eea13261a7e5a9871fca68b4ed`/`0000000000000000000000000000000000000000000000000000000000000000`/' \
  "$D/corpus/evidence/round52/PROVENANCE.md"
commit "$D" sha-column; treediff "$D" "$POS2"; m2 sha-column "$D"

D=$(fixture fabricated-id); c2cand "$D"
printf '| S999 | `graders/pypi-server/tests/test_outputs.py` | `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` |\n' \
  >> "$D/corpus/evidence/round52/PROVENANCE.md"
commit "$D" fabricated-id; treediff "$D" "$POS2"; m2 fabricated-id "$D"

D=$(fixture fourth-cell); c2cand "$D"
sed -i 's/^| S228 | \(.*\) |$/| S228 | \1 | raw.githubusercontent.com\/harbor-framework\/terminal-bench-2 |/' "$D/corpus/evidence/round52/PROVENANCE.md"
commit "$D" fourth-cell; treediff "$D" "$POS2"; m2 fourth-cell "$D"

D=$(fixture outside-rebind); c2cand "$D"
printf '| S236 | `graders/write-compressor/solution/solve.sh` | `01550b7de7ab1320b1898eae055226bb7c73bee259c75102d2240c974a730409` |\n' \
  >> "$D/corpus/evidence/round94/PROVENANCE.md"
commit "$D" outside-rebind; treediff "$D" "$POS2"; m2 outside-rebind "$D"

D=$(fixture outside-row-delete); c2cand "$D"
python3 - "$D" <<'EOF'
import subprocess, sys
d = sys.argv[1]
# delete one BASE row that carries no anchor-digest gate output at all (round-99 CriticClaims F6 / MutC2 M17)
out = subprocess.run([sys.executable, d + "/plans/anchor_digest_check.py", "--lane", d, "--verbose"],
                     capture_output=True, text=True, cwd=d).stdout
named = {w for line in out.splitlines() for w in line.split()[1:2]}
p = d + "/corpus/SOURCES.md"; lines = open(p).read().split("\n")
victim = next(l for l in lines if l.startswith("| S0") and l.split("|")[1].strip() not in named)
print("DELETED", victim.split("|")[1].strip())
open(p, "w").write("\n".join(l for l in lines if l != victim))
EOF
commit "$D" outside-row-delete; treediff "$D" "$POS2"; m2 outside-row-delete "$D"

D=$(fixture row-edit)
python3 - "$D" <<'EOF'
import importlib.util, sys
d = sys.argv[1]
spec = importlib.util.spec_from_file_location("c2", d + "/plans/round100_c2_rowcensus_bind.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p = d + "/corpus/SOURCES.md"; t = open(p).read()
for tok, _c, _u in m.POP.values():
    t = t.replace(tok, "elided")
open(p, "w").write(t)
EOF
commit "$D" row-edit; treediff "$D" "$POS2"; m2 row-edit "$D"

D=$(fixture gate-edit); c2cand "$D"; printf '\n# forged\n' >> "$D/plans/anchor_digest_check.py"; commit "$D" gate-edit
treediff "$D" "$POS2"; m2 gate-edit "$D"
D=$(fixture capture-edit); c2cand "$D"; printf '\n# forged\n' >> "$D/corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py"
commit "$D" capture-edit; treediff "$D" "$POS2"; m2 capture-edit "$D"
D=$(fixture c2counter-edit); c2cand "$D"; printf '\n# forged after freeze\n' >> "$D/plans/round100_c2_rowcensus_bind.py"
commit "$D" c2counter-edit; treediff "$D" "$POS2"; m2 c2counter-edit "$D"
D=$(fixture live-forged); c2cand "$D"
sed -i 's/^LIVE S228 http=200/LIVE S228 http=404/' "$D/.ufo/waves/round-100/L1/c2-live-refetch.txt"
git -C "$D" add -f .ufo/waves/round-100/L1/c2-live-refetch.txt; commit "$D" live-forged; treediff "$D" "$POS2"; m2 live-forged "$D"
D=$(fixture c2-extra-file); c2cand "$D"; printf 'stray\n' > "$D/corpus/evidence/round52/NOTES.md"
commit "$D" c2-extra-file; treediff "$D" "$POS2"; m2 c2-extra-file "$D"
echo "BATTERY $RUN complete"
