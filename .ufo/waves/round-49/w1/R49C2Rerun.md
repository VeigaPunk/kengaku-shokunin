# R49C2Rerun — independent v4 counter rerun

**Axis:** coverage (R49-C2). This is a scoped counter review, not a claim-admission judgment.

## Freeze and candidate

Before measurement, verified the committed stage-1 freeze: `git cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93` returned `commit`; its commit time is `2026-10-28 09:14:40 -0300`, and `plans/round-49-claims.md` is present in that tree. Both measurement clones had `HEAD=9d2900af41e4d1fc6022eff99010436fde6dbd93`; the freeze predates these runs. No external source was opened (no URL/quote applicable).

Reran the delivered candidate `.ufo/waves/round-49/w1/R49C2ExecCounter/candidate.py` (SHA-256 `9e9b47b027d82027f89ab149872b4807fda988c4b12dba88700294380d2b9c7b`), not my earlier local reconstruction. The probe candidate is SHA-256 `29c2387f26b1594e61a953f0ecca256ececbb917b4b65dc697be24690aacf340`; the amended dry table is `905e04a1aa0434275b27d6cb1a910ce5a17d0c7fbc102b54b1fadb168189d944`.

## Exact commands and observed results

1. Base clone (stage-1 commit), after copying the candidate to the untracked `plans/round49_c2_verify.py`:

```sh
python3 "$D/plans/round49_c2_verify.py" --lane "$D" --dry --work "$S/canonical-base-work"
```

Observed output, verbatim:

```text
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93 lane=/fast/scratch/hyaku/kengaku-r49/R49C2Rerun/lane
PACKAGE unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V15 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V1 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V3 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V4 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V5 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V6 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V7 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V8 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V9 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V10 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V11 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
V12 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
    filler: V3 ok rows=7 bad=0
    filler: V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
    filler: V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
    filler: V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
    filler: V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
    filler: V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
    filler: V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
V14 DEFECT package unreadable: spec pin pending: SPEC_SHA256 is a stage-2 placeholder
checks=14 defects=13
PREDICATE R49-C2 fail
```

Exit: 1. This is the frozen base/do-nothing control; the candidate correctly refuses an unpinned stage-2 spec. It is not an admission measurement.

2. Pre-receipt staged candidate clone, assembled at the same frozen `HEAD` from the current wave artifacts (candidate, draft r49 spec with the stage-2 probe/dry pins filled in a scratch copy, v2 probe, 20-case dry table, 23-mutant plan and payloads). For this diagnostic only, I filled the candidate's `SPEC_SHA256`, `PROBE_SHA256`, `DRY_SHA256`, `MUT_N=23`, and `MUT_FLOOR=12` in the scratch copy; the counter and package artifacts remain uncommitted, and the stage-3 receipt/control-receipt pins remain unavailable. Staged clone `git status --porcelain` had 5 entries. Command:

```sh
python3 "$D/plans/round49_c2_verify.py" --lane "$D" --dry --work "$S/staged-work"
```

Observed output, verbatim:

```text
REV 9d2900af41e4d1fc6022eff99010436fde6dbd93 lane=/fast/scratch/hyaku/kengaku-r49/R49C2Rerun/staged
V15 DEFECT inputs=11 tables=7 blocked=4
V1 ok listed=8 wrong=0 extra=0
V3 ok rows=7 bad=0
V4 DEFECT precondition: the receipt is unreadable
V5 DEFECT probe=frozen dry_byte_equal=False
V6 ok census_exit=0 registry=corpus/SOURCES.md
V7 DEFECT precondition: the receipt is unreadable
V8 DEFECT controls=3 gates=base:exit=1,p10=0 filler:exit=1,p10=0 echo:exit=1,p10=0 stage2=none stage3=none cases=0 observed=0 bad=6 no commit adds the stage-2 counter plans/round49_c2_verify.py (the ordering anchor is absent) | no commit adds the receipt corpus/evidence/round49/polyglot-c-py-probe.txt (the stage-3 landing is absent) | the receipt carries no CASE lines (no measured run)
V9 DEFECT precondition: the receipt is unreadable
V10 DEFECT precondition: the receipt is unreadable
V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0
V12 ok rows=7 defective=0 live=0
    filler: V3 ok rows=7 bad=0
    filler: V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
    filler: V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
    filler: V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
    filler: V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
    filler: V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
    filler: V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
MUTATION DEFECT
V14 DEFECT mutants=23 caught=11 floor=12 baseline_defects=V10,V4,V7,V9 cap-test-outputs-values:caught(V12) cap-test-outputs-listing:caught(V12) cap-instruction-stdout:caught(V12) cap-test-sh-reward:caught(V12) cap-solve-sh-comment:caught(V12) cap-dockerfile-base:caught(V12) cap-task-toml-internet:caught(V12) cap-readme-cases:caught(V12) entry-casetable-verdict-flip:CLEAN entry-mechanism-line-shift:CLEAN entry-source-id-removed:CLEAN entry-reqmap-label-invert:CLEAN receipt-verdict-swap-compile-warning:CLEAN receipt-prediction-drift:CLEAN receipt-summary-splice:CLEAN receipt-inventory-rename:CLEAN dry-inventory-rename:CLEAN dry-inventory-duplicate:CLEAN spec-s168-digest-drift:caught(V3,V12) package-unreadable spec-s172-capture-name:caught(V3,V12) package-unreadable spec-row-set-contraction:caught(V3,V12) package-unreadable probe-tags-line-shift:CLEAN probe-case-expect-flip:CLEAN
checks=14 defects=8
PREDICATE R49-C2 fail
```

Exit: 1. This is a pre-receipt diagnostic, not the frozen landing-tip score: V8 correctly reports no committed stage-2 counter/stage-3 receipt; V15/V4/V7/V9/V10 are blocked by the absent stage-3 receipt. The new probe's `--dry` output does not byte-match its 20-case pinned table (`V5 … False`); the probe candidate still has the 18-case table per `R49C2ExecProbe.md` §5. This is an actionable stage-2 blocker: the probe revision and amended dry table must be brought into byte agreement before stage-check can pass. V14 currently catches 11/23 (<12) while baseline substantive legs V4/V7/V9/V10 are already defective in this pre-receipt tree; therefore this observation does not establish the final stage-2 mutation-floor result, but the present tree does fail the frozen floor.

## Additional receipt-contract defect

The candidate emits only `REV <commit>` in both uncommitted-tree runs; it does not emit the required `TREE-BYTES` for content measured from an uncommitted clone (claims §Receipt discipline/Q22). The staged run was dirty (5 status entries), yet its output has no dirty-tree byte count. This prevents the output alone from identifying the measured staged content. The base result likewise has an untracked candidate file and no `TREE-BYTES`.

No full probe run was performed: both counter invocations used `--dry`; the candidate's V2/full probe leg was excluded. V5's permitted probe `--dry` check ran on the staged candidate and returned `dry_byte_equal=False`. The staged candidate tree did not yet contain a stage-3 receipt or committed stage-2 counter, so no landing-tip admission conclusion is possible. No lsp device/server was available in this runtime; semantic checks here rely on the counter's own emitted results, not grep output.

**VERDICT:** R49-C2 candidate fails on the frozen base as expected and fails the current pre-receipt staged-tree dry run (`checks=14 defects=8`, exit 1). Actionable blocker: staged probe and 20-case dry table are inconsistent (`V5`); candidate also omits Q22 `TREE-BYTES` for dirty-tree receipts. Not an admission verdict.
