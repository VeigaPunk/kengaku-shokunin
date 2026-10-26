# R38BatMain — battery38 module `mainx` (frozen mutants N17, N18)

Seat: executor, round-38 wave 1. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(clone of HEAD `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e` under `/fast/scratch/hyaku/kengaku-r38/R38BatMain/lane`,
`git rev-parse --show-toplevel` verified = the clone, then removed). No lane file written; no `git add/commit`
anywhere; no mutating `jj`; no tool installed (nothing needed; pacman not touched).

## Deliverable

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-38/build/R38BatMain/battery/mainx.py`
(47 lines, stdlib only, no import-time side effects)

    e066e19d499c04e12c37275fb45738306cb4e7c38b4af616140cadc5887e3561  mainx.py

Landing path for the L1: `plans/battery38/mainx.py` (single module, both fids carry the `mainx-` prefix).

| fid | mutant | shape | build |
|---|---|---|---|
| `mainx-root-not-a-directory` | N17 (MAIN, silence) | `expect=error`, `defects=[]` | `d` left empty; argv `package --root <d>/absent-root --require-clean-tree` — a path **inside** `d` that exists nowhere (`missing.exists()` asserted False in the builder). |
| `mainx-spec-invalid-json` | N18 (MAIN, silence) | `expect=error`, `defects=[]` | builder writes `d/spec-invalid.json` = `{"rows": {\n` (not JSON) and passes `--root d … --spec d/spec-invalid.json`; the counter's spec-inside-`d` rule is satisfied. |

Both are the counter's MAIN shape exactly: reference exits 2 before any clause line, so the declared defect set is
the observed empty set (counter line: `wrong` requires `res[1] == frozenset([])` and `not res[1]` for `error`).

## Primary run (paste of `.ufo/waves/round-38/build/R38BatMain/receipt-only-N17-N18.txt`, exit=0)

Command (from the lane root, `TMPDIR=$S`):

```
python3 plans/round38_c1_verify.py --lane "$S/lane" \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-38/build/R38BatMain/battery \
  --only N17,N18 --work "$S/w"
```

```
PINS total=14 mismatched=0
FIXTURE mainx-root-not-a-directory expect=error declared=- observed_rc=2 observed_defects=- ok
FIXTURE mainx-spec-invalid-json expect=error declared=- observed_rc=2 observed_defects=- ok
BATTERY fixtures=66 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT N17 MAIN silence killed by=mainx-root-not-a-directory -- a --root that is not a directory is a setup error, exit 2 [docstring 'exit ... 2 = usage/setup'; R37PlanNext B7]
MUTANT N18 MAIN silence killed by=mainx-spec-invalid-json -- an unexpected crash never maps onto 0 or 1 [docstring; R37PlanNext B8]
MUTANTS total=2 killed=2 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

`fixtures=66` = the frozen 64 (round-36 battery 14 + battery37 50) + my 2; `renamed_disagree=0` shows both
fixtures are path-independent under the counter's rename probe; `null_detected=0` shows the byte-identical null
gate reproduces every reference result. `PREDICATE C1 n/a` is the expected development label (`--only` given).

## Mutant exit codes, proved directly (not just via the counter)

Script: copy `plans/pkg_gate.py` bytes three ways in scratch, assert `src.count(old) == 1` for each frozen
`old -> new` (both assert passed), run the two fixture argv shapes. Output:

```
N17 ref: rc=2 stdout=[] stderr=['setup: root not a directory: /fast/scratch/.../p17/absent-root']
N17 N17: rc=1 stdout=["P1 DEFECT pinned=3 mismatched=[...]", 'P2 DEFECT receipt unreadable: ...', "P3 DEFECT no '## Located quotes' section"] stderr=[]
N18 ref: rc=2 stdout=[] stderr=['setup: JSONDecodeError: Expecting property name enclosed in double quotes: line 2 column 1 (char 11)']
N18 N18: rc=0 stdout=[] stderr=['setup: JSONDecodeError: Expecting property name enclosed in double quotes: line 2 column 1 (char 11)']
```

So N17's mutant is **not** 2 — it falls through `if False:` into `cmd_package` on the missing tree, where
`read()` swallows the `OSError`s and `c_captures`' `capdir.iterdir()` raises inside `run_checks`, which catches it
per clause (`plans/pkg_gate.py:297-301`), so the run prints `P1..P8 DEFECT` and exits 1 at `plans/pkg_gate.py:387`.
N18's mutant exits **0** from the mutated handler (`plans/pkg_gate.py:393-395`). Both are in the counter's
`mut[0] in (0, 1)` band, and the reference is exactly 2 for each.

## Load-bearing table (delete each fixture in turn → its mutant flips to SURVIVED)

Scratch-only variant modules (never in the lane), each holding exactly one of the two fixtures with the same
`build` body and fid; receipt `.ufo/waves/round-38/build/R38BatMain/receipt-load-bearing.txt`:

| module | `--only` | fixture lines | BATTERY | MUTANTS |
|---|---|---|---|---|
| without `mainx-root-not-a-directory` | N17 | `mainx-spec-invalid-json … ok` | `fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0` | `killed=0 survived=1` — **N17 SURVIVED** |
| without `mainx-spec-invalid-json` | N18 | `mainx-root-not-a-directory … ok` | `fixtures=65 wrong=0 renamed_disagree=0 sidechannel=0` | `killed=0 survived=1` — **N18 SURVIVED** |

Each fixture is therefore the sole killer of its mutant in this module; no cross-kill (the N18 fixture cannot kill
N17: the crash precedes the root guard, so the N17 mutant still exits 2 on it; the N17 fixture cannot kill N18: the
root guard returns 2 before the handler, so the N18 mutant still exits 2 on it).

## Side-channel scan

`grep -nE '/proc|ppid|cmdline|psutil|environ' mainx.py` → no hits; the counter's own scan agrees
(`sidechannel=0`). The module never inspects which gate copy runs — it only writes fixture bytes and returns argv.

## Risks / notes for the L1

- **`plans/battery38/` does not exist yet** in the lane tree; I wrote only into my report dir as instructed. The
  L1 must copy `mainx.py` to `plans/battery38/mainx.py` for the frozen predicate run; fids are collision-free
  against the 64 frozen fids.
- My module deliberately does **not** reuse `ctx.genuine_package`: neither mutant is reachable once the genuine
  package is in place (N17 needs a missing root, N18 needs an unparsable spec), and both fixtures exit before any
  clause reads tree bytes. The `ctx` argument is accepted but unused in both builders.
- Both fixtures are cheap and hermetic (two `d` writes total: one zero-byte directory state, one 12-byte spec
  file); no git, no probe re-run, no subprocess from the fixture itself.
- `null_detected=0` is measured on the full 66-fixture set, so my two fixtures are also null-stable.
- Untested by me on purpose (wave rule): no build/lint/test run beyond the frozen counter invocations above; the
  L1 owns the full `MUTANTS total=22 killed=22` aggregate and the no-harm re-run of the round-37 counter.
- No `--spec` default-spec assumption is made for N17: the counter appends the frozen r35 spec, which is what the
  reference needs to reach the root guard.

VERDICT: battery38-mainx-killed-2/2-wrong-0
