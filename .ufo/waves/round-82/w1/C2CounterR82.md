# C2CounterR82 — R82-C2 counters delivered (closure-debt counter + repair checks)

Seat `C2CounterR82` (executor), kengaku round 82 wave w1. Claim: `plans/round-82-claims.md` §R82-C2
(frozen `12f1029a45cf0097a3afd030d757bf93b87f8018`). Base revision for every revert:
`a3a03ac31451e58f1742b9bccb73b72c2d90a95c`.

## Deliverables (byte-final)

| file | sha256 | lines |
|---|---|---|
| `.ufo/waves/round-82/w1/C2CounterR82.py` (integrates to `plans/round82_c2_closure_debt.py`) | `077f39c0cbe8451ba51438f283067bd46ae9045fec98990f4f2f669dfbbb2caa` | 556 |
| `.ufo/waves/round-82/w1/C2ChecksR82.py` (integrates to `plans/round82_c2_checks.py`) | `0a00d818e716569d36b26459bb588521b5d1b4b555db5fb366e68252d1aa3484` | 568 |

Both confirmed byte-identical (`cmp`) to the validated scratch copies. Stdlib only; both honour
`--work` and never write into the lane (all scratch under `/fast/scratch/hyaku/kengaku-r82/C2CounterR82`,
deleted after this report).

## Differences built vs the round-81 pair (as the item specified)

1. **Universe derived, never listed** — the counter scans the measured tree for
   `corpus/lessons/round-*-verifier-spotcheck.md`, picks the largest round number, and reads the
   `- **<X><n> · ` lines of that file's `## 5.` section; ids register as `R<round>-<X><n>` (round 81 →
   `R81-V1…V7`; the letter rides the file). No hardcoded round or id list. The stale/rename mutants
   below exist to kill any re-hardcoding.
2. **Sensitivity leg reverts to `a3a03ac3…`** — each closed row may name `evidence_path` (+ optional
   `reverted_state: "dir"` for deletion repairs like V5's stray directory): base blob restored when
   tracked at BASE, deleted when new, empty directory created when `dir`. A check still passing
   reverted is `CHECK-NOT-REPAIR-SENSITIVE`.
3. **`UNIVERSE spotcheck=<path> ids=7 <csv>`** printed every run, path derived.

Extra generality carried from the r81 code: `--rev REV` trees get a `.git` pointer so git-backed
checks (u1/u7 ancestor legs) work in archive copies; row close may name a tracked path or an
ancestor commit; trivial checks are `CHECK-TRIVIAL`.

## Evidence (commands + outputs)

Counter battery, run from the deliverable paths:

```
$ python3 C2CounterR82.py --selftest --work W/st
SELFTEST cases=10 red=9 failures=0
$ python3 C2CounterR82.py --mutants --lane <lane> --work W/mt
MUTANTS real=6 killed=6 survived=0          # docstring says "Six attributed data mutations"; len(MUTANTS)=6 — no V4-style drift in this file
$ python3 C2CounterR82.py --control-presence --lane <lane> --work W/ct
CONTROL presence ids=7 closed=7 defects=21 codes=CHECK-TRIVIAL,CLOSE-NOT-REPAIR,SOURCE-LINE
CONTROL presence target_reached=False
```

Checks battery, run from the deliverable path against the lane:

```
$ python3 C2ChecksR82.py --selftest --lane <lane> --work W/cs
U4-LANE-STATE repaired=yes detail=-        # lane's r81 counter now prints real=6 vs docstring "Six" (c804dd41)
SELFTEST cases=10 red=9 failures=0
```

Canonical BEFORE, counter at BASE over the clone (rc verified, not the pipe's):

```
$ python3 plans/round82_c2_closure_debt.py --lane . --rev a3a03ac31451e58f1742b9bccb73b72c2d90a95c
UNIVERSE spotcheck=corpus/lessons/round-81-verifier-spotcheck.md ids=7 R81-V1,…,R81-V7
DEBT-TOTAL ids=7 registered=0 closed=0 checks_passed=0
INDEX corpus/lessons/round-81-verifier-spotcheck.md indexed=no
DEFECT DEBT-UNREGISTERED R81-V1 … R81-V7 (7 lines)
DEFECT INDEX-MISSING corpus/lessons/round-81-verifier-spotcheck.md
DEFECTS n=8 / TARGET ids=7 closed=0 checks_passed=0 indexed=no / PREDICATE R82-C2 fail ; BASE_EXIT=1
```

Full green simulation (shared clone at `c804dd41` + my two files placed at `plans/`, the L1's seven
routed rows shape + a settled-wave `w1-results.json` fabricated, sim commit `0e86cad9`):

```
$ python3 plans/round82_c2_closure_debt.py --lane . --work W/sim
DEBT-TOTAL ids=7 registered=7 closed=7 checks_passed=7
INDEX … indexed=yes
DEFECTS n=0                                # sensitivity leg ran: all 7 evidence reverts produced FAILing checks
TARGET ids=7 closed=7 checks_passed=7 indexed=yes
PREDICATE R82-C2 pass ; GREEN_EXIT=0
```

Live state at the lane tip (`c804dd41` + in-flight worktree, measured read-only): the L1's routed
rows R81-V1…V7 are on disk with `check: python3 plans/round82_c2_checks.py u<k>`; my counter runs
them and reports `registered=7 closed=7 checks_passed=6`, the single defect
`CHECK-FAIL R81-V6 … .ufo/waves/round-82/w1-results.json absent (wave not settled)`, `DEFECTS n=1`,
`PREDICATE fail`, rc 1 — u6 goes green only when the wave settles and the results file is committed,
which is the claim's design. Per-check probe at the tip: `OK u1 u2 u3 u4 u5 u7`, `FAIL u6` (unsettled).

Cross-validation: the L1 pre-integrated its own pair at `plans/round82_c2_{closure_debt,checks}.py`
(untracked, 385+216 lines). Its counter prints the same `UNIVERSE`, the same
`registered=7 closed=7 checks_passed=6`, the same single V6 defect, `PREDICATE fail`, rc 1. Both
pairs agree at BASE shape and at the tip; integration choice is the L1's.

## What I attacked, and what I could not break

- **Universe hardcoding** — mutants `rename-spotcheck-round` (round-83 file) and selftest case
  `stale-spotcheck` (round-79 file, round-80 still present) both flip the universe and die with
  `DEBT-UNREGISTERED`; killed. (Development caught and fixed a real double-`V` bug — `R81-VV1` — before
  these batteries existed.)
- **Sensitivity laundering** — all seven evidence reverts in the green sim fail their checks,
  including `reverted_state: dir` for the stray directory; `CHECK-NOT-REPAIR-SENSITIVE` never silent.
- **Trivial/unfailable checks** — `--control-presence` (rows closed on the spot-check itself, check
  `true`) reaches `target_reached=False` on `CLOSE-NOT-REPAIR` + `CHECK-TRIVIAL`; killed.
- **Close-evidence forgery** — mutants `close-names-spotcheck`, `evidence-literal-absent`,
  `close-no-evidence`, `drop-one-row`, `status-reopened`, `duplicate-row`, `source-line`,
  `index-missing` all killed; the close must name a tracked artifact whose bytes carry the id and the
  row's `evidence_literal`.
- **V2 in-place anchor edit** — checks case `u2-inplace-edit` (frozen S260/S261 cells corrected in
  place instead of supersede rows) fails: `corpus/QUALITY.md` Q34 + the fleet SOURCES contract make
  every S-row cell except status/recheck/used-by immutable, so u2 asserts the frozen cells keep their
  base bytes AND the newest `supersedes S260`/`supersedes S261` row recomputes from the receipt
  (quote verbatim at line 1 = 7 words; `MINTED_BY_SHA` line 14 → `stamp 2-14`; `OBSERVATIONS_BEGIN`
  15 → `:1-15`; first observation 16) plus every `(N words)` claim in the round-81 lesson (12/13/19).
- **Wave-shape slack** — checks case `u6-low-share` (attack 3/14 = 21.4%) fails; the V6 leg computes
  share over exactly the campaign list reviewer/critic/mutation-tester/labrat and requires a
  mutation-tester seat with non-empty output.
- Could not break: the green sim stands against all six mutants + the control, and two independently
  written counter pairs produce identical verdicts at BASE, at the tip, and on the sim tree.

## Risks / residuals (stated, not papered over)

- **V2 literal-residual**: with S260/S261 bytes frozen (correct under Q34), the claim sentence "what
  S260/S261 state equals a mechanically recomputed value" is true only under the newest-statement
  reading — an integrator ruling. u2 prints the residual visibly every run, e.g.
  `V2 reading=supersede s260-frozen=9 words / 2-16 / 17 s261-frozen=14,17`.
- **u6 settle dependency**: the predicate cannot pass before `.ufo/waves/round-82/w1-results.json`
  exists and carries ≥25% attack share + a live mutation-tester; per the seat roster this wave seats
  4 attack of 12 (33%), but the settled file is the authority.
- **Mid-flight churn observed**: S260's cells were briefly edited in place during the wave and later
  restored to frozen bytes with S265/S266 supersede rows (commit `c804dd41`); u2 fails either
  regression. `plans/anchor_line_check.py` is blind to S-row deletion (ConnectorR82 finding), so u2's
  presence + supersede assertion is the only mechanism that fails on S265/S266 removal.
- One battery run observed a transient `docstring=7 real=6` while the L1 was mid-write on the r81
  counter; the committed state is `Six`/`real=6` (verified: `U4-LANE-STATE repaired=yes`, and
  `git show c804dd41:plans/round81_c2_spotcheck_debt.py` carries six `MUTANTS` entries).

## Tooling record

No tools installed or upgraded (no pacman transaction — host-wide pause respected; nothing via
uv/npx either). Python 3 stdlib only, per the item's constraint.
