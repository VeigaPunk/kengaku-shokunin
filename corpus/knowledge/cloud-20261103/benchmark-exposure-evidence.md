# Kengaku knowledge lesson 6: Exposure, evidence, and the timing of contamination

## Aim

Distinguish opportunities for benchmark exposure from evidence that a particular model actually trained on an item, and distinguish both from the size of any resulting score inflation. A harder held-out set can broaden an evaluation, but a score gap between different sets is not a contamination estimate. A clean-looking checkpoint also does not establish what will happen after later training.

## Case 1: Public copies and synthetic neighbors

In a 2024 study of code evaluation, Matton and colleagues searched public GitHub repositories for HumanEval prompts and found many copies. They also found high prompt similarity between public coding benchmarks and synthetic datasets, including semantic similarities that exact-string filtering could miss. Public availability and similarity create plausible exposure paths. Neither observation establishes that a particular model ingested a particular benchmark item: that needs model-specific training or selection provenance, or a carefully qualified inference from other evidence. A similar programming problem may share a domain or structure without being a leaked copy. [1, §§3.1–3.2]

Synthetic data adds an indirect path. A generator can produce a near-neighbor or reproduce material present in its inputs or earlier training, and a later model might train on that output. But a similarity match alone does not establish the generator's source, whether the later model trained on that example, or whether training on it increased an evaluation score. Overlap checks should examine provenance and semantic as well as exact matches, with their own false-positive and false-negative limits. [1, §3.2]

The authors report that adding evol-instruct to a Command R Refresh fine-tune increased HumanEval by 9% and MBPP by 2%, while LBPP was unchanged. They report those changes as percentages; the text does not specify a percentage-point interpretation, so do not convert them to points. This is evidence about that fine-tuning comparison and these benchmark outcomes, not proof that leakage was the sole cause. The paper itself considers both direct leakage and broad coverage of similar problems as possibilities; differences in task difficulty and transfer can also matter. [1, §3.2]

## Case 2: A harder set is not a clean subtraction

The same authors created Less Basic Python Problems (LBPP), 161 human-authored coding problems with unit tests. Experienced annotators were asked for original problems, including problems inspired by non-freely-available textbooks without copying their exercises. A strong model was used in the loop to select problems it could not solve, and reviewers checked originality and ambiguity. This procedure deliberately made the collection harder; it does not make LBPP interchangeable with HumanEval. [1, §4]

In the paper's historical zero-shot pass@1 table, Mistral Large scored 0.92 on HumanEval and 0.50 on LBPP, a difference of 0.42, or 42 percentage points. The tasks differ in content and difficulty, so 42 points is not an estimate of contamination, nor a claim about the current model or current leaderboard. The result supports using varied evaluations and reporting their construction rather than translating the cross-benchmark gap into memorization. [1, Table 2 and §4]

The authors constructed LBPP as a new, held-out benchmark for their contemporary evaluations and subsequently released it publicly. That release creates a possible path into later corpora and synthetic data. It is not a permanent cleanliness guarantee: for a later model, check the relevant benchmark version, publication and training dates, and data and selection provenance rather than relying on the original description. Dates constrain possible paths, but a date alone cannot rule out earlier private access, related sources, undocumented training stages, or later re-use. [1, abstract and §4; 2]

## Case 3: The gap can return after post-training

Kocyigit and Yildirim's separate 2026 preprint uses a controlled injection rather than inferring training from public overlap. They started from Qwen2.5 checkpoints of 0.5B and 1.5B parameters and Gemma3 checkpoints of 1B and 4B, then compared clean and contaminated extended-pretraining arms. The contaminated mixture included five copies of GSM8K and MBPP test items in its first 2 billion tokens of a roughly 25-billion-token continuation; the clean arm did not receive that injected test material. The authors then separately applied supervised fine-tuning (SFT) or group relative policy optimization (GRPO), using post-training data they describe as uncontaminated. The clean and contaminated continuations provide an experimental comparison, not a provenance audit of any deployed product. [3, abstract and §3]

The authors report that the contaminated-versus-clean score gap could narrow toward zero during continued pretraining and reappear after post-training. In their experiments, SFT's extra gains appeared on the injected tasks but not on the selected comparison benchmarks; GRPO also showed gains on those comparison benchmarks, which the authors interpret as evidence of some broader transfer. GSMPlus and HumanEval are comparison sets, not perfect matched twins of GSM8K and MBPP: the authors note that HumanEval and MBPP have different difficulty levels. The observations concern the tested injected items, checkpoints, two model families up to 4B, token mixture, training recipes, benchmarks and metrics. The paper’s 95% intervals describe evaluation-time uncertainty and exclude training-seed variability. These results do not prove that any production model was contaminated, that zero measured difference means no prior exposure, or that every post-training method will revive a hidden effect. [3, §§3–5 and limitations]

## A reasoning sequence for an evaluation claim

1. **Name the claim.** Is it that an item was publicly accessible, appeared in a candidate corpus, was actually used in a particular training run or selection process, or inflated the final score? These are different propositions, each needing its own evidence.
2. **Trace the path and time.** Record benchmark item and version, public or private release date, candidate source, collection dates, deduplication, training and post-training runs, and checkpoint selection. Distinguish documented access and inclusion from unknowns. A publicly available item is a risk signal, not a model-specific training log.
3. **Inspect matches.** Preserve the compared texts and match method. Review exact matches, paraphrases, code structure, and alternative common-source explanations. A match can be relevant even when it is not verbatim, but similarity alone cannot settle provenance or effect.
4. **Use a suitable counterfactual.** Where an authorized study exists, compare otherwise matched clean and deliberately contaminated arms from the same starting checkpoint, with documented mixtures, exposure dosage, seeds, evaluation, and uncertainty. Check whether other changes confound the comparison. Exposure can be known in the injected continuation even if the original checkpoint's entire prehistory is not independently established.
5. **Observe the lifecycle and a broader target.** Compare equivalent checkpoints before and after later training, and include independently constructed, appropriate comparison tasks where possible. Describe their domain, difficulty, and independence; avoid treating differences between unlike tasks as a pure leakage effect.
6. **Report what is known and unknown.** State counts, denominators, metrics, versions, uncertainty, and plausible alternative explanations. A small or null observed gap can be consistent with a small effect, imprecision, or a difference that appears only under other conditions; it does not prove absence of training exposure.

This is a proposed reasoning and study design, not a claim that any experiment was executed for this lesson.

## Practice: hypothetical falsifiable controls

These invented cases are not additional results from either paper. Each states what the given evidence supports and what further observation would change or narrow the conclusion.

1. **Public copies:** A test prompt appears in 100 public repositories. No information links those repositories to model A's training. Exposure is possible, not established for A. A verified training manifest and item-level inclusion record covering A's relevant run would support a stronger inclusion claim; evidence the sources were excluded would weaken that path but may not eliminate every other path.
2. **Synthetic neighbor:** A synthetic prompt resembles a test problem in wording and algorithm, but both could derive from a common textbook exercise. The match warrants inspection, not an assertion that the benchmark leaked into model B. A documented generator input and output lineage, followed by B's ingestion record, would distinguish the proposed path from the common-source account.
3. **Known injection:** Two continuations start from the same checkpoint and use matched recipes except that one receives five documented copies of selected test items. Successful ingestion logs establish exposure in that continuation. A higher contaminated-arm score, with appropriate repeated-run uncertainty, estimates an effect for that intervention and setup; it does not by itself establish the cause of any other model's score.
4. **Harder held-out comparison:** A model scores 90% on a public set and 50% on a new set whose items are deliberately harder. The 40-point difference is observed, not a 40-point leakage estimate. A matched controlled intervention can test an exposure effect; a simple score gap cannot separate exposure from differences in task distribution.
5. **Gap at checkpoints:** A controlled contaminated arm leads by 8 points soon after injection and by 1 point after further pretraining. That describes a narrowing in those measurements. It does not show the items were erased or establish the size of any later effect; compare the documented arms again after the specified post-training recipe.
6. **Post-training divergence:** After matched post-training, the same controlled arms differ by 4 points on injected items and by 0 on a separate comparison set. The pattern is consistent with a local advantage in that setup, but a zero observed difference is not proof of zero transfer. Report sample sizes, intervals, test sensitivity, and whether the comparison set is genuinely independent and sufficiently similar.
7. **Null result after injection:** In a small experiment, the contaminated arm's score is 1 point higher with an interval that also permits a meaningful decrease or increase. The recorded injection still establishes exposure; the effect's direction and magnitude remain uncertain. More informative comparisons could narrow the interval rather than turning this result into a claim of cleanliness.
8. **Release after a documented cutoff:** A benchmark was first made public in 2025, and the documented data collection for one model ended in 2024. That timeline rules out ingestion from the 2025 public release in that particular collection window, assuming the dates are accurate. It does not rule out prior private access or related material, and says nothing about a later fine-tuning run unless that run is also documented.
9. **Release before training:** A benchmark was public in 2023, and a model's data collection occurred in 2025. The chronology makes exposure possible, not established. Evidence of inclusion in the actual mixture would strengthen the claim; an audited exclusion for all relevant stages would weaken that particular explanation.
10. **Changed recipe confound:** The contaminated arm also receives a larger learning rate and a different post-training dataset. Its higher score cannot be attributed to injected examples alone. Matching those factors or adding appropriate ablations would test competing explanations.
11. **Different units:** A report states that a score increased by 9% without specifying whether this is a relative change or a percentage-point change. Preserve the author's wording and request the baseline and calculation. If a score rises from 50% to 59%, the increase is 9 percentage points but 18% relative to the baseline; the two quantities differ.
12. **Selection without training exposure:** A developer repeatedly picks checkpoints using the same public benchmark but provides no benchmark items in training. The benchmark can still become a selection target, limiting its independence as a final evaluation. Selection records would support this claim; they do not establish that the item text was used as a training example.

## Takeaway

An accessible or similar item is a reason to investigate, not proof of model-specific ingestion. Establishing exposure and estimating its effect require different evidence. Compare like with like, include post-training in the timeline, and preserve uncertainty when a benchmark is harder, provenance is missing, or a measured gap is small.

## Sources

1. Alexandre Matton, Tom Sherborne, Dennis Aumiller, Elena Tommasone, Milad Alizadeh, Jingyi He, Raymond Ma, Maxime Voisin, Ellen Gilsenan-McMahon, and Matthias Gallé, “On Leakage of Code Generation Evaluation Datasets,” arXiv:2407.07565v3, 3 October 2024, §§3–4 and Table 2: https://arxiv.org/abs/2407.07565v3 (HTML: https://arxiv.org/html/2407.07565)
2. Cohere For AI, LBPP public dataset release: https://huggingface.co/datasets/CohereForAI/lbpp . The public repository may evolve; the historical results above are attributed to the 2024 paper.
3. Muhammed Yusuf Kocyigit and Caglar Yildirim, “The Impact of Post-training on Data Contamination,” arXiv:2601.06103v1, 3 January 2026, §§3–5 and limitations: https://arxiv.org/html/2601.06103

The two cited articles are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This lesson paraphrases and summarizes their findings; it does not reproduce their benchmark datasets.

Neither paper supplies proof of contamination for a particular current production model.

## Manual review record

An independent reviewer manually assessed all 12 hypothetical controls:

1. Public copies establish possible exposure, not model-specific ingestion; provenance could strengthen or weaken the proposed path.
2. Similarity admits a common-source explanation; generator lineage and the later model's ingestion records would help distinguish the path.
3. Documented injection establishes exposure in that continuation; the controlled score difference estimates an effect for that setup.
4. The observed 40-point cross-task gap is not a leakage estimate because the sets differ in difficulty and content.
5. A narrowing gap does not establish erasure or the later effect; reassess after the specified post-training.
6. A local advantage with zero observed comparator gap does not prove no transfer; uncertainty and comparator quality matter.
7. Documented injection establishes exposure even when an interval leaves the effect imprecise.
8. A later public release cannot be the source of an earlier collection on the stipulated dates, but earlier private access or later training remains possible.
9. Release before collection permits exposure but does not establish inclusion; audited inclusion or exclusion changes the evidence.
10. Differences in learning rate and post-training data confound attribution to injection; matching or ablations can address them.
11. A change from 50% to 59% is 9 percentage points and 18% relative; the paper's ambiguous 9% wording should not be silently converted.
12. Selecting checkpoints against a benchmark weakens evaluation independence without proving its items were used in training.

This record describes a manual reasoning review of invented examples. No model, dataset, API, or system tests were run for this lesson.
