# kengaku round 94 — frozen claims

Frozen at commit F of round 94 (the single commit that adds this file). Author: kengaku (L1
KengakuR94, hyaku run 15, attempt 1). Base: `0cbb927914e07818e1aaee7e72d8b3c90a2d21c2` (lane tip at
round start; clean, pushed; round 93 admitted, MANIFEST index 1388). P0 mechanism predictions and
capture: `bdcb1ec06434adfdea25823a2fb90f33bcf1dc5c`. Instruments P1:
`997a6fe5fbb4a4af9f38e436bccd8f604da1d746`. Control receipts P2:
`74b3d2a1e88112763a06a2bdbdfb7ee14a531f55` (`.ufo/waves/round-94/L1/controls/`).

Order (the round-93 discipline, kept): P0 predictions → P1 every instrument → P2 every do-nothing,
forgery and sandbox control executed against P1 and committed → F this file with the sha256 of
every instrument → the official probe run, ledger flip and SOURCES rows → measurement. **No file in
the table below changes after F.** An instrument defect found after F is routed to round 95 and
the affected claim is reported not met; it is never repaired in round.

```frozen-instruments
3e1e17641ff6737fda8b72d05819106aecd3861b2a8d711ee765c513c90995cb  plans/round94_compressor_probe.py
e3c0c0eaef0f1d04319683970a2e9ef10df8be656f79368d797399ff4691d394  plans/round94-cases.json
ff6a6e4622c56fe8f4de41dfbddcd1f9d90f9b98fa2f99bac0c1bd22447872d9  plans/round94_c1_replay.py
8574b4d5dca7f3817f1beb42c024c80791a0b958b04da94361e9e2a6cc4964de  plans/round94_freeze_integrity.py
17d2a7d52fbd703db1c4df661168f22a36481f289962ea66d5e98a0466190b98  plans/round94_c2_counter.py
809f486053e3ffbce852111dee1f63d80ab31297bd33172389e50278bed384e2  corpus/evidence/round94/graders/write-compressor/tests/test_outputs.py
7f8d9ef66943f912a217aa48f4ef5efc967b44c2b21d0f56df029b5ab413f62a  corpus/evidence/round94/graders/write-compressor/tests/original-decomp.c
0fc483d0fb31128dfa41ed11adca56c88688888189826ef9daeafd7559b4fa4e  corpus/evidence/round94/graders/write-compressor/tests/original-data.txt
01550b7de7ab1320b1898eae055226bb7c73bee259c75102d2240c974a730409  corpus/evidence/round94/graders/write-compressor/solution/solve.sh
7f8d9ef66943f912a217aa48f4ef5efc967b44c2b21d0f56df029b5ab413f62a  corpus/evidence/round94/graders/write-compressor/environment/decomp.c
0fc483d0fb31128dfa41ed11adca56c88688888189826ef9daeafd7559b4fa4e  corpus/evidence/round94/graders/write-compressor/environment/data.txt
```

## Round shape (declared before dispatch)

One v1 wave (band 8–16), ≥25 % attack seats, ≤2 connector seats, dispatched after the
measurement. The §3 planner seat is held by the L1 (validator rule). No `model` is passed; routing
is the host table. Wave findings are routed, not repaired (frozen rule above).

## R94-C1 — coverage (the lowest-scoring non-retired axis; held at its L0 cap 7)

**Claim.** A twelfth located offline replay of a pinned Terminal-Bench 2.0 grader:
`write-compressor` @ `2fd12b88` (classes `file-artifact`, `stdout-inspection`, `subprocess-exec`),
replayed through `plans/round94_compressor_probe.py`: the reference `data.comp` is rebuilt offline
from the captured `solve.sh` heredoc with the host `rustc`, then 8 cases × 4 observed legs (the
outcome of each of the grader's three test functions, and the staged `data.comp` size); the
population ledger flips the member to `executed` (round 94).

**Frozen predicate.** At the measured tip T:
`python3 plans/round94_c1_replay.py --lane . --rev T --work DIR` prints
`LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass`, then
`TARGET executed_rows=38 member=write-compressor located=1 executed=1 cases=8 legs=32 mismatches=0 defects=0`,
then `PREDICATE R94-C1 pass`, exit 0. Ledger after (L7, from the committed ledger): executed
37 → 38 of 88, `file-artifact` 28 → 29 of 76, `stdout-inspection` 12 → 13 of 29,
`subprocess-exec` 14 → 15 of 45, and the executed member set equals BASE's plus
`write-compressor` (no swap).

**Predictions.** Filed from mechanism at P0 before any probe run
(`.ufo/waves/round-94/L1/predictions-mechanism.txt`): 7 of 8 vectors held in the dry runs; C08
(one inverted byte) was predicted `P,F,P,2264` and observed `P,E:UnicodeDecodeError,P,2264` in
dry runs 1–3 — the grader's own `subprocess.run(..., text=True)` raises on the corrupted output
before its assertion runs. The frozen table carries the observed vector and says so in the case
`why`. Decisive semantic legs: C04 (tampering with /app/data.txt and /app/decomp.c cannot change
the verdict: `setup()` restores both from /tests), C06 (the decoder stops before trailing padding,
so round-trip and size are independent walls), C08 (above).

**Controls (executed against P1, committed at P2).** do-nothing at BASE and at P1: all nine legs
fail, rc 1; ledger flip without a receipt: only L7 passes, rc 1; class-matched member swap
(aggregates kept): L7 fails on the member set, rc 1 (round-93 W-5); sandbox outage
`--bwrap /nonexistent/bwrap`: could-not-evaluate, rc 2.

**Source (sourced claim, CORPUS rule 1).** New rows for the grader, the two staged originals,
the reference solution and the environment files, all opened 2026-11-05 at `2fd12b88` (HTTP 200,
byte sha256 equal to the table above); `tests/test.sh` and the task's Dockerfile are opened and
rejected as replay inputs (network installs; image build).

**Kill rule.** Any failing leg, any DEFECT line, any mismatch, or `executed_rows` ≠ 38 at the
measured tip fails the claim; could-not-evaluate (rc 2) is not met. A mispredict is recorded,
never repaired.

## R94-C2 — calibration (held at ceiling 10)

**Claim (calibration content).** The lane's round-93 self-assessment said its freeze-integrity
counter discriminates forged gates ("four forgeries rc 1", `plans/round-93-claims.md`, SCORECARD
round-93 row). Observed at BASE: the frozen round-93 counter passes **5 known false gates** (three
round-93 seat forgeries x-head-not-rev, x-diff-rev-minus-1, x-table-at-rev; surviving mutants m06,
m13): `PREDICATE R93-C2 pass`, rc 0 for each (`controls/before-r93-counter-*.txt`). The admitted
capability row also states a property its gate does not hold (TREESAME-merge false intact, second
table block ignored, duplicate rows double-counted — W-2/W-3/W-6). After: gate v2
(`plans/round94_freeze_integrity.py`) closes those three, and the round-94 counter turns each of
the 5 known false gates red at its own designated fixture (P2 receipts), and kills the same 7
attacks re-made as CLI-path mutants of v2 itself (W5). Known false gates passing the lane's
counter: **5 → 0**.

**Frozen predicate.** At the measured tip T:
`python3 plans/round94_c2_counter.py --lane . --rev T --work DIR` prints `W1 pass`, `W2 pass`,
`W3 pass`, `W4 pass`, `W5 pass`, `TARGET legs_passed=5 of 5`, `PREDICATE R94-C2 pass`, exit 0,
where (the counter's docstring is the full definition): W1 = round-92 history broken=3 intact=1
rc 1 AND round-93 history 9/9 intact rc 0; W2 = 12 counter-owned fixtures through the CLI; W3 =
`SELFTEST cases=15 ok=15` in both W1 runs, echoed; W4 = this file's own table at T, freeze = the
single commit adding this file, instruments ≥ 8, broken=0, rc 0; W5 = null CLI copy keeps 12/12
fixtures and mutants K1–K7 are each killed at their designated fixture.

**Controls (executed against P1, committed at P2).** do-nothing at BASE: 0 of 5, rc 1; positive:
real gate at P1 passes W1, W2, W3, W5, fails W4 only (`claims-add-commits=0`); cheapest control —
the round-93 gate offered as v2: fails (TREESAME, second block, duplicate row RED; W3; W5 anchors);
each of the 5 known false gates: rc 1 with its designated fixture RED.

**Kill rule.** Any W leg failing at T fails the claim. Edits to any tabled file after F make W4 fail
by construction.

## Separability

C1 is verifiable without C2 (its counter reads this file's table but not the gate); C2 is
verifiable without C1 landing (W1, W2, W3, W5 read no C1 artifact; W4 reads only tabled bytes,
which exist at F before the C1 receipt and ledger flip).

## Not claimed (carried, with pointers)

Round-92 gate v3 defects (override vacuity `plans/round92_burndown.py:306-329`, marker skip
`:445`/`:558`), the unpinned round-92 counters, and the unguarded sibling
`cost_model_for_tests.py` stay open and are carried in the round-94 lesson. The round-93 closure's
conformance items 1, 2 and 6 (SKILL.md registry row, `## Capabilities` row, SELFTEST echo) are done
this round without a claim slot; item 6 is W3's echo.
