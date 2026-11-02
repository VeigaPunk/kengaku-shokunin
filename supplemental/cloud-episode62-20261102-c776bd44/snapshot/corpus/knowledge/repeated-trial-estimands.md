source: S226 — https://github.com/openai/human-eval/blob/b9453e8f1865df0a0057a1383767caa400acfbcf/human_eval/evaluation.py at b9453e8f1865df0a0057a1383767caa400acfbcf, lines13–36/86–91; S227 — https://github.com/sierra-research/tau-bench/blob/59a200c6d575d595120f1cb70fea53cef0632f6b/tau_bench/run.py at 59a200c6d575d595120f1cb70fea53cef0632f6b, lines180–203; S228 — https://arxiv.org/html/2406.12045v1 §3 Pass^k metric; S229 — https://arxiv.org/html/2107.03374v2 §2.1 and Appendix A
verified-at: 2026-11-02
recheck: 180d — re-fetch the two exact code pins and paper versions; compare capture digests and re-read metric domains; do not substitute main/master
writer: kengaku-shokunin-round62

# Repeated-trial metrics: discovery, reliability, and missing outcomes

Admitted on its manual/sourced finite-panel scope by parent-appointed independent
reviewer `/root/judge_kengaku_round62`; report
`.ufo/waves/round-62/review/REVIEW.md`. This is entry admission, not round closure.

## What is measured

For a fixed task with n recorded planned slots, c known successes and complete
binary observations, uniformly select k distinct slots, with 1≤k≤n.
There are C(n,k) subsets. Exactly C(n−c,k) contain no success, while C(c,k)
contain only successes. Thus the exact finite-panel proportions are

- discovery, A = 1 − C(n−c,k)/C(n,k), conventionally estimating pass@k;
- consistency, R = C(c,k)/C(n,k), conventionally estimating pass^k.

C(a,k)=0 when nonnegative a<k. k>n has no subset and supplies neither a zero
score nor a perfect score. At k=1 both equal c/n. As k increases within the
same fixed panel, A cannot decrease and R cannot increase: enlarging a subset
cannot erase an existing success or repair an existing failure. Neither
quantity certifies that a grader's success label captures the intended task.

S228 §3 defines different future-trial events and supplies both estimators.
The finite-panel combinatorial identity above requires no stochastic model;
interpreting it as an unbiased estimate of 1−(1−p_t)^k or p_t^k requires iid
Bernoulli outcomes with stable p_t within task and a fixed design. Correlated
retries, changing prompts/tools/user simulation, adaptive stopping, or an
unreliable grader do not acquire that interpretation by using this formula.

## Why a plug-in power is not the same estimate

Replacing p with c/n in 1−(1−p)^k or p^k samples the empirical distribution
with replacement. The combinatorial estimators instead average distinct-slot
subsets. The formulas may agree at boundaries or k=1 but are not interchangeable.
S229 Appendix A explicitly discusses the plug-in bias; the exact finite-panel
argument is that repeated selection of one recorded slot is not a distinct
trial. A calculation can be arithmetically correct yet estimate the wrong event.

## Aggregation fixes the task population

For T prespecified tasks, compute each task's value and take T^{-1}Σ_t.
This is an equal-task macro average. Pooling successes and attempts changes
weighting when n_t differs; for k>1 it also constructs fictitious subsets
spanning different tasks. Compute per task first. An entirely omitted task
cannot be detected from the surviving results alone: retain a planned task/slot
manifest. No claim here identifies the correct population for every benchmark.

The proposed reporting rule refuses a suite value if any planned task has n_t<k,
rather than silently changing the target population to eligible tasks. This
is a declared lane reporting policy, not a universal requirement or a claim
that every upstream harness uses the same policy.

## Failure versus unresolved outcome

An observed valid score of zero is a failure; an infrastructure error, missing
record, or ungraded output is unresolved for this model-success estimand. Keep
those counts separate. If an operational estimand deliberately counts system
outages as failures, declare that different policy before evaluation; do not
retrofit it to whichever score looks better.

For u unresolved slots among n planned slots and c observed successes, the
unknown total success count lies in [c,c+u]. Both subset functions increase in
that count. Consequently sharp finite-panel bounds are

A ∈ [1−C(n−c,k)/C(n,k), 1−C(n−c−u,k)/C(n,k)],
R ∈ [C(c,k)/C(n,k), C(c+u,k)/C(n,k)].

All unresolved outcomes being failures achieves both lower endpoints; all being
successes achieves both upper endpoints. This proves sharpness without a
missing-at-random assumption. Macro-average corresponding endpoints over the
fixed task population. These are **missing-outcome identification bounds**, not
95% confidence intervals, prediction intervals, or a power calculation. Even
when they collapse, sampling uncertainty can remain large. Conversely, a
nonzero u can leave a particular metric's bounds equal through saturation;
retain the unresolved status rather than pretending the observations were complete.

## What the pinned implementations actually say (read, not executed)

| Surface | Read semantics | Limit |
|---|---|---|
| HumanEval estimate_pass_at_k | Per-task combinatorial estimator implemented numerically; outer evaluation computes a task mean only for k with every total≥k | The inner helper assumes valid n,c,k; its early branch alone is not a valid n<k policy. No generated code or benchmark runner executed here |
| tau-bench display_metrics | Counts successes within tolerance of reward1; uses number of distinct trial IDs across the entire results list; averages per-task combinatorial reliability | The expected balanced, aligned-trial panel matters; arbitrary incomplete panels do not automatically have correct per-task n. Code reading is not evidence of a published score defect |
| tau-bench run exception path | Constructs reward0 for caught exceptions (lines88–99) | The lane's unresolved bounds intentionally answer a different question; no claim that upstream implements this uncertainty policy |

## Decision table

| Question | Report | Refuse |
|---|---|---|
| Can multiple attempts discover one success? | pass@k with k,n_t, fixed tasks | Renaming it reliable all-k success |
| Will every attempt succeed? | pass^k, with trial-generation assumptions | Using pooled pass@1 raised to k |
| Unequal repeats | Per-task estimators then fixed-task macro mean | Trial-pooled shortcut or silent eligibility exclusion |
| Missing/ungraded runs | Separate failure/error/missing counts and endpoint bounds | Dropping errors or presenting bounds as a CI |
| k exceeds a task's planned n | Ineligible and no fixed-suite score under this policy | Zero, perfect score, or an unexplained subset of tasks |
| Synthetic worked panels | Arithmetic/interpretation validation only | Broad model intelligence or deployment-reliability claims |

## Extension and falsifiers

Extends `paired-eval-uncertainty-reporting.md` into repeated-trial event and
aggregation semantics; the earlier note covers pairing, clustering, power and
adaptive inference, not these exact estimands. The historical tau-bench prior-art
mention is not a claim that this mathematics is novel. No new TB2 task grader
is held: 17/89 remains unchanged.

A subset enumeration contradicting either formula on its stated domain, an
unknown-outcome completion outside the derived interval, or a cited source
whose actual formula/aggregation differs falsifies the corresponding claim.
Agreement on hand-worked panels does not validate a runtime implementation,
prove iid sampling, or establish any model's success rate.

## Worked demonstration

Ten independent hand-derived panels and exact-rational answers:
`corpus/evidence/round62/manual-answers.md` (frozen before oracle release).
Public challenge and released hand oracle are retained in
`.ufo/waves/round-62/review/`. The source-code implementations were not run.
