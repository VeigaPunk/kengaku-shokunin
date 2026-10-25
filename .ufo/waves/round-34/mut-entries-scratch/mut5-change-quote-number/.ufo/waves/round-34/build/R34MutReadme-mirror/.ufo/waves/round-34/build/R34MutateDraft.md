# R34 mutation harness draft

Files changed: `.ufo/waves/round-34/build/R34MutateDraft/round34_mutate.py`; harness output: `.ufo/waves/round-34/build/R34MutateDraft/harness-run.txt`.

The script exports `HEAD` with `git archive` into a temporary tree, initializes an isolated temporary Git repository (the counter invokes `git ls-files`), runs the clean counter gate, and defines the eight requested mutant operations and `--selftest`. No lane index or source checkout is changed.

Exact run evidence (command: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/build/R34MutateDraft/round34_mutate.py`; output saved verbatim at the harness-run path):

```
CLEAN exit=1
DEFECT N3 round31-report-append-only-erratum: /tmp/round34-mutate-5t9hp86t/clean/.ufo/reports/round-31/kengaku.md is unreadable
DEFECT N4 round32-report-closure-hash: /tmp/round34-mutate-5t9hp86t/clean/.ufo/reports/round-32/kengaku.md is unreadable
DEFECT N7 round33-lesson-ledger-correction: round-33 lesson has no dated correction stating ledger sum 36+53=89
checks=8 defects=3
```

The frozen tip export does not contain either required `.ufo/reports/round-{31,32}/kengaku.md`; direct directory read of lane `.ufo/reports/` showed only `round-17/kengaku.md`. N7 is also intentionally red pre-integration per L1's message. Since the harness correctly requires a clean exit 0, it stops at the clean gate and does not claim mutation detections. Counter draft check N1 also requires a Git worktree; the harness now initializes/commits only its temporary archive sandbox, not the lane.

Risks/blockers: counter/harness contract cannot currently be exercised against the frozen archive because two counter input reports are absent from that archive, and N7 correction is intentionally pending integration. Mutations M5/M6/M7/M8 are mapped to the counter's intended checks N5/N6/N3/N4, but available source paths differ: counter N6 reads round-30 lesson while the frozen mutation instruction names round-31; N3/N4 read `.ufo/reports/` while mutation instructions mention fleet-report copies. These mismatches need integration-owner reconciliation before a valid full run. No fabricated clean result or mutant detection is reported.

VERDICT: mutate-harness <MUTANTS total=8 detected=0> exit=1