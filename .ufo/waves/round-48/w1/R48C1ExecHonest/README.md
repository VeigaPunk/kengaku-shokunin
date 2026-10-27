# Round-48 C1 — frozen honest fixture population (seat R48C1ExecHonest)

This directory is the wave-1 executor deliverable for R48-C1 (`plans/round-48-claims.md` §C1 (a)): the honest
population the stage-2 counter pins, its per-fixture build scripts, and their identity receipts. It contains no
counter, runs no fence, gate or gated tool, and makes no admission claim.

## Frozen artefacts

| path | what it is |
|---|---|
| `population.txt` | the frozen population: one `HONEST <tree_sha256> <population> <module>#<build> <fid> <tool>` line per fixture, plus a 4-line provenance header |
| `population.sha256` | `sha256  population.txt` (the stage-2 pin) |
| `modules.sha256` | `sha256  <module>` for all 38 modules the population is built from (22 battery + 16 novel) |
| `build_honest_population.py` | the builder: rebuilds every fixture, checks determinism, writes the receipts and the population file |
| `modules/r46novel/*.py` | the 9 round-46 novel honest classes, rebuilt from `.ufo/waves/round-46/w2/R46W2C1HoHonest.md` |
| `modules/novel48/*.py` | 7 NEW honest classes this seat authored (n10–n16) |
| `identity.jsonl` | one JSON identity per fixture, sorted |
| `receipts/<population>/<module>--<fid>.json` | the same identity, one file per fixture |
| `builder-receipt.txt` | the run receipt: `REV`, population and module digests, guards, per-fixture `IDENTITY` lines, host facts |

## Composition (frozen)

| population | fixtures | source |
|---|---|---|
| `battery42` | 29 | `plans/battery42/*.py` (5 modules) |
| `battery43` | 42 | `plans/battery43/*.py` (7 modules) |
| `battery44` | 33 | `plans/battery44/*.py` (10 modules) |
| `r46novel` | 9 | `modules/r46novel/*.py` (9 modules, one class each) |
| `novel48` | 7 | `modules/novel48/*.py` (7 modules, one class each) |
| **total** | **120** | 85 `anchor`, 35 `order`; 0 duplicate `fid` |

## Consumer contract

The 104 battery fixtures and the 16 novel fixtures use the same contract (the round-44 builder the round-46
counter already imports, `plans/round44_c1_verify.py`):

```python
FIXTURES = [{"fid": str, "tool": "anchor" | "order", "expect": ..., "defects": ..., "build": build}]
def build(ctx, d):   # fills the EMPTY directory d; returns the tool argv tail as list[str]
```

`ctx` offers `ctx.init`, `ctx.git`, `ctx.write`, `ctx.sh`, with pinned git identity and dates, so a build is
hermetic and deterministic. `argv` values are relative (`"repo"`) or `{WORK}`-normalized; no absolute scratch
path enters a receipt. The 16 novel fixtures carry `expect=None, defects=None`: they are inputs to the fence's
HONEST leg, and declare no expectation about the tools' own output.

## Identity

`tree_sha256` is a sha256 over the fixture's canonical entry list — `D <rel> <mode>` per directory, `F <rel>
<mode> <content-sha256>` per regular file, sorted. The only masked path is `.git/index` at any depth (git caches
inode/mtime stat data there; the round-44 counter's `fingerprint()` skips it too). Each fixture is built twice in
separate parents and `deterministic: true` means both normalized tree digests were equal; `repos[].head`,
`refs` (refname + objectname) and `fsck_rc` are recorded per discovered repository.

Repo discovery is "every work-tree directory holding a real `.git` directory"; `rev-parse --show-toplevel` must
equal that directory (round-44 rule R4) and `git fsck --strict` must exit 0.

## Rebuilding

```
python3 build_honest_population.py --lane <lane at a543d920> --modules <this dir>/modules \
    --out <this dir> --work <scratch outside the lane> --jobs 8 --repeats 2
```

The builder refuses to run (`--assert-base`, default on) unless the lane is the stage-1 freeze `a543d920` and
`plans/fixture_fence.py` is the BASE fence `05d5fe03…`: the novel classes were authored against the base fence
*description*, so a repaired fence is not a valid authoring tree. `--no-assert-base` rebuilds at another revision
and reports that tree's fence digest instead; the fences' presence in the header is the authoring-provenance
statement, and the tree digests do not depend on it.

## Limits (named)

- No scored run: no counter, fence, gate or gated tool was executed over these fixtures; stage 2 is absent at the
  frozen revision, so a scored run is not permitted. A fence verdict on any fixture here is unmeasured.
- The population says these states are *honest* (ordinary `git init` repository state, every byte inside `d`); it
  does not say the base or any repaired fence admits them. Measuring that is the counter's job.
- `.git/index` is masked, so two builds that differ only in git's stat cache share an identity.
- The population is host-sensitive in one respect: `hooks/*.sample` and `info/exclude` come from the installed
  git (2.56.0 on this host) and are part of the identity digest.
- `novel48` is this seat's own authoring; a critic seat that finds one of n10–n16 not ordinary should report it as
  a defect of this population rather than a fence defect, and stage 2 decides what to pin.
