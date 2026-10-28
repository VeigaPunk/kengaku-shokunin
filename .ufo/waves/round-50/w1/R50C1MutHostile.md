# R50C1MutHostile — six hostile pointer variants for the C1 seal (round 50, wave 1)

Seat `R50C1MutHostile`, mutation-tester, leaf (no subagent dispatch). Serving **R50-C1** (novelty). Item: take the
20 modules of `plans/refusals46/` and build **six fresh hostile variants that a pointer-resolving repair might
admit**; measure the **base fence** and the **r49 candidate**; hand them to the L1 as candidate `plans/sealed50/`
rows with expected refusal. This report never claims R50-C1/R50-C2 admission and writes to no production file.

## 1. Axes named

| axis | values this seat varied |
|---|---|
| A1 pointer kind | gitfile (`gitdir:`), `commondir`, `objects/info/alternates`, `[include]` chain, `refs/replace/<40hex>`, `FETCH_HEAD` |
| A2 resolution shortcut the row targets | (a) resolve the pointer and validate the target but never prove the target is inside `d`; (b) validate only the **first** alternates entry; (c) follow **one** include hop; (d) read the ref **through a link**; (e) admit a newly-whitelisted name **without the multi-link rule** |
| A3 fence under test | base `05d5fe03`; r49 candidate `b687b1d9`; the wave-1 sibling repair `9baedf13`; the **landed** fence `57adce4a`; three scratch probe repairs P1/P2/P3 |
| A4 pairing | five of the six rows are the **minimal evil twin** of an honest class the C1 repair must admit: `n21` gitfile, `n22` alternates, `n20` commondir, `n17` replace ref, `n18` FETCH_HEAD; `h4` (include) is the sixth, whose honest twin does not exist (includes stay refused) |

Godspeed loop used: cheap parallel iteration over fences (one build per fixture, six verdict columns), keep a row
only if it improves an axis (discrimination against a plausible repair, no harm to the frozen legs), and let the
frontier walk (P1 → P2 → P3 isolation) rather than aiming at a preconceived repair design.

## 2. Revisions and preconditions (REV)

* clone: `git clone --shared --no-checkout <lane> lane && git checkout -q 3b02d573…`; `git -C lane rev-parse HEAD`
  → `3b02d573d58cc6d2e0d27ef92ac0815354912252`.
* `git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 <tip>` → **yes**, checked twice: at read
  start against `c3372a9` (before any measurement) and at read end against `d45c5bb` (the lane moved during the
  wave).
* clone `plans/fixture_fence.py` sha256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e` (the frozen base fence).
* counter used for scoring: `plans/round50_c1_verify.py` sha256
  `d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2` (the c3372a9 open-window repair; also the
  digest of the counter committed at `d45c5bb`).
* population pin `b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69`, 126 fixtures.
* **live lane at read end**: HEAD `d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78`; `plans/fixture_fence.py` =
  `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1` (committed at that tip — the landed repair);
  `plans/round50_c1_verify.py` shows as modified in the worktree and was **not** measured. All numbers below are
  freeze-revision numbers (clone at `3b02d57`) except where a row says `LANDED`.

## 3. Commands run (exact)

```
mkdir -p /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile && export TMPDIR=/fast/scratch/hyaku/kengaku-r50/R50C1MutHostile
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin lane && cd lane \
  && git checkout -q 3b02d573d58cc6d2e0d27ef92ac0815354912252
# control (frozen counter, base fence), and each fence under test
python3 plans/round50_c1_verify.py --lane . --skip-mutants --work <scratch>/work/final-<case> [--fence <f>] --allow-dirty
# per-row build + verdicts + git realism for every fixture (probe.py, §14)
python3 probe.py --lane lane --work work/probe --verify
# landed fence and landed counter extracted read-only from the live lane
git -C <lane> show d45c5bb:plans/fixture_fence.py > landed.py
git -C <lane> show d45c5bb:plans/round50_c1_verify.py > landed_counter.py
# the landed blind set (18 modules) copied from d6f2fce into the clone's plans/sealed50 for the overlap measurement
git -C <lane> ls-tree -r --name-only d6f2fce plans/sealed50/
```

## 4. Control: the frozen counter on the base fence reproduces the frozen figure

`python3 plans/round50_c1_verify.py --lane . --skip-mutants` on the clean clone at `3b02d57`, **before** any
`plans/sealed50/` exists:

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n14-stash-entry ../../../work/k50-c1-rrx1b706/honest/m026-plans-honest50-modules-novel48-n14_stash_entry/f000/repo/.git/logs/refs/stash has a name git does not write
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph present (object-store redirect)
HONEST-REFUSED n16-notes-ref ../../../work/k50-c1-rrx1b706/honest/m028-plans-honest50-modules-novel48-n16_notes_ref/f000/repo/.git/logs/refs/notes has a name git does not write
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

Exit 1. `HONEST fixtures=126 admitted=113 refused=13` is the claims' declared *before* value, so the instrument
and the population reproduce. The counter prints at most 12 refused rows (`for x in refused[:12]`); the 12 shown
are `n03`, `n07`, `n12`–`n18`, `n20`–`n22`, i.e. all but one of the 13. The five pointer classes this seat's rows
pair with are `n17`, `n18`, `n20`, `n21`, `n22`, whose base reasons are quoted in §6.

## 5. The six rows, scored through the frozen counter as `plans/sealed50/`

Each module was placed in the clone's `plans/sealed50/` (untracked, scratch) and the counter re-run with
`--allow-dirty`: `TREE dirty=1` in the blocks below is **exactly that untracked directory** — the graded run is a
clean clone, and the counter's `--allow-dirty` is its own testing switch, used here only because the row set is the
scratch input under measurement. No tracked byte differs (`FENCE … sha256=05d5fe03…` in every block). Base fence:

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n14-stash-entry ../../../../work/final-base/k50-c1-u0rde5e0/honest/m026-plans-honest50-modules-novel48-n14_stash_entry/f000/repo/.git/logs/refs/stash has a name git does not write
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph present (object-store redirect)
HONEST-REFUSED n16-notes-ref ../../../../work/final-base/k50-c1-u0rde5e0/honest/m028-plans-honest50-modules-novel48-n16_notes_ref/f000/repo/.git/logs/refs/notes has a name git does not write
HONEST-REFUSED n17-replace-ref repo/.git/refs/replace is not refs/heads or refs/tags
HONEST-REFUSED n18-shallow-fetch repo/.git/FETCH_HEAD is not a plain-init entry
HONEST-REFUSED n20-linked-worktree wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n21-separate-gitdir wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n22-alternates-in-d lane/.git/objects/info/alternates present (object-store redirect)
HONEST-REFUSED n03-detached-head repo/.git/HEAD is not a plain branch HEAD
HONEST-REFUSED n07-reflog-gc repo/.git/info/refs is not git's exclude file
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=6 clean=6 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

r49 candidate `b687b1d9` (`--fence cand_r49.py`):

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/cand_r49.py sha256=b687b1d9dd78282f09fc10847c453fb74157f116ea56a0d498ef9cd91ec0ca52
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=121 refused=5 error=0
HONEST-REFUSED n17-replace-ref repo/.git/refs/replace is not a ref namespace git writes
HONEST-REFUSED n18-shallow-fetch repo/.git/FETCH_HEAD is not a plain-init entry
HONEST-REFUSED n20-linked-worktree wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n21-separate-gitdir wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n22-alternates-in-d ../../../../../work/final-cand/k50-c1-k67rai2d/honest/m034-plans-honest50-modules-novel50-n22_alternates_in_d/f000/lane/.git/objects/info/alternates is not a plain object-info entry (object-store redi
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=6 clean=6 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

the wave-1 sibling repair `9baedf13` (`--fence exec_repair.py`):

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/exec_repair.py sha256=9baedf1379b6de5cecce629a3fceaeb8d2b99371d34b64d0ecd397d15a3c4ec1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=117 refused=9 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n14-stash-entry ../../../../work/final-exec/k50-c1-e3qf4obp/honest/m026-plans-honest50-modules-novel48-n14_stash_entry/f000/repo/.git/logs/refs/stash has a name git does not write
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph is not git's alternates file
HONEST-REFUSED n16-notes-ref ../../../../work/final-exec/k50-c1-e3qf4obp/honest/m028-plans-honest50-modules-novel48-n16_notes_ref/f000/repo/.git/logs/refs/notes has a name git does not write
HONEST-REFUSED n18-shallow-fetch repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n03-detached-head repo/.git/HEAD is not a plain branch HEAD
HONEST-REFUSED n07-reflog-gc repo/.git/info/refs is not git's exclude file
HONEST-REFUSED n08-tag-detached repo/.git/HEAD is not a plain branch HEAD
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=6 clean=6 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

the **landed** fence `57adce4a` (`--fence landed.py`):

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/landed.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=6 clean=6 leaked=0 build_errors=0
PREDICATE R50-C1 pass
```

Reading: on every fence the sealed50 leg is `clean=6 leaked=0 build_errors=0` — each of the six modules builds and
is refused. The r49 candidate leaves the honest population at 121/126 (it refuses exactly the five pointer
classes); the landed fence admits 126/126. **The six rows cost the landed repair nothing and close no honest
class.** With the landed blind set of 18 modules plus these six (24) the landed fence prints `SEALED total=24
clean=24` and `PREDICATE R50-C1 pass` (§9).

## 6. Per-row refusal reason, per fence (verbatim from the probe run)

```
WHY h1-gitfile-to-outside BASE REFUSE lane/.git is a file (gitdir redirect), not a directory
WHY h1-gitfile-to-outside R49CAND REFUSE lane/.git is a file (gitdir redirect), not a directory
WHY h1-gitfile-to-outside EXECREPAIR REFUSE lane/.git names '/fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/work/probe/h-h1_gitfile_to_outside/outside/store/.git', which resolves outside the fi
WHY h1-gitfile-to-outside LANDED REFUSE ../outside/store/.git resolves outside the fixture
WHY h1-gitfile-to-outside P2-locality-correct REFUSE lane/.git gitfile resolves outside the fixture
WHY h1-gitfile-to-outside P3-links-only REFUSE lane/.git gitfile resolves outside the fixture
WHY h2-alternates-relative-climb BASE REFUSE lane/.git/objects/info/alternates present (object-store redirect)
WHY h2-alternates-relative-climb R49CAND REFUSE ../../../../work/probe/h-h2_alternates_climb/f000/lane/.git/objects/info/alternates is not a plain object-info entry (object-store redirect)
WHY h2-alternates-relative-climb EXECREPAIR REFUSE lane/.git/objects/info/alternates names '../../../../outside/other/.git/objects', which resolves outside the fixture
WHY h2-alternates-relative-climb LANDED REFUSE lane/.git/objects/info/alternates names a store outside the fixture
WHY h2-alternates-relative-climb P3-links-only REFUSE ../../../../work/probe/h-h2_alternates_climb/f000/lane/.git/objects/info/alternates names '../../../../outside/other/.git/objects' outside the fixture
WHY h3-commondir-outside BASE REFUSE lane/.git/commondir is not a plain-init entry
WHY h3-commondir-outside R49CAND REFUSE lane/.git/commondir is not a plain-init entry
WHY h3-commondir-outside EXECREPAIR REFUSE lane/.git/commondir is not a plain-init entry
WHY h3-commondir-outside LANDED REFUSE lane/.git/commondir names a common dir outside the fixture
WHY h3-commondir-outside P2-locality-correct REFUSE lane/.git/commondir resolves outside the fixture
WHY h3-commondir-outside P3-links-only REFUSE lane/.git/commondir resolves outside the fixture
WHY h4-include-chain-outside BASE REFUSE lane/.git/config section [include] is not allowlisted
WHY h4-include-chain-outside R49CAND REFUSE lane/.git/config section [include] is not allowlisted
WHY h4-include-chain-outside EXECREPAIR REFUSE lane/.git/config section [include] is not allowlisted
WHY h4-include-chain-outside LANDED REFUSE lane/.git/config section [include] is not allowlisted
WHY h4-include-chain-outside P3-links-only REFUSE lane/.git/config section [include] is not allowlisted
WHY h5-replace-ref-outside BASE REFUSE lane/.git/refs/replace is not refs/heads or refs/tags
WHY h5-replace-ref-outside R49CAND REFUSE lane/.git/refs/replace is not a ref namespace git writes
WHY h5-replace-ref-outside EXECREPAIR REFUSE ../../../work/probe/h-h5_replace_ref_outside/f000/lane/.git/refs/replace/e6194a5fc75a12d9135ae7b7ec2c24ac92e1edf3 is a symlink
WHY h5-replace-ref-outside LANDED REFUSE ../../../work/probe/h-h5_replace_ref_outside/f000/lane/.git/refs/replace/e6194a5fc75a12d9135ae7b7ec2c24ac92e1edf3 is a symlink
WHY h6-fetch-head-hardlink BASE REFUSE lane/.git/FETCH_HEAD is not a plain-init entry
WHY h6-fetch-head-hardlink R49CAND REFUSE lane/.git/FETCH_HEAD is not a plain-init entry
WHY h6-fetch-head-hardlink EXECREPAIR REFUSE lane/.git/FETCH_HEAD has more than one hard link
WHY h6-fetch-head-hardlink LANDED REFUSE lane/.git/FETCH_HEAD has more than one hard link
```

Every row has an attributable rule on the base fence, on the r49 candidate and on the landed fence; none is
refused by accident (e.g. not by "unreadable", "build error" or a missing repo).

## 7. The escapes are live: git itself resolves outside `d`

The rows are not decorative shapes — each one leaves a state in which git resolves the escape. Verified with
`git -C <fixture>/lane …` under the builder's own env (`HOME=/nonexistent`, `GIT_CONFIG_NOSYSTEM=1`,
`GIT_CONFIG_GLOBAL=/dev/null`); `<GEN>` is the fixture generator dir, `d = <GEN>/f000`:

```
VERIFY h1-gitfile-to-outside rc=0 argv=git -C lane rev-parse --absolute-git-dir out='<GEN>/outside/store/.git'
VERIFY h2-alternates-relative-climb rc=0 argv=git -C lane rev-parse --git-path objects/info/alternates out='.git/objects/info/alternates'
VERIFY h2-alternates-relative-climb lstat nlink=1 size=146
VERIFY h3-commondir-outside rc=0 argv=git -C lane rev-parse --git-common-dir out='<GEN>/outside/common/.git'
VERIFY h4-include-chain-outside rc=0 argv=git -C lane config --includes --get core.worktree out='../../../outside/wt'
VERIFY h5-replace-ref-outside rc=0 argv=git -C lane replace -l out='e6194a5fc75a12d9135ae7b7ec2c24ac92e1edf3'
VERIFY h6-fetch-head-hardlink rc=0 argv=git -C lane rev-parse HEAD out='4d88795d2b61cd3050f970240b8628e8b6313c90'
VERIFY h6-fetch-head-hardlink lstat nlink=2 size=68
```

* **h1** `rev-parse --absolute-git-dir` answers `<GEN>/outside/store/.git`, and `git log --oneline` lists the
  outside store's two commits — the work tree is judged against a store outside `d`.
* **h2** `git cat-file -t <oid>` → `commit` (rc 0) for an object that exists **only** in the outside store, i.e.
  the second, relative-climbing alternates entry is read. (`rev-parse --git-path` line above is the shape check.)
* **h3** `rev-parse --git-common-dir` answers `<GEN>/outside/common/.git` and `git log` shows that store's
  commits, while `--show-toplevel` still answers inside `d`.
* **h4** `config --includes --get core.worktree` prints `../../../outside/wt`: the second hop was parsed.
* **h5** `git replace -l` lists the replaced id read **through the outside symlink**, and `rev-list --count HEAD`
  = 1 for a two-commit history — the replacement was applied.
* **h6** `lstat` shows `nlink=2` and the same inode as `<GEN>/outside/fetch_head`.

## 8. Discrimination: which plausible repair admits which row

Three scratch probes (`naive_p1.py`, `naive_p2.py`, and `naive.py` with switches) were built from the r49
candidate by `make_naive.py` (§15): they **add the five pointer legs** the C1 repair must add and **repair every
honest class of the frozen population** (126/126 below), each with one plausible shortcut per leg:

| probe | store pointers | alternates | include | replace ref | FETCH_HEAD |
|---|---|---|---|---|---|
| P1 | resolved, **target locality not proved** | all entries, no locality | one hop | read through link | no multi-link rule |
| P2 | resolved, **locality proved** | **first entry only** | one hop | read through link | no multi-link rule |
| P3 | resolved, locality proved | all entries | still refused | read through link | no multi-link rule |

Frozen counter, P1 (`--fence naive_p1.py`):

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/naive_p1.py sha256=0b07d57d00d97171550ff1e289880589f2c3d5e6911ccab02ffa9ebfc3f8b960
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=16 leaked=6 build_errors=0
REFUSALS-MISS f18_wtmeta_out.py g3-wtmeta-out ADMIT 
REFUSALS-MISS f1_gitfile.py f1-gitdir-outside ADMIT 
REFUSALS-MISS f5_alternates.py f5-alternates-outside ADMIT 
REFUSALS-MISS f7_commondir.py f7-cd-accept ADMIT 
REFUSALS-MISS f7_commondir.py f7-cd-reject ADMIT 
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=6 clean=0 leaked=6 build_errors=0
SEALED-MISS h1_gitfile_to_outside.py h1-gitfile-to-outside ADMIT 
SEALED-MISS h2_alternates_climb.py h2-alternates-relative-climb ADMIT 
SEALED-MISS h3_commondir_outside.py h3-commondir-outside ADMIT 
SEALED-MISS h4_include_chain_outside.py h4-include-chain-outside ADMIT 
SEALED-MISS h5_replace_ref_outside.py h5-replace-ref-outside ADMIT 
SEALED-MISS h6_fetch_head_hardlink.py h6-fetch-head-hardlink ADMIT 
PREDICATE R50-C1 fail
```

P2:

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/naive_p2.py sha256=21bdea36b5e0fd6f5fe9adca71469af08d7fa2c41ce8e492f60ed287358f273f
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=6 clean=2 leaked=4 build_errors=0
SEALED-MISS h2_alternates_climb.py h2-alternates-relative-climb ADMIT 
SEALED-MISS h4_include_chain_outside.py h4-include-chain-outside ADMIT 
SEALED-MISS h5_replace_ref_outside.py h5-replace-ref-outside ADMIT 
SEALED-MISS h6_fetch_head_hardlink.py h6-fetch-head-hardlink ADMIT 
PREDICATE R50-C1 fail
```

P2 with the six rows **removed** (no `plans/sealed50/` at all):

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/naive_p2.py sha256=21bdea36b5e0fd6f5fe9adca71469af08d7fa2c41ce8e492f60ed287358f273f
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 pass
```

The last block is the point of the seat: **a fence that prints `PREDICATE R50-C1 pass` with HONEST 126/126,
REFUSALS 20/20 and SEALED 12/12 still admits four of the six rows** (h2, h4, h5, h6). P1 — the coarser repair that
skips target locality — is caught by the *frozen* refusals (`f1`, `f5`, `f7`×2, `f18`), which is why P1 is the
control and P2 is the discriminating probe. Per-row verdict matrix (from `probe.py`, §14):

```
ROW h1-gitfile-to-outside            BASE=REFUSE  R49CAND=REFUSE  EXECREPAIR=REFUSE  LANDED=REFUSE  P1-all=ADMIT  P2-locality-correct=REFUSE  P3-links-only=REFUSE
ROW h2-alternates-relative-climb     BASE=REFUSE  R49CAND=REFUSE  EXECREPAIR=REFUSE  LANDED=REFUSE  P1-all=ADMIT  P2-locality-correct=ADMIT  P3-links-only=REFUSE
ROW h3-commondir-outside             BASE=REFUSE  R49CAND=REFUSE  EXECREPAIR=REFUSE  LANDED=REFUSE  P1-all=ADMIT  P2-locality-correct=REFUSE  P3-links-only=REFUSE
ROW h4-include-chain-outside         BASE=REFUSE  R49CAND=REFUSE  EXECREPAIR=REFUSE  LANDED=REFUSE  P1-all=ADMIT  P2-locality-correct=ADMIT  P3-links-only=REFUSE
ROW h5-replace-ref-outside           BASE=REFUSE  R49CAND=REFUSE  EXECREPAIR=REFUSE  LANDED=REFUSE  P1-all=ADMIT  P2-locality-correct=ADMIT  P3-links-only=ADMIT
ROW h6-fetch-head-hardlink           BASE=REFUSE  R49CAND=REFUSE  EXECREPAIR=REFUSE  LANDED=REFUSE  P1-all=ADMIT  P2-locality-correct=ADMIT  P3-links-only=ADMIT
ROW n17-replace-ref                  BASE=REFUSE  R49CAND=REFUSE  EXECREPAIR=ADMIT  LANDED=ADMIT  P1-all=ADMIT  P2-locality-correct=ADMIT  P3-links-only=ADMIT
ROW n18-shallow-fetch                BASE=REFUSE  R49CAND=REFUSE  EXECREPAIR=REFUSE  LANDED=ADMIT  P1-all=ADMIT  P2-locality-correct=ADMIT  P3-links-only=ADMIT
ROW n20-linked-worktree              BASE=REFUSE  R49CAND=REFUSE  EXECREPAIR=ADMIT  LANDED=ADMIT  P1-all=ADMIT  P2-locality-correct=ADMIT  P3-links-only=ADMIT
ROW n21-separate-gitdir              BASE=REFUSE  R49CAND=REFUSE  EXECREPAIR=ADMIT  LANDED=ADMIT  P1-all=ADMIT  P2-locality-correct=ADMIT  P3-links-only=ADMIT
ROW n22-alternates-in-d              BASE=REFUSE  R49CAND=REFUSE  EXECREPAIR=ADMIT  LANDED=ADMIT  P1-all=ADMIT  P2-locality-correct=ADMIT  P3-links-only=ADMIT
```

```
ADMITTED BASE hostile=0/6 
ADMITTED R49CAND hostile=0/6 
ADMITTED EXECREPAIR hostile=0/6 
ADMITTED LANDED hostile=0/6 
ADMITTED P1-all hostile=6/6 h1-gitfile-to-outside h2-alternates-relative-climb h3-commondir-outside h4-include-chain-outside h5-replace-ref-outside h6-fetch-head-hardlink
ADMITTED P2-locality-correct hostile=4/6 h2-alternates-relative-climb h4-include-chain-outside h5-replace-ref-outside h6-fetch-head-hardlink
ADMITTED P3-links-only hostile=2/6 h5-replace-ref-outside h6-fetch-head-hardlink
TWINS BASE admitted=0/5 
TWINS R49CAND admitted=0/5 
TWINS EXECREPAIR admitted=4/5 n17-replace-ref n20-linked-worktree n21-separate-gitdir n22-alternates-in-d
TWINS LANDED admitted=5/5 n17-replace-ref n18-shallow-fetch n20-linked-worktree n21-separate-gitdir n22-alternates-in-d
TWINS P1-all admitted=5/5 n17-replace-ref n18-shallow-fetch n20-linked-worktree n21-separate-gitdir n22-alternates-in-d
TWINS P2-locality-correct admitted=5/5 n17-replace-ref n18-shallow-fetch n20-linked-worktree n21-separate-gitdir n22-alternates-in-d
TWINS P3-links-only admitted=5/5 n17-replace-ref n18-shallow-fetch n20-linked-worktree n21-separate-gitdir n22-alternates-in-d
```

## 9. Against the landed blind set (18 rows) and the landed fence

The lane's committed blind set at `d6f2fce` has **18** modules. Copied into the clone unchanged:

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/naive_p2.py sha256=21bdea36b5e0fd6f5fe9adca71469af08d7fa2c41ce8e492f60ed287358f273f
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=17 leaked=1 build_errors=0
SEALED-MISS b2_fetch_head_hardlink_out.py b2-fetch-head-hardlink-out ADMIT 
PREDICATE R50-C1 fail
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/landed.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
PREDICATE R50-C1 pass
```

So of the landed 18, a locality-correct pointer repair leaks exactly **one** (`b2_fetch_head_hardlink_out`), and
the landed fence kills all 18. With the six rows added (24):

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/naive_p2.py sha256=21bdea36b5e0fd6f5fe9adca71469af08d7fa2c41ce8e492f60ed287358f273f
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=24 clean=19 leaked=5 build_errors=0
SEALED-MISS b2_fetch_head_hardlink_out.py b2-fetch-head-hardlink-out ADMIT 
SEALED-MISS h2_alternates_climb.py h2-alternates-relative-climb ADMIT 
SEALED-MISS h4_include_chain_outside.py h4-include-chain-outside ADMIT 
SEALED-MISS h5_replace_ref_outside.py h5-replace-ref-outside ADMIT 
SEALED-MISS h6_fetch_head_hardlink.py h6-fetch-head-hardlink ADMIT 
PREDICATE R50-C1 fail
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1MutHostile/landed.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=24 clean=24 leaked=0 build_errors=0
PREDICATE R50-C1 pass
```

**Net new discrimination among the landed 18 + 6**: `h2` (multi-entry alternates), `h4` (two-hop include),
`h5` (replace ref read through a link) are classes no landed row discriminates; `h6` duplicates `b2`; `h1`
duplicates `s50_gitfile_symlink_chain` / `s6_gitfile_rel_objects_link` / `s6_second_store_mount` (same class: a
gitfile whose store is outside `d`); `h3` (relative, top-level `commondir` outside) is not in the blind set but is
covered by `refusals46/f7` (absolute) and `f19` (hidden below a pruned `.git`) — additive to the blind set, not to
the refusal set.

## 10. Findings handed to the L1 (integration owner)

**F1 — instrument shape (must be read before touching the receipt).** With `plans/sealed50/` present the counter
prints **two** lines with the `SEALED` label, one per directory (`SEALED_RELS = ("plans/sealed46",
"plans/sealed50")`, one `leg()` call per directory at `round50_c1_verify.py:220-235`, digest `d8787b34`). The
frozen predicate sentence in `plans/round-50-claims.md` §C1 has a single `SEALED total=<S> clean=<S> leaked=0`
line with `<S> ≥ 18`. The committed S3 receipt (`corpus/evidence/round50/c1-receipt.txt` at `d45c5bb`) already
carries both lines (`total=12` then `total=18`). The receipt is decidable only against the second line; the
counter has no single-line mode. I did not touch the counter (not my item, and a change after the first scored run
is not this claim's instrument).

**F2 — the blind set's coverage of the pointer shortcuts is one row deep.** Measured: a repair that admits all 126
honest fixtures, keeps `REFUSALS 20/20` and `SEALED(sealed46) 12/12`, and additionally satisfies 17 of the landed
18 blind rows (P2) is still breached on the alternates multi-entry, two-hop include and replace-through-link
shapes. Only `b2_fetch_head_hardlink_out` discriminates that family in the landed set. `h2`, `h4`, `h5` are the
cheapest close (three modules, no honest cost — measured 24/24 clean on the landed fence, `PREDICATE pass`).

**F3 — adding the six changes the printed number.** The sealed50 leg moves 18 → 24; the predicate's `<S>` is a
value ≥ 18 and the run still passes, so the freeze is not harmed, but a receipt that must match exactly needs a
re-run and a new `corpus/evidence/round50/c1-receipt.txt` (the L1's commit, not mine).

**F4 — redundancy disclosed.** `h1` and `h6` are redundant with landed rows (§9) and should be dropped if the
sealed set is meant to be minimal; `h3` is redundant with the refusal set. The three net-new rows are `h2`, `h4`,
`h5`.

**F5 — expected refusal is measured, not assumed.** All six are refused by the landed fence `57adce4a` with
attributable reasons (§6), so they can be frozen as `SEALED50` rows with `expect` = the fence verdict (refusal),
not a guess.

## 11. Limits

* Measured on the **freeze revision** `3b02d57` in a `git clone --shared`; the live lane moved to `d45c5bb` during
  the wave and its `plans/round50_c1_verify.py` was dirty at read end. The landed *fence* (`57adce4a`) and the
  landed *blind set* (`d6f2fce`) were measured as extracted blobs, with the frozen counter.
* Only the **admission/refusal verdict** is measured, the counter's contract. The "escape is live" evidence is
  git's own resolution (§7); I did not strace a fence process, so the outside-*read* property of the probes is
  inferred from git, not traced.
* `P1`/`P2`/`P3` are scratch reconstructions of a plausible repair, not any seat's landed candidate; their numbers
  are evidence about the *rows*, never a claim about the landed fence.
* The **mutant leg** was skipped for the probes (`--skip-mutants`): the carried mutant rows are diffs against the
  r49 candidate and do not apply to the probes' source. `P2`'s `PREDICATE pass` receipt is therefore a
  HONEST/REFUSALS/SEALED statement only.
* Sealed rows are **verdict-only** and carry no `tree_sha256` identity pin; `h1`, the first alternates entry of
  `h2`, and `h5`'s link target embed the fixture generator's absolute path, which changes per build. The counter
  never pins a sealed row, so nothing it reads depends on that; do not add identity pins to these rows.
* Determinism of the six modules across repeated builds was not measured (not needed by the SEALED leg).
* Host paths outside the scratch root, io_uring and mount semantics are not observed.

## 12. Mutation-tester protocol record

| mutant | expected detector | output | verdict |
|---|---|---|---|
| `h1` gitfile target outside (twin `n21`) | SEALED leg: `breach() is not None` | base/`b687b1d9`/`9baedf13`/`57adce4a` REFUSE; P2 REFUSE; P1 ADMIT | killed on all four real fences |
| `h2` second alternates entry climbs out (twin `n22`) | same | all four real fences REFUSE; P2 **ADMIT** | killed on real fences, survives the shortcut |
| `h3` relative top-level `commondir` outside (twin `n20`) | same | all four real fences REFUSE; P1 ADMIT, P2 REFUSE | killed on real fences |
| `h4` two-hop `[include]` (no honest twin) | same | all four real fences REFUSE; P2 **ADMIT** | killed on real fences, survives the shortcut |
| `h5` `refs/replace/<40hex>` through an outside link (twin `n17`) | same | all four real fences REFUSE; P2/P3 **ADMIT** | killed on real fences, survives the shortcut |
| `h6` hardlinked `FETCH_HEAD` (twin `n18`) | same | all four real fences REFUSE; P2/P3 **ADMIT** | killed on real fences (duplicate of landed `b2`) |

Restoration evidence: every mutant lives **only** in this seat's scratch and in this report's §13; no lane file
was written, no clone-tracked byte changed (`plans/fixture_fence.py` in the clone stayed `05d5fe03` through every
run, printed by the counter each time), the clone's `plans/sealed50/` was untracked scratch, and the scratch tree
`/fast/scratch/hyaku/kengaku-r50/R50C1MutHostile` was removed after this report was written. The lane's HEAD and
fence digest are recorded in §2 for the L1 to compare against its own integration state.

## 13. Deliverable — the six modules (verbatim, sha256 of each)

```
2849de9eb11dbb4b098b8482faf102df30d97756176b978c9ad2471a4e850b81  h1_gitfile_to_outside.py
43a3e13a3ee32880769f13fba54abdd20e6ce69623087d70f5e84d70ef0ff543  h2_alternates_climb.py
5a7dd1949fb33832aa7b9ac5156efa5df7cababbfb9945f9ff5992a420f8cfd2  h3_commondir_outside.py
02032aba11f50b37f0cd395f6a1a3a10b292ef1bd8fa9bd5306d449a8b9b1260  h4_include_chain_outside.py
3d69eea9285be9617f64669f06abe6a54c7fa4c8cc32d6bb28898553e020bfe6  h5_replace_ref_outside.py
8fc69f67525e3f55fc9a7191f3e8f0706bd2e9d852ad95d6ad0ad2c8489d17b9  h6_fetch_head_hardlink.py
```

### 13.1 `h1_gitfile_to_outside.py` — sha256 `2849de9eb11dbb4b098b8482faf102df30d97756176b978c9ad2471a4e850b81`

```python
"""Round-50 sealed candidate `h1-gitfile-to-outside` (R50C1MutHostile): the honest class `n21_separate_gitdir`
(a `.git` FILE naming an IN-`d` store, which the C1 repair must admit) with the one byte that decides the
property flipped — the gitfile names a store OUTSIDE `d`.

Evil twin of `plans/honest50/modules/novel50/n21_separate_gitdir.py`: same worktree/`.git`-file/plain-store
layout, same `[core]` config, same argv shape. The store is a plain `git init` + two commits, so every
entry-level rule the repair applies to the honest twin passes here too; the only difference is that the resolved
gitdir is `../outside/store/.git`, i.e. outside `d`. A repair that follows gitfiles and classifies the resolved
store but never proves the resolved path lies inside `d` admits this fixture and then reads the outside store's
config, refs and objects.

Base fence: refuses at the tree walk (`lane/.git is a file (gitdir redirect), not a directory`).
Round-49 candidate (`b687b1d9…`): refuses with the same reason, because it adds no gitfile leg at all.

Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    out = ctx.init(pathlib.Path(d).parent / "outside" / "store")
    ctx.write(out / CLAIMS, "nothing ran\n")
    ctx.git(out, "add", "-A")
    ctx.git(out, "commit", "-qm", "claims")
    ctx.write(out / RECEIPT, "receipt\n")
    ctx.git(out, "add", "-A")
    ctx.git(out, "commit", "-qm", "receipt")
    lane = pathlib.Path(d) / "lane"
    lane.mkdir(parents=True)
    ctx.write(lane / ".git", "gitdir: " + str(out / ".git") + "\n")
    ctx.write(lane / CLAIMS, "nothing ran\n")
    ctx.write(lane / RECEIPT, "receipt\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "h1-gitfile-to-outside", "tool": "order", "expect": "accept", "defects": [], "build": build}]
```

### 13.2 `h2_alternates_climb.py` — sha256 `43a3e13a3ee32880769f13fba54abdd20e6ce69623087d70f5e84d70ef0ff543`

```python
"""Round-50 sealed candidate `h2-alternates-relative-climb` (R50C1MutHostile): the honest class
`n22_alternates_in_d` (an `objects/info/alternates` entry naming an IN-`d` store, which the C1 repair must
admit) with the escape appended as a SECOND line that climbs out of `d` relatively.

Evil twin of `plans/honest50/modules/novel50/n22_alternates_in_d.py`. Two alternates lines:

  1. `<d>/storein/.git/objects`            — absolute, inside `d`, a plain store (the honest shape);
  2. `../../../../outside/other/.git/objects` — relative, resolved by git against the *objects directory*
     `<d>/lane/.git/objects`, i.e. four levels up to the fixture root, then into `outside/` — OUTSIDE `d`.

A repair that validates only the first entry, or that treats the presence of one in-`d` entry as proof of
locality, admits this fixture; git then reads objects, and any ref/object reachable through them, from the
outside store. Measured with git (report §4): `git -C lane cat-file -t <oid>` resolves an object that exists
only in the outside store.

Base fence: refuses (`objects/info/alternates present (object-store redirect)`).
Round-49 candidate: refuses (`…/alternates is not a plain object-info entry (object-store redirect)`).

Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    storein = ctx.init(pathlib.Path(d) / "storein")
    ctx.write(storein / CLAIMS, "nothing ran\n")
    ctx.git(storein, "add", "-A")
    ctx.git(storein, "commit", "-qm", "claims")
    other = ctx.init(pathlib.Path(d).parent / "outside" / "other")
    ctx.write(other / "borrowed.txt", "borrowed\n")
    ctx.git(other, "add", "-A")
    ctx.git(other, "commit", "-qm", "borrowed")
    lane = ctx.init(pathlib.Path(d) / "lane")
    ctx.write(lane / CLAIMS, "nothing ran\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "claims")
    ctx.write(lane / ".git/objects/info/alternates",
              str(storein / ".git/objects") + "\n"
              + "../../../../outside/other/.git/objects\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "h2-alternates-relative-climb", "tool": "order", "expect": "accept", "defects": [],
             "build": build}]
```

### 13.3 `h3_commondir_outside.py` — sha256 `5a7dd1949fb33832aa7b9ac5156efa5df7cababbfb9945f9ff5992a420f8cfd2`

```python
"""Round-50 sealed candidate `h3-commondir-outside` (R50C1MutHostile): a top-level store whose `.git/commondir`
names a common store OUTSIDE `d` by a RELATIVE climb.

The C1 repair must admit the honest `n20_linked_worktree` shape, whose `.git/worktrees/<name>/commondir` is a
relative path (`../..`) resolved against the gitdir. This row keeps the same pointer and the same resolution
rule but moves the base one level up and the target outside `d`:

    d/lane/.git/commondir = ../../../outside/common/.git      (relative to the gitdir = d/lane/.git)

Distinct from the frozen `plans/refusals46/f7_commondir.py` (ABSOLUTE commondir, store beside `d`) and from
`f19_commondir_hidden.py` (relative commondir hidden below a pruned `.git/modules/…`): here the pointer is
relative and sits at the top level of the lane's own `.git`, the shape a repair's commondir branch reads first.

A repair that resolves `commondir` and classifies the resolved common store, but never proves the resolved path
is inside `d`, admits it; git then reads config, refs and objects from the outside store while
`rev-parse --show-toplevel` still answers inside `d` (measured, report §4).

Base fence: refuses (`commondir is not a plain-init entry`).
Round-49 candidate: refuses with the same reason.

Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    common = ctx.init(pathlib.Path(d).parent / "outside" / "common")
    ctx.write(common / CLAIMS, "nothing ran\n")
    ctx.git(common, "add", "-A")
    ctx.git(common, "commit", "-qm", "claims")
    ctx.write(common / RECEIPT, "receipt\n")
    ctx.git(common, "add", "-A")
    ctx.git(common, "commit", "-qm", "receipt")
    lane = pathlib.Path(d) / "lane"
    gd = lane / ".git"
    gd.mkdir(parents=True)
    ctx.write(gd / "HEAD", "ref: refs/heads/master\n")
    ctx.write(gd / "commondir", "../../../outside/common/.git\n")
    ctx.write(lane / CLAIMS, "nothing ran\n")
    ctx.write(lane / RECEIPT, "receipt\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "h3-commondir-outside", "tool": "order", "expect": "accept", "defects": [], "build": build}]
```

### 13.4 `h4_include_chain_outside.py` — sha256 `02032aba11f50b37f0cd395f6a1a3a10b292ef1bd8fa9bd5306d449a8b9b1260`

```python
"""Round-50 sealed candidate `h4-include-chain-outside` (R50C1MutHostile): a `[include]` chain whose FIRST hop
stays inside `d` and whose SECOND hop climbs out.

A pointer-resolving repair that generalises "resolve the pointer, classify the target" from store pointers to
config redirects would check the top-level include path (`d/inc1.cfg`, inside `d`) and stop. The included file
is itself a config: git reads it (relative paths resolve against the included file's own directory) and follows
its `[include] path = ../outside/inc2.cfg` to the fixture root and out of `d`, where `inc2.cfg` sets
`core.worktree` to an outside directory.

Measured with git (report §4): `git -C lane config --includes --get core.worktree` prints the outside path, i.e.
the second hop is live, not decorative.

Base fence: refuses `[include]` at the section allowlist.
Round-49 candidate: refuses the same way (no include leg added).

Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    lane = ctx.init(pathlib.Path(d) / "lane")
    ctx.write(lane / CLAIMS, "nothing ran\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "claims")
    ctx.write(pathlib.Path(d) / "inc1.cfg",
              "[include]\n\tpath = ../outside/inc2.cfg\n")
    ctx.write(pathlib.Path(d).parent / "outside" / "inc2.cfg",
              "[core]\n\tworktree = ../../../outside/wt\n")
    gd = lane / ".git"
    cfg = gd / "config"
    cfg.write_text(cfg.read_text() + "[include]\n\tpath = ../../inc1.cfg\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "h4-include-chain-outside", "tool": "order", "expect": "accept", "defects": [], "build": build}]
```

### 13.5 `h5_replace_ref_outside.py` — sha256 `3d69eea9285be9617f64669f06abe6a54c7fa4c8cc32d6bb28898553e020bfe6`

```python
"""Round-50 sealed candidate `h5-replace-ref-outside` (R50C1MutHostile): the honest class `n17_replace_ref`
(`refs/replace/<40hex>`, a full-40-hex ref, which the C1 repair must admit) where the ref FILE is a symlink
into a store OUTSIDE `d`.

    d/lane/.git/refs/replace/<HEAD>  ->  <outside>/repl      (a file holding an in-`d` commit id)

The ref name is git's own replace-ref shape and the content is a plain 40-hex id, so every name-and-content
rule a repair adds for `n17` passes; only the file *type* (a symlink whose target is outside `d`) and the
link location distinguish it. A repair that admits `refs/replace/<40hex>` by name and validates the body it
reads (through the link) admits this fixture, and git then resolves the replacement from outside `d`.

Measured with git (report §4): `git -C lane replace -l` lists the replaced id, i.e. git read the outside file.

Base fence: refuses (`refs/replace is not refs/heads or refs/tags`).
Round-49 candidate: refuses (`refs/replace is not a ref namespace git writes`).

Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    lane = ctx.init(pathlib.Path(d) / "lane")
    ctx.write(lane / "a.txt", "one\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-q", "-m", "one")
    ctx.write(lane / "b.txt", "two\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-q", "-m", "two")
    first = ctx.sh("git", "-C", str(lane), "rev-parse", "HEAD~1").stdout.strip()
    head = ctx.sh("git", "-C", str(lane), "rev-parse", "HEAD").stdout.strip()
    outside = pathlib.Path(d).parent / "outside" / "repl"
    ctx.write(outside, first + "\n")
    ctx.sh("mkdir", "-p", str(lane / ".git/refs/replace"))
    ctx.sh("ln", "-s", str(outside), str(lane / ".git/refs/replace" / head))
    ctx.write(lane / CLAIMS, "nothing ran\n")
    ctx.write(lane / RECEIPT, "receipt\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "h5-replace-ref-outside", "tool": "order", "expect": "accept", "defects": [], "build": build}]
```

### 13.6 `h6_fetch_head_hardlink.py` — sha256 `8fc69f67525e3f55fc9a7191f3e8f0706bd2e9d852ad95d6ad0ad2c8489d17b9`

```python
"""Round-50 sealed candidate `h6-fetch-head-hardlink` (R50C1MutHostile): the honest class `n18_shallow_fetch`
(`.git/FETCH_HEAD`, which the C1 repair must admit) where the file has a second name OUTSIDE `d`.

    d/lane/.git/FETCH_HEAD  ==  <outside>/fetch_head      (nlink = 2, same inode)

The content is a well-formed FETCH_HEAD line, so any content rule a repair adds for `n18` passes; the file is
indistinguishable from the honest twin except by `lstat.st_nlink`. A repair that whitelists `FETCH_HEAD` by
name and content while dropping the round-46 multi-link rule (the rule base applies to every top-level store
file) admits a file whose bytes another name outside `d` can rewrite after the decision.

Base fence: refuses (`FETCH_HEAD is not a plain-init entry`).
Round-49 candidate: refuses with the same reason.

Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail.
"""
import pathlib

CLAIMS = ".ufo/waves/round-42/claims/round-42-claims.md"
RECEIPT = "corpus/evidence/round42/receipt.txt"


def build(ctx, d):
    lane = ctx.init(pathlib.Path(d) / "lane")
    ctx.write(lane / "a.txt", "one\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-q", "-m", "one")
    head = ctx.sh("git", "-C", str(lane), "rev-parse", "HEAD").stdout.strip()
    outside = pathlib.Path(d).parent / "outside" / "fetch_head"
    ctx.write(outside, head + "\t\tbranch 'master' of ../src\n")
    ctx.sh("ln", str(outside), str(lane / ".git/FETCH_HEAD"))
    ctx.write(lane / CLAIMS, "nothing ran\n")
    ctx.write(lane / RECEIPT, "receipt\n")
    return ["--lane", "lane", "--claims", CLAIMS, "--receipt", RECEIPT]


FIXTURES = [{"fid": "h6-fetch-head-hardlink", "tool": "order", "expect": "accept", "defects": [], "build": build}]
```

## 14. Detector — `probe.py` (verbatim, sha256 `7e461eec903cc2eb565a7eca9295837a7b48b2fe9e1071a1f74263ed5ae6aa64`)

One build per fixture (the counter's own `build_once` over the round-44 `Ctx`), then one verdict
column per fence; `ADMIT` = `breach() is None`, `ERROR` never an admission. Run with
`python3 probe.py --lane lane --work work/probe --verify`.

```python
#!/usr/bin/env python3
"""R50C1MutHostile probe harness: one build per fixture, then one verdict column per fence under test.

Reuses the frozen round-50 counter's own machinery (`build_honest_population.build_once` over the round-44
`Ctx`, and the counter's `verdicts()` semantics: ADMIT when `breach() is None`, BREACH otherwise, ERROR never an
admission). Prints one line per fixture with the reason each fence gave, so a refusal is attributable to a rule.

Usage: python3 probe.py --lane CLONE --work DIR [--verify]
"""
import argparse
import importlib.util
import json
import os
import pathlib
import subprocess
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MODULE_FILES = [
    "h1_gitfile_to_outside.py",
    "h2_alternates_climb.py",
    "h3_commondir_outside.py",
    "h4_include_chain_outside.py",
    "h5_replace_ref_outside.py",
    "h6_fetch_head_hardlink.py",
]


def build_once_all(hb, k44, path, gen):
    """The counter's build returns positional tuples; name them once here."""
    out = []
    for fid, tool, expect, defects, argv, d, build in hb.build_once(k44, path, gen):
        out.append({"fid": fid, "tool": tool, "expect": expect, "defects": defects,
                    "argv": argv, "dir": d, "build": build, "module": path.name})
    return out


def verdict(fence, f):
    try:
        r = fence.breach(f["dir"], f["argv"], f["tool"])
    except Exception as e:                                          # a raising fence is never an admission
        return "ERROR", f"{type(e).__name__}: {e}"
    return ("ADMIT", "") if r is None else ("REFUSE", str(r))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--modules", default=str(pathlib.Path(__file__).resolve().parent / "mods"))
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)

    here = pathlib.Path(__file__).resolve().parent
    hb = load(lane / "plans/honest50/build_honest_population.py", "probe_hb")
    hb.ALLOW_NO_REPO = True
    k44 = load(lane / "plans/round44_c1_verify.py", "probe_k44")

    # the six hostile rows plus the five honest twins the C1 repair must admit (provenance for the delta)
    seen = []
    for name in MODULE_FILES:
        p = pathlib.Path(a.modules) / name
        gen = work / ("h-" + p.stem)
        gen.mkdir(parents=True, exist_ok=True)
        seen += build_once_all(hb, k44, p, gen)
    twins = [
        ("n17", lane / "plans/honest50/modules/novel49/n17_replace_ref.py"),
        ("n18", lane / "plans/honest50/modules/novel49/n18_shallow_fetch.py"),
        ("n20", lane / "plans/honest50/modules/novel49/n20_linked_worktree.py"),
        ("n21", lane / "plans/honest50/modules/novel50/n21_separate_gitdir.py"),
        ("n22", lane / "plans/honest50/modules/novel50/n22_alternates_in_d.py"),
    ]
    for tag, p in twins:
        gen = work / ("t-" + tag)
        gen.mkdir(parents=True, exist_ok=True)
        seen += build_once_all(hb, k44, p, gen)

    fences = [
        ("BASE", lane / "plans/fixture_fence.py", None),
        ("R49CAND", here / "cand_r49.py", None),
        ("EXECREPAIR", here / "exec_repair.py", None),
        ("LANDED", here / "landed.py", None),
        ("P1-all", here / "naive.py", {"store_nolocality": True, "alternates_first_only": True,
                                       "include_one_hop": True, "replace_through_link": True,
                                       "fetch_no_nlink": True}),
        ("P2-locality-correct", here / "naive.py", {"store_nolocality": False, "alternates_first_only": True,
                                                    "include_one_hop": True, "replace_through_link": True,
                                                    "fetch_no_nlink": True}),
        ("P3-links-only", here / "naive.py", {"store_nolocality": False, "alternates_first_only": False,
                                              "include_one_hop": False, "replace_through_link": True,
                                              "fetch_no_nlink": True}),
    ]
    mods = []
    for tag, path, shortcuts in fences:
        m = load(path, f"probe_fence_{tag.replace('-', '_')}")
        mods.append((tag, m, path, shortcuts))

    print("REV " + subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"],
                                  capture_output=True, text=True).stdout.strip())
    for tag, m, path, shortcuts in mods:
        import hashlib
        print(f"FENCE {tag} path={path} sha256={hashlib.sha256(path.read_bytes()).hexdigest()}")

    rows = []
    for f in seen:
        row = {"fid": f["fid"], "tool": f["tool"], "dir": f["dir"], "argv": f["argv"], "v": {}}
        for tag, m, path, shortcuts in mods:
            if shortcuts is not None:
                m.SHORTCUTS.clear()
                m.SHORTCUTS.update(shortcuts)
            v, why = verdict(m, f)
            row["v"][tag] = (v, why)
        rows.append(row)

    tags = [t for t, *_ in mods]
    for row in rows:
        cells = "  ".join(f"{t}={row['v'][t][0]}" for t in tags)
        print(f"ROW {row['fid']:<32} {cells}")
    print()
    for row in rows:
        for t in tags:
            v, why = row["v"][t]
            if v != "ADMIT":
                print(f"WHY {row['fid']} {t} {v} {why[:150]}")
    print()
    hostile = [r for r in rows if r["fid"].startswith("h")]
    for t in tags:
        adm = [r["fid"] for r in hostile if r["v"][t][0] == "ADMIT"]
        print(f"ADMITTED {t} hostile={len(adm)}/6 {' '.join(adm)}")
    twins_rows = [r for r in rows if not r["fid"].startswith("h")]
    for t in tags:
        adm = [r["fid"] for r in twins_rows if r["v"][t][0] == "ADMIT"]
        print(f"TWINS {t} admitted={len(adm)}/5 {' '.join(adm)}")

    if a.verify:
        print()
        verify(lane, work, k44, rows)
    (work / "probe.json").write_text(json.dumps(
        [{"fid": r["fid"], "v": {t: {"verdict": r["v"][t][0], "why": r["v"][t][1]} for t in tags}} for r in rows],
        indent=1))
    return 0


def verify(lane, work, k44, rows):
    """Run git itself on the built fixtures: is the escape live, or only a shape the fence rejects?"""
    ctx = k44.Ctx(work)
    env = dict(ctx.ENV)
    cases = {
        "h1-gitfile-to-outside": ("lane", ["rev-parse", "--absolute-git-dir"]),
        "h2-alternates-relative-climb": ("lane", ["rev-parse", "--git-path", "objects/info/alternates"]),
        "h3-commondir-outside": ("lane", ["rev-parse", "--git-common-dir"]),
        "h4-include-chain-outside": ("lane", ["config", "--includes", "--get", "core.worktree"]),
        "h5-replace-ref-outside": ("lane", ["replace", "-l"]),
        "h6-fetch-head-hardlink": ("lane", ["rev-parse", "HEAD"]),
    }
    by_fid = {r["fid"]: r for r in rows}
    for fid, (sub, args) in cases.items():
        r = by_fid.get(fid)
        if r is None:
            print(f"VERIFY {fid} missing")
            continue
        d = pathlib.Path(r["dir"]) / sub
        p = subprocess.run(["git", "-C", str(d)] + args, env=env, capture_output=True, text=True)
        out = (p.stdout.strip() or p.stderr.strip()).replace(str(pathlib.Path(r["dir"]).parent), "<GEN>")
        print(f"VERIFY {fid} rc={p.returncode} argv=git -C {sub} {' '.join(args)} out={out[:160]!r}")
        if fid in ("h2-alternates-relative-climb", "h6-fetch-head-hardlink"):
            target = d / ".git/FETCH_HEAD" if fid.startswith("h6") else d / ".git/objects/info/alternates"
            try:
                st = os.lstat(target)
                print(f"VERIFY {fid} lstat nlink={st.st_nlink} size={st.st_size}")
            except OSError as e:
                print(f"VERIFY {fid} lstat failed {e}")


if __name__ == "__main__":
    sys.exit(main())
```

## 15. Probe generator — `make_naive.py` (verbatim, sha256 `786bfb24b6e00eaad42ddcf71701741a1c4306e572718f99ece172c910f4a7fc`)

Applies each source substitution exactly once to `cand_r49.py` (`b687b1d9`) and writes `naive.py`
(`9a9245ffcb4212f625491d4b0b5f52053040f1bba18dd55d8f7fad2219096bce`); `SHORTCUTS` is read at call time, so a probe is one baked dict
(`naive_p1.py` `0b07d57d00d97171550ff1e289880589f2c3d5e6911ccab02ffa9ebfc3f8b960`, `naive_p2.py` `21bdea36b5e0fd6f5fe9adca71469af08d7fa2c41ce8e492f60ed287358f273f`).

```python
#!/usr/bin/env python3
"""Build `naive.py`, a SCRATCH-ONLY probe fence: the round-49 candidate (`b687b1d9…`, which already admits
121/126 honest) extended with the five pointer legs the C1 repair must add (gitfile, commondir, worktrees,
alternates, refs/replace, FETCH_HEAD/shallow, include). It is NOT a candidate for landing: it embodies one
plausible repair shortcut per leg, each switchable at runtime through `SHORTCUTS`, so the seat can measure which
hostile row each shortcut admits.

Every source substitution asserts it applies exactly once; the script prints the resulting sha256.
"""
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "cand_r49.py"
DST = HERE / "naive.py"

PAIRS = []


def sub(old, new):
    PAIRS.append((old, new))


# --- 1. constants: pointer names, the gitfile pattern, the shortcut table, per-call globals ------------------
sub('''GIT_TOP = {"HEAD", "ORIG_HEAD", "COMMIT_EDITMSG", "config", "description", "hooks", "index", "info",
           "logs", "objects", "refs", "packed-refs"}''',
    '''GIT_TOP = {"HEAD", "ORIG_HEAD", "COMMIT_EDITMSG", "config", "description", "hooks", "index", "info",
           "logs", "objects", "refs", "packed-refs", "FETCH_HEAD", "shallow", "commondir", "worktrees"}

# round-50 probe: one plausible repair shortcut per pointer leg. Mutated by the harness, read at call time.
SHORTCUTS = {"store_nolocality": False, "alternates_first_only": False,
             "include_one_hop": False, "replace_through_link": False, "fetch_no_nlink": False}
GITFILE = re.compile(r"\\Agitdir:[ \\t]*(.+?)[ \\t]*\\n?\\Z")
_D = None
_GITFILES = {}
_VISITED = set()''')

# --- 2. _store: visited guard, pointer names, commondir/FETCH_HEAD/shallow legs, commondir required-set ------
sub('''def _store(gd, label, ddev):
    """Classify one `.git` directory, entry by entry, against what `git init` + commits writes."""
    ents = _entries(gd)
    if ents is None:
        return f"{label} unreadable"
    have = set()''',
    '''def _store(gd, label, ddev):
    """Classify one `.git` directory, entry by entry, against what `git init` + commits writes."""
    key = _norm(gd)
    if key in _VISITED:
        return None
    _VISITED.add(key)
    ents = _entries(gd)
    if ents is None:
        return f"{label} unreadable"
    have = set()''')

sub('''        if name in GIT_DIRS:
            if not stat.S_ISDIR(mode):
                return f"{label}/{name} is not a directory"
            continue
        if not stat.S_ISREG(mode):
            return f"{label}/{name} is not a regular file"
        if _linked(mode, n):
            return f"{label}/{name} has more than one hard link"''',
    '''        if name in GIT_DIRS:
            if not stat.S_ISDIR(mode):
                return f"{label}/{name} is not a directory"
            continue
        if name == "worktrees":
            if not stat.S_ISDIR(mode):
                return f"{label}/worktrees is not a directory"
            why = _worktrees(q, f"{label}/worktrees", ddev)
            if why:
                return why
            continue
        if not stat.S_ISREG(mode):
            return f"{label}/{name} is not a regular file"
        if _linked(mode, n) and not (name in ("FETCH_HEAD", "shallow") and SHORTCUTS["fetch_no_nlink"]):
            return f"{label}/{name} has more than one hard link"''')

sub('''        elif name == "packed-refs":
            why = _packed(q, label)
            if why:
                return why
    for req in ("HEAD", "config", "objects", "refs"):''',
    '''        elif name == "packed-refs":
            why = _packed(q, label)
            if why:
                return why
        elif name == "FETCH_HEAD":
            if size > TEXT_CAP:
                return f"{label}/FETCH_HEAD exceeds {TEXT_CAP} bytes"
        elif name == "shallow":
            raw = _read(q, TEXT_CAP)
            if raw is None:
                return f"{label}/shallow unreadable"
            for line in raw.split(b"\\n"):
                if line and HEX40.match(line) is None:
                    return f"{label}/shallow carries a row git does not write"
        elif name == "commondir":
            raw = _read(q, 4096)
            if raw is None or not raw.strip():
                return f"{label}/commondir is empty"
            target = pathlib.Path(_norm(os.path.join(str(gd), raw.strip().decode("ascii", "replace"))))
            if not target.is_dir():
                return f"{label}/commondir names no directory"
            if not SHORTCUTS["store_nolocality"] and not _inside(target, _D):
                return f"{label}/commondir resolves outside the fixture"
            why = _store(target, f"{label}/commondir", ddev)
            if why:
                return why
    reqs = ("HEAD",) if "commondir" in have else ("HEAD", "config", "objects", "refs")
    for req in reqs:''')

# --- 2b. a commondir-bearing gitdir keeps no local objects/refs/logs: they live in the common dir ----------
sub("""    if \"hooks\" in have:
        why = _hooks(gd / \"hooks\", f\"{label}/hooks\", ddev)""",
    """    if \"commondir\" in have:
        return None
    if \"hooks\" in have:
        why = _hooks(gd / \"hooks\", f\"{label}/hooks\", ddev)""")

# --- 3. worktree-metadata classifier (n20's `.git/worktrees/<name>`) ---------------------------------------
sub('''# ---------- the decision ----------''',
    '''def _worktrees(p, label, ddev):
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    for name, mode, _s, _n, dev in ents:
        q = p / name
        if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
            return f"{_rel(q, label)} is not a worktree directory"
        if dev != ddev:
            return f"{_rel(q, label)} crosses a mount boundary"
        why = _worktree(q, f"{label}/{name}", ddev)
        if why:
            return why
    return None


def _worktree(p, label, ddev):
    ents = _entries(p)
    if ents is None:
        return f"{label} unreadable"
    allowed = {"commondir", "gitdir", "HEAD", "ORIG_HEAD", "index", "logs", "refs"}
    have = set()
    for name, mode, size, n, dev in ents:
        q = p / name
        if stat.S_ISLNK(mode):
            return f"{label}/{name} is a symlink"
        if dev != ddev:
            return f"{label}/{name} crosses a mount boundary"
        if name not in allowed:
            return f"{label}/{name} is not a worktree-metadata entry"
        if name in ("logs", "refs"):
            if not stat.S_ISDIR(mode):
                return f"{label}/{name} is not a directory"
            if name == "refs":
                why = _refs(q, f"{label}/refs", ddev)
                if why:
                    return why
            continue
        if not stat.S_ISREG(mode):
            return f"{label}/{name} is not a regular file"
        have.add(name)
        if name == "commondir":
            raw = _read(q, 4096)
            if raw is None or not raw.strip():
                return f"{label}/commondir is empty"
            target = pathlib.Path(_norm(os.path.join(str(p), raw.strip().decode("ascii", "replace"))))
            if not target.is_dir():
                return f"{label}/commondir names no directory"
            if not SHORTCUTS["store_nolocality"] and not _inside(target, _D):
                return f"{label}/commondir resolves outside the fixture"
            why = _store(target, f"{label}/commondir", ddev)
            if why:
                return why
        elif name == "gitdir":
            raw = _read(q, 4096)
            if raw is None or not raw.strip():
                return f"{label}/gitdir is empty"
        elif name == "HEAD":
            body = _read(q, 200)
            if body is None or (HEAD_REF.match(body) is None and HEAD_HEX.match(body) is None):
                return f"{label}/HEAD is not a branch line or a detached sha"
        elif name == "ORIG_HEAD":
            body = _read(q, 200)
            if body is None or HEX40.match(body) is None:
                return f"{label}/ORIG_HEAD is not a 40-hex sha"
        elif name == "index":
            if size > INDEX_CAP:
                return f"{label}/index exceeds {INDEX_CAP} bytes"
    if "commondir" not in have:
        return f"{label} has no commondir"
    return None


# ---------- the decision ----------''')

# --- 4. objects/info/alternates ----------------------------------------------------------------------------
sub('''        if name == "commit-graphs":
            why = _graph_dir(q, f"{label}/commit-graphs", ddev)
            if why:
                return why
            continue
        return f"{_rel(q, label)} is not a plain object-info entry (object-store redirect)"''',
    '''        if name == "commit-graphs":
            why = _graph_dir(q, f"{label}/commit-graphs", ddev)
            if why:
                return why
            continue
        if name == "alternates":
            raw = _read(q, TEXT_CAP)
            if raw is None:
                return f"{_rel(q, label)} unreadable"
            entries = [ln.strip() for ln in raw.decode("ascii", "replace").splitlines() if ln.strip()]
            if not entries:
                return f"{_rel(q, label)} is empty"
            if SHORTCUTS["alternates_first_only"]:
                entries = entries[:1]
            for ent in entries:
                target = pathlib.Path(_norm(os.path.join(str(p.parent), ent)))
                if not target.is_dir():
                    return f"{_rel(q, label)} names no object directory"
                if not SHORTCUTS["store_nolocality"] and not _inside(target, _D):
                    return f"{_rel(q, label)} names {ent!r} outside the fixture"
            continue
        return f"{_rel(q, label)} is not a plain object-info entry (object-store redirect)"''')

# --- 5. refs/replace ----------------------------------------------------------------------------------------
sub('''        if name not in REF_NAMESPACES:
            return f"{label}/{name} is not a ref namespace git writes"''',
    '''        if name == "replace":
            why = _replace_tree(q, label, ddev)
            if why:
                return why
            continue
        if name not in REF_NAMESPACES:
            return f"{label}/{name} is not a ref namespace git writes"''')

sub('''def _refs(p, label, ddev):''',
    '''def _replace_tree(p, label, ddev):
    """`refs/replace/<40hex>`: git's replace namespace. A repair that resolves the ref through a link first
    (SHORTCUTS["replace_through_link"]) and validates only the 40-hex body cannot see where the body came from.
    """
    ents = _entries(p)
    if ents is None:
        return f"{_rel(p, label)} unreadable"
    for name, mode, _s, n, dev in ents:
        q = p / name
        if dev != ddev:
            return f"{_rel(q, label)} crosses a mount boundary"
        if not REF_HEX.match(name):
            return f"{_rel(q, label)} has a name git does not write"
        if stat.S_ISLNK(mode):
            if not SHORTCUTS["replace_through_link"]:
                return f"{_rel(q, label)} is a symlink"
            body = _read(q, 200)
            if body is None or HEX40.match(body) is None:
                return f"{_rel(q, label)} is not a 40-hex ref"
            continue
        if not stat.S_ISREG(mode):
            return f"{_rel(q, label)} is a special file"
        if _linked(mode, n):
            return f"{_rel(q, label)} has more than one hard link"
        body = _read(q, 200)
        if body is None or HEX40.match(body) is None:
            return f"{_rel(q, label)} is not a 40-hex ref"
    return None


def _refs(p, label, ddev):''')

# --- 6. config [include] ------------------------------------------------------------------------------------
sub('''    sect, sub = "", None''', '''    sect, sub, in_include = "", None, False''')

sub('''            if m is not None:
                sect = m.group(1).decode("ascii").lower()
                sub = None
                if sect not in CFG_SECTIONS:
                    return f"{label}/config section [{sect}] is not allowlisted"
                continue''',
    '''            if m is not None:
                sect = m.group(1).decode("ascii").lower()
                sub = None
                in_include = sect == "include"
                if in_include:
                    if not SHORTCUTS["include_one_hop"]:
                        return f"{label}/config section [include] is not allowlisted"
                    continue
                if sect not in CFG_SECTIONS:
                    return f"{label}/config section [{sect}] is not allowlisted"
                continue''')

sub('''        why = _config_value(label, sect, sub, m.group(1).decode("ascii").lower(),
                            val_raw.strip(b" \\t") if eq else b"", bool(eq))
        if why:
            return why''',
    '''        key = m.group(1).decode("ascii").lower()
        if in_include:
            if key != "path":
                return f"{label}/config include key {key} is not allowlisted"
            target = pathlib.Path(_norm(os.path.join(
                str(p.parent), val_raw.strip(b" \\t").decode("ascii", "replace"))))
            if not target.is_file():
                return f"{label}/config include path names no file"
            if not _inside(target, _D):
                return f"{label}/config include path resolves outside the fixture"
            continue
        why = _config_value(label, sect, sub, key,
                            val_raw.strip(b" \\t") if eq else b"", bool(eq))
        if why:
            return why''')

# --- 7. tree walk: `.git` FILE -> resolve the gitfile ------------------------------------------------------
sub('''            if name == ".git":
                return None, f"{_rel(p, d)} is a file (gitdir redirect), not a directory"''',
    '''            if name == ".git":
                body = _read(p, 4096)
                m = GITFILE.match(body.decode("ascii", "replace")) if body is not None else None
                if m is None:
                    return None, f"{_rel(p, d)} is a file (gitdir redirect), not a directory"
                tgt = pathlib.Path(_norm(os.path.join(str(p.parent), m.group(1))))
                if not SHORTCUTS["store_nolocality"] and not _inside(tgt, d):
                    return None, f"{_rel(p, d)} gitfile resolves outside the fixture"
                repos.append(t)
                _GITFILES[_norm(t)] = tgt
                continue''')

# --- 8. breach: per-call state, gitfile stores, lane membership ---------------------------------------------
sub('''    d = pathlib.Path(_norm(dpath))
    ddev = st.st_dev''',
    '''    d = pathlib.Path(_norm(dpath))
    global _D
    _D = d
    _GITFILES.clear()
    _VISITED.clear()
    ddev = st.st_dev''')

sub('''    for repo in repos:
        why = _store(repo / ".git", f"{_rel(repo / '.git', d)}", ddev)
        if why:
            return why''',
    '''    for repo in repos:
        gd = _GITFILES.get(_norm(repo), repo / ".git")
        why = _store(gd, f"{_rel(gd, d)}", ddev)
        if why:
            return why''')

# --- 9. the 40-hex ref-name pattern ------------------------------------------------------------------------
sub('''REF_PATH = re.compile(r"\\A[A-Za-z0-9_][A-Za-z0-9._/-]*\\Z", re.ASCII)''',
    '''REF_PATH = re.compile(r"\\A[A-Za-z0-9_][A-Za-z0-9._/-]*\\Z", re.ASCII)
REF_HEX = re.compile(r"\\A[0-9a-f]{40}\\Z", re.ASCII)''')


# --- 10b. reflog dir allowlist and the worktree-format extension section --------------------------------
sub("""if not (rel in (\"refs\", \"refs/heads\", \"refs/tags\", \"refs/notes\")""",
    """if not (rel in (\"refs\", \"refs/heads\", \"refs/tags\", \"refs/notes\", \"refs/remotes\")""")

sub('CFG_SECTIONS = {"core", "user", "init"}', 'CFG_SECTIONS = {"core", "user", "init", "extensions"}')

sub("""    (\"core\", \"safecrlf\"): \"safecrlf\",
}""",
    """    (\"core\", \"safecrlf\"): \"safecrlf\",
    (\"extensions\", \"worktreeconfig\"): \"bool\",
}""")


# --- 10c. `refs/remotes` namespace and the relative-worktrees extension key ------------------------------
sub('REF_NAMESPACES = ("heads", "tags", "notes")', 'REF_NAMESPACES = ("heads", "tags", "notes", "remotes")')

sub("""    (\"extensions\", \"worktreeconfig\"): \"bool\",
}""",
    """    (\"extensions\", \"worktreeconfig\"): \"bool\",
    (\"extensions\", \"relativeworktrees\"): \"bool\",
}""")


# --- 10d. the worktree back-pointer `gitdir` must resolve inside d (frozen f18) ---------------------------
sub('"FETCH_HEAD", "shallow", "commondir", "worktrees"}',
    '"FETCH_HEAD", "shallow", "commondir", "worktrees", "gitdir"}')

sub("""        elif name == \"commondir\":
            raw = _read(q, 4096)""",
    """        elif name == \"gitdir\":
            raw = _read(q, 4096)
            if raw is None or not raw.strip():
                return f\"{label}/gitdir is empty\"
            target = pathlib.Path(_norm(os.path.join(str(gd), raw.strip().decode(\"ascii\", \"replace\"))))
            if not os.path.lexists(str(target)):
                return f\"{label}/gitdir names no path\"
            if not SHORTCUTS[\"store_nolocality\"] and not _inside(target, _D):
                return f\"{label}/gitdir resolves outside the fixture\"
        elif name == \"commondir\":
            raw = _read(q, 4096)""")

sub("""        elif name == \"gitdir\":
            raw = _read(q, 4096)
            if raw is None or not raw.strip():
                return f\"{label}/gitdir is empty\"
        elif name == \"HEAD\":""",
    """        elif name == \"gitdir\":
            raw = _read(q, 4096)
            if raw is None or not raw.strip():
                return f\"{label}/gitdir is empty\"
            target = pathlib.Path(_norm(os.path.join(str(p), raw.strip().decode(\"ascii\", \"replace\"))))
            if not SHORTCUTS[\"store_nolocality\"] and not _inside(target, _D):
                return f\"{label}/gitdir resolves outside the fixture\"
        elif name == \"HEAD\":""")


# --- 10. the two honest classes the probe must also repair to be a *complete* repair ----------------------
sub('    m = re.fullmatch(r"refs/(?:heads|tags|notes)/(.+)", rel, re.ASCII)',
    '    m = re.fullmatch(r"refs/(?:heads|tags|notes|remotes)/(.+)", rel, re.ASCII)')

sub("""    elif need == \"0\":
        if low not in (\"0\", \"\"):
            return f\"{label}/config {where} must be 0\"""",
    """    elif need == \"0\":
        if low not in (\"0\", \"1\", \"\"):
            return f\"{label}/config {where} must be 0 or 1\"""")


def main():
    src = SRC.read_text()
    out = src
    for i, (old, new) in enumerate(PAIRS, 1):
        n = out.count(old)
        if n != 1:
            print(f"SUBSTITUTION {i} applies {n} times, expected 1: {old.splitlines()[0][:90]!r}",
                  file=sys.stderr)
            return 2
        out = out.replace(old, new)
    header = ('"""round-50 probe fence (R50C1MutHostile, scratch only): the round-49 candidate plus the five\n'
              'pointer legs the C1 repair must add, each with one plausible shortcut switch in SHORTCUTS.\n'
              'Generated by make_naive.py from cand_r49.py (b687b1d9…); NOT a landing candidate."""\n')
    out = header + out
    DST.write_text(out)
    print(f"NAIVE {DST} sha256={hashlib.sha256(out.encode()).hexdigest()} lines={len(out.splitlines())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## VERDICT

`VERDICT`: six fresh hostile pointer variants authored and measured; **all six REFUSED** by the base fence
`05d5fe03`, the r49 candidate `b687b1d9`, the wave-1 sibling repair `9baedf13` and the **landed** fence
`57adce4a`, each with an attributable rule (`build_errors=0` on the `plans/sealed50/` leg). A locality-correct
pointer repair (P2) that admits all 126 honest fixtures and keeps `REFUSALS 20/20` + `SEALED(sealed46) 12/12`
**admits four of the six (h2, h4, h5, h6)** and passes the whole predicate when the six are absent — so the rows
are discriminating, not decorative: `h2`, `h4`, `h5` are net-new against the landed 18-row blind set (which the
same repair defeats on 17/18), `h6` duplicates landed `b2`, `h1` duplicates landed gitfile rows and `h3`
duplicates `refusals46/f7`+`f19`. Handed to the L1 as candidate `plans/sealed50/` rows with **expected refusal**
(measured on the landed fence: 24/24 clean, `PREDICATE R50-C1 pass`, sealed50 leg 18 → 24). No production file
was written, no claim admitted, scratch removed.

`AXES`: novelty (R50-C1) — pointer kind × resolution shortcut × fence under test (§1).
`REV`: `3b02d573d58cc6d2e0d27ef92ac0815354912252` (clone measured); landed fence `57adce4a` measured as a blob of
`d45c5bb`; live lane at read end `d45c5bb`.
