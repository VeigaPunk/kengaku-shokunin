# kengaku: benchmark evolution without protocol drift

Date: 2026-11-03 · Batch 5

**Unassimilated post-hyaku reading proposal; assimilation awaits the user’s explicit instruction.** No benchmark, model call, training, installation or corpus change was performed. This is a historical-to-current protocol comparison, not a current-best benchmark ranking.

## From MMLU breadth to MMLU-Pro discrimination

**Timeline and reading.** Hendrycks et al.'s [MMLU](https://arxiv.org/abs/2009.03300v3) first appeared 2020-09-07; the selected v3 is 2021-01-12, associated with ICLR 2021. Its 57-subject multiple-choice design made broad academic coverage measurable. Wang et al.'s [MMLU-Pro](https://arxiv.org/abs/2406.01574v6) first appeared 2024-06-03; selected v6 is 2024-11-06, accepted to NeurIPS 2024 Datasets and Benchmarks. Read dataset construction and prompt-robustness experiments: harder reasoning-oriented items, removal of noisy/trivial questions and up to ten choices alter the measurement problem, rather than merely increasing a leaderboard's difficulty.

**Current implementation bridge.** The official repository [snapshot](https://github.com/TIGER-AI-Lab/MMLU-Pro/tree/f418b116db00b065c2aea046518d8fcf74d39872), dated [2026-03-18T03:57:33Z](https://github.com/TIGER-AI-Lab/MMLU-Pro/commit/f418b116db00b065c2aea046518d8fcf74d39872), was resolved and read on 2026-11-03. Its [README evaluation example](https://github.com/TIGER-AI-Lab/MMLU-Pro/blob/f418b116db00b065c2aea046518d8fcf74d39872/README.md) enables wrong-answer retries, although the runner default is zero. The accompanying [runner](https://github.com/TIGER-AI-Lab/MMLU-Pro/blob/f418b116db00b065c2aea046518d8fcf74d39872/evaluate_from_apiX.py#L1479-L1493)'s comparison with the known answer makes this a material protocol choice. This observation does not invalidate the paper or establish how any published score was produced.

**What changed and stayed.** More alternatives change the guessing baseline; different selection and subject mixtures change what the score represents. Both remain bounded question-answer tests, not evidence of tool reliability, real-world competence or absence of contamination. The older benchmark remains useful for historical continuity and overlapping subject diagnostics when its exact version and protocol are preserved. That usefulness is a design judgment, not a recommendation to merge the two scores.

**Original future question.** After hyaku, would a model ordering survive a comparison that separates benchmark choice, answer extraction and correctness-conditioned retries? First design a paper ledger with first-attempt accuracy, separately labeled retry-assisted results, truncations and total token budgets. Keep question-set changes separate from harness changes; no execution is proposed here.

**Rights and novelty.** MMLU's arXiv record grants distribution to arXiv, not general reuse. MMLU-Pro's paper is CC-BY-4.0; repository [LICENSE](https://github.com/TIGER-AI-Lab/MMLU-Pro/blob/f418b116db00b065c2aea046518d8fcf74d39872/LICENSE) is Apache-2.0. Dataset rights require independent review before copying. Only original commentary and links are included. MMLU is mentioned in the supplied registry, but these papers, MMLU-Pro and this protocol transition were absent from all supplied prior-batch context.
