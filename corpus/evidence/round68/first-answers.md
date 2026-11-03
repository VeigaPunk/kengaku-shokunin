# Round68 first answers — immutable before independent review

2026-11-03. Assessment inputs frozen at d7af088c78c5b469cc89f6f0018b050cafff3379. I read only reviewer/inputs.md and source-novelty.md, not expectations-private.md. Actual primary-source study preceded these answers: official HumanEval estimate_pass_at_k plus its calling loop, pinned to b9453e8f1865df0a0057a1383767caa400acfbcf; tau-bench arXiv2406.12045v1 §3 Pass^k metric; Chen et al. arXiv2107.03374v2 abstract. No provider calls, generated benchmark samples or executable scoring. Arithmetic below is original hand derivation over the invented case data, not measured model performance.

## A — finite pool, not unsupported extrapolation

For uniform subsets of three distinct candidates from six, failing subsets number C(4,3)=4 out of C(6,3)=20. Thus pass@3=1-4/20=4/5=.8. The proposed with-replacement plug-in calculation gives 1-(2/3)^3=19/27, about .7037; it answers a different sampling question and is not this finite-pool calculation. No subset of eight distinct candidates exists in a pool of six: n<k makes the finite estimator unsupported. HumanEval's caller omits k when any task lacks enough samples; the helper alone must not be used to launder this invalid input.

With c=0 and 1<=k<=6, all subsets fail, hence empirical finite-pool success is zero. That does not prove the true generation process has zero success probability. A future-generation interpretation requires an appropriate sampling design, independent identically distributed trials for the stated estimator's usual interpretation, and uncertainty from the finite data. Need additional independently collected candidates and a defined sampling/evaluation protocol for k=8, not a formula extension or an invented guarantee.

## B — oracle superiority and selector inferiority coexist

A's empirical oracle candidate-set success is90/100=.90; B's is80/100=.80. But actual deployed returned-answer success is54/100=.54 for A and72/100=.72 for B. Reject the unqualified 'A wins': A wins this oracle metric; B wins this observed deployed-output metric at the stated equal budget.

A loses36/100 tasks to selection despite an available valid candidate, versus B's8/100. Conditional on a solvable candidate set, selector success is54/90=.60 for A and72/80=.90 for B, so conditional failure is.40 and.10. These are not overall failure rates: those are46/100 and28/100, comprising oracle-unavailable10+selection-loss36 and20+8. A selector cannot synthesize answers, so candidate availability is an upper bound on its success. Need joint per-task system outcomes and sampling/uncertainty evidence for a population comparison; these fixed-set rankings need no invented population inference.

## C — pooled marginal success does not identify joint events

X: at least one success on50/100 tasks=.50; both successes on50/100=.50. Y: at least one on100/100=1; both on0/100=0. Pooled single-trial success is.50 in both. The proposed.75/.25 assumes independent Bernoulli outcomes with the same.50 success probability in the relevant conditioning unit; the supplied joint data contradict treating that assumption as an observed fact. Heterogeneous task difficulty also makes applying a pooled marginal p to every task inappropriate even if within-task draws were independent.

These are exact aggregates for these pairs, not universal future retry probabilities. Need a defined task distribution and repeated within-task joint outcomes to assess future retry behavior; recording only marginal averages discards the crucial dependence. Do not call at-least-one success all-attempt reliability.

## D — feasibility precedes ranking

Both spend5000 tokens, but A's8seconds violates the4second cap; B's3seconds meets it. Under both declared constraints B is the only demonstrated eligible pipeline, with65/100 observed success. A's70/100 remains a valid descriptive token-only advantage on this set; it is not an eligible deployment advantage. No contradiction arises because the objectives differ. The bare model cannot be ranked separately from its candidate generation, selector and orchestration. For deployment beyond this exact reported condition, request per-task latency distribution/tail compliance and total resource accounting, not only a possibly averaged latency number. Need a feasible measured A variant before claiming it can win under the joint constraint.

## E — a second draw is not a free correct-answer oracle

P's.70 at3000 and Q's.82 at6000 are measured properties of those pipelines, not of a new two-P-and-select pipeline. Under truly identical independent.70 trials an oracle at-least-one calculation would be.91, but neither independence nor oracle access is established. If each repeated P call really retains marginal.70, the joint at-least-one probability can range from.70 to1 depending on dependence. Even that is an oracle bound, not deployable selection success. Two3000-token runs already consume6000 before any additional selector cost; the claimed equal-budget system may violate the cap.

Reject the claimed.91 deployment win. A valid next measurement freezes a feasible generation+selector pipeline whose total cost is<=6000, records joint candidate outcomes plus the actual returned answer on the same prespecified tasks, counts failures and all selector cost, and compares to Q under the same evaluative/latency contract. If a zero-token deterministic selector is proposed, specify and evaluate it rather than assuming it chooses correctly. No universal Q superiority follows from rejecting the unsupported new-pipeline claim.

## F — valid oracle diagnostic, invalid production label

With no adaptation of generation to the held-out tests,83/100 is a valid empirical at-least-one/test-oracle success metric for the five generated candidates on these tasks. It is not useless and not production accuracy. The unavailable-test selector has informational access that production lacks. The actual static-ranker deployment observation is61/100; its22-task gap from83 is lost candidate-set opportunity, assuming the same evaluator/outputs and no synthesis. Neither figure alone proves real-world correctness or generalization.

If generation was adapted using held-out results, those tests are no longer untouched evaluation evidence for the whole adaptive process. The83 may still describe that adaptive test-guided search on this finite test set, but must be relabeled with feedback access and full search budget, and cannot be compared as the original unadapted five-sample metric. Use new untouched evaluation tests/tasks and the genuinely deployable policy to assess the resulting pipeline. Production might legitimately have some verifier, but the case explicitly excludes these held-out tests; do not invent access.

## G — accept the carefully bounded statement

Accept.74/100 exceeds69/100 by5percentage points on the fixed set under the stated evaluator and total token cap. Joint outcomes are unnecessary for that arithmetic. Their absence prevents reconstructing the paired discordances and associated paired uncertainty, not reporting the observed marginals. The memo explicitly refuses population and evaluator-external superiority, so lack of proof of either is not a contradiction.

Latency was not specified; consequently the memo cannot establish compliance with any latency requirement, but no such requirement is asserted. Likewise evaluator-validity concerns bound the interpretation of 'passing' without refuting the truthful test-set statement. For broader ranking, collect paired task outcomes, repetition/design information and uncertainty, plus operational constraints and independent validity checks matching the intended claim. Do not substitute reflexive skepticism for calibrated acceptance.

## H — preserve the task as the sampling unit

Pooling gives1-C(4,2)/C(8,2)=1-6/28=22/28=11/14, about.785714. It mixes candidates from different prompts/tasks, so it is not the probability of finding an answer by selecting two candidates for a particular task. Per task, task1's pass@2 is1 and task2's0; equal-task averaging yields.50. That is the requested benchmark quantity.

Per-task all-two success is also1 for task1 and0 for task2, average.50. Pooling all-two would give C(4,2)/C(8,2)=3/14, another wrong-unit quantity for this benchmark. These observations establish only success under the declared tests on these sampled tasks/candidates. They cannot establish full real-world correctness, hidden-case validity, or future model success without appropriate new evidence.

## Synthesis

The reusable question is: whose success, selected by what information, on which task unit, under what complete budget? More correct candidates can coexist with worse delivered answers; fixed-set claims can remain correct even when broad deployment claims fail. The eight cases diagnose these distinctions only. They do not demonstrate training-induced gains, because no pre-study matched first-answer baseline was measured.
