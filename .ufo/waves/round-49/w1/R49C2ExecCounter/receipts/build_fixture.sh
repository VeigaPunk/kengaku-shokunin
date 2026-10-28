#!/usr/bin/env bash
# Scratch-only fixture builder for seat R49C2ExecCounter. Nothing here is committed to the lane; the clone
# lives under /fast/scratch/hyaku/kengaku-r49/R49C2ExecCounter and every history it writes is local.
set -euo pipefail
S=/fast/scratch/hyaku/kengaku-r49/R49C2ExecCounter
L=/home/vgpnk/Projects/shokunin/kengaku-shokunin
FREEZE=9d2900af41e4d1fc6022eff99010436fde6dbd93
export TMPDIR=$S
cd "$S"
rm -rf fixture work-*
git clone --shared "$L" fixture >/dev/null 2>&1
cd fixture
test "$(git rev-parse --show-toplevel)" = "$PWD"
git checkout -q -b wave "$FREEZE"
mkdir -p corpus/evidence/round49 plans/mutants49 .ufo/waves/round-49/claims
cp plans/pkg-spec-r46.json plans/pkg-spec-r49.json
cp corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt corpus/evidence/round49/polyglot-c-py-dry-cases.txt
cp corpus/evidence/round46/polyglot-c-py-probe.txt corpus/evidence/round49/polyglot-c-py-probe.txt
python3 - <<'PY'
import json, pathlib
p = pathlib.Path("plans/pkg-spec-r49.json")
s = json.loads(p.read_text())
s["name"] = "round-49 tb2-polyglot-c-py package (seat fixture: shape only, not an admission)"
s["receipt"] = "corpus/evidence/round49/polyglot-c-py-probe.txt"
s["receipt_sha256"] = "PENDING-STAGE-2"
s["dry"] = "corpus/evidence/round49/polyglot-c-py-dry-cases.txt"
p.write_text(json.dumps(s, indent=1) + "\n")
PY
M=plans/mutants49
sed 's/^CASE nop predicted=fail observed=fail/CASE nop predicted=fail observed=pass/' \
    corpus/evidence/round49/polyglot-c-py-probe.txt > $M/receipt-observed-flip.payload
sed 's/^| `nop` | F | fail |/| `nop` | F | pass |/' \
    corpus/knowledge/tb2-polyglot-c-py-grader.md > $M/entry-case-row.payload
sed 's/"sha256": "b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec"/"sha256": "c94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec"/' \
    plans/pkg-spec-r49.json > $M/spec-anchor-digest.payload
{ cat corpus/evidence/round46/tb2-polyglot-c-py/instruction.md; printf '\n'; } > $M/capture-instruction.payload
{ cat corpus/evidence/round49/polyglot-c-py-probe.txt; printf '# noop trailing comment, measures nothing\n'; } \
    > $M/noop-receipt-comment.payload
python3 - <<'PY'
import json, hashlib, pathlib
m = pathlib.Path("plans/mutants49")
plan = {"mutants": [
 {"name": "receipt-observed-flip", "target": "corpus/evidence/round49/polyglot-c-py-probe.txt",
  "payload": "plans/mutants49/receipt-observed-flip.payload",
  "sha256": hashlib.sha256((m/"receipt-observed-flip.payload").read_bytes()).hexdigest(),
  "description": "one receipt case's observed verdict flipped"},
 {"name": "entry-case-row", "target": "corpus/knowledge/tb2-polyglot-c-py-grader.md",
  "payload": "plans/mutants49/entry-case-row.payload",
  "sha256": hashlib.sha256((m/"entry-case-row.payload").read_bytes()).hexdigest(),
  "description": "one ## Case table row's observed verdict flipped"},
 {"name": "spec-anchor-digest", "target": "plans/pkg-spec-r49.json",
  "payload": "plans/mutants49/spec-anchor-digest.payload",
  "sha256": hashlib.sha256((m/"spec-anchor-digest.payload").read_bytes()).hexdigest(),
  "description": "one spec row's anchor sha256 changed: the spec pin refuses the mutant"},
 {"name": "capture-instruction", "target": "corpus/evidence/round46/tb2-polyglot-c-py/instruction.md",
  "payload": "plans/mutants49/capture-instruction.payload",
  "sha256": hashlib.sha256((m/"capture-instruction.payload").read_bytes()).hexdigest(),
  "description": "a capture gains a trailing line"},
 {"name": "noop-receipt-comment", "target": "corpus/evidence/round49/polyglot-c-py-probe.txt",
  "payload": "plans/mutants49/noop-receipt-comment.payload",
  "sha256": hashlib.sha256((m/"noop-receipt-comment.payload").read_bytes()).hexdigest(),
  "description": "a receipt gains a comment line: measures nothing"},
]}
(m/"plan.json").write_text(json.dumps(plan, indent=1) + "\n")
PY
python3 "$S/fill.py" "$PWD" "$S/candidate.py" plans/round49_c2_verify.py 2
for c in base filler echo; do
  python3 plans/round49_c2_verify.py --lane . --control "$c" --work "$S/work-ctl-$c" \
      > ".ufo/waves/round-49/claims/control-c2-$c.txt" 2>&1 || true
done
git add plans/round49_c2_verify.py plans/pkg-spec-r49.json \
        corpus/evidence/round49/polyglot-c-py-dry-cases.txt plans/mutants49 .ufo/waves/round-49/claims
git -c user.name=R49C2ExecCounter -c user.email=seat@scratch.local commit -q \
    -m "r49-c2 fixture: stage 2 (counter + pins + dry table + mutants + control receipts)"
STAGE2=$(git rev-parse HEAD)
python3 - <<'PY'
import hashlib, json, pathlib
rel = "corpus/evidence/round49/polyglot-c-py-probe.txt"
p = pathlib.Path("plans/pkg-spec-r49.json"); s = json.loads(p.read_text())
s["receipt_sha256"] = hashlib.sha256(pathlib.Path(rel).read_bytes()).hexdigest()
p.write_text(json.dumps(s, indent=1) + "\n")
PY
git add plans/pkg-spec-r49.json corpus/evidence/round49/polyglot-c-py-probe.txt
git -c user.name=R49C2ExecCounter -c user.email=seat@scratch.local commit -q \
    -m "r49-c2 fixture: stage 3 (fresh receipt + its pin)"
STAGE3=$(git rev-parse HEAD)
echo "stage2=$STAGE2 stage3=$STAGE3"

# ---- ordering-rule variants: each is a branch whose history breaks exactly one clause -------------------
mix() {  # copy the stage-2/stage-3 content into the current (freeze-based) branch
  git checkout -q "$STAGE3" -- plans/round49_c2_verify.py plans/pkg-spec-r49.json \
      corpus/evidence/round49 plans/mutants49 .ufo/waves/round-49/claims
}
# (b) receipt lands in the same commit as the stage-2 counter
git checkout -q -b same-commit "$FREEZE"
mix
git -c user.name=R49C2ExecCounter -c user.email=seat@scratch.local commit -q -m "fixture variant: one commit"
# (c) receipt lands before the stage-2 counter
git checkout -q -b early-receipt "$FREEZE"
git checkout -q "$STAGE3" -- plans/pkg-spec-r49.json corpus/evidence/round49/polyglot-c-py-probe.txt
git -c user.name=R49C2ExecCounter -c user.email=seat@scratch.local commit -q -m "fixture variant: receipt first"
git checkout -q "$STAGE3" -- plans/round49_c2_verify.py corpus/evidence/round49/polyglot-c-py-dry-cases.txt \
    plans/mutants49 .ufo/waves/round-49/claims
git -c user.name=R49C2ExecCounter -c user.email=seat@scratch.local commit -q -m "fixture variant: stage 2 after"
# (d) stage 3 lands the receipt without its pin
git checkout -q -b no-pin "$STAGE2"
git checkout -q "$STAGE3" -- corpus/evidence/round49/polyglot-c-py-probe.txt
python3 - <<'PY'
import json, pathlib
p = pathlib.Path("plans/pkg-spec-r49.json"); s = json.loads(p.read_text())
s["receipt_sha256"] = "PENDING-STAGE-2"; p.write_text(json.dumps(s, indent=1) + "\n")
PY
git add plans/pkg-spec-r49.json corpus/evidence/round49/polyglot-c-py-probe.txt
git -c user.name=R49C2ExecCounter -c user.email=seat@scratch.local commit -q -m "fixture variant: stage 3, pin pending"
# (e) the stage-3 receipt is the dry table echoed (no observed= lines), pin coherent
git checkout -q -b echo-receipt "$STAGE2"
cp corpus/evidence/round49/polyglot-c-py-dry-cases.txt corpus/evidence/round49/polyglot-c-py-probe.txt
python3 - <<'PY'
import hashlib, json, pathlib
p = pathlib.Path("plans/pkg-spec-r49.json"); s = json.loads(p.read_text())
s["receipt_sha256"] = hashlib.sha256(pathlib.Path("corpus/evidence/round49/polyglot-c-py-probe.txt").read_bytes()).hexdigest()
p.write_text(json.dumps(s, indent=1) + "\n")
PY
git add plans/pkg-spec-r49.json corpus/evidence/round49/polyglot-c-py-probe.txt
git -c user.name=R49C2ExecCounter -c user.email=seat@scratch.local commit -q -m "fixture variant: echo receipt"
# (f) a receipt edited AFTER its stage-3 landing commit
git checkout -q -b edited-after "$STAGE3"
sed 's/^CASE nop predicted=fail observed=fail/CASE nop predicted=fail observed=pass/' \
    corpus/evidence/round49/polyglot-c-py-probe.txt > "$S/.edited" && mv "$S/.edited" corpus/evidence/round49/polyglot-c-py-probe.txt
git add corpus/evidence/round49/polyglot-c-py-probe.txt
git -c user.name=R49C2ExecCounter -c user.email=seat@scratch.local commit -q -m "fixture variant: receipt edited after landing"
# (g) two tags get violating cases: V7's tag rule passes, the map-row rule still needs the stage-2 entry repair
git checkout -q -b v7-tags "$STAGE2"
git checkout -q "$STAGE3" -- corpus/evidence/round49/polyglot-c-py-probe.txt
python3 - <<'PY'
import hashlib, json, pathlib
p = pathlib.Path("corpus/evidence/round49/polyglot-c-py-probe.txt")
lines = p.read_text().splitlines(True)
out = []
for line in lines:
    if line.startswith("CASE oracle-solve-sh ") or line.startswith("CASE trailing-ws "):
        line = line.replace(" violates= ", " violates=both-print,toolchain ", 1)
    out.append(line)
p.write_text("".join(out))
spec = pathlib.Path("plans/pkg-spec-r49.json"); s = json.loads(spec.read_text())
s["receipt_sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
spec.write_text(json.dumps(s, indent=1) + "\n")
PY
git add plans/pkg-spec-r49.json corpus/evidence/round49/polyglot-c-py-probe.txt
git -c user.name=R49C2ExecCounter -c user.email=seat@scratch.local commit -q -m "fixture variant: both-print/toolchain violated"
# (h) a committed control receipt carries a P10 line (the round-46 V8 class)
git checkout -q -b p10-receipt "$STAGE3"
printf 'gate: P10 DEFECT fresh probe exit=2\n' >> .ufo/waves/round-49/claims/control-c2-echo.txt
git add .ufo/waves/round-49/claims/control-c2-echo.txt
git -c user.name=R49C2ExecCounter -c user.email=seat@scratch.local commit -q -m "fixture variant: control receipt shows P10"
# (i) a committed control receipt carries an executed-probe CASE line
git checkout -q -b observed-receipt "$STAGE3"
printf 'CASE nop predicted=fail observed=pass tests=F predicted_tests=F match=no regrade=same violates=single-file\n' \
    >> .ufo/waves/round-49/claims/control-c2-base.txt
git add .ufo/waves/round-49/claims/control-c2-base.txt
git -c user.name=R49C2ExecCounter -c user.email=seat@scratch.local commit -q -m "fixture variant: control receipt shows an executed case"
git checkout -q wave
echo "branches: $(git branch --format='%(refname:short)' | tr '\n' ' ')"
