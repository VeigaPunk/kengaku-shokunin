# R33FN3Newline — N3 `near()` newline probe (check_n3 wrapped-erratum attack)

Seat: `KengakuR33.R33FN3Newline` (mutation-tester, leaf), round 33 falsify wave / hyaku run 7,
2026-10-25. Frozen claim: `plans/round-33-claims.md` §C2 item N3 — the round-31 fleet report
"carries an appended erratum with `a44b5a8` **within 400 characters** of `superseded` or
`erratum` and naming the real locator-fix commit `ae95fe0`". Target instrument:
`plans/round33_defects.py` `check_n3` (lines 100–112) via `near()` (lines 60–66).

## Mutant (one plausible defect, as tasked)

A round-31 report fixture that satisfies every N3 guard **except line placement**: the hash on
one physical line, the erratum sentence starting the next physical line.

```
cites a44b5a8 as the fix

`a44b5a8` is a phantom hash, the locator fix landed at ae95fe0.
Erratum: superseded by ae95fe0
```

sha256 `4595cd4434578f41d6a8c8ca578f9abad383f6ee2c3da8c56131ece445554794` (121 bytes).
Byte gaps from end of `a44b5a8` (line 3): **65 chars** to `superseded`, **56 chars** to
`Erratum` — both far inside the code's 300-char window and the frozen text's 400-char window.
Guards: `a44b5a8` present (append-only guard passes), `ae95fe0` present.

## Method

Fresh sandbox `/tmp/r33-R33FN3Newline/`; instrument copied, never edited:

```
$ cp plans/round33_defects.py /tmp/r33-R33FN3Newline/ && sha256sum both && cmp
6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6  <lane>/plans/round33_defects.py
6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6  /tmp/r33-R33FN3Newline/round33_defects.py
COPY-IDENTICAL
$ python3 /tmp/r33-R33FN3Newline/probe.py
```

Detector = the copied module's own `check_n3(SB, fixture)` (the same explicit-fixture hook the
counter's selftest uses, keeping the probe hermetic — no fleet path read). Four stages:
pristine → mutant → restore → instrument-hash recheck. No git command run anywhere; no lane,
fleet, or sibling file touched; no tools installed (stdlib `python3` sufficed).

## Observed output (verbatim)

```
=== STAGE 1 PRISTINE (erratum sentence on one physical line) ===
fixture=r31-pristine-oneline.md sha256=fdbdf36b8c76cd4a98ad60c2cc448fa52091d934398e7957da4e30675e75d023 bytes=124
check_n3 -> ''
near(a44b5a8, superseded) = True
near(a44b5a8, erratum)    = False
BASELINE PASS (green as expected)

=== STAGE 2 MUTANT (hash line, then 'Erratum: superseded by ae95fe0' on next line) ===
fixture=r31-mutant-wrapped.md sha256=4595cd4434578f41d6a8c8ca578f9abad383f6ee2c3da8c56131ece445554794 bytes=121
check_n3 -> 'no appended erratum supersedes the a44b5a8 citation'
guards: 'a44b5a8' in text = True; 'ae95fe0' in text = True
near-window a44b5a8->superseded: fwd=False rev=False
near-window a44b5a8->erratum: fwd=False rev=False
byte gap a44b5a8(end,line3) -> superseded(line4) = 65 chars
byte gap a44b5a8(end,line3) -> Erratum(line4)    = 56 chars
  near(..., flags=re.I | re.DOTALL) = True
  near(..., width=400)              = False
DETECTOR on mutant: RED (flagged as defect)

=== STAGE 3 RESTORE (exact pristine bytes back into fixture A) ===
sha256(stage1) == sha256(stage3): True   (fdbdf36b…d023)
check_n3 after restore -> ''

=== STAGE 4 INSTRUMENT UNTOUCHED ===
lane  script sha256 = 6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6
sandbox copy sha256 = 6ef17abc7ac11cc294efde5e23a3679e1335d5e42ef4a840069a70287064d5b6

=== VERDICT SUMMARY ===
baseline_ok=True mutant_detector_red=True restored=True
```

(Stage-2 counterfactuals invoked the sandbox module's `near()` with kwargs only; no file was
mutated at any point, so no source restore was required — proven by the Stage-4 hash equality.)

## Verdict: FALSE-NEGATIVE (frozen predicate accepted, counter reddens) — mutant killed by the
detector but compliant with the claim, i.e. a calibration gap, not a saved invariant

- The wrapped erratum is valid under the frozen N3 predicate (both gaps 56/65 < 400 characters;
  a newline is a character), yet `check_n3` rejects it with
  `'no appended erratum supersedes the a44b5a8 citation'`.
- Root cause pinned: `near()` builds `re.escape(a) + r".{0,300}" + re.escape(b)` with
  `flags=re.I` only — no `re.DOTALL` — so `.` never matches `\n`; all four windows
  (`a→b`/`b→a` × `superseded`/`erratum`) are False across the single newline. Adding
  `re.DOTALL` alone greens the mutant (`True`); raising width to the frozen 400 without
  `DOTALL` does not (`False`). The discriminator is the newline, not the distance.
- Baseline (same erratum on one physical line, sha256 `fdbdf36b…d023`) is green, so the
  experiment is conclusive; restoration is hash-proven and the instrument is byte-identical to
  the lane copy before and after.
- This independently reproduces counter-attack row E3c and blind spot B2
  (`.ufo/waves/round-33/build/R33CounterAttack.md`) and FleetErrata F1. Consequence: the
  counter forces repaires to cram `a44b5a8`+keyword onto one physical line (exactly what the
  landed fleet erratum at `3d3ca566` does), and honest wrapped prose reddens — the detector
  measures line-local co-occurrence, not the frozen within-400-characters predicate.
- Coverage finding only; no contract, claim, or instrument changed. Boundary note: the
  400-vs-300 width axis is sibling seat `R33FN3Width`'s; width appears here solely as a one-shot
  counterfactual to exclude distance as the cause. `R33FN3HashContext` owns the `ae95fe0`
  context axis (untouched here).

Scope: no lane/fleet edit, commit, stage, or index touch; no tool installs; scratch
`/tmp/r33-R33FN3Newline/` (instrument copy `6ef17abc…d5b6`, `probe.py`, two fixtures). The only
lane-tree byte written is this report file.

VERDICT: n3-newline-falsified (false-negative reproduced; counter uncalibrated to wrapped errata)
