# Round 25 — pre-registration (frozen before wave 1, 2026-10-20)

Base: lane `master` = `6180e4fb92e90c0b172e9788e2c765d097f2e142` (jj-colocated, clean at readiness).
Author: KengakuR25 (L1; holds the frozen planner seat — the wave validator rejects `planner`).
Amendments are appended below as `## Amendment N`, never edited in place.

## Axis state at base (SCORECARD.md §Round 24 re-derived table, `:608-616`)

novelty 7 · coverage 7 · calibration 8 · operability 8 · freshness 8 · adjacency 8 · depth 9.
Lowest non-retired: **novelty 7, tied with coverage 7**. No stagnation waiver (novelty < saturation line 8).
Tie-break: coverage stays capped at 7 by the declared-but-unresolvable-surface clause until the operator
rules the round-24 coverage-cap question; a coverage move cannot change its number, novelty can.

**Legacy-label mapping (PROTOCOL.md "Fleet-2 conventions": a SCORECARD axis not defined in AXES.md is
worked only with its mapping in the same row).** `novelty` → canonical **coverage** (AXES.md:12 —
"edge classes" the skill governs; LEARNING.md expansion trend): a novelty move adds a construct the lane
can now observe, i.e. a new governed edge class. It is scored as its own legacy row with this mapping
written in the row; it is not a seventh axis. Consequence: this round makes no separate coverage claim
(two claims on one canonical axis would be one claim).

## C1 — novelty (→ coverage): interval-calibrated attribution accuracy from committed receipts

Construct (new to the lane): the attribution instrument's (`plans/attrib_probe.py`) accuracy, per-leg
recall and per-leg specificity as **exact intervals**, and the leg-share bound implied by those intervals
(Rogan–Gladen form, S011-style bias accounting), with every stored point verdict re-verdicted under an
interval rule. Every stored r21–r23 verdict today is a point fraction against bar 0.80 with a min-n rule.

Frozen population P1: the committed files `corpus/evidence/attrib-r2[123]-*.log` at base (9 files). Per
file, the scored block is the LAST `## GT + scoring at close` block (the receipts' own
`AUTHORITATIVE SCORING SECTION` rule, `attrib-r21-impl-ds-trials.log:316`); files with no such block
contribute 0 scored trials and are reported as trial-only. Two blocks whose trial tables are identical
(same trial ids, predictions, GT, chains) are one sample, counted once, and the duplicate is named.
No receipt byte is edited; no endpoint is contacted.

Frozen rule: two-sided 95% Clopper–Pearson exact interval (α = 0.05). Verdict per estimate:
`PASS` iff lower ≥ bar; `FAIL` iff upper < bar; `INDETERMINATE` otherwise; `UNTESTED` iff n = 0.
Bar = the receipt's own stated bar (0.80). Wilson 95% is printed as a sensitivity column, never as the
verdict. Leg-share bound: for leg L with observed predicted share q, the true-share bound is the
min/max of (q + sp − 1)/(se + sp − 1), clipped to [0,1], over se ∈ [se_L, 1], sp ∈ [sp_L, 1], where
se_L / sp_L are the CP lower bounds (reported as conservative, not Bonferroni-exact).

Power ask (planner-registered; a wave-1 critic may tighten it, never loosen it): with zero errors the CP
lower bound is 0.025^(1/n); it first reaches 0.80 at **n = 17** (n=16 → 0.7940; n=17 → 0.8049). Any
point PASS with n < 17 cannot be an interval PASS. The construct is measured at or above its power ask
only for blocks with n ≥ 17; legs below it are reported INDETERMINATE, never PASS.

Predictions (filed before the instrument exists; scored at close with Brier; near-deterministic math is
labelled so — these test the parse/dedup understanding, not forecast skill):

| id | event | P(yes) |
|---|---|---|
| P1 | the stored r22 `TARGET hyper 10/10 -> PASS` re-verdicts INDETERMINATE | 0.95 |
| P2 | `attrib-r22-legs.log` and `attrib-r22-opencode-trials.log` authoritative blocks are the same sample (dedup fires) | 0.55 |
| P3 | every authoritative overall-accuracy block with n ≥ 17 re-verdicts PASS | 0.90 |
| P4 | at least one per-leg recall with n ≥ 1 re-verdicts INDETERMINATE | 0.97 |
| P5 | the instrument finds at least one scored trial marked incorrect in P1 | 0.10 |

Counting command (lands with the instrument): `python3 plans/attrib_calibration.py --summary`.
Before: 0 interval estimates / 0 interval verdicts exist for the instrument (sweep:
`grep -rlE 'Clopper|Wilson|confidence interval' corpus/evidence/attrib-* plans/attrib*` → expected empty).
After: one interval verdict per estimate in P1, printed with its counts.
Failure capability: `--selftest` must exit nonzero on (i) a flipped GT cell, (ii) a known CP value
perturbed, (iii) a duplicate block counted twice; the red runs are committed.
Novelty +1 fires only if all three rubric legs hold (`SCORECARD.md:244`): new construct (sweep above),
instrument in-repo and offline, prior-art verdict with fetched URLs (new SOURCES rows opened this round),
and the power ask is met. Otherwise the row records `improved` (verdict-only) or `unchanged`, honestly.

## C2 — calibration: SCORECARD/SHONEN/PROVINCE/README current-state assertions re-derived mechanically

AXES.md:15 calibration signal: "SHONEN.md/SCORECARD entries match observed repo state". The round-24
census was presence-based (W3ReviewKengaku F9). C2 builds `plans/state_check.py`, which re-derives each
frozen assertion from the repo (re-running offline commands, resolving paths and `:line` anchors,
diffing SHONEN against the PROTOCOL.md canonical seed) and exits 0 (all match) / 1 (mismatch) / 2 (usage).

Frozen population P2 (extracted from base bytes; any later row is out of population):
- P2a `SCORECARD.md` `## Capabilities` rows (3): run the row's offline command; every expected token in
  the row's evidence cell must appear in its output.
- P2b `SCORECARD.md` round-24 re-derived axis table (7 rows, `:610-616`): every backticked path/anchor
  resolves; numeric claims re-derive where the row names a command.
- P2c `SHONEN.md`: seed block byte-identical to `PROTOCOL.md` canonical seed modulo `<name>`; one
  evidence line per box; every pointer resolves.
- P2d `PROVINCE.md` `## Surfaces` rows (9): first backticked local path `test -e` (tilde expanded); a
  failing path must carry `ABSENT` on its row (QUALITY R4); URL/endpoint rows are counted
  `offline-unverifiable` and never contacted.
- P2e `corpus/README.md` index rows naming `knowledge/`, `lessons/`, `evidence/` paths: both directions
  (row → file; file → row).

Counting command: `python3 plans/state_check.py --summary` → `assertions=<n> match=<m> mismatch=<k>
offline_unverifiable=<u>`. Before = run against a `git archive` of base `6180e4f`; after = run against
the landed tree. Claim: mismatches at base > 0 found and each closed by an appended correction (never a
rewrite of history), after = 0 mismatches on P2, plus a red mutation run (`--selftest`).
Calibration +1 is **not** claimed by this design (the rubric +1 needs a scored probe); the row records
the observable move with score held unless the critic and non-author closure rule otherwise.

Separability: C1 touches attribution receipts and a new instrument; C2's population is frozen at base,
so C1's new SCORECARD rows are outside P2. Each verifies with the other reverted.

## Frontier step (inside the claim cap)

- New `corpus/SOURCES.md` rows only for sources opened this round (C1 prior art: exact binomial
  intervals, misclassification-corrected prevalence, S011 re-open). C1's knowledge entry cites them.
- `corpus/lessons/round-25.md` `## Mistakes`: mine at least one with a red-before demonstration.
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` at start
  (exit 0, `kengaku ok`, 2026-10-20 base) and at end.

## Conformance carried (not claims)

D17 (`SHONEN.md` canonical form) and D18 (SKILL frontmatter triggers/anti-trigger/arbitration) are
repaired as file-contract conformance, measured by C2's P2c check and a frontmatter grep respectively.
D15 (missing r19–23 fleet reports) is not fabricated or retro-labelled.
