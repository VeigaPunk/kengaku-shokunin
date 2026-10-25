#!/usr/bin/env bash
# R35RevLedger fixture verification of plans/defect_ledger.py (read-only w.r.t. the lane).
set -u
LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
D=$(mktemp -d /tmp/k35-XXXX)
git clone -q --no-checkout --shared "$LANE" "$D/lane" || exit 9
git -C "$D/lane" sparse-checkout set --no-cone "SCORECARD.md" "corpus" "plans" \
  ".ufo/waves/round-34/assimilation/captures/tb2-eval" \
  ".ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html" \
  ".ufo/waves/round-34/build/R34C2CounterDraft.md" \
  ".ufo/waves/round-34/build/R34MutC2Harness.md" || exit 9
git -C "$D/lane" checkout -q master || exit 9
T=$(git -C "$D/lane" rev-parse --show-toplevel)
[ "$T" = "$D/lane" ] || { echo "TOPLEVEL MISMATCH: $T"; exit 9; }
echo "fixture=$D toplevel=$T tip=$(git -C "$D/lane" rev-parse master)"

run() { echo "--- $1"; (cd "$D/lane" && python3 plans/defect_ledger.py --lane . 2>&1; echo "exit=$?"); }

echo "=== T0 baseline (fresh clone, committed state only)"
run T0

echo "=== T1 D1: untracked file inside round-34 scope"
touch "$D/lane/.ufo/waves/round-34/STRAY.txt"
run T1
rm "$D/lane/.ufo/waves/round-34/STRAY.txt"

echo "=== T2 D1 scope gap: untracked OUT of scope + tracked-modified in scope"
touch "$D/lane/STRAY-ROOT.txt"
cp "$D/lane/SCORECARD.md" "$D/lane/SCORECARD.bak"
printf '\nstray edit\n' >> "$D/lane/SCORECARD.md"
run T2
mv "$D/lane/SCORECARD.bak" "$D/lane/SCORECARD.md"
rm "$D/lane/STRAY-ROOT.txt"

echo "=== T3 D3: working-tree-only manifest repair (committed manifest still 4 lines)"
EV="$D/lane/.ufo/waves/round-34/assimilation/captures/tb2-eval"
cp "$EV/SHA256SUMS" "$EV/SHA256SUMS.bak"
H1=$(sha256sum "$EV/test_outputs.py" | cut -d' ' -f1)
H2=$(sha256sum "$EV/test.sh" | cut -d' ' -f1)
printf '%s  test_outputs.py\n%s  test.sh\n' "$H1" "$H2" >> "$EV/SHA256SUMS"
echo "committed manifest lines: $(git -C "$D/lane" show master:.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS | wc -l)"
run T3

echo "=== T4 D3: corrupted digest"
printf '0000000000000000000000000000000000000000000000000000000000000000  test_outputs.py\n' > "$EV/SHA256SUMS"
printf '%s  antibody.fasta\n' "$(sha256sum "$EV/antibody.fasta" | cut -d' ' -f1)" >> "$EV/SHA256SUMS"
run T4
mv "$EV/SHA256SUMS.bak" "$EV/SHA256SUMS"

echo "=== T5 D4: correction line missing one required term, then complete, then duplicated"
cp "$D/lane/SCORECARD.md" "$D/lane/SCORECARD.bak"
printf -- '- **D4 correction (round 34 C2):** the red selftest was the mutation harness (R34MutC2Harness.md:12, SELFTEST green failed), not the counter draft.\n' >> "$D/lane/SCORECARD.md"
run T5a
mv "$D/lane/SCORECARD.bak" "$D/lane/SCORECARD.md"
cp "$D/lane/SCORECARD.md" "$D/lane/SCORECARD.bak"
printf -- '- **D4 correction (round 34 C2):** the red selftest was the mutation harness (R34MutC2Harness.md:12, SELFTEST green failed), not the counter draft (R34C2CounterDraft.md:8, cases=10 failed=0).\n' >> "$D/lane/SCORECARD.md"
run T5b
printf -- '- **D4 correction (round 34 C2):** duplicate line (R34C2CounterDraft.md:8, cases=10 failed=0, R34MutC2Harness.md:12, SELFTEST green failed).\n' >> "$D/lane/SCORECARD.md"
run T5c
mv "$D/lane/SCORECARD.bak" "$D/lane/SCORECARD.md"

echo "=== T6 D5: erratum without round-35 Mistakes row; then with; then two errata"
cp "$D/lane/corpus/lessons/round-34.md" "$D/lane/corpus/lessons/round-34.bak"
printf -- 'Erratum (round 35): the S091 refusal reason "quote absent" is false; the quote is present in nec-s091-reopen.html.\n' >> "$D/lane/corpus/lessons/round-34.md"
run T6a
mkdir -p "$D/lane/corpus/lessons"
printf -- '## Mistakes\n\n| mistake | fix |\n|---|---|\n| S091 refused on a false reason | re-grounded from nec-s091-reopen.html |\n' > "$D/lane/corpus/lessons/round-35.md"
run T6b
printf -- 'Erratum (round 35): second erratum line mentioning nec-s091-reopen.html and present.\n' >> "$D/lane/corpus/lessons/round-34.md"
run T6c
mv "$D/lane/corpus/lessons/round-34.bak" "$D/lane/corpus/lessons/round-34.md"
rm "$D/lane/corpus/lessons/round-35.md"

echo "=== T7 flip all statuses to closed (reproduce control-c2-flip in fixture)"
cp "$D/lane/corpus/defects.jsonl" "$D/lane/corpus/defects.jsonl.bak"
python3 - "$D/lane/corpus/defects.jsonl" <<'EOF'
import json,sys
p=sys.argv[1]
rows=[json.loads(l) for l in open(p) if l.strip()]
for r in rows: r["status"]="closed"
open(p,"w").write("".join(json.dumps(r)+"\n" for r in rows))
EOF
run T7
mv "$D/lane/corpus/defects.jsonl.bak" "$D/lane/corpus/defects.jsonl"

echo "=== T8 unknown check name, status=open"
python3 - "$D/lane/corpus/defects.jsonl" <<'EOF'
import json,sys
p=sys.argv[1]
rows=[json.loads(l) for l in open(p) if l.strip()]
rows[0]["check"]="nope"
open(p,"w").write("".join(json.dumps(r)+"\n" for r in rows))
EOF
run T8

echo "=== T9 status typo 'Closed'"
python3 - "$D/lane/corpus/defects.jsonl" <<'EOF'
import json,sys
p=sys.argv[1]
rows=[json.loads(l) for l in open(p) if l.strip()]
for r in rows: r["status"]="Closed"; r["check"]="r34_d1"
open(p,"w").write("".join(json.dumps(r)+"\n" for r in rows))
EOF
run T9

echo "=== T10 malformed JSON line"
printf 'not-json\n' >> "$D/lane/corpus/defects.jsonl"
run T10

echo "=== T11 missing defects.jsonl"
mv "$D/lane/corpus/defects.jsonl" /tmp/k35-defects.jsonl.bak
run T11
mv /tmp/k35-defects.jsonl.bak "$D/lane/corpus/defects.jsonl"

echo "=== T12 empty ledger"
: > "$D/lane/corpus/defects.jsonl"
run T12

echo "=== T13 D2 edge: nonexistent root pathspec"
git -C "$D/lane" ls-tree -r --name-only master -- no/such/dir | wc -l
echo "exit=$?"

rm -rf "$D"
echo "=== fixture removed"
