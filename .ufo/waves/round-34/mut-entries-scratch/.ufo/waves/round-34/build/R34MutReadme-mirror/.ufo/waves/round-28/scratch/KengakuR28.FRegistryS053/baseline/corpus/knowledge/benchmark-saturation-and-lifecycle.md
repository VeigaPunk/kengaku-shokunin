source: S007 — https://arxiv.org/html/2602.16763 — §2.1 Definition and Scope, §4.1; S008 — https://arxiv.org/abs/2511.04703 — Abstract
verified-at: 2026-10-19
recheck: 2027-01-17 (90d) — re-open both URLs, recompute the saturation index from the paper's public data/code (github.com/evaleval/benchmark-saturation) against a dated leaderboard snapshot, and report sensitivity to k and α

# Benchmark saturation and lifecycle

## Claim

A benchmark is saturated only when top models are statistically
indistinguishable under the evaluation's uncertainty AND performance is near
the benchmark's empirical ceiling; a high score alone is neither necessary nor
sufficient. Indistinguishability without ceiling proximity is stagnation, not
saturation, and any retirement call must name the model set, leaderboard
snapshot, and uncertainty assumptions behind it.

## Evidence

- The definition is discrimination loss plus ceiling. S007, §2.1: "the loss of
  reliable discriminative power among top-performing models".
- Saturation ≠ stagnation. S007, §2.1: "stagnation refers to statistical
  indistinguishability among top models, whereas saturation additionally
  requires that performance is near the empirical ceiling".
- It is widespread but not universal. S007, §4.1: "Of the 60 benchmarks
  analyzed, 29 exhibit high or very high saturation (Sindex ≥ 0.7)".
- Hiding test data does not prevent it. S007, §4.1: "Hiding test data does not
  appear to prevent saturation once benchmarks are widely adopted" (H1
  rejected, though only N=4 private benchmarks in the set).
- Expert curation, not secrecy, is what tracks resilience. S007, Abstract:
  "resilience to saturation is impacted by expert-curation, not by public test
  data".
- Saturation can be benign. S007, §1 footnote: if the benchmark was valid,
  "saturation means that a task can be considered 'solved'".
- Validity failures sit under the scores. S008, Abstract: a 29-reviewer
  "systematic review of 445 LLM benchmarks" found "patterns related to the
  measured phenomena, tasks, and scoring metrics which undermine the validity
  of the resulting claims".

## What this does not establish

- S007's index is one operationalization: k=5 top models and an n_eff=n^0.5
  shrinkage are chosen parameters; Table 1 shows bin assignments move under
  k=3 or α∈{0,1} even though ranks correlate.
- Its public-vs-private null rests on 4 private benchmarks — too small to prove
  secrecy is useless, only too weak to assume it protects.
- It studies text benchmarks with leaderboard data; multimodal and
  no-leaderboard suites are out of scope.
- S008 reports construct-validity defects as patterns, not a per-benchmark
  verdict on any specific suite.
- Falsifier: a top-model gap exceeding z·SE_Δ at a new snapshot un-saturates
  the benchmark — stagnation can lift after a paradigm shift (S007, §2.2).

## Attribution

S007 is an arXiv preprint (v4, EvalEval Coalition; flagged ICML in its
keywords) whose index, bins, and thresholds are the authors' chosen
operationalization — cite as one study's index, not a ground-truth meter; some
coauthors contributed to analyzed evaluations (disclosed CoI). S008 is an
arXiv preprint systematic review (Nov 2025, 29 expert reviewers, 445
benchmarks).

## Extends

Extends `benchmark-selection.md` and SKILL.md anti-pattern 1 ("a benchmark's
reputation outlives its signal") by replacing the informal "stale" label with
an explicit, uncertainty-aware construct, and supplies the construct-validity
check (S008) that anti-pattern 2's mechanism-proof warning lacked. New coverage
row: `Benchmark saturation and lifecycle`.

## How kengaku applies it

| Situation | Do | Don't |
|---|---|---|
| Calling a benchmark "saturated" | State top-k set, dated leaderboard snapshot, SE assumptions (S007's k, α), and whether the verdict is saturation or stagnation | Call saturation from a high top score alone |
| Retiring a benchmark from the stack | Check whether top models are inside z·SE_Δ of each other AND near the empirical ceiling | Retire on reputation age; keep on a "private split" claim |
| Interpreting a plateau at low scores | Read it as model-level stagnation — discrimination may return with a new model class | Declare the task solved, or the benchmark dead, without the ceiling check |
| Adopting a new benchmark | Run S008's validity lens: does the task/metric match the claimed phenomenon? | Let a fresh score substitute for a validity argument |

## Rejected

- **Private test items alone guarantee longevity.** Rejected: S007 reports no
  meaningful public/private saturation difference (H1) — but on N=4 private
  benchmarks, so the defensible rule is "measure discrimination and exposure",
  not either direction of the secrecy claim. Flip: a larger private-benchmark
  sample with exposure controls showing a real saturation difference.
- **High score = saturated.** Rejected by definition: S007 requires
  indistinguishability AND ceiling proximity; a tight cluster at 40% is
  stagnation, at 98% saturation — and a valid saturated benchmark can mean
  "solved", not "broken". Flip: none needed; it is a definitional error, not a
  contingent one.
