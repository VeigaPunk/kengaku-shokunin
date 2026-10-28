# R50C1CritBlind6 — blind hostile modules: the second repo's store, and the `.git`-file widening

Seat: critic (attack role), R50-C1 novelty. Leaf member, no dispatch. Read-only against the lane.
REV measured: `3b02d573d58cc6d2e0d27ef92ac0815354912252` (stage-1 freeze) on a `git clone --shared`;
lane tip at session start `c3372a9b24d3a200946a6b37dc0a31ed5c982cc1`; ancestry verified first (below).

## Axes

| axis | what this seat moves |
|---|---|
| novelty (R50-C1) | the SEALED leg's blind held-out set: 2 modules / 5 fixtures, one of which is a measured, load-bearing counterexample to a containment test that every existing lane artifact passes |
| coverage | untouched (open L0 cap); named here only so the round's claim split stays visible |
| calibration (R50-C2) | untouched |

## Deliverables (blind modules, landable at `plans/sealed50/`)

```
.ufo/waves/round-50/w1/C1CritBlind6/sealed/s6_second_store_mount.py            sha256 cfb0005ddfe5011c23b3ca87cfefb10691f454408b0a412d1ea7162d8fb2a80d
.ufo/waves/round-50/w1/C1CritBlind6/sealed/s6_gitfile_rel_objects_link.py      sha256 efe4ad43bde65eaf43371893d535dde122ddf1d0c244f4d751ebc009445ffd4d
```

Contract: `build(ctx, d)` + `FIXTURES`, the same shape `plans/sealed46/*.py` uses; `tool="order"`,
`expect="reject"`. Both were authored against the fence text at the freeze (`plans/fixture_fence.py`
`05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e`) without reading any sibling
seat's module.

| module | fid | the hostile state |
|---|---|---|
| `s6_second_store_mount` | `seal6-second-store-outside` | two repos; repo A (`lane`) honest and named by `--lane`; repo B's store is **outside `d`**, named by a **git-written absolute** gitfile. The store lives at a sibling whose name **shares `d`'s prefix** (`f000-evil`), so a containment test written as `str(target).startswith(str(d))` admits it. |
| | `seal6-second-store-twin` | two repos; repo B's store is inside `d`, but one loose object in it has a second name outside `d` (`nlink=2`). |
| `s6_gitfile_rel_objects_link` | `seal6-gitfile-up-outside` | the repository **is** `d`; `d/.git` is the FILE `gitdir: ../s6-store-up` — the `../` form naming a store **outside `d`** — and that store's `objects` is a **symlink** to a third location outside `d`. |
| | `seal6-gitfile-up-inside-link` | the honest `n21` layout (repo `d/sub/repo`, store `d/sub/store`, `gitdir: ../store`) with one entry changed: `store/objects` is a **symlink** outside `d`. |
| | `seal6-gitfile-submodule-store-link` | `second/.git` = `gitdir: ../main/.git/modules/sub`; that path is inside `d`, under a `.git` the tree walk never enters, and is a **symlink** to a full, honest-looking store outside `d`. |

Every fixture stays **live** through its escape: `git -C <repo> rev-parse --verify HEAD` returns a real
commit in all five (`receipts/all-fences-verdicts.txt`, `LIVE` lines), so no refusal can be excused as
"the repo was already broken".

## Item (i): can the mount boundary be built? — measured, no

The literal shape (a store whose `st_dev` differs from `d`'s while the store is lexically inside `d`)
is **not expressible as a fixture state** on this host, and the emulation the item suggests is
**forbidden by the kernel**, not merely unavailable:

```
st_dev=66309 /fast
st_dev=66308 /tmp
st_dev=33 /dev/shm
st_dev=56 /home
link /tmp -> EXDEV          rename /tmp -> EXDEV
link /dev/shm -> EXDEV      rename /dev/shm -> EXDEV
mount(/dev/shm -> a2) rc= -1 EPERM st_dev still 66309
child: st_dev=33            parent: st_dev=66309            unprivileged_userns_clone=1
```

(`receipts/device-probe.txt`.) A hardlink is by definition one inode, hence one device: `os.link` across
filesystems returns `EXDEV` always, so "hardlink into a different device" cannot emulate a mount
boundary in any fixture, on any host. In-process `mount()` is `EPERM`; a private user+mount namespace
*does* produce `st_dev=33` under `d`, but only inside the child process, and the fence runs in the
counter's process. A module *could* call `unshare(CLONE_NEWUSER|CLONE_NEWNS)` from `build()` (measured
working in-process), but that is **process state, not fixture state**: it reconfigures the counter's
namespace for every later fixture, is invisible to `tree_identity`, and makes the same module build
differently on a host with `unprivileged_userns_clone=0`. That is a harness attack, not a hostile
fixture — it is reported below as a counter-level shape, not shipped as a module.

What is buildable, and what the module ships, is the same hazard in the form a fence can see with no
capability: **a second repository inside `d` whose store is not provably inside `d`** (absolute
gitfile to an outside store; object bytes with a second name outside `d`).

## Counterexample (the finding that matters)

`seal6-second-store-outside` is the only artifact in the lane that catches a plausible containment bug
that the 126-fixture honest population, the 20 `refusals46` modules and the 12 `sealed46` modules all
pass. Probe (`probes/repair_prefix.py`, sha256 `89918c0b…`): the base fence with a `.git`-file branch
whose containment test is `str(target).startswith(str(d))` — no separator, no `normpath` guard — the
same class of slip `_inside()` exists to prevent.

```
=== repair_prefix (counter, frozen instrument, clone at 3b02d57) ===
HONEST fixtures=126 admitted=114 refused=12 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=2 clean=1 leaked=1 build_errors=0
SEALED-MISS s6_second_store_mount.py seal6-second-store-outside ADMIT
```

`receipts/counter-repair_prefix.txt`. The same probe is refused by a correct repair
(`probes/repair_careful.py`, `SEALED total=2 clean=2 leaked=0`) and by the base fence — so the fixture
is **satisfiable** and the kill direction is **witnessed on two fences**, not assumed.

## Item (ii): the `.git`-file widening, attacked where the walk cannot see

The widening is load-bearing for the round: honest `n21`/`n20` force the fence to stop refusing
`gitdir:` files. Measured against a tight pair — the population's own `n21` module, a scratch honest
twin with *my* layout, and my hostile twin differing by exactly the `store/objects` entry
(`receipts/twin-pair.txt`):

```
FENCE fixture_fence.py 05d5fe03aa3be6b7
  twin-twin-n21-inside                 BREACH  sub/repo/.git is a file (gitdir redirect), not a directory
  sealed-seal6-gitfile-up-inside-link  BREACH  sub/repo/.git is a file (gitdir redirect), not a directory
  population-n21-separate-gitdir       BREACH  wt/.git is a file (gitdir redirect), not a directory
FENCE repair_careful.py 70b7cc3a6fca8992
  twin-twin-n21-inside                 ADMIT
  sealed-seal6-gitfile-up-inside-link  BREACH  sub/store/objects is a symlink
  population-n21-separate-gitdir       ADMIT
FENCE repair_sloppy.py 991639c3bcd0c217
  twin-twin-n21-inside                 ADMIT
  sealed-seal6-gitfile-up-inside-link  BREACH  sub/store/objects is a symlink
  population-n21-separate-gitdir       ADMIT
```

A principled gitfile repair admits honest `n21` and the honest twin, and refuses the hostile twin for
exactly the entry that carries the breach. Verdict on the widening: **it holds** against the two
repairs I could build — including the omission I expected to be fatal (`repair_sloppy.py`: no `lstat`
of the gitfile target, no realpath containment). The reason is structural, and the L1 should know it:
the base fence's per-store **allowlist** already closes the holes a `gitdir:` redirect opens. Every
unwalked placement a symlinked store could occupy is rejected by the *containing* store's own
classification — `main/.git/modules` is "not a plain-init entry", `objects/info/*` is
"object-store redirect", `refs/*` must be 40-hex files — so `seal6-gitfile-submodule-store-link` is
refused even by the no-lstat probe, on the containing store, not on the target. Negative result,
recorded so the L1 does not pay for a defence that is already free.

## Counter-level shape, not shipped (escalation)

The mount-boundary *fixture* the item asked for is reachable only as **counter state**: run the
instrument under `unshare -Ur -m` with `mount --bind <other-fs-dir> <fixture>/repo2/.git` created
before the fence call. Measured capability: `unshare -Ur -m true` → rc 0, `mount --bind /dev/shm` →
child `st_dev=33`, parent unchanged. If the L1 wants "the store is on another filesystem" observed at
all, it belongs in a counter leg (a fifth leg or a `--mount-probe` flag) with the device comparison
inside the fence (`os.lstat(store).st_dev != os.lstat(d).st_dev` → refuse). It must **not** be a
sealed module: a module that mutates the counter's namespace makes the SEALED count host-dependent
and can silently poison every later fixture in the run.

## The lane moved under this seat — landed state at report time (read-only, measured on a clone)

My matrix above is against the **freeze** (`3b02d57`, fence `05d5fe03…`), as the seat bounds require.
While I worked, S2/S3 landed: lane HEAD is `d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78`, and the
repaired fence is `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1` (commit `6db0279`,
991 lines). Because the landed set *already contains my two modules*, I measured the landed artifact on
a second `git clone --shared` at HEAD (never the live checkout):

```
REV d45c5bb23b5ecff7f6a069cdb17db2a5fed7bc78
TREE dirty=0
FENCE …/plans/fixture_fence.py sha256=57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1
POPULATION fixtures=126 pin=b5197f94… mismatched=0 build_errors=0
HONEST fixtures=126 admitted=126 refused=0 error=0
REFUSALS total=20 clean=20 leaked=0 build_errors=0
SEALED total=12 clean=12 leaked=0 build_errors=0
SEALED total=18 clean=18 leaked=0 build_errors=0
PREDICATE R50-C1 pass
```

(`receipts/counter-landed-s2.txt`.) Three facts the integrator needs from that run:

1. **The landed copy of `s6_second_store_mount.py` is one revision behind my deliverable**:
   `f2425983…` in the lane vs `cfb0005d…` here. The lane holds my *pre-strengthening* body, i.e. its
   outside store sits at the plainly-named sibling `s6-store-second`; the prefix-sharing sibling
   (`f000-evil`) that makes `seal6-second-store-outside` catch `startswith` containment is **not** in
   the graded set. `s6_gitfile_rel_objects_link.py` landed byte-identical (`efe4ad43…`).
   Measured cost of taking the stronger body: none — installing `cfb0005d…` in the same clone gives
   `SEALED total=18 clean=18 leaked=0` and `PREDICATE R50-C1 pass` unchanged
   (`receipts/counter-landed-s2-strengthened.txt`). Recommend the swap.
2. `57adce4a…` refuses `st_dev != ddev` ("crosses a mount boundary") at two sites. Per the measurement
   in section (i), **no sealed module can exercise that branch** — a mount point under `d` is not a
   fixture state — so as landed it is untested code inside the analysed object. Either name it in the
   claims' limits or witness it with the counter leg below.
3. The live worktree's `plans/round50_c1_verify.py` is **modified after the scored run**
   (`850ec790…` in the worktree vs `d8787b34…` committed). Whatever the S3 receipt names as its counter
   digest, the tree at HEAD is not the tree that produced it; an integrator should either commit or
   revert that edit before any further scoring.

## Coverage this seat does NOT add (measured negative)

Coordination fact from `R50C1ExecRepair` (a dropped `_refs` call makes honest `n17` pass by absence,
unseen by the frozen 32 hostile modules) checked against my fixtures: with `_refs` neutered
(`probes/repair_norefs.py`, sha256 `3a71b174…`), **all five of my fixtures stay refused for their own
reasons** (`receipts/norefs-probe.txt`). My modules do not cover refs classification; that regression
needs its own probe (`refs/notes`, a non-hex `refs/replace`) before S2. Do not count this seat's
SEALED contribution toward it.

## Residual hole (reasoned, NOT measured — hypothesis for the alternates widening)

`[INFERENCE]` The walk classifies only directories that hold a `.git`; a **bare store** inside `d`
(`d/alt` with `objects/`, `refs/`, no `.git`) is therefore never classified, and its own
`objects/info/alternates` is never read. A repair that admits `alternates` (n22) and validates only the
file it was pointed at — target inside `d` — would admit a two-hop chain
(`repo/objects/info/alternates -> d/alt/objects`, `d/alt/objects/info/alternates -> <outside>`) and
read objects outside `d` through a walk-visible, symlink-free path. Not built here: it is the
alternates seat's family, and my item names the gitfile/objects shape. Smallest safe correction if it
lands: validate `alternates` recursively (classify the target store, including its own
`objects/info`), and cap the hop count.

## Exact commands and evidence

```
# ancestry + revision (lane, read-only)
git rev-parse HEAD                                    -> c3372a9b24d3a200946a6b37dc0a31ed5c982cc1
git merge-base --is-ancestor 3b02d573… HEAD           -> ANCESTOR=yes

# my clone (scratch), then the frozen instrument with my modules installed in plans/sealed50
git clone --shared <lane> lane-clone && git -C lane-clone checkout -q 3b02d573…
python3 plans/round50_c1_verify.py --lane . --allow-dirty --skip-mutants --work <S>/cwork
  REV 3b02d573d58cc6d2e0d27ef92ac0815354912252
  TREE dirty=2
  FENCE …/plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
  POPULATION fixtures=126 pin=b5197f94… mismatched=0 build_errors=0
  HONEST fixtures=126 admitted=113 refused=13 error=0
  REFUSALS total=20 clean=20 leaked=0 build_errors=0
  SEALED total=12 clean=12 leaked=0 build_errors=0
  SEALED total=2 clean=2 leaked=0 build_errors=0        <- my two blind modules, both clean
  SEALED50-TOTAL 2 expected_min=6                       <- my clone holds only 2 (the landing needs ≥6)
  PREDICATE R50-C1 fail                                 <- base fence: HONEST 113, as the claim states

# same instrument against candidate repairs (--fence), and against the HEAD-repaired counter
python3 plans/round50_c1_verify.py --lane . --allow-dirty --skip-mutants --fence <S>/fences/repair_careful.py
python3 plans/round50_c1_verify.py --lane . --allow-dirty --skip-mutants --fence <S>/fences/repair_sloppy.py
python3 plans/round50_c1_verify.py --lane . --allow-dirty --skip-mutants --fence <S>/fences/repair_prefix.py
python3 plans/round50_c1_verify_repaired.py --lane . --allow-dirty --skip-mutants     # HEAD d8787b34… copy
                                                       -> SEALED total=2 clean=2 leaked=0 (identical)

# the landed artifact (second clone at HEAD, no --allow-dirty needed):
git clone --shared <lane> lane-head && cd lane-head
python3 plans/round50_c1_verify.py --lane . --skip-mutants --work <S>/cwork-head
                                                       -> HONEST 126/126, REFUSALS 20/20,
                                                          SEALED 12/12 + 18/18, PREDICATE pass
# then with this seat's strengthened module installed in that clone:
cp <wave>/C1CritBlind6/sealed/s6_second_store_mount.py plans/sealed50/
python3 plans/round50_c1_verify.py --lane . --allow-dirty --skip-mutants
                                                       -> SEALED 18/18 clean, PREDICATE pass
```

`dirty=2` are my two installed modules (`plans/sealed50/`), the only writes to the clone; no lane
file was touched. The `--allow-dirty` and `--skip-mutants` flags are testing-only and are stated rather
than hidden; the mutant leg is not this item's and the candidate battery is not what my fixtures score.

Fixture verdict matrix over three fences and a deliberate bug: `receipts/all-fences-verdicts.txt`,
`receipts/prefix-probe-verdicts.txt`, `receipts/norefs-probe.txt`. Determinism: both modules are
byte-identical over two builds at
the same path (`receipts/determinism-samepath.txt`); `seal6-second-store-outside` differs across
*different* build roots only because git writes the store's absolute path into the gitfile
(`receipts/determinism.txt`) — a store outside `d` cannot be identity-pinned, which is why this shape
belongs on the hostile side and why honest classes must keep the relative gitfile form (`n21` does).

## Smallest safe correction (for the L1)

1. The two modules are **already in the lane** (`plans/sealed50/`, commit `6db0279`) at digests
   `efe4ad43…` (gitfile) and `f2425983…` (second-store = my pre-strengthening body). Swap the second
   to this seat's `cfb0005d…`: byte-identical refusal behaviour on the landed fence (measured), and it
   is the only artifact that pins containment against a `startswith` slip. `SEALED50_MIN` is already
   satisfied (18 modules at HEAD).
2. In the repaired `_tree`/`breach`, the `.git`-file branch must: (a) parse a plain `gitdir:` line,
   (b) resolve **lexically** (`_norm`), (c) require containment through `_inside()` — never
   `startswith`, never `resolve()`, (d) `os.lstat` the target and refuse a symlink, (e) classify the
   **resolved target** with the unchanged `_store` allowlist, and (f) keep counting the worktree as a
   repository for `--lane`. Steps (a)–(d) are what `seal6-second-store-outside`,
   `seal6-gitfile-up-outside` and `seal6-gitfile-submodule-store-link` pin; (e) is what
   `seal6-gitfile-up-inside-link` pins; the `nlink` rule retained on the store's objects is what
   `seal6-second-store-twin` pins.
3. Do not test the device boundary with a module. If it is claimed, it is a counter leg with the
   namespace created outside the fence; otherwise the `st_dev != ddev` branch ships unexercised and
   must be named as such in the claims' limits (an unexercised refusal branch is not evidence).
4. Do not expect these five fixtures to cover the refs classification: a `_refs` call dropped from
   `_store` leaves all five refused (`receipts/norefs-probe.txt`). The n17-by-absence regression that
   `R50C1ExecRepair` found needs its own refs probe, whatever repair lands.

## Limits

- Two modules, five fixtures; this is a sample of the `.git`-file and second-store surfaces, not a
  proof. Nothing here admits R50-C1 and no axis is claimed by this seat.
- Host-sensitive: `EXDEV`/`EPERM`/userns numbers are this host (linux 7.2.11-arch1-1);
  `seal6-second-store-outside` embeds an absolute store path, so its bytes are host- and
  root-dependent by construction.
- `repair_careful.py`/`repair_sloppy.py`/`repair_prefix.py` are **seat probes**, not proposals: they
  implement only the gitfile branch, so their `HONEST admitted=114` is not a claim candidate (the
  honest legs still need n17/n18/n20/n22 and eight more classes).
- The alternates recursion above is `[INFERENCE]`, unmeasured, and out of this item's scope.

## Scratch

`/fast/scratch/hyaku/kengaku-r50/R50C1CritBlind6` (1.2 GB: two `--shared` clones + build trees) was
removed before this seat yielded — verified gone. Every cited receipt lives in this wave directory,
never in `/tmp`, and the probes in `C1CritBlind6/probes/` are runnable as-is
(`repair_careful.py`, `repair_sloppy.py`, `repair_prefix.py`, `repair_norefs.py` import
`fixture_fence_base.py` from the same directory, which is a byte-identical copy of
`plans/fixture_fence.py` at `3b02d57`, sha256 `05d5fe03…`).

VERDICT: R50-C1 not admitted (no admission claimed). Blind modules delivered and witnessed:
2 modules / 5 fixtures, all refused by the base fence and by a principled repair, refused with a
distinguishable reason post-repair (one per fixture), live through their escapes, deterministic at a
fixed path; `seal6-second-store-outside` is a measured counterexample that catches a `startswith`
containment test which the 126-fixture honest population, `refusals46` and `sealed46` all pass.
Literal mount-boundary store: NOT BUILDABLE as fixture state — measured (`EXDEV`, `EPERM`, namespace
invisibility), escalated as a counter-level shape. The `.git`-file widening holds against both
candidate repairs (negative result, with the allowlist named as the reason).
Landed artifact measured on a clean clone at `d45c5bb`: fence `57adce4a…` — HONEST 126/126,
REFUSALS 20/20, SEALED 12/12 + 18/18, PREDICATE pass; my gitfile module landed byte-identical, the
second-store module landed one revision behind (prefix-strengthening absent), and the strengthened body
re-runs to the same `pass`, so the swap is free. Two open items for the L1: the landed `st_dev != ddev`
branch cannot be exercised by any sealed module, and the worktree's `plans/round50_c1_verify.py`
(`850ec790…`) is modified after the scored run (`d8787b34…` committed).
