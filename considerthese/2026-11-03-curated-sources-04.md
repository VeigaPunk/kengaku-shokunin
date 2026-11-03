# kengaku: fourth curated source to consider after hyaku

Date: 2026-11-03

**Status: unassimilated future reading after hyaku.** A methodological candidate, not an evaluation result or adopted dependency. No model calls, dataset downloads or benchmark execution.

## WildBench: when length correction changes a judgment

**Primary source:** Ai2's [WildBench snapshot](https://github.com/allenai/WildBench/tree/d6b8dcaf377d173d031980f97c16e1a82618c03d), revision d6b8dcaf377d173d031980f97c16e1a82618c03d. Its [commit record](https://github.com/allenai/WildBench/commit/d6b8dcaf377d173d031980f97c16e1a82618c03d) dates to 2024-08-01T07:26:26Z. Read 2026-11-03; this is a historical reference, not a current leaderboard claim.

**Source summary:** WildBench uses example-specific checklists for judgment. Its pairwise aggregation converts a slight win into a tie when the winner exceeds the loser's character length by more than K; strong wins remain unchanged. Marked truncated or empty responses contribute no labels, but remain in the overall reward denominator, len(eval_result). Task-category rewards instead divide by counted labels, task_instance_num. The README describes GPT-4-turbo scoring, while the table script's ordinary score branch selects GPT-4o: prose alone does not establish the evaluator configuration.

**Reading path:** README.md, Evaluation → Metrics → Mitigating Length Bias; [leaderboard/data_dir/_create_tables.py](https://github.com/allenai/WildBench/blob/d6b8dcaf377d173d031980f97c16e1a82618c03d/leaderboard/data_dir/_create_tables.py), lines 66–71, 109–153 and 159–196; leaderboard/show_eval.sh, the multiple K settings.

**New domain gap:** Existing judge-calibration and prompt-sensitivity reading does not substitute for auditing a deterministic transformation between raw preference labels and reported rankings.

**Bounded future question, original proposal:** After hyaku, could two models reverse ordering solely through this correction? Draft six synthetic pairwise records covering slight/strong wins, both winner orientations, an exact-K boundary and an excluded response. Hand-tabulate raw and corrected labels at disabled, zero and one positive K. Calculate both denominator conventions and preserve exclusion counts before comparing overall and category aggregates. This is a proposed paper exercise, not a claim that correction improves validity.

**Limits and rights:** Character length is not relevance or correctness. Historical evaluator choices and thresholds require separate validation. Repository [license](https://github.com/allenai/WildBench/blob/d6b8dcaf377d173d031980f97c16e1a82618c03d/LICENSE) is Apache-2.0; external dataset and provider terms remain separate. WildBench, paper identifier and repository aliases were absent from the reviewed registries and three earlier batches.
