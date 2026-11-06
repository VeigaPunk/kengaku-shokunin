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

# ---------------- shared: do-nothing, c1only, c2only, both (each measured by both counters)
D=$(fixture do-nothing); m1 do-nothing "$D"; m2 do-nothing "$D"
D=$(fixture c1only); receipt "$D"; c1cand "$D"; commit "$D" c1only; m1 positive "$D"; m2 c1only "$D"; POS=$D
D=$(fixture c2only); c2cand "$D"; commit "$D" c2only; m2 positive "$D"; m1 c2only "$D"
D=$(fixture both); receipt "$D"; c1cand "$D"; c2cand "$D"; commit "$D" both; m1 both "$D"; m2 both "$D"

# ---------------- C1 forgeries
D=$(fixture extra-member); receipt "$D"; c1cand "$D"
python3 - "$D/plans/grader-population-ledger.json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
d["members"]["crack-7z-hash"].update(status="executed", reason="replayed", round=99)
open(p, "w").write(json.dumps(d, indent=1) + "\n")
EOF
commit "$D" extra-member; m1 extra-member "$D"

D=$(fixture forged-receipt); cp "$POS/corpus/evidence/round99/bnfit-probe.txt" "$D/corpus/evidence/round99/"
sed -i '0,/^DETAIL C03 /s/final=[0-9a-f]*/final=0000000000000000/' "$D/corpus/evidence/round99/bnfit-probe.txt"
c1cand "$D"; commit "$D" forged-receipt; m1 forged-receipt "$D"

D=$(fixture counter-edit); receipt "$D"; c1cand "$D"
printf '\n# forged after freeze\n' >> "$D/plans/round99_c1_replay.py"
commit "$D" counter-edit; m1 counter-edit "$D"

# ---------------- C2 forgeries
# partial: one of the eight new files absent (round95 -> S306 stays unbound). Runs 1-2 used `git rm` on the
# still-untracked copy, which failed ("pathspec did not match"), so that fixture equalled positive and passed;
# fixed to rm -f and re-run as partial-fixed-run{1,2} (lesson M2).
D=$(fixture partial); c2cand "$D"; rm -f "$D/corpus/evidence/round95/PROVENANCE.md"; commit "$D" partial; m2 partial "$D"

# URL channel: positive plus a round-98-style URL column on one new file (the side channel K3 forbids)
D=$(fixture url-channel); c2cand "$D"
printf '| S180 | `sources/tb2-readme.md` | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md |\n' \
  >> "$D/corpus/evidence/round79/PROVENANCE.md"
commit "$D" url-channel; m2 url-channel "$D"

# duplicate binding: a second line binds S180 to its byte-identical round-82 copy (round-98 MutC2 M11/M16)
D=$(fixture duplicate-line); c2cand "$D"
printf '| S180 | `fetch/candidate_README.md` | `7dfa9992c45c7e30744cda7ce659ba77309f43120a0990fce033eb8afd972364` |\n' \
  >> "$D/corpus/evidence/round82/PROVENANCE.md"
commit "$D" duplicate-line; m2 duplicate-line "$D"

# sha column wrong on one line (round-98 MutC2 M05/M18: sha column was unread)
D=$(fixture sha-column); c2cand "$D"
sed -i 's/`39ce8d137a30e1fd80eeae146b1c424e56f688f4ddd001259eb98543d3209439`/`0000000000000000000000000000000000000000000000000000000000000000`/' \
  "$D/corpus/evidence/round50/PROVENANCE.md"
commit "$D" sha-column; m2 sha-column "$D"

# outside re-bind: positive plus a line binding a non-population row (S210) to a capture
D=$(fixture outside-rebind); c2cand "$D"
printf '| S210 | `tb2-openssl-selfsigned-cert/solution/solve.sh` | `58cf3c844e907745cd81fb4bd75efb3d080e2f0e82b589c56c954ae6e1756510` |\n' \
  >> "$D/corpus/evidence/round59/PROVENANCE.md"
commit "$D" outside-rebind; m2 outside-rebind "$D"

# row-edit forgery: POP tokens blanked out of SOURCES.md, no provenance
D=$(fixture row-edit)
python3 - "$D" <<'EOF'
import importlib.util, sys
d = sys.argv[1]
spec = importlib.util.spec_from_file_location("c2", d + "/plans/round99_c2_rowscoped_bind.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p = d + "/corpus/SOURCES.md"; t = open(p).read()
for tok, _ in m.POP.values():
    t = t.replace(tok, "elided")
open(p, "w").write(t)
EOF
commit "$D" row-edit; m2 row-edit "$D"

D=$(fixture gate-edit); c2cand "$D"; printf '\n# forged\n' >> "$D/plans/anchor_digest_check.py"; commit "$D" gate-edit; m2 gate-edit "$D"
D=$(fixture capture-edit); c2cand "$D"; printf '\n# forged\n' >> "$D/corpus/evidence/round50/git-fetch.adoc"; commit "$D" capture-edit; m2 capture-edit "$D"
D=$(fixture c2counter-edit); c2cand "$D"; printf '\n# forged after freeze\n' >> "$D/plans/round99_c2_rowscoped_bind.py"; commit "$D" c2counter-edit; m2 c2counter-edit "$D"
