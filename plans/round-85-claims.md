# kengaku round 85 — frozen claims

2026-11-04, hyaku run 15, attempt 1; L1 KengakuR85 holds the planner seat. All times UTC unless an offset is written.
Base revision: `0de45354d7aff18e4a23a348ec13de3a1f707a44` (master, round-84 closure tip; clean, ahead=0).
Two causally separable claims on two distinct axes. Coverage is the lowest non-retired axis (score 7, L0 cap
`kengaku | round-25/33/51` still open, nothing assumed answered); calibration is 10 (held at ceiling, exercised).
No stagnation waiver. No novelty construct, score increase or serving-plane claim is made.

This round's frozen inputs are committed IN THIS FREEZE COMMIT, not in a later instrument commit: the case table
`plans/round85-cases.json` and the defect list `plans/round85-defects.json` are part of the freeze tree, so a
counter that reads them from `FREEZE_REV` fails closed at exit 2 when they are absent (R84-V2's repair).

## R85-C1 — coverage: third offline replay, `sqlite-db-truncate` (first `serialization-schema` member)

Predicate R85-C1: the base-unexecuted `sqlite-db-truncate` member has exactly one located, host-pinned receipt
`corpus/evidence/round85/sqlite-db-truncate-probe.txt` whose frozen eight-case table (`plans/round85-cases.json`)
reproduces the captured grader's single test function with zero mismatches on a two-leg vector (leg `score`: the
set-intersection cardinality; leg `verdict`: the grader's `score > 6` pass/fail), and the population ledger marks
that receipt executed in round 85.

Subject: `corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py`, sha256
`8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881` (ledger pin prefix `8f5bc11018687d8c`;
the live pinned URL returns these bytes, opened this round). One function: `test_json_data` — reads
`/app/recover.json` as JSON, builds `{(word, value)}` sets from the hardcoded eight-item `soln` list and from the
data, and asserts `len(soln_tuples & data_tuples) > 6`. The grader runs unmodified inside bubblewrap: `/usr` and
`/etc` read-only, the case directory bound as `/app` with the case's `recover.json`, the grader read-only at
`/tests`. No reimplementation of the assertion, no function patch, no mocked `open`/`json`, no host `/app` write.
AssertionError or FileNotFoundError = F; normal return = P; any other exception = setup defect (a defect, never a
red witness).

The score leg is observed inside the same sandbox by a harness that imports the captured module with `runpy` and
counts `len(soln_tuples & data_tuples)` from `/app/recover.json` — the grader's own `soln` data and Python's own
set semantics, no reimplementation of the threshold. The verdict leg is the real `test_json_data()` return.

Frozen case table (`plans/round85-cases.json`; predicted vector `score/verdict`):

| id | staged `/app/recover.json` | predicted |
|---|---|---|
| exact8 | all eight solution pairs | 8/P |
| seven | seven pairs (drop `testword09`) | 7/P |
| six | six pairs (drop `testword08`, `testword09`) | 6/F |
| empty | `[]` | 0/F |
| extras | all eight pairs plus four non-solution pairs | 8/P |
| duplicates | each of the eight pairs twice (16 rows) | 8/P |
| string-values | eight words, values as JSON strings (`"10.0"` …) | 0/F |
| int-values | six words with integer values (`10`, `25`, `42`, `50`, `75`, `99`) | 6/F |

The table discriminates: set semantics (duplicates 8, not 16), extras tolerance (extras 8), the strict `> 6`
boundary (7/P vs 6/F), type sensitivity (string values 0), and int/float equality (ints match floats, 6/F).

Counter: `python3 plans/round85_c1_replay.py --lane . [--rev REV] --work DIR`. Probe tool:
`plans/round85_sqlite_truncate_probe.py` (`--lane DIR --work DIR`); the instrument prints
`CASE <id> predicted=<score>:<P|F> observed=<score>:<P|F>`, `cases=8 legs=16 mismatches=0`, and
`PREDICATE R85-PROBE pass`.

Target: `TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0`,
`PREDICATE R85-C1 pass`, exit 0.
Before (BASE `0de45354`): `TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects>=1`,
`PREDICATE R85-C1 fail`, exit 1. Counting outputs at BASE and after are the population-gate figures:
executed 28 → 29, unexecuted 60 → 59; `serialization-schema` class executed 0 of 9 → 1 of 9.

Receipt stamp (all required): MEMBER, SUBJECT_CAPTURE, SUBJECT_SHA, CASE_TABLE_SHA, TOOL, TOOL_SHA,
HOST_PYTHON, HOST_OPENSSL, LANE_TIP, WORKTREE clean, COMMAND (reconstructed argv, never executed from the
receipt), EXIT 0, and an OBSERVATIONS_BEGIN/END block.

Controls, executed before any real scoring and committed as receipts: do-nothing (no receipt at the revision),
ledger-only (executed flag, absent receipt), fabricated observations (complete stamp, wrong CASE vectors), and
**forged correct-vector receipt** (a receipt whose stamp and vectors are all valid but whose observation block was
not produced by the tool's run — rejected by the counter's unconditional REPRODUCE leg). Each must print
`target_reached=False`. Mutants of the counter must each be killed with a finding-specific nonzero exit.

Kill rule: any observed vector ≠ predicted, any setup exception, any missing receipt field, any control reaching
target, any receipt whose subject sha differs from the pin, or a REPRODUCE run whose observation block differs
from the receipt's → claim fails at that revision (honest stop, no retune).
Exit codes: 0 pass, 1 fail, 2 could-not-evaluate.

Sourced claim: the subject is cited to a new `corpus/SOURCES.md` row S272 (the pinned upstream
`sqlite-db-truncate/tests/test_outputs.py`, opened 2026-11-04 at the pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`),
recorded in `corpus/lessons/round-85.md` Gate. The row supports member replay only, not a solved-task or model
claim.

## R85-C2 — calibration: the eight owner-routed round-84 defects discharged with a base-sensitive gate

Motivation: the outside round-84 closure (`corpus/lessons/round-84-verifier-spotcheck.md` §Routed defects) routed
R84-V1, V2, V3, V5, V6, V7, V8 and V9 to this lane while its report claimed nothing carried; R84-V4 is
operator-owned (open L0 `kengaku | round-84`) and is named, never counted.

Predicate R85-C2: each of the eight owner-routed ids carries (a) a substantive repair in the measured tree,
(b) a check that exits 0 at the measured revision, and (c) a demonstrated red at BASE `0de45354` when the same
check is run against it; `plans/round85-defects.json` lists the eight ids and the check names, and the counter
`plans/round85_c2_debt.py` is the executable form of (b) and (c).

The eight checks (each defects-specific, never a generic presence test):

| id | repair | check (red at BASE) |
|---|---|---|
| R84-V1 | `.ufo/waves/round-84/w1-results.json`, `w1/CriticR84.md`, `w1/CriticR84/critique.md`, `w1/CriticR84/report.txt` are tracked | `git cat-file -e REV:<path>` for all four |
| R84-V2 | `plans/round85-cases.json` and `plans/round85-defects.json` exist at `FREEZE_REV`, and the C1 counter exits 2 (SETUP) when the freeze tree lacks them | freeze-tree presence + a SETUP fixture run |
| R84-V3 | the C1 counter's REPRODUCE leg is unconditional and the forged-receipt control is rejected | `--control-forged-receipt` prints `target_reached=False`, exit 1 |
| R84-V5 | `corpus/QUALITY.md` gains the row the round-84 freeze promised (the considerthese §2 criterion) | the row exists with its citation and its executable form |
| R84-V6 | the held entry's `writer:` no longer equals a seat id; the Q13 checker's line-start author rule is exercised | entry writer not a seat id + checker selftest green |
| R84-V7 | the round-85 lesson and report carry `expansion: unchanged` and a dated correction of the round-84 grade | the correction line names R84-V7 in the lesson |
| R84-V8 | the carried red plans-registry gate is green (the round-83 counter's flag spelling made literal) | `round82_c1_plans_registry.py --lane .` → `PREDICATE R82-C1 pass`, exit 0 |
| R84-V9 | the C2 before-revision is an existing revision (BASE) and the future-file condition is priced in the lesson | the lesson's definition-horizon line names BASE and prices absent future files |

Target: `TARGET ids=8 closed=8 checks_passed=8 indexed=yes defects=0`, `PREDICATE R85-C2 pass`, exit 0;
sensitivity: `SENSITIVITY n=8 failed_at_base=8`, exit 0.
Before (BASE): `TARGET ids=8 closed=0 checks_passed=0 indexed=no defects=8`, `PREDICATE R85-C2 fail`, exit 1.

Counter: `python3 plans/round85_c2_debt.py --lane . [--rev REV] --work DIR` (`--selftest`, `--mutants`,
`--control-presence`, `--sensitivity`).

Kill rule: any remaining defect, any check green at BASE (base-insensitive), a repair that is prose only, or an
`indexed=no` → claim fails. Frozen claim sentences, the defect list, the counters' predicates and the targets are
not edited after the wave scores.

## Frontier and wave contract (round 85)

- Shape: ONE v1 wave, 12 seats, policy `scripts/hyaku/ufo-wave-policy.json` (band 8–16). Attack seats (reviewer ×2,
  critic, mutation-tester) = 4/12 (≥25 %). Connector seats: 1.
- Planner seat: the L1 (KengakuR85). A bounded data walk rides the scout (`ScoutR85`).
- Routing via `task.agentModelOverrides` only; no model passed.
- Considerthese: `considerthese/2026-10-26.md` §Self-improvement suggestions 2 (one standing TB2 admission counter
  with a built-in filler control). Mined now in the form R84 promised and did not land: a QUALITY criterion whose
  executable half is the admitted entry's own counter with a committed filler/junk package that must stay red.
- Assimilation: none. `merge/kengaku/` (175 staged rows, 65 knowledge entries) is not drawn on by these frozen
  claims; it remains unadopted backlog.
- Mistake mined: R84-V2 (a frozen input committed after its freeze revision, making the counter's freeze anchor
  inert). Evidence: `corpus/lessons/round-84-verifier-spotcheck.md` §R84-V2; captured-by: none (no criterion
  required the frozen input to exist at the freeze revision). Fix: this freeze commit carries the table and the
  defect list, and the C1 counter fails closed (exit 2) when they are absent at `FREEZE_REV`.
