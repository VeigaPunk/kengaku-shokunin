# CritPredictions — critic: epistemic status of P1–P5 and honest Brier scoring

Read-only. All arithmetic recomputed offline from committed receipts; no instrument needed.

## Ground truth
- `diff` of authoritative tables `corpus/evidence/attrib-r22-legs.log:318-339` vs `corpus/evidence/attrib-r22-opencode-trials.log:210-231` → IDENTICAL (T01–T20, same cls/prediction/GT/chain/correct). Frozen dedup rule (claims.md:31-32) fires → P2 = YES; the duplicate must be named. Different journal windows (:313 vs :205), frozen sha (:315 vs :207) and ablations (loo:hdr_tells 19/20 :349 vs 18/20 :241) sit outside the dedup key.
- `grep '| NO'` over all five authoritative tables → 0 rows; every ACCURACY is k/k=1.000 (`attrib-r21-impl-ds-trials.log:297`, `attrib-r21-impl-glm-trials.log:173`, `attrib-r22-legs.log:342`, `attrib-r22-opencode-trials.log:234`, `attrib-r23-stream.log:298`) → P5 = NO.
- CP zero-error lower `0.025^(1/n)`: n=10→0.6915, n=13→0.7529, n=17→0.8049, n≥18→≥0.8147 — matches the filed power ask (claims.md:43) and forces P1/P3/P4 arithmetically.
- Trial-only (no `## GT + scoring at close` block): attrib-r21-ds-trials, attrib-r21-glm-trials, attrib-r22-legs-hyper, attrib-r23-stream-trials — 5 of 9 files scored.

## F1 — Four of five predictions are deterministic on committed bytes
Receipts predate filing; outcomes were derivable at filing from base + frozen rule:
- P1 (0.95→yes): hyper 10/10, n=10<17 → lo 0.6915<0.80 → INDETERMINATE regardless of correctness. Stored twice: `attrib-r22-legs.log:344`, `attrib-r22-opencode-trials.log:236`.
- P3 (0.90→yes): unique overall blocks {20/20, 22/22, 20/20 deduped, 30/30}, all n≥17, k=n → all PASS. No k<n authoritative block exists.
- P4 (0.97→yes): per-leg counts 9,10,13,6 all <17 (devin 9 `attrib-r21-impl-glm-trials.log:172`, hyper 10 `attrib-r22-legs.log:341`, alibaba 6 `attrib-r23-stream.log:297`) → INDETERMINATE forced.
- P5 (0.10→no): every table all-YES.
claims.md:47-48 labels this honestly ("parse/dedup understanding, not forecast skill"). Residual risk: the CLOSE report forgetting it — Brier on self-derivable events measures resolver faithfulness, not forecast skill.

## F2 — P2 is the only genuine forecast and carries ~90% of Brier mass
P2 (0.55): the one event with irreducible-at-filing uncertainty (dedup is a byte compare the planner chose not to run; per the diff it resolves YES). Under outcome vector (1,1,1,1,0): mean Brier = **0.0452**, P2 = **89.6%** of loss; if dedup failed, 0.0652, P2 = 92.8%. A headline mean ~0.05 is a statement about one coin-flip, not five calibrated probabilities.

## F3 — Two event-definition ambiguities to pin before scoring
- P3 "overall-accuracy block": `attrib-r23-stream.log:320` stores `"verdict":"FAIL"` (r23 target/mode clause; adjudication :341-344) while :298 stores `ACCURACY 30/30 -> PASS`. Reading score_summary.verdict flips P3. Score ACCURACY-fraction verdicts only; the composite must not feed the exit-0 re-verdict check either.
- `TARGET opencode-go 0/0 -> FAIL` (`attrib-r22-legs.log:345`, `attrib-r23-stream.log:303`, others) re-derives UNTESTED — a legal re-verdict change, not an inconsistency; else exit 1 will be misread.

## What the close report must say so calibration is not inflated
1. Per-row `derivable at filing` flag + derivation basis (this file supplies them).
2. Mean Brier WITH split {P1,P3,P4,P5} vs P2 plus P2's loss share — the `probe-r19-hyper.log:92-95` idiom (mean beside always-0.5 reference, dominant contributor named).
3. n=5: no reliability/resolution decomposition, no calibration-axis inference; C2's no-+1 holding (claims.md:92-93) must not be argued upward via this score.
4. Outcomes read verbatim from `python3 plans/attrib_calibration.py --summary`.

## Smallest safe correction
One `## Amendment 1` (claims.md:5): (a) pin P3 = ACCURACY-fraction verdicts, score_summary composite excluded; (b) require per-row determinism flags + split-Brier in the close; (c) name the deduped file pair when P2 resolves.

## Falsifiable condition
Close is honest iff `python3 plans/attrib_calibration.py --summary` reproduces (1,1,1,1,0) — any deviation is an instrument/parse defect to investigate before scoring — AND the round summary prints determinism flags + Brier split; a bare mean Brier falsifies the correction.

VERDICT: P1/P3/P4/P5 deterministic (outcomes already computable: 1,1,1,0); P2 the only true forecast carrying ~90% of Brier mass — honest scoring requires determinism flags, the P3 ambiguity pinned, and split-Brier reporting; otherwise calibration inflates.

Installs: none (python3 stdlib, diff, grep).
