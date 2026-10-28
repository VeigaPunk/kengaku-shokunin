# R49-C1 — `R49C1ExecHonest`: frozen honest population for stage 2

| field | value |
|---|---|
| seat | `R49C1ExecHonest` (executor, leaf) |
| claim served | R49-C1 (calibration) |
| wave | round-49 / w1 (kengaku, hyaku run 10), one v2 build-and-attack wave |
| base (stage-1 freeze) | `9d2900af41e4d1fc6022eff99010436fde6dbd93` |
| measured revision (all receipts) | `REV 9d2900af41e4d1fc6022eff99010436fde6dbd93` |
| date | 2026-10-28 |
| deliverable | `.ufo/waves/round-49/w1/R49C1ExecHonest/plans/honest49/` (tree-shaped, stage-2 candidate) |
| scored runs | **none** — no fence, gate, counter or gated tool executed (`SCORED none` in the receipt) |

## Axes named

- **Calibration** (the axis R49-C1 works): this seat supplies the honest *population* half of the calibration
  measurement — the frozen set the v3 counter's `HONEST fixtures=<H> admitted=<H> refused=0` line is measured
  on, with per-fixture identity receipts so a refusal can be pinned to an exact tree.
- **Correctness-of-evidence** (secondary, enabling): item → artifact traceability — a pinned population digest,
  per-module digests, per-fixture receipts, and two further full passes proving reproducibility.

No other axis is touched: nothing here measures a fence, claims admission, or alters production files.

## 1. Stage-1 freeze verified before any measurement

```
$ git -C <lane> log --format='%H %ci %s' -2 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
3a548330c4899c6c5df34168a44a59f66828ce74 2026-10-27 09:58:06 -0300 round-48 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git -C <lane> merge-base --is-ancestor 9d2900af41e4d1fc6022eff99010436fde6dbd93 HEAD && echo ANCESTOR
ANCESTOR: yes                     # lane HEAD at dispatch = af88aab193e6… (w1 spec commit, descendant)
$ git -C <clone> rev-parse HEAD
9d2900af41e4d1fc6022eff99010436fde6dbd93
$ sha256sum <clone>/plans/fixture_fence.py <clone>/plans/round44_c1_verify.py
05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e  …/plans/fixture_fence.py
6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad  …/plans/round44_c1_verify.py
```

The freeze predates every measurement in this report (freeze 09:14:40 -0300; builder passes 09:24–09:26).
Stage 1 changed only `plans/round-49-claims.md`, so the fence is still the base fence `05d5fe03…` — the
authoring-provenance condition the novel classes were written against. The builder's `--assert-base` guard
re-checks lane rev, fence digest and round-44 builder digest on every run and printed:

```
GUARD base-fence-ok plans/fixture_fence.py sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e
GUARD builder-ok plans/round44_c1_verify.py sha256=6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad
GUARD lane-rev-ok 9d2900af41e4d1fc6022eff99010436fde6dbd93
```

Work was read-only against `git clone --shared` of the lane (clone toplevel verified:
`git -C <scratch>/lane rev-parse --show-toplevel` → `<scratch>/lane`), except my own wave-dir report and the
candidate tree below.

## 2. Deliverable (all under `.ufo/waves/round-49/w1/R49C1ExecHonest/plans/honest49/`)

| path | content |
|---|---|
| `population.txt` | 124 `HONEST <tree_sha256> <population> <module>#<build> <fid> <tool>` rows + 4-line provenance header |
| `population.sha256` | `6af8841e1c4a8dec8c50f03a4633cccab72e0b73f53fb3d12447177cdd23c34e  population.txt` |
| `modules.sha256` | 42 rows (22 battery + 20 novel), lane-relative tree-shaped module paths |
| `identity.jsonl` | 124 identity records, sorted by (population, module, fid) — sha256 `a7fc521f…` |
| `receipts/<population>/<module>--<fid>.json` | 124 per-fixture receipts (identical records) |
| `builder-receipt.txt` | run receipt: `REV`, digests, guards, 125 `MASKED` rows, 124 `IDENTITY` rows, host facts |
| `determinism/receipt.txt` + `population-runB/C.txt` + `identity-runB/C.jsonl` | three-pass reproducibility evidence |
| `build_honest_population.py` | the r49 builder (round-48 builder, re-based + prefix + novel49 + mask/quiescence changes) |
| `modules/r46novel/*.py` (9), `modules/novel48/*.py` (7) | the 16 round-48 novel modules, **byte-identical copies** |
| `modules/novel49/*.py` (4) | n17–n20, authored this seat |
| `README.md` | composition, masks, rebuild command, limits |

Composition (`COUNTS` line, verbatim):
`COUNTS battery42=29 battery43=42 battery44=33 r46novel=9 novel48=7 novel49=4` → **124 fixtures**,
`89 anchor / 35 order`, 0 duplicate `fid`, 42 modules (`modules=42`).

### Copy fidelity of the 16 r48 modules

`sha256sum modules/r46novel/*.py modules/novel48/*.py` reproduces all 16 rows of the round-48
`modules.sha256` exactly (e.g. `9e1a2058… n01_packed_refs.py`, `04919778… n10_empty_repo.py`,
`fabcc598… n16_notes_ref.py`): the carry-forward is byte-identical, not a re-authoring.

## 3. Exact commands run

```bash
S=/fast/scratch/hyaku/kengaku-r49/R49C1ExecHonest
mkdir -p "$S" "$S/work"; export TMPDIR="$S"
git clone --shared -q <lane> "$S/lane"
git -C "$S/lane" checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93

# per-class development probes (scratch-only harness dev/try_novel.py; builds each module twice)
python3 dev/try_novel.py dev/modules/novel49/n17_replace_ref.py      # …n18, n19, n20
python3 dev/diff2.py      dev/modules/novel49/n20_linked_worktree.py # what differed between the two builds

# the three full passes (A shipped into the tree, B and C into scratch)
python3 plans/honest49/build_honest_population.py \
    --lane "$S/lane" --modules plans/honest49/modules \
    --out <tree|"$S/runB"|"$S/runC"> --work "$S/work" --jobs 8 --repeats 2

# carry-forward cross-check against the round-48 population (join on fid, compare tree_sha256/tool/population)
python3 - <tree>/population.txt <lane>/.ufo/waves/round-48/w1/R48C1ExecHonest/population.txt

# artifact integrity
( cd <tree> && sha256sum -c population.sha256 )     # population.txt: OK
# modules.sha256: every row's path resolves and its digest matches (42/42)
```

## 4. Observed outputs (verbatim)

Builder verdict (all three passes, rc=0):

```
POPULATION population.txt sha256=6af8841e1c4a8dec8c50f03a4633cccab72e0b73f53fb3d12447177cdd23c34e fixtures=124
CHECKS all-ok
PREDICATE POPULATION ok
```

`CHECKS all-ok` is the conjunction of: 22/22 battery module digests equal to the round-46 `PINS` table
(`grep -c 'ok=0' builder-receipt.txt` → 0), battery total 104, r46novel 9, novel48 7, novel49 4, no duplicate
fid, no build failures, every fixture `deterministic=1`, every discovered repo `toplevel_ok`, every `fsck_rc=0`,
no fixture without a repository, zero symlinks / special files / hard links, every gitdir inside its fixture.

Population header (verbatim):

```
# HONEST POPULATION round-49 C1 v1
# lane=9d2900af41e4d1fc6022eff99010436fde6dbd93 builder_sha256=3fc30c8e3b70d70f5421b5a2c7a1097b3a79547e02240ac31c78fb4e054bcf31 base_fence_sha256=05d5fe03aa3be6b79eb2469b7c86d0a20c9b424bea2e058d580e31a96c8aad5e builder_tree=plans/round44_c1_verify.py@6cf05323bafa9cdbb7c4dd1613b524b95a591d4ada2f8253150f87534cbe48ad
# columns: HONEST <tree_sha256> <population> <module>#<build> <fid> <tool>
# mask=.git/index .git/worktrees/*/index (volatile; git stat cache)
```

### Determinism — the item's "twice" is discharged three times over

Each fixture is built twice per pass in separate parents (`--repeats 2`, `deterministic=1` on all 124
`IDENTITY` rows), **and** the whole builder ran three times:

```
A(shipped)   population.txt     sha256=6af8841e1c4a8dec8c50f03a4633cccab72e0b73f53fb3d12447177cdd23c34e
B            population.txt     sha256=6af8841e1c4a8dec8c50f03a4633cccab72e0b73f53fb3d12447177cdd23c34e
C            population.txt     sha256=6af8841e1c4a8dec8c50f03a4633cccab72e0b73f53fb3d12447177cdd23c34e
A/B/C        modules.sha256     sha256=efbaed1ea56dd7560822bd62912f566c0fa94b9210f48ba297506273b67acf3b  (all equal)
A/B/C        identity.jsonl     sha256=a7fc521ffdc5f11b84cc6abccd1427ef79c148ac2106193f7ecd5b523618cce2  (all equal)
comparison: every one of the 124 per-fixture receipts byte-equal across A/B/C -> True
```

### Carry-forward cross-check (fid join against round 48)

```
new fixtures: 124 old fixtures: 120
missing from new: []
added in new: ['n17-replace-ref', 'n18-shallow-fetch', 'n19-template-less-init', 'n20-linked-worktree']
digest mismatches on shared fids: 0
tool mismatches: []
population mismatches: []
```

All 120 round-48 fixture tree digests reproduce byte-for-byte at the new base; the four additions are the only
delta. That is the strongest available statement that the carry-forward is faithful.

## 5. The four NEW novel classes (n17–n20)

Byte excerpts below were captured by a scratch-only rebuild of the shipped modules under the same round-44
`Ctx` (git 2.56.0, pinned identity/dates); the authoritative digests are the builder's, in `population.txt`.

| fid | module | tree_sha256 | build fact |
|---|---|---|---|
| `n17-replace-ref` | `n17_replace_ref.py` | `e91ecd9b80fb00c26f65e9a7910a29b5d52da382cac0d79c47e2d33b454c671c` | `git replace <HEAD~1> HEAD` → `refs/replace/4d88795d…` |
| `n18-shallow-fetch` | `n18_shallow_fetch.py` | `9d6d6db9c3bf80d726fcd66cd7d01cf605b0d5d2f72289f63e0db23083e73e2f` | `.git/shallow` boundary after `git fetch --depth 1` |
| `n19-template-less-init` | `n19_template_less_init.py` | `564d1f2b35e2f2cb48fdb54fe74ed528b167454ee1b7e83d5bd9e895dd47b059` | `git init --template <empty>`: no hook file at all |
| `n20-linked-worktree` | `n20_linked_worktree.py` | `1168dfde593e0feef0c5c5138e8f6746933b89cb6f7403f26a55d217a12e12fd` | linked worktree whose `.git` is a file |

**n17 — replace ref.** `for-each-ref` in the built fixture:

```
refs/heads/master e6194a5fc75a12d9135ae7b7ec2c24ac92e1edf3 | refs/replace/4d88795d2b61cd3050f970240b8628e8b6313c90 e6194a5fc75a12d9135ae7b7ec2c24ac92e1edf3
```

One documented ref namespace whose *name* is a 40-hex object id — the exact shape a path-shaped ref check
over-refuses. `fsck=0`, `gitdir_inside=1`, `deterministic=1`, `masked=1` (`.git/index` only).

**n18 — shallow boundary.** The first shape tried, `git clone --depth 1 --no-local src repo`, is **rejected**
with a measured reason: git rewrites the local source to an absolute path, so `.git/config` and all three
reflogs carried the build's scratch path (`diff2.py` showed exactly `config`, `logs/HEAD`,
`logs/refs/heads/master`, `logs/refs/remotes/origin/HEAD` differing between two builds) and no two builds could
share an identity. A promisor/`--filter=blob:none` clone is also rejected: `git fsck --strict` reports the
omitted blobs missing, so the store is not self-contained. The shipped shape — sibling source inside the same
fixture dir, `git remote add origin ../src`, `git fetch --depth 1 origin master`, `git reset --hard FETCH_HEAD`
— gives the shallow state with no absolute path:

```
.git/shallow: da9314e69a1a45b05fd69755f0c6aa7442abdbb1
config [remote] block: url = ../src fetch = +refs/heads/*:refs/remotes/origin/*
FETCH_HEAD: da9314e69a1a45b05fd69755f0c6aa7442abdbb1		branch 'master' of ../src
git log --oneline: da9314e add c.txt          # history behind the boundary is absent, as designed
fsck --strict rc: 0
```

`masked=2` (`repo/.git/index`, `src/.git/index`), `gitdir_inside=1` for both repos, `deterministic=1`.

**n19 — default `core.hooksPath`, no hook file.** `git init -b master --template <empty dir>` then one commit:

```
.git entries: ['COMMIT_EDITMSG', 'HEAD', 'config', 'index', 'logs', 'objects', 'refs']
hooks dir exists: False | info dir exists: False
config: [core] repositoryformatversion = 0 filemode = true bare = false logallrefupdates = true
hooksPath key present: False
fsck --strict rc: 0
```

This is the class the item named: `core.hooksPath` unset (default) and **no** non-sample hook file — indeed no
`hooks/` directory at all — so a fence that passes only because the sample hook set is present will refuse it.

**n20 — linked worktree with a `.git` file (kept, not refused).** The item allowed refusing this class if it
had to fail. It does not:

```
wt/.git type: file= True | content: gitdir: ../repo/.git/worktrees/wt
worktrees/wt/gitdir: ../../../../wt/.git        # --relative-paths: both pointers are relative
worktrees/wt/commondir: ../..
worktree list: … repo  HEAD 4d88795d… branch refs/heads/master | … wt  HEAD 4d88795d… branch refs/heads/feature
absolute path bytes in tree: []
fsck --strict rc: 0
```

It was non-deterministic in its first measurement for exactly one reason: `repo/.git/worktrees/wt/index`, the
per-worktree stat cache, was the **only** entry that differed between two builds (`diff2.py` output: one line,
`F repo/.git/worktrees/wt/index`). Every other byte — `wt/.git`, `worktrees/wt/gitdir`, `commondir`,
`worktrees/wt/HEAD`, `ORIG_HEAD`, `logs/HEAD` — was byte-stable. Keeping the class therefore required the one
named deviation below.

## 6. Named deviation: the identity mask gains one narrow entry (for the L1 to accept or reject at stage 2)

Round 48's rule was "the only masked path is `.git/index` at any depth". This tree masks a second set:
`.git/worktrees/<name>/index`. Justification, measured not asserted:

- it is the *same file* for a linked worktree — git's index, i.e. a stat cache of inode/mtime data — and the
  round-44 counter's `fingerprint()` already skips `.git/index` for that reason;
- the measurement shows it is the only volatile entry (one differing line, above);
- it is masked narrowly: no object-store byte, ref, config, reflog, `gitdir`, `commondir` or worktree metadata is
  masked, and `builder-receipt.txt` prints a `MASKED` row per excluded entry (125 rows: 121 fixtures with one,
  n18 and n20 with two, n10 with none because an unborn repo has no index).

If the L1 prefers the strict single-mask rule, dropping `n20_linked_worktree.py` is the only change needed
(`novel49-total` would become 3 and `<H>` would move 124 → 123); the builder's `NOVEL49_TOTAL` constant and the
`COUNT`/`CHECKS` assertions make any such edit explicit rather than silent.

## 7. Builder change forced by measurement (auto-maintenance race), and proof it changed no byte

A full pass of the re-based builder failed **once** with:

```
BUILD-FAIL [Errno 2] No such file or directory: …/work/k49-honest-lmguikla/gen/r1/76aa01d29eba/f013/repo/.git/objects/maintenance.lock
CHECKS battery-total build-failures=1
PREDICATE POPULATION fail
```

`76aa01d29eba` = `sha256("battery43/a_alt.py")[:12]`, the 14-fixture module: git's `git gc --auto` from a
`git commit` spawns a detached auto-maintenance child (`gc.autoDetach` default true); the child takes
`$GIT_DIR/objects/maintenance.lock` after the commit returned, and the lock raced a tree read. Two guards were
added to the builder:

- `QUIET_ENV` — `maintenance.auto=false`, `gc.auto=0`, `gc.autoDetach=false`, passed as **process environment
  only** (`GIT_CONFIG_*` keys), so no repository byte and no written config changes;
- `retry_read()` — a tree read that hits a vanished entry is re-read (≤5 attempts), a persistent one still raises.

Proof it changed nothing: that pre-quiescence pass's 124 `IDENTITY` lines are byte-identical to this tree's
(`diff <(grep '^IDENTITY ' run1-console) <(grep '^IDENTITY ' builder-receipt.txt)` → no output), and its
`identity.jsonl` digest `a7fc521f…` equals this tree's — exactly the digest the shipped builder produces in all
three passes. Recorded in `determinism/receipt.txt` under `PRE-QUIESCENCE PASS`.

## 8. Stage-2 handoff numbers

- `<H>` candidate = **124** = 104 battery + 9 r46novel + 7 novel48 + 4 novel49; claimed spread 89 anchor / 35 order.
- Population pin: `population.sha256` = `6af8841e1c4a8dec8c50f03a4633cccab72e0b73f53fb3d12447177cdd23c34e`.
- Module pins: `modules.sha256` (42 rows), e.g. `9f38f07a… n17_replace_ref.py`, `64ecb769… n18_shallow_fetch.py`,
  `d28745b7… n19_template_less_init.py`, `75cc4fff… n20_linked_worktree.py`, all under `plans/honest49/modules/…`.
- Identity pin: `identity.jsonl` = `a7fc521ffdc5f11b84cc6abccd1427ef79c148ac2106193f7ecd5b523618cce2`.
- The two pins are disjoint from every other stage-2 literal in `plans/round-49-claims.md`; no predicate line,
  control or kill rule is touched by this seat.

## 9. Limits (named)

- **No scored run.** No counter, fence, gate or gated tool was executed; stage 2 does not exist at the measured
  revision. Nothing here says any fence admits or refuses these fixtures — the base fence's behaviour on the
  extended population is unmeasured by this seat (round 48 measured 8 refusals on the 120; the four new classes
  are exactly the shapes — `refs/replace`, a relative remote + shallow file, a missing hooks dir, a `.git` *file*
  — a store-path/ref-allowlist fence is most likely to over-refuse, but that is a prediction for the counter).
- **Host-sensitivity.** `hooks/*.sample`, `info/exclude` and `description` come from installed git (2.56.0);
  n20 needs `git worktree add --relative-paths` (git ≥ 2.48); n18 relies on the local transport honouring
  `--depth` (verified here, git 2.56.0).
- **n18 is shallow, not partial-filtered**, by design: a self-contained honest store is the precondition, and a
  promisor store fails `git fsck --strict`.
- **n19's "no hook file" is a directory-absence claim**, stronger than the item's wording; a critic who wants
  "samples present, no active hook" should say so, and that state is already covered by every other class.
- **One measurement was flaky before the quiescence guard** (one full pass in three). The shipped builder is the
  guarded one, and its reproducibility is shown by three clean passes, but a fourth pass on a differently loaded
  host is not something this seat measured.
- `MODULES dir=<absolute wave-dir path>` appears in `builder-receipt.txt` as the measured input (round-48
  precedent); it is a receipt fact, not a hardcoded path in any tool.

## 10. Scratch, writes, and boundaries

- Scratch `S=/fast/scratch/hyaku/kengaku-r49/R49C1ExecHonest` (one `git clone --shared`, `TMPDIR=$S`,
  `--work` inside it) — **removed before yield**; `ls -d $S` → `No such file or directory`. Every scratch path
  cited above therefore no longer exists; all citable evidence is in this file or the wave-dir tree.
- Writes were limited to: this report, the `plans/honest49/` candidate tree under my wave dir, and scratch. No
  production file (`plans/*`, `corpus/*`, `SCORECARD.md`, `LOG.md`, …), no commit, no mutating git/jj command in
  the lane, no sibling repo, no `.ufo/state`.
- Every fixture git call ran through the round-44 `Ctx`, which asserts `rev-parse --show-toplevel` equals the
  repo dir before writing; the clone's own toplevel was asserted before any checkout.

## 11. Sources opened

No external URL, paper or web source was opened for this item, so no URL/access-date/quote is due. Sources read
were lane-local: `plans/round-49-claims.md` (§C1 (a)(b)(c)(e)), `corpus/lessons/round-48-verifier-spotcheck.md`
(routed defects 1–4), `corpus/lessons/round-48.md` (§R48-C1 status), the round-48 deliverable
`.ufo/waves/round-48/w1/R48C1ExecHonest/` (`README.md`, `population.txt`, `modules.sha256`, modules) and
`plans/round44_c1_verify.py` (`Ctx`, `fingerprint`). Recorded quotes: spot-check §5 defect 4 — "the candidate's
≥12-mutant kill battery was never reported … Any future C1 admission attempt needs the mutation floor committed
with receipts" (that is the mutation-tester seats' deliverable, not this population's).

## VERDICT

`population frozen (stage-2 candidate): H=124 fixtures, deterministic across 3 full passes and 2 builds per fixture, 120/120 round-48 digests reproduced, 4 NEW classes n17-n20 (n20 kept under one narrowly named worktree-index mask), SCORED none, no admission claimed.`

