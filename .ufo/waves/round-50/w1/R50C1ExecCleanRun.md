# R50C1ExecCleanRun — C1 before-receipt on the BASE fence

**Seat**: R50C1ExecCleanRun (executor, leaf). **Serves**: R50-C1 (novelty). **No claim is scored or admitted here.**
**Item**: run the frozen predicate once on a clean `git clone --shared` of the lane at the stage-1 freeze with the
BASE fence and save the complete output to `w1/C1ExecCleanRun/receipt-base-fence.txt`.

## Axes named

- **Novelty (C1)** — the only axis this seat touches, and only as the *before* control: it measures what the
  unrepaired fence does to the frozen 126-fixture honest population. It does not move the axis.
- **Calibration (C2)** — untouched. Coverage — untouched (operator-capped; not claimed this round).
- The seat adds no artifact to `plans/`, `corpus/`, `SCORECARD.md`; it produces a measurement only.

## Revision measured (REV line)

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1ExecCleanRun/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
```

- Ancestry verified **before** any measurement: `git -C <lane> merge-base --is-ancestor 3b02d57… 5c56819…` → exit 0.
- Lane tip moved during this seat (other seats/L1 integrating), so the check was repeated at the new tip:
  `5c56819` → `822f3b7` (C2 corrections) → `c3372a9` (C1 counter open-window repair); `merge-base --is-ancestor
  3b02d57… c3372a9` → exit 0. The stage-1 freeze is an ancestor of every tip observed.
- Measured tree = **clean clone at 3b02d57**, not the live checkout (the live checkout carried 5 dirty lines owned by
  other seats at measurement time).

## Exact commands run

```sh
S=/fast/scratch/hyaku/kengaku-r50/R50C1ExecCleanRun
mkdir -p "$S"; export TMPDIR=$S
git clone --quiet --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout --quiet --detach 3b02d573d58cc6d2e0d27ef92ac0815354912252
# guards: toplevel == $S/lane, HEAD == 3b02d573…, status --porcelain == 0 lines,
#         fence/counter/population sha256 == the three frozen pins
mkdir -p "$S/work"
cd "$S/lane"
if env TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --work "$S/work" --skip-mutants \
     > "$S/run4.out" 2> "$S/run4.err"; then rc=0; else rc=$?; fi   # rc=1
```

Observed clone provenance: `TOPLEVEL=/fast/scratch/hyaku/kengaku-r50/R50C1ExecCleanRun/lane`,
`HEAD=3b02d573d58cc6d2e0d27ef92ac0815354912252`, `DIRTY_LINES=0`,
alternates → `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.git/objects`.
Host: python 3.14.8, git 2.56.0, linux 7.2.11-arch1-1.

`--skip-mutants` is used because the frozen MUTANTS leg is the S2-side re-derivation (QUALITY Q38) and cannot inform
a do-nothing control's honest-geometry number; the three legs the item names are unaffected by the flag. `--allow-dirty`
was **not** passed.

## Observed output (verbatim, complete)

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1ExecCleanRun/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n14-stash-entry ../../../../work/k50-c1-b9dtndys/honest/m026-plans-honest50-modules-novel48-n14_stash_entry/f000/repo/.git/logs/refs/stash has a name git does not write
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph present (object-store redirect)
HONEST-REFUSED n16-notes-ref ../../../../work/k50-c1-b9dtndys/honest/m028-plans-honest50-modules-novel48-n16_notes_ref/f000/repo/.git/logs/refs/notes has a name git does not write
HONEST-REFUSED n17-replace-ref repo/.git/refs/replace is not refs/heads or refs/tags
HONEST-REFUSED n18-shallow-fetch repo/.git/FETCH_HEAD is not a plain-init entry
HONEST-REFUSED n20-linked-worktree wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n21-separate-gitdir wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n22-alternates-in-d lane/.git/objects/info/alternates present (object-store redirect)
HONEST-REFUSED n03-detached-head repo/.git/HEAD is not a plain branch HEAD
HONEST-REFUSED n07-reflog-gc repo/.git/info/refs is not git's exclude file
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

Exit status measured at run time: **EXIT=1**. stderr: 0 bytes.

### Required match, item by item

| required | observed | |
|---|---|---|
| `HONEST fixtures=126 admitted=113 refused=13` | identical | ✅ |
| `REFUSALS total=20 clean=20` | identical (`leaked=0 build_errors=0`) | ✅ |
| `SEALED total=12 clean=12` | identical (`leaked=0 build_errors=0`) | ✅ |
| exit 1 | 1 | ✅ |

Also reproduced: `POPULATION … mismatched=0 build_errors=0` with pin `b5197f94…`, `TREE dirty=0`,
`FENCE … sha256=05d5fe03…`. `PREDICATE R50-C1 fail` is the **expected** result for the do-nothing control
(`plans/round-50-claims.md` control row 1: "`PREDICATE fail` on `HONEST admitted=113`").

## Reproducibility

Two independent invocations, byte-identical modulo the `mkdtemp` suffix (`s/k50-c1-[a-z0-9_]+/k50-c1-WORKDIR/`;
`cmp -s` → identical). sha256 of the normalized stdout:
`14380cfa4154036930a2666e334211be79b2cece97b11c7184729f157db112f2`.

## Evidence retained (wave dir, citable)

All under `.ufo/waves/round-50/w1/C1ExecCleanRun/`:

```
receipt-base-fence.txt              b9a1f6c809c1e6c7313b95164bfff6c2b91a828811e3592a5c521a0a3447bdb8
run4.stdout.raw                     bdee6cdfe013c9c6910997628186102b0138fa2cb5b3654cebb63e1df26dcfbe
run4.stderr.raw                     e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  (empty)
run4.exit.raw                       4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865  ("1\n")
run2.stdout.raw                     5f1f653a3fd31fe87818158b0c88ca4eec1cff45146bde68a4bec56540c1aa32  (independent repeat)
stdout.workdir-normalized.txt       14380cfa4154036930a2666e334211be79b2cece97b11c7184729f157db112f2
```

The receipt block inside `receipt-base-fence.txt` was diffed against `run4.stdout.raw` with the work-dir suffix
normalized: identical except the file's trailing blank line.

## Findings for the L1 (not acted on — outside this seat's item)

1. **Lane advanced while this seat ran.** HEAD went `5c56819` → `822f3b7` → `c3372a9`. At `c3372a9` the counter's
   digest changed `f9b9873e…` → `d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2` (open-window
   repair: hostile module attribution keyed by `str(path)` instead of `path.name`, 2 insertions/2 deletions; the
   predicate sentence and the literals `126/20/12/SEALED50_MIN` are untouched in that diff — `plans/fixture_fence.py`
   is still `05d5fe03…`).
   This receipt is bound to the **stage-1** tree and the **stage-1 counter `f9b9873e…`**, which is the correct
   "Before" tree per the claim doc; the open-window rule requires the L1 to record the old→new counter digest in
   `round-50-claims.md` and, if the repaired counter is the one scored at S3, to re-take the do-nothing before
   control on the repaired counter. That re-run is not this seat's item, so it was not performed.
2. **`--work` parent must exist.** `tempfile.mkdtemp(dir=a.work)` creates only the child; the first attempt with a
   non-existent `--work` died `FileNotFoundError` before any measurement (no stdout, no fixture built). Harmless for
   S3 (the documented S3 command does not pass `--work`) but worth knowing: a driver that passes `--work` must
   `mkdir -p` it. Not filed as a counter defect.
3. The base fence refuses **13** honest fixtures: the 5 documented in-`d` classes (`n17`, `n18`, `n20`, `n21`, `n22`)
   plus `n03-detached-head`, `n07-reflog-gc`, `n12-local-config-user`, `n13-remote-origin`, `n14-stash-entry`,
   `n15-commit-graph`, `n16-notes-ref` — the eight the claim doc does not enumerate. The repair scope at S2 is
   therefore wider than "five classes" if the target `admitted=126` is to be met; the claim doc's own population
   composition already counts these fixtures, so the arithmetic is consistent, but the S2 fence work must clear all 13.

## Limits

- Admission decisions only, on this host (git 2.56.0, python 3.14.8); the fixture identity pins make host sensitivity
  visible rather than silent. Outside-`d` reads were not measured (they belong to `round46_c1_verify.py`), the MUTANTS
  leg was not run, io_uring/host paths outside the scratch root were not observed.
- The work-dir path inside two `HONEST-REFUSED` lines is a scratch path printed by the counter; it is not citable
  evidence and the normalized copy is the citable form.
- This seat wrote only its report and receipt dir under `.ufo/waves/round-50/w1/`; production files, `SCORECARD.md`,
  `LOG.md`, `corpus/`, `.ufo/state`, `MANIFEST.json` and sibling repos were untouched. Lane `git status` after the
  seat shows no entry created by it (`corpus/QUALITY.md` modified and `w1.ready`/`w1.ready.partial` are other seats').
- Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1ExecCleanRun` (clone, work tree, raw runs) was **removed before
  yield**; removal observed: `SCRATCH_REMOVED`.
- No tool was installed or upgraded during this seat (nothing needed).

## VERDICT

**PASS — before-receipt reproduced exactly on a clean clone of the stage-1 freeze with the base fence.**
`HONEST fixtures=126 admitted=113 refused=13`, `REFUSALS total=20 clean=20`, `SEALED total=12 clean=12`,
`PREDICATE R50-C1 fail`, exit 1, `TREE dirty=0`, fence `05d5fe03…`. R50-C1 is **not** admitted by this receipt and
no production file was touched.
