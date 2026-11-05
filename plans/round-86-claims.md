# Kengaku round 86 — frozen claims (hyaku run 15, attempt 1, 2026-11-04)

L1: `KengakuR86`. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch `master`.
BASE = `88651a72ef112ed9f5361e1c8c197babec691f96` (round-85 non-author closure tip; the lane state this
round started from). Inherited unlanded work from the earlier attempt of this same round (commits
`0481a6d3`, `c939e6b5`, `bfda0472`, `9972c87c`) is named in the report: the instruments, case table and
the box-4 re-pin are reused after re-verification; nothing is re-declared from an unverified transcript.

Two claims, two distinct axes, causally separable. Neither is exploratory. No claim is re-declared from
a prior round and no target is narrowed after landing.

## R86-C1 — coverage (the lane's lowest non-retired axis, held at its L0 cap)

**Claim.** The lane's executed Terminal-Bench 2.0 grader population, as recorded by
`plans/grader-population-ledger.json`, grows by exactly one member — `raman-fitting`, whose ledger
`classes` are `file-artifact`, `numeric-band` and `serialization-schema` — by a located offline replay
of that member's pinned captured grader over eight frozen schema-drift case shapes, and the counter
`plans/round86_c1_replay.py` prints, at the measured tip, `TARGET members=1 cases=8 legs=24
mismatches=0 located=1 executed=1 defects=0` followed by `PREDICATE R86-C1 pass`, exit 0.

**Frozen predicate (the counter's own condition, unchanged since this file was committed).**

```python
ok = (not defects and stats["members"] == 1 and stats["cases"] == 8
      and stats["legs"] == 24 and stats["mismatches"] == 0
      and stats["located"] == 1 and stats["executed"] == 1)
```

**Target.** `defects=0`, `PREDICATE R86-C1 pass`, exit 0 at the measured tip; `defects=7`,
`located=0`, `executed=0`, `PREDICATE R86-C1 fail`, exit 1 at BASE.

**Counting command.**

```sh
python3 plans/round86_c1_replay.py --lane . --rev <REV> --work <scratch-dir>
```

**Kill rule.** Any `DEFECT` line at the measured tip, or a BASE run that reaches the target, makes the
claim unmet. A target reached only by a tree that is not the measured committed revision does not count.

**Eight legs, one defect line each.** `L1-receipt` (the receipt the ledger names exists),
`L2-stamp` (its stamp carries every required field and its `MEMBER`/`SUBJECT_CAPTURE`/`SUBJECT_SHA`/
`CASE_TABLE_SHA`/`TOOL`/`TOOL_SHA`/`EXIT` agree with the measured bytes), `L3-tip` (its `LANE_TIP`
resolves and is an ancestor of the measured revision), `L4-table` (the case table at the measured
revision is byte-identical to the frozen table read at the freeze revision), `L5-vectors` (the eight
`CASE` lines carry the frozen predicted vectors, `observed == predicted`, `cases=8 legs=24
mismatches=0`, `PREDICATE R86-PROBE pass`), `L6-reproduce` (re-running the pinned tool from the measured
tree reproduces the receipt's observation block exactly), `L7-ledger` (the population ledger row is
`status=executed`, `round=86`, names this receipt, `subject=tb2-header`, `verdict=cases`), `L8-subject`
(the captured grader bytes hash to the frozen `SUBJECT_SHA`).

**Honest limit (stated so it is not overclaimed).** A receipt whose observed vectors are correct *and*
whose stamp names the measured tip and the true digests is not, by observation alone, distinguishable
from a freshly minted one: `L6` reproduces the observation, it does not authenticate an author. `L2`
and `L3` are what a receipt copied in from elsewhere cannot satisfy. The round does not run
Terminal-Bench, the task image or a harness, does not measure model or agent behaviour, and speaks for
this one member's eight frozen case shapes only.

**Controls (run before the tip data run, at the frozen instrument bytes).** `--control-do-nothing`
(BASE tree), `--control-ledger-only` (ledger row rewritten, no receipt), `--control-fabricated-
observations` (receipt with invented observed vectors), `--control-forged-receipt` (receipt minted
from another tree). Each must print `target_reached=False`; a control that reaches the target voids
the claim before any tip run.

**Sourced.** The claim rests on `corpus/SOURCES.md` row **S274**, opened this round: the pinned
`raman-fitting/tests/test_outputs.py` at Terminal-Bench 2.0 commit `2fd12b88`, fetched and byte-compared
against `corpus/evidence/round52/graders/raman-fitting/tests/test_outputs.py`.

## R86-C2 — calibration (held at ceiling 10)

**Claim.** The lane's own self-assessment mismatch count — the number of `MISMATCH:` lines printed by
`python3 plans/state_check.py --summary` over the measured tree, i.e. frozen self-assessment prose that
the repo's own bytes contradict — falls from **1** to **0**, and the one assertion it repairs
(`P3c.box.4.pointer.1`: `SHONEN.md` box 4 pointed at `PROVINCE.md:129` while `### Adjacent` sits at
line 151) is repaired by *deriving* the line from `PROVINCE.md` bytes, not by hand-editing the pin.
`plans/round86_c2_repin.py` prints at the measured tip `TARGET derived_line=151
shonen_pointer=PROVINCE.md:151 pin_line=151 state_mismatches=0 selftest=pass defects=0` and
`PREDICATE R86-C2 pass`, exit 0.

**Frozen predicate.**

```python
ok = not defects and stats["derived_line"] is not None
```

with legs `P1-derive` (`### Adjacent` occurs exactly once and its line is read from the measured
bytes), `P2-shonen` (box 4's first pointer is `PROVINCE.md:<derived>`), `P3-pin` (the box-4 entry of
`P3C_PINS` in `plans/state_check.py` carries the same derived line and token), `P4-state`
(`state_check.py --summary --root <tree>` prints zero `MISMATCH:` lines, `VERDICT: PASS`, exit 0),
`P5-selftest` (`plans/state_check.py --selftest` still exits 0).

**Target.** `defects=0`, `state_mismatches=0`, `PREDICATE R86-C2 pass`, exit 0 at the measured tip;
`defects=3`, `state_mismatches=1`, `PREDICATE R86-C2 fail`, exit 1 at BASE.

**Counting command.**

```sh
python3 plans/round86_c2_repin.py --lane . --rev <REV> --work <scratch-dir>
python3 plans/state_check.py --summary            # the population the claim counts
```

**Kill rule.** A tip run with any `DEFECT` line, or a BASE run whose `state_mismatches` is not 1, makes
the claim unmet. Re-pinning by moving the pointer *to* the pin (leaving the pin where it was) is not a
repair: the `stale-pin`, `pointer-only` and `pin-only` controls must each fail.

**Why this is not laundering a frozen assertion.** The round-85 lesson's rule is that a stale frozen pin
may not be silently rewritten. `P1` derives the line from the measured bytes every run; `P4` reads the
instrument's own output, not this round's prose; and the controls prove the two halves of the repair are
independently necessary. The historical pin value `129` is retained in the counter as `STALE_LINE` and
in the lesson, never erased from the record.

**Controls (before the tip data run).** `--control-do-nothing` (BASE tree), `--control-stale-pin`,
`--control-pointer-only`, `--control-pin-only`; each must print `target_reached=False`.

## Causally separable

Each claim's counter reads only its own artefacts. Reverting C1's receipt and ledger row leaves C2 at
`defects=0` (it reads `PROVINCE.md`, `SHONEN.md`, `plans/state_check.py` and nothing C1 writes).
Reverting C2's two-line repair leaves C1 at `defects=0` (it reads the receipt, the case table, the tool,
the ledger row and the captured grader bytes, none of which C2 touches). The separation test is run and
committed under `.ufo/waves/round-86/L1/separation.txt`.

## Axes this round does not move

`novelty` 8, `depth` 10, `operability` 10 (three counters reachable, but the replay method is rounds
83–85's — no new capability row), `freshness` 10, `adjacency` 9: all held, none claimed. `coverage`
stays at its L0 cap (`kengaku | round-25/33/51`) and `calibration` stays at its ceiling: repairs of
routed defects restore, they do not extend a ceiling.
