#!/usr/bin/env bash
# mutate_test.sh — mutation harness for kengaku-shokunin grader.py (round 10).
#
# Purpose: falsify/confirm that grader.py actually VERIFIES its evidence, per the
# pinned CLI spec. Every mutation is applied to COPIES under a mktemp -d dir;
# the repository originals are never touched. The grader itself is never edited.
#
# Usage: bash mutate_test.sh [REPO_ROOT]
#   REPO_ROOT defaults to /home/vgpnk/projects/shokunin/kengaku-shokunin
#
# Mutation matrix (one variant = fresh copies + at most one mutation + one run):
#   M0 control        no mutation                                          -> expect exit 0
#   M1 record-level   flip `ok:true` of the FIRST A-INC record (r8 jsonl)  -> expect exit 1
#   M2 summary-level  `A-INC: 7/10` -> `A-INC: 8/10` in r8 run.log         -> expect exit 1
#   M3 re-parse-level corrupt the fenced ```json block inside `raw` of the
#                     FIRST A-MONO record (r9 jsonl): first digit seq -> "0XX",
#                     so the block no longer parses as JSON                -> expect exit 1
#
# Grader CLI spec (pinned):
#   python3 grader.py [--selftest] [--r8-jsonl P] [--r8-runlog P] [--r9-jsonl P] [--r9-md P]
#   exit 0 = every recomputed value matches the stored one
#   exit 1 = at least one mismatch (`MISMATCH <check-id>: stored=<x> recomputed=<y>`)
#   exit 2 = missing/unreadable input
#
# Output: one "M<i> PASS|FAIL" line per variant; exit 0 iff all four match
# expectations. Exit 3 = harness precondition failure (grader missing, sentinel
# absent/ambiguous, evidence unreadable) — a harness fault, NOT a grader gap.

set -u

REPO="${1:-/home/vgpnk/projects/shokunin/kengaku-shokunin}"

if [ ! -f "$REPO/grader.py" ]; then
  echo "SKIP: $REPO/grader.py not found (L1 has not landed it yet); nothing to mutate."
  exit 3
fi

# --- evidence sources (read-only; originals are never modified) -------------
R8JSON_SRC="$REPO/corpus/evidence/round8-horizon/results.jsonl"
R8LOG_SRC="$REPO/corpus/evidence/round8-horizon/run.log"
R9JSON_SRC="$REPO/corpus/evidence/round9-replication/results-r9.jsonl"
R9MD_SRC="$REPO/corpus/evidence/round9-replication/replication.md"

for f in "$R8JSON_SRC" "$R8LOG_SRC" "$R9JSON_SRC" "$R9MD_SRC"; do
  if [ ! -r "$f" ]; then
    echo "HARNESS FAULT: cannot read $f"
    exit 3
  fi
done

# --- temp workspace: all mutations happen here, never in the repo -----------
mkdir -p /tmp/kengaku-r10 || exit 3
TMP=$(mktemp -d /tmp/kengaku-r10/mutate.XXXXXX) || exit 3
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/r8" "$TMP/r9"

copy_inputs() {
  cp "$R8JSON_SRC" "$TMP/r8/results.jsonl"    || return 1
  cp "$R8LOG_SRC"  "$TMP/r8/run.log"          || return 1
  cp "$R9JSON_SRC" "$TMP/r9/results-r9.jsonl" || return 1
  cp "$R9MD_SRC"   "$TMP/r9/replication.md"   || return 1
}

# --- grader invocation: all four paths EXPLICIT (mutated copies live in $TMP,
#     so repo-relative defaults must never be exercised); capture exit code ---
GRADE_RC=""
run_grader() {
  local label="$1"
  echo "--- grader run [$label] ---"
  python3 "$REPO/grader.py" \
    --r8-jsonl "$TMP/r8/results.jsonl" \
    --r8-runlog "$TMP/r8/run.log" \
    --r9-jsonl "$TMP/r9/results-r9.jsonl" \
    --r9-md "$TMP/r9/replication.md"
  GRADE_RC=$?
  echo "--- grader exit=$GRADE_RC ---"
}

# --- M<i> PASS/FAIL bookkeeping ---------------------------------------------
RESULT_M0="FAIL"; RESULT_M1="FAIL"; RESULT_M2="FAIL"; RESULT_M3="FAIL"
expect() { # $1 = variant id (M0..M3), $2 = expected grader exit code
  local id="$1" want="$2"
  if [ "$GRADE_RC" -eq "$want" ]; then
    echo "$id PASS"
    eval "RESULT_$id=PASS"
  else
    echo "$id FAIL (grader exit $GRADE_RC, expected $want)"
  fi
}

# --- M1: record-level mutation ----------------------------------------------
# Flip `ok: true -> false` on the FIRST A-INC record with ok==true.
# Surgical: replace the escaped substring `"ok": true` (verified unique within
# that one line) with `"ok": false` — a 1-byte semantic change; the line is not
# re-serialized, so every other byte of the record is untouched.
mutate_m1() {
  python3 - "$TMP/r8/results.jsonl" <<'PYEOF' || return 1
import json, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    lines = f.read().splitlines(True)  # keepends
done = False
out = []
for line in lines:
    if not done and line.strip():
        rec = json.loads(line)
        if rec.get("cell") == "A-INC" and rec.get("ok") is True:
            if line.count('"ok": true') != 1:
                print("M1 harness fault: '\"ok\": true' not unique in target line", file=sys.stderr)
                sys.exit(3)
            out.append(line.replace('"ok": true', '"ok": false', 1))
            done = True
            continue
    out.append(line)
if not done:
    print("M1 harness fault: no A-INC record with ok==true found", file=sys.stderr)
    sys.exit(3)
for l in "".join(out).splitlines():  # mutated file must still be valid JSONL
    if l.strip():
        json.loads(l)
with open(path, "w", encoding="utf-8") as f:
    f.write("".join(out))
PYEOF
}

# --- M2: summary-level mutation ---------------------------------------------
# The stored SUMMARY line `A-INC: 7/10` (verified: exactly one occurrence in
# run.log) is edited to `A-INC: 8/10`. The recomputed tally from the jsonl
# records stays 7, so the grader's summary-vs-records cross-check must fire.
mutate_m2() {
  python3 - "$TMP/r8/run.log" <<'PYEOF' || return 1
import sys
path = sys.argv[1]
s = open(path, encoding="utf-8").read()
if s.count("A-INC: 7/10") != 1:
    print("M2 harness fault: sentinel 'A-INC: 7/10' absent or ambiguous", file=sys.stderr)
    sys.exit(3)
open(path, "w", encoding="utf-8").write(s.replace("A-INC: 7/10", "A-INC: 8/10", 1))
PYEOF
}

# --- M3: re-parse-level mutation ---------------------------------------------
# The `raw` field of the FIRST A-MONO r9 record is a fenced block:
#   ```json\n{"nails": 0, "bolts": 0, "screws": 7, "hinges": 16}\n```
# Appending inside the block's WHITESPACE would not change the parsed value,
# so the mutation rewrites the FIRST digit sequence inside the block, turning
# `0` into `0XX`: the re-parsed block no longer parses as JSON, so any grader
# that re-derives got from raw must diverge -> exit 1.
# Surgical: replace the JSON-escaped raw substring (verified unique within that
# one line) — the line is not re-serialized, so all other bytes are untouched.
mutate_m3() {
  python3 - "$TMP/r9/results-r9.jsonl" <<'PYEOF' || return 1
import json, re, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    lines = f.read().splitlines(True)
done = False
out = []
for line in lines:
    if not done and line.strip():
        rec = json.loads(line)
        if rec.get("cell") == "A-MONO":
            raw = rec["raw"]
            m = re.search(r"\d+", raw)
            if not m:
                print("M3 harness fault: no digit sequence inside raw", file=sys.stderr)
                sys.exit(3)
            new_raw = raw[:m.start()] + m.group(0) + "XX" + raw[m.end():]
            esc_old, esc_new = json.dumps(raw), json.dumps(new_raw)
            if line.count(esc_old) != 1:
                print("M3 harness fault: escaped raw substring not unique in line", file=sys.stderr)
                sys.exit(3)
            out.append(line.replace(esc_old, esc_new, 1))
            done = True
            continue
    out.append(line)
if not done:
    print("M3 harness fault: no A-MONO record found", file=sys.stderr)
    sys.exit(3)
for l in "".join(out).splitlines():  # mutated file must still be valid JSONL
    if l.strip():
        json.loads(l)
with open(path, "w", encoding="utf-8") as f:
    f.write("".join(out))
PYEOF
}

# ============================ MUTATION VARIANTS ==============================
# Each variant gets FRESH copies so mutations never accumulate.

echo "== M0 control: unmutated copies =="
copy_inputs || exit 3
run_grader "M0-control"
expect M0 0

echo "== M1: flip ok:true -> ok:false on first A-INC (record layer) =="
copy_inputs || exit 3
mutate_m1 || exit 3
run_grader "M1-ok-flip"
expect M1 1

echo "== M2: A-INC: 7/10 -> 8/10 in run.log SUMMARY (summary layer) =="
copy_inputs || exit 3
mutate_m2 || exit 3
run_grader "M2-summary-edit"
expect M2 1

echo "== M3: 0 -> 0XX inside raw json block of first A-MONO (re-parse layer) =="
copy_inputs || exit 3
mutate_m3 || exit 3
run_grader "M3-raw-corrupt"
expect M3 1

# --- verdict -----------------------------------------------------------------
if [ "$RESULT_M0" = PASS ] && [ "$RESULT_M1" = PASS ] && \
   [ "$RESULT_M2" = PASS ] && [ "$RESULT_M3" = PASS ]; then
  echo "ALL PASS — grader catches all three corruption layers, clean control passes"
  exit 0
else
  echo "GRADER GAP: at least one layer is NOT caught -> mutation survived (see FAIL lines above)"
  exit 1
fi
