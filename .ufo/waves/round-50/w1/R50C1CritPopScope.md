# R50C1CritPopScope — population completeness attack on R50-C1 (novelty)

Seat: critic, leaf member (no dispatch). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Wave: round 50, w1. Item: enumerate documented git states the frozen 126-fixture honest population does not
hold; mark each must-admit / may-refuse / out-of-scope with a git-doc pointer; quantify the over-refusal surface
this population cannot see.

## REV

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
5c56819f7964f4af19c960de08a49cd8f95781ce          # at session start; tip advanced to 822f3b7 mid-session
$ git merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD; echo $?
0  (ANCESTOR_OK)
$ git log --oneline 3b02d57..822f3b7 | cat
822f3b7 round-50: C2 corrections (12 pointers resolved append-only), git-doc sources S173-S177, honest-geometry knowledge entry
5c56819 round-50: w1 v2 wave spec + dispatch evidence (72 seats, 34 attack, policy v2 accepted)
$ sha256sum plans/fixture_fence.py        # at lane tip 822f3b7
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
```

**Measured revision 1 (population census and base-fence probes): `3b02d573d58cc6d2e0d27ef92ac0815354912252`**
(stage-1 freeze, verified ancestor), via `git clone --shared` at that commit. At that time the lane tip was
`5c56819`→`822f3b7` and `plans/fixture_fence.py` was still the base fence `05d5fe03…`.

**Measured revision 2 (landed repair, §7): `6db0279e2506c1788b26c2586b4d2d774228c6a9`.** The lane landed
`c3372a9` (counter open-window repair) and `6db0279` ("S3 fence repair (five documented git shapes resolved by
containment), sealed50 hostile set, re-derived mutant battery"). At `6db0279e` the fence is
`57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1` and the frozen predicate **passes**:
`HONEST fixtures=126 admitted=126 refused=0`, `REFUSALS 20/20`, `SEALED 12/12` + `12→18/18`,
`MUTANTS total=22 caught=15 floor=12 met`, `PREDICATE R50-C1 pass`, rc=0, `TREE dirty=0`. §1–§6 are the base-fence
census (still valid as the "before"); §7 re-measures the same absent-state probe set against the landed fence.

Axes named: **novelty** (C1's honest-geometry denominator — what `HONEST fixtures=126 admitted=126` can and
cannot mean). Secondary: **quality** (mutant-battery sensitivity on allowlist branches the population never
exercises). Not claimed: coverage (operator-capped), C1/C2 admission.

## 1. Baseline reproduction (fast leg and full leg, base fence, clean clone)

```
$ TMPDIR=$S python3 plans/round50_c1_verify.py --lane . --skip-mutants --work "$S/work"
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=0
FENCE .../lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
... (12 HONEST-REFUSED lines)
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
PREDICATE R50-C1 fail
```

The measured state in the brief reproduces (`126/113/13`). Two receipt defects fall out of this run, both on
the base fence's honest leg, both cheap to fix in S2:

* **`HONEST-REFUSED` truncates silently.** `refused[:12]` prints 12 lines while the summary says
  `refused=13`. The unlisted refusal is `n08-tag-detached` (`repo/.git/HEAD is not a plain branch HEAD`). A
  receipt that shows 13 and lists 12 is not a receipt of the 13.
* **`--work DIR` crashes when the parent does not exist**: `tempfile.mkdtemp(..., dir=a.work)` →
  `FileNotFoundError` (exit 1, no counter lines). Pass a normal `--work` and it is fine; the argument should
  `mkdir` rather than crash.

Full leg (mutant battery as carried), same clone:

```
MUTANT broken  c1-mut-01,02,04,06,08,09,11,15,17,18,21,23   (12: patch does not apply — battery is a candidate against the r49 candidate fence)
MUTANT survived c1-mut-05-git-top-commondir
MUTANT survived c1-mut-07-config-cr
MUTANT survived c1-mut-10-inside-prefix
MUTANT survived c1-mut-12-store-required
MUTANT survived c1-mut-14-argv-placeholder
MUTANT survived c1-mut-16-argv-shape-tail
MUTANT survived c1-mut-20-packedref-peel
MUTANT survived c1-mut-22-fixture-symlink
MUTANTS total=23 caught=3 broken=12 floor=12 verdict=unmet
```

Measured on the base fence: **3 caught, 8 survived, 12 inapplicable** (the brief's "4 of 23 change the vector"
is close but not the measured triple). `c1-mut-20-packedref-peel` surviving is not a stray: it is section 4's
witnessed blind branch.

## 2. The full refusal set of the base fence (correcting the starting state)

The brief names five refused classes (`n17,n18,n20,n21,n22`). Measured over the frozen 126: **13 fixtures in
13 classes, 11 distinct first-reason strings**:

| fid | class | first reason |
|---|---|---|
| n03-detached-head | r46novel | `HEAD is not a plain branch HEAD` |
| n07-reflog-gc | r46novel | `info/refs is not git's exclude file` |
| n08-tag-detached | r46novel | `HEAD is not a plain branch HEAD` |
| n12-local-config-user | novel48 | `config section [user] is not allowlisted` |
| n13-remote-origin | novel48 | `config section header b'[remote "origin"]' is not plain` |
| n14-stash-entry | novel48 | `logs/refs/stash has a name git does not write` |
| n15-commit-graph | novel48 | `objects/info/commit-graph present (object-store redirect)` |
| n16-notes-ref | novel48 | `logs/refs/notes has a name git does not write` |
| n17-replace-ref | novel49 | `refs/replace is not refs/heads or refs/tags` |
| n18-shallow-fetch | novel49 | `FETCH_HEAD is not a plain-init entry` |
| n20-linked-worktree | novel49 | `wt/.git is a file (gitdir redirect)` |
| n21-separate-gitdir | novel50 | `wt/.git is a file (gitdir redirect)` |
| n22-alternates-in-d | novel50 | `objects/info/alternates present (object-store redirect)` |

The five-class list is a subset (the r49/r50-authored ones). The repair is bound by all 13: every fixture in
the population must reach ADMIT.

## 3. Population coverage of the documented store surface (measured, not asserted)

Method: build all 126 fixtures once (`plans/honest50/build_honest_population.py` + round-44 `Ctx`), scan each
built tree for every documented entry, score the base fence per fixture. Scratch tool `census.py` (not
committed) — the population side is a faithful re-use of the frozen builder, so its numbers match the counter.

`gitrepository-layout(5)` (Git 2.56.0 `man 5`) documents **38 store entries**. Population holds **25**, holds
**zero** of the other **13**:

```
config.worktree  branches/  common(wording)  sharedindex.<SHA-1>  info/grafts  info/attributes
info/sparse-checkout  remotes/  logs/refs/tags/<name>  modules/  worktrees/<id>/locked
worktrees/<id>/config.worktree  objects/info/http-alternates
  -> measured 0/126 for every one of these (scan: config.worktree 0, top:sharedindex 0, top:modules 0,
     logs/refs/tags 0, worktrees/<id>/locked 0, worktrees/<id>/config.worktree 0, top:branches 0,
     top:remotes 0, info/grafts 0, info/attributes 0, info/sparse-checkout 0, objects/info/http-alternates 0)
```

Entries the population *does* hold but only inside a fixture that is refused for another reason (the repair is
therefore bound by them, and the honest leg never sees their rule fire separately): `objects/info/packs`,
`info/refs`, `objects/pack/*.{pack,idx,rev}`, `objects/info/commit-graph` (all n07/n15),
`refs/remotes/*` + `logs/refs/remotes/*` + `FETCH_HEAD` + `shallow` (n18), `refs/replace` (n17),
`refs/notes` (n16), `refs/stash` (n14), `config:[user]` (n12), `config:[remote]` (n13,n18),
`[extensions] relativeWorktrees` + `worktrees/<id>/{gitdir,commondir}` (n20), gitfile `.git` (n20,n21),
`objects/info/alternates` (n22).

## 4. Documented states the population does not hold — measured verdict + classification

26 scratch probes (plus 12 isolated-entry probes), each built with git in scratch (clean env:
`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, fixed identity), each scored with
`plans/fixture_fence.py::breach` at the freeze; two builds per probe for the determinism column.
`det` = two builds give the same `tree_identity` (i.e. addable to the pinned population as-is). `ladder` =
number of independent fence rules the state trips (diagnostic: the named entry is deleted and the fence re-run).

| # | state | doc pointer | git writes it | in 126? | base verdict | rules | class |
|---|---|---|---|---|---|---|---|
| 1 | `objects/pack/multi-pack-index` | `git-multi-pack-index(1)`, `gitformat-pack(5)` | yes | 0/126 | **BREACH** `multi-pack-index is not a pack file` | 3* | **must-admit** |
| 2 | `objects/info/commit-graphs/` chain | `git-commit-graph(1) --split`, `gitformat-commit-graph(5)` | yes | 0/126 | **BREACH** `commit-graphs present (object-store redirect)` | 1 | **must-admit** |
| 3 | `config.worktree` + `info/sparse-checkout` + `[extensions] worktreeConfig` (`git sparse-checkout set`) | `git-sparse-checkout(1)`, `gitrepository-layout(5)` | yes | 0/126 | **BREACH** `[extensions] is not allowlisted` (+ `config.worktree`, `info/sparse-checkout` unbound) | 3 | **must-admit** (2 of 3 rules unbound) |
| 4 | `modules/` + `[submodule "<n>"]` (`git submodule add`) | `gitrepository-layout(5) modules`, `gitsubmodules(7)` | yes | 0/126 | **BREACH** `sub/.git is a file` then `[submodule "sub"]` | 2 | **must-admit** (gitfile rule bound by n20/n21; `modules/` + `[submodule]` unbound) |
| 5 | `MERGE_HEAD`,`MERGE_MSG`,`MERGE_MODE`,`AUTO_MERGE` (conflicted merge left in place) | `git-merge(1)` FILES | yes | 0/126 | **BREACH** `AUTO_MERGE is not a plain-init entry` | 4 | **must-admit** |
| 6 | `sharedindex.<40hex>` (`git update-index --split-index`) | `gitrepository-layout(5)`, `git-update-index(1)` | yes | 0/126 | **BREACH** `sharedindex.<sha> is not a plain-init entry` | 1 | **must-admit**, `det=False` |
| 7 | `logs/refs/tags/<name>` (`git tag --create-reflog`) | `gitrepository-layout(5)`, `git-tag(1)` | yes | 0/126 | **ADMIT** (`_log_name_ok` allows `refs/tags`) | 0 | must-admit, **already admitted, unwitnessed** |
| 8 | `worktrees/<id>/locked`, `worktrees/<id>/config.worktree` | `gitrepository-layout(5)`, `git-worktree(1)` | yes | 0/126 | **BREACH** `.git/worktrees is not a plain-init entry`; the two inner files are never classified (the fence classifies only directories named `.git`) | 1 | **must-admit** (and a containment decision: `worktrees/<id>/gitdir`/`commondir` name paths/stores) |
| 9 | `core.worktree` naming a work tree inside `d` | `git-config(1) core.worktree`, `gitrepository-layout(5)` | yes (`git config`) | 0/126 | **BREACH** `config key core.worktree is not allowlisted` | 1 | **must-decide** (value-dependent; name-based refusal cannot admit the in-`d` case) |
| 10 | `[extensions] objectformat=sha256` + 64-hex refs/objects (`git init --object-format=sha256`) | `git-init(1)`, `gitrepository-layout(5)` format v1 | yes | 0/126 | **BREACH** `[extensions] is not allowlisted` | 1 | **must-decide** (`det=True`) |
| 11 | `reftable/` + `[extensions] refstorage=reftable`, HEAD `ref: refs/heads/.invalid` (`git init --ref-format=reftable`) | `git-init(1) --ref-format`, `gitrepository-layout(5)` format v1 | yes | 0/126 | **BREACH** `HEAD is not a plain branch HEAD` then `[extensions]` | 2 | **must-decide**, `det=False` |
| 12 | `rr-cache/` + `MERGE_RR` (`rerere.enabled` + a merge) | `git-rerere(1)` | yes (with config) | 0/126 | **BREACH** `AUTO_MERGE` … `MERGE_RR` … `[rerere]` | 6 | **must-decide** |
| 13 | `info/grafts` | `gitrepository-layout(5) info/grafts` (deprecated, superseded by `git-replace(1)`) | **no** (read only) | 0/126 | **BREACH** `info/grafts is not git's exclude file` | 1 | may-refuse + record decision |
| 14 | `info/attributes` | `gitrepository-layout(5) info/attributes` | **no** | 0/126 | **BREACH** | 1 | may-refuse |
| 15 | `objects/info/http-alternates` | `gitrepository-layout(5)` | **no** | 0/126 | **BREACH** `http-alternates present (object-store redirect)` | 2 | may-refuse |
| 16 | `branches/`, `remotes/` legacy shorthands | `gitrepository-layout(5)` (read stops in git 3.0) | **no** (legacy) | 0/126 | **BREACH** `branches is not a plain-init entry` | 1 | out-of-scope |
| 17 | enabled hook (`hooks/pre-commit`, no `.sample`) | `githooks(5)` | **no** (user renames) | 0/126 | **BREACH** `pre-commit is not a hook sample` | 1 | may-refuse (executable code) |
| 18 | `[filter "lfs"]`,`[lfs]`,`.git/lfs/`, LFS hook (`git lfs install --local`) | `git-lfs` (third-party), `gitattributes(5)` | third-party | 0/126 | **BREACH** `[lfs] is not allowlisted` | 2 | out-of-scope (third-party state) |
| 19 | LFS **pointer** files only (no `lfs install`) | `gitattributes(5)`, git-lfs pointer spec | blob content | 0/126 | **ADMIT** (no store entry: only `.gitattributes` + a pointer blob) | 0 | out-of-scope (already admitted) |
| 20 | `packed-refs` peeled `^<40hex>` line (annotated tag + `pack-refs --all`) | `git-pack-refs(1)`, `gitrepository-layout(5) packed-refs` | yes | **0/126** (header only: n01,n07 carry no peeled line) | **ADMIT** | 0 | must-admit, **already admitted, unwitnessed** |
| 21 | cruft `pack-*.mtimes` (plain `git gc` with unreachable objects; `gc.cruftPacks` **unset** in 2.56) | `git-gc(1) --cruft`, `gitformat-pack(5)` | yes | **0/126** (n07 uses `--prune=now`) | **ADMIT** (name allowlisted) | — | must-admit, **already admitted, unwitnessed** |
| 22 | `pack-*.keep`, `pack-*.bitmap` (`git repack -b`, `.keep`) | `gitformat-pack(5)`, `git-repack(1)` | yes | 0/126 | **ADMIT** (name allowlisted) | — | must-admit, **already admitted, unwitnessed** |

Isolated entry rules (second measurement, so no entry's rule is inferred from a multi-deviation fixture;
plain `git init`+commit plus exactly one entry)::

    config.worktree empty file      -> '.git/config.worktree is not a plain-init entry'
    info/sparse-checkout            -> ".git/info/sparse-checkout is not git's exclude file"
    modules/ dummy dir              -> '.git/modules is not a plain-init entry'
    rr-cache/ dir                   -> '.git/rr-cache is not a plain-init entry'
    MERGE_RR file                   -> '.git/MERGE_RR is not a plain-init entry'
    reftable/ dir                   -> '.git/reftable is not a plain-init entry'
    worktrees/w/locked              -> '.git/worktrees is not a plain-init entry'
    worktrees/w/config.worktree     -> '.git/worktrees is not a plain-init entry'
    [submodule "x"] section         -> '.git/config section header b\'[submodule "x"]\' is not plain'
    64-hex ref body                 -> 'refs/heads/wide is not a 40-hex ref'
    64-hex loose object             -> 'objects/ab/000…0 is not a loose object'
    logs/refs/tags/v1               -> None          (admitted)

`*` MPI ladder (measured): `info/refs` → `objects/info/packs` → `objects/pack/multi-pack-index is not a pack
file` → ADMIT. The first two are bound by n07; the third is not bound by any fixture.

Population-absent states that are *composition* of two present classes (the item asks about one): shallow +
`refs/replace` — measured BREACH on the composed fixture, but every rule it trips (`[remote]`, `shallow`,
`refs/replace`, `FETCH_HEAD`) is already bound by n13/n17/n18 separately. Blind risk ≈ 0; an entry-level
allowlist repair admits the composition for free. Recorded as must-admit, low risk.

## 5. Quantification — the over-refusal surface this population cannot see

A fence can be repaired to `HONEST fixtures=126 admitted=126` while still refusing every state above that the
126 does not hold, because none of those entries appears in any of the 126 built trees (measured 0/126). The
surface:

* **11 classes / 23 store entries refused by the base fence, absent from the population, git-written and
  inside `d`** (each rule measured in isolation, §4): `objects/pack/multi-pack-index` (1);
  `objects/info/commit-graphs/` (1); `config.worktree`+`info/sparse-checkout`+`extensions.worktreeConfig`
  (3); `modules/`+`[submodule]` (2); `MERGE_HEAD`,`MERGE_MSG`,`MERGE_MODE`,`AUTO_MERGE` (4);
  `sharedindex.<sha>` (1); `worktrees/<id>/locked`+`config.worktree` (2); `core.worktree` (1);
  `extensions.objectformat`+64-hex refs+64-hex objects (3); `reftable/`+`extensions.refstorage`+reftable HEAD
  (3); `rr-cache/`+`MERGE_RR` (2). Of those **14 are must-admit, 9 are must-decide**
  (reftable/sha256/core.worktree/rerere).
* **5 entries already admitted but unwitnessed** — `packed-refs` peeled `^`, `pack-*.mtimes`, `pack-*.keep`,
  `pack-*.bitmap`, `logs/refs/tags/<name>`. A repair (or a mutant) that narrows these branches changes no
  verdict. Witnessed: `c1-mut-20-packedref-peel` **survived** the full reference vector (126 honest + 32
  hostile); `.mtimes`/`.bitmap`/`.keep` are admitted once the `objects/info` rules are removed (ladder on the
  plain-`gc`, `repack -b` and `.keep` fixtures, measured ADMIT).
* **3 documented absent classes are unpinnable under the frozen identity policy** — reftable
  (`det=False`: table filename suffix is random, even HEAD presence differed between two builds),
  split-index (`det=False`: `sharedindex.<sha>` follows the mutable index), submodule-as-written
  (`det=False`: `.git/modules/sub/config` records the **absolute** source URL, plus `[remote]`/`[branch]`).
  They cannot be appended to a `tree_sha256`-pinned population without a new mask or a build rewrite (the n21
  gitfile rewrite is the precedent), so the blindness is partly structural, not just sampling.

Ratio: the repair's visible denominator is 13 refused fixtures; the invisible surface is 11 classes / 23
refused entries plus 5 unwitnessed admissions — i.e. **the over-refusal the counter can see is a lower bound
by roughly one order of magnitude in classes**.

## 6. Strongest counterexample

```
$ TMPDIR=… python3 - <<'PY'      # two packs then: git multi-pack-index write
... repo/.git/objects/pack/multi-pack-index exists ...
fence.breach(d, ["--lane","repo"], "anchor") -> 'repo/.git/objects/pack/multi-pack-index is not a pack file'
PY
```

`git multi-pack-index write` is documented (`git-multi-pack-index(1)`, file format in `gitformat-pack(5)`),
writes one file inside `d`, and no fixture in the 126 holds it. A repaired fence that only satisfies the 126
(and the 32 hostile) can print `HONEST fixtures=126 admitted=126` / `PREDICATE R50-C1 pass` while refusing the
repository of anyone who ran multi-pack maintenance. The same holds for a repo left mid-merge (4 entries,
`git-merge(1)` FILES — the single most ordinary transient state), for `git commit-graph write --split` (the
repair is tempted to allow the *name* `objects/info/commit-graph`, which n15 fixes, and still refuse the chain
directory), and for `git sparse-checkout set` (n20 binds `[extensions]` only for `relativeWorktrees`; the
*keys* and `config.worktree` stay unbound).

This is a **fixable defect under the frozen contract**, not a reason to reject C1: the predicate sentence, the
four legs, the literals and the population pin do not change if the S2 fence decides these entries.

## 7. Measured against the landed S3 fence (`6db0279e`, fence `57adce4a…`)

Same probe set, same trees, scored with both fences. Landed counter first:

```
REV 6db0279e2506c1788b26c2586b4d2d774228c6a9
TREE dirty=0
FENCE .../plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f94… mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
MUTANTS total=22 caught=15 broken=0 floor=12 verdict=met
PREDICATE R50-C1 pass
```

**Fixed by the landed repair (measured ADMIT, base refused):** plain `git gc` (`info/refs`,
`objects/info/packs`, `objects/info/commit-graph`, cruft `pack-*.mtimes`); real `git commit-graph write
--split` chain (`objects/info/commit-graphs/`); `refs/notes` (+ its reflog); `refs/replace/<40hex>`;
`logs/refs/tags/<name>`; peeled `packed-refs` `^`. The landed fence also validates commit-graph content: a
synthetic `graph-<40hex>.graph` with junk magic is refused, so only real git-written files pass (a genuine
strength over the base fence, which refused the directory wholesale).

**Still refused by the landed fence** (each probe: plain init+commit plus the one documented entry, or the real
git command; all inside `d`, all git-written, all 0/126 in the population):

| class | measured landed reason |
|---|---|
| `objects/pack/multi-pack-index` (`git multi-pack-index write`; also the real two-pack repo) | `objects/pack/multi-pack-index is not a pack file` |
| `config.worktree` | `config.worktree is not a plain-init entry` |
| `info/sparse-checkout` + `extensions.worktreeConfig` (`git sparse-checkout set`) | `info/sparse-checkout is not a plain .git/info entry`; `config key extensions.worktreeconfig is not allowlisted` |
| `modules/` + `[submodule "…"]` (`git submodule add`) | `config section [submodule "sub"] is not allowlisted` (and `modules is not a plain-init entry`) |
| `MERGE_HEAD`/`MERGE_MSG`/`MERGE_MODE`/`AUTO_MERGE` (left mid-merge) | `AUTO_MERGE is not a plain-init entry` |
| `sharedindex.<40hex>` (`git update-index --split-index`) | `sharedindex.<sha> is not a plain-init entry` |
| `worktrees/<id>/locked`, `worktrees/<id>/config.worktree` | `… is not a worktree-store entry` (the store is now classified; the set is incomplete) |
| `core.worktree` naming an in-`d` work tree | `config key core.worktree is not allowlisted` |
| `extensions.objectformat=sha256` + 64-hex refs/objects | `config key extensions.objectformat is not allowlisted`; `is not a 40-hex ref`; `is not a loose object` |
| `reftable/` + `[extensions] refstorage` (`git init --ref-format=reftable`) | `HEAD is not a branch line or a detached sha` (plus `reftable is not a plain-init entry`) |
| `rr-cache/` + `MERGE_RR` (rerere) | `rr-cache is not a plain-init entry`; `MERGE_RR is not a plain-init entry` |

Counts, landed: of the 11 classes / 23 entries from §5, **1 entry (commit-graph chain) is now admitted; 10
classes / 22 entries remain refused — 13 must-admit and 9 must-decide.** The two may-refuse entries
(`info/grafts`, `info/attributes`) are still refused, correctly under a recorded decision.

**Regression check requested by the repair seat** (their concern: the new `refs/replace` allowance might pass
by absence instead of by the `_refs` allowlist). Measured on the landed fence:

```
refs/replace/<40hex> body "not-a-sha"      -> '../../../…/repo/.git/refs/replace/aaa…a is not a 40-hex ref'
refs/notes/commits body "junk"             -> '../../../…/repo/.git/refs/notes/commits is not a 40-hex ref'
refs/replace/<40hex>/nested (40-hex leaf)  -> None   (admitted: a valid loose-ref layout inside d)
```

The new namespaces are still run through the ref-content allowlist; the regression is **not** present in
`57adce4a`. `refs/replace/<40hex>/nested` is admitted, which is defensible (inside `d`, valid 40-hex leaf);
record it as a decided shape rather than a defect.

## Impacted axes

* **novelty (C1, 7→8)** — primary. The instrument's honest leg is a 126-sample of a 38-entry documented
  surface; `admitted=126` is a statement about the sample. Without a coverage bound the "honest geometry"
  claim reads as "admits the documented store shapes", which is measured false for 10 classes on the landed
  fence (§7). The novelty gain survives if the limit is stated and the remaining entries are decided; it does
  not survive being presented as full coverage.
* **quality** — the mutant floor's sensitivity is exactly the population's sensitivity. Frozen kills must not
  be claimed for the peeled/`mtimes`/`keep`/`bitmap` branches (Q38: witness, don't assume; `mut-20` survives).
* **coverage** — untouched (operator-capped; not claimed).

## Smallest safe correction

1. **Fence, entry-by-entry against the doc, not against the 126.** S3 fixed the chain and the four ref/store
   shapes it names; **13 must-admit entries remain refused on the landed fence** (MPI; `config.worktree`;
   `info/sparse-checkout` + `extensions.worktreeConfig`; `modules/`; `[submodule]`; the four merge-state
   files; `sharedindex.<sha>`; `worktrees/<id>/{locked,config.worktree}`). Each is a scratch probe of seconds
   (§4/§7) — an S4 allowlist widening, or a recorded exclusion if the lane knowingly refuses them.
2. **Record a decided exclusion for the 9 must-decide entries**, in the claims' own commondir style
   ("recorded as a decided exclusion, not an unknown"), each with its doc pointer and the reason: `reftable`
   and `sha256` are backend-level (their stores cannot be classified by a name allowlist; refusing is
   containment-safe), `core.worktree` is value-dependent (must refuse out-of-`d`, so a name-based rule is only
   defensible when stated), `rr-cache`/`MERGE_RR` are rerere-opt-in state. Silence here is the defect;
   refusal with a recorded reason is not. If `worktrees/` is admitted as a directory, decide whether
   `worktrees/<id>/{gitdir,commondir,locked,config.worktree}` are classified or knowingly accepted — no
   fixture witnesses either choice.
3. **State the coverage bound in the claims' `## Named limits`** (L1 owns the claims file): the frozen 126
   holds 25 of the 38 `gitrepository-layout(5)` entries, and lists the 11 classes / 23 entries this census
   refuses plus the 5 unwitnessed admissions. The predicate sentence, the four leg names, the literals `126`/`20`/`12`/`SEALED50_MIN` and the
   population pin stay untouched — this is a limit statement, not a fixture addition (the pin forbids one).
4. **Mutant battery (S2, CANDIDATE re-derivation)**: do not freeze rows on the peeled/`mtimes`/`keep`/`bitmap`
   branches — they cannot be witnessed by this vector (`mut-20` survived). If the S2 fence widens those
   branches, a witnessed kill needs a *new* fixture, which the pin forbids; record them as unexercised.
5. **Two receipt fixes in the counter** (open-window, instrument repairs, measured defects): print all
   refusals (drop `[:12]`, currently hides `n08-tag-detached`), and `mkdir` the `--work` parent instead of
   crashing with `FileNotFoundError`.

Not corrections: `info/grafts` (git only reads it), `info/attributes`, `info/http-alternates`, legacy
`branches/`/`remotes/`, enabled hooks, `git lfs install` state — refusal is defensible; each needs its
decision written down, not a fixture.

## Limits

* Read-only clone of the lane at `3b02d573…`; the live checkout was never written. Probes are scratch-only and
  never committed.
* §1–§6 were measured against the base fence `05d5fe03…` (no repair existed at `3b02d573…`/`822f3b7`); §7 was
  measured against the landed S3 fence `57adce4a…` at `6db0279e`. Every verdict is reproducible by
  re-running the same git commands; probe fixtures are single-build witnesses except where `det` is reported
  (two builds, `tree_identity`).
* The ladder in §4 is diagnostic: it deletes the entry the current reason names, so ladder length is a count of
  independent rules on one state, not a git-pure fixture.
* Host facts: git 2.56.0, `gitrepository-layout(5)` dated 2026-09-27, `git-lfs 3.8.0`. `gc.cruftPacks` unset
  and plain `git gc` writes `pack-*.mtimes` (measured); `feature.manyFiles=true git gc` did **not** write a
  multi-pack-index here, so MPI is claimed only for `git multi-pack-index write` / incremental-repack.
* Scratch dir `/fast/scratch/hyaku/kengaku-r50/R50C1CritPopScope` removed before yield; receipts are the
  verbatim blocks above (citable in this report only).

VERDICT (landed state, `6db0279e` / fence `57adce4a…`): the predicate passes and the landed repair is real —
`HONEST 126/126`, 20/20 refusals, 30/30 sealed, 22 mutants/15 caught, `refs/replace` and `refs/notes` still
run through the 40-hex ref allowlist, commit-graph content is validated. But the honest leg's denominator is
still the frozen 126, so **10 documented git-written classes / 22 entries remain refused by the landed fence
with nothing in the instrument able to see it** (13 must-admit, 9 must-decide; measured in §7), and 5 admitted
branches stay unwitnessed. C1 must present `admitted=126` as a sample statement plus a coverage-bound row in
`## Named limits`; the remaining entries are an S4 decision, not a predicate failure.

VERDICT (base-fence measurement, §1–§6): **C1's honest leg is a bounded sample, and the bound is measurable.** Reproduced base state
`126/113/13`; the base fence's refusal set is 13 fixtures in 13 classes (not five). The frozen population holds
25 of 38 `gitrepository-layout(5)` entries and 0 of 11 documented git-written classes that the base fence
refuses (23 entries, each rule measured in isolation), plus 5 already-admitted-but-unwitnessed entries
(`c1-mut-20-packedref-peel` survived as witness) and 3 classes unpinnable under the current identity policy
(reftable, split-index, submodule-as-written). A repair can reach `HONEST admitted=126` / `PREDICATE pass`
while still refusing multi-pack-index repos, mid-merge repos, split commit-graphs, sparse-checkout, submodules,
split-index, sha256 and reftable stores. This is fixable in S2 without touching the predicate, the legs, the
literals or the population pin: decide the 23 entries entry-by-entry (14 admit / 9 recorded exclusions), state
the coverage bound in `## Named limits`, and do not freeze mutant kills on the five unexercised allowlist
branches.
