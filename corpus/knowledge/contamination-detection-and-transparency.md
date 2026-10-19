source: S001 — https://aclanthology.org/2026.gem-main.50/ — Abstract; S002 — https://arxiv.org/html/2510.02386v1 — §3.1 Table 2, §4 Table 5; S004 — https://arxiv.org/abs/2605.19999 — Abstract
verified-at: 2026-10-19
recheck: 2027-01-17 (90d) — re-open the three URLs and re-verify the quoted sentences; check for post-training detector evaluations before any new model-family contamination claim

# Contamination detection and transparency

## Claim

A negative result from one contamination-detector family does not establish that
a model is uncontaminated; it bounds only what that detector could see at its
access level and contamination tier. Reinforcement-learning post-training can
conceal the signals detectors rely on while the performance inflation survives,
so an evaluation must state the detector, its access and tier scope, and keep a
transparency record rather than report "clean".

## Evidence

- No detector family is reliable across the board. S001, Abstract: "no detection
  method is consistently reliable across contamination tiers, model-access
  settings, and training stages" (systematic review of 55 studies through late
  2025, five detection families).
- Instruction-tuning and post-training stages are under-covered. S001, Abstract:
  "We identify instruction tuning as a persistent blind spot".
- Reported inflation magnitudes are setting-dependent. S001, Abstract:
  "inflation estimates spanning roughly 6%–40% under benchmark- and
  setting-dependent assumptions".
- RL post-training hides contamination. S002, Abstract: "even a brief Group
  Relative Policy Optimization (GRPO) training can markedly conceal
  contamination signals that most detection methods rely on"; Table 2 shows
  reference-free AUROCs falling to near 50% after 156 GRPO steps.
- CoT contamination of a finished reasoning model is nearly invisible. S002, §4:
  "almost all the detection approaches consistently perform near random guess
  in all the benchmarks".
- Concealment is not forgetting: inflation persists. S002, §3.1: "the
  contaminated model, further trained with GRPO, still shows an average
  performance inflation of 7.14% across six benchmarks".
- One proposed remedy is construction-side. S004, Abstract: benchmark datasets
  should be "contamination-resistant, i.e., unlearnable, but support
  inference" (position paper, not a deployed method).

## What this does not establish

- S001 is a review, not a detector evaluation; it does not rank any single
  method as trustworthy on your model.
- S002's concealment is demonstrated on 7–8B distills with GRPO/RAFT++ on six
  math benchmarks; it does not prove every RL recipe or model size conceals.
- S004 proposes a direction; it supplies no working contamination-resistant
  benchmark today.
- Falsifier: a detector shown to keep high AUROC across SFT, RL, and post-CoT
  stages on held-out reasoning models would narrow this claim's scope.

## Attribution

S001 is a peer-reviewed systematic review (GEM 2026, ACL Anthology, Outstanding
Paper). S002 is an arXiv preprint (v1, 2025-09-30) with released code; treat as
preprint, not proceedings. S004 is an arXiv position paper (2026-05-19): a call
to action, not empirical validation.

## Extends

Extends `corpus/knowledge/benchmark-selection.md` (its "re-check contamination
status before citing" rule gains the tier/access machinery) and SKILL.md
anti-patterns 1 and 8. New coverage row: `Contamination detection and
transparency`.

## How kengaku applies it

| Situation | Do | Don't |
|---|---|---|
| Reporting a contamination check | Name detector family, model access (weights/logits/black-box), contamination tier tested (T1–T4), and what a negative cannot rule out | Write "uncontaminated" from one detector's negative |
| Evaluating a post-RL reasoning model | Assume detector signals may be concealed; require transparency records of training stages | Trust a logit/perplexity negative as stage-agnostic |
| Scoring inflation risk | Report the 6%–40% range as benchmark- and setting-dependent, not a point estimate | Quote a single inflation number as the inflation |
| Choosing a benchmark for a claim | Prefer suites with a documented transparency card or auditable construction | Treat a private/hidden split as proof of cleanliness |

## Rejected

- **DCR factor as "decontaminated accuracy" (S003).** Rejected as a general
  score correction: the authors state "we do not consider this adjusted
  accuracy to be the accurate performance of the model after removing all BDC
  risk" (§2.4.2), validate only to 72B "excluding frontier-scale systems", and
  admit the framework is "not yet adaptable to generative tasks such as machine
  translation and summarization" (Limitations). Flip: validation on frontier
  models and generative tasks with the adjustment tied to recovered accuracy.
