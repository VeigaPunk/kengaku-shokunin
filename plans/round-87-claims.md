# Round 87 — frozen claims (kengaku)

Frozen in commit A (this file and `plans/round87-cases.json`), before any instrument, receipt or score
exists. Base: `b9be687774e6b559470f5b0d9b936315b51ff311` (round-86 spot-check tip, `master`). Measured tip:
the commit that lands the receipt, ledger and corpus edits (named in the round report), never a commit
whose bytes changed after the first score. Nothing below may be edited after freeze; a frozen element that
looks wrong is reported, not repaired.

Two claims, distinct axes, causally separable (each counter reads only its own surface). Shape: one v1 wave.

## R87-C1 — coverage (lowest non-retired axis, held at its L0 cap of 7)

**Move:** a fifth located offline replay of a Terminal-Bench 2.0 grader, `mteb-retrieve`, by the round-87
replay counter `plans/round87_c1_replay.py` over the frozen eight-case table `plans/round87-cases.json`.
The counter reads its own `executed_rows` from the population ledger (this closes round-86 spot-check
routed defect R86-V4, the `members=1` literal, by counting instead of printing a constant).

- **Before (BASE `b9be6877`):** `TARGET executed_rows=30 member=mteb-retrieve located=0 executed=0 defects=7`,
  `PREDICATE R87-C1 fail`, exit 1.
- **After (measured tip):** `TARGET executed_rows=31 member=mteb-retrieve located=1 executed=1 defects=0`,
  `PREDICATE R87-C1 pass`, exit 0. Ledger: executed 30 → 31; `file-artifact` 22 of 76 → 23 of 76.
- **Predicate (one sentence, identical in this file, the counter's `PREDICATE R87-C1` line and the report):**
  pass iff the captured grader bytes at the measured revision hash to the frozen subject SHA, and the receipt
  at that revision re-derives under legs L1–L8, and the probe re-run from the measured tree reproduces the
  receipt observation block, and the observed vector of all eight frozen cases equals its predicted vector.
- **Kill rule:** any leg L1–L8 failing at the measured tip makes the claim unmet; so does any mismatch between
  the probe re-run and the receipt. Editing the case table after commit A voids the claim.
- **Do-nothing control:** the counter at BASE must report `defects=7` (exit 1). A ledger-only control (ledger
  row flipped, receipt absent) must fail L1. A forged-receipt control (stamp `LANE_TIP` replaced by a commit
  that is not an ancestor of the measured revision) must fail L3. Each control's exit code and defect lines are
  committed to `.ufo/waves/round-87/L1/` before the measured tip is scored.
- **Sourced:** the grader bytes are row `S275` in `corpus/SOURCES.md`, opened in this round (2026-11-05):
  `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/mteb-retrieve/tests/test_outputs.py`
  returned HTTP 200, 559 bytes, sha256 `e4e6b21f…c0b`, byte-identical to the round-52 capture.
- **Honest limit (carried from round 86):** a receipt whose observation block is correct and whose stamp names
  the measured tip is not distinguishable by observation from a freshly minted one. L6 reproduces the
  observation; it does not authenticate an author.

## R87-C2 — calibration (held at its ceiling of 10)

**Move:** the lane's live current-state documents assert case-set facts about the round-86 replay. Their
mismatch count against the table-derived facts goes from 1 to 0. The round-86 spot-check (R86-V3) found that
`corpus/README.md` says "eight frozen schema-drift cases" while the frozen table derives eight case shapes,
six schema-drift (`why` text containing "schema drift") and two controls. Scope is `corpus/README.md`,
`PROVINCE.md` and `SKILL.md` only; append-only logs (`LOG.md`), filed round-86 lesson text and frozen claim
files are out of scope and are not rewritten.

- **Before (BASE `b9be6877`):** `TARGET mismatches=1 defects=2`, `PREDICATE R87-C2 fail`, exit 1.
  (`mismatches` = `corpus/README.md:941` asserts "eight … schema-drift cases" against 6 derived; `defects`
  adds the canonical round-86 row being absent.)
- **After (measured tip):** `TARGET mismatches=0 defects=0`, `PREDICATE R87-C2 pass`, exit 0. The `lessons/round-86.md`
  row of `corpus/README.md` states `eight case shapes, six schema-drift and two controls`.
- **Predicate:** pass iff no line in the scope asserts a schema-drift case count that differs from the count
  derived from `plans/round86-cases.json` at the measured revision, and the `lessons/round-86.md` row carries
  the derived canonical sentence.
- **Kill rule:** a reverted phrase, a re-introduced count that disagrees with the derivation, or a derivation
  whose result changes at the measured revision makes the claim unmet.
- **Controls:** BASE must report the defects above. A fixture README whose derived sentence says "five
  schema-drift and three controls" must report `mismatches>=1`. The round-86 table at the measured revision is
  unchanged, so the derivation itself is the control's reference.
- **Axis note:** calibration is at its ceiling 10. Following round-86 C2 precedent, the score stays 10 and the
  row records the mismatch 1 → 0 move and its verdict; a reading of "held" is not an improvement claim on the
  score itself.

## Frontier step (not a claim)

`corpus/SOURCES.md` gains `S275` (grader bytes for `mteb-retrieve`, tier A for scope "member replay only",
status `mined`, used-by the round-87 lesson). Census before → after is measured by
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` (exit 0 required at round end).

## Mistake mined (not a claim)

Class `reference-drift`: the round-86 closure report cites `.ufo/waves/round-86/L1/outside-gates.txt`, which
exists in no ref. Fix: `plans/round87_report_paths.py`. Red-before is the round-86 report itself (exit 1,
`DEFECT pointer .ufo/waves/round-86/L1/outside-gates.txt`); green-after is this round's report.

## Exploratory claims

None. Assimilation: none — `merge/kengaku/` remains blocked by L0 `kengaku | round-54`.
