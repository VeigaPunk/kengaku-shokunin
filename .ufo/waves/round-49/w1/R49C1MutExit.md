# R49C1MutExit — control exit / output-label mutation

Axes named: **calibration** (assigned R49-C1); **coverage** is outside this seat's item. No admission judgment.

## Freeze and scope

Verified before measurement: `9d2900af41e4d1fc6022eff99010436fde6dbd93` exists as a commit, subject `round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims`, timestamp `2026-10-28 09:14:40 -0300`, and is an ancestor of lane HEAD `af88aab`. Scratch clone HEAD/REV measured: `9d2900af41e4d1fc6022eff99010436fde6dbd93`. Stage-2 `round49_c1_verify.py` and mutant plan were not present at lane tip; this bounded probe therefore used the frozen-base `plans/round46_c1_verify.py` contract, not a v3 counter or scored R49 admission run.

Scratch clone top-level check: `git -C "$D" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r49/R49C1MutExit/lane`; equality to `$D` verified before any fixture writes. No web/source URL opened (URL/access-date/quote: not applicable).

## Mutant and detector

Targeted counter tail in scratch copies of `plans/round46_c1_verify.py`:
- `X`: make counter return 0 regardless of predicate.
- `L`: hard-code legacy `PREDICATE C1 pass` label.
- `T`: retag the conditional predicate as `PREDICATE R49-C1`.
- `XL`: hard-code legacy pass label and return 0.
- `XLT` (**assigned counterfeit mutant**): hard-code exact future label `PREDICATE R49-C1 pass` and return 0, bypassing computed `good`.
- `HX`: invert harness exit statuses 10/11.

These are scratch-only counter mutations; each compiled with `python3 -m py_compile`. The control fences were scratch-only: `refuse_all.py` returns a reason for every fixture; `admit_all.py` returns `None`. Detector was the same counter invocation on each control, checking output labels, leg rollups, predicate line and process exit code. The pristine counter correctly fails both controls.

Exact commands (run from scratch `$S=/fast/scratch/hyaku/kengaku-r49/R49C1MutExit`, `TMPDIR=$S`):

```sh
python3 "$S/mut/P.py" --lane "$S/lane" --work "$S/work/P-RA" --jobs 12 --fence "$S/fences/refuse_all.py"
python3 "$S/mut/XLT.py" --lane "$S/lane" --work "$S/work/XLT-RA" --jobs 12 --fence "$S/fences/refuse_all.py"
python3 "$S/mut/XLT.py" --lane "$S/lane" --work "$S/work/XLT-RESTORED" --jobs 12 --fence "$S/fences/refuse_all.py"
```

Admit-all cross-control command used the same form with `--work "$S/work/XLT-AA" --fence "$S/fences/admit_all.py"`. Every run recorded `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` and TREE-BYTES hashes in its captured log. Base-tree `P` run (before using the must-fail controls) had `PINS total=65 mismatched=0`, `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`, `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, `PREDICATE C1 pass`, rc=0. This is the original round-46 fence/population, not the round-49 extended honest population.

## Observed outputs

Pristine on refuse-all: `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`; `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=0 refused=104 read=0 hung=0 build_errors=0`; `REASON honest-not-admitted`; `PREDICATE C1 fail`; `RC=1`.

Pristine on admit-all: `REFUSALS total=20 clean=0 leaked=20 read=0 hung=0 build_errors=0`; `SEALED total=12 clean=0 leaked=12 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `REASON refusals-not-clean,sealed-not-clean,contradicted=32`; `PREDICATE C1 fail`; `RC=1`.

Full counterfeit XLT on refuse-all: `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`; `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=0 refused=104 read=0 hung=0 build_errors=0`; `REASON honest-not-admitted`; **`PREDICATE R49-C1 pass`; `RC=0`**.

Full counterfeit XLT on admit-all: `REFUSALS total=20 clean=0 leaked=20 read=0 hung=0 build_errors=0`; `SEALED total=12 clean=0 leaked=12 read=0 hung=0 build_errors=0`; `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`; `REASON refusals-not-clean,sealed-not-clean,contradicted=32`; **`PREDICATE R49-C1 pass`; `RC=0`**.

Other mutant observations (refuse-all / admit-all respectively): X (exit always 0) emitted fail / rc=0 on both controls; L (hard-coded legacy label) emitted pass / rc=1 on both; T (retag only) emitted `PREDICATE R49-C1 fail` / rc=1 on both; XL (legacy pass label + exit 0) emitted pass / rc=0 on both, but not the exact R49-C1 label; HX caused refuse-all to fail on hostile legs and admit-all to fail on honest leg. Thus **the exact required R49-C1 pass label plus zero exit is counterfeit-accepted by a predicate-only detector**; checking the claimed leg lines or rerunning controls rejects the result. The counter itself is the source of its printed label/status, so output/status alone are insufficient authentication.

## Hashes / restoration

Measured base counter (`plans/round46_c1_verify.py`) and pristine `P.py`: `ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508`. Base fence: `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`. Mutated XLT: `8ae9ec05f0a2d9adf7f83bd119d0747853a721fa5b9b97cbec1b26bd5f1969b5`. Other mutant hashes were captured in scratch `logs/mutants-digests.txt`.

Restored `XLT.py` by copying pristine `P.py`; before/restored/after hashes all observed as `ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508` (`RESTORATION-EXACT`). The restored same detector run again printed `REASON honest-not-admitted`, `PREDICATE C1 fail`, `RC=1`.

Limits: no stage-2 v3 counter/population/mutant plan existed in the frozen lane tip; this establishes the counterfeit behavior for the frozen r46 counter path and exact anticipated R49 label, not end-to-end behavior of the not-yet-landed v3 counter. The recorded r46 honest total is 104, whereas frozen R49-C1 extends it.

VERDICT: **KILLED by substantive control checks, SURVIVES a predicate-label-plus-exit-only detector.** The exact counterfeit produces the specified success signature on both must-fail controls. No R49 claim admission asserted. Scratch clone and all temporary files removed before yielding.
