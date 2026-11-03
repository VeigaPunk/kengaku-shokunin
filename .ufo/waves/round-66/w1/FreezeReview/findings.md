# FreezeReview — kengaku round 66, wave 1, seat FreezeReview-4 (2026-11-03)

Scope: attack the frozen claims text (`plans/round-66-claims.md`) against the counters
(`plans/round66_c1_tensor_probe.py`, `plans/round65_c1_sqlite_probe.py` at HEAD `2c1ef88a`).
Read-only: no lane file edited; attack fixtures built in scratch and copied here.
All relative paths are lane-root; every observed value cites the command that produced it.

Method recap: read the claims file in full (74 lines); read the tensor probe in full
(346 lines: `frozen`, `KEYS`, `check_receipt`, `cmd_run`, `cmd_selftest`); read the R65
`receipt_failures`/`check_receipt`/argparse at HEAD; ran every counting command as written;
ran three receipt-forgery attacks against `check_receipt` (fixtures in `attack-fixtures/`);
`diff -u`'d every case against K1; verified grader sha vs SHA256SUMS line 171; verified the
three frontier quotes with `grep -F` in their captures.

## Findings (by severity)

### F1 — MUST-FIX (R66-C1, code wrong): `CASE` lines are optional; a receipt with none passes the gate, so the byte-binding clause is not enumerated

The predicate sentence says the receipt's "every `case_sha` and `junit_sha` equals the
committed bytes". `check_receipt` only validates `case_sha`/`junit_sha` on receipts that
carry `CASE` lines (`round66_c1_tensor_probe.py:267-278`: the loop iterates over lines
matching `CASE ...` and appends problems only per matched line; no "missing CASE line"
check mirrors the VECTOR presence check at :262-264). A receipt with GRADER + PROBE + the
five VECTOR lines + PREDICATE, and zero `CASE` lines, skips every byte binding.

Evidence (fixture `attack-fixtures/nocase.txt`, sha256 `fdac4996...`, built in scratch under
`/fast/scratch/hyaku/kengaku-r66/FreezeReview/`, then):

    $ python3 plans/round66_c1_tensor_probe.py --check-receipt <scratch>/nocase.txt; echo $?
    CHECK ok cases=5
    PREDICATE R66-C1 pass
    0

Same class of gap as kill rule (d)'s K2 hole, which the counter *did* close for VECTOR
lines (`for case in CASES: if case not in seen: problems.append(...)`). The C2
named-limitation paragraph calls the C1 per-case junit binding "the stronger check" —
as implemented it is circumventable by omission, so the stronger-check contrast is not
earned. Verdict: the **code** is wrong (or the predicate text overstates enforcement);
add a "every CASE must be present" rule mirroring the VECTOR rule. Reported, not edited.

### F2 — MUST-FIX (R66-C2, text wrong for the receipt that exists): the strict `PROBE` sha clause is unsatisfiable — the committed R65 receipt carries no PROBE sha line

Frozen strict requirement: "the receipt's `PROBE` sha equals the committed
`plans/round65_c1_sqlite_probe.py` bytes at the strict run's revision" and "A receipt
missing any of these ... exits 1". The committed R65 receipt has no `PROBE sha256=` line:

    $ grep -n -E 'PROBE|instrument' corpus/evidence/round65/sqlite-gcov-probe.txt
    2:# instrument plans/round65_c1_sqlite_probe.py version=r65-c1/1

The `# instrument` comment names a version, not a sha256 of the probe bytes; there is
nothing for strict to compare. Implemented literally, `--strict` must refuse the committed
receipt → kill rule (b) fires ("strict refuses the committed R65 receipt → the strict
predicate is wrong for the receipt that exists"). Dropping or softening the clause means
the text is not implemented. The claims text and the receipt that exists are inconsistent;
one of them must move before C2 can be admitted, and the text is frozen — so this must be
surfaced now, not after the run.

### F3 — SHOULD-FIX (R66-C2, text under-determined): the strict `TOOLCHAIN` clause is circular; refusing the fabricated fixture hinges on the undefined word "well-formed"

Frozen text: "`TOOLCHAIN` values equal the values the receipt itself carries for
gcc/gcov/bwrap/python and are well-formed". A value trivially equals what the receipt
carries — as written the clause is vacuous. The fabricated receipt
(`corpus/evidence/round66/red/fabricated-r65.txt` line 4) reads
`TOOLCHAIN gcc=fabricated gcov=fabricated bwrap=fabricated python=fabricated`, which
satisfies the default gate's own well-formedness standard
(`round65_c1_sqlite_probe.py:681-686`: non-empty and not `(none)`). Every other strict
clause (GRADER sha, AMALG sha, VECTOR table, NOBIND G1–G5 `delta=0` — the fabricated
receipt carries 5 `delta=0` lines) is copied correctly by the fixture. So the only literal
clause that can refuse it is "well-formed" — undefined in the claims. If the builder
implements well-formed as the default gate does, kill rule (a) fires (strict accepts the
fabricated fixture). Pin the definition (e.g. version-pattern match, or TOOLCHAIN must
agree with the receipt's `CC`/`GCOV`/`BWRAP` detail lines, which the fabricated fixture
lacks) in the strict implementation and say so in the round report.

### F4 — SHOULD-FIX (R66-C1, text/code classification mismatch): kill rule (b) is not enforced as written — a K1 vector mismatch yields a FAIL verdict (exit 1), not SETUP could-not-evaluate (exit 2)

Frozen kill rule (b): "K1 is not 13/13 P → SETUP-level failure of the reference, the claim
is not evaluated". Code: `verdict_lines` treats a K1 vector mismatch like any other vector
mismatch → `PREDICATE R66-C1 fail`, `cmd_run` returns 1 (`round66_c1_tensor_probe.py:241-243,
281-282`); `check_receipt` likewise reports a `CHECK defect` and exits 1. No path maps a
K1-only mismatch to `setup_error`/exit 2, and kill rule (c)'s SETUP-cause list does not
include it. Both readings refuse admission, but the contract's label and exit code differ
from the code. Either the rule text or the code classification is wrong; report-side fix
required (record in the round report which side moved).

### F5 — MUST-FIX (R66-C1, text factually false as executed; frozen artifact mutated): junit is receipt-PARENT-local, not receipt-local, and the post-freeze run overwrote the frozen junit directory

Pre-freeze honesty says: "the junit directory is receipt-local, so a re-run cannot
overwrite committed junit bytes", and the freeze lists `corpus/evidence/round66/tensor/junit/`
among the frozen artifacts. `cmd_run` copies junit to `receipt.parent / "junit"`
(`round66_c1_tensor_probe.py:231-234`). The receipt of record and the control receipt share
one parent (`corpus/evidence/round66/tensor/`), so the post-freeze scoring run
(`receipt.txt`, mtime 18:04; `junit/*.xml` mtimes 18:03–18:04; `prefreeze-run2.txt` 18:02)
overwrote the bytes the frozen control names:

    $ python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/prefreeze-run2.txt; echo $?
    CHECK defect: k1-ref junit_sha does not match committed junit bytes
    CHECK defect: k2-none junit_sha does not match committed junit bytes
    CHECK defect: k3-stub junit_sha does not match committed junit bytes
    CHECK defect: k4-col-nogather junit_sha does not match committed junit bytes
    CHECK defect: k5-row-noreduce junit_sha does not match committed junit bytes
    PREDICATE R66-C1 fail
    1

Consequences: the "cannot overwrite" sentence is false; a listed frozen artifact now holds
the receipt-of-record's bytes; the pre-freeze control is no longer re-derivable from
committed bytes. C1 admission itself is intact — `receipt.txt` binds the *current* junit
bytes and the counting command passes (see F9) — but the round report must not repeat the
"receipt-local" sentence as fact, and the control-receipt binding should be disclosed as
broken (or the receipt of record re-homed to a receipt-specific junit path before scoring).

### F6 — NOTE (R66-C1, claims sentence false on disk, inert): `prefreeze-run1.txt` still exists although the claims say it was removed

Claims: "The superseded first-run receipt was removed unscored."
`corpus/evidence/round66/tensor/prefreeze-run1.txt` exists (mtime 17:56, PROBE
`2a6aaacc98d19528...` — the pre-fix probe). It is inert: the counter refuses it:

    $ python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/prefreeze-run1.txt | head -1
    CHECK defect: probe sha does not match the committed probe

Either delete it (lane housekeeping, not this seat) or correct the sentence.

### F7 — NOTE (R66-C1, diagnostics): unknown case name in a VECTOR line crashes `check_receipt` with an unhandled KeyError instead of a named finding

    $ python3 plans/round66_c1_tensor_probe.py --check-receipt <scratch>/bogus.txt 2>&1 | tail -1
        if any(vec.get(k) != FROZEN_TABLE[case][k] for k in KEYS):
    KeyError: 'bogus'

(fixture `attack-fixtures/bogus.txt`, sha256 `143fda8f...`). Exit is 1 either way, so no
admission risk; but the refusal is a traceback, not a `CHECK defect:` line. One guard
(`if case not in FROZEN_TABLE: problems.append(...); continue`) fixes it.

### F8 — NOTE (status, R66-C2): the strict counting commands do not run at HEAD; both default commands run exactly as claimed

At HEAD `plans/round65_c1_sqlite_probe.py` has no `--strict` (argparse: `--lane --work
--receipt --check-receipt --selftest --render-table`):

    $ python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round66/red/fabricated-r65.txt --strict; echo $?
    round65_c1_sqlite_probe.py: error: unrecognized arguments: --strict
    2

(same for the committed receipt: exit 2). Expected mid-wave — the build seat lands strict.
Current default-mode state, both as the claims predict:

    $ python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round66/red/fabricated-r65.txt; echo $?   → CHECK ok cases=5 / PREDICATE R65-C1 pass / 0   (the M-1 defect, still live)
    $ python3 plans/round65_c1_sqlite_probe.py --check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt; echo $?    → CHECK ok cases=5 / PREDICATE R65-C1 pass / 0   (regression pin holds)

Post-strict rerun must show: fabricated `--strict` → exit 1 with a named finding;
committed `--strict` → exit 0; committed default → byte-identical behavior. Given F2/F3,
strict cannot satisfy both kill rules (a) and (b) under a literal reading — the build seat
should read F2/F3 before implementing.

### F9 — VERIFIED (no defect): predicate ↔ code equivalence, kill rules, K2 isolation, case diffs, counting commands

- **(a) Predicate sentences match the code conditions and labels.** `frozen()`
  (:63-83) yields exactly the claims table: K1 all P; K2 all F; K3 `exists` P rest F;
  K4 `exists` P + row all P + column ws1 P / ws2,ws4 F; K5 mirror on row. Labels identical:
  the claims' after-command output `CHECK ok cases=5` + `PREDICATE R66-C1 pass` exit 0 is
  printed verbatim by `cmd_check` and observed live on the receipt of record:
  `python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt; echo $?`
  → `CHECK ok cases=5` / `PREDICATE R66-C1 pass` / `0`.
- **(b) Kill rules implementable and enforced:** (a) enforced at run (`verdict_lines`
  frozen-table compare) and at check (per-line table compare; a mutated line is flagged
  even if a later duplicate line matches — `seen` last-wins but problems are appended per
  line); (c) enforced (`setup_error` exit 2 on grader-sha drift :216-217, missing venv
  :218-219, port 12355 busy before each case :224-225, missing junit :180-181);
  (d) demonstrated below; (e) enforced via the `case_sha` committed-bytes binding — with
  the F1 caveat. R66-C2 kill (c) (default unchanged) verified at HEAD. R66-C1 kill (b) —
  see F4. R66-C2 kills (a)/(b) — see F2/F3.
- **(c) K2 alone cannot meet R66-C1** — demonstrated, not assumed:
  `python3 plans/round66_c1_tensor_probe.py --check-receipt <scratch>/k2only.txt; echo $?`
  (fixture `attack-fixtures/k2only.txt`, sha256 `40d58133...`) →
  `CHECK defect: k1-ref has no VECTOR line` … (all four) … `PREDICATE R66-C1 fail`, exit 1.
- **(d) Universal clauses:** VECTOR-side "every CASE must be present" is enumerated
  (`:262-264`); the case_sha/junit_sha "every" is NOT (F1). R65 strict's "each VECTOR line"
  and "each NOBIND G1–G5 with delta=0" are implementable — the committed receipt carries
  `grep -c 'delta=0'` = 5; the default gate checks NOBIND presence only (:748-751), strict
  adds the delta check.
- **(e) One-method-body claim holds.** `diff -u k1-ref k4-col-nogather`: docstring hunk +
  one hunk replacing `ColumnParallelLinear.forward`'s body with
  `return F.linear(x, self.weight, self.bias)`. `diff -u k1-ref k5-row-noreduce`:
  docstring hunk + one hunk deleting the `all_reduce` block from
  `RowParallelLinear.forward` (bias add retained). Exactly one *method body* each; K3 is a
  full-file stub by design (the one-body claim covers K4/K5 only). The mutants' shapes
  match their frozen vectors: ws=1 untouched (no gather/reduce needed), ws∈{2,4} wrong.
- **(f) Counting commands, exit codes (all run as written, from the lane root):**
  R66 after → 0 (F9a). R65 before (fabricated default) → 0. R65 after-1/after-2 (strict)
  → 2 at HEAD (F8). R65 after-3 (committed default) → 0.
- **Bindings:** probe sha256 = `c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3`
  (committed file, and the `PROBE` line of both `prefreeze-run2.txt` and `receipt.txt`) —
  matches the claims sentence. Grader sha256 `4ae4285e...` = SHA256SUMS line 171 = capture
  `corpus/evidence/round66/sources/torch-tensor-parallelism-test_outputs.py` =
  `GRADER_SHA256` in the probe. Grader defines 13 tests (1 `test_parallel_linear_exists` +
  2 parametrized × bias{True,False} × world{1,2,4}); `key_of` extracts bias/ws
  order-independently from pytest ids; grader sets `MASTER_PORT=12355` itself (line 31),
  so the probe's lock/port-busy discipline is the right one. K2's `CASE rc=1` claim matches
  `prefreeze-run2.txt` line 6. Before-evidence matches: `grep -c torch-tensor-parallelism
  corpus/evidence/round52/graders/executed17.lst` → 0 (rc 1); class-survey line 14 names
  the class, line 21 `EXECUTED-COVERAGE ... classes-uncovered=network-service,process-environment,...`.
- **Frontier quotes grep -F-able in their captures (calibration):** S183 quote → 1 hit;
  S233 `sqlite-amalgamation-3540100/sqlite3.c` → line 5, same line carries `9582521`;
  S234 quote → 1 hit. All three frozen located quotes stand.

## Residual risk and verification gaps

- The receipt of record (`receipt.txt`) already exists at HEAD with PREDICATE pass. I did
  not re-run the probe (`--run`) — that is the runner seat's job; my verdicts on the
  receipt are re-derivations, not fresh executions. The K1 13/13 result is taken from the
  committed receipt + its matching junit bytes, not re-measured.
- F1's no-CASE receipt and F7's unknown-case receipt are forgeries I constructed; no lane
  receipt contains them. If the orchestrator wants the F1 fix counter-verified post-fix,
  rerun `--check-receipt attack-fixtures/nocase.txt` and require exit 1.
- I did not audit `cmd_selftest` coverage beyond reading it: it mutates a vector and copies
  junit, but never exercises a receipt missing CASE lines (F1) or an unknown case name
  (F7) — the selftest would not have caught either.
- TOOLCHAIN-pin ambiguity (F3) and the strict discriminator set were analyzed statically at
  HEAD; the built `--strict` may resolve them differently (better or worse). The two
  must-fix items F1/F2 should be adjudicated before C1's receipt is scored / C2's strict is
  reviewed against the claims text.

Seat artifacts written: `.ufo/waves/round-66/w1/FreezeReview/findings.md` (this file),
`.ufo/waves/round-66/w1/FreezeReview/attack-fixtures/{k2only,nocase,bogus}.txt`,
and the Report copy at `.ufo/waves/round-66/w1/FreezeReview.md`. Scratch
`/fast/scratch/hyaku/kengaku-r66/FreezeReview/` removed before yield. No lane file edited;
no tool installed; no network used.
