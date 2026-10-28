# R50C1ExecParity — before/after refusal parity for R50-C1 (novelty)

Seat `R50C1ExecParity` (executor, judge=novelty), wave `.ufo/waves/round-50/w1`.
Serves R50-C1: "an honest-geometry instrument for the fixture fence … plus the fence repaired so it passes"
(`plans/round-50-claims.md`).

    REV 85102cf560240ff64943f73d4368b9131f15f7e6

The lane advanced during this wave: the dispatch named `71f5f5f77591d8c3d19297ee9785436da45209e4`, the live
tip at measurement is `85102cf5` ("round-50: receipt re-run on the hardened counter (850ec790) at 61f6257;
instrument/receipt reconciled"). Both the stage-1 freeze `3b02d573d58cc6d2e0d27ef92ac0815354912252` and the
base tip `71f5f5f7` were verified ancestors of the measured tip **before** any measurement:

    $ git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD   -> YES
    $ git merge-base --is-ancestor 71f5f5f77591d8c3d19297ee9785436da45209e4 HEAD   -> YES

All measurement ran against one read-only `git clone --shared` of the lane at that revision
(`git rev-parse --show-toplevel` = `/fast/scratch/hyaku/kengaku-r50/R50C1ExecParity/lane`,
`git rev-parse HEAD` = `85102cf5…`, `git status --porcelain` = 0 lines). Nothing in the lane, the wave dir
outside my own seat dir, or any sibling repo was modified; no commit, push, stash, checkout or jj command was
run; no tool was installed or upgraded.

## Axes (named before the moves)

1. **Parity (primary, serves novelty).** For every fixture of the two frozen hostile sets, is the refusal
   *decision* invariant across the base fence, the r49 candidate and the landed round-50 repair? This is the
   property the claims' SEALED/REFUSALS legs assume and no artifact stated.
2. **Sensitivity of the measuring rig.** A parity table where every cell is `BREACH` is worthless unless the
   same rig, on the same fences, can emit `ADMIT`. Positive control below.
3. **Reproducibility.** The table must be byte-identical across independent runs and independent fixture
   builds, and the fixture population must be the pinned one (identity-checked).
4. **Reconciliation with the frozen instrument.** My per-fixture rows must add up to the counter's own leg
   rollups at the same revision, or one of the two is wrong.

## The three fences measured (digests are the identity of each column)

| column | file | sha256 |
|---|---|---|
| `base` | `plans/fixture_fence.py` @ `71f5f5f7` (= @ freeze `3b02d57`, byte-identical) | `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` |
| `r49` | `.ufo/waves/round-49/w1/R49C1ExecFenceA/fence_a.py` (the r49 candidate; never landed) | `b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52` |
| `repair` | `plans/fixture_fence.py` @ `85102cf5` (the landed S3 repair, `6db0279`) | `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1` |

The base-fence extraction and the r49 candidate copy are in this seat dir (`base_fence.py`,
`r49_candidate.py`, `repair_fence.py`) with `SHA256SUMS.txt`, so every cell is re-runnable from the wave dir
alone.

## Method (no new decision logic)

The driver imports the frozen counter's own functions — `build_all`, `verdicts`, `HARNESS` from
`plans/round50_c1_verify.py` @ `850ec790` — so fixture construction, the Q39 name hiding (per-module random
parent token, 8 decoy siblings), the out-of-process `python -I` harness, the exit-code verdict channel
(10 BREACH / 11 ADMIT / else ERROR) and the argv form are exactly the instrument's, not a re-implementation.
Each fence is scored against a **fresh, independently built** fixture population (so a fence that mutates a
fixture cannot poison a later column), with `hb.ALLOW_NO_REPO = True` as the counter sets it for the hostile
legs. Reason strings are normalized (`<fixture dir>` → `{D}`, scratch root → `{W}`) and whitespace-collapsed
for tabular stability; **verdicts are never normalized**.

Command (cwd = the shared clone, `TMPDIR` = scratch):

    $ cd $S/lane && python3 $S/parity.py --lane . --fences $S/fences --work $S/work --out $S/parity.tsv

## Result — the parity table

`.ufo/waves/round-50/w1/R50C1ExecParity/parity.tsv` — 75 fixture rows × 3 verdict columns
(columns: `set module fid base r49 repair changed base_why r49_why repair_why`). Written into a
seat-scoped subdirectory of the wave dir because `w1/` is shared with 70+ sibling seats and a bare
`parity.tsv` there would be a writer-path collision.

    PARITY refusals46 rows=34 base_breach=34 r49_breach=34 repair_breach=34
    PARITY sealed46   rows=15 base_breach=15 r49_breach=15 repair_breach=15
    PARITY sealed50   rows=26 base_breach=26 r49_breach=26 repair_breach=26
    CHANGED rows=0
    ALL-BREACH all_fences=True rows=75

* `refusals46` — 20 frozen modules → 34 fixtures.
* `sealed50` — the **assembled** blind set as landed (20 modules → 26 fixtures; the assembly grew 18 → 20 in
  `3dda12f`, so this is the post-adoption set the repair is actually scored against, not the wave-1 subset).
* `sealed46` — 12 frozen modules → 15 fixtures. **Supplementary**: my item names only refusals46 + sealed50,
  but the claim's SEALED leg is `12 frozen + N blind`, so the frozen half was measured too rather than
  implied. It costs nothing and closes the leg.

Every `build` in every round returned `build_errors=0`; every cell is a fence decision, not a harness error
(the reason columns carry the fences' own refusal strings, e.g. `BREACH lane/.git/config carries a bare CR`,
`BREACH wt/.git is a .git file that is not a gitdir line`, `BREACH lane/.git/objects/info/alternates names a
store outside the fixture`).

**Rows that changed: none.** 0 of 75 rows changed verdict across the three fences. The r49 candidate is
verdict-identical to the base fence on the entire hostile surface, and the repair preserves every refusal the
base fence made. The repair's honest-side delta is therefore exactly additive: it buys admissions without
surrendering a single hostile decision.

### Secondary observation — 31 rows keep `BREACH` but change *why*

Decision-stable, rationale-changed (`base_vs_repair_reason_diff=31`, `base_vs_r49=11`, `r49_vs_repair=23`).
Full list: `R50C1ExecParity/reason-changes.txt`. Shape of the change:

```text
refusals46  g3-wtmeta-out                  | .../worktrees is not a plain-init entry -> .../worktrees/g3-wt/gitdir points outside the fixture
refusals46  f1-gitdir-outside              | .git is a file (gitdir redirect) -> ../side/gitdir resolves outside the fixture
refusals46  config-core-attributes-file-outside | config line b'attributesFile = …' is not a plain key=val -> config key core.attributesfile is not allowlisted
refusals46  f5-alternates-outside          | alternates present (object-store redirect) -> alternates names a store outside the fixture
refusals46  f7-cd-accept/-anchor/-reject   | commondir is not a plain-init entry -> commondir names a common dir outside the fixture
sealed46    sealed-pack-redirect            | .git/info/refs is not git's exclude file -> pack is a symlink
sealed50    b2-fetch-head-hardlink-out      | FETCH_HEAD is not a plain-init entry -> FETCH_HEAD has more than one hard link
sealed50    b4a-gitfile-newline-two-pointers| wt/.git is a file (gitdir redirect) -> wt/.git is a .git file that is not a gitdir line
sealed50    b4b-gitfile-store-include       | wt/.git is a file -> store/config section [include] is not allowlisted
sealed50    seal6-gitfile-up-inside-link    | sub/repo/.git is a file -> sub/store/objects is a symlink
sealed50    x1-cd-abs, x1-cd-rel            | commondir is not a plain-init entry -> COMMIT_EDITMSG is not a worktree-store entry
sealed50    x2-alt-abs, x2-alt-rel          | wt/.git is a file -> store/objects/info/alternates names a store outside the fixture
```

Two of these are worth the L1's attention as review targets, not defects of this seat:

* `x1-cd-abs` / `x1-cd-rel` (commondir escape) are refused by the repair for `COMMIT_EDITMSG is not a
  worktree-store entry`, i.e. the commondir-*escape* rule is not the operative guard for those two fixtures;
  they are refusal-stable, but the reason shown is not the escape. If the round's narrative says those rows
  are caught by containment, the receipt does not support the *mechanism*, only the verdict.
* `seal6-gitfile-submodule-store-link` is refused by the repair for `main/.git/modules is not a plain-init
  entry` — again a shape rule, not containment of the linked store.

## Axis 2 — sensitivity control (the rig can say ADMIT)

Same rig, same three fences, the five honest classes the base fence is documented to over-refuse
(`R50C1ExecParity/control-honest.txt`):

    n17-replace-ref        BREACH  BREACH  ADMIT
    n18-shallow-fetch      BREACH  BREACH  ADMIT
    n20-linked-worktree    BREACH  BREACH  ADMIT
    n21-separate-gitdir    BREACH  BREACH  ADMIT
    n22-alternates-in-d    BREACH  BREACH  ADMIT

with the base fence's own over-refusal reasons verbatim (`repo/.git/refs/replace is not refs/heads or
refs/tags`, `repo/.git/FETCH_HEAD is not a plain-init entry`, `wt/.git is a file (gitdir redirect), not a
directory` ×2, `lane/.git/objects/info/alternates present (object-store redirect)`) and `ADMIT ADMIT` (empty
reason) under the repair. The all-`BREACH` table above is therefore a property of the fences, not of an inert
harness.

## Axis 3 — reproducibility and population identity

    $ cmp parity.tsv parity2.tsv && cmp parity.tsv parity3.tsv   -> DETERMINISTIC_3RUNS rows=75

Three runs, three independent work roots, byte-identical table (`R50C1ExecParity/parity-run.txt`). Full-fence
run over the frozen honest population, same rig (`R50C1ExecParity/popcmp-honest.txt`):

    POPULATION sha256=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 pin=b5197f94… (equal)
    HONEST base_fence.py   fixtures=126 admitted=113 refused=13 error=0  IDENTITY mismatched=0
    HONEST r49_candidate   fixtures=126 admitted=121 refused=5  error=0  IDENTITY mismatched=0
    HONEST repair_fence.py fixtures=126 admitted=126 refused=0  error=0  IDENTITY mismatched=0
    DIFF base->r49_candidate changed=8    DIFF base->repair changed=13    DIFF r49->repair changed=5

The 8 rows the r49 candidate fixes (`n03,n07,n08,n12,n13,n14,n15,n16`) are the r48 classes; the 5 rows it
still refuses are exactly `n17,n18,n20,n21,n22` — the classes this round's repair is about. That is the
cleanest available characterisation of the `r49` column: on the **hostile** surface it is the base fence, on
the honest surface it is half a repair.

## Axis 4 — reconciliation with the frozen instrument

Same clone, same revision, the counter's own legs (`R50C1ExecParity/counter-crosscheck.txt`):

    REV 85102cf560240ff64943f73d4368b9131f15f7e6
    TREE dirty=0
    FENCE …/plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
    POPULATION fixtures=126 pin=b5197f94… mismatched=0 build_errors=0
    HONEST fixtures=126 admitted=126 refused=0 error=0
    REFUSALS total=20 clean=20 leaked=0 build_errors=0
    SEALED total=12 clean=12 leaked=0 build_errors=0
    SEALED total=20 clean=20 leaked=0 build_errors=0
    PREDICATE R50-C1 pass

My table's 34 refusal fixtures / 41 sealed fixtures, all `BREACH` under `repair`, are exactly the population
the counter's `clean=20` + `clean=12` + `clean=20` module counts are computed over: the two artifacts agree
per fixture and per module. (This is a cross-check of my rig against the frozen instrument on a read-only
clone; it is **not** the round's scored receipt, which is `corpus/evidence/round50/c1-receipt.txt`.)

## Limits (named, not hidden)

* Only **admission decisions** are measured — the same limit the claims name. Outside-`d` reads made *while
  deciding* remain `plans/round46_c1_verify.py`'s property and are not re-scored here.
* Reason strings are auxiliary evidence, not part of the parity criterion: the fences truncate them (~40
  bytes of a config line), so two of them embed the scratch root; they are normalized here (`{D}`, `{W}`) and
  would not be stable across differently-rooted hosts. Verdicts are exit codes and are not affected.
* The `r49` column is the r49 **candidate** (`b687b1d9…`), which never landed; it is the fence the *carried*
  23-row r49 mutant battery was authored against (the landed `plans/mutants50/c1-mutants.json` is the
  re-derived 15-row battery against the repair, `target: plans/fixture_fence.py (round-50 repair)`). Nothing
  here says the r49 candidate was wrong — only that its verdict vector is the base fence's on this surface.
* Host-sensitive where git output is: git 2.56.0, Python 3.14.8, `LC_ALL=C.UTF-8`, `PYTHONHASHSEED=0`; the
  fixtures were rebuilt here (identity vs the pinned population re-checked, `mismatched=0`) but a different
  git would build different bytes.
* `sealed50` is scored as landed (20 modules). The wave-1 assembly saw 18; the two late modules were adopted
  in `3dda12f` before the scored run, so the landed set is the one that matters.
* No mutant leg was run (my item is parity, and the mutant battery is `R50C1ExecMutRebase`'s).
* I did not evaluate whether the repair's rationale on `x1-cd-*` / `seal6-gitfile-submodule-store-link` is the
  *intended* guard — flagged above for the L1; it is a review question, not a parity failure.

## Artifacts (this seat dir = `.ufo/waves/round-50/w1/R50C1ExecParity/`)

| file | what |
|---|---|
| `parity.tsv` | the deliverable: 75 rows, 3 verdict columns + per-fence reason |
| `parity.py` | driver (imports the frozen counter's `build_all`/`verdicts`/`HARNESS`) |
| `control.py`, `control-honest.txt` | sensitivity control (base BREACH → repair ADMIT on the 5 honest classes) |
| `popcmp.py`, `popcmp-honest.txt` | 126-fixture honest rollup per fence + verdict diffs |
| `counter-crosscheck.txt` | the frozen counter's legs at the same REV |
| `parity-run.txt` | three-run determinism receipt |
| `reason-changes.txt` | the 31 verdict-stable, rationale-changed rows |
| `base_fence.py`, `r49_candidate.py`, `repair_fence.py`, `SHA256SUMS.txt` | the three fences and all digests |

Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1ExecParity` (762 MB, one `git clone --shared`, all fixture
builds) was removed after these artifacts were copied here; `TMPDIR` was confined to it throughout.

## VERDICT

**PASS (scoped).** 75/75 fixtures of the two frozen hostile sets — 20 `refusals46` modules (34 fixtures),
the assembled `sealed50` set (20 modules, 26 fixtures) and, supplementary, the 12 `sealed46` modules (15
fixtures) — are `BREACH` under the base fence `05d5fe03…`, the r49 candidate `b687b1d9…` and the landed repair
`57adce4a…` at `REV 85102cf5…`. **No row changed its verdict**; 31 rows changed only their refusal rationale.
The rig is proven able to emit `ADMIT` (5/5 honest classes flip under the repair), the table is byte-identical
across three independent runs, the honest population is the pinned 126 with `mismatched=0`, and the per-fixture
rows reconcile exactly with the counter's `REFUSALS clean=20`, `SEALED clean=12/20`, `HONEST 126/126`.
