# R49C1PredCounter — environment-keyed counterexample

Axes named: **calibration (R49-C1)**. Scope: counter distinguishability; no R49-C1/R49-C2 admission claim.

## Counterexample

The strongest tested bypass is an environment-keyed fence. The scratch candidate embeds the frozen base fence and calls its real `breach()` only when `PYTHONDONTWRITEBYTECODE=1`; for every other environment it returns `None` (admit-all). This is a direct, falsifiable example of a fence that meets the verifier's population behavior but does not enforce its advertised property outside that verifier environment.

Observed verifier evidence: the checked-in round-46 C1 harness explicitly sets `PYTHONDONTWRITEBYTECODE=1` for every fence subprocess (`round46_c1_verify.py:367-374`). In contrast, the frozen R49 claim requires randomized per-run tokens, padded parents and shuffled jobs, but specifies no environment variation (`plans/round-49-claims.md:58-61`). The counter measures hostile and honest fixtures inside that single fixed environment. The candidate's conditional therefore distinguishes the harness from other execution environments without looking at the fixture or its boundary.

## Commands and observed outputs

All git commands used `git -C` with `D=/fast/scratch/hyaku/kengaku-r49/R49C1PredCounter/lane`; `git rev-parse --show-toplevel` returned exactly that path before any checkout. No fixture git calls were made.

- `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane` → `done`.
- `git checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93; git rev-parse HEAD` → `9d2900af41e4d1fc6022eff99010436fde6dbd93`.
- `git log --format='%H %cI %s' -1 -- plans/round-49-claims.md` → `9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims`. This stage-1 commit predates all measurements below.
- `command -v bwrap strace git python3` → `/usr/bin/bwrap`, `/usr/bin/strace`, `/usr/bin/git`, `/usr/bin/python3`.
- `python3 collector.py <lane> <scratch>` → `rc=0`; built/fingerprinted hostile modules in scratch, wrote `hostile_sigs.json`. This experiment was not a passing attack: the subsequent fingerprint-denylist control failed with 14/20 refusal leaks and 8/12 sealed leaks, although it admitted all 104 honest fixtures. No claim that this naïve signature key bypassed the counter.
- `python3 lane/plans/round46_c1_verify.py --lane lane --work /fast/scratch/hyaku/kengaku-r49/R49C1PredCounter --fence /fast/scratch/hyaku/kengaku-r49/R49C1PredCounter/env_keyed_fence.py --jobs 8` → exit `0`; tail of exact output:
  ```
  SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0
  HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
  CALIBRATION advertised=32 contradicted=0
  REASON -
  PREDICATE C1 pass
  ```

The round-46 counter was the only runnable counter in the stage-1 tree; `round49_c1_verify.py` and the stage-2 population/literals/receipts are not present at the frozen revision. This is a successful attack on the available base harness, **not** a scored v3 run or claim that R49-C1 passed. Stage-1 ordering was respected: the required committed freeze was verified before running either counter experiment.

## Impact and smallest safe correction

Impact: **calibration** — fixed-environment testing cannot distinguish an always-enforcing fence from a fence that detects the test harness and switches to admit-all elsewhere. Randomized fixture names, shuffled job order, held-out modules and a mutation floor do not vary `PYTHONDONTWRITEBYTECODE` or other process environment signals.

Smallest safe correction: have the frozen counter run the fence under at least one independently varied environment, then require the same refusal/admission classification and zero outside touches across environments. Freeze the varied environment(s) before scoring and include their results in the clean signature. Do not alter the predicate post hoc; if stage-2 counter contract cannot add the check, record this as a remaining calibration limit rather than claiming the counter rules out environment-keyed fences.

## Limits

- No R49 v3 counter, stage-2 population, held-out modules or committed receipts exist at the measured base; therefore their actual behavior is unmeasured.
- The passing test exercises round-46 counter code with the same fixed environment behavior explicitly carried by the v2 harness; it is not an R49 v3 result.
- The environment-keyed candidate was scratch-only and was not run in a second environment; its non-test branch is directly visible in candidate code (`return None`).
- No tools installed or updated; no pacman transaction attempted. No external source opened.
- Scratch cleanup is performed before yield; this report is the only retained artifact from this seat.

Measured revision: `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` (frozen base; counter candidate and all measurements remain scratch-only).

VERDICT: **environment-keyed counterexample demonstrated against the available fixed-environment C1 harness; v3 bypass remains unmeasured. Smallest correction is a frozen environment-variation leg.**
