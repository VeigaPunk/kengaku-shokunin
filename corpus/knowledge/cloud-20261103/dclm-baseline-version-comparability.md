# A score is a measurement contract

**Topic:** Language-model evaluation and calibration. Sources accessed 2026-11-03.

## Objective

Given a reported aggregate score, identify the evaluated task format, baseline and version before making a comparison. A correct answer distinguishes a change in the measurement from a change in the model; checks the task set and aggregation denominator; and states uncertainty without upgrading a plausible conclusion to a guarantee.

## The incident

DataComp-LM (DCLM) reports aggregates built from task accuracies normalized against task-specific reference values. In [issue #114](https://github.com/mlfoundations/dclm/issues/114), contributor `jeffreywpli` explained that some reference values had been selected for the original versions of tasks rather than the variants used by their `llmfoundry` evaluations. The problem concerned the inputs to centering; it did not establish a change in the recorded raw accuracies or model weights.

For the four-option `bigbench_language_identification` evaluation, the reference changed from 9.1% to 25%. For `agi_eval_lsat_ar`, the original five-option task became four-option and the reference changed from 20% to 25%. The `commonsense_qa` evaluation combined two labels in a four-option version, and its reference changed from 20% to 40.3%.

The intended policy was more nuanced than setting every reference to the reciprocal of the number of options, N. According to the contributor, a majority-label rate would replace 1/N when it exceeded 1/N by more than 0.05 and there were at least N in-context examples. The 62% yes-label reference for BoolQ was intentional under that rationale. This describes the project's design choice, not a universal endorsement of majority-label centering.

The project introduced corrected v2 aggregates while retaining v1 for historical comparison in [PR #115](https://github.com/mlfoundations/dclm/pull/115), merged on 2025-09-09. The PR reports Spearman correlation above 0.999 in its empirical comparison; issue #114 gives the weaker bound above 0.99. The result is evidence of substantial rank consistency for the analyzed results, not proof that every pair kept its order or that the result applies to other populations. In the [README](https://github.com/mlfoundations/dclm), the same DCLM-BASELINE 7B, 2.6T-token row has CORE v1 57.1 and v2 56.0. These are alternative versions of an aggregate, not evidence that the model degraded or changed.

## Mechanism and a worked counterfactual

The [aggregation code](https://github.com/mlfoundations/dclm/blob/main/eval/aggregated_metrics.py) computes each centered score as

`centered = (raw_accuracy - baseline) / (1 - baseline)`

where both inputs are proportions; metadata stores the baseline as a percentage and code divides by 100. Selected task-level centered scores are averaged for the aggregate. This transformation puts the chosen baseline at 0 and perfect accuracy at 1. It can be negative below baseline, and is undefined when baseline equals 1. The relevant denominator is `1 - baseline`, not the baseline or the number of answer choices. The aggregation's task count is a separate denominator.

**Our hypothetical arithmetic, not a source-reported model result:** holding raw accuracy fixed at 0.60 yields `(0.60 - 0.20)/(1 - 0.20) = 0.50`; using baseline 0.403 gives `(0.60 - 0.403)/(1 - 0.403) = 0.197/0.597 ≈ 0.330`. This difference reflects the centering assumption. It is not a 17-point drop in raw accuracy. A single-task example does not recover the README's aggregate difference because the aggregate includes other tasks and their changes.

## Practical evaluation procedure

1. Trace the exact dataset split, task implementation, answer choices, label mapping and in-context setup used by the run. Check the baseline against that implementation and the stated policy; do not infer it solely from a canonical task name.
2. Record raw per-task outputs, metadata/version, aggregation task list and missingness alongside the score. A score without this provenance is not enough to certify comparability.
3. Recompute both models with the same version, inputs and complete task set when evidence permits. If not, label the comparison unresolved rather than directly subtracting v1 from v2. Retain historical results rather than silently rewriting them.
4. Inspect both the normalization denominator and which tasks contribute to each reported mean. A full-suite claim requires the expected tasks, not merely a numeric-looking partial average.
5. Treat aggregate rank correlation as population-level evidence, not a guarantee for a particular pair. Check that pair and quantify relevant sampling uncertainty before claiming a winner.
6. For a benchmark or model-grader report, separately validate the grading target, answer key/label mapping, parsing and aggregation. A corrected baseline alone does not establish that the grader measures the intended capability, that the result generalizes, or that a training intervention is safe.

The current aggregation code explicitly marks `Core_{version}` unavailable if a required CORE task is absent, and `Extended_{version}` unavailable if metadata tasks are missing. It also calculates other means before those checks. These gates check task-key presence; they do not by themselves validate every present value, including null or invalid values. [Issue #121](https://github.com/mlfoundations/dclm/issues/121) separately alleges these other numeric means can silently reflect only available tasks. It was open when checked; treat its implications as a reported concern, not an adjudicated maintainer finding or a test result from this lesson. Inspect the exact output field and task coverage before interpretation.

## Proposed falsifiable checks

These are designed cases and expected judgments, not executed tests. Each case can fail if the stated expected judgment is not reached. For grading, require the essential reasoning stated after **Pass**; reject the specific contrary judgment after **Fail**. Equivalent wording is acceptable. The goal is measurement interpretation, not recall of identifiers alone.

1. **Version mismatch.** A report compares 57.1 CORE v1 with 56.0 CORE v2 for the same DCLM row and says the model got worse. **Pass:** reject that conclusion; identify normalization-version change and request same-version comparison. **Fail:** accept a 1.1-point decline as model deterioration.
2. **Historical comparability.** Two reports use v1 with the same implementation, task list, and baselines, with full coverage. **Pass:** regard them as comparable on this version dimension while still checking model/evaluation conditions and uncertainty; identify v1 as historical. **Fail:** declare comparison invalid solely because v2 exists, or establish overall validity from version alone.
3. **Centering arithmetic.** Raw accuracy 0.60 and baseline 0.403. **Pass:** show or imply `(0.60-0.403)/(1-0.403) ≈ 0.330`; distinguish raw from centered. **Fail:** return 0.197 as centered or divide by 0.403.
4. **Invalid denominator.** A proposed baseline is 1.0. **Pass:** flag division by zero and decline to compute the centered value. **Fail:** produce a finite score or silently substitute a baseline.
5. **Imbalance exception.** An evaluator applies 0.50 to DCLM BoolQ solely because there are two labels. **Pass:** flag conflict with the maintainers' deliberate 0.62 majority-label policy and request exact setup. **Fail:** call 0.50 automatically correct or assert 0.62 is universally correct for all BoolQ implementations.
6. **Missing CORE task.** An expected CORE task is absent; another aggregate field contains a number. **Pass:** do not present that number as full CORE; note the code's versioned CORE N/A behavior and check coverage. **Fail:** declare complete CORE solely because some other mean is numeric.
7. **Complete task coverage.** All tasks required by the specified CORE definition are present, with matching version and compatible inputs. **Pass:** accept the missing-task gate as satisfied, while leaving correctness of raw scores, metadata and uncertainty to separate checks. **Fail:** claim missingness solely because some unrelated EXTENDED task is absent, or claim the whole evaluation validated merely because CORE is complete.
8. **Correlation versus pairwise ordering.** The PR reports Spearman >0.999 over its analyzed results. **Pass:** say ranks were highly consistent in that analysis, but verify a particular pair before asserting its order is unchanged. **Fail:** say every pair is necessarily unchanged, or dismiss the finding as evidence of no consistency.
9. **Insufficient precision.** Two models' point estimates differ by 0.1 points, without sample counts, uncertainty or paired results. **Pass:** report the observed difference with version and ask for uncertainty/paired evidence before a reliable superiority claim. **Fail:** assert a statistically reliable winner from the point estimates alone.
10. **Grader validity.** A grader returns the expected numeric aggregate after a baseline correction, but its answer-key mapping was not checked. **Pass:** distinguish arithmetic correctness from grading validity and request a mapping/label audit. **Fail:** certify the grader or model capability solely because arithmetic matches.
11. **Baseline matches the run.** A four-choice evaluation has a documented majority label of 40.3% under the relevant policy. **Pass:** use 0.403, not automatically 0.25, if the stated policy's conditions are met; otherwise withhold the choice pending missing details. **Fail:** infer 0.25 from choice count alone or apply the majority rule without checking its conditions.
12. **Source claim versus extrapolation.** An open issue alleges partial means can appear complete. **Pass:** attribute the concern to #121, inspect coverage and exact field, and say it remains unadjudicated here. **Fail:** assert that maintainers confirmed the allegation or that every output is necessarily wrong.

## Scope and evidence limits

This is a source synthesis with a hypothetical calculation and proposed checks. No check was executed on a model, dataset, API or system, and no model weights were trained as part of this work. The material does not establish generalization or safety.

## Sources

- [DCLM issue #114](https://github.com/mlfoundations/dclm/issues/114): maintainer explanation, baseline policy and three CORE corrections.
- [DCLM PR #115](https://github.com/mlfoundations/dclm/pull/115): merge date, version preservation, correction and reported rank correlation.
- [DCLM aggregate implementation](https://github.com/mlfoundations/dclm/blob/main/eval/aggregated_metrics.py): normalization, aggregation and missing-task handling; `main` is mutable.
- [DCLM repository README](https://github.com/mlfoundations/dclm): version guidance and model table; `main` is mutable.
- [DCLM issue #121](https://github.com/mlfoundations/dclm/issues/121): separate open allegation about partial means, not a resolved finding.

## Independent manual review of proposed cases

An independent reviewer manually assessed all 12 proposed cases in the original lesson draft and passed their stated expected judgments. This review did not execute the cases against a model or system. The present public-facing adaptation has not itself received that independent review.

1. **Pass:** A version change is not evidence of model degradation.
2. **Pass:** Two v1 scores are comparable only conditionally on matching implementation, task set and other evaluation conditions.
3. **Pass:** The hypothetical centered score is 0.197/0.597, approximately 0.330.
4. **Pass:** A baseline of 1 causes division by zero.
5. **Pass:** BoolQ's majority-label policy is conditional, not a universal binary-task rule.
6. **Pass:** A missing required CORE key is guarded; a numeric value in another field is insufficient to establish complete CORE.
7. **Pass:** Satisfying the CORE missing-task gate does not validate the entire evaluation.
8. **Pass:** High rank correlation does not guarantee preservation of every pairwise ordering.
9. **Pass:** A point-estimate gap alone does not establish statistically reliable superiority.
10. **Pass:** Correct arithmetic does not establish grader validity.
11. **Pass:** The majority baseline applies under the stated policy only if both policy conditions hold.
12. **Pass:** Attribute the separate concern to issue #121 and check the field and coverage; the issue remains unadjudicated here.

No model, dataset, API or system test or model training occurred as part of this review. Generalization and safety remain unestablished.

**Source rights note:** The [DCLM repository license](https://github.com/mlfoundations/dclm/blob/main/LICENSE) is MIT, copyright © 2024 mlfoundations. This synthesis reports facts and describes the mathematical method; it does not reproduce repository code, datasets or figures. The repository license does not itself establish the rights status of individual issue or pull-request comments.
