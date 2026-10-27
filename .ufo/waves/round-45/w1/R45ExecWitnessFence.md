# R45ExecWitnessFence — a witness `plans/fixture_fence.py` for C1 (round 45, wave 1, calibration)

Axes named: **calibration** (primary — the advertised-vs-observed count on the ten hostile modules and the 104
honest fixtures), **operability** (a fence an L1 can land as it stands), **depth** (each escaped module becomes a
leg that decides from `d`'s own bytes). Coverage / novelty untouched: no C2 surface was read or written.

Leaf seat: no subagents, no background jobs; nothing installed (no tool/version/channel change to record);
nothing in the lane was written — every artifact here is a draft for the L1, produced in my clone and scratch.

## 1. What was built

`plans/fixture_fence.py`, **258 lines**, written only from the contract in this seat prompt (it never imports
`plans/round44_c1_verify.py`; the counter imports that, the fence does not):

- sha256 `a860672ffc2c208c4f3f1476c1a1b64723de441551dec86042f1838ce2813c49`
- witness at `<clone>/plans/fixture_fence.py` while measuring; the byte-identical copy for integration is
  `w1/R45ExecWitnessFence/fixture_fence.py`.

Interface exactly as frozen: `breach(d: pathlib.Path, argv: list[str], tool: str) -> str | None`.

Legs, static first (no subprocess — nothing outside `d` can be parsed before the verdict), git second:

| leg | rule | refuses |
|---|---|---|
| a argv | order argv exactly `--lane V --claims V --receipt V`; anchor argv `--lane`, `--evidence-ref`, `--verbose` only; every value that names a path resolves inside `d` | `--claim`/`--receip` abbreviation, `..`, absolute-outside |
| b walk | no symlink under `d` resolves outside it | symlinked include/store |
| c git store | `.git` FILE: its `gitdir:` target must resolve inside `d`; `.git` DIR: no `commondir`, no `config.worktree`, no `objects/info/alternates`; no `.git/config*` text carrying `[include`/`[includeIf` or `worktreeconfig` | f1, f4, f5, f7, f8, f10 |
| d above | no `.git` above `d` up to the module build root (`d.parent`) | f6 |
| e store probe | for every repo under `d`: `rev-parse --absolute-git-dir` and `--show-toplevel`, `GIT_CEILING_DIRECTORIES=d.parent`, no stdin, 30 s timeout; rc != 0 is a breach; gitdir must be inside `d`, toplevel exactly the repo | f2, f9 |
| f lane probe | when `--lane` lies inside a repo found under `d`: `rev-parse --show-toplevel` bounded the same way, toplevel inside `d` | f2, f9 |

## 2. Before / after (measured, not quoted)

Envelope for every run below: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/claims/envelope.sh "$S/env" …`
(home read-only, `~/.cache` overlaid from scratch, content digest of `~/.local/bin` before/after).
All nine runs: `local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged` — no measurement invalid.

**Before — the round-44 fence** (control `w1/R45ExecWitnessFence/control-r44-selfcontained.txt`). The claim-dir
adapter `claims/fences/r44_tail.py` is *not self-contained* (§6.2), so I sliced the five leg functions plus
`PIN_CHECK_ENV`/`GIT_TIMEOUT`/`ORDER_SHAPE`/`ANCHOR_OPTS`/`PATH`/`GIT_PINS` by AST out of the pinned
`plans/round44_c1_verify.py` (asserted digest `6cf05323…48ad`) and wrapped them in that adapter's `breach`
(`w1/R45ExecWitnessFence/r44_fence_selfcontained.py`, 159 lines, sha256 `4a1f33068fa8c4c7ccd8342d8199c36a7a3c01acc671b96b5be7ababc5d8dc8a`):

```
FENCE plans/fixture_fence.py sha256=4a1f33068fa8c4c7ccd8342d8199c36a7a3c01acc671b96b5be7ababc5d8dc8a
REFUSALS total=10 clean=3 leaked=3 read=4 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=7
PREDICATE C1 fail
```

This independently reproduces the frozen `claims/control-c1-fence-r44.txt` line for line, per module
(f7/f8/f9 `LEAKED`, f1/f4/f6/f10 `READ`, f2/f3/f5 clean) — the round-44 fence's **125** outside opens on the seven
contradicted modules (6+1+3+95+16+4, f9 0). `ENVELOPE start 23:35:13` / `end 23:35:49 exit=1 … unchanged`.

**After — the witness** (`w1/R45ExecWitnessFence/witness-run1.txt`, `witness-run2.txt`):

```
PINS total=33 mismatched=0
FENCE plans/fixture_fence.py sha256=a860672ffc2c208c4f3f1476c1a1b64723de441551dec86042f1838ce2813c49
REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=0
PREDICATE C1 pass
```

Run 1 `ENVELOPE start 23:31:30` → `end 23:31:40 exit=0 … unchanged`; run 2 `start 23:32:12` → `end 23:32:22
exit=0 … unchanged`. Command (`--lane` = clone, `--work` = scratch outside the lane, both under the envelope):

```
envelope.sh "$S/env" /usr/bin/python3 "$S/lane/plans/round45_c1_verify.py" --lane "$S/lane" --work "$S/work" --jobs 4
```

All 13 refusal fixture runs print `opens=0`; all 104 honest runs print `ADMIT opens=0`. So on the frozen surface
the witness never spawns a git child at all: every refusal is decided from `d`'s bytes.

## 3. Control comparison (every row measured by me under the envelope)

| fence | REFUSALS | HONEST | contradicted | predicate | outside opens on the 7 r44-contradicted modules |
|---|---|---|---|---|---|
| `claims/fences/admit_all.py` | `clean=0 leaked=10` | `admitted=104` | 10 | fail | 0 (nothing inspected) |
| `claims/fences/refuse_all.py` | `clean=10` | `admitted=0 refused=104` | 0 | fail | 0 |
| `claims/fences/static_only.py` | `clean=9 leaked=1` (f6) | `admitted=0 refused=104` | 1 | fail | 0 |
| round-44 fence (self-contained slice) | `clean=3 leaked=3 read=4` | `admitted=104` | 7 | fail | **125** |
| `claims/fences/r44_tail.py` as-is | `clean=0 leaked=10` | `admitted=0 refused=104` | 10 | fail | — (NameError, §6.2) |
| **witness (this seat)** | `clean=10 leaked=0 read=0` | `admitted=104` | **0** | **pass** | **0** |

Receipts: `control-admit_all.txt`, `control-refuse_all.txt`, `control-static_only.txt`, `control-r44_tail.txt`,
`control-r44-selfcontained.txt`. `static_only` fails exactly where the contract says an indiscriminate `.git`
scan must fail (f6 leaks because the repo is above `d`; all 104 honest refused), and `refuse_all` shows the
predicate is not reachable by refusing — the witness is on the only admitted point of that trade-off.

## 4. The minimal delta

Per module, round-44 fence → witness, with the one leg that flips it (all six legs are static; none needs git):

| module | r44 | witness | delta leg |
|---|---|---|---|
| f1 gitdir-outside | READ (6 opens) | BREACH, 0 | c: resolve the `.git` file's `gitdir:` before calling git |
| f2 deep core.worktree | clean | BREACH, 0 | e/f already there (`--show-toplevel` ≠ repo) |
| f3 abbrev argv | clean | BREACH, 0 | a already there (exact order shape) |
| f4 FIFO include | READ (1 open, `git hung`) | BREACH, 0, 0.07 s | c: `[include` text scan of `.git/config*` before any git child |
| f5 alternates | clean | BREACH, 0 | c already there |
| f6 repo above d | READ (3 opens) | BREACH, 0 | d: `.git` at `d.parent` (the module build root) |
| f7 commondir | LEAKED (95 opens) | BREACH, 0 | c: `.git/commondir` present |
| f8 config.worktree | LEAKED (16 opens) | BREACH, 0 | c: `config.worktree` / `extensions.worktreeConfig` text |
| f9 refuse-to-describe | LEAKED | BREACH, 0 | e: rc != 0 from `--show-toplevel` is a breach |
| f10 lane include (regular) | READ (4 opens) | BREACH, 0 | c: same include text scan (decided before `lane_breach` can run git) |

**Minimal delta = one structural move: every leg that can be decided by reading `d` (and its ancestors up to the
build root) runs before the first git child, and rc != 0 is a refusal.** That move contributes exactly six
static predicates — gitfile target, `commondir`, `config.worktree`/`worktreeConfig`, include text, above-`d`,
rc-as-breach — each of which flips a distinct contradiction; no leg is removable (f1, f4/f10, f6, f7, f8 are each
invisible to `git` except by a call that has already opened the outside path). The git legs of the round-44 fence
(F2–F6) are kept unchanged in substance and merely moved after the static pass.

## 5. Adversarial boundary probe (six shapes outside the frozen set, `strace -f -y`, receipt `adv-probe.txt`)

`adv_probe.py` builds each shape under scratch, runs `breach` under `strace -f -y` and counts successful opens
under the probe root but outside the fixture dir (driver's own harness excluded). `ENVELOPE start 23:36:12` →
`end 23:36:14 exit=0 … unchanged`.

```
CASE includeif-outside-regular expect=BREACH got=BREACH opens=0 secs=0.07
CASE include-fifo-outside     expect=BREACH got=BREACH opens=0 secs=0.07
CASE worktreeconfig-no-file   expect=BREACH got=BREACH opens=0 secs=0.08
CASE gitfile-store-outside    expect=BREACH got=BREACH opens=0 secs=0.08
CASE gitfile-store-inside     expect=ADMIT  got=ADMIT  opens=0 secs=0.12
CASE repo-above-build-root    expect=ADMIT  got=ADMIT  opens=0 secs=0.07
ADV all six = ok
```

`[includeIf "gitdir:/**"]`, an `[include]` to a FIFO, a `config.worktree` enabling extension with no second file,
and an outside `gitfile` are all refused with zero outside opens and no hang; an inside-`d` store and a repo
*two* levels above `d` are admitted — the latter is the named limit below.

## 6. Limits and risks (named, measured where possible)

1. **Above the module build root is invisible.** `above_breach` looks only at `d.parent`, the bound the frozen
   contract sets ("up to the module build root"); probe `repo-above-build-root` measures the admit. Inside the
   counter's builder (`dest/f000`, `dest` = build root) this is exactly the f6 shape, which is caught. Do not
   claim more than that in the C1 text.
2. **`claims/fences/r44_tail.py` is not self-contained.** Loaded standalone by the round-45 harness it raises
   `NameError` on the five leg names (they live in `round44_c1_verify.py`), so the counter records every fixture
   as `ERROR` → `REFUSALS clean=0 leaked=10`, `HONEST admitted=0 refused=104` (`control-r44_tail.txt`, fence
   sha256 `a918bb69…b9ffb6`). The frozen `control-c1-fence-r44.txt` was produced from fence sha256 `db71ea2a…4bafcb`,
   which is **not preserved** under `claims/`; my AST-sliced reconstruction (`4a1f3306…dc8a`) reproduces its
   numbers exactly, and is the artifact the L1 should keep if the before-state is re-measured.
3. **An inside-`d` `gitfile` store is admitted** (probe `gitfile-store-inside`) — a store inside the fixture is
   not an escape; the round-44 fence refused every `gitfile`. The frozen refusal set contains only the outside
   form, so this costs nothing, but it is the one place the witness is deliberately looser than round 44.
4. **A `--lane` that is no repository is admitted** (the tool's own setup error), as in round 44. f6 is refused by
   leg d, not by the lane probe, so the ordering matters and is stated in the module docstring.
5. **Calibration is exact only on the frozen 104 + 10.** None of the 104 honest fixtures carries an include, a
   linked worktree, a bare store or a symlink, so the honest side does not pin those legs; the held-out attack and
   non-author source review still ride admission, as frozen.
6. `git`/`python3` must be on the sandbox `PATH`; a git probe that cannot start is a breach, never clean.

## 7. Evidence index (all under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-45/w1/R45ExecWitnessFence/`)

| file | bytes | sha256 |
|---|---|---|
| `fixture_fence.py` (the witness, = what ran) | 10974 | `a860672ffc2c208c4f3f1476c1a1b64723de441551dec86042f1838ce2813c49` |
| `witness-run1.txt` | 11861 | `f0afa945ccac21da9a30356be729fbaf77ab4ba5bd2a1990c1f59cde26e63435` |
| `witness-run2.txt` | 11861 | `8f6c2516644dcadc99e53db164f8807918c65c9a273006543b35f3cc9b53235e` |
| `r44_fence_selfcontained.py` | 8348 | `4a1f33068fa8c4c7ccd8342d8199c36a7a3c01acc671b96b5be7ababc5d8dc8a` |
| `control-r44-selfcontained.txt` | 11487 | `089ddb1cf1f7d18737f93a743580656fb390a544d208f1b035729568d93728c5` |
| `control-r44_tail.txt` | 20344 | `164df9b5aa5bc4fd44ae9f4f31395a08bb5916550f59ab557fc442aae246694a` |
| `control-admit_all.txt` | 10867 | `bf3fe184019f8fa5aec239d61dccf67941ff20d77f1ff6e226f2745c6948340a` |
| `control-refuse_all.txt` | 14483 | `05f4d9fe495e1021e8b1b8f5615873b0780c0c7cab52372479b7ea48d5893c17` |
| `control-static_only.txt` | 15148 | `61f06643b9f9b98cb69f74391e843cab0831750d64d4da37d543bf55aa129e8f` |
| `adv_probe.py` / `adv-probe.txt` | 6649 / 1634 | receipts contain the six-case table above |

Measurement environment: clean clone of the lane at `git -C <clone> rev-parse HEAD`
`05b02e2b7894a9c83219685f2374905e11c1beda`, toplevel verified equal to the clone path; `PINS total=33
mismatched=0` in every counter run (the counter re-checks the 33 pinned digests after the run too). Scratch
`/fast/scratch/hyaku/kengaku-r45/R45ExecWitnessFence` deleted with `plans/scratch_guard.py safe-rm` after the
receipts above were copied here.

VERDICT: witness-fence-pass-yes
