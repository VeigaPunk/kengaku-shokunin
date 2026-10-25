# F35DanglingRefs — dangling path citations after the D2 deletion

Seat: scout (leaf — no subagents, no background jobs, no `task`).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Tip examined: `dfee6fff631ebc5f623ba4506e5c7992a215401c`
(`refs/heads/master` == tip, verified). D2 deletion commit: `dfcd294c60a00215c55bc4ce0b620440cd5e402f`
("round-35: C2 close round-34 routed defects D1-D5 (drafts committed, mirror roots deleted, manifest, D4/D5 corrections, ledger closed, Q23)").
Freeze: `11d64530`. No tool installed or updated (none needed). All lane reads were `git -C <lane> …`
read-only; the only writes were into this seat's own directory and one `/tmp` fixture.

## Axes named

1. **Completeness of the dangling set** — every committed file at tip that cites a path the D2
   commit removed, found by exhaustive tree scan (not by eyeball grep).
2. **Resolvability through history** — for each cited deleted path: is it recoverable, and from
   which named commit?
3. **Load-bearing-ness** — does any admitted claim (C1 or C2) depend on a cited path that no longer
   exists at tip? (This is the falsification question: a stale-but-harmless citation and a
   broken-admission citation are different findings.)

## Fixture (per the fixture rule)

```
D=$(mktemp -d /tmp/k35f-dangle-XXXX)
git clone -q --no-checkout --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"
git -C "$D/lane" sparse-checkout set --no-cone '/.ufo/waves/round-34/' '/.ufo/waves/round-35/' \
  '/corpus/' '/plans/' '/SCORECARD.md' '/LOG.md' '/PROVINCE.md' '/scripts/'
git -C "$D/lane" checkout -q dfee6fff631ebc5f623ba4506e5c7992a215401c
```

```
toplevel=/tmp/k35f-dangle-d7fy/lane  D=/tmp/k35f-dangle-d7fy
dfee6fff631ebc5f623ba4506e5c7992a215401c
```

`git -C "$D/lane" rev-parse --show-toplevel` == `$D/lane` — verified before any write.
**Fixture note:** my first fixture (`/tmp/k35f-B6rR`) was destroyed mid-run by a sibling's
`/tmp/k35f-*` glob cleanup (reported to `F35MutReceipt`; I re-created under a unique
`k35f-dangle-` prefix and rm -rf only that exact path). Separately `/tmp` reached 100% (128G,
`du -sh /tmp` = 123G) from sibling fixtures, so one probe write failed with
`No space left on device`; that probe was re-run in a space-safe form and its result is reported
below. The fixture was removed at the end (`rm -rf /tmp/k35f-dangle-d7fy`).

## Baseline: the two frozen predicates still pass at the tip

Run in the fixture clone at the tip:

```
$ python3 plans/round35_c1_verify.py --lane .
V1 ok
V2 ok
V3 ok
V4 ok
V5 ok
V6 ok
checks=6 defects=0
PREDICATE C1 pass
exit=0

$ python3 plans/defect_ledger.py --lane .
R34-D1 status=closed observed=pass agree=yes untracked=0
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
R34-D3 status=closed observed=pass agree=yes listed=6 evaluator_listed=True bad=0
R34-D4 status=closed observed=pass agree=yes correction_lines=1
R34-D5 status=closed observed=pass agree=yes erratum_lines=1 r35_mistake_row=True
rows=5 closed=5 observed_pass=5 mismatches=0
PREDICATE C2 pass
exit=0
```

The D2 deletion did not break either admitted counter. The rest of this report asks the sharper
question: what is left behind that still points at the deleted bytes.

## What was deleted

```
$ git show --name-status --diff-filter=D dfcd294 | grep -c '^D'
109410
$ git show --name-status --diff-filter=R dfcd294 | grep -c '^R'
3
```

109,410 deletions + 3 renames-out-of-the-roots = **109,413** committed paths removed, matching the
count the ledger and lesson quote.

```
$ git ls-tree -r --name-only 11d64530 -- .ufo/waves/round-34/mut-entries-scratch \
    .ufo/waves/round-34/build/R34MutRegistry/mirror .ufo/waves/round-34/build/R34MutRegistry/mut | wc -l
109413
$ git ls-tree -r --name-only dfee6fff631ebc5f623ba4506e5c7992a215401c -- (same three roots) | wc -l
0
```

The three deleted roots are exactly the three roots `plans/defect_ledger.py:50` now guards, and
all three are empty at the tip.

**Scope note (a real limit of the deletion, not of my scan).** The three roots were the *only*
paths removed. Same-class recursive mirrors survive elsewhere in the tree:

```
$ git ls-tree -r --name-only dfee6fff631ebc5f623ba4506e5c7992a215401c \
    | grep -E '\.ufo/waves/[^/]+/[^/]+/\.ufo/waves/|/corpus/SOURCES\.md$' | awk -F/ '{print $3}' | sort | uniq -c
     35 round-28
      7 round-34
      1 round-35
```

43 residual same-class paths at tip (35 under `round-28`, 7 under `round-34`, 1 under
`round-35` — `.ufo/waves/round-35/build/R35RowsDraft/validate/corpus/SOURCES.md`). Under round-34
they sit in `.ufo/waves/round-34/build/R34ReviewCounterC1Attacks/{base,a3..a8}/` (28 paths) —
i.e. **inside the D2 root's parent tree but outside the three guarded roots**, so `r34_d2`
(`committed_mirror_paths=0`) cannot see them. These were present at the freeze too (42 paths at
`11d64530`), so round 35 did not introduce them; it did not remove them either. **This is a
coverage gap in the D2 guard's root list, not a dangling citation.** It is reported here because
the seat's premise ("which committed files cite paths that no longer exist") is a proxy for
"what did the deletion miss", and this is the sharper thing the deletion missed. Flagging for the
calibration axis; I did not test whether a same-class path under a *new* root would flip `r34_d2`
(see "What I did not run").

## Finding 1 — the dangling citation set (complete, by exhaustive scan)

Method: enumerate every tracked file at tip (`git ls-tree -r --name-only dfee6fff…`, 9,193 paths),
read each one's bytes, and match path tokens against `lost = (tree at 11d64530) − (tree at tip)`
= 109,413 paths. Three citation shapes are counted:

| shape | citing files | citation lines |
|---|---|---|
| **A** — cites an exact deleted file path | 15 | 15 |
| **B** — cites a deleted root directory name (the path itself, not a file) | 24 | 36 |
| **C** — cites a deleted subtree by relative name inside its own seat dir (`mirror/`, `mut/`) | 1 | 2 |
| **union of files** | **25** | — |

### A. Exact deleted-file citations — 15 files, 15 lines, 6 distinct deleted paths

Every one of the 15 lines is inside `.ufo/waves/round-34/build/R34MutRegistry/out/`, and every one
names one of six deleted paths:

```
.ufo/waves/round-34/build/R34MutRegistry/out/baseline.validate.txt:16        -> .ufo/waves/round-34/build/R34MutRegistry/mirror/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/mut-m1-column-count.diff.txt:3   -> .../mirror/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/mut-m1-column-count.sha256:1     -> .../mut/m1-column-count/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/mut-m2-escaped-pipe.diff.txt:3   -> .../mirror/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/mut-m2-escaped-pipe.sha256:1     -> .../mut/m2-escaped-pipe/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/mut-m3-duplicate-id.diff.txt:3   -> .../mirror/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/mut-m3-duplicate-id.sha256:1     -> .../mut/m3-duplicate-id/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/mut-m4-community-tier-a.diff.txt:3-> .../mirror/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/mut-m4-community-tier-a.sha256:1  -> .../mut/m4-community-tier-a/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/mut-m5-missing-usedby.diff.txt:3  -> .../mirror/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/mut-m5-missing-usedby.sha256:1    -> .../mut/m5-missing-usedby/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/post.validate.txt:16             -> .../mirror/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/pristine.after-baseline.sha256:1 -> .../mirror/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/pristine.post.sha256:1           -> .../mirror/corpus/SOURCES.md
.ufo/waves/round-34/build/R34MutRegistry/out/pristine.sha256:1                -> .../mirror/corpus/SOURCES.md
```

These are absolute-path receipts (`sha256sum` output and census `file ok <abs path>` lines). The
paths are absolute, so they point into the *live lane working tree*, not into a committed path —
which is why the `git grep` for the relative prefix does not surface them, and why the `git grep`
in the seat brief under-counts. Reproduce:

```
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin grep -n -I -e 'R34MutRegistry/mirror/corpus/SOURCES.md' \
    -e 'R34MutRegistry/mut/' dfee6fff631ebc5f623ba4506e5c7992a215401c -- .ufo/waves/round-34/build/R34MutRegistry/out/
```

The receipts no longer verify in place:

```
$ cd $D/lane/.ufo/waves/round-34/build/R34MutRegistry
$ sha256sum -c out/pristine.sha256
sha256sum: /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-34/build/R34MutRegistry/mirror/corpus/SOURCES.md: No such file or directory (os error 2)
$ sha256sum -c out/mut-m1-column-count.sha256
sha256sum: .../R34MutRegistry/mut/m1-column-count/corpus/SOURCES.md: No such file or directory (os error 2)
```

(the lane path is hard-coded in the receipt, so the check fails against the fixture's clone too).
**This is a present-tense false statement in committed bytes** — a receipt that says "hash of file
X" where X no longer exists anywhere in the working tree.

### B. Deleted-root-name citations — 24 files, 36 lines

Files that name one of the three deleted roots (as a path prefix, not necessarily as a
resolvable file):

- `.ufo/waves/round-34/build-results.json:335`
- `.ufo/waves/round-34/build/R34MutEntries.md:10`, `:91`
- `.ufo/waves/round-35/build/R35ConnDefectClasses.md:59`
- `.ufo/waves/round-35/build/R35LessonDraft/round-35.md:25`
- `.ufo/waves/round-35/build/R35MutLedgerD1D2.md:74,75,76,78,79,80,99,100`
- `.ufo/waves/round-35/build/R35RevLedger.md:17`
- `.ufo/waves/round-35/make_falsify_spec.py:62`, `:76`
- `LOG.md:1007`
- `corpus/lessons/round-34-verifier-spotcheck.md:30`, `:31`, `:76`
- plus the 15 `out/` files from class A (their absolute paths contain the root names)

### C. Relative citations inside the seat's own directory — 1 file, 2 lines

`.ufo/waves/round-34/build/R34MutRegistry.md:4` — "Writes confined to `.ufo/waves/round-34/build/R34MutRegistry/`
(this report, `probe.sh`, `out/`, `mirror/`, `mut/`)" — and `:8` — "`mirror/` = byte copy of lane `corpus/`".
Both name directories that the deletion removed.

## Finding 2 — is each dangling citation still resolvable through history? (yes, with one commit named)

Every deleted path was added by **`0b3c627d5199e291b2674a84fdfc87a752923981`** ("round-34:
evaluator coverage attempt and calibration honest stop", 2026-10-25) and removed by `dfcd294c`.
`0b3c627` is reachable and is an ancestor of `refs/heads/master`, so the blobs are not gc-able:

```
$ git log --all --format='%H %s' --diff-filter=A -1 -- .ufo/waves/round-34/mut-entries-scratch
0b3c627d5199e291b2674a84fdfc87a752923981 round-34: evaluator coverage attempt and calibration honest stop
$ git log --all --format='%H %s' --diff-filter=A -1 -- .ufo/waves/round-34/build/R34MutRegistry/mirror
0b3c627d5199e291b2674a84fdfc87a752923981 round-34: evaluator coverage attempt and calibration honest stop
$ git log --all --format='%H %s' --diff-filter=D -1 -- .ufo/waves/round-34/mut-entries-scratch
dfcd294c60a00215c55bc4ce0b620440cd5e402f round-35: C2 close round-34 routed defects D1-D5 (...)
$ git merge-base --is-ancestor 11d64530 refs/heads/master && echo YES
YES
```

And the *content* is byte-recoverable: every one of the six cited deleted files reproduces its
committed receipt digest exactly from `0b3c627`:

```
$ git show 0b3c627:.ufo/waves/round-34/build/R34MutRegistry/mirror/corpus/SOURCES.md | sha256sum
53b5f9ec6b13032e74b4d36338186b9674f0c76f95accce0709c6a773c896e1d -     # == out/pristine.sha256
$ for n in m1-column-count m2-escaped-pipe m3-duplicate-id m4-community-tier-a m5-missing-usedby; do ... done
m1-column-count        rec=8acc8321050e act=8acc8321050e MATCH
m2-escaped-pipe        rec=7ad0d218ec99 act=7ad0d218ec99 MATCH
m3-duplicate-id        rec=69abb3ac41b1 act=69abb3ac41b1 MATCH
m4-community-tier-a    rec=9278cbdac734 act=9278cbdac734 MATCH
m5-missing-usedby      rec=a3952812c2f4 act=a3952812c2f4 MATCH
```

So: **every dangling citation is resolvable through history, and the single commit that holds all
of them is `0b3c627`** (with `11d64530` as the last tree containing the roots intact). The
round-35 lesson's claim "mirror roots deleted at the tip (history keeps them; no rewrite)"
(`corpus/lessons/round-35.md:26`) is **verified true**, and so is `LOG.md:1008` "deleted at the
tip (history keeps them)".

The routed-defect source line that D2's own check depends on also still resolves — it is a
citation of a *commit*, and that commit is still in the tree:

```
$ git ls-tree -r -l 58a19f37 -- .ufo/waves/round-34/mut-entries-scratch | awk '{n++; s+=$4} END {print "blobs="n" logical_MiB="s/1048576}'
blobs=106323 logical_MiB=1650.56
```

which reproduces the `corpus/lessons/round-34-verifier-spotcheck.md:31` figure (106,323 blobs,
1650.6 MiB) **exactly**, and the per-root counts behind `R35RevLedger.md`'s F3 finding are also
reproducible from history:

```
$ git ls-tree -r --name-only 11d64530 -- .ufo/waves/round-34/mut-entries-scratch | wc -l   -> 106323
$ git ls-tree -r --name-only 11d64530 -- .ufo/waves/round-34/build/R34MutRegistry/mirror | wc -l -> 515
$ git ls-tree -r --name-only 11d64530 -- .ufo/waves/round-34/build/R34MutRegistry/mut | wc -l -> 2575
```

(515 + 2,575 + 106,323 = 109,413 — the frozen ledger figure.)

## Finding 3 — is any dangling citation load-bearing for an admitted claim? **No. Zero.**

This is the load-bearing test, and it is a negative result, so here is the evidence that would
have shown disagreement.

**Test 1 — intersection with the admitted counters' read-sets is empty.** The files an admitted
counter actually opens:

- `plans/round35_c1_verify.py` (C1): `corpus/evidence/round35/tb2-eval/*`, `corpus/SOURCES.md`,
  `corpus/README.md`, `corpus/knowledge/tb2-protein-assembly-grader.md`,
  `corpus/evidence/round35/tb2-grader-probe.txt`, `plans/tb2_grader_probe.py`,
  `scripts/sources-census.sh`.
- `plans/defect_ledger.py` (C2): `corpus/defects.jsonl`, `corpus/lessons/round-34.md`,
  `corpus/lessons/round-35.md`, `.ufo/waves/round-34/assimilation/captures/tb2-eval/SHA256SUMS`,
  `.ufo/waves/round-34/assimilation/captures/nec-s091-reopen.html`,
  `.ufo/waves/round-34/build/R34C2CounterDraft.md`, `.ufo/waves/round-34/build/R34MutC2Harness.md`,
  `SCORECARD.md`.

```
A ∩ admitted-counter read-set = []
```

**Test 2 — no admitted surface cites a deleted path.** Deleted-path citations per admitted file:

```
corpus/knowledge/tb2-protein-assembly-grader.md: 0
corpus/SOURCES.md:                              0
corpus/README.md:                               0
corpus/defects.jsonl:                           0
corpus/lessons/round-35.md:                     0
corpus/lessons/round-34.md:                     0
corpus/evidence/round35/tb2-grader-probe.txt:   0
corpus/evidence/round35/tb2-eval/SHA256SUMS:    0
SCORECARD.md:                                   0
LOG.md:                                         0
plans/round-35-claims.md:                       0
```

(`LOG.md` appears in the class-B *root-name* list at `:1007`, but that line is the narrative
"D2: 109,413 committed mirror paths … deleted at the tip (history keeps them)" — it describes the
deletion, it does not depend on the bytes. It also carries zero *exact deleted-path* citations.)

**Test 3 — the registry is clean.** No `used-by` cell of `corpus/SOURCES.md` points into a deleted
root, and no row's used-by points at the deleted round-34 entry:

```
$ git show dfee6fff…:corpus/SOURCES.md | grep -n -E 'mut-entries-scratch|R34MutRegistry'
(nothing)
```

**Test 4 — both predicates still pass at the tip in a clean clone** (quoted in full above):
`checks=6 defects=0 / PREDICATE C1 pass / exit 0` and `rows=5 closed=5 observed_pass=5
mismatches=0 / PREDICATE C2 pass / exit 0`. If any dangling citation were load-bearing, one of
these would have gone red at the tip; neither did.

**Test 5 — the only round-35 report that *reads* the dangling receipts is not admitted.** The 15
class-A files live in `.ufo/waves/round-34/build/R34MutRegistry/out/`. Nothing at tip reads them:

```
$ git grep -n -I -e 'R34MutRegistry/out' dfee6fff… -- .
(nothing)
```

Their parent report `.ufo/waves/round-34/build/R34MutRegistry.md` is cited only by the round-34
wave machinery (`build-dispatch.json`, `build-plan.txt`, `build-results.json`), never by
`corpus/`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md` or `plans/`:

```
$ git grep -n -I -e 'R34MutRegistry\.md' dfee6fff… -- corpus/ SCORECARD.md LOG.md PROVINCE.md plans/
(nothing)
```

## Finding 4 — the one *present-tense false statement* in committed bytes (not load-bearing)

Three committed sentences assert the deleted trees as if they exist now. These are the only
dangling citations that are factually wrong rather than merely pointing at history:

1. `.ufo/waves/round-34/build/R34MutEntries.md:91` —
   "Scratch mirrors retained as evidence under `.ufo/waves/round-34/mut-entries-scratch/`"
   → the directory is gone at tip. This is the *only* "retained as evidence" claim in the tree.
2. `.ufo/waves/round-34/build/R34MutRegistry.md:4` — "Writes confined to … (this report, `probe.sh`,
   `out/`, `mirror/`, `mut/`)" and `:8` — "`mirror/` = byte copy of lane `corpus/`"
   → `mirror/` and `mut/` are gone at tip.
3. The 15 class-A receipts — `sha256sum` lines naming an absolute lane path that no longer exists
   (demonstrated failing `sha256sum -c` above).

Load-bearing? **No.** All three live in round-34 wave evidence that nothing at tip reads
(Test 5), and the round-35 lesson (`corpus/lessons/round-35.md:26`) correctly states the mirror
roots *were* deleted with history intact. These are stale sentences, not broken admissions.

## Finding 5 — a second, distinct dangling class: `plans/round34_*.py` (33 files, 120 lines)

The same commit `dfcd294` also **moved** the three round-34 plan drafts out of `plans/` into
`.ufo/waves/round-34/drafts/` (the `R100` renames). At tip:

```
$ for p in plans/round34_c1_verify.py plans/round34_defects.py plans/round34_mutate.py; do
    git cat-file -e dfee6fff…:"$p" && echo PRESENT || echo MISSING; done
MISSING MISSING MISSING
$ git ls-tree -r --name-only dfee6fff… -- .ufo/waves/round-34/drafts/
.ufo/waves/round-34/drafts/round34_c1_verify.py
.ufo/waves/round-34/drafts/round34_defects.py
.ufo/waves/round-34/drafts/round34_mutate.py
```

(`git log --all -- plans/round34_c1_verify.py` is empty: those paths were **never tracked** — they
were the untracked D1 leftovers the round-34 spot-check counted. So their citation is unresolvable
in history *at that path*; the content survives at the new `drafts/` path.)

33 committed files still cite `plans/round34_c1_verify.py` / `plans/round34_defects.py` /
`plans/round34_mutate.py` (120 lines), including `SCORECARD.md` (2 lines, at the round-34 C1 row
`:1164`) and `plans/round-34-claims.md` (10 lines). Two sub-cases:

- **Intentional.** `plans/defect_ledger.py:38-41` names the three paths as the D1 *watchlist*
  (`git ls-files --others --exclude-standard -- plans/round34_c1_verify.py …`). This is the guard
  mechanism and must keep naming them. Not dangling in the harmful sense.
- **Stale.** The 2 `SCORECARD.md` lines are a **readable instruction that no longer works**:
  SCORECARD.md:1164 tells the reader the round-34 C1 counter is
  `plans/round34_c1_verify.py --lane .`, and that file does not exist at tip. The row itself is
  marked "not admitted; no axis score move", so it carries no admitted claim — but it is a
  user-facing broken command in a permanent surface.

Class A ∪ class B-`plans/round34_*` = **50 distinct committed files** carry at least one
citation to a path that no longer exists at tip (17 A-only, 25 B-only, 8 in both).

## Finding 6 — a live re-creation vector: the committed `probe.sh` rebuilds the deleted trees

The committed script `.ufo/waves/round-34/build/R34MutRegistry/probe.sh` writes to the very paths
the D2 commit deleted, and it hard-codes the live lane:

```
probe.sh:8   LANE=/home/vgpnk/Projects/shokunin/kengaku-shokunin
probe.sh:9   S="$LANE/.ufo/waves/round-34/build/R34MutRegistry"
probe.sh:12  rm -rf "$OUT" "$S/mirror" "$S/mut"
probe.sh:13  mkdir -p "$OUT" "$S/mirror" "$S/mut"
probe.sh:41  rm -rf "$d"; mkdir -p "$d/corpus"
```

Running it as committed re-creates `mirror/` and `mut/` **inside the lane**. That is exactly what
D1 is supposed to catch, and it does — reproduced in the fixture clone:

```
$ mkdir -p $D/lane/.ufo/waves/round-34/build/R34MutRegistry/mirror/corpus
$ echo x > $D/lane/.ufo/waves/round-34/build/R34MutRegistry/mirror/corpus/SOURCES.md
$ git -C $D/lane ls-files --others --exclude-standard -- .ufo/waves/round-34/
.ufo/waves/round-34/build/R34MutRegistry/mirror/corpus/SOURCES.md
$ python3 $D/lane/plans/defect_ledger.py --lane $D/lane
R34-D1 status=closed observed=fail agree=NO untracked=1
R34-D2 status=closed observed=pass agree=yes committed_mirror_paths=0
…
rows=5 closed=5 observed_pass=4 mismatches=1
PREDICATE C2 fail
exit=1
```

**Reading:** D1 is a working-tree check and D2 is a committed-tip check; the same recreated
mirror trips D1 (red) and not D2 (green, since it is untracked). The guards do cover the
round-34 tree — but only for *untracked* leakage under `.ufo/waves/round-34/` and *committed*
leakage under the three named roots. A **committed** mirror under a *fourth* round-34 path
(`.ufo/waves/round-34/build/R34ReviewCounterC1Attacks/…`, which already exists in committed form
with 28 same-class paths) would trip neither. That is the calibration gap named in "What was
deleted" above, now with the mechanism: `r34_d2`'s root list is a three-element allowlist.

The probe.sh re-creation test itself could not be executed end-to-end because `/tmp` hit 100%
(`No space left on device` on the fixture write). The `mkdir`/`rm -rf` behaviour is established
from the committed script text (lines 8-13, 41) and the D1 trip is demonstrated directly with an
equivalent file creation, so the claim "running probe.sh re-creates the mirror under the lane" is
supported by script text plus an equivalent demonstrated D1 trip; the full probe.sh run is
**not** reported as executed.

## Summary table

| # | dangling class | citing files | lines | resolvable in history? | load-bearing for C1/C2? |
|---|---|---|---|---|---|
| A | exact deleted file path (`R34MutRegistry/mirror\|mut/...`) | 15 | 15 | yes — `0b3c627` (bytes+digest verified) | **no** (0 read it) |
| B | deleted root name cited | 24 | 36 | yes — `0b3c627`; counts reproduce exactly | **no** |
| C | relative `mirror/`/`mut/` in own seat dir | 1 | 2 | yes — `0b3c627` | **no** |
| — | `plans/round34_*.py` (moved to `drafts/`, never tracked) | 33 | 120 | at old path: **never in history**; content at `.ufo/waves/round-34/drafts/` | **no** (D1 watchlist is intentional; SCORECARD:1164 is a stale but non-admitted command) |
| union A∪B∪C | | **25** | | | **0 load-bearing** |
| union incl. `plans/round34_*` | | **50** | | | **0 load-bearing** |

## What I did not run / could not run

- The **full** `probe.sh` end-to-end re-run (blocked: `/tmp` at 100%, 128G; the file write failed
  with `ENOSPC`). The re-creation vector is established from script text + an equivalent D1 trip.
- A mutation that **commits** a same-class mirror under a *fourth* round-34 path (to prove the
  `r34_d2` allowlist gap empirically). The gap is established from the committed tree contents
  (28 same-class paths already committed under `.ufo/waves/round-34/build/R34ReviewCounterC1Attacks/`,
  which the three guard roots do not cover) and from the check's implementation
  (`plans/defect_ledger.py:49-51`, three literal roots). The sibling seat `F35MutLedgerD2` owns
  the D2 mutation test; I did not duplicate it.
- No `git add/commit/stash/checkout/reset/push` and no mutating `jj` was run in the lane. The one
  fixture-commit attempt inside the clone was abandoned when `/tmp` filled; the clone is deleted.

## Files written by this seat

- `.ufo/waves/round-35/falsify/F35DanglingRefs.md` (this report)
- `/tmp/k35f-dangle-d7fy` (fixture) — created and `rm -rf`'d by this seat.

VERDICT: dangling-50-loadbearing-0
