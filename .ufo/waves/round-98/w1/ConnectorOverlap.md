# ConnectorOverlap — round 98 (cross-claim and cross-lane scan)

Seat: ConnectorOverlap (leaf, no dispatch). Lane `kengaku-shokunin`, round 98.
BASE `49a1c4f1097db7c923da56d4213cad75772ed1c0`; F `e1a3afd9069a19e38fd0bc3b015970231f303fc7`;
T `8e37fc65d5649bb37166fdd6b1657445a8cb55b9`. All work in a `git clone --shared` detached at T
under `/fast/scratch/hyaku/kengaku-r98/ConnectorOverlap/`; no lane edit, no commit, no task call.
Receipts: `.ufo/waves/round-98/w1/ConnectorOverlap/`.

**Verdict in one line.** C1 and C2 touch disjoint bytes; no sibling lane overlaps either claim;
C1's ledger flip and L10 and C2's predicate all reproduce independently at T; **one unstated
second-order effect**: `corpus/evidence/PROVENANCE.md` clears **two rows outside C2's 39-row
population** through the gate's *pre-existing* `provenance-url` rule, so the gate's defect count
falls by 41, not 39. The frozen predicates are not falsified by it (K7 is a subset test), but the
`GATE defects base=… rev=…` line is not a clean measure of C2's effect and must not be cited as one.

---

## 1. C1 and C2 touch disjoint bytes inside the shared candidate files

`git diff -U0 e1a3afd9 8e37fc65` = 5 files, +114/−5. Per-hunk attribution:

| file | hunk | lines | claim | note |
|---|---|---|---|---|
| `SKILL.md` | `@@ -74 +74 @@` | 1 | **C1** | `file-artifact` 32 → 33 of 76 |
| `SKILL.md` | `@@ -84 +84 @@` | 1 | **C1** | `serialization-schema` 7 → 8 of 10 |
| `SKILL.md` | `@@ -705,0 +706,4 @@` | 4 | **MIXED 2/2** | 706–707 C1 (`round98-regexchess-probe`, `round98-c1-replay`), 708–709 C2 (`round98-c2-nested-bind`, `round98-provenance-build`) |
| `corpus/SOURCES.md` | `@@ -341,0 +342,8 @@` | 8 | **C1** | S326–S333 |
| `corpus/evidence/PROVENANCE.md` | new | 52 | **C2** | 39-row binding table |
| `corpus/evidence/round98/regexchess-probe.txt` | new | 41 | **C1** | probe receipt, `LANE_TIP e1a3afd9` (= F) |
| `plans/grader-population-ledger.json` | `@@ -766,3 +766,7 @@` | 7 | **C1** | `regex-chess` flip |

Findings:

- **Line-disjoint, not hunk-disjoint.** The only shared candidate file is `SKILL.md`. Its three
  hunks are line-disjoint; the registry hunk is a single additive block of four independent table
  rows split 2/2 by claim. A per-hunk reading therefore reports one "mixed" hunk while per-line
  attribution is clean. No hunk rewrites a line the other claim owns, and no C1 edit is inside a
  C2-owned line (or the reverse).
- **The mixed hunk cannot move either predicate.** `grep -c SKILL plans/round98_*.py` → 0 for all
  four round-98 scripts, so neither counter reads `SKILL.md`. This is the same immateriality the
  claim records for the post-P2 registry-row amendment, re-measured here rather than taken on trust.
- **Shared read surface, scoped apart.** Both counters read `corpus/SOURCES.md`. C2's population is
  derived at BASE and K7 is explicitly restricted to rows present at BASE
  (`round98_c2_nested_bind.py:24-25`, `:251`), so C1's eight added rows cannot enter it; C1's L10
  is scoped to rows added after BASE and runs the *BASE* gate bytes (`:147-151`). Neither claim can
  move the other's numbers through SOURCES.md.
- **One real coupling, inert here.** C1's L10 executes the frozen gate over the T tree, which
  contains C2's `PROVENANCE.md` (the gate reads any file named `PROVENANCE.md`,
  `anchor_digest_check.py:263`). The coupling is inert for this round — no S326–S333 URL appears in
  the 39-row table (`grep -c regex-chess corpus/evidence/PROVENANCE.md` → 0) — but L10 is not
  byte-independent of C2, and a future new row sharing a bound URL would be.

## 2. Sibling-lane overlap: none

Read-only scan of `/home/vgpnk/Projects/shokunin/*-shokunin` (21 lanes: 20 siblings + this one):

- **No sibling replays Terminal-Bench `regex-chess`, or any TB grader.** No
  `*/corpus/evidence/*/graders` tree exists outside `kengaku-shokunin/`. The only `regex-chess`
  string outside the lane is `revenger-shokunin/.ufo/waves/round-98/w1/ConnectorOverlap/query_7_script_bom.log:2108`,
  a grep hit that *prints the kengaku capture path* — a read of this lane's bytes, not a replay.
- **No sibling carries a PROVENANCE-style binding.** `provenance-row` outside kengaku appears only
  in unrelated senses (a game-dev-2d cost note, a lore schema row, tabi ledger row counts). No
  sibling references `plans/anchor_digest_check.py` by path except fleet-level
  `.ufo/reports/round-*/kengaku.md` copies of this lane's own reports.
- **Same-name, different corpus.** `kaidoku-shokunin/tools/round-44/c2-counter.py` and
  `kama-shokunin/tools/round64-c2-counter.py` are their own anchor-digest counters over their own
  corpora; they share no bytes, no gate and no captures with this lane.
- **Prior scan, not prior work.** `kama-shokunin/.ufo/waves/round-76/w1/CON01Overlap.md` already
  catalogued this gate's C2 predicate from outside. It is a description; it executes nothing.

Execution overlap across lanes is zero. The only cross-lane traffic is read-only description.

## 3. Cheapest next replays among the 39 unattempted ledger members

Ledger at T: 88 members, 46 unexecuted = 39 `unattempted` + 3 `candidate-library-required` +
2 `browser-required` + 1 `vm-required` + 1 `external-db-required`.

**Uniform blocker, and it is the dominant cost.** All 39 unattempted captures are round-52
*tests-only*: exactly `tests/test.sh` + `tests/test_outputs.py`, with **no** `solution/solve.sh`,
`environment/Dockerfile`, `task.toml` or `instruction.md`. `regex-chess` was cheap because P0
captured all seven files flat; none of these 39 can run a captured positive control as-is. Each
needs an upstream fetch of the solution and environment at staging time (network before the probe,
as with the venv) before it can carry a claim of the C1 shape. That cost is identical for all 39,
so the ranking below is by *grader purity and environment weight*, not by capture completeness.

| # | member | grader | deps | why cheapest |
|---|---|---|---|---|
| 1 | `mteb-leaderboard` | 537 B, 2 tests | stdlib only | Two assertions on one line of `/app/result.txt`; the environment is a results table and the solution a filter — the smallest possible stage. |
| 2 | `crack-7z-hash` | 789 B, 2 tests | stdlib only | Exact-string assertion on `/app/solution.txt`; needs only a small password-protected archive and a brute-forcer for the positive control. |
| 3 | `count-dataset-tokens` | 467 B, 1 test | stdlib only | Single substring assertion on `/app/answer.txt`; smallest grader in the population, though the dataset+tokenizer make staging heavier than #1–#2. |
| 4 | `bn-fit-modify` | 5.9 KB, 9 tests | `pandas`, `scipy` (pip) | Highest leg count per unit cost: deterministic OLS fit plus a KS test, no system toolchain, no network at grade time. |
| 5 | `train-fasttext` | 1.1 KB, 2 tests | `fasttext-wheel`, `scikit-learn`, `numpy` (pip) | Threshold-based (accuracy > 0.62, model < 150 MB), pip-only, no system toolchain; cost is the `/tests/private_test.tar.gz` the capture does not carry. |

Next tier and why it is *not* cheap: `fix-ocaml-gc` (809 B stdlib grader, but the positive control
is an OCaml runtime build), `prove-plus-comm` (1.1 KB, but `coqc`), `qemu-startup` /
`qemu-alpine-ssh` (stdlib graders, VM), `git-multibranch` (needs nginx + sshd), `mailman`
(`smtplib` + `make`), `overfull-hbox` (LaTeX), `mcmc-sampling-stan` / `rstan-to-pystan` (Stan),
`extract-moves-from-video` / `pytorch-model-cli` / `sam-cell-seg` (torch), `winning-avg-corewars`
(`pmars`), `path-tracing*` / `gpt2-codegolf` / `custom-memory-heap-crash` (gcc).

Value note for the planner: #1–#3 are the cheapest to stage but are one- and two-assertion content
checks — they will locate few grading gaps. #4 buys nine legs for one pip install and is the best
coverage-per-cost item on the list.

## 4. What I re-measured at T (independent of the claim counters)

| check | result |
|---|---|
| C2 counter, `round98_c2_nested_bind.py --rev T` | `LEGS K1..K7=pass`; `TARGET pop=39 cleared=39 still=0 unbound=0 rows_changed=0 captures_changed=0 new_old_row_defects=0`; `PREDICATE R98-C2 pass`; rc 0 |
| gate at T | `rows=325 tokens=209 defects=45`; **zero** DEFECT lines for S326–S333 (C1's L10, confirmed without the C1 counter) |
| gate at BASE | `rows=317 tokens=201 defects=86` |
| ledger set equality | BASE executed 41 → T 42; `T−BASE = {regex-chess}`; `BASE−T = ∅`; exactly one member record changed; equals BASE+member |
| frozen instruments (13) | all match the `frozen-instruments` table byte-for-byte at T |
| candidate bytes (4) | all match the `candidate-bytes` table byte-for-byte at T |
| capture dir F vs T | identical 9 files; `README.md` and `SHA256SUMS` were present at F, not added by C |
| K5 independent | all 39 POP `SOURCES.md` rows byte-identical BASE→T |
| K6 independent | all 38 distinct POP captures byte-identical BASE→T; every POP token still equals the sha256 of its capture at T |

The C1 replay itself was run from the clone root against T with the pinned venv
(python 3.13.16, chess 1.11.2, pytest 8.4.1); its result is recorded in §5.

## 5. C1 replay at T — pass, exact frozen string

Run from the clone root, detached at T, grader venv pre-staged with the `test.sh` pins
(python 3.13.16, chess 1.11.2, pytest 8.4.1). Wall 654.56 s. Receipt
`ConnectorOverlap/c1-replay-at-T.txt`:

```
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass L10=pass
TARGET executed_rows=42 member=regex-chess cells=file-artifact:33,serialization-schema:8 set_equals_base_plus_member=1 located=1 executed=1 cases=12 legs=60 mismatches=0 new_rows=8 new_rows_flagged=0 defects=0
PREDICATE R98-C1 pass
```

The `TARGET` line is byte-identical to the frozen predicate in `plans/round-98-claims.md`
(checked as a literal substring, not by eye), and `rc=0`. This is an execution, not a receipt
re-read: mid-run the work tree held staged case directories (`w/rerun/cases/{C01,C04,C07,C11,C12,…}`)
and `w/rerun/runner.py`, and the 654 s wall is consistent with 12 grader re-runs; the counter
removes its work tree on exit. C1's set-equality leg agrees with the independent ledger diff in §4
(`T−BASE = {regex-chess}`, `BASE−T = ∅`), computed from `git show` without the counter.

## 6. Finding — PROVENANCE.md's URL column clears two non-population rows

The gate's defect count falls **86 → 45 (−41 lines)**, but C2's population is **39**. Exact
accounting (receipt `ConnectorOverlap/gate-delta.txt`):

- 39 POP rows fully cleared = 39 lines;
- **S230** fully cleared = 1 line;
- **S213** partially cleared = 1 of its 2 lines;
- 86 − 40 − 1 = 45. No new defects at T.

Mechanism, from the gate's own `--verbose` output at T:

```
BIND S201 capture=…/round52/graders/chess-best-move/tests/test_outputs.py by=provenance-row
BIND S213 capture=…/round52/graders/chess-best-move/tests/test_outputs.py by=provenance-url
BIND S234 capture=…/round52/graders/kv-store-grpc/tests/test_outputs.py  by=provenance-row
BIND S230 capture=…/round52/graders/kv-store-grpc/tests/test_outputs.py  by=provenance-url
```

`anchor_digest_check.py:344` (frozen bytes, K1-verified unchanged) binds **any** SOURCES row whose
`(repo, subpath)` appears in a `PROVENANCE.md` URL column — independently of the population. The
new file's `pinned URL` column is generated from the 39 POP rows, and two non-POP *supersedes* rows
share those URLs:

- **S230** (`kv-store-grpc`; BASE class `digest-wrong-capture`, declared locator
  `round52/graders/SHA256SUMS`) → cleared by `provenance-url`. S234's own row text says it
  "supersedes S230 form", so the clear is semantically defensible — but it is not C2's stated
  mechanism and not in K3/K4.
- **S213** (`chess-best-move`; BASE classes `token-outside-anchor` + `anchor-unbound`, row text
  "correction row superseding S201") → its `anchor-unbound` line cleared by `provenance-url`;
  `token-outside-anchor` survives, so the row stays defective and K7's subset test still passes.

Effect on the frozen predicates: **none**. K7 is a subset test over BASE rows and clearing is a
subset move; K3/K4 iterate POP only; K1/K5/K6 are unaffected (re-verified in §4). C2's predicate
passes exactly as frozen.

Effect on the claim's account: C2 says the file binds "each row … through the gate's
provenance-row rule" and names 39 rows. The measured blast radius is **41 defect lines over 41
rows, through two different gate rules**. The TARGET line and kill rule do not cover the extra two,
so the claim is not falsified — but the informational `GATE defects base=… rev=…` line is not a
measure of C2's effect and must not be cited as one in round 99 or in any later freshness argument.

Risk to carry forward: the URL channel is population-independent. Any future duplicate or
supersedes row sharing a URL with a bound row is cleared without being in the population, subject
only to its digest resolving. The P2 control battery exercised do-nothing, positive, partial,
row-edit, wrong-capture, gate-edit, capture-edit, c1only and both — **none exercised a duplicate-URL
row**, which is the one binding path this round did not control. That is the natural forgery control
for a future round, and the cheapest way to make the channel explicit rather than incidental.

## 7. Verdict

- **C1 (coverage):** **pass** at T, reproduced independently — all ten legs, the frozen `TARGET`
  literal, `rc=0`; ledger set equality re-derived from `git show` without the counter; S326–S333
  carry zero anchor-digest defects under the BASE gate bytes. No defect found.
- **C2 (freshness):** predicate **pass** at T, reproduced independently; frozen instruments, rows
  and captures unchanged (K1/K5/K6 re-verified outside the counter). One unstated second-order
  effect (S230, S213) that does not falsify the frozen predicate but does overstate the defect-count
  delta as evidence.
- **Cross-claim:** disjoint bytes; one mixed additive hunk in `SKILL.md` that no counter reads; one
  inert read coupling (C1's L10 executes the gate over a tree containing C2's file).
- **Cross-lane:** zero execution overlap; no sibling replays `regex-chess` or carries a
  provenance-style binding.
- **Ledger:** 39 unattempted, all tests-only captures; top-5 cheapest ranked in §3.

## 8. Bounded proposal (one move, both axes, no harm)

**Move.** For round 99, take `bn-fit-modify` as the next located replay (item #4 in §3) **and**
carry the duplicate-URL row as its paired freshness control: one SOURCES row that shares a bound
row's URL but is outside the population, with the gate's `provenance-url` binding asserted
explicitly rather than discovered.

- **Coverage axis:** `bn-fit-modify` is the highest leg count per unit cost in the unattempted
  population (9 tests, deterministic OLS + KS, pip-only `pandas`/`scipy`, no system toolchain, no
  network at grade time). It adds a `file-artifact` member with a numeric-band assertion, which the
  round-98 replay (`regex-chess`, file-artifact + serialization-schema) does not duplicate.
- **Freshness axis:** the §6 finding shows the URL channel is population-independent and was never
  controlled. Making it an explicit, asserted binding converts an incidental effect into a measured
  one and closes the one binding path the P2 battery left open.
- **Why not cheaper:** `mteb-leaderboard`, `crack-7z-hash` and `count-dataset-tokens` are cheaper to
  stage but carry one or two content assertions each — they would raise the replay count without
  locating a grading gap, which is the failure mode the coverage axis is supposed to punish.
- **Risks:** (i) all 39 captures are tests-only, so the positive control needs an upstream
  `solve.sh` fetch at staging — the same pre-probe network allowance the venv already uses, but it
  must be pinned and digested or the replay's provenance is weaker than `regex-chess`'s; (ii) the
  KS test is stochastic in principle — the grader's own comment says the fit is deterministic up to
  numerical precision over repeated runs, so the replay should pin the sample size and seed rather
  than assume; (iii) adding a duplicate-URL control touches `corpus/SOURCES.md`, which both claims
  read — it must land as a new row, never an edit to an existing one.
- **Verification:** the C1 shape (12 cases × 5 legs is not available here; `bn-fit-modify` has 9
  test functions and a reward leg → 10 legs) with `set_equals_base_plus_member=1`; and a freshness
  counter whose do-nothing control leaves the duplicate row defective and whose positive control
  clears it with `by=provenance-url` printed in the BIND line.
