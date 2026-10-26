#!/usr/bin/env bash
# F41RevRider gaming probes for plans/routed_open.py — runs only inside $S.
set -u
S=/fast/scratch/hyaku/kengaku-r41/F41RevRider
R=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-41/falsify/F41RevRider
RID=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/routed_open.py
mkdir -p "$S/receipts" "$R"
mk() { D=$(mktemp -d -p "$S"); git -C "$D" init -q; mkdir -p "$D/corpus"; printf 'R1 routed\nR2 routed\n' > "$D/lesson.md"; printf '%s' "$D"; }

# G1: closed row, vacuous check (true), fabricated close evidence
A=$(mk)
cat > "$A/corpus/routed-findings.jsonl" <<'EOF'
{"id": "G1", "class": "t", "source": "lesson.md:1", "opened_round": 1, "status": "closed", "close": "fabricated deadbeef absent.md:1", "blocker": null, "check": "true", "note": null}
EOF
echo "== G1 closed + check=true + fabricated close" > "$S/receipts/G1.txt"
python3 "$RID" --lane "$A" --observe >> "$S/receipts/G1.txt" 2>&1; echo "rc=$?" >> "$S/receipts/G1.txt"

# G2: closed row, check=null, fabricated close
B=$(mk)
cat > "$B/corpus/routed-findings.jsonl" <<'EOF'
{"id": "G2", "class": "t", "source": "lesson.md:1", "opened_round": 1, "status": "closed", "close": "fabricated evidence, nothing done", "blocker": null, "check": null, "note": null}
EOF
echo "== G2 closed + check=null + fabricated close" > "$S/receipts/G2.txt"
python3 "$RID" --lane "$B" --observe >> "$S/receipts/G2.txt" 2>&1; echo "rc=$?" >> "$S/receipts/G2.txt"

# G3: self-referential check — greps the file for its own closed status
C=$(mk)
cat > "$C/corpus/routed-findings.jsonl" <<'EOF'
{"id": "G3", "class": "t", "source": "lesson.md:2", "opened_round": 1, "status": "closed", "close": "self-certified", "blocker": null, "check": "grep -q '\"status\": \"closed\"' corpus/routed-findings.jsonl", "note": "work on lesson.md:2 never done"}
EOF
echo "== G3 self-referential check (work never done)" > "$S/receipts/G3.txt"
python3 "$RID" --lane "$C" --observe >> "$S/receipts/G3.txt" 2>&1; echo "rc=$?" >> "$S/receipts/G3.txt"

# G4: check mutates the lane (observe runs it unsandboxed from the lane root)
D4=$(mk)
cat > "$D4/corpus/routed-findings.jsonl" <<'EOF'
{"id": "G4", "class": "t", "source": "lesson.md:1", "opened_round": 1, "status": "closed", "close": "evidence", "blocker": null, "check": "touch pwned.txt", "note": null}
EOF
echo "== G4 lane-mutating check" > "$S/receipts/G4.txt"
python3 "$RID" --lane "$D4" --observe >> "$S/receipts/G4.txt" 2>&1; echo "rc=$?" >> "$S/receipts/G4.txt"
ls -l "$D4/pwned.txt" >> "$S/receipts/G4.txt" 2>&1
git -C "$D4" status --porcelain >> "$S/receipts/G4.txt" 2>&1

# G5: refused row dodges the burn-down tally
E=$(mk)
cat > "$E/corpus/routed-findings.jsonl" <<'EOF'
{"id": "G5", "class": "t", "source": "lesson.md:1", "opened_round": 1, "status": "refused", "close": null, "blocker": "decided not to", "check": null, "note": "nothing done, excluded from routed_open"}
EOF
echo "== G5 refused row dodges tally" > "$S/receipts/G5.txt"
python3 "$RID" --lane "$E" >> "$S/receipts/G5.txt" 2>&1; echo "rc=$?" >> "$S/receipts/G5.txt"

# G6: the real protection — closed row whose check fails is caught
F=$(mk)
cat > "$F/corpus/routed-findings.jsonl" <<'EOF'
{"id": "G6", "class": "t", "source": "lesson.md:1", "opened_round": 1, "status": "closed", "close": "evidence", "blocker": null, "check": "false", "note": null}
EOF
echo "== G6 closed + failing check (protection demo)" > "$S/receipts/G6.txt"
python3 "$RID" --lane "$F" --observe >> "$S/receipts/G6.txt" 2>&1; echo "rc=$?" >> "$S/receipts/G6.txt"

# G7: pinned-ledger guard is name-based only
G7=$(mk)
cat > "$G7/corpus/routed-findings.jsonl" <<'EOF'
{"id": "G7", "class": "t", "source": "lesson.md:1", "opened_round": 1, "status": "open", "close": null, "blocker": null, "check": null, "note": null}
EOF
cp "$G7/corpus/routed-findings.jsonl" "$S/ledger-copy.jsonl"
echo "== G7 --file ledger-copy.jsonl (renamed ledger copy) accepted?" > "$S/receipts/G7.txt"
python3 "$RID" --lane "$G7" --file "$S/ledger-copy.jsonl" >> "$S/receipts/G7.txt" 2>&1; echo "rc=$?" >> "$S/receipts/G7.txt"

cat "$S/receipts/G1.txt" "$S/receipts/G2.txt" "$S/receipts/G3.txt" "$S/receipts/G4.txt" "$S/receipts/G5.txt" "$S/receipts/G6.txt" "$S/receipts/G7.txt"
