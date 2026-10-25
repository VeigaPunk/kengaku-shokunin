# r10-mutation-sh — mutation harness for kengaku grader.py

Artifact of **MutationHarness** (L2, round 10 fleet lane). Deliverable per brief:
`/tmp/kengaku-r10/mutate_test.sh` (bash, executable, FINAL sha256
`ad0511f2b8a49d3f9bd597afd0b99f46bf84b587af044c98150bdae92dd803f8`), full contents
below, plus `bash -n` output and layer-separation design notes.
The harness was first validated by an independent reference oracle
(`/tmp/kengaku-r10/probe_ref.py`, sha256
`539ce420027d2c3207ddc94bbd4026dd362463dc3699a669c1db009ba537715c`) that
re-derives each check layer from the mutated copies and reports which layer
diverges; after L1 landed grader.py, the harness was EXECUTED against the real
grader — live results in §7: **M0..M3 all PASS, harness exit 0, byte-identical
repeat run**.

## 1. Ground facts established (all commands + outputs)

| Fact | Command (terse) | Output |
|---|---|---|
| grader.py absent | `test -e <repo>/grader.py && echo EXISTS \|\| echo ABSENT` | `GRADER_ABSENT` |
| r8 jsonl shape | `json.loads` per line in eval | 268 records, no CR, keyset shapes: 10×meta, 140×graded(A-INC 100/A-MONO 10/B-* 32... minus), 70×ack, 32×B, 12+4×C |
| first A-INC ok==true | scan | **line 11** (`pid=1, turn=1`, `"ok": true` unique in line, `got==want` True) |
| run.log sentinel | `log.count("A-INC: 7/10")` | `1` (exactly one occurrence) |
| r9 first A-MONO | scan | **line 19** (`pid=101, turn=1`), `raw = '```json\n{"nails": 0, "bolts": 0, "screws": 7, "hinges": 16}\n```'` |
| original hashes | `sha256sum` | r8 jsonl `bd986e5e…92e2204`, r9 jsonl `c20158bd…1affbcb`, run.log `c977c6aa…2b3bef64` |
| originals untouched | `sha256sum` after all probes | 3/3 identical to repo files (see §4) |

## 2. Full script: /tmp/kengaku-r10/mutate_test.sh

```bash
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
```

## 3. `bash -n` syntax-check output

Command: `bash -n /tmp/kengaku-r10/mutate_test.sh && echo "bash -n: OK"`
Output (bash -n is silent on success; the echo proves rc=0):

```
bash -n: OK
```

Additional no-grader dry run (spec-conformant precondition handling):
Command: `/tmp/kengaku-r10/mutate_test.sh; echo "no-grader exit=$?"`
Output:

```
SKIP: /home/vgpnk/projects/shokunin/kengaku-shokunin/grader.py not found (L1 has not landed it yet); nothing to mutate.
no-grader exit=3
```

Exit 3 is reserved for harness preconditions (grader missing / sentinel missing /
evidence unreadable) so that a harness exit 1 always means "grader ran and a
mutation SURVIVED" — never "the harness broke".

## 4. Design notes: why each mutation trips a DIFFERENT grader check layer

The three mutations are constructed so that each is provably invisible to two of
the three verification layers and detectable only by its target layer. Evidence
below is from an independent oracle (`probe_ref.py`) that re-derives each layer
separately; it reported exactly one divergent layer per mutation (§5).

### M1 — record-level layer (flip stored `ok`, records otherwise consistent)

Target: r8 jsonl line 11 (`A-INC`, pid=1, turn=1), `"ok": true` → `"ok": false`.
Verified 1-byte splice (`'"ok": true'` count in line = 1); `got == want` is True
in that record, so after the flip `ok != (got == want)`.

* Invisible to the summary layer — **by evidence, not assumption**. horizon.py
  builds the SUMMARY from `res["final_ok"]`, and `run_inc` returns
  `final_ok = ckpt_oks[-1]`: the LAST graded turn per pid (horizon.py:161-166,
  read directly). Predicate census over the 10 A-INC pids
  (all10=5, ge7of10=7✓, last_ok=7✓, first_ok=9, t7_ok=7✓, ge6of10=9,
  maj_strict=9): the stored `A-INC: 7/10` is reproduced by `last_ok` (and
  coincidentally `ge7of10`). Flipping pid1/turn1 leaves `last_ok` at **7**
  (pid 1 has 6/10 turn-ok; its last graded turn, turn 10, stays ok) — so a
  faithful summary recomputation still says 7/10 and does NOT fire. Under the
  alternative census-consistent predicate `ge7of10` the summary WOULD also fire
  (7→6), which only strengthens exit 1. Either way M1 cannot pass a grader that
  implements any record-level `ok`-vs-`got`/`want` check; and the only
  summary-consistent predicate that masks M1 at summary level (`last_ok`) is
  precisely the one horizon.py actually used.
* Invisible to the re-parse layer: the record's raw block still parses and still
  equals `got` (untouched fields).

Cross-check headroom: among all 100 A-INC records there are **0** existing
disagreements between `ok` and `got==want`, so a grader implementing this check
is not accidentally satisfied/fouled by other records.

### M2 — summary-level layer (stored tally vs recomputed tally)

Target: the unique `A-INC: 7/10` line in the run.log copy (count verified == 1)
→ `A-INC: 8/10`. The r8 jsonl is untouched, so the recomputed tally from records
stays 7 while the stored summary says 8 — only a stored-vs-recomputed summary
cross-check can fire. Record-level checks pass (every record is still internally
consistent); the re-parse layer is on the r9 file and is not even in play.
Conversely a grader that merely recomputes records and never compares against
run.log passes M2 → mutation survives → harness prints `M2 FAIL`.

### M3 — re-parse-level layer (re-derive `got` from `raw`)

Target: r9 jsonl line 19 (`A-MONO`, pid=101); inside its fenced block the first
digit sequence `0` → `0XX` (+2 bytes), applied by splicing the JSON-escaped
`raw` substring (verified unique in the line), so the rest of the line is
byte-identical and the file stays valid JSONL.

* Why a digit and not whitespace: the spec forbids whitespace-only changes —
  they leave the parsed JSON value identical, so a correct re-parse layer would
  NOT fire and the mutant would falsely survive. `0XX` makes
  `json.loads(block)` raise JSONDecodeError (verified), so
  `extract_json_block(raw)` (verbatim from replicate.py: fenced-block regex
  first, brace-regex fallback) returns None ≠ stored `got` — the re-derived
  answer diverges from the stored one.
* Invisible to the record layer: `ok`, `got`, `want` are untouched (and the
  stored `ok:false`/`nwrong:3` of this record already disagrees with `got`, which
  is fine — the layer under test is re-parse, not ok-consistency).
* Invisible to the summary layer: r8 files and replication.md untouched.

### Why the four expectations are attributable

Each variant runs on FRESH copies (mutations never accumulate), so
`M0=0, M1=1, M2=1, M3=1` can only all hold if the grader has (at least) one live
check in each of the three layers. A grader missing any layer survives exactly
one mutant class and the harness names it (`M<i> FAIL`). The M0 control guards
the opposite failure: a grader that always exits 1 (or flags the two legitimate
brace-fallback raws, §6) fails M0 and is rejected as over-firing.

## 5. Oracle verification log (stand-in for grader runs until L1 lands grader.py)

probe_ref.py re-derives: (a) record layer `ok == (got==want)` over all graded
records of both files; (b) summary layer — every `=== SUMMARY ===` line vs
recomputed tallies (A-* = last-graded-turn-ok per pid; others = ok count);
(c) re-parse layer — `extract_json_block(raw) == got` for graded records, with
the extractor ported **verbatim** from replicate.py (407 chars).
Note: the probe does NOT check replication.md; the r9-md path is exercised by
the harness only as grader input, per spec.

```
== P0 unmutated ==   ALL LAYERS AGREE          exit=0
== P1 after M1 ==    DIVERGENT record: A-INC pid=1 turn=1 ok=False but got==want is True
                                                exit=1   (record layer ONLY — summary stayed 7/10, reparse clean)
== P2 after M2 ==    DIVERGENT summary: A-INC stored 8/10 recomputed 7/10
                                                exit=1   (summary layer ONLY)
== P3 after M3 ==    DIVERGENT reparse: A-MONO pid=101 no fenced json block
                                                exit=1   (reparse layer ONLY — extractor returns None on 0XX block)
```

Isolation of originals across all probes:
`sha256sum` of the three pre-probe saved copies vs the repo files — identical:
`bd986e5e…` (r8 jsonl), `c977c6aa…` (run.log), `c20158bd…` (r9 jsonl). 3/3 match.

## 6. Caveat for the L1 grader author (UNVERIFIED against grader, verified against data)

Two r9 graded records (`A-CKPT710`, pid=104, turns 7 and 10) have `got` but a
raw whose fenced opener was truncated mid-transcript
(`'{"nails": 25, ...}\n```'`); replicate.py's `extract_json_block` recovers them
via its brace-regex fallback (126 of 128 graded r9 records have a fenced block;
these 2 do not). A grader that REQUIRES a fenced block for every graded record
would flag these two on M0 and exit 1 — a false mismatch. The grader should
reuse replicate.py's `extract_json_block` verbatim (as probe_ref.py does; P0
then agrees on all 284+268 records). This is the one place where M0's
"expect exit 0" depends on grader implementation details beyond the pinned CLI
spec.

## 7. LIVE EXECUTION against landed grader.py (addendum)

L1 landed `grader.py` at repo root (41571 bytes, sha256
`7a51f6c8cc486679dbee7425f5061a33eceb74b6702b9310848f2a9c893ec9c2`, mtime
2026-09-28 19:17:54) with CLI matching the pinned spec. Main confirmed the
extractor is ported verbatim (fenced-block first, brace fallback second), so the
§6 caveat is retired: no M0 false-flag.

Command: `/tmp/kengaku-r10/mutate_test.sh; echo "harness-exit=$?"`
Key output (grader lines verbatim; `[pin] r*_SKIPPED` lines elided):

```
== M0 control: unmutated copies ==
CHECKS n=145 mismatches=0 errata_pinned=1
VERDICT: PASS — stored evidence fully re-derives offline
--- grader exit=0 ---
M0 PASS
== M1: flip ok:true -> ok:false on first A-INC (record layer) ==
MISMATCH r8.replay.A-INC.ok: 1/100 records differ (first: (1, 1, 'ok'))
CHECKS n=145 mismatches=1 errata_pinned=1
VERDICT: FAIL
--- grader exit=1 ---
M1 PASS
== M2: A-INC: 7/10 -> 8/10 in run.log SUMMARY (summary layer) ==
MISMATCH r8.summary.A-INC: stored=(8, 10) recomputed=(7, 10)
MISMATCH r9.crossround.A-INC.r8_col: stored='7/10' recomputed='8/10'
MISMATCH r9.crossround.A-INC.r8_col_vs_replay: stored='7' recomputed='8'
CHECKS n=145 mismatches=3 errata_pinned=1
VERDICT: FAIL
--- grader exit=1 ---
M2 PASS
== M3: 0 -> 0XX inside raw json block of first A-MONO (re-parse layer) ==
MISMATCH r9.replay.A-MONO.got: 1/8 records differ (first: (101, 1, 'got'))
MISMATCH r9.replay.A-MONO.nwrong: 1/8 records differ (first: (101, 1, 'got'))
MISMATCH r9.observed.A-MONO.mean_nwrong: stored='2.250' recomputed='2.375'
MISMATCH r9.failure_classes.parse_fail: stored='0/32' recomputed='1/32'
MISMATCH r9.failure_classes.state_error: stored='12/32' ... recomputed='23/32' ...
MISMATCH r9.failure_classes.mono.parse: stored='0/8' recomputed='1/8'
MISMATCH r9.failure_classes.mono.state_error: stored='8/8' recomputed='7/8'
CHECKS n=145 mismatches=7 errata_pinned=1
VERDICT: FAIL
--- grader exit=1 ---
M3 PASS
ALL PASS — grader catches all three corruption layers, clean control passes
harness-exit=0
```

Every mutant is killed by checks of its intended layer (M1: record replay;
M2: summary + crossround; M3: re-parse + downstream observed/failure-class
aggregates). One harness bug was found and fixed during live execution: the
post-mutation JSONL sanity check originally validated the whole file with a
single `json.loads` ("Extra data" on line 2) — now line-wise in both M1 and M3
blocks (this is the only diff vs the version quoted in §2; §2 quote above has
been updated to match).

### 7.1 First-run finding: grader v1 failed its own clean control

The FIRST live run (against the initially landed grader, 41777 bytes, mtime
19:15) caught a real defect before L1's fix:

```
MISMATCH r9.onset.predicted_vs_observed: stored='5.0 predicted' recomputed='5.8 observed'
CHECKS n=145 mismatches=1 errata_pinned=1
VERDICT: FAIL
--- grader exit=1 ---
M0 FAIL (grader exit 1, expected 0)
harness-exit=3 (M3 aborted on the same pre-fix harness bug)
```

M0 exists exactly to catch over-firing graders; it did. grader.py was replaced
by L1 at 19:17:54 (41571 bytes, hash above) and the subsequent full run passes
clean. Originals were never touched (§5 hashes).

### 7.2 Re-validation against grader v3 (19:22:26)

grader.py changed again after v2 validation (mtime 2026-09-28 19:22:26, 41912
bytes, sha256 `6fb13f771423734a5dd3de9f6ca6f662ed2faa46f22e3236acf723a25f951596`).
Re-ran the harness unchanged (script sha still
`ad0511f2b8a49d3f9bd597afd0b99f46bf84b587af044c98150bdae92dd803f8`):

Command: `/tmp/kengaku-r10/mutate_test.sh > run4.log 2>&1; echo "harness-exit=$?"`
Output: `M0 PASS / M1 PASS / M2 PASS / M3 PASS / ALL PASS`, harness exit 0,
11 MISMATCH lines — same counts and check-ids as the v2 run. The ONLY textual
difference between v2 and v3 outputs is the ruling prose inside the expected
M3 mismatch `r9.failure_classes.state_error` (v3 rewords the provenance
conjecture and cites replication.md §Errata); numbers identical
(`stored='12/32' recomputed='23/32' expected adjudicated '24/32'`).
Harness verdict is therefore grader-version-robust across v2 and v3.

