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

## Amendment 1 (2026-10-20 ~21:30 -03, after wave-1 read-only findings, BEFORE any instrument output was read)

Inputs: `.ufo/waves/round-25/build/{CritNoveltyLegit,CritAxisMapping,CritPowerAsk,CritPredictions,CritIidCluster,CritC2Calibration,CritSeparability,DupR22Scout,FreezeShaScout,TrialVsImplScout,ConnKagiKama,ConnSoujiKaidoku}.md`.
Every change below tightens or clarifies; none loosens a frozen rule.

1. **C1 before-statement narrowed.** "0 interval estimates" was false: `corpus/knowledge/attrib-r21.md:139,154,156,374`
   print descriptive Wilson 95% intervals for overall accuracy (no verdict, no per-leg, no CP). Before =
   0 exact (CP) intervals, 0 per-leg recall/specificity intervals, 0 interval-carrying verdicts, 0 in-repo
   instrument. Widened sweep: `grep -rnE 'Clopper|Wilson|confidence interval' corpus plans SKILL.md grader.py`.
2. **Mapping is nominal and row-scoped.** `novelty` is recorded as a sub-axis of canonical coverage
   (coverage/constructs vs coverage/surfaces). It serves the distinct-axes rule and the expansion trend only;
   the novelty row is scored by the novelty rubric (`SCORECARD.md:244`) and the canonical coverage row keeps
   its own number and cap. Dissent on record: CritAxisMapping argues calibration is the closer fit; rejected
   because the instrument's accuracy is domain output, not the lane's self-assessment.
3. **Power ask tightened (CritPowerAsk).** Interval PASS at bar 0.80 needs n >= N(e) with e errors:
   N = 17, 26, 34, 41, 48, 55 for e = 0..5. ":45 legs below it are reported INDETERMINATE" is restated as
   "never PASS" (a leg with failures can FAIL).
4. **Dedup clarified, frozen rule kept.** The literal row-equality rule fires on `attrib-r22-legs.log:312` ≡
   `attrib-r22-opencode-trials.log:204` although request windows/pins show two executions. The frozen rule is
   applied as written (counted once, the conservative direction) and a pooled-if-distinct sensitivity line is
   printed beside it; the verdict comes from the frozen rule.
5. **Out-of-population blocks named.** Non-last blocks (`attrib-r21-impl-ds-trials.log:130,176,222`,
   `attrib-r22-legs.log:260`, `attrib-r23-stream.log:194`) are listed as non-authoritative and never
   re-verdicted. A stored `0/0 -> FAIL` re-verdicts UNTESTED (label migration, named as such).
6. **P3 event pinned:** scored on `ACCURACY:` lines only (not the r23 `score_summary` shim-level `verdict`).
7. **Brier honesty (CritPredictions).** P1, P3, P4, P5 were derivable from committed bytes at filing; P2
   is the only genuine forecast. The close reports per-row `derivable-at-filing` flags and the Brier split;
   no calibration credit is taken from this score.
8. **Clustering caveat (CritIidCluster).** Each block's n counts repeated sends of 1-3 prompt bodies; the
   CP interval is trial-level (iid) and is reported with `bodies=m` and an `iid-fragile` flag. Cluster-level
   n (m <= 3) can never PASS; the knowledge entry carries this limit.
9. **Instrument contract hardening.** Empty population or unreadable receipt -> exit 2 with a `SETUP` line
   (no vacuous PASS). `rg_bound` handles se_lo + sp_lo <= 1 as unidentified -> [0,1].
10. **C2 separability and grammar (CritSeparability, CritC2Calibration).** P2a sources-registry tokens are
    re-derived on the base registry population (ids <= S026; the registry is append-only), so C1's new rows
    cannot move C2. P2b anchors are resolved by content (the line's text) not absolute line number. P2e's
    file->row direction is scoped to the base file manifest; files added this round are reported as `new`,
    not counted. P2c's seed is frozen into `plans/fixtures/r25/shonen-seed.txt` with the PROTOCOL.md sha256.
    A stale base assertion closed by an appended dated correction (QUALITY R1) is reported `superseded`
    (separately from match), and the correction's own value is re-checked.

## Amendment 2 (2026-10-20 ~22:30 -03, AFTER instrument output — falsify-wave corrections; disclosed as post-output)

Inputs: `.ufo/waves/round-25/falsify/*.md`. Each item tightens, narrows or corrects; none loosens a frozen rule or
changes a stored-verdict re-verdict.

1. **Non-firing specificity carries no verdict** (CritSpecificity): a leg the instrument never predicted has
   specificity n/n by construction (the complement of its 0 share); its verdict is `-` (`non-firing`). PASS count
   12 → 7; transitions unchanged.
2. **Share bound relabelled** (CritRgBound): the round's `rg95` held the observed share fixed, so it was a
   conditional sensitivity bound, not a 95% interval for the true share. It prints as `rg_cond`; a second bound
   `rg90` adds the observed-share CP95 arm (≥ 90% by union bound under any dependence). `rg90` is vacuous or near
   vacuous for every P1 leg — itself the finding: these samples cannot identify leg shares beyond the GT counts.
3. **`bodies`/`iid-fragile` on every PASS** (CritBodiesFlag): computed per estimate; fragile when fewer distinct
   request-body classes than `need_n(errors)` stand behind a PASS. `bodies` counts request-body classes (payloads),
   not distinct prompt texts (impl-glm's two classes share one prompt).
4. **Boundary anchors** (MutVerdictBoundary, MutRgBound, MutDedupManifest): selftest pins lo == bar → PASS,
   hi == bar → not FAIL, Rogan–Gladen corners/clip/pole, Wilson both ends, CP vs the exact-rational table (1e-11),
   and dedup-key sensitivity to predictions. SETUP exits (code 2) for empty or unreadable receipts.
5. **C2 implementation brought to P2d as registered** (StateSelftestExec, CritPreregAdherence): an endpoint-first
   surface row is offline-unverifiable (v1 had tested a `/proc/1299` pid pin inside it), so the base count is
   10, not 11 (v2 receipt). ABSENT counts only as the declared `**ABSENT**`/`**ABSENT <date>**` marker; a frozen
   capability row that loses its command is a mismatch; a correction supersedes only when it restates the full
   census; the base registry population must be exactly S001–S026; a deleted frozen base file is a mismatch;
   the SHONEN seed fixture is sha256-pinned and checked against the fleet PROTOCOL.md when present.
6. **Novelty +1 withdrawn** (PriorArtWeb, confirmed by the L1 opening https://pypi.org/project/cigate/): CI-lower-
   bound gating of LLM-judge rates with a Rogan–Gladen core and refusal at TPR + TNR ≤ 1 is published as tooling
   (cigate 0.2.0; also sigeval, EvalGlass per PriorArtWeb). The rubric's "already published" cap applies to the
   construct; novelty is held at 7 with the observable recorded. CritNoveltyFresh's dissent (+1 fires) is on record.
7. **Display slip (M30):** line 43 above prints the n = 16 lower bound as 0.7940 (truncated); the exact value is
   0.794093 (rounds to 0.7941). The verdict and the n = 17 power ask are unchanged.
8. **P2 prediction:** scored 1 under the literal dedup key and 0 under its "same sample" wording (distinct
   executions); all five predictions were derivable from bytes committed before filing (CritBrierHonesty).
