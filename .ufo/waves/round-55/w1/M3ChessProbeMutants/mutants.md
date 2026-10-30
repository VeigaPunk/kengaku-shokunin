# M3ChessProbeMutants — mutation record for `plans/round55_c3_chess_probe.py`

Seat `M3ChessProbeMutants`, kengaku round 55 wave 1 (v2, build+attack), 2026-10-30.
Lane `kengaku-shokunin` @ `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (claims freeze read first:
`plans/round-55-claims.md`). No predicate, counter, kill rule or target below was changed.
**All mutations were applied to scratch copies only** under
`/fast/scratch/hyaku/kengaku-r55/M3ChessProbeMutants/`; the lane file was never written.

## 0. Baseline (pristine) — the reference the mutants are judged against

| item | value |
|---|---|
| pristine probe sha256 | `7bd2863ca745f1656a23617d66a1926b12e2656b17fdc903b69d3eb28ce72d60` |
| lane file sha256 before AND after all runs | `7bd2863ca745f1656a23617d66a1926b12e2656b17fdc903b69d3eb28ce72d60` (unchanged) |
| lane file git status before/after | `?? plans/round55_c3_chess_probe.py` (untracked, unmodified) |
| captured grader sha256 | `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` (= frozen pin) |
| command | `python3 <copy> --lane <lane> --work <scratch>/work-base --receipt <scratch>/receipts/base.txt` |
| exit code | **0** |
| receipt sha256 | `de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca` |

Baseline receipt (`receipts/base.txt`):

```
cases=12 observed_pass=5 observed_fail=7 mismatches=0
PREDICATE R55-C3 pass
```

Two independent runs of the pristine copy produced **byte-identical** receipts
(`base.txt` == `base2.txt`), so the detector is deterministic. The pristine receipt is also
**byte-identical to the lane's already-committed-but-untracked receipt**
`corpus/evidence/round55/chess-best-move-probe.txt` (sha256 `de082669…8aaca`) — the probe
reproduces the round's committed evidence exactly. Wall clock 0.40 s, MAXRSS 20.5 MB.

## 1. Mutant M1 — verdict mapping inverted (pass ↔ fail)

Mutation (one behaviour-bearing point, `run_in_sandbox`): the `P` and `F` returns swapped.

```python
     if proc.returncode == 0:
-        return "P", proc.returncode, out
+        return "F", proc.returncode, out
     if "AssertionError" in out:
-        return "F", proc.returncode, out
+        return "P", proc.returncode, out
```

Expected detector: the receipt must flip to `mismatches>0` / `PREDICATE fail`.
**Observed — mutant KILLED** (`receipts/mut1.txt`, sha256 `dabd1f6e…9311`, exit code **1**):

```
-case both-lowercase-two-lines predicted=P observed=P rc=0
+case both-lowercase-two-lines predicted=P observed=F rc=0
…  (all 12 case lines flip; rc values are unchanged, proving only the *mapping* moved)
-cases=12 observed_pass=5 observed_fail=7 mismatches=0
-PREDICATE R55-C3 pass
+cases=12 observed_pass=7 observed_fail=5 mismatches=12
+PREDICATE R55-C3 fail
```

The frozen predicate holds: `mismatches=12 > 0`, `PREDICATE R55-C3 fail`, exit 1. The mutant is
detected by the receipt exactly as the kill rule for R55-C3 requires (an observed≠predicted case
must count as a mismatch). Full diff: `receipts/diffs/mut1-vs-base.diff`.
Note the pass/fail *counters* swapped 5/7 → 7/5 — the mutant is visible in three independent
places (case lines, summary counts, predicate line), so this mutant is not near the detector's edge.

## 2. Mutant M2 — mismatch counter skipped (the leg the round's kill rule leans on)

Mutation (one behaviour-bearing point, `run_battery`): the increment is deleted, leaving the
comparison unused.

```python
         if observed != predicted:
-            mismatches += 1
+            # MUTANT: mismatch counter skipped
```

Expected detector per the tasking: the summary must still change (or the case lines must expose
it); if NOTHING observable changes, the mismatch leg is decorative — a finding.
**Observed on the frozen case table — mutant SURVIVES, byte-identical to baseline:**
`cmp base.txt mut2.txt` → identical; sha256 of both = `de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca`;
exit code **0**; `mismatches=0`, `PREDICATE R55-C3 pass`, identical case lines.

**Why it survives, and why that is not the same as "the leg is dead":** on the frozen table every
one of the 12 predictions is correct, so `mismatches` is 0 whether or not the counter runs. The
counter is only *observable* when a case mispredicts. To separate "counter absent" from "counter
present but never triggered", I ran the auxiliary pair below with one deliberately mispredicted
case (`single-move-only` predicted flipped F→P, so observed F ≠ predicted P):

| variant | source | receipt summary | predicate | exit |
|---|---|---|---|---|
| M2b — control: mispredicted case, counter INTACT | `receipts/mut2b.txt` | `observed_pass=5 observed_fail=7 mismatches=1` | `PREDICATE R55-C3 fail` | **1** |
| M2c — mispredicted case, counter SKIPPED | `receipts/mut2c.txt` | `observed_pass=5 observed_fail=7 mismatches=0` | `PREDICATE R55-C3 pass` | **0** |

Diff M2b → M2c (`receipts/diffs/mut2b-vs-mut2c.diff`):

```
-cases=12 observed_pass=5 observed_fail=7 mismatches=1
-PREDICATE R55-C3 fail
+cases=12 observed_pass=5 observed_fail=7 mismatches=0
+PREDICATE R55-C3 pass
```

**Verdict: the mismatch leg is real and load-bearing** — with a mispredicted case present, deleting
the counter flips the receipt from `mismatches=1 / PREDICATE fail / exit 1` to
`mismatches=0 / PREDICATE pass / exit 0`. The case lines alone do **not** expose it: M2c's case
line still reads `CASE single-move-only predicted=P observed=F rc=1`, so a reader of the case
lines sees the discrepancy, but the *summary* line and the *predicate* both stay green. The
summary `mismatches=` counter is therefore the only thing standing between a mispredicted case and
a false `PREDICATE R55-C3 pass`.

**Coverage finding (reported, not fixed — not this seat's file):** the frozen 12-case table cannot
exercise the mismatch leg at all, because every frozen prediction is correct. The shipped receipt
`mismatches=0` is thus consistent with *both* a working counter and a deleted one. The counter is
verified correct only by the negative control above, not by the round's own receipt. If the L1 wants
the mismatch leg covered by the committed artefact, the case table would need one deliberately
mispredicted case (or a `--selftest`-style negative case) — that is a change to the frozen case
table, i.e. amendment data, and is the L1's call, not mine.

## 3. Mutant M3 — null mutant: case execution order reversed

Mutation (one behaviour-bearing point, `run_battery`): `for … in CASES:` → `for … in reversed(CASES):`.

Expected detector: output must be equivalent (order-insensitive summary).
**Observed — null mutant CONFIRMED, summary order-insensitive** (`receipts/mut3.txt`, exit **0**):

```
base : cases=12 observed_pass=5 observed_fail=7 mismatches=0   / PREDICATE R55-C3 pass
mut3 : cases=12 observed_pass=5 observed_fail=7 mismatches=0   / PREDICATE R55-C3 pass
```

Sorted CASE-line sets are **identical** (`diff receipts/base-cases-sorted.txt receipts/mut3-cases-sorted.txt`
→ empty; `receipts/diffs/mut3-sorted-cases-vs-base.diff`). Raw bytes differ only in line *order*
(receipt sha256 `214899a2…e8db` vs base `de082669…8aaca`) — the counters and the predicate are
invariant, exactly as an order-insensitive multiset comparison requires. Good: the probe has no
order-dependent state (each case gets its own `/app` dir, its own sandbox).

**One observation worth recording:** the *receipt bytes* are order-sensitive (case lines are
emitted in execution order) while the *summary* is order-insensitive. Any downstream check that
pins the receipt by sha256 would break under a reordering of the case table; a check that parses
`cases=… observed_pass=… observed_fail=… mismatches=…` would not. The round's after-predicate
quotes the summary form, so this is consistent with the claim, but the byte-level receipt hash is
the brittle form.

## 4. Auxiliary probes (beyond the three required mutants)

| id | mutation | observed | value |
|---|---|---|---|
| M4 | `BWRAP = "/nonexistent/bwrap"` | exit **2**, all 12 cases `observed=SETUP rc=-1`, `SETUP cases=…` line, no PREDICATE line | the SETUP path is reachable and distinct from a verdict; a broken sandbox is not silently scored |
| M5 | `GRADER_SHA256` pin → all-zero | exit **2**, `SETUP grader sha256 a540714e… != frozen pin 0000…` | the upstream-identity leg is real and fails closed (refuses to run against drifted bytes) |
| M6 | `run_in_sandbox(..., timeout=0)` | exit **2**, 12× `SETUP … timeout after 0s` | the bounded-wait leg is real and fails closed |
| M7 | `reversed-order` case body → `"g2g4 e2e4 e2e4"` (duplicate token) | exit **1**, `CASE reversed-order predicted=P observed=F rc=1`, `mismatches=1`, `PREDICATE R55-C3 fail` | the probe discriminates a duplicated token from the two-move multiset — the full-multiset (not set) semantics of the grader are genuinely exercised by the frozen table |

M5/M6 also answer a round-kill-rule question directly: kill rule (c) "the upstream identity check
fails at the pin" is a *code* leg with teeth — mutating the pin makes the tool refuse to run
rather than score drifted bytes.

M4's stderr carries the first three lines of the sandbox error per case, e.g.
`SETUP-ERROR both-lowercase-two-lines rc=-1: failed to exec bwrap: [Errno 2] No such file or directory: '/nonexistent/bwrap'`.

**Observation:** M4's and M6's *receipts* are byte-identical to each other (`d6493ac7…3c36`) — a
missing bwrap and a zero timeout both render as "12 cases, observed=SETUP rc=-1, mismatches=0,
SETUP cases=<all 12>", with no PREDICATE line. The two failures are distinguishable only in
**stderr** (`failed to exec bwrap: …` vs `timeout after 0s: …`), which the `--receipt` file does
not capture (the receipt gets stdout only). So a consumer reading only the committed receipt cannot
tell a broken sandbox from a timeout — both are simply "no PREDICATE line, exit 2". Not a claim
defect (the exit code and the absence of a PREDICATE line are unambiguous), but worth recording:
the receipt is not self-describing about *why* the run failed.

## 5. Selftest path cross-check

`--selftest` (toy grader, never touches the TB2 capture) on the pristine copy:
`SELFTEST cases=2 failures=0`, exit **0**. On the mutants:

| copy | selftest result | exit |
|---|---|---|
| mut1 (mapping inverted) | `toy-pass predicted=P observed=F`, `toy-fail predicted=F observed=P`, `failures=2` | **1** |
| mut2 (counter skipped) | `failures=0` | 0 |
| mut3 (order reversed) | `failures=0` | 0 |

The toy selftest detects the verdict-mapping inversion but is blind to the mismatch counter (it
has its own separate `failures` counter in `run_selftest`, not the `mismatches` counter under
test) and blind to case ordering. Consistent with M2/M3 findings.

## 6. Independent upstream re-verification (read-only GETs; no auth, no POST)

Not part of the three mutants, but it closes the R55-C3 kill rule (c) check independently of the
lane's own tooling. The upstream repo is `harbor-framework/terminal-bench-2` (the pin does **not**
resolve in `laude-institute/terminal-bench` or `-terminal-bench-datasets` — those are 404/422,
and the lane's own `corpus/evidence/round53/pin-tree-2fd12b88.json` names the right repo).

- `GET https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88…66d6?recursive=1`
  → HTTP 200, 1446 entries, `truncated: false`; the tree contains
  `chess-best-move/tests/test_outputs.py` blob `6ec2300aaac167ebd547a9ccfe00abc6af410a75` (971 B).
- `GET …/raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…66d6/chess-best-move/tests/test_outputs.py`
  → HTTP 200, sha256 `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` —
  **byte-identical to the lane's captured grader and to the probe's frozen pin**.
- Same path on `laude-institute/terminal-bench@main` (task lives under `original-tasks/`) → sha256
  `a540714e…f286` too — the file is unchanged between the pin and current main.
- The grader's own assertion, read from the upstream bytes: `assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"` —
  the probe's oracle derives only from the captured grader's own assertion, and the probe's
  `PROG` calls exactly `test_outputs.test_move_correct()`.

**A1 amendment verified independently:** the claim states chess-best-move `tests/test.sh` is
byte-identical to the held regex-log runner (both sha256 `4770437e…6c334`). Confirmed: upstream
`chess-best-move/tests/test.sh` at the pin = `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334`,
identical to the lane's captured `chess-best-move/tests/test.sh`, identical to
`corpus/evidence/round52/graders/regex-log/tests/test.sh`, identical to
`corpus/evidence/round36/tb2-regex-log/test.sh` (S109's file). Dropping the third SOURCES row is
correct — a new row would duplicate held ground.

## 7. Hash ledger

| file | sha256 |
|---|---|
| pristine probe (== lane file) | `7bd2863ca745f1656a23617d66a1926b12e2656b17fdc903b69d3eb28ce72d60` |
| base receipt / base2 receipt | `de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca` |
| mut1 receipt | `dabd1f6ee0083b3281569bd45aed576b4364b5e575a967f1be2fb87cce1f9311` |
| mut2 receipt | `de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca` (== base) |
| mut2b receipt | `b1dc9c65f72325b2d549bff62177db6e9ff7458b6e32954bb3235cb21242fcca` |
| mut2c receipt | `47548c354ec004ce5efae2f1423a9f33c7f24b1e952bc2d015e7d9056d03f294` |
| mut3 receipt | `214899a264f42074dadc039b7f382553dcfc3a92b91d09317be08810ea80e8db` |
| mut4 receipt | `d6493ac7d081a834bd3475a67c03fef8f6eb6b9b0ab0c138b77ed26c83833c36` |
| mut5 receipt | `0d6874e5ca05eb4f7180d925d3c085b5d4c4a86f8595e19396e90dd5a56d6809` |
| mut6 receipt | `d6493ac7d081a834bd3475a67c03fef8f6eb6b9b0ab0c138b77ed26c83833c36` (== mut4 receipt) |
| mut7 receipt | `fc71ddbdd074fbeee922f897f8d58ff495691679efa11c61a864d3da27fe722b` |
| mut1 probe copy | `c33452cfb9fd5aee0b1dcd72f8dd058a9c469947fc802eca62d2b77d430a4c35` |
| mut2 probe copy | `2208a6c68e4282cf85f9ea49ca8a2822f6ce999d2ba224f7e732abb636dfc07a` |
| mut2b probe copy | `ac47885e8645c419a238bde5dd9e4ad78b3bb1cc0066436243f5935e41795dcf` |
| mut2c probe copy | `c5a353df3da107de0261e0d35f64c060eec9dce1c709f8f10142481773df9d7b` |
| mut3 probe copy | `707d6349a019522bbb3c7c93c660fc8e09c0ccfb7ea5095079a979ab62040f6a` |
| mut4 probe copy | `a976002029c166e0d50e380693e983af258630c03c8464ac8526032d4d1cd73e` |
| mut5 probe copy | `87f4e3e70d399c85b93b0c0f76f76bf8a256b2e1842d4245bd264602bd35156c` |
| mut6 probe copy | `ddc4f819c05bea4838293e9d831a7bd996d2aa1b5c8b282d8d011865c30c97aa` |

Per-receipt hashes: `receipts/SHA256SUMS.txt`. Raw diffs: `receipts/diffs/`.
