# R49C2CritDoNothing — C2 do-nothing control review

Axis: **coverage**.

## Evidence

- Frozen claims read in full: `plans/round-49-claims.md`; routed issue read: `corpus/lessons/round-48-verifier-spotcheck.md`; lesson read: `corpus/lessons/round-48.md`.
- Stage-1 freeze exists in the committed lane tree and predates measurement: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse --verify '9d2900af41e4d1fc6022eff99010436fde6dbd93^{commit}'` → `9d2900af41e4d1fc6022eff99010436fde6dbd93`; `git log -1` → `2026-10-28 09:14:40 -0300`, subject `round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering claims)`. Measurement diagnostic was later, on scratch revision below.
- Frozen base: `9d2900af41e4d1fc6022eff99010436fde6dbd93`. The stage-1 tree already contains `plans/polyglot_c_py_probe.py` (SHA-256 `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`), the round-46 spec, receipt, and dry table. Probe first committed at `cf7de6a` (round-46 stage-2 instruments).
- The v4 counter `plans/round49_c2_verify.py` and its stage-2 pins are absent from the stage-1 tree, so the frozen C2 predicate cannot be scored here. I did not run the v4 counter or a full probe.

## Non-scored inherited-counter diagnostic

Exact commands:

```sh
export TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing
cd /fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing
git clone --shared --quiet lane diag
test "$(git -C diag rev-parse --show-toplevel)" = /fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag
git -C diag rm --quiet plans/pkg-spec-r46.json
git -C diag commit --quiet -m 'scratch diagnostic: remove package spec'
git -C diag rev-parse HEAD
python3 diag/plans/round46_c3_verify.py --lane diag --work /fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag-work
```

Scratch control revision measured: `58a1456930960df8bb9c6ab4aa7b343fd5f32268` (derived from frozen base; only the round-46 spec removed). The diagnostic inherited counter output, verbatim:

```text
PACKAGE unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V1 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V2 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V3 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V4 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V5 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V6 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V7 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V8 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V9 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V10 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V11 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
V12 DEFECT package unreadable: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r49/R49C2CritDoNothing/diag/plans/pkg-spec-r46.json'
    filler: V3 ok rows=7 bad=0
    filler: V4 DEFECT cases=16 mismatches_named=0/0 bad=["match=yes on a mismatching case: ['float-c']"]
    filler: V6 DEFECT census_exit=1 registry=plans/filler46/SOURCES-filler.md
    filler: V7 DEFECT rows=4 tags=4 bad=['single-file: no receipt case violates it', 'python-run: no receipt case violates it', 'c-run: no receipt case violates it', 'fib: no receipt case violates it']
    filler: V9 DEFECT case_rows=1/16 bad=['case table rows=1 receipt cases=16 equal=False', 'PROVINCE.md names the task and the entry on no line']
    filler: V10 DEFECT DECISIVE keys differ from the frozen case ids (stage-2 pin not aligned)
    filler: V12 DEFECT rows=7 defective=7 live=7 first=S166:line,words
V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12
checks=13 defects=12
PREDICATE C3 fail
COUNTER_EXIT=1
```

The diagnostic output was fully captured in the command result. No external source was opened; URL/access-date/quote: not applicable.

## Finding / limit

The inherited counter rejects a package-unreadable do-nothing control cleanly (12 defects; exit 1), but this is **not** a scored R49-C2 result and does not establish the R49 control receipt. The literal stage-1 base is not the described “base tree (no `plans/polyglot_c_py_probe.py`)”: that path is present in it. Thus the control construction is ambiguous: literal base with the old probe versus a derived base with the probe removed. The R49 v4 counter/control receipt is also not yet in the frozen tree; do not infer its behavior from C3.

Smallest safe correction: stage-2 control receipt must state the exact measured tree/revision and construction. If literal base is intended, remove “no probe” from the description; if probe absence is intended, name and pin the derived control tree explicitly. Then require its v4 output to show `PREDICATE R49-C2 fail`, exit 1. This only clarifies/records the control and does not change the frozen predicate.

VERDICT: **C2 do-nothing control not scored under the frozen v4 predicate; no evidence it reaches pass.** Diagnostic inherited C3 control failed as expected. Control-text/tree mismatch requires explicit stage-2 construction; no R49-C2 admission claim.