# Rank uncertainty depends on the unit of inference

## Aim

A leaderboard gives an ordering for the scores observed. Whether that order would persist under different evaluation conditions is a separate question. Define the population of interest and how observations are paired before interpreting an interval for a model's rank. Many related measurements do not automatically provide the information of the same number of independent subjects.

## What the MMLU analysis illustrates

In their analysis of PromptEval's MMLU correctness matrix, Neuhof and Benjamini compared 15 models across 57 subjects and 100 prompt variants. Every subject contained at least 100 questions; the authors sampled 100 per subject for a balanced analysis. Scores were paired by subject, question and prompt when comparing models. Their main score and rank intervals use a 5% miscoverage level. The main rank intervals are marginal for individual models, not simultaneous across the 15 models. [1, §§2–3]

A choice of inferential unit changes what variation enters the calculation. In the balanced sample, one model pair has 57 × 100 × 100 = 570,000 paired subject–question–prompt differences. That count is not 570,000 independent subjects: measurements can share subjects, questions or prompts. The paper's naive analysis treats each triple as a unit and displays tightly separated intervals. Ignoring dependence can underestimate uncertainty, and those intervals do not establish a stable ordering for new subjects, questions or prompts. [1, §3.1 and Fig. 1]

The authors also calculated one average paired difference per subject, averaging that subject's 100 sampled questions and 100 prompt variants. The resulting 57 values, rather than the 570,000 triples, supply the variation and degrees of freedom for the subject-level paired test. With balanced cells this leaves the overall average difference unchanged, while the uncertainty calculation and degrees of freedom change. In the subject-level display, the intervals for three models include fourth place from the top. Inclusion of that position does not establish equal performance or assign a probability to a particular model occupying it. [1, §3.1, Eq. 7 and Fig. 2]

The subject-level target considers variation over subjects and their associated questions, with the particular studied prompts averaged as fixed. Any extension to future subjects requires defensible sampling or exchangeability and model assumptions; the 57 named subjects are not necessarily representative of every future task. The alternative prompt-level comparison averages over the observed subjects and questions and uses a prompt variant as the unit. It concerns a prompt population for those fixed tasks. Within a subject, using questions or prompts as units addresses other targets. The intended population, design and dependence should determine the choice. [1, §§2.2–3.2]

To examine whether the different numbers of units explained the contrast, the authors recalculated prompt-level intervals after randomly selecting 57 of the 100 variants. They report similar prompt-based results and interpret the comparison as evidence of greater subject heterogeneity in this dataset. This sensitivity check does not establish that subject variability always exceeds prompt variability, remove sampling uncertainty, or make the sample representative of other datasets. [1, §3.1]

## Interpreting rank intervals

The paper obtains rank bounds from directional paired comparisons after adjusting for multiple comparisons with Holm's method. Under the method's assumptions, a model's 95% marginal interval has at least 95% coverage in repeated samples for that model's true rank. This is not a guarantee that all 15 intervals cover jointly, and it is not a 95% posterior probability for the true rank in one realized interval. A simultaneous procedure has a different joint error-control target; the paper provides a separate example. [1, §2.1 and Appendices A, B.2]

A sample ordering and an interval for the underlying rank answer different questions. Overlapping intervals do not establish equivalence; neither does a non-significant result establish equal performance. For practical interchangeability, specify a meaningful margin and use an appropriate equivalence analysis. Failure to demonstrate a difference larger than a margin is not proof of equivalence. Conversely, statistical detection alone does not show that an effect is practically important. When population scores tie, the possible positions may form a set; the paper's coverage definition requires the interval to contain that set. [1, §§2.1, 4]

## A reasoning sequence for benchmark comparisons

1. State the decision and target: the observed evaluation set, new subjects and questions, new prompts on fixed tasks, or another population. Record which dimensions are fixed, sampled, or uncertain.
2. Preserve stable identifiers for model, subject, question, prompt, and run. Match both models on the same relevant units before subtracting; investigate missing, duplicate, or mismatched records rather than silently inventing pairs.
3. Count observations and independent or exchangeable inferential units separately. Specify the aggregation, weighting, and assumptions; subject-level averaging with equal weights targets a different quantity from weighting by the number of questions when subject sizes differ.
4. Inspect variation and dependence at the selected level. Averaging within a cluster does not by itself make clusters representative or independent. For unbalanced or crossed designs, choose a method suitable for the actual dependence and target, and report its assumptions.
5. Predefine the comparisons, multiplicity control, confidence level, and whether coverage is per model or joint. State how ties, missingness, and model selection are handled.
6. Report score differences, interval bounds, practical relevance, and uncertainty together. A narrow result under one inferential unit does not automatically transfer to a different population.

This sequence is guidance for a proposed evaluation, not evidence that an evaluation was run.

## Practice: hypothetical falsifiable controls

The following cases are invented examples, not results from the paper. Each names a check or observation that could change the conclusion.

1. **Aligned IDs:** Model A scores question IDs 1 and 2 under prompt P, while model B scores IDs 2 and 3. Pairing rows by their display order creates false matches. Only ID 2 is an observed match; a record for A on 3 or B on 1 would permit another. Verify subject, question, prompt, and run identifiers before calculating contrasts.
2. **Clusters versus observations:** A balanced evaluation has 4 subjects, 10 questions each, and 5 prompts each. It has 200 triples per model, but 4 subject-level average differences for a subject-level comparison, not 200 independent subjects. More questions can improve within-subject measurement; adding independently sampled subjects changes the between-subject evidence. These counts alone do not determine a confidence interval.
3. **Unequal sizes:** Subject X has 10 questions and a paired average advantage of 10 points; Y has 90 questions and an advantage of 0 points. Equal subject weighting gives 5 points; question weighting gives 1 point, assuming equal prompt counts. Neither is universally correct: an explicit target and weights decide which average is relevant. Different observed subject effects or weights would change the result.
4. **Marginal versus simultaneous:** Fifteen valid 95% marginal intervals do not imply 95% joint coverage of all ranks. A pre-specified simultaneous procedure with appropriate assumptions could justify a joint statement; observed overlap among the displayed intervals cannot supply that guarantee.
5. **Coverage check:** In a simulation whose true ranks and data-generating process are known, repeat the entire interval procedure over many independent simulated datasets. Count runs covering each model's true rank and runs covering all models. A low empirical coverage rate beyond simulation uncertainty would challenge the claimed guarantee for that scenario; one failure alone would not disprove 95% coverage.
6. **Practical effect:** An estimated difference of 0.1 percentage point is statistically detectable in a large, well-designed study. If a decision requires at least 2 points, statistical significance alone does not establish practical importance. A confidence interval and a pre-specified decision margin can reveal whether an effect of relevant size is supported or excluded.
7. **Overlap is not equivalence:** Two 95% rank intervals overlap. This does not prove the models are tied or practically interchangeable. A separately designed equivalence test with a prespecified score-scale margin and sufficient precision could support an equivalence claim; a wide interval or non-significant test cannot.
8. **True ties:** If two models truly have the same population score, a deterministic tie-break may assign distinct displayed positions even though the underlying ordering is not uniquely determined. State the tie rule and assess coverage of the possible-rank set; evidence of a nonzero population difference would change the tie premise.
9. **Subject sampling:** A benchmark contains only arithmetic subjects, and the desired deployment includes law and medicine. A subject-level interval over arithmetic does not automatically cover that broader deployment ranking. A justified sampling frame and data from the intended mixture could support a more relevant generalization.
10. **Prompt resampling:** Two designs use 57 independent prompt-level differences, yet one has much greater spread in those differences. Equal unit counts do not force equal standard errors. Inspect the observed paired variability and study design before attributing an interval difference to sample size alone.
11. **Unknown counts:** A report claims A is first on most subjects but does not disclose the number of subjects, the number of wins, or ties. It supplies no exact win fraction, interval, or confidence level. A complete count with its denominator and sampling design would permit an appropriately qualified calculation; do not invent one.
12. **Missing cells:** If B failed to produce outputs on hard questions and analysis keeps only complete pairs, the resulting contrast targets the retained subset and may be biased for the intended set. Compare missingness by model and task, state the policy, and check sensitivity; recovered outcomes or a justified missing-data model could alter the result.

## Takeaway

Pair like with like, then decide what must vary to answer the actual question. Rank confidence intervals are only as interpretable as their target population, dependence assumptions, error control, and treatment of ties. A paper's observed contrast between subject and prompt variability is evidence for its studied benchmark and protocol, not a universal ranking guarantee.

## Sources and scope

1. Bitya Neuhof and Yuval Benjamini, “Quantifying Ranking Uncertainty in LLM Benchmarks,” arXiv:2607.16259v1, 28 June 2026, especially §§2–4 and Appendices A–B: https://arxiv.org/abs/2607.16259. The paper is distributed under the [arXiv perpetual, non-exclusive license](https://info.arxiv.org/help/license/index.html); that is not a blanket public reuse grant.
2. Authors' analysis repository: https://github.com/BityaNeuhof/quantifying-rank-uncertainty. The repository identifies its code as MIT licensed and says the dataset is not included. Its README notes that random question sampling may cause minor ranking differences.
3. PromptEval correctness dataset record: https://huggingface.co/datasets/PromptEval/PromptEval_MMLU_correctness. The dataset card identifies its license as MIT. The paper, code and dataset have distinct terms; neither the code nor dataset license licenses the paper.

This synthesis reports the cited study and adds independently invented practice examples. It does not reproduce paper text, code, data, figures or screenshots. The prior review assessed source claims and the 12 cases by manual reasoning. No model, dataset, API, or system test was performed, and the study was not independently replicated here.
