# R39BatP1 — battery39 P1 fixture for M02 (executor, round 39 wave 1)

Seat: R39BatP1 (leaf executor). Lane read from scratch clone only; no lane file touched. Scratch
`/fast/scratch/hyaku/kengaku-r39/R39BatP1` (NVMe), removed at the end.

## Deliverable

One file, written only under the wave build dir:

- `.ufo/waves/round-39/build/R39BatP1/battery/p1m.py` — 39 lines, stdlib only (`pathlib`), one fixture,
  `FIXTURES[0].fid = "p1m-second-pin-appended-bytes"`, `expect="reject"`, `defects=["P1"]`.
  sha256 `a82fa251ca1bd4041d8bec2badac3e6fe3ba53f2f1427baee685b5571e0c1c3e`:
  `sha256sum …/battery/p1m.py` → the same string. `py_compile` ok. Side-channel token scan
  (`grep -nE "/proc|ppid|cmdline|psutil|environ" p1m.py`) → no match.

Mutant targeted: **M02**, clause `P1`, direction `silence`
(`plans/round39_c1_verify.py`, `MUTANTS` row: `bad = [... for rel, dig in pins.items() ...]` →
`bad = [... for rel, dig in list(pins.items())[:1] ...]`; advertised “every frozen instrument is checked
against its pin, not only the first”).

Fixture: the GENUINE round-35 package (`ctx.genuine_package`), appended bytes on the **second** pinned
instrument (`OFF_PIN = b"\n# p1m off-pin witness byte\n"`), pin order read from
`ctx.spec["frozen_instruments"]` (`rels[1]`, never hardcoded; `len(rels) < 2` raises instead of degrading to
the first pin), then index-only `ctx.git_add(d)` so P9 sees no untracked file. argv
`["package", "--root", <d>, "--require-clean-tree"]`; no fixture-owned spec.

## Calibration

### 1. Raw attribution (reference vs M02 on the built fixture)

Command (scratch, `$S=/fast/scratch/hyaku/kengaku-r39/R39BatP1`): build via `p1m.FIXTURES[0]["build"](ctx, d)`
with `r37.Ctx`, then run the frozen gate source and the one-line M02 replacement on the same dir with the
frozen spec. Output:

```
== ref rc=1
P1 DEFECT pinned=3 mismatched=['plans/round35_c1_verify.py']
P2 ok receipt_sha256=pinned
P3 ok rows=22 distinct_quotes=22 distinct_lines=22 out_of_word_range=0
P4 ok checked=22 bad=0 first=0
P5 ok manifest_entries=6 bad=0 first=0
P6 ok rows=3 bad=0 first=0
P7 ok source_lines=3 bad=0 first=0
P8 ok index_rows=45 knowledge_files=45 bad=0 first=0
P9 ok untracked=0 first=0
defects=1
== M02 rc=0
P1 ok pinned=3 mismatched=0
… (P2–P9 byte-identical to the reference; defects=0)
```

The DEFECT set on the unmodified gate is exactly `{P1}` (declared `defects` matches, no extra clause), the
reference exit code is 1 (`expect="reject"`), and the mutant flips only `P1` to `ok` with rc 0 — the declared
silence. Same shape as pre-freeze witness W-X01
(`.ufo/waves/round-38/falsify/F38XMutP/witness-run.txt`: `ref P1,P9 -> mutant P9`); P9 is absent here because
the mutation is staged, so the fixture's clause set is the minimum.

### 2. Counter run, development mode (M02 only)

```
$ python3 …/plans/round39_c1_verify.py --lane "$S/lane" --battery-dir …/round-39/build/R39BatP1/battery \
    --only M02 --work "$S/w"
PINS total=26 mismatched=0
FIXTURE p1m-second-pin-appended-bytes expect=reject declared=P1 observed_rc=1 observed_defects=P1 ok
BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M02 P1 silence killed by=p1m-second-pin-appended-bytes -- every frozen instrument is checked against its pin, not only the first […]
MUTANTS total=1 killed=1 survived=0 invalid=0 null_detected=0
PREDICATE C1 n/a (non-default battery or mutant subset)
```

`renamed_disagree=0` (the fixture carries no absolute path in its bytes; argv is rewritten consistently) and
`null_detected=0` (the copy-run of the same gate reproduces the reference result on this fixture).

### 3. Load-bearing table (delete the fixture in turn)

The module holds exactly one fixture; deleting it is the only leave-one-out variant.

| module variant (`--battery-dir`) | `fixtures=` | M02 result |
|---|---|---|
| `p1m.py` as delivered | 87 | `killed by=p1m-second-pin-appended-bytes` |
| `p1m.py` with `FIXTURES = []` | 86 | `SURVIVED exhibits=none` |

Deletion run (same command, `--battery-dir "$S/empty"`):

```
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M02 P1 silence SURVIVED exhibits=none -- every frozen instrument is checked against its pin, not only the first […]
MUTANTS total=1 killed=0 survived=1 invalid=0 null_detected=0
```

So the kill is the fixture's, not an artefact of module import or of the round-36/37/38 battery.

### 4. Full default counter in the clone (module at `plans/battery39/p1m.py`)

```
$ cp …/battery/p1m.py "$S/lane/plans/battery39/p1m.py"
$ cd "$S/lane" && python3 plans/round39_c1_verify.py --lane . --work "$S/w"
PINS total=26 mismatched=0
FIXTURE p1m-second-pin-appended-bytes expect=reject declared=P1 observed_rc=1 observed_defects=P1 ok
BATTERY fixtures=87 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M01 D5 mirror killed by=d5m-n21-manifest-row-2 -- …
MUTANT M02 P1 silence killed by=p1m-second-pin-appended-bytes -- …
MUTANT M03 P3 silence SURVIVED exhibits=none -- …
MUTANT M04 P7 silence SURVIVED exhibits=none -- …
MUTANT M05 RUN rc-silence killed by=p23-p2-receipt-deleted -- …
MUTANT M06 MAIN rc-mirror killed by=r36-P0 -- …
MUTANT M07 D5 mirror SURVIVED exhibits=none -- …
MUTANTS total=7 killed=4 survived=3 invalid=0 null_detected=0
PREDICATE C1 fail
```

M02 moves from SURVIVED (round-39 do-nothing control: `killed=3 survived=4`) to killed by this fixture;
M03, M04, M07 remain the other seats' scope, so the aggregate predicate still fails at this seat's tip — as
expected for one wave-1 module. `invalid=0` and `mismatched=0` on the clone at tip `7504738` (round-38
non-author spot-check ancestry; the frozen pin set matches).

## Evidence retained here

All numbers above are pasted from this seat's runs; the scratch dirs (`$S/lane`, `$S/w`, `$S/empty`,
`$S/rawwork`) were deleted after copying these lines. No receipt file was kept outside this report by design
(the counter output is the artefact). Commands are reproducible from a fresh `--shared` clone of the lane.

## Risks and limits

- **Discarded variant.** A first version carried five fixtures (second-pin bytes, third-pin bytes, second pin
  missing, spec-owned second-pin digest, spec-owned fourth pin) and printed all five `FIXTURE … ok` with
  `MUTANT M02 … killed by=p1m-second-pin-appended-bytes`, `BATTERY fixtures=91 wrong=0 renamed_disagree=0
  sidechannel=0`. It was reduced to one fixture because with redundant killers no per-fixture deletion flips
  M02 to SURVIVED, which the acceptance requires; the single fixture is also the minimal exact witness shape.
  The other four mechanisms remain unproven as fixtures (they are covered by the same clause line).
- The kill records a result difference in the declared direction (`P1 DEFECT` → `P1 ok`, rc 1 → 0) on a
  package whose other nine clauses are green; it does not measure the fixture's intent beyond that.
- The fixture stages its corruption (`git add -A`) because P9 counts untracked files only; an unstaged variant
  (the W-X01 shape) would declare `{P1, P9}`, which is not needed here.
- Module assumes the frozen spec still pins ≥ 2 instruments; if a future spec shrank to one pin the build
  raises and the counter prints `SETUP …` (rc 2) rather than silently corrupting the first pin.
- No package manager or tool install was performed (host pacman paused; nothing installed).

VERDICT: battery39-p1m-M02-killed-wrong-0
