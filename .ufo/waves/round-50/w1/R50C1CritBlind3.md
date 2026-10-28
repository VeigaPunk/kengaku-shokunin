# R50C1CritBlind3 — two blind hostile modules for the R50-C1 `SEALED` leg

REV `c3372a9b24d3a200946a6b37dc0a31ed5c982cc1` (lane `kengaku-shokunin`, tip when this seat ran) — the four
instrument files this seat used are **byte-identical** to their blobs at the stage-1 freeze
`3b02d573d58cc6d2e0d27ef92ac0815354912252` (verified in "Revision" below), so every measurement is of the frozen
instrument content, not of a later tree.

VERDICT: **delivered, with two findings the integration owner must act on.** Both assigned blind modules exist,
build under the round-44 builder contract, and are refused by the base fence. Each one is the *unique*
discriminator for a specific repair move that the frozen honest leg forces (measured: shape-only repair leaks
`b1`, misordered repair leaks `b2`). A third hole opened by the same repair is measured and is **not** one of my
two deliverables: containment checked per repository is not enough — the alternates borrow graph must be walked
(receipt `receipts/verdict-matrix.json`, column `ctl-chain`).

## Axes named

| axis | how this seat touches it |
|---|---|
| **novelty** (R50-C1, 7 → 8) | primary. These are the first sealed modules whose hostile property is *induced by the repair the honest leg demands*, not a legacy escape: `refs/replace` (`n17`), `objects/info/alternates` (`n22`), `.git/FETCH_HEAD` (`n18`). Without them the `SEALED leaked=0` line says nothing about the three new code paths the repair must add. |
| C1 predicate integrity (honesty of `SEALED leaked=0`) | measured counterexample: two plausible repairs reach `SEALED leaked=0` on the 12 frozen modules while admitting an outside-`d` read. |
| coverage (not claimed this round) | `SEALED` gains discrimination on three newly-admitted names; the count contribution is 2 of `SEALED50_MIN=6`. |

Not touched: no production file, no `SCORECARD.md`/`LOG.md`/`corpus/`, no commit, no claim of C1/C2 admission.

## Deliverables (blind, hostile, sealed)

Both live under the assigned path and are handed over as files, not as prose.

| file | sha256 | fid | tool |
|---|---|---|---|
| `C1CritBlind3/sealed/b1_replace_ref_target_outside_store.py` | `34354116e3c11fbf5b12be1dad8f5869fefddbec8fdf2dc0ee2be535457ae6c4` | `b1-replace-target-outside-store` | `anchor` |
| `C1CritBlind3/sealed/b2_fetch_head_hardlink_out.py` | `6a15228b050b18b31be3f9ebaa1f465893467e2a190bd1427c0a13e787c3c3a9` | `b2-fetch-head-hardlink-out` | `anchor` |

(`receipts/module.sha256`. Both are one-fixture modules, so `SEALED clean` requires exactly one `BREACH` each.)

**b1 — `refs/replace/<40hex>` whose target object lives in an outside store borrowed through alternates.** Inside
`d`: `lane/` (two commits), `lane/.git/refs/replace/<ORIG>` → `<TARGET>` written by `git replace`, and
`lane/.git/objects/info/alternates` = `../../../../outside-store/.git/objects`. `outside-store/` is a second
repository in the build root, **outside `d`**, whose HEAD is `<TARGET>`. The entry is **relative**, so a repair
that rejects only absolute alternates paths still leaks it.

**b2 — `.git/FETCH_HEAD` as a hardlink to a file outside `d`.** `lane/.git/FETCH_HEAD` is a regular file with
`st_nlink == 2`, canonical content `<H>\t\tbranch 'master' of ../src\n`; its second name is
`<build>/fetch-head-store`, outside `d`.

## Witnesses (measured, `receipts/witness.json`)

b1 — the replace target is only reachable through the outside store:

```
b1_alternates_entry            = '../../../../outside-store/.git/objects'
b1_alternates_resolves_to      = '/fast/scratch/…/gen/b1/outside-store/.git/objects'
b1_alternates_inside_d         = False
b1_target                      = '72850be5f5b9b23afbbe39f7c232a26f66c9e84f'
b1_target_loose_inside_d       = False
b1_pack_dir_entries            = []
b1_target_loose_outside        = True
b1_cat_file_type               = 'commit'          # `git -C lane cat-file -t <TARGET>`
b1_cat_file_without_alternates_rc = 128            # same command with the alternates entry removed
b1_fsck_rc                     = 0                 # the state is git-consistent from inside d
b1_strace_outside_open_count   = 9                 # path refs under outside-store while resolving <TARGET>
```

The nine strace references include `…/outside-store/.git/objects/72/850be5…` — the replaced commit's loose
object file. So the escape is a genuine read of object bytes outside `d`, and it is invisible to every lexical
path check on the fixture's own files.

b2 — the bytes `d` reads have a name outside `d` (store-identity escape, the `f16` class moved onto a top-level
file):

```
b2_nlink = 2    b2_inode = 1879085898    b2_second_inode = 1879085898    b2_size = 68
b2_second_name_inside_d = False
b2_content              = "e6194a5fc75a12d9135ae7b7ec2c24ac92e1edf3\t\tbranch 'master' of ../src\n"
b2_rev_parse_fetch_head = 'e6194a5fc75a12d9135ae7b7ec2c24ac92e1edf3'
b2_read_inside_d_after_outside_write = "MUTATED THROUGH THE OUTSIDE NAME\n"
```

The last line is the escape: writing the outside name changes what the file inside `d` says. This module is a
*pointer* escape, not an outside `open` — no path outside `d` is ever opened, which is why it must be judged by
link identity (`nlink > 1`), and why `plans/round46_c1_verify.py` (the outside-open counter) cannot see it.

## Verdict matrix (measured, `receipts/verdict-matrix.json`)

Four candidate repairs were generated from the base fence by explicit text surgery (diffs in `receipts/`); the
columns `n17`, `n22` are the frozen honest fixtures, and the three `ctl-*` columns are scratch controls.

```
fence             b1        b2        n17       n22       ctl-fetch-plain  ctl-chain  ctl-replace-in-alt
base (05d5fe03…)  BREACH    BREACH    BREACH    BREACH    BREACH           BREACH     BREACH
p1-shape-only     ADMIT     BREACH    ADMIT     ADMIT     BREACH           ADMIT      ADMIT
p2-narrow-link    BREACH    ADMIT     BREACH    BREACH    ADMIT            BREACH     BREACH
p3-scoped-fix     BREACH    BREACH    ADMIT     ADMIT     ADMIT            ADMIT      ADMIT
p4-graph-fix      BREACH    BREACH    ADMIT     ADMIT     ADMIT            BREACH     ADMIT
```

| candidate | sha256 | what it does |
|---|---|---|
| `base` | `05d5fe03aa3b…8aad5e` | the fence under test, unchanged |
| `p1-shape-only` | `4a26cbe0ed5e3969cac661c866808e45d580b5f85f86011a96158ff8ce9d4996` | allow `refs/replace` (40-hex name/body) and allow an alternates entry that merely names an existing directory |
| `p2-narrow-link` | `0f9642b8be88e43330f95e40aec91822f967d3b6096f56616b9b27f7209927b1` | add `FETCH_HEAD`/`shallow` to the admitted names, with the shape branch placed **ahead** of `_store`'s `_linked()` test |
| `p3-scoped-fix` | `e010b6630425dc0f5008c616963a435bfcd74cb039117e69abeedef29ecfa36e` | p1 + every alternates entry must resolve inside `d`; `FETCH_HEAD`/`shallow` admitted **after** `_linked()` |
| `p4-graph-fix` | `6ecc6340a8ae06dc2e434c2e3ad884e1ff092603779783ccce01c2aa0b041138` | p3 + the alternates *borrow graph* is walked (visited set, depth cap 8) |

Reading of the matrix, which is the whole point of the seat:

* `b1` is the only column that `p1` admits and `p3` refuses. `p1` is what a repair looks like when it satisfies
  `n17` and `n22` by shape alone: it says `ADMIT` to a fixture whose object bytes are outside `d`.
* `b2` is the only column that `p2` admits and `p3` refuses. `p2` differs from `p3` in *one* respect — where the
  new name branch sits relative to `_linked()`.
* `ctl-fetch-plain` (identical bytes, one link) is `ADMIT` under `p2`/`p3`/`p4`, so `b2`'s refusal is a
  discrimination, not a blanket refusal of `FETCH_HEAD`.
* `ctl-replace-in-alt` (honest: alternates **inside** `d`, replace target only in that in-d store) is `ADMIT`
  under `p3`/`p4` and witness-verified: `alt_in_d_target_in_lane_own_store = False`,
  `alt_in_d_target_in_main_store = True`, `alt_in_d_cat_file_type = 'commit'`. `p1` also admits it — p1 cannot
  tell the honest and the hostile replace fixture apart; only containment can.
* `base` refuses all seven, which reproduces the claims' `HONEST refused=13` composition: `n17`, `n18`, `n20`,
  `n21`, `n22` are all over-refused by the fence under test.

### Base-fence refusal reasons (verbatim)

```
base  b1                 lane/.git/objects/info/alternates present (object-store redirect)
base  b2                 lane/.git/FETCH_HEAD is not a plain-init entry
base  n17                repo/.git/refs/replace is not refs/heads or refs/tags
base  n22                lane/.git/objects/info/alternates present (object-store redirect)
```

Note what `b2`'s base reason means, because it changes the module's role: `_tree` never descends into a `.git`
directory, so the `nlink > 1` rule of `_tree` **does not see `.git/FETCH_HEAD`**; the only link test that could
is `_store`'s `_linked()`, and it sits after `if name not in GIT_TOP`. The base fence therefore refuses `b2` by
*name*, not by link identity. There is no pre-existing property to regress: once the repair adds the name, the
position of that test is the only thing that refuses the fixture. That is exactly what `p2` shows.

## Counterexample (strongest available from local evidence)

Take the honest leg seriously and repair the fence the cheap way (`p1`): `SEALED leaked=0` and
`HONEST admitted=126` can both hold while an admitted fixture's git store reads
`<build>/outside-store/.git/objects/72/850be5…` — nine strace references outside `d`, and `cat-file` fails with
rc 128 the moment the alternates entry is removed (`receipts/witness.json`). The predicate as frozen cannot see
this: it records `ADMIT`/`BREACH`, not *why*. Two consequences the L1 should carry into S2:

1. the `SEALED` leg is only as strong as its module set, and the 12 frozen modules do not cover any of the three
   names the repair must add;
2. a *reason*-blind predicate means a repair that refuses `refs/replace` and alternates outright would also read
   `SEALED leaked=0` — the honest leg (`n17`, `n22`) is the only thing that separates "correct" from "refuses
   everything new". Both facts are visible in my matrix, which is why the honest columns are in it.

Second counterexample (not one of my deliverables, measured for the repair's benefit): `ctl-chain`
(`receipts/candidate-b3-alternates-chain.py`) has `lane/.git/objects/info/alternates = ../../../store/objects`
(**inside** `d`) where `store/` is a plain directory that is not a repository
(`chain_store_is_a_repo = False`), and `store/objects/info/alternates = ../../../far-store/.git/objects`
(outside `d`). `p3` admits it (`ADMIT`); resolution still reaches `far-store/.git/objects/88/fc999…` outside `d`
(9 strace references), because git follows the borrow graph recursively. `p4` refuses it.

## Impacted axes

* **novelty (C1)** — positively: the sealed set now constrains the three new code paths, which is the part of C1
  that "one command, four legs, one predicate" is supposed to buy. A repair that passes `HONEST 126/126` and
  still reads outside `d` would otherwise score novelty 8 on an untrue instrument.
* **C1 predicate integrity** — the `SEALED` count alone cannot carry it (see counterexample); the frozen
  predicate sentence stays untouched, so nothing in this seat redefines `SEALED50_MIN` or the kill rule.
* **coverage** — unchanged; campaign count contribution 2/6 toward `SEALED50_MIN`, no claim made here.

## Smallest safe correction (for the S2 repair, not applied by this seat)

Three rules, each the smallest thing that closes one measured leak and none of them over-refusing a git-writable
state (all three are implemented in `p4-graph-fix`, `receipts/diff-p4-graph-fix.patch`, and pass the honest
columns):

1. **alternates containment, on the whole borrow graph.** Admit `objects/info/alternates` only when every entry
   resolves (normpath against the *objects* directory that holds the file, no symlink following) inside `d`, and
   re-apply the same rule to each alternate's own `info/alternates`, with a visited set and a depth cap. Two
   details are load-bearing and both are measured failures: anchoring the resolution to `objects/info` instead of
   `objects` refuses the honest `n22` (`p1`'s first real draft, discarded); checking only the repositories
   `_tree` finds admits `ctl-chain`, because an alternate need not be a repository.
2. **`refs/replace/<40hex>`: name shape and body shape only.** Do not resolve the target. Once rule 1 proves the
   borrow graph inside `d`, a resolvable target is inside `d` by construction. Do **not** add "the target must
   exist in this repository's own loose objects or pack": that refuses `ctl-replace-in-alt`, a state `git replace`
   itself writes, because the target legitimately lives in an in-`d` alternate
   (`alt_in_d_target_in_lane_own_store = False`, measured).
3. **`FETCH_HEAD` / `shallow`: add the names after the generic tests, not before.** The new branch must sit
   *after* `_store`'s regular-file and `_linked()` checks (and `_tree`'s link rule must not be narrowed to
   `objects/`). `p2` differs from `p3` in nothing else and admits `b2`.

If the L1 wants the chain hazard inside the frozen `SEALED` leg, `receipts/candidate-b3-alternates-chain.py` is a
ready module — but adding it is a decision outside this seat's item (it is not in `sealed/`, so it cannot be
mistaken for one of the two deliverables), and the count is already satisfied by ≥4 further blind modules.

## Integration receipt (the modules as the counter consumes them)

Two modules copied into a scratch clone's `plans/sealed50/` (nothing written to the lane), then the frozen
counter, verbatim (`receipts/counter-base-fence-with-blind-modules.txt`):

```
REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
TREE dirty=1
FENCE /fast/scratch/hyaku/kengaku-r50/R50C1CritBlind3/lane-c1/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
HONEST-REFUSED n12-local-config-user repo/.git/config section [user] is not allowlisted
HONEST-REFUSED n13-remote-origin repo/.git/config section header b'[remote "origin"]' is not plain
HONEST-REFUSED n14-stash-entry ../../../../integration/k50-c1-0ywg32cc/honest/m026-plans-honest50-modules-novel48-n14_stash_entry/f000/repo/.git/logs/refs/stash has a name git does not write
HONEST-REFUSED n15-commit-graph repo/.git/objects/info/commit-graph present (object-store redirect)
HONEST-REFUSED n16-notes-ref ../../../../integration/k50-c1-0ywg32cc/honest/m028-plans-honest50-modules-novel48-n16_notes_ref/f000/repo/.git/logs/refs/notes has a name git does not write
HONEST-REFUSED n17-replace-ref repo/.git/refs/replace is not refs/heads or refs/tags
HONEST-REFUSED n18-shallow-fetch repo/.git/FETCH_HEAD is not a plain-init entry
HONEST-REFUSED n20-linked-worktree wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n21-separate-gitdir wt/.git is a file (gitdir redirect), not a directory
HONEST-REFUSED n22-alternates-in-d lane/.git/objects/info/alternates present (object-store redirect)
HONEST-REFUSED n03-detached-head repo/.git/HEAD is not a plain branch HEAD
HONEST-REFUSED n07-reflog-gc repo/.git/info/refs is not git's exclude file
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=2 clean=2 leaked=0 build_errors=0
SEALED50-TOTAL 2 expected_min=6
PREDICATE R50-C1 fail
```

What this pins: both modules build under the counter's own builder with `build_errors=0`, and the base fence
refuses both (`SEALED total=2 clean=2 leaked=0`). `PREDICATE fail` is expected and correct here — the only failing
condition is `SEALED50-TOTAL 2 expected_min=6` (four blind modules short), plus the base fence's honest leg. The
run also reproduces the frozen stage-1 counters exactly (`HONEST 126/113/13`, `REFUSALS 20/20`, `SEALED46 12/12`),
independently of the stage-1 receipts.

While this seat ran, the integration owner created the production `plans/sealed50/` and copied both deliverables
into it; the copies are byte-identical to the files delivered here
(`34354116e3c11fbf5b12be1dad8f5869fefddbec8fdf2dc0ee2be535457ae6c4`,
`6a15228b050b18b31be3f9ebaa1f465893467e2a190bd1427c0a13e787c3c3a9`). That write is the integrator's, not this
seat's: `SEALED50_MIN=6` is therefore satisfiable without further authorship from me, and the `SEALED` leg of the
S3 run will exercise `b1` and `b2` as delivered.

## Post-yield: the two modules measured against the lane's uncommitted repair (`57adce4a`)

While this seat ran, a repair appeared **uncommitted in the lane working tree** (`plans/fixture_fence.py`,
sha256 `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`, 533+/117- vs the frozen
`05d5fe03…`). Since my modules exist to constrain exactly that file, I snapshotted it read-only into scratch and
re-ran the fixtures against it. Receipt:
`receipts/verdicts-against-lane-repair-57adce4a.json` (sha256 `b5a9e7fd83ee39aa618ae5550703a787a31bb218c54ee56d096400bed0d820ff`).

```
fence            b1      b2      ctl-chain  ctl-fetch-plain  ctl-replace-in-alt  n17    n22    p-junk-branch  p-replace-body-junk  p-stray-ref-ns
base-05d5fe03    BREACH  BREACH  BREACH     BREACH           BREACH              BREACH BREACH BREACH         BREACH               BREACH
lane-57adce4a    BREACH  BREACH  BREACH     ADMIT            ADMIT               ADMIT  ADMIT  BREACH         BREACH               BREACH
```

Verbatim reasons on the lane version:

```
b1          lane/.git/objects/info/alternates names a store outside the fixture
b2          lane/.git/FETCH_HEAD has more than one hard link
ctl-chain   store/objects/info/alternates names a store outside the fixture
n17         ADMIT      n22         ADMIT      ctl-fetch-plain  ADMIT      ctl-replace-in-alt  ADMIT
```

So **all three hazards this seat measured are closed in `57adce4a`, and all four honest partners stay admitted** —
including the chain fixture, whose second-level alternate lives in a directory that is not a repository, so the
lane version is walking the borrow graph rather than checking repositories only. My `p1`/`p2` leaks are therefore
*not* live against this snapshot.

`_refs` liveness (the R50C1ExecRepair finding — `n17` passing by absence rather than by the allowlist): three
targeted probes, all `BREACH` on the lane version, so `_refs` is still called with its namespace and body rules
intact:

```
p-junk-branch        refs/heads/junk-branch is not a 40-hex ref
p-replace-body-junk  refs/replace/<40hex> is not a 40-hex ref        # name right, body junk -> refused
p-stray-ref-ns       refs/foo is not a ref namespace git writes
```

Limits of this section, to keep it honest: it is a snapshot of an **uncommitted, concurrently edited** file (the
digest is the attribution — if `plans/fixture_fence.py` changes again, this section does not describe it); it
covers 10 fixtures, not the 126-row honest population, so it says nothing about `HONEST 126/126`; and it does not
touch the mutant battery (`MUTANTS` floor is still R50C1ExecRepair's open item).

## Revision and lineage (why the measured tree is the frozen one)

```
$ git -C <lane> rev-parse HEAD
c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
$ git -C <lane> merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD   # exit 0
$ sha256sum plans/fixture_fence.py plans/round50_c1_verify.py plans/honest50/population.txt
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  plans/fixture_fence.py
d8787b34b0e0964edab9f117e63e5d4865c749eb5be8bcde3d39ef831f4a69e2  plans/round50_c1_verify.py
b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69  plans/honest50/population.txt
$ git -C <lane> diff --stat 3b02d573… c3372a9b… -- plans/
 plans/round-50-claims.md   | 6 ++++++
 plans/round50_c1_verify.py | 4 ++--
```

The clone (`git clone --shared`, scratch) sits at the tip, not at `3b02d573`, because a `git checkout` is a
mutating command this seat is not allowed to run. Instead of checking the freeze out, I proved content identity:
for the four files this seat used, the worktree bytes equal the `3b02d573:<path>` blobs
(`plans/fixture_fence.py` `05d5fe03…`, `plans/honest50/build_honest_population.py` `35e3de60…`,
`plans/round44_c1_verify.py` `6cf05323…`, `plans/honest50/population.txt` `b5197f94…`; all four `MATCH`). The only
`plans/` difference between the freeze and the tip is the counter's documented open-window repair
(`f9b9873e…` → `d8787b34…`, recorded in the claims table) and the claims table itself. So the fence, the
population, the builder and the counter are the frozen instruments.

## Commands run (exact)

```
git -C <lane> rev-parse HEAD ; git -C <lane> merge-base --is-ancestor 3b02d573… HEAD
git -C <lane> diff --stat 3b02d573… c3372a9b… -- plans/ ; git -C <lane> status --porcelain
sha256sum plans/fixture_fence.py plans/round50_c1_verify.py plans/honest50/population.txt
git clone --shared --quiet <lane> /fast/scratch/hyaku/kengaku-r50/R50C1CritBlind3/lane-c1
  # then, per instrument: git cat-file -p 3b02d573:<path> | sha256sum  vs  sha256sum <worktree path>
# fixture-behaviour prototypes (plain git, scratch dirs proto1/proto2/proto3, env per command, no exported
# GIT_CONFIG_*): git init / add / commit / replace / cat-file / fsck / rev-parse ; stat ; ln ; strace
TMPDIR=/fast/scratch/…/R50C1CritBlind3 python3 /fast/scratch/…/R50C1CritBlind3/drive.py
  # -> receipts/witness.json, receipts/diff-p*.patch, receipts/verdict-matrix.json
cp C1CritBlind3/sealed/*.py <clone>/plans/sealed50/
TMPDIR=<scratch> python3 plans/round50_c1_verify.py --lane . --skip-mutants --allow-dirty --work <scratch>/integration
```

All fixture git calls ran with `-C <dir>` inside the scratch root and with `env` per command; no `GIT_CONFIG_*`,
no `GIT_AUTHOR_*`/`GIT_COMMITTER_*` was exported into any shell. No mutating git command was run in the lane or
any sibling repo; the only mutation of my scratch clone was adding the untracked `plans/sealed50/` used for the
integration run.

## Limits

1. **The predicate is reason-blind.** `SEALED` records `ADMIT`/`BREACH`, not the refusal reason, so these modules
   constrain the verdict vector, not the mechanism. A repair that refuses `refs/replace` and alternates outright
   still passes them; only the honest leg (`n17`, `n22`) rejects that. This is a property of the frozen counter,
   not something a module can fix.
2. **Both modules are strict on the repaired fence, not leaks of the base fence.** The base fence refuses both
   (measured above), and `b2` is refused by *name*, not by link identity — so `b2`'s trap fires only along the
   new `FETCH_HEAD` path. That is the honest reading of their value: regression guards on the S2 repair.
3. `b2` is a store-identity escape, not an outside `open`: the round-46 outside-open counter cannot see it, and
   neither can any string scan of path values inside `d`.
4. Observed surfaces only: no io_uring, no host paths outside the scratch root, no claim that these are the only
   shapes the repair can leak. `b1` and `b2` cover the three names the S2 repair must add; `ctl-chain` shows one
   more (borrow-graph depth) and is not a deliverable.
5. The fixtures are not identity-pinned and not in the population — they are hostile modules, so host-sensitive
   git output cannot silently change the predicate; conversely, they contribute nothing to `POPULATION`.
6. The lane tree changed under this seat while it ran: `M corpus/QUALITY.md` was already dirty before my first
   command, and `M plans/mutants50/c1-mutants.json`, `?? plans/sealed50/`, then a large uncommitted
   `plans/fixture_fence.py` repair and edits to `plans/round50_c1_verify.py`/`SCORECARD.md`/`LOG.md` appeared
   afterwards. None of those are mine; I wrote no lane file. Everything in this report other than the explicitly
   labelled `57adce4a` section is bound to REV `c3372a9b…`, where the counter was `d8787b34…` — if the current
   lane counter has a different digest, the run quoted above still describes the tree I measured.
7. `p1`..`p4` are scratch prototypes written to *measure* the modules. They are not a proposed patch, and the
   `d` plumbing they add (`_objects(p, label, d)`, `_store(gd, label, d)`) is one shape of several.

## Scratch

`/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind3` — removed at the end of this seat; all receipts were copied
into `C1CritBlind3/receipts/` first. Files in this seat's wave dir:

```
sealed/  b1_replace_ref_target_outside_store.py  b2_fetch_head_hardlink_out.py
receipts/ module.sha256  witness.json  verdict-matrix.json
          counter-base-fence-with-blind-modules.txt
          diff-p1-shape-only.patch  diff-p2-narrow-link.patch  diff-p3-scoped-fix.patch  diff-p4-graph-fix.patch
          control-fetch-head-plain.py  control-replace-target-in-d-alternate.py
          candidate-b3-alternates-chain.py
```

Impacted axes: novelty (primary), C1 predicate integrity, coverage (count only). Counterexample: shape-only
repair admits an outside-`d` object read. Smallest safe correction: three rules above, implemented and measured
in `p4-graph-fix`.

VERDICT: **two blind modules delivered and integrated (`SEALED total=2 clean=2 leaked=0 build_errors=0` on the
base fence); both are live traps for the S2 repair (`p1` leaks `b1`, `p2` leaks `b2`); one additional repair hole
measured and handed over as `candidate-b3`, not as a deliverable.**
