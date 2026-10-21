source: S009 — https://arxiv.org/html/2506.22316 — Abstract, §4.2 Table 3; S010 — https://arxiv.org/html/2602.02219 — Abstract, §5.2 Table 3, §5.6; S011 — https://proceedings.mlr.press/v306/lee26bl.html — Abstract; S012 — https://arxiv.org/html/2306.05685v4 — Abstract, §3.3
verified-at: 2026-10-19
recheck: 2027-01-17 (90d) — re-open the four URLs and re-verify the quoted sentences; recheck whenever the judge family, rubric, or calibration label set changes

# LLM-judge calibration

## Claim

For binary pass/fail outcomes, an uncorrected LLM-judge pass fraction is biased
when judge sensitivity and specificity are imperfect; a defensible report
calibrates on human labels and carries uncertainty from both the test cases and
the calibration cases. Separately, rubric presentation order is a measurable
bias that flips selections, so order must be audited or permuted before scores
drive ranking.

## Evidence

- Naive judge scores are biased. S011, Abstract (ICML 2026, PMLR 306):
  "imperfect sensitivity and specificity of the LLM judges induce bias in
  naive evaluation scores".
- A correction exists with two-sided uncertainty. S011, Abstract: "confidence
  intervals that account for uncertainty from both the test dataset and a
  human-labeled calibration dataset"; it "remains unbiased under distribution
  shift between the test and calibration datasets".
- Ordering perturbations move scores. S009, Abstract: three bias types —
  "rubric order bias, score ID bias, and reference answer score bias"; §4.2
  Table 3 shows flip rates up to ~45–48% under the Ref-5 perturbation.
- Ordering also flips selections. S010, §1 (contributions): "rubric ordering
  alone flips the top-1 candidate on 15% to 41% of prompts".
- Bias direction is a judge property, not a rubric property. S010, Abstract:
  "some judges favor the first option, while others favor the last".
- Permutation is a partial fix. S010, Abstract: improvements "in the
  correlation between model judgments and human annotations are obtained
  primarily for models that exhibit strong bias".
- The canonical study set the baseline. S012, §3.3: "we found all of them
  exhibit strong position bias"; Abstract: GPT-4 achieved "over 80% agreement,
  the same level of agreement between humans" — but judges "cannot pass the
  more advanced 'repetitive list' attack".

## What this does not establish

- S011's framework is stated for binary outcomes with human calibration labels;
  it does not correct free-form rubric scores or multi-way preferences.
- S010's permutation reduces a specific position bias; it does not certify the
  judge as human-aligned — even the near-uniform GPT-OSS-120B showed 21–38%
  top-1 reversal.
- S012's 80% agreement is a 2023 GPT-4/MT-Bench/Arena result, not a property of
  every judge or domain.
- Falsifier: a judge with sens+spec=1 on human labels makes the bias term zero
  — the claim would then reduce to ordinary binomial uncertainty.

## Attribution

S011 is peer-reviewed proceedings (ICML 2026) with released software. S012 is
the canonical 2023 judge paper (NeurIPS 2023 D&B track; v4 arXiv) — canonical,
not current art. S009 (v4) and S010 (v3) are arXiv preprints; S010's judges are
open-weight models only, so its bias directions don't cover proprietary judges.

## Extends

Extends `eval-theory-notes.md` §"LLM-as-judge, algorithm-as-aggregator" (its
"judgment to the model, aggregation to a classical algorithm" rule gains a
calibrated-estimator form) and `eval-prior-art-calibration.md`'s pricing method
with a measured correction protocol. New coverage row: `Judge calibration`.

## How kengaku applies it

| Situation | Do | Don't |
|---|---|---|
| Binary judge verdicts (pass/fail) | Estimate sensitivity and specificity on a human-labeled calibration set; report corrected fraction with CIs carrying both uncertainty sources | Report the raw judge pass fraction as the score |
| Rubric-scored judging | Audit order sensitivity (permute score options and criteria); average a small K of random orderings | Rank candidates on a single fixed-order rubric pass |
| Choosing rubric granularity | Prefer 3–5 point scales (S010: extremes n=2 and n=9 carry the highest Cramér's V) | Assume a finer rubric buys precision — it can buy bias |
| Citing judge agreement | Name judge model, dataset, and agreement-vs-human level | Generalize S012's >80% GPT-4 figure to a new judge |

## Rejected

- **Permutation as human-accuracy proof.** Rejected: S010 finds balanced
  permutation statistically indistinguishable from random ordering on 10/12
  cells and helps human correlation mainly for strongly biased judges; a judge
  corrected for position bias "can therefore still be biased through criterion
  order" (§5.5). Flip: paired-bootstrap evidence that a permutation protocol
  lifts human correlation for the specific judge in use.

## Corrections (round 24 post-review, 2026-10-19)

Appended after the orchestrator's non-author spot-check; the lines above stay as
landed in `94da19e`. Re-opened S009 and S012 today.

- §Evidence S009 "flip rates up to ~45–48% under the Ref-5 perturbation" is not
  what Table 3 (§4.2) reports as a single range. Exact cells: Ref-5 FR on
  **BiGGen Bench 35.40–45.54%** and on **FLASK 40.53–48.58%** across the five
  judges (Ref-5 applied only to those two datasets). Read: Ref-5 flips roughly
  35–49% of scores depending on judge and dataset.
- §Evidence S012: "over 80% agreement, the same level of agreement between
  humans" is in the Abstract (correct), but "cannot pass the more advanced
  'repetitive list' attack" is in **§3.3 Limitations of LLM-as-a-Judge**
  (verbosity bias), not the Abstract.

## Corrections (round 25, 2026-10-20)

Appended; the lines above stay as landed. Source: round-25 reviewer RevF11 re-opened S010
(https://arxiv.org/html/2602.02219, §5.4 and Table 4) on 2026-10-20.

- §How kengaku applies it, "Choosing rubric granularity": the S010 pattern "extremes n=2 and n=9 carry the
  highest Cramér's V" holds on **5 of 6 judges** (§5.4: "on 5 of 6 judge models the lowest V sits at an
  intermediate scale"); GPT-OSS-20B peaks at n=5 (Table 4: V = 0.035, 0.035, 0.080, 0.036 at n = 2, 3, 5, 9).
  Do not state the extremes pattern as universal. (Closes kaika W3 F11.)
