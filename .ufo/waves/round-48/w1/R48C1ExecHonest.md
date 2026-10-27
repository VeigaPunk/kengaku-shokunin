# R48C1ExecHonest — frozen honest battery builder (R48-C1, calibration)

Seat `R48C1ExecHonest` (executor, `@m_mim`), kengaku round 48 wave 1. Item: build the frozen honest battery —
rebuild the 104 battery42/43/44 fixtures, rebuild the 9 round-46 novel classes from their wave-2 report
descriptions, and author NEW novel honest classes; per-fixture build script + identity receipt; freeze the
population list with digests; author against the BASE fence description only.

`REV a543d92083557dd9b33ee674e9b99b03411f80af` — every fixture identity below was built from a clone of the lane
at the round-48 stage-1 freeze.

## Axes named

- **calibration** — R48-C1 only. No coverage/novelty/depth claim. No admission claim for R48-C1 or R48-C2: this
  seat produces the frozen honest *population*; the counter that scores it is written elsewhere and pinned at
  stage 2.

## Scored-run gate (checked before any execution)

The item forbids a scored counter/probe run unless the freeze exists in the committed lane tree and predates the
measurement. Checked, and no scored run was made:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af
commit
$ git -C … merge-base --is-ancestor a543d92083557dd9b33ee674e9b99b03411f80af HEAD && echo ANCESTOR_OK
ANCESTOR_OK
$ git -C … cat-file -e a543d92083557dd9b33ee674e9b99b03411f80af:plans/round48_c1_verify.py
fatal: path 'plans/round48_c1_verify.py' does not exist in 'a543d92083557dd9b33ee674e9b99b03411f80af'
$ git -C … cat-file -e HEAD:plans/round48_c1_verify.py
fatal: path 'plans/round48_c1_verify.py' does not exist in 'HEAD'
$ git -C … ls-tree -r --name-only a543d920… | grep -c '^\.ufo/waves/round-48/claims/'
0
```

Stage 1 (predicate/contract/controls/kill rule) is committed; **stage 2 (counter files, `<P>`/`<H>`/`<S>`/`<B>`
literals, pins, before-control receipts) is absent at both the freeze and HEAD**. A scored C1 run would therefore
be a measurement of claimed work before the population was frozen — so none was made. The builder below is not a
counter, a probe or a gated-tool run: it builds fixtures and digests them, and its receipt records
`SCORED none (no fence, gate or counter executed; stage-2 freeze absent at a543d920…)`.

## What landed

All paths are under the lane wave dir (untracked; the L1 integrates). No production file was read-modified or
written: `plans/*`, `corpus/*`, `SCORECARD.md`, `LOG.md`, `.ufo/state` untouched; no commit/push/jj.

| path | role | sha256 |
|---|---|---|
| `.ufo/waves/round-48/w1/R48C1ExecHonest/population.txt` | **frozen population**, 120 `HONEST` lines + 4 header lines | `70804edeaaf7bc297fac33a88867de59a1c1413addae3d02d32f91ea497bc7da` |
| `…/population.sha256` | the stage-2 pin (`sha256  population.txt`) | same digest |
| `…/modules.sha256` | 38 module digests (22 battery + 16 novel) | `51bfcfc4c9e6b664663f2ce5cfc8e5034808669bac3f0543d3915c1cdad11140` |
| `…/build_honest_population.py` | the builder (rebuild, determinism check, receipts, population emission) | `3cdadac39efc93e1a2c20ba9efa34b136c322d45f4cd2f296b188b0d0e69b427` |
| `…/modules/r46novel/*.py` | 9 modules, one fixture each — the round-46 novel honest classes rebuilt | see `modules.sha256` |
| `…/modules/novel48/*.py` | 7 modules, one fixture each — NEW honest classes n10–n16 | see `modules.sha256` |
| `…/identity.jsonl` | 120 identity receipts, one JSON per fixture, sorted | — |
| `…/receipts/<population>/<module>--<fid>.json` | the same identity, one file per fixture (120 files) | — |
| `…/builder-receipt.txt` | run receipt: `REV`, digests, guards, 120 `IDENTITY` lines, host facts | — |
| `…/README.md` | consumer contract for the stage-2 counter author | — |

Per-fixture build script: for the 16 novel fixtures the module file *is* the build script (`build(ctx, d)`); for
the 104 battery fixtures it is the pinned `plans/batteryNN/<module>.py` plus the named function, and each
`population.txt` line names it (`<module>#<build>`). Per-fixture identity receipt: `receipts/…json` +
`identity.jsonl` + one `IDENTITY` line in `builder-receipt.txt`.

## Frozen population

Composition, verbatim from the receipt:

```
COUNTS battery42=29 battery43=42 battery44=33 r46novel=9 novel48=7
POPULATION population.txt sha256=70804edeaaf7bc297fac33a88867de59a1c1413addae3d02d32f91ea497bc7da fixtures=120
```

| population | fixtures | modules | source |
|---|---|---|---|
| `battery42` | 29 | a_class 6, a_route 6, a_row 6, o_clause 5, o_scan 6 | `plans/battery42/` |
| `battery43` | 42 | a_alt 14, a_err 6, a_row 3, a_url 4, o_alt 6, o_excuse 3, o_scan 6 | `plans/battery43/` |
| `battery44` | 33 | u14c_name_a 4, u14c_name_b 4, u5_short_a 3, u5_short_b 4, u6_long_a 4, u6_long_b 3, u7_twin_a 3, u7_twin_b 3, u9_worktree_a 2, u9_worktree_b 3 | `plans/battery44/` |
| `r46novel` | 9 | n01–n09, one class each | rebuilt from `w2/R46W2C1HoHonest.md` |
| `novel48` | 7 | n10–n16, one class each | authored by this seat |
| **total** | **120** | 38 modules | 85 `anchor` / 35 `order`, **0 duplicate `fid`** |

The 104 are provably *the same* 104 the round-46 counter measured: the builder imports `plans/round46_c1_verify.py`
and compares every battery module digest with its `PINS` row — `22/22 ok=1` (`BATTERY-MODULE-PIN … ok=1` × 22 in
`builder-receipt.txt`). The 104 count also equals that counter's `HONEST_TOTAL`.

## The 9 rebuilt round-46 novel honest classes

Each is one module in `modules/r46novel/`, built with the round-44 contract (`ctx.init`/`ctx.git`/`ctx.write`,
pinned identity and dates), returning `["--lane", "repo"]`. `tree_sha256` is the frozen identity.

| fid | class (from `R46W2C1HoHonest.md`) | git operations | tree_sha256 (first 16) |
|---|---|---|---|
| `n01-packed-refs` | packed refs after `gc`/`pack-refs` | commit, lightweight tag, `pack-refs --all --prune`, commit | `f5d3ee88474303cf` |
| `n02-annotated-tag` | annotated tags | commit, `tag -a v1.0.0` | `164240178bbc91c3` |
| `n03-detached-head` | detached HEAD | 2 commits, `checkout <sha>` | `9c691b180bbf1a37` |
| `n04-merge-commit` | a merge commit | branch, side commit, `merge --no-ff` | `d99f315fd7e3c156` |
| `n05-gitignore` | `.gitignore` | commit `.gitignore` + tracked file | `cac32789551f0141` |
| `n06-linear-30` | 30-commit linear history | 30 commits on one branch | `607642d4bfacc2f0` |
| `n07-reflog-gc` | reflog gc | 2 commits, `reflog expire --expire=now --all`, `gc --prune=now` | `40290797a6819095` |
| `n08-tag-detached` | annotated tag + detached HEAD | tag, 2 commits, `checkout <sha>` | `b477dcb86397cf5c` |
| `n09-ignored-untracked` | ignored untracked file | `.gitignore *.tmp`, commit, write ignored `scratch.tmp` | `2f30385bc3b69296` |

## The 7 NEW honest classes (n10–n16)

Ordinary `git init` repository states not in the round-46 set. Reason column is why a fence that refuses them is
over-refusing (the honesty case) — stated from the base fence *description* and the git command, never from a
repaired fence and never from a fence verdict.

| fid | class | git operations | why honest | tool/argv | tree_sha256 (16) |
|---|---|---|---|---|---|
| `n10-empty-repo` | fresh init, zero commits | `git init -b master` only | the state a fixture is in before its first commit; unborn `refs/heads/master`, empty `refs/*`, no index/logs/object | anchor `--lane repo` | `18993be152d5b138` |
| `n11-multibranch` | three local branches, one slash-named | claims commit → `branch feature`, `branch release/v1`, feature commit, receipt commit | `git branch`/`checkout` write only under `.git`; nested ref name is `git branch release/v1`'s own shape | **order** `--lane repo --claims plans/round-48-claims.md --receipt corpus/evidence/round48/fixture-order-receipt.txt` | `4b3373f96146f2b5` |
| `n12-local-config-user` | `[user]` identity in local config | `config --local user.name/user.email`, commit | two inert string keys; name no path, run no program, redirect nothing | anchor | `4ae5ef0959f37933` |
| `n13-remote-origin` | `[remote "origin"]` | commit, `remote add origin https://example.invalid/…` | inert remote declaration; no fetch, hermetic `example.invalid` URL, gated tools never contact a remote | anchor | `2df1b6c090aa4961` |
| `n14-stash-entry` | one stash push | commit, edit, `stash push` | writes `refs/stash`, `logs/refs/stash`, `ORIG_HEAD`, 2 stash commits — all inside `d` | anchor | `2bc9df7ef61fbb2a` |
| `n15-commit-graph` | commit-graph | 2 commits, `commit-graph write --reachable` | `objects/info/commit-graph` is not a store redirect; `gc` writes it too | anchor | `b8983120df277023` |
| `n16-notes-ref` | notes namespace | commit, `notes add -m …` | `refs/notes/commits` + its reflog, written and read inside `d` | anchor | `0b88c06652999f1b` |

`n11` is the only `order`-shaped novel fixture: its claims blob is committed before the receipt and no `claims/`
blob carries a gate `P10` or `CASE … observed=` line, so the fixture is contract-shaped for
`plans/order_check.py` as well as for the fence. (`order_check.py` was **not** run — that would be a probe of
claimed work.)

## Identity scheme (and why a receipt is a reproducible statement)

Per fixture, `tree_sha256` = sha256 over the sorted canonical entry list — `D <rel> <mode>` per directory,
`F <rel> <mode> <content-sha256>` per regular file. Masked: `.git/index` at any depth, the only non-reproducible
byte set (git's inode/mtime stat cache; the round-44 counter's own `fingerprint()` skips it too). Measured, not
assumed: the first builder run masked `.git/index` only at the fixture root and reported most battery fixtures
non-deterministic — every module whose repo sits below the fixture dir (`repo/.git/index`); after the mask was
made depth-independent every fixture is `deterministic=1`.

Each fixture is built **twice** into separate parents (`--repeats 2`) and the normalized digests compared, so
`deterministic=1` is a two-sample statement. Identity is normalized: `argv` tokens under the fixture dir are
rewritten to `{WORK}`, repo entries carry `repo.name` only, so **no absolute scratch path enters any receipt**
(`grep -rl '/fast/scratch' identity.jsonl receipts/ population.txt builder-receipt.txt` → none).

Guards in the builder (`--assert-base`, default on), which is how "authored against the BASE fence description
only" is enforced rather than asserted:

```
GUARD base-fence-ok plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
GUARD builder-ok plans/round44_c1_verify.py sha256=6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad
GUARD lane-rev-ok a543d92083557dd9b33ee674e9b99b03411f80af
```

A repaired fence in the tree makes the authoring provenance unprovable, so the builder refuses (`SETUP … is not
the base fence …`) instead of rebuilding. `--no-assert-base` exists for a later rebuild at another revision.

## Commands and observed outputs

Scratch: `export TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1ExecHonest`; one shared clone,
`git clone --shared --quiet <lane> lane && git -C lane checkout -q a543d92…` (`rev-parse --show-toplevel` →
`/fast/scratch/hyaku/kengaku-r48/R48C1ExecHonest/lane`).

```
$ python3 $W/build_honest_population.py --lane $TMPDIR/lane --modules $W/modules --out $W \
      --work $TMPDIR/work --jobs 8 --repeats 2
REV a543d92083557dd9b33ee674e9b99b03411f80af
POPULATION population.txt sha256=70804edeaaf7bc297fac33a88867de59a1c1413addae3d02d32f91ea497bc7da fixtures=120
MODULE-MANIFEST modules.sha256 sha256=51bfcfc4c9e6b664663f2ce5cfc8e5034808669bac3f0543d3915c1cdad11140 modules=38
BUILDER build_honest_population.py sha256=3cdadac39efc93e1a2c20ba9efa34b136c322d45f4cd2f296b188b0d0e69b427
MODULES dir=/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-48/w1/R48C1ExecHonest/modules repeats=2 jobs=8
MASK .git/index
COUNTS battery42=29 battery43=42 battery44=33 r46novel=9 novel48=7
GUARD base-fence-ok … GUARD builder-ok … GUARD lane-rev-ok …
HOST git=git version 2.56.0 python=3.14.8 platform=Linux-7.2.11-arch1-1-x86_64-with-glibc2.44
SCORED none (no fence, gate or counter executed; stage-2 freeze absent at a543d92083557dd9b33ee674e9b99b03411f80af)
DURATION seconds=8.5
CHECKS all-ok
PREDICATE POPULATION ok
```

Reproducibility (the population file is a pure function of the lane tree + modules, not of the run):

```
$ cmp -s pop-run1.txt population.txt && echo "population.txt byte-identical across runs"   # jobs 8 → 4
population.txt byte-identical across runs
$ cmp -s id-run1.jsonl identity.jsonl && echo "identity.jsonl byte-identical across runs"
identity.jsonl byte-identical across runs
$ cmp -s pop-run2.txt population.txt && echo "population.txt identical (jobs 4 -> 8)"
population.txt identical (jobs 4 -> 8)
```

Consistency across all 120 receipts (`identity.jsonl`):

```
fixtures 120
dup fids []
det 120
tools {'anchor': 85, 'order': 35}
all fsck0 True
all toplevel True
any symlink/special/hardlink: False
```

Structural honesty audit (in every receipt): `symlinks=0 specials=0 hardlinks=0 gitdir_inside=1` for all 120; and
`rev-parse --show-toplevel` equals the repo directory (round-44 rule R4), `git fsck --strict` exit 0. A fixture
with no indirection and a `d`-internal gitdir cannot read outside `d` to decide anything — that is the honesty
claim this seat can make **without** running a fence over it.

Sample receipt (`receipts/novel48/n11_multibranch--n11-multibranch.json`):
`files=49 dirs=42`, `head=3738f316c5d7d27d073b9efbd5903c537654bd1f`, refs
`refs/heads/feature`, `refs/heads/master`, `refs/heads/release/v1`, `fsck_rc=0`, `toplevel_ok=true`.
Sample (`…/n10_empty_repo--n10-empty-repo.json`): `files=18 dirs=10`, `head=null`, `refs=[]`, `fsck_rc=0`.

No fence, gate or gated tool was executed at any point; no counter output was produced or copied.

## Coordination

`R48C1ExecControls` (C1 controls seat) needs this population for the base-fence control @`0f77f9b` (the control
only reaches `HONEST … refused>=9` if the 9 rebuilt classes are present). Handed over by message with the final
digests above; the artifacts stay in the lane wave dir (citable), and no write went into another seat's scratch.
Two earlier digests (`efbc74…`, `e6a682…`) were superseded by receipt-field fixes; the final value
`70804ede…` reproduced across three runs and was sent as a correction.

## Limits (named)

1. **No scored measurement.** No fence verdict exists for any of the 120 fixtures. Admission of the population is
   measured by the stage-2-pinned counter at scoring time; nothing here says the base or any repaired fence
   admits them.
2. **`novel48` is this seat's authoring.** If a critic finds one of n10–n16 not an ordinary `git init` state, that
   is a defect of *this population* (drop it before stage-2 pinning, with the drop reported), not a fence defect.
   The honesty arguments for n13 (remote) and n15 (commit-graph) are the two a fence author could most reasonably
   contest; both are inert store/worktree metadata inside `d`.
3. **Identity excludes `.git/index`.** Two builds that differ only in git's stat cache share a digest. The index is
   the only masked path; everything else is content-addressed.
4. **Host-sensitive bytes.** `hooks/*.sample` and `info/exclude` come from the installed git (2.56.0 here) and are
   part of the identity digest, so a rebuild on another git patch level can move digests without any fixture
   changing. The stage-2 pin is therefore a pin for this host's git; `builder-receipt.txt` records the version.
5. **Anchored to the authoring tree.** `--assert-base` pins lane `a543d920` and base fence `05d5fe03…`; a rebuild
   after the repair must use `--no-assert-base`, and the guard lines then report the tree it actually ran on.
6. **Executable-bit and mode bits are in the identity.** Fixtures built under a different umask would differ; the
   builder runs under the pinned `Ctx.ENV` only for git, not for `ctx.write`, which uses the process umask.
7. **Battery fids are reused names.** `fid` uniqueness is asserted across the frozen population (0 duplicates); it
   is keyed `(population, module, fid)` in the receipts because the battery convention does not promise global
   uniqueness by itself.

## Risks for the repair (not a recommendation, an observation)

The base fence's three refusal mechanisms each have a frozen honest class that trips it: `.git/HEAD` must be a
`ref: refs/heads/…` line (n03, n08 detach it), `_refs` accepts only `heads`/`tags` (n14 `refs/stash`, n16
`refs/notes`), and `_config` allowlists `[core]` keys only (n12 `[user]`, n13 `[remote "origin"]`); `_objects`
requires `objects/info` to be empty (n15 `commit-graph`). The nine round-46 classes additionally trip the
plain-init allowlist through `packed-refs`, tag objects, merge commits and expired logs. A repair that keeps the
allowlist shape must therefore widen exactly these four classifiers — and the frozen kill rule still refuses any
admission that has traced outside access, so widening them costs nothing on the hostile legs.

## Sources (opened this seat; access date 2026-10-27)

| source | opened as | located quote (≤25 words) |
|---|---|---|
| `plans/round-48-claims.md` | `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` | "a fixture result is `LEAK` only if traced opens/reads outside `d` are observed (§C1 (b))" |
| `corpus/lessons/round-46-verifier-spotcheck.md` | `file://…/corpus/lessons/round-46-verifier-spotcheck.md` | "repair over-refusal (9/9 novel honest controls refused) and broaden positive controls" (Routed defects 1) |
| `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` | `file://…/.ufo/waves/round-46/w2/R46W2C1HoHonest.md` | "packed refs after `gc`/`pack-refs`, annotated tags, detached HEAD, a merge commit, `.gitignore`, a 30-commit linear history" |
| `plans/fixture_fence.py` @ `a543d920` (base) | `file://…/plans/fixture_fence.py` | "admit only a fixture whose git store is provably the shape a plain `git init` + commits writes inside `d`" |
| `plans/round44_c1_verify.py` @ `a543d920` | `file://…/plans/round44_c1_verify.py` | "`build(ctx, d)` fills the EMPTY directory d and returns the tool argv tail as a list of str" |
| `plans/round46_c1_verify.py` @ `a543d920` | `file://…/plans/round46_c1_verify.py` | "the 22 modules of the standing batteries `plans/battery42`, `plans/battery43`, `plans/battery44` (104 fixtures …)" |
| `plans/order_check.py` @ `a543d920` | `file://…/plans/order_check.py` | "FAIL when the freeze commit (the first commit adding <claims>) already contains <receipt>" |

No network source was opened; all sources are local committed lane bytes at `a543d920`.

## Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r48/R48C1ExecHonest` held the clone, the shape probe and the build
work dir; receipts were copied into the wave dir first, and the scratch tree **was removed** before yielding
(verified: `test ! -e /fast/scratch/hyaku/kengaku-r48/R48C1ExecHonest` → true). `/tmp` held three comparison
copies under 1 MB, deleted.

VERDICT: `honest-population-frozen` — 120 fixtures (104 battery @ 22/22 pinned module digests + 9 rebuilt round-46
novel classes + 7 new honest classes n10–n16), all built from the stage-1 freeze, each build twice for a
deterministic per-fixture identity, all `fsck --strict` clean, all `toplevel_ok`, zero symlinks/specials/hardlinks,
`population.txt` sha256 `70804edeaaf7bc297fac33a88867de59a1c1413addae3d02d32f91ea497bc7da` reproducible across
three runs; **no scored counter/probe run made — stage 2 is absent at `a543d920` and at HEAD, so the C1 predicate
is unmeasured and no admission is claimed.**
