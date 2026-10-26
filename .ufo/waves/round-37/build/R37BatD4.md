# R37BatD4 — C1 battery module `d4.py`: M44, M45, M46 (D4 correction-line clause)

Round 37 wave 1, seat R37BatD4 (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Frozen inputs read, not modified: `plans/round-37-claims.md` (C1 section, whole file), `plans/round37_c1_verify.py`
(M44/M45/M46 `old → new` text and the fixture API), `plans/pkg_gate.py` (`cmd_d4`, `single_line`, `run_checks`),
`plans/pkg-spec-r35.json` (`d4.label`, three `d4.patterns`), `plans/round36_c1_verify.py` (`d4_line`,
`build_line_fixtures`).

Gate digest at run time: `GATE plans/pkg_gate.py sha256=frozen` (counter line 1), i.e.
`ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41` — the frozen digest.

## Files changed

Exactly one file written (implementation) plus this report:

- `.ufo/waves/round-37/build/R37BatD4/battery/d4.py` — 3454 bytes, stdlib-only (`import pathlib` only),
  fid prefix `d4-`, 3 fixtures.
  sha256 `6c08d5391f4c9f461bb0b07d9de720bf0cc167a3a558c86f6fef5d0dad171c64`.
- `.ufo/waves/round-37/build/R37BatD4.md` — this report.

Nothing in `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md`,
`SHONEN.md`, nor the lane's index/jj state was touched. No git or jj command was run in the lane.
Scratch `S=/fast/scratch/hyaku/kengaku-r37/R37BatD4` (passed as `--work` and `TMPDIR`) is removed.

The L1 integrates by copying `d4.py` to `plans/battery37/d4.py`; the module itself is location-independent
(it reads all lane bytes through `ctx`).

## What each fixture does (single defect, exact declared set)

The gate's D4 clause (`plans/pkg_gate.py:315-325`) has three decision points; each mutant silences one:

```
lines = single_line(args.file)              # read(): OSError -> None; drops blank-only lines
if lines is None:                           # (a) unreadable
    return False, "file unreadable"
if len(lines) != 1 or not lines[0].startswith(spec["d4"]["label"]):   # (b) count / label
    return False, f"line_count={len(lines)} labelled=False"
bad = [... if not re.search(pat, lines[0])]  # (c) pattern1..3
```

| fid | mutant it must kill | construction | unmodified gate output |
|---|---|---|---|
| `d4-m44-file-unreadable` | M44 `d4 file unreadable` (`return False, "file unreadable"` → `True`) | `--file` names `<fixture-dir>/d4-correction-absent.txt`, never created | `D4 DEFECT file unreadable` → rc 1 |
| `d4-m45-not-one-line` | M45 `d4 file is not exactly one line` (`if len(lines) != 1 or not lines[0].startswith(...)` → `if not lines[0].startswith(...)`) | two non-blank lines; line 1 is the genuine D4 correction line `ctx.d4_line()` verbatim, line 2 is prose with no pattern text | `D4 DEFECT line_count=2 labelled=False` → rc 1 |
| `d4-m46-label-not-carried` | M46 `d4 line does not carry the label` (same guard → `if len(lines) != 1:`) | one line = genuine line with only its label prefix changed to `- **D4 correction note (round 34 C2):**`; every byte after the label unchanged, so all three patterns still match | `D4 DEFECT line_count=1 labelled=False` → rc 1 |

Each declares `expect: "reject"`, `defects: ["D4"]`. `d4-line` runs one clause, so the declared set is the
complete observed set — no second clause can fire, and none does. The two `labelled=False` notes are the
discriminator that each fixture exercises exactly one half of guard (b): M45's shows `line_count=2` with the
label correct, M46's shows `line_count=1` with only the label wrong.

Direct probe of all three (fixtures built from the module itself, gate run at the freeze digest):

```
== d4-m44-file-unreadable argv=['d4-line', '--file', '<S>/probe/d4-m44-file-unreadable/d4-correction-absent.txt'] exists=False bytes=-
   gate stdout: D4 DEFECT file unreadable | defects=1 rc= 1
== d4-m45-not-one-line argv=['d4-line', '--file', '<S>/probe/d4-m45-not-one-line/d4-correction-two-lines.txt'] exists=True bytes=583
   line: - **D4 correction (round 34 C2):** the round-34 C2 row's "candidate counter draft's selftest was not green" is wrong. The counter draft's selftest was
   line: See the round-34 counter draft for the surrounding discussion.
   gate stdout: D4 DEFECT line_count=2 labelled=False | defects=1 rc= 1
== d4-m46-label-not-carried argv=['d4-line', '--file', '<S>/probe/d4-m46-label-not-carried/d4-correction-relabelled.txt'] exists=True bytes=525
   line: - **D4 correction note (round 34 C2):** the round-34 C2 row's "candidate counter draft's selftest was not green" is wrong. The counter draft's selftes
   gate stdout: D4 DEFECT line_count=1 labelled=False | defects=1 rc= 1
```

(gate argv in that probe: `python3 plans/pkg_gate.py <argv…> --spec plans/pkg-spec-r35.json`; long line bodies
truncated at 150 chars only in this transcript. The full genuine line stays intact in the fixture file.)

## Required run, in full

Command (exactly as assigned, `$S=/fast/scratch/hyaku/kengaku-r37/R37BatD4`):

```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round37_c1_verify.py \
  --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
  --battery-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-37/build/R37BatD4/battery \
  --only M44,M45,M46 --work "$S"
```

Output (complete, exit 0):

```
GATE plans/pkg_gate.py sha256=frozen
FIXTURE r36-P0 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-P1 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P2 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P3 expect=reject declared=- observed_rc=1 observed_defects=P3 ok
FIXTURE r36-P4 expect=reject declared=- observed_rc=1 observed_defects=P6 ok
FIXTURE r36-P5 expect=reject declared=- observed_rc=1 observed_defects=P1 ok
FIXTURE r36-P6 expect=reject declared=- observed_rc=1 observed_defects=P9 ok
FIXTURE r36-P7 expect=reject declared=- observed_rc=1 observed_defects=P1,P3,P6,P9 ok
FIXTURE r36-L1 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L2 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L3 expect=reject declared=- observed_rc=1 observed_defects=D4 ok
FIXTURE r36-L4 expect=accept declared=- observed_rc=0 observed_defects=- ok
FIXTURE r36-L5 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE r36-L6 expect=reject declared=- observed_rc=1 observed_defects=D5 ok
FIXTURE d4-m44-file-unreadable expect=reject declared=D4 observed_rc=1 observed_defects=D4 ok
FIXTURE d4-m45-not-one-line expect=reject declared=D4 observed_rc=1 observed_defects=D4 ok
FIXTURE d4-m46-label-not-carried expect=reject declared=D4 observed_rc=1 observed_defects=D4 ok
BATTERY fixtures=17 wrong=0 renamed_disagree=0
MUTANT M44 D4 killed by=d4-m44-file-unreadable -- d4 file unreadable
MUTANT M45 D4 killed by=d4-m45-not-one-line -- d4 file is not exactly one line
MUTANT M46 D4 killed by=d4-m46-label-not-carried -- d4 line does not carry the label
MUTANTS total=3 killed=3 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

Exit code 0 (dev mode returns 0 because `wrong=0`, `renamed_disagree=0`, `survived=0`, `invalid=0`,
`null_detected=0`). Every FIXTURE line of my module ends `ok`; the 14 frozen round-36 fixtures still read
`ok` in the same run (they are always loaded in `--battery full`, dev mode included), so the module does not
disturb the frozen battery. `renamed_disagree=0`: the counter re-ran all 17 fixtures under other directory
names; my three paths are built from the handed-in directory, so the bytes moved with them. `null_detected=0`:
a byte-identical gate copy reproduces all three reference results.

## Load-bearing check (delete one fixture at a time)

Method: same module with one appended filter line — `FIXTURES = [f for f in FIXTURES if f["fid"] != "<fid>"]` —
into a scratch battery dir, driver re-run with `--only M44,M45,M46 --work "$S"`:

| dropped fixture | M44 | M45 | M46 | BATTERY |
|---|---|---|---|---|
| `d4-m44-file-unreadable` | **SURVIVED** | killed by=`d4-m45-not-one-line` | killed by=`d4-m46-label-not-carried` | fixtures=16 wrong=0 renamed_disagree=0 |
| `d4-m45-not-one-line` | killed by=`d4-m44-file-unreadable` | **SURVIVED** | killed by=`d4-m46-label-not-carried` | fixtures=16 wrong=0 renamed_disagree=0 |
| `d4-m46-label-not-carried` | killed by=`d4-m44-file-unreadable` | killed by=`d4-m45-not-one-line` | **SURVIVED** | fixtures=16 wrong=0 renamed_disagree=0 |

Each drop flips exactly the matching mutant to SURVIVED and leaves the other two killed; the surviving
fixtures keep reading `ok` (declarations unaffected). Example, drop `d4-m45-not-one-line`, complete mutant
block:

```
MUTANT M44 D4 killed by=d4-m44-file-unreadable -- d4 file unreadable
MUTANT M45 D4 SURVIVED -- d4 file is not exactly one line
MUTANT M46 D4 killed by=d4-m46-label-not-carried -- d4 line does not carry the label
MUTANTS total=3 killed=2 survived=1 invalid=0 null_detected=0
```

## Cross table: fixture × mutant (no fixture kills a neighbour)

Each gate variant built from the frozen `old → new` text (asserted `count(old) == 1` per mutant), run on each
fixture; cell = `rc:defect-clauses`:

```
fixture                       REF             M44             M45             M46
d4-m44-file-unreadable        rc1:D4          rc0:-           rc1:D4          rc1:D4
d4-m45-not-one-line           rc1:D4          rc1:D4          rc0:-           rc1:D4
d4-m46-label-not-carried      rc1:D4          rc1:D4          rc1:D4          rc0:-
```

Perfect diagonal: each fixture changes exactly one mutant's result and is itself clean under the other two.
This is the single-defect property of the battery, not only of each fixture's label.

## Risks / limits

- The demonstration is observational, as the freeze names (claims §C1 "Limit named at freeze"): each fixture
  shows its branch is reached and its result is visible; it does not show the check is the right check.
- M45's second line is arbitrary prose with no pattern text (`See the round-34 counter draft for the
  surrounding discussion.`); the unmodified gate never reaches the pattern loop on this fixture (guard (b)
  rejects first), and every mutant variant that removes only the count check accepts lines[0] alone, so the
  choice of text cannot affect any of the three mutants. It deliberately contains none of the three pattern
  strings, so it cannot be mistaken for a pattern fixture.
- M46 alters only the label prefix (`correction` → `correction note`), leaving `- **D4 …` shape; a mutant that
  loosened the label check to a prefix such as `- **D4` would not be killed by this fixture. That mutant is not
  in the frozen list, so it is a limit of this freeze, not of this fixture.
- M44's path is inside the fixture directory on purpose: an absolute path outside it would still be relocated
  textually by the renamed run, but keeping it inside means the copy moves no dangling reference and the
  `exists=False` invariant survives the rename.
- The module assumes `ctx.d4_line()` is non-`None` and that the genuine line starts with `spec.d4.label`;
  both hold on the lane and both are asserted with `RuntimeError` rather than silently building a vacuous
  fixture. If a future spec move breaks either, the driver reports `SETUP`/error rather than a false kill.
- Full-battery integration (`plans/battery37/d4.py`) is the L1's step; in dev mode the counter loads the
  battery file from `--battery-dir`, which is what I ran. My module has no dependency on its own path.

VERDICT: battery-d4-killed-3/3-wrong-0
