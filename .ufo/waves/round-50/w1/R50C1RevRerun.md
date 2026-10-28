# R50C1RevRerun — independent rerun of the frozen R50-C1 predicate against the repair candidate

Seat: reviewer (`R50C1RevRerun`), leaf member, no dispatch. Serving **R50-C1 (novelty)**.
Item: rerun the frozen predicate against
`.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py` on a clean clone at
`3b02d573d58cc6d2e0d27ef92ac0815354912252`, report every line verbatim, the exit code, and whether
HONEST / REFUSALS / SEALED match the seat's claim. No summary accepted; this is a rerun, not a review of a
summary.

## Axes named

1. **Reproducibility** — does an independent clean clone + independent invocation print the same leg lines?
2. **Claim match** — do HONEST / REFUSALS / SEALED equal the seat's own receipt, and do they satisfy the frozen
   predicate sentence in `plans/round-50-claims.md` §C1?
3. **Instrument soundness** — do the frozen literals (`126`, `20`, `12`, `SEALED50_MIN`, population pin) bind in
   the counter, or can a tree satisfy a leg vacuously?
4. **Repair completeness** — which honest classes moved, which did not, and what code path holds each refusal.

## Revision measured

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
```

Ancestry asserted **before** any measurement:

```
$ cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
$ git rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/kengaku-shokunin
$ git rev-parse HEAD
c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
$ git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD && echo ANCESTOR=yes
ANCESTOR=yes
$ git log -1 --format='%H %ci %s' 3b02d573d58cc6d2e0d27ef92ac0815354912252
3b02d573d58cc6d2e0d27ef92ac0815354912252 2026-10-28 14:18:09 -0300 round-50: C1 four-control receipts and C2 before/selftest receipts (pre-data)
```

Lane tip observed `c3372a9b24d3a200946a6b37dc0a31ed5c982cc1`; the freeze is an ancestor. The clone used for
every measurement is a `git clone --shared` of the lane checked out at the freeze:

```
$ git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin lane50
$ cd lane50 && git checkout -q 3b02d573d58cc6d2e0d27ef92ac0815354912252
$ git rev-parse HEAD
3b02d573d58cc6d2e0d27ef92ac0815354912252
$ git rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r50/R50C1RevRerun/lane50
$ git status --porcelain        # empty
```

Host: `git version 2.56.0`, `Python 3.14.8`. The lane checkout was never written; every git call in this seat
was `git -C <scratch clone>` or `-C <lane>` read-only (`rev-parse`, `status`, `ls-tree`, `log`, `merge-base`).

## Commands run

```
# baseline: the do-nothing fence, my harness reproduces the measured state
python3 plans/round50_c1_verify.py --lane . --work "$S/work-base" --skip-mutants

# candidate, fast legs
python3 plans/round50_c1_verify.py --lane . --fence "$S/cand-final.py" --work "$S/wfinal" --skip-mutants

# candidate, the full frozen predicate including MUTANTS
python3 plans/round50_c1_verify.py --lane . --fence "$S/cand-final.py" --work "$S/wfinal"

# instrument probe: does SEALED50_MIN bind when plans/sealed50 is absent? (scratch copy of the clone)
mkdir -p "$S/lane50-probe/plans/sealed50"
python3 plans/round50_c1_verify.py --lane . --fence "$S/cand-final.py" --work "$S/work-probe" --skip-mutants

# post-item: the literal frozen predicate on a fresh clone of the lane tip (fence committed at 6db0279)
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin lane-tip
git -C lane-tip checkout -q d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
cd lane-tip && python3 plans/round50_c1_verify.py --lane . --work "$S/wtip"     # run twice; diff empty
```

`$S` = `/fast/scratch/hyaku/kengaku-r50/R50C1RevRerun`; `cand-final.py` is a byte copy of the live candidate
(`sha256 6df6a2a3…`, taken 17:32Z, re-verified unchanged at 17:36Z; `9baedf13…` measured at 17:37Z
through the same knob). The candidate was **live-edited during my
window** — five distinct digests were measured (see §"Per-revision table"); the full receipt below is pinned to the
last one.

## Observed output — baseline (do-nothing fence at the freeze commit), verbatim

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1RevRerun/lane50/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n14-stash-entry ../../../../work-base/k50-c1-67asm54z/honest/m026-plans-honest50-modules-novel48-n14_stash_entry/f000/repo/.git/logs/refs/stash has a name git does not write
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph present (object-store redirect)
HONEST-REFUSED n16-notes-ref ../../../../work-base/k50-c1-67asm54z/honest/m028-plans-honest50-modules-novel48-n16_notes_ref/f000/repo/.git/logs/refs/notes has a name git does not write
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
EXIT=1
```

This is the frozen "before" line `HONEST fixtures=126 admitted=113 refused=13` and control row 1, reproduced on
my own clone: harness validated before the candidate was scored. The counter prints at most 12
`HONEST-REFUSED` lines (`refused[:12]`), so the 13th base refusal is not printed; it is `n08-tag-detached`, as
the candidate run below shows (`13 − 4 repaired = 9`, and the candidate's 9 include `n08`).

## Observed output — candidate `sha256 6df6a2a3…`, full frozen predicate, verbatim

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1RevRerun/cand-final.py sha256=6df6a2a331a66195cfeb963b457372596cd55ac1199d7d97027323a533a76ec2
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=117 refused=9 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n14-stash-entry ../../../../wfinal/k50-c1-x5r6nk1n/honest/m026-plans-honest50-modules-novel48-n14_stash_entry/f000/repo/.git/logs/refs/stash has a name git does not write
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph is not git's alternates file
HONEST-REFUSED n16-notes-ref ../../../../wfinal/k50-c1-x5r6nk1n/honest/m028-plans-honest50-modules-novel48-n16_notes_ref/f000/repo/.git/logs/refs/notes has a name git does not write
HONEST-REFUSED n18-shallow-fetch repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n03-detached-head repo/.git/HEAD is not a plain branch HEAD
HONEST-REFUSED n07-reflog-gc repo/.git/info/refs is not git's exclude file
HONEST-REFUSED n08-tag-detached repo/.git/HEAD is not a plain branch HEAD
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
MUTANTS total=23 caught=1 broken=15 floor=12 verdict=unmet
PREDICATE R50-C1 fail
EXIT=1
```

Mutant detail lines (verbatim, 15 `broken` / 7 `survived`):

```
MUTANT broken c1-mut-01-gitdir-file patch-rc=1 1 out of 1 hunk FAILED
MUTANT broken c1-mut-02-symlink-dir-dead patch-rc=1 1 out of 1 hunk FAILED
MUTANT broken c1-mut-03-drop-file-mountbound patch-rc=1 1 out of 1 hunk FAILED
MUTANT broken c1-mut-04-hardlink-threshold patch-rc=1 1 out of 1 hunk FAILED
MUTANT broken c1-mut-05-git-top-commondir patch-rc=1 1 out of 1 hunk FAILED
MUTANT broken c1-mut-06-objinfo-fallthrough patch-rc=1 1 out of 1 hunk FAILED
MUTANT survived c1-mut-07-config-cr
MUTANT broken c1-mut-08-config-unknown-key patch-rc=1 1 out of 1 hunk FAILED
MUTANT broken c1-mut-09-url-insteadof patch-rc=1 2 out of 2 hunks FAILED
MUTANT survived c1-mut-10-inside-prefix
MUTANT broken c1-mut-11-head-ref-widen patch-rc=1 1 out of 1 hunk FAILED
MUTANT survived c1-mut-12-store-required
MUTANT survived c1-mut-14-argv-placeholder
MUTANT broken c1-mut-15-hook-suffix patch-rc=1 1 out of 1 hunk FAILED
MUTANT survived c1-mut-16-argv-shape-tail
MUTANT broken c1-mut-17-config-value-backslash patch-rc=1 1 of 1 hunk FAILED
MUTANT broken c1-mut-18-graph-magic-empty patch-rc=1 1 out of 1 hunk FAILED
MUTANT broken c1-mut-19-lane-membership patch-rc=1 1 out of 1 hunk FAILED
MUTANT survived c1-mut-20-packedref-peel
MUTANT broken c1-mut-21-log-namespace patch-rc=1 1 out of 1 hunk FAILED
MUTANT survived c1-mut-22-fixture-symlink
MUTANT broken c1-mut-23-gitdir-repo-reorder patch-rc=1 1 out of 1 hunk FAILED
```

## Does it match the seat's claim?

The repair seat published its own receipts in `C1ExecRepair/` during my window
(`receipt-candidate-skip-mutants.txt`, `receipt-candidate-mutants.txt`, `receipt-base-fence-control.txt`, all
`FENCE … sha256=6df6a2a3…`). Comparison, line for line:

| line | seat receipt (`C1ExecRepair/`) | my independent rerun | match |
|---|---|---|---|
| `REV` | `3b02d573…` | `3b02d573…` | ✅ |
| `TREE dirty=` | `0` | `0` | ✅ |
| `POPULATION` | `fixtures=126 pin=b5197f94… mismatched=0 build_errors=0` | identical | ✅ |
| `HONEST` | `fixtures=126 admitted=117 refused=9 error=0` | identical | ✅ |
| the 9 `HONEST-REFUSED` | n12, n13, n14, n15, n16, n18, n03, n07, n08 with the same reasons | identical, byte-for-byte apart from the work-dir path in the n14/n16 lines | ✅ |
| `REFUSALS` | `total=20 clean=20 leaked=0 build_errors=0` | identical | ✅ |
| `SEALED` | `total=12 clean=12 leaked=0 build_errors=0` | identical | ✅ |
| `MUTANTS` | `total=23 caught=1 broken=15 floor=12 verdict=unmet` | identical | ✅ |
| `PREDICATE` | `R50-C1 fail` | identical | ✅ |
| exit | 1 | 1 | ✅ |

**The seat's numbers reproduce exactly; the seat does not claim a pass.** The candidate therefore does **not**
satisfy the frozen predicate in `plans/round-50-claims.md` §C1, which requires
`HONEST fixtures=126 admitted=126 refused=0`, `SEALED total=<S>` with `<S> ≥ 18`, `MUTANTS … caught ≥ 12 …
verdict=met`, `PREDICATE R50-C1 pass`, exit 0. Three of the five legs fail.

Per-revision table (candidate edited under me; each digest measured once on the same clone):

| candidate sha256 | utc | HONEST | REFUSALS | SEALED | MUTANTS | PREDICATE |
|---|---|---|---|---|---|---|
| `cb0dd886…` (14:29 local) | ~17:24Z | 117/9 | 20/20 | 12/12 | not run | fail |
| `0117b4b6…` (14:30 local) | ~17:29Z | 117/9 | 20/20 | 12/12 | not run | fail |
| `ae47fc3e…` | 17:31Z | 117/9 | 20/20 | 12/12 | caught=1 broken=15 | fail |
| `6df6a2a3…` (14:31) | 17:32Z–17:36Z stable | 117/9 | 20/20 | 12/12 | caught=1 broken=15 | fail |
| `9baedf13…` (14:37, newest) | 17:37Z | 117/9 | 20/20 | 12/12 | not run | fail |

## Findings

### F1 — blocking (candidate): the repair moves HONEST 113 → 117 and stops; 9 documented honest states stay refused

The candidate repairs exactly four classes — `n17-replace-ref`, `n20-linked-worktree`, `n21-separate-gitdir`,
`n22-alternates-in-d` — and touches none of the other nine. Each remaining refusal is held by an identifiable
line of the candidate:

| class | refusal printed | code path that holds it |
|---|---|---|
| `n03-detached-head`, `n08-tag-detached` | `HEAD is not a plain branch HEAD` | `_store`: `HEAD_REF = \Aref: refs/heads/…` — a 40-hex detached HEAD never matches |
| `n07-reflog-gc` | `info/refs is not git's exclude file` | `_store`: the `info/` walk admits `exclude` only |
| `n12-local-config-user` | `config section [user] is not allowlisted` | `CFG_SECTIONS = {"core", "extensions"}` |
| `n13-remote-origin`, `n18-shallow-fetch` | `config section header b'[remote "origin"]' is not plain` | `SECTION_LINE = \A\[([A-Za-z][A-Za-z0-9.-]*)\]\Z` has no subsection form; `n18`'s `FETCH_HEAD` is now admitted by name but its `[remote "origin"]` block (the `../src` relative URL the class requires) is not |
| `n14-stash-entry`, `n16-notes-ref` | `…/logs/refs/stash`/`logs/refs/notes` `has a name git does not write` | `_log_name_ok` admits `HEAD` and `refs/(heads\|tags)/…` only |
| `n15-commit-graph` | `objects/info/commit-graph is not git's alternates file` | `_objects`: `objects/info` admits `alternates` only (the base's blanket object-store refusal was narrowed, but `commit-graph` is still refused) |

Each of these is a state the frozen population calls honest and `git` itself writes; the frozen kill rule is
`HONEST admitted < 126` → C1 not admitted. The candidate is a partial repair, not a repair.

### F2 — blocking (mutant leg): the carried battery cannot be scored against the repaired fence

`MUTANTS total=23 caught=1 broken=15 floor=12 verdict=unmet`. The 15 `broken` rows fail `patch` with
`1 out of 1 hunk FAILED`: the payloads are inline diffs against the **r49 candidate** fence's context (e.g.
`c1-mut-01` deletes the base's blanket `.git`-file rule at `@@ -259,8 +259,6 @@`, which the repaired fence no
longer contains). Seven rows apply and **survive** on the repaired fence: `c1-mut-07-config-cr`,
`c1-mut-10-inside-prefix`, `c1-mut-12-store-required`, `c1-mut-14-argv-placeholder`, `c1-mut-16-argv-shape-tail`,
`c1-mut-20-packedref-peel`, `c1-mut-22-fixture-symlink`. So the battery is not only inapplicable, it is
directionally stale: those seven kill directions are not witnessed on this fence (QUALITY Q38 requires
witnessing, not assuming). Even with HONEST at 126 the predicate would print
`verdict=unmet` and `PREDICATE R50-C1 fail`.

### F3 — high (instrument): `SEALED50_MIN` does not bind when `plans/sealed50/` is absent

`plans/round50_c1_verify.py:262-265`:

```python
if (lane / "plans/sealed50").is_dir():
    n = len(sorted((lane / "plans/sealed50").glob("*.py")))
    if n < SEALED50_MIN:
        say(f"SEALED50-TOTAL {n} expected_min={SEALED50_MIN}")
        ok = False
```

`plans/sealed50/` exists at neither the freeze commit nor the lane tip
(`git ls-tree -d --name-only c3372a9… plans/` → `plans/sealed46` only), so on the tree every receipt in this
wave measures, the guard is skipped entirely: the run above prints no `SEALED50-TOTAL` line and accepts
`SEALED total=12 clean=12`. Probe on a scratch copy of the clone with an empty `plans/sealed50/` added:

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
HONEST fixtures=126 admitted=117 refused=9 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=0 clean=0 leaked=0 build_errors=0
SEALED50-TOTAL 0 expected_min=6
PREDICATE R50-C1 fail
EXIT=1
```

The pin fires only when the directory exists. Consequence: a tree with **zero** blind modules satisfies the
SEALED leg (12 ≥ 12 frozen, `leaked=0`), so `SEALED total=<S>` with `<S> ≥ 18` is not an enforced invariant —
it is an accident of whether the directory is present. This contradicts §C1's own sentence that `<S>` and `<M>`
"are literals in the counter … not values the counter can satisfy from the files it reads". No control catches
it: control row 1 (do-nothing) fails on HONEST, so the SEALED leg is never the failing leg in any control.
Repairable inside the open window (the predicate sentence, leg names and literals do not change): make the
absence of `plans/sealed50/` a `SEALED50-TOTAL 0 expected_min=6` failure instead of a skip.

### F4 — medium (instrument): the SEALED leg prints two lines, so the frozen receipt line cannot appear

`leg()` labels every non-refusal directory `SEALED`
(`label = "REFUSALS" if rel == REFUSALS_REL else "SEALED"`) and is called once per entry of
`SEALED_RELS = ("plans/sealed46", "plans/sealed50")`. Once the blind modules land, a run prints
`SEALED total=12 …` **and** `SEALED total=<blind> …` — observed in the probe above — so the single frozen line
`SEALED total=<S> clean=<S> leaked=0 build_errors=0` with `<S>` ≥ 18 will never be printed as one line, and a
receipt checker matching the claim's literal line will read `SEALED total=12` and stop. The two directories
must be aggregated into one leg before the S3 receipt exists.

### F5 — low (instrument): a missing `--work` directory is a traceback with exit 1, not a setup error

`tempfile.mkdtemp(dir=a.work)` raises `FileNotFoundError` when `--work` does not exist; the process exits 1 with
a Python traceback and no `PREDICATE` line — the same exit code as `fail`, while the docstring reserves exit 2
for setup errors. Observed verbatim on my first invocation:

```
FileNotFoundError: [Errno 2] No such file or directory: '/fast/scratch/hyaku/kengaku-r50/R50C1RevRerun/work-fast/k50-c1-2qd54gd0'
EXIT=1
```

An operator typo is thus indistinguishable from a predicate failure by exit code alone.

### F6 — observation (not a defect of the candidate): every number here is a `--fence` run, not the literal frozen command

The frozen command is `python3 plans/round50_c1_verify.py --lane .` with the fence at
`plans/fixture_fence.py`. The candidate is uncommitted by design (seats cannot edit production), so it can only
be scored through the testing knob `--fence PATH`. The `FENCE … sha256=` line makes the substitution auditable,
but no receipt produced this wave can be the frozen predicate until the repaired fence lands at
`plans/fixture_fence.py` in the S2 commit. The dirty-tree guard covers the lane only; a modified `--fence` file
outside the tree is invisible to `TREE dirty=` by construction.

## What does hold (measured, not assumed)

- `POPULATION fixtures=126 pin=b5197f94… mismatched=0 build_errors=0` — the pinned population rebuilds with
  zero identity mismatches on an independent clean clone at the freeze commit.
- `REFUSALS total=20 clean=20 leaked=0` and `SEALED total=12 clean=12 leaked=0` on the candidate — the four new
  admissions (`n17`, `n20`, `n21`, `n22`) open no hole in the 32 frozen hostile modules.
- The candidate starts no git child: its imports are `os`, `pathlib`, `re`, `stat` only (code fact; the
  outside-`d` read property remains with `plans/round46_c1_verify.py` and was not measured here).

## Limits

- Measured on one host (`git 2.56.0`, `Python 3.14.8`); the population is host-sensitive by design and the
  identity pins are what make that visible.
- The candidate was live-edited during my window (five digests,
  `cb0dd886 → 0117b4b6 → ae47fc3e → 6df6a2a3 → 9baedf13`); every digest printed the same HONEST 117/9,
  REFUSALS 20/20 and SEALED 12/12. The full receipt (including MUTANTS) is pinned to `6df6a2a3…` at
  17:32Z–17:36Z; the newest digest `9baedf13…` was measured at 17:37Z on the fast legs with identical results.
  The comparison in §"Does it match the seat's claim?" was made against the seat's receipts; its report
  `R50C1ExecRepair.md` (seat-prefixed path, on disk since 14:33) was read afterwards and carries the same
  lines — see §"Corrections". A later revision needs a new rerun, not this report.
- Not measured here: outside-`d` reads (no strace leg in this counter), io_uring, `plans/round46_c1_verify.py`'s
  B1–B6 legs, and the `MUTANTS` kill directions beyond the seven survivors listed in F2.
- No lane write, no commit, no mutating git/jj command; all fixtures ran inside
  `/fast/scratch/hyaku/kengaku-r50/R50C1RevRerun`, removed before yield.

## Verdict

**VERDICT (the item as assigned): the repair candidate does NOT satisfy the frozen R50-C1 predicate, and the
seat's receipts reproduce exactly.** Independent rerun at `REV 3b02d573d58cc6d2e0d27ef92ac0815354912252` on
candidate `sha256 6df6a2a331a66195cfeb963b457372596cd55ac1199d7d97027323a533a76ec2`:
`HONEST fixtures=126 admitted=117 refused=9 error=0`, `REFUSALS total=20 clean=20 leaked=0 build_errors=0`,
`SEALED total=12 clean=12 leaked=0 build_errors=0`,
`MUTANTS total=23 caught=1 broken=15 floor=12 verdict=unmet`, `PREDICATE R50-C1 fail`, exit **1** — identical,
line for line, to the repair seat's own report (`R50C1ExecRepair.md`, read at 17:40Z) and receipts. HONEST,
REFUSALS and SEALED **match the seat's claim exactly**; none of the three satisfies the frozen predicate, which
needs 126/0, and the candidate additionally fails the mutant floor. The candidate repair is a 4-class partial
(113 → 117) with 9 documented honest states still refused (F1), and the carried r49 mutant battery cannot score
it (F2). It was never the landing artifact: see the post-item verification below.

**Post-item correction to the candidate's status: it is superseded.** The lane committed an S3 fence repair at
`6db0279e2506c1788b26c2586b4d2d774228c6a9` (fence `57adce4a…`), and that fence **passes the literal frozen
predicate** on a clean clone — measured here, not taken from the lane's receipt (below).

## Post-item verification: the committed lane fence passes the literal frozen predicate

After the candidate was measured, the lane moved: `plans/fixture_fence.py` is committed at `6db0279` as
`57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1` (worktree clean for that path), lane tip
`d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78`. On a fresh `git clone --shared` at that tip, with `TREE dirty=0`
and the **literal** command (`--lane .`, no `--fence`):

```
REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
TREE dirty=0
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1RevRerun/lane-tip/plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
EXIT=0
```

Two independent runs on the same clone are byte-identical (`diff` empty), so the pass is deterministic. The
committed S3 receipt `corpus/evidence/round50/c1-receipt.txt` (measured at `d6f2fce`) carries the same nine
lines apart from `REV` and the scratch `FENCE` path, and `# exit=0`.

Facts that follow, stated so the integrator does not misattribute anything:

- The literal predicate is now runnable and passes. Every number in this report *above* this section is
  candidate-scoped and **must not** be attributed to the landed fence `57adce4a…`, which I did not measure
  through the candidate path.
- The mutant floor is satisfied by a **re-derived** 15-row battery (`caught=15 broken=0`), not the carried
  23-row r49 battery that reads `caught=1 broken=15` on the candidate. F2 below therefore describes the
  carried battery, and is resolved in the landing commit by re-derivation, as §C1's open window required.
- `SEALED` prints **two** lines (`12` and `18`), not the one line §C1 quotes. Substance holds — 30 frozen+blind
  modules, all refused, `leaked=0`, and the blind line alone is `18 ≥ 18` — but the quoted receipt block and
  the counter's output do not have the same shape (F4, now live rather than latent).

## Corrections to two statements I made before the lane moved

1. **The repair seat's report exists.** I looked for `C1ExecRepair.md`; the item-named path is seat-prefixed,
   `R50C1ExecRepair.md`. It has been on disk since 14:33 and is non-empty (`sha256 0932339161e3f4…` at 17:40Z,
   still being extended). Its claim lines — `HONEST 117/9`, `REFUSALS 20/20`, `SEALED 12/12`,
   `MUTANTS total=23 caught=1 broken=15 verdict=unmet`, `PREDICATE R50-C1 fail` — are what my rerun reproduces.
   There is no routed defect here; the error was mine.
2. **The lane fence is committed, not dirty.** At 17:38Z I recorded `plans/fixture_fence.py` as modified and
   uncommitted (` M`, sha `57adce4a…`, tip `c3372a9`). That was true when I looked and false minutes later:
   commit `6db0279` landed it at 14:38:49 local, and `git status --porcelain plans/fixture_fence.py` is now
   empty. The digest never changed (`57adce4a…`), only its commit state.

## Instrument defects that survive in the landed counter (`d8787b34…`)

Re-checked at the tip, the landed counter still has all three, at the same lines:

- **F3 (high, latent now):** `if (lane / "plans/sealed50").is_dir(): … if n < SEALED50_MIN` — absence of the
  directory is still a skip, not a failure. It is satisfied by content today (`plans/sealed50/` holds 18
  modules, `18 ≥ 6`), so the landed pass does not depend on the hole; but a tree that drops `plans/sealed50/`
  would still print `SEALED total=12 clean=12` and pass that leg.
- **F4 (medium, live):** the SEALED label is reused per directory, so the scored receipt carries two `SEALED`
  lines (observed). §C1's quoted block shows one line with `<S> ≥ 18`; the counter cannot print that shape.
- **F5 (low):** a missing `--work` parent still tracebacks with exit 1 instead of the documented exit 2.

These are counter/claims-shape defects, not predicate failures: the landed run exits 0 and prints
`PREDICATE R50-C1 pass`.

## Residual risk / verification gaps (updated)

1. F3 remains a satisfied-by-absence guard; only a control that removes `plans/sealed50/` would show it, and no
   control in the wave does.
2. F4 means a judge comparing §C1's quoted single `SEALED` line against the scored receipt sees a mismatch of
   shape (two lines) with no mismatch of substance.
3. The candidate I was assigned and the landed fence `57adce4a…` are textually incompatible repairs; only the
   landed one was measured here through the literal command, and only the candidate through `--fence`.
3b. For the carried r49 battery the seven survivors (`c1-mut-07/10/12/14/16/20/22`) are still unresolved in
   both directions — semantic no-ops on the repaired fence, or unexercised by the population. The landed
   re-derived 15-row battery sidesteps the question rather than answering it for those seven directions.
4. Not measured by this seat: outside-`d` reads (no strace leg in this counter), io_uring,
   `plans/round46_c1_verify.py`'s B1–B6 legs, and the kill direction of each of the 15 re-derived mutants
   beyond `caught=15 broken=0` on the frozen legs.
5. The landed pass is one host (`git 2.56.0`, `Python 3.14.8`) on one clone, reproduced twice; the population's
   identity pins are what make host drift visible.

Scratch: `/fast/scratch/hyaku/kengaku-r50/R50C1RevRerun` removed before yield (verified empty).
