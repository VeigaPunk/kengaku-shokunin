# `plans/honest49/` — round-49 C1 frozen HONEST fixture population (stage-2 candidate)

Seat `R49C1ExecHonest` (executor), wave `round-49/w1`. This tree is the stage-2 candidate for
`plans/round-49-claims.md` §C1 (a): the honest population the v3 counter pins, its per-module digests, and one
identity receipt per fixture. It contains no counter and runs no fence, gate or gated tool, so it makes no
admission claim and produces no scored measurement.

Built at the round-49 stage-1 freeze `9d2900af41e4d1fc6022eff99010436fde6dbd93` (base fence
`plans/fixture_fence.py` still `05d5fe03…`, round-44 builder `plans/round44_c1_verify.py` still `6cf05323…`).

## Frozen artefacts

| path | what it is |
|---|---|
| `population.txt` | the frozen population: one `HONEST <tree_sha256> <population> <module>#<build> <fid> <tool>` line per fixture, 124 fixtures, plus a 4-line provenance header |
| `population.sha256` | `sha256  population.txt` — the stage-2 pin (`6af8841e…`) |
| `modules.sha256` | `sha256  <lane-relative module path>` for all 42 modules (22 battery + 20 novel) |
| `identity.jsonl` | one identity record per fixture, sorted by (population, module, fid) |
| `receipts/<population>/<module>--<fid>.json` | the same record, one file per fixture (124 files) |
| `builder-receipt.txt` | the run receipt: `REV`, population/module digests, guards, `MASKED` rows, per-fixture `IDENTITY` lines, host facts |
| `determinism/` | two further full builder passes (`population-runB/C.txt`, `identity-runB/C.jsonl`) and `receipt.txt` comparing all three passes |
| `build_honest_population.py` | the builder: rebuilds every fixture, checks determinism, writes the receipts above |
| `modules/r46novel/`, `modules/novel48/` | the 16 round-48 novel modules, byte-identical copies (digests re-checked against `.ufo/waves/round-48/w1/R48C1ExecHonest/modules.sha256`) |
| `modules/novel49/` | the 4 NEW honest classes authored this round (n17–n20) |

## Composition (frozen)

| population | fixtures | source |
|---|---|---|
| `battery42` | 29 | `plans/battery42/*.py` (5 modules) |
| `battery43` | 42 | `plans/battery43/*.py` (7 modules) |
| `battery44` | 33 | `plans/battery44/*.py` (10 modules) |
| `r46novel` | 9 | `modules/r46novel/*.py` (one class each) |
| `novel48` | 7 | `modules/novel48/*.py` (one class each) |
| `novel49` | 4 | `modules/novel49/*.py` (one class each) |
| **total** | **124** | 89 `anchor`, 35 `order`; 0 duplicate `fid` |

The four new classes are ordinary repository states neither earlier set covers:

- `n17_replace_ref` — a `git replace` entry: one `refs/replace/<40-hex>` file.
- `n18_shallow_fetch` — a `.git/shallow` boundary reached by `git fetch --depth 1` from a sibling repository
  inside the same fixture dir (relative `origin` URL `../src`, so no absolute path enters the tree).
- `n19_template_less_init` — `git init --template <empty dir>`: default (unset) `core.hooksPath`, and no hook
  file exists at all, not even a sample.
- `n20_linked_worktree` — a linked worktree whose `.git` is a file (`git worktree add --relative-paths`, git
  2.48+; host git 2.56.0).

## Identity

`tree_sha256` is a sha256 over the fixture's canonical entry list — `D <rel> <mode>` per directory, `F <rel>
<mode> <content-sha256>` per file, sorted. Two volatile sets are masked, each measured rather than assumed:

- `.git/index` at any depth — git's stat cache; the round-44 counter's `fingerprint()` skips it too.
- `.git/worktrees/<name>/index` — the *per-worktree* stat cache of n20's linked worktree, measured as the only
  entry that differed between two n20 builds. No object store, ref, config, reflog or worktree metadata byte is
  masked, and `builder-receipt.txt` prints a `MASKED` row for every excluded entry.

Every fixture is built twice per pass in separate parents; `deterministic=1` means both normalized digests were
equal. Each discovered repository must satisfy `rev-parse --show-toplevel` == its directory, exit 0 under
`git fsck --strict`, and keep its gitdir inside the fixture dir; the structural audit records symlinks, special
files and hard links per fixture (all zero here).

## Rebuilding

```
python3 build_honest_population.py --lane <lane clone at 9d2900af> --modules modules \
    --out <this dir> --work <scratch outside the lane> --jobs 8 --repeats 2
```

`--assert-base` (default on) refuses any other lane revision, any fence other than `05d5fe03…`, and any
round-44 builder other than `6cf05323…`. The `QUIET_ENV` keys (`maintenance.auto=false`, `gc.auto=0`,
`gc.autoDetach=false`) are process environment only: they stop git's detached auto-maintenance from racing the
digest reader and change no repository byte (measured — the pre-quiescence and final passes share one
`identity.jsonl` digest).

## Limits (named)

- No scored run: no counter, fence, gate or gated tool was executed over these fixtures; the stage-2 freeze does
  not exist at the measured revision, so a scored run is not permitted and no fence verdict is claimed.
- The population says these states are *honest* (ordinary repository state, every byte inside the fixture dir,
  no indirection). It does not say any fence admits them; measuring that is the stage-2 counter's job.
- The population is host-sensitive in two respects: `hooks/*.sample`, `info/exclude` and `description` come from
  the installed git (2.56.0 here), and n20 requires `git worktree add --relative-paths` (git ≥ 2.48).
- The tree digests of the 120 carried-forward fids are byte-identical to the round-48 population at the same base
  fence, so a critic can diff the two population files fid by fid.
