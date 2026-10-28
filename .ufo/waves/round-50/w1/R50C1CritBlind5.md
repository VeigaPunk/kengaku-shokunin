# R50C1CritBlind5 — two blind hostile modules for the R50-C1 instrument

Seat: critic, serving **R50-C1 (novelty)**. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Item: author TWO blind hostile modules — (i) an honest-looking repo with an extra
`.git/objects/info/alternates` **chain A→B where B is outside `d`**, (ii) a linked worktree whose
**`commondir` points outside `d` while its own gitdir is inside**. Under `C1CritBlind5/sealed/`.

## Axes named

- **novelty (R50-C1)** — the two modules are held-out hostile geometry for the *widening* the C1 repair must make
  so the honest in-`d` indirection classes (`n20` linked worktree, `n21` separate gitdir, `n22` alternates-in-d)
  are admitted. They score that repair on the property it claims (no read outside `d`), not on the shape of the
  first file it inspects.
- Coverage: not touched (operator-capped L0). Calibration (R50-C2): not touched — no artefact pointer was added,
  removed or rewritten.

## Revision measured

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
```

`git merge-base --is-ancestor 3b02d573… HEAD` → `FREEZE_ANCESTOR_OK`; lane tip at measurement time
`c3372a9b24d3a200946a6b37dc0a31ed5c982cc1`. Every fixture was built and every fence verdict taken from a
`git clone --shared` of the lane checked out at the freeze commit, never from the live checkout. Fence under test:
`plans/fixture_fence.py` sha256 `05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`.

An additional, non-authoritative measurement was taken against the in-flight repair candidate that sits in this
wave directory: `.ufo/waves/round-50/w1/C1ExecRepair/fence_candidate.py`. It moved while this seat measured —
`6df6a2a331a66195cfeb963b457372596cd55ac1199d7d97027323a533a76ec2` at 14:33 then
`9baedf1379b6de5cecce629a3fceaeb8d2b99371d34b64d0ecd397d15a3c4ec1` at 14:36 (the digest its own author reports).
Both digests were measured separately; both return the identical verdict and the identical reason string on both
of my modules, so the seat's finding does not depend on which one is current. That run is a critique of a
proposal, nothing more; the judged fence is whatever S2 commits.

Separately, the lane's own working-tree `plans/fixture_fence.py` became `57adce4a…` at 14:36 (see below). The two
repair texts are not stackable — the candidate is the five mechanisms its author's item names, the lane file adds
a mount/device-boundary leg, detached-HEAD acceptance and commit-graph/info-refs allowances — and neither was
measured in the other's presence. Nothing in this seat's evidence mixes them: every number below names its digest.

## Deliverable

Installed at `.ufo/waves/round-50/w1/C1CritBlind5/sealed/` — the integrator copies these two files into
`plans/sealed50/` verbatim (they are the only two files this seat authored; both are self-contained, single
fixture, tool `anchor`):

| file | sha256 | fid | tool | argv |
|---|---|---|---|---|
| `h_alternates_chain.py` | `35286a7076194a55ee66671d6120c8a9cf4a1316b690fe4c3f2fb82588f78bd4` | `bl5-alternates-chain-out` | `anchor` | `--lane lane` |
| `h_wt_commondir_out.py` | `3e3ec5b6bcd2a5fb5dc1f72fc70fe6195382359a09d511179201d78fdbe5889d` | `bl5-wt-commondir-out` | `anchor` | `--lane wt` |

Names collide with nothing in `plans/sealed46/` (`a_*`, `c_*`, `p_*`, `s_*`) or `plans/refusals46/` (`f1…f20`).
With these two installed `plans/sealed50/` holds 2 modules, so the counter's `SEALED50_MIN` (6) is not yet met by
this seat alone — that is the L1's composition problem, reported below as observed, not as a defect of the modules.

### `h_alternates_chain.py`

```python
"""Sealed blind hostile module A — round-50 wave-1 seat `R50C1CritBlind5` (critic, R50-C1).

Attack class: **an alternates CHAIN whose second hop leaves `d`.**

    lane/.git/objects/info/alternates  ->  ../../../mid/.git/objects      (resolves INSIDE d)
    mid/.git/objects/info/alternates   ->  ../../../../chain-out/.git/objects   (resolves OUTSIDE d)

`lane` is an ordinary one-commit repository; its own alternates entry names an object store that is inside the
fixture, exactly the shape the round-50 honest class `n22_alternates_in_d` declares honest. The escape is one
hop deeper: `mid` itself borrows from `d.parent/chain-out`, so `git` resolves `lane`'s history through
`mid`'s objects and then through `chain-out`'s objects, and `chain-out` is NOT under `d`.

Why this is the blind hostile counterpart of the repair (not of the base fence). The round-50 repair must widen
the store allowlist so `n22` (a single in-`d` alternates entry) is admitted; the tempting widening is "admit an
`alternates` file whose direct target resolves inside `d`". That rule admits `n22` **and** this module: the
direct target here is inside `d`. Only a repair that resolves the chain transitively (git follows nested
`alternates`, up to its own depth limit) and requires *every* hop inside `d` refuses it. So the module scores a
repair by the property it claims (no read outside `d`), not by the shape of the first line it sees.

Measured on the base fence `05d5fe03…`: BREACH, reason `objects/info/alternates present (object-store
redirect)` — the base fence refuses this class by the same blanket rule that over-refuses honest `n22`, so that
refusal carries no information about the repair. Real-git witness (seat receipt): `git -C lane cat-file -p
<chain-out commit>:b-only.txt` prints `outside bytes` while no object of that commit exists anywhere under `d`;
moving `chain-out` away makes the same read fail with `unable to normalize alternate object path` naming the
resolved outside path.

Determinism: every entry is a relative path resolved against the object database directory git resolves it
against, so no build-scratch absolute path enters the tree; the two ordinary repos are plain `git init` +
commits. Round-44 builder contract: `build(ctx, d)` fills `d` and returns the argv tail. `expect` is this
seat's statement of the required verdict (`breach`); the round-50 counter reads only `fid`/`tool`/`build`.
"""


def build(ctx, d):
    out = ctx.init(d.parent / "chain-out")
    ctx.write(out / "b-only.txt", "outside bytes\n")
    ctx.git(out, "add", "-A")
    ctx.git(out, "commit", "-qm", "out")
    mid = ctx.init(d / "mid")
    ctx.write(mid / "mid.txt", "mid\n")
    ctx.git(mid, "add", "-A")
    ctx.git(mid, "commit", "-qm", "mid")
    lane = ctx.init(d / "lane")
    ctx.write(lane / "lane.txt", "lane\n")
    ctx.git(lane, "add", "-A")
    ctx.git(lane, "commit", "-qm", "lane")
    # hop 1: inside d (the shape honest n22 declares honest); hop 2: outside d
    ctx.write(lane / ".git/objects/info/alternates", "../../../mid/.git/objects\n")
    ctx.write(mid / ".git/objects/info/alternates", "../../../../chain-out/.git/objects\n")
    return ["--lane", "lane"]


FIXTURES = [{"fid": "bl5-alternates-chain-out", "tool": "anchor", "expect": "breach", "defects": [], "build": build}]
```

### `h_wt_commondir_out.py`

```python
"""Sealed blind hostile module B — round-50 wave-1 seat `R50C1CritBlind5` (critic, R50-C1).

Attack class: **a linked worktree whose gitdir is inside `d` and whose `commondir` leaves `d`.**

    wt/.git            "gitdir: ../wtadmin"                 a FILE, target INSIDE d
    wtadmin/gitdir     "../wt/.git"                         back-pointer, INSIDE d
    wtadmin/commondir  "../../wt-common/.git"               resolves OUTSIDE d

Built with real git, then relocated the way a moved store leaves a worktree: `git init` + commit + `git branch
feature` in `d.parent/wt-common`, `git worktree add --relative-paths -q d/wt feature`, then the per-worktree
admin directory (`wt-common/.git/worktrees/wt`) is moved into `d` and its two relative pointers are rewritten.
Git accepts and honours the result: `git -C wt rev-parse --show-toplevel` answers `d/wt` (inside) and
`rev-parse --absolute-git-dir` answers `d/wtadmin` (inside), while `rev-parse --git-common-dir` answers
`d.parent/wt-common/.git` (outside) and `git -C wt log`/`cat-file` read refs and objects from there (seat
receipt; moving the outside store away makes those reads fail).

Why this is the blind hostile counterpart of the repair. The repair must widen the allowlist twice for the
honest classes: a `.git` FILE whose target is inside `d` (`n21_separate_gitdir`) and the per-worktree metadata of
`n20_linked_worktree` (which carries `gitdir` and `commondir`). The tempting widenings — "admit a gitfile whose
target resolves inside `d`", "admit a worktree store whose `commondir` is a relative path", "admit `commondir`
== `../..`" — each admit this module, because its gitfile target is inside `d` and its `commondir` is a plain
relative path. Only a repair that resolves `commondir` against the *gitdir* (not against `d`, and not by shape)
and requires the resolved common store inside `d` refuses it. Both rev-parse legs a fence would consult for the
boundary answer "inside", so this class is invisible to a rev-parse-based gate and visible only to a
store-content walk.

Measured on the base fence `05d5fe03…`: BREACH, reason `wt/.git is a file (gitdir redirect), not a directory` —
the same blanket rule that over-refuses honest `n20`/`n21`, so that refusal says nothing about the repair.

Determinism: every pointer is relative (git `--relative-paths` wrote the originals; the relocation rewrites them
relative to their own directories), so no build-scratch absolute path enters the tree. Round-44 builder
contract: `build(ctx, d)` fills `d` and returns the argv tail. `expect` is this seat's statement of the required
verdict (`breach`); the round-50 counter reads only `fid`/`tool`/`build`.
"""
import shutil


def build(ctx, d):
    out = ctx.init(d.parent / "wt-common")
    ctx.write(out / "seed.txt", "seed\n")
    ctx.git(out, "add", "-A")
    ctx.git(out, "commit", "-qm", "seed")
    ctx.git(out, "branch", "feature")
    ctx.sh("git", "-C", str(out), "worktree", "add", "--relative-paths", "-q", str(d / "wt"), "feature")
    adm = d / "wtadmin"
    shutil.move(str(out / ".git" / "worktrees" / "wt"), str(adm))
    ctx.write(d / "wt" / ".git", "gitdir: ../wtadmin\n")
    ctx.write(adm / "gitdir", "../wt/.git\n")
    ctx.write(adm / "commondir", "../../wt-common/.git\n")
    return ["--lane", "wt"]


FIXTURES = [{"fid": "bl5-wt-commondir-out", "tool": "anchor", "expect": "breach", "defects": [], "build": build}]
```

## What real git does in each module (the property the modules exist to test)

Both witnesses were taken with the lane's own `Ctx`-isolated git env, on the built fixture:

```
WITNESS bl5-alternates-chain-out outside-commit=cc4a0bfcaf43164a2c4420dbab49410c6dd7aceb
WITNESS bl5-alternates-chain-out read-outside-object rc=0 stdout='outside bytes'
WITNESS bl5-alternates-chain-out object-under-d=[] object-outside-d=['chain-out/.git/objects/cc/4a0bfcaf43164a2c4420dbab49410c6dd7aceb']
WITNESS bl5-alternates-chain-out outside-moved-away rc=128 err=['error: unable to normalize alternate object path: .../f000/mid/.git/objects/../../../../chain-out/.git/objects']
```

```
WITNESS bl5-wt-commondir-out toplevel rc=0 out=['…/f000/wt']
WITNESS bl5-wt-commondir-out absolute-git-dir rc=0 out=['…/f000/wtadmin']
WITNESS bl5-wt-commondir-out git-common-dir rc=0 out=['…/wt-common/.git']
WITNESS bl5-wt-commondir-out log rc=0 out=['a94edab seed']
WITNESS bl5-wt-commondir-out objects-dirs-under-d=[]
WITNESS bl5-wt-commondir-out outside-moved-away rc=128 err=["fatal: Invalid path '…/moveaway/wt/wt-common': No such file or directory"]
```

Reading the second block: **no `objects` directory exists anywhere under `d`**, both rev-parse legs a
boundary gate would consult answer *inside* `d`, and `git log` still resolves the commit from the outside store.
That is the whole attack: the escape is invisible to path-identity checks and visible only by resolving the
pointer contents.

Neither fixture trips a blanket structural rule by accident — `TREE anomalies=0 []` for both (no symlink, no
special file, no `nlink>1`), so a refusal cannot be an artefact of the tree-shape rules that the base fence
applies to everything.

## The counterexample: narrow widenings admit the modules, resolving widenings refuse them

`tools/naive_rules.py` implements, for the same fixture, the tempting widenings a repair author writes and the
resolving rules the claim requires. Verbatim (receipts `blind5-narrow-rules.txt` on the base fence,
`blind5-narrow-rules-candidate.txt` on the candidate fence; the rule verdicts are fence-independent):

```
FIXTURE bl5-alternates-chain-out module=h_alternates_chain.py
  FENCE       BREACH mid/.git/objects/info/alternates names '../../../../chain-out/.git/objects', which resolves outside the fixture
  R1a alternates one-hop  ADMIT  1 direct line(s) inside d (does not read the target's own alternates)
  R1b alternates transitive REFUSE hop 2: …/mid/.git/objects -> …/chain-out/.git/objects outside d
  REALGIT     rc=0     lane reads cc4a0bfcaf43 only present outside d -> 'outside bytes'
FIXTURE bl5-wt-commondir-out module=h_wt_commondir_out.py
  FENCE       BREACH wtadmin (via wt/.git)/commondir names '../../wt-common/.git', which resolves outside the fixture
  R2a gitfile one-hop    ADMIT  1 gitfile(s), targets inside d (target classified as a store, bytes unread)
  R2b gitfile+commondir   REFUSE … commondir -> …/wt-common/.git outside d
  R3a commondir text     ADMIT  1 commondir(s) hold a relative path (target never resolved)
  R3b commondir resolved  REFUSE wtadmin/commondir -> …/wt-common/.git outside d
  REALGIT     rc=0     common-dir=…/wt-common/.git log='a94edab seed' (no objects dir under d)
FIXTURE n22-alternates-in-d module=n22_alternates_in_d.py
  FENCE       ADMIT
  R1a alternates one-hop  ADMIT  1 direct line(s) inside d (does not read the target's own alternates)
  R1b alternates transitive ADMIT  2 store(s), every hop inside d
FIXTURE n20-linked-worktree module=n20_linked_worktree.py
  FENCE       ADMIT
  R2a gitfile one-hop    ADMIT  1 gitfile(s), targets inside d (target classified as a store, bytes unread)
  R3a commondir text     ADMIT  1 commondir(s) hold a relative path (target never resolved)
  R3b commondir resolved  ADMIT  1 commondir(s) resolve inside d
FIXTURE n21-separate-gitdir module=n21_separate_gitdir.py
  FENCE       ADMIT
  R2a gitfile one-hop    ADMIT  1 gitfile(s), targets inside d (target classified as a store, bytes unread)
```

The `FENCE` lines above are the repair candidate's (it admits all three honest indirection classes and refuses
both modules). The rule lines are the critique:

- **R1a** (resolve only the lane store's own one hop) admits honest `n22` **and** admits
  `bl5-alternates-chain-out`, where real git reads outside `d`. A repair that implements R1a passes the honest
  leg and leaks this module.
- **R2a** (admit a gitfile whose target is inside `d`, without resolving the target's `commondir`) admits honest
  `n20`/`n21` **and** admits `bl5-wt-commondir-out`, where real git's common dir is outside `d`.
- **R3a** (accept a `commondir` because it is a relative path — "git only writes `../..`") admits honest `n20`
  **and** admits `bl5-wt-commondir-out`.

So each module is passable only by the resolving rule (R1b / R2b / R3b), and those resolving rules cost nothing
on the honest leg. That is exactly the discrimination the sealed50 leg is meant to provide, and it is why the
modules are worth the slot: they fail every cheap widening of the exact two rules the honest population forces
the round to relax.

## What the two modules measure on the fences that exist now

Base fence (`05d5fe03…`), full counter run with the two modules installed in a scratch clone's
`plans/sealed50/` (`--allow-dirty`, `--skip-mutants`; the clone is dirty only because the modules are untracked
there — this is a control run, not a scored predicate run):

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE …/lane/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=113 refused=13 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=2 clean=2 leaked=0 build_errors=0
SEALED50-TOTAL 2 expected_min=6
PREDICATE R50-C1 fail
```

Both modules are `clean=2` on the base fence, and both for the *blanket* reason that also refuses their honest
counterparts — `lane/.git/objects/info/alternates present (object-store redirect)` and `wt/.git is a file
(gitdir redirect), not a directory`. Their base-fence refusal is therefore **not** evidence of anything; their
value is entirely in what they force of the repair, which is the point of a blind module.

Repair candidate (wave file, uncommitted; measured at both of its digests, `6df6a2a3…` and `9baedf13…`):
`HONEST fixtures=126 admitted=117 refused=9`, `REFUSALS total=20 clean=20`, `SEALED total=12 clean=12`,
`SEALED total=2 clean=2 leaked=0` — the candidate refuses both modules **on the escaping geometry**, verbatim
(identical at both digests):

```
FENCE fid=bl5-alternates-chain-out verdict=BREACH why="mid/.git/objects/info/alternates names '../../../../chain-out/.git/objects', which resolves outside the fixture"
FENCE fid=bl5-wt-commondir-out verdict=BREACH why="wtadmin (via wt/.git)/commondir names '../../wt-common/.git', which resolves outside the fixture"
```

and admits `n20`/`n21`/`n22` (`FENCE ADMIT` for all three in the rule receipt; none of them appears in the
candidate's `HONEST-REFUSED` list). On my two modules the candidate's resolution logic is correct. Its
`refused=9` is a different matter (it still over-refuses `n12`, `n13`, `n14`, `n15`, `n16`, `n18`, `n03`, `n07`,
`n08`), so it cannot pass the honest leg as it stands; that is its author's item, not this one.

### The repaired fence now in the live tree (S2 working state, uncommitted)

While this seat was measuring, the integrator's S2 work appeared in the lane working tree. It is not a commit and
may change; recorded at measurement time for what it is: `plans/fixture_fence.py` sha256
`57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1` (copied into scratch; the live checkout was
never run). Against that fence, with **only** my two modules in the clone's `plans/sealed50/`:

```
FENCE fid=bl5-alternates-chain-out verdict=BREACH why='mid/.git/objects/info/alternates names a store outside the fixture'
FENCE fid=bl5-wt-commondir-out verdict=BREACH why='wtadmin/commondir names a common dir outside the fixture'
```

```
REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
TREE dirty=1
FENCE …/S2-fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69 mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=2 clean=2 leaked=0 build_errors=0
SEALED50-TOTAL 2 expected_min=6
PREDICATE R50-C1 fail
```

`PREDICATE … fail` here is only `SEALED50-TOTAL 2 expected_min=6` from my two-module clone; every other line is the
S2 fence's own property. So the S2 fence resolves both escapes correctly, and the honest `n20`/`n21`/`n22`
classes it must now admit do not cost it either module's refusal.

### Cross-check: ref bodies (the class the frozen 32 cannot catch)

Seat `R50C1ExecRepair` reported a transient defect in its own candidate — a dropped `_refs` call let
`n17-replace-ref` pass by *absence* of the check rather than by the allowlist — and noted correctly that the
frozen 32 hostile modules cannot catch it, because nothing on the hostile side carries a ref whose **body** git
would never write (the honest `n16`/`n17` only force refs to be admitted). `tools/probe_refs.py` supplies the
pair: the honest classes stay honest (40-hex body) and the hostile fixtures carry `junk` in
`.git/refs/replace/<40 hex>` and `.git/refs/notes/commits`. Verbatim (receipt `blind5-refs-probe.txt`):

```
##### base fence 05d5fe03…
FIXTURE bl5-ref-junk-replace source=hostile verdict=BREACH why=repo/.git/refs/replace is not refs/heads or refs/tags
FIXTURE bl5-ref-junk-notes source=hostile verdict=BREACH why=repo/.git/refs/notes is not refs/heads or refs/tags
FIXTURE n16-notes-ref source=honest verdict=BREACH why=…/logs/refs/notes has a name git does not write
FIXTURE n17-replace-ref source=honest verdict=BREACH why=repo/.git/refs/replace is not refs/heads or refs/tags
##### candidate 9baedf13…
FIXTURE bl5-ref-junk-replace source=hostile verdict=BREACH why=…/refs/replace/aaaa… is not a 40-hex ref
FIXTURE bl5-ref-junk-notes source=hostile verdict=BREACH why=repo/.git/refs/notes is not refs/heads, refs/tags or refs/replace
FIXTURE n16-notes-ref source=honest verdict=BREACH why=…/logs/refs/notes has a name git does not write
FIXTURE n17-replace-ref source=honest verdict=ADMIT
##### lane S2 fence 57adce4a…
FIXTURE bl5-ref-junk-replace source=hostile verdict=BREACH why=…/refs/replace/aaaa… is not a 40-hex ref
FIXTURE bl5-ref-junk-notes source=hostile verdict=BREACH why=…/refs/notes/commits is not a 40-hex ref
FIXTURE n16-notes-ref source=honest verdict=ADMIT
FIXTURE n17-replace-ref source=honest verdict=ADMIT
```

The lane file (`57adce4a…`) validates ref bodies **and** admits both honest ref classes, so the regression the
peer warns about is not present in it; its refusal is on the body, not on the ref name. The candidate
(`9baedf13…`) validates the `refs/replace` body but still refuses `refs/notes` by name, which is one of its nine
honest over-refusals — no leak, just an unfinished widening. This is the one place where my measurement
disagrees with a reading of the peer's note: at `9baedf13…` the dropped-body-check defect is gone (refused on the
body), so the class is not an open hole in either text; the probe is the cheap guard for S3.

### Gap in the blind set as it stands (finding for the L1)

The eighteen `plans/sealed50/` modules authored by the other blind seats exercise `.git`-file targets, symlinked
`objects`, `refs/replace` targets, a worktree **extra entry**, `FETCH_HEAD` hardlinks, config `[include]`,
`argv` escapes and single-hop alternates (`s50_alternates_dotdot_abs.py` is one absolute line with `..`; `b1_…`
is over-determined by a first-hop escape). **No landed module carries a `commondir` at all** (`grep -l
commondir plans/sealed50/*.py` → nothing; `s50_06_wt_extra_entry.py` builds a git-written worktree whose
`commondir` is inside `d`), and none builds a two-hop alternates chain. Those are precisely the two relaxations
the honest classes `n20`/`n22` force:

- a fence whose `commondir` rule is **R3a** (relative text, never resolved) admits `bl5-wt-commondir-out`, is
  admitted by every honest class, and would pass the eighteen landed modules, `refusals46`, `sealed46` and the
  126-fixture population. Without this seat's module B that leak is invisible to the whole instrument.
- a fence whose alternates rule is **R1a** (one hop from the lane store) admits `bl5-alternates-chain-out` and
  likewise passes everything else.

The S2 fence in the tree passes both, so the gap is closed for this candidate; it remains the reason these two
modules belong in the frozen set rather than being nice-to-have.

## Distinctness from the frozen 32, the landed 18 and the honest classes

- `refusals46/f5_alternates.py` — one hop, direct escape: `alternates` names an outside store. Mine keeps the
  first hop **inside** `d` and escapes at the second.
- `refusals46/f7_commondir.py` — a top-level `.git` **directory** carrying an absolute `commondir`, no gitfile.
  Mine is a worktree admin dir reached through a `.git` file, and the `commondir` is relative (`../..`-style
  climb).
- `refusals46/f19_commondir_hidden.py` — relative `commondir` below a **pruned** `.git/modules/…` path that the
  walk never descends, with `--lane` naming that hidden store. Mine is reached through the fixture's own gitfile
  and `--lane` names the worktree root.
- `refusals46/f18_wtmeta_out.py` — a linked worktree whose **checkout** lives outside `d` while the store stays
  inside. Mine is the mirror image: checkout and gitdir inside `d`, **common store outside**.
- `refusals46/f1_gitfile.py` — `.git` file whose target is outside `d`. Mine: target inside `d`.
- `sealed46/s_objects_link.py`, `p_info_redirect.py` — symlinked object dirs. Mine has no symlink.
- `sealed50/s50_alternates_dotdot_abs.py` (seat `R50C1CritBlind1`) — **one** absolute alternates line whose `..`
  segments leave `d`; the opening hop already escapes. Mine is relative, its opening hop is **inside** `d`, and
  the escape is only at hop 2, so no absolute-vs-unresolved path test reaches it.
- `sealed50/b1_replace_ref_target_outside_store.py` — a `refs/replace` target reachable through an alternates
  entry that itself leaves `d` (over-determined). Mine has no replace ref; the alternates chain is the only
  indirection in play.
- `sealed50/s50_06_wt_extra_entry.py` — a git-written worktree with an unlisted entry in its store. Its
  `commondir` is the one git wrote, inside `d`; mine is the escaping one. No landed module carries a
  `commondir` that resolves outside `d`.
- Honest `n20`/`n21`/`n22` — the all-inside versions; my modules differ from each by exactly one resolved hop or
  one resolved pointer, which is what makes them blind enough to be generated from the honest description and
  still meaningful.

## Critique beyond the two modules (composed indirection)

`tools/probe_compose.py` (scratch probe, **not** a deliverable) composes the two kinds: gitfile → `wtadmin`
(inside), `commondir` → `d/shared` (inside, a **bare** store), `shared/objects/info/alternates` → outside. Real
git reads the outside commit (`REALGIT log rc=0 out='cc4a0bf out'`). The candidate refuses it — but for a
neighbouring reason, `wtadmin (via wt/.git)/commondir store/config core.bare must be false`, i.e. the
bare-store rule, not the cross-kind resolution. That is a fair trade (bare stores are outside the honest
population's shapes), and it is recorded so the L1 does not read "candidate refuses the composition" as
"candidate resolves across kinds". If a later honest class ever admits a bare common store, this probe is the
first thing to re-run.

## Commands run (all in `/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind5`, `TMPDIR` there)

```
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kengaku-shokunin lane
git -C lane checkout -q 3b02d573d58cc6d2e0d27ef92ac0815354912252      # REV measured; worktree clean
python3 C1CritBlind5/blind5_drive.py --lane lane --module-dir C1CritBlind5/sealed --work drive5
python3 C1CritBlind5/blind5_drive.py --lane lane --module-dir C1CritBlind5/sealed \
        --fence <wave>/C1ExecRepair/fence_candidate.py --work drive4
python3 C1CritBlind5/naive_rules.py --lane lane [--fence <candidate>] --module-dir C1CritBlind5/sealed \
        --extra-module lane/plans/honest50/modules/novel49/n20_linked_worktree.py \
        --extra-module lane/plans/honest50/modules/novel50/n21_separate_gitdir.py \
        --extra-module lane/plans/honest50/modules/novel50/n22_alternates_in_d.py --work nw2
python3 C1CritBlind5/probe_compose.py --lane lane [--fence <candidate>] --work compose-*
python3 C1CritBlind5/probe_refs.py --lane lane --fence <fence> \
        --honest lane/plans/honest50/modules/novel48/n16_notes_ref.py \
        --honest lane/plans/honest50/modules/novel49/n17_replace_ref.py --work refs-<digest>
cp C1CritBlind5/sealed/*.py lane/plans/sealed50/                     # scratch clone only
python3 plans/round50_c1_verify.py --lane . --allow-dirty --skip-mutants [--fence <candidate>] --work …
diff -r -x index -x moveaway drive drive2                             # DIFF_RC=0: two builds identical
```

Receipts copied here: `receipts/blind5-drive-base.txt`, `blind5-drive-candidate-9baedf13.txt`,
`blind5-drive-S2.txt`, `blind5-narrow-rules.txt`, `blind5-narrow-rules-candidate.txt`,
`counter-with-blind50.txt`, `counter-with-blind50-candidate-6df6a2a3.txt`,
`counter-with-blind50-candidate-9baedf13.txt`, `counter-with-blind50-S2.txt`, `blind5-refs-probe.txt`,
`blind5-compose-base.txt`, `blind5-compose-candidate.txt`. Drivers: `tools/blind5_drive.py`,
`tools/naive_rules.py`, `tools/probe_refs.py`, `tools/probe_compose.py`.

## Limits

- Reading only: the modules prove the *outside read* by which object git demands, not by tracing syscalls. Two
  builds are byte-identical (`diff -r` excluding the `index` stat caches, `DIFF_RC=0`), and no build-scratch
  absolute path enters either tree (`grep -rl` for the scratch root over both trees: no hits), so the verdicts
  are not path-dependent — but identity is *not* pinned the way the honest population pins it, because a sealed
  module is scored on the fence verdict, not on a digest row.
- Module B's shape is git-**accepted**, not git-**written** by a single command: `git worktree add` writes the
  admin dir outside and the relocation moves it in. It is the same planted state class as `f7`/`f19`, and it is
  the only way to get "gitdir inside, common dir outside" — git itself never writes that pair in that order. A
  repair may legitimately refuse it by "git does not produce this", which is still a refusal; the module cannot
  distinguish "refused because the escape resolves outside" from "refused because the shape is not
  git-produced". Module A has no such ambiguity (both hops are plain `alternates` files git follows).
- The counter's `SEALED50_MIN=6` is not reached by this seat alone (2 of 6). The measured `SEALED50-TOTAL 2
  expected_min=6` line is a composition gap for the L1, not a failure of either module.
- The candidate fence is an uncommitted wave file; its measured pass is a proposal's property, not R50-C1's.
  The S2 fence measured above is likewise a working-tree state (`57adce4a…`), not a commit: its two refusals
  must be re-taken on the clean S2/S3 clone before they count for anything, and they are only as good as that
  digest matching the committed file.
- No mutant leg was run: the carried `plans/mutants50/c1-mutants.json` is a candidate against the r49 fence and
  has no bearing on two new sealed modules (the counter's own `--skip-mutants` control path).

Scratch `/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind5` removed before yield; the citable copies are the ones
under this directory. `C1CritBlind5/sealed/__pycache__` was removed twice: another seat is importing the two
modules straight from this directory (the `.pyc` regenerates within seconds), so a `__pycache__` appearing there
is not part of the deliverable and the files to copy are the two `.py` files with the digests in the table above.

VERDICT: `delivered` — two blind hostile modules authored, deterministic, axis-clean (no symlink/hardlink
artefacts), refused by the base fence only through the blanket rules that also over-refuse their honest
counterparts; refused on the escaping geometry itself by the repair candidate in this wave directory at both of
its digests (`6df6a2a3…` and `9baedf13…`) and by the S2 working-tree fence (`57adce4a…`, `HONEST 126/126`,
`REFUSALS 20/20`, `SEALED 12/12`, these two `clean=2`). Every cheap widening that admits the honest
`n20`/`n21`/`n22` classes admits them and leaks a real outside read (R1a / R2a / R3a in the rule receipt), and
the eighteen blind modules already landed in `plans/sealed50/` contain no `commondir` and no multi-hop
alternates case — so these two modules are the only held-out check on the two relaxations the round's honest
classes force. Cross-checks run for the integrator: the composed-indirection probe (candidate refuses only via
its bare-store rule) and the refs-body probe (the lane S2 file validates ref bodies and admits honest
`n16`/`n17`; the class the peer warned about is closed in that text). Axis worked: novelty (R50-C1); no
production file, commit, or scored run touched.
