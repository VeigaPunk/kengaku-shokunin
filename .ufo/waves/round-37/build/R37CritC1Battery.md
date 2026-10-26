# R37CritC1Battery — is `plans/round37_c1_verify.py` a measurement or a keyhole?

Seat: critic (wave 1). Lane read-only. Scratch: `/fast/scratch/hyaku/kengaku-r37/R37CritC1Battery`
(deleted at the end). All battery modules and raw receipts live beside this file
(`./sidechannel/`, `./attacks/`, `./receipts/`).

State measured: lane tip `a3163e6` ("round-37: C1 battery37 (9 modules, 50 single-defect fixtures …),
working-tree run killed=55/55"); gate digest `ea638822…` (unchanged); a second clone at `44b7298`
(the tip before the battery landed), where `plans/battery37/` did not exist.

## Headline

The predicate *passes* on a two-fixture battery that exercises **none** of the 50 advertised clauses it
"demonstrates". Both print the same `BATTERY`, `MUTANTS` and `PREDICATE` lines and exit 0:

```
$ python3 <clone a3163e6>/plans/round37_c1_verify.py --lane <clone>     # battery37 = my 2 modules
GATE plans/pkg_gate.py sha256=frozen
BATTERY fixtures=16 wrong=0 renamed_disagree=0
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass                                              (exit 0; receipts/predicate3.txt)

$ python3 <clone a3163e6>/plans/round37_c1_verify.py --lane <clone>     # the landed 50 fixtures
GATE plans/pkg_gate.py sha256=frozen
BATTERY fixtures=64 wrong=0 renamed_disagree=0
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0
PREDICATE C1 pass                                              (exit 0; receipts/honest.txt)
```

The counter's own definition is `killed iff some fixture's result differs from the reference`
(`plans/round37_c1_verify.py:24`). Result = `(returncode, set of clause ids printing DEFECT)`
(`:270-278`). Nothing ties the *changed* clause to the mutant's advertised clause, to the fixture's
declaration, or to the subcommand that ran. That is the whole attack surface.

## Impacted axes

**Calibration** (the judge for this seat) directly: the C1 predicate's `killed=55` line is satisfiable
without demonstrating 49 of the 50 advertised classes, so the mismatch count it reports is not evidence.
**Depth** secondarily: the counter's docstring claims a kill is "silencing that one branch", which the
result tuple cannot distinguish from a side-channel flip. **Coverage** untouched — C2 reads none of this.
No landed fixture is shown wrong; the landed 50 are attribute-clean.

## Attack 1 — the P10 clause is an oracle for "which gate am I running under"

`c_rerun` re-runs `spec["probe_cmd"]` as a child of the gate, `cwd = fixture root`
(`plans/pkg_gate.py:267-280`). The probe *file* is pinned by P1 (`frozen_instruments` lists three paths),
but P1 hashes only those files: `python3 plans/tb2_grader_probe.py` puts `<fixture>/plans` on
`sys.path[0]`, and the probe's first statement is `import argparse` (`plans/tb2_grader_probe.py:15`).
An **unpinned, extra** `plans/argparse.py` therefore runs first, inside the gate's P10 child — while the
pinned probe bytes are untouched, so P1 stays green.

The shim walks `/proc/<pid>/stat` to the ancestor running the gate, hashes its bytes, and:
pristine gate (reference and null copies are byte-identical) → write the pinned receipt, P10 `ok`;
any other gate → write the receipt plus one line, P10 `DEFECT`. Module:
`./sidechannel/crit_p10_sidechannel.py` (fixture `crit-p10-sidechannel`, `expect=accept`, `defects=[]`).

```
$ python3 plans/round37_c1_verify.py --lane . --battery-dir …/sidechannel --work "$S/work"
FIXTURE crit-p10-sidechannel expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=15 wrong=0 renamed_disagree=0
MUTANT M02 P2 killed by=crit-p10-sidechannel -- receipt unreadable
…
MUTANT M55 D5 killed by=crit-p10-sidechannel -- d5 quote absent from the capture
MUTANTS total=55 killed=54 survived=1 invalid=0 null_detected=0     (receipts/sidechannel-full.txt)
```

49 of those 54 kills come from **one** fixture whose reference DEFECT set is empty (the other five are
the round-36 battery's); it creates no P2, P3, P4, P5, P6, P7, P8, P9, D4 or D5 defect at all.
M43 survives this fixture (it converts "output is not byte-equal" into a pass — the mismatch is the
trigger), so `./sidechannel/crit_p10_mismatch.py` adds the genuinely single-clause P10 fixture; with both,
`killed=55` on the real lane and `PREDICATE C1 pass` in predicate mode at `a3163e6`
(`receipts/full2.txt`, `receipts/predicate3.txt`).

### 1b — the same kill with no `/proc` and no gate digest: the null check is a single sample

Order in `main()` is fixed: reference loop, renamed copies, **one** null run per fixture, then the mutants
(`plans/round37_c1_verify.py:314-358`). A shim that increments a counter file in its own tree (ignored by
`.gitignore`, so P9 stays clean) emits the receipt for runs 1–3 and a different byte stream from run 4 on
(`./sidechannel/crit_p10_run_order.py`):

```
MUTANT M06 P3 killed by=crit-p10-run-order …
MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0     (receipts/two-full.txt)
```

49 of the 55 kills are this fixture's; `null_detected=0` because the null copy is run exactly once.

## Attack 2 — a kill by crash, and a kill by the wrong subcommand

* **Crash**: the shim SIGKILLs the ancestor gate under any non-pristine gate. Reference
  `(0, frozenset())` vs M06 `(-9, frozenset())` — the counter keeps non-0/1 codes "as they are" and counts
  a kill (`./attacks/crit_p10_crash.py`, `MUTANT M06 P3 killed by=crit-p10-crash`, counter exit 0,
  `receipts/show-crash.txt`, `receipts/crash.txt`). A 900 s hang is the same difference shape via
  `run_gate(..., timeout=900)` → `("timeout", frozenset())` (not run; 900 s per mutant).
* **Cross-mode**: an attribution audit the counter does not perform — for each mutant, is its own clause
  in the reference DEFECT set and gone from the mutant's, and does the killing fixture use the mutant's
  subcommand? Landed battery: `UNATTRIBUTED=0`. Hostile battery: `UNATTRIBUTED=49`, and for
  M44-M46, M48-M53, M55 the killing fixture is a `package` run that never invokes `d4-line`/`d5-line`
  (`mode_ok=NO`; `receipts/attr-honest.txt`, `receipts/attr-hostile.txt`).

## What the counter catches, and one rule it does not enforce

| attack | module | counter reaction |
|---|---|---|
| probe truncates the mutant gate file | `./attacks/crit_p10_tamper.py` | `invalid(mutant file changed during the run)`, exit 1 (`:377`) |
| fixture keys on its own directory name | `./attacks/crit_p10_namekey.py` | `RENAMED … DISAGREES`, `renamed_disagree=1`, exit 1 |
| fixture carrying two independent edits | `./attacks/crit_multi_defect.py` | **not caught** — `FIXTURE crit-multi-defect declared=P3,P8 … ok` |

The renamed check is sound for name-keying but blind to what actually executes: it copies fixtures and
rewrites `str(d)` in argv (`:334-344`); the gate copies are never renamed, and the hostile fixtures key on
content, so they show `renamed_disagree=0`.

## Integrity: fixture code runs with the counter's privileges, unsandboxed

`build(ctx, d)` is called in-process (`:309`), *after* `gate_src`/`gate_ok` were computed. A builder —
and the P10 probe, which can read `--spec` from its ancestor's cmdline — can rewrite the lane being
measured while the counter prints `sha256=frozen`:

```
$ python3 <clone>/plans/round37_c1_verify.py --lane <clone> --only M01   # ./attacks/crit_build_write.py
GATE plans/pkg_gate.py sha256=frozen
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
clone gate now: d4b373e5…   (freeze ea638822…)

$ … --only M06                                     # ./attacks/crit_lane_write.py (run-time, via P10)
GATE plans/pkg_gate.py sha256=frozen              … survived=1 invalid=0
clone gate now: 2f3fb763…   (freeze ea638822…)
```

Only the mutant copy is re-hashed after a run; the reference gate, the fixtures, the spec and the lane are
not. Both probes refuse to write when the derived lane is the real lane; both demos ran on clones.

## Finding about the freeze's own rule

The work order and commit `a3163e6` call these "single-defect fixtures"; the frozen claims encode only
"declares `expect` and its exact `DEFECT` clause set" (`plans/round-37-claims.md:34-36`), so the counter
matches the frozen text and the stronger rule lives outside it. The counter compares only
`declared == observed DEFECT set`; it has no notion of edit count, so `./attacks/crit_multi_defect.py` (one-word quotes **and** deleted README) is `ok`. The landed
modules already declare sets of 2–4 clause ids (`plans/battery37/p23.py:130`, `p4.py:90-91`, `p7.py:100`,
`p910.py:101-103`) — mostly one edit with several consequences, but the counter cannot tell that from two
edits. The landed battery itself is clean on attribution (`UNATTRIBUTED=0`), so C1's current pass is not
*false*; it is *uninformative*: the identical `MUTANTS` and `PREDICATE` lines are reproducible without
touching a single advertised branch.

## Reproduce

```
S=/fast/scratch/hyaku/kengaku-r37/<seat>; mkdir -p "$S"
# predicate mode, hostile battery (clone so plans/battery37 can be replaced; lane untouched)
git clone -q --shared <lane> "$S/clone" && test "$(git -C "$S/clone" rev-parse --show-toplevel)" = "$S/clone"
rm -f "$S/clone/plans/battery37"/*.py
cp <this dir>/sidechannel/*.py "$S/clone/plans/battery37/"
python3 "$S/clone/plans/round37_c1_verify.py" --lane "$S/clone"        # PREDICATE C1 pass, exit 0
# development mode against the real lane, one attack at a time
python3 <lane>/plans/round37_c1_verify.py --lane <lane> --battery-dir <this dir>/attacks --only M06 --work "$S/work"
```
Every module exports `FIXTURES` only (import-safe), and each `build()`/probe refuses to write when the
lane it derives is the real lane.

## Smallest safe correction (ordered, each cheap)

1. **Attribute the kill** in `differs()`: count it only when `clause in ref_bad`, `clause not in mut_bad`,
   the killing fixture's `defects` declares `clause`, and the fixture's `argv[0]` matches the clause family
   (`package` for P*, `d4-line` for D4, `d5-line` for D5). Print the changed clause. This alone turns
   `UNATTRIBUTED=49` into 0 and defeats every attack above except the tamper control (which stays `invalid`).
2. **Interleave the null copy** (one null run after every k mutants) and rebuild/hash each fixture between
   runs; a single null sample cannot see a run-order trigger.
3. **Make the gate copies uniform** (same basename in per-mutant dirs) so `/proc` paths carry no mutant id;
   run the probe with `python3 -P` so `<fixture>/plans` cannot shadow stdlib. Both need a gate change —
   frozen this round, so record as a limit, not a silent edit.
4. **Hash what you measure**: gate, spec and the files fixtures may touch, before and after the whole run,
   and re-check `gate_ok` at the end; run `build()` in a child process.
5. Keep P10 as an advertised clause, but do not let a fixture decide *whether* its own probe is inspected:
   a P10 fixture should be built so the probe fails for a stated, checkable reason.

## Limits of this critique

Attacks are observational (the freeze's own standard): I show that `killed=55` is reachable without
demonstrating the classes, not that any landed fixture is wrong — the landed 50 are attribute-clean and the
freeze's 5 demonstrated classes (M01, M05, M40, M47, M54) reproduce exactly on a clone at `44b7298`
(`killed=5 survived=50`, `PREDICATE C1 fail`, `receipts/predicate.txt`). The 600 s / 900 s timeout paths
were reasoned from code, not run.

VERDICT: c1-counter-gameable-yes-9-attacks
