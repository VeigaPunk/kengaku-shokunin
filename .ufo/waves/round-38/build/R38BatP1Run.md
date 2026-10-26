# R38BatP1Run — battery38 module for N01, N16 (round 38 wave 1, executor)

Seat: `R38BatP1Run`. Lane read from a shared clone at `/fast/scratch/hyaku/kengaku-r38/R38BatP1Run/lane`
(clone top-level verified equal to that path, `2c5f4e0` = tip carrying the freeze commit `e95cf550`).
Nothing in the lane was written; the module lives only in this report dir and was exercised via
`--battery-dir`.

## Files changed

| path | role |
|---|---|
| `.ufo/waves/round-38/build/R38BatP1Run/battery/b1run.py` | the battery38 module (stdlib only, 48 lines) |
| `.ufo/waves/round-38/build/R38BatP1Run/counter-dev-N01-N16.txt` | verbatim counter output (development mode) |
| `.ufo/waves/round-38/build/R38BatP1Run/load-bearing-n01off.txt` | counter output with the N01 fixture removed |
| `.ufo/waves/round-38/build/R38BatP1Run/load-bearing-n16off.txt` | counter output with the N16 fixture removed |

Module sha256:

```
95a094976b9c5b79be10d06651419806be75555b09e9b4b03118a43a10b15e8d  .../battery/b1run.py
```

Fixture ids: `b1run-n01-empty-pins`, `b1run-n16-clause-crash` (prefix `b1run-`, unique among the fleet
by construction; the counter's duplicate-id check passed).

## What each fixture does

Both use `ctx.genuine_package(d)` (git-init verified + the genuine round-35 package bytes from
`plans/pkg-spec-r35.json`), write a spec **inside `d`**, stage it with `ctx.git_add(d)`, and return
`["package", "--root", str(d), "--require-clean-tree", "--spec", str(spec_path)]`. Staging the spec keeps
P9 clean; carrying `--spec` makes the counter use the fixture's spec instead of the frozen r35 one.

- **`b1run-n01-empty-pins`** — `copy.deepcopy(ctx.spec)` with `frozen_instruments = {}`. Genuine package,
  every other clause passes. Reference: `c_instruments` returns `bool(pins) and not bad`
  (`plans/pkg_gate.py:115`) → `P1 DEFECT pinned=0`, rc 1. Mutant N01 (`return not bad, ...`) → `P1 ok`,
  so the declared clause disappears (silence kill). `defects=["P1"]`, `expect=reject`.
- **`b1run-n16-clause-crash`** — `copy.deepcopy(ctx.spec)` with `entry_rules.quote_words = [3]`. The
  genuine entry parses, then `lo, hi = rules["quote_words"]` (`plans/pkg_gate.py:125`) raises
  `ValueError: not enough values to unpack`; `run_checks` turns it into `P3 DEFECT clause error ValueError`
  (`plans/pkg_gate.py:299`). Mutant N16 flips the handler's `ok` to `True` → `P3 ok`. `defects=["P3"]`,
  `expect=reject`.

Observed DEFECT sets equal the declared sets exactly (FIXTURE lines below), so no surprise clause fires:
emptying `frozen_instruments` fires only P1, and the quote-shape crash fires only P3 (P4/P5/P6 still pass
because the crash is inside P3 only).

## Evidence

### 1. Development-mode counter run

Command (from the clone; `S=/fast/scratch/hyaku/kengaku-r38/R38BatP1Run`):

```
python3 plans/round38_c1_verify.py --lane "$S/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-38/build/R38BatP1Run/battery \
  --only N01,N16 --work "$S/w"
```

Output (full text in `counter-dev-N01-N16.txt`; rc=0):

```
PINS total=14 mismatched=0
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
...
FIXTURE b1run-n01-empty-pins expect=reject declared=P1 observed_rc=1 observed_defects=P1 ok
FIXTURE b1run-n16-clause-crash expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N01 P1 silence killed by=b1run-n01-empty-pins -- an empty frozen_instruments pin set is not an accept [capability row: 'against a spec of pinned digests'; R37PlanNext B1]
MUTANT N16 RUN silence killed by=b1run-n16-clause-crash -- a clause that cannot run is a defect, never a pass [gate run_checks comment; R37PlanNext B6]
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Every FIXTURE line of the module is `ok`, `renamed_disagree=0`, `sidechannel=0`, `null_detected=0`, and
each mutant is attributed to the module's own fid.

### 2. Load-bearing table (fixture deleted in turn)

Variant modules were generated in scratch by dropping one entry from the module's final `FIXTURES` list;
the source module was never mutated. Each variant was run with the same `--lane/--only/--work` shape.

| module variant | fixture count | N01 | N16 |
|---|---|---|---|
| `b1run.py` (both fixtures) | 66 | killed by `b1run-n01-empty-pins` | killed by `b1run-n16-clause-crash` |
| only `b1run-n16-clause-crash` | 65 | **SURVIVED** | killed by `b1run-n16-clause-crash` |
| only `b1run-n01-empty-pins` | 65 | killed by `b1run-n01-empty-pins` | **SURVIVED** |

Verbatim tails (`load-bearing-n01off.txt`, `load-bearing-n16off.txt`), rc=1 each:

```
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N01 P1 silence SURVIVED -- ...
MUTANT N16 RUN silence killed by=b1run-n16-clause-crash -- ...
MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0
```

```
BATTERY fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N01 P1 silence killed by=b1run-n01-empty-pins -- ...
MUTANT N16 RUN silence SURVIVED -- ...
MUTANTS total=2 killed=1 survived=1 invalid=0 null_detected=0
```

Each fixture is load-bearing for exactly its own mutant, and neither fixture is killed by the other's
mutant (the cross direction stays killed independently).

### 3. Side-channel scan

`grep -c -E '/proc|ppid|cmdline|psutil|environ' battery/b1run.py` → `0`; the counter independently
printed `sidechannel=0`.

## Behaviour summary

- `b1run-n01-empty-pins`: `expect=reject`, `defects=["P1"]`, observed rc 1 / `P1`; kills N01 (silence).
- `b1run-n16-clause-crash`: `expect=reject`, `defects=["P3"]`, observed rc 1 / `P3`; kills N16 (RUN).

Both fixtures pass `renamed_disagree=0`, i.e. the spec path inside `d` is rewritten correctly when the
fixture tree is copied to the counter's renamed path.

## Risks / limits

- The N01 fixture proves only the empty-pin direction; a spec with pins that all mismatch is covered by
  other gates/battery (r36 P5 `P1` observed) and is not this fixture's claim.
- The N16 fixture depends on `quote_words` being unpacked as exactly two values in the frozen gate
  (`plans/pkg_gate.py:125`, pinned digest `ea638822…`); the counter's pin check would flag a gate byte
  change before the mutant could be judged invalid.
- Both fixtures stage a fixture-owned spec before P9, so `--require-clean-tree` stays clean; if a future
  landing changed `ctx.git_add` semantics the FIXTURE line would go `WRONG` visibly rather than pass
  silently.
- Development mode prints `PREDICATE C1 n/a`; the full predicate (`MUTANTS total=22 killed=22`) is the L1's
  wave integration run, not this seat's — this seat killed 2/2 of its assigned mutants with 0 wrong
  fixtures.

VERDICT: battery38-b1run-killed-2/2-wrong-0
