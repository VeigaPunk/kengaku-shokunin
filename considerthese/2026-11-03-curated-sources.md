# kengaku: curated sources to consider after hyaku

Date: 2026-11-03

**Status: unassimilated future reading.** These are candidate references, not trained knowledge, verified local capabilities, adopted dependencies, or changes to current training. Reserved for possible post-hyaku assimilation under the lane’s normal admission review. Earlier dated reflections remain unchanged.

Selection checked against the supplied PROVINCE, source registry and considerthese context, including exact URLs and source-entity mentions. Kengaku was checked against its reconciled active context. No candidate code was executed.

## 1. HELM: Holistic Evaluation of Language Models

- Type: Methodology paper.
- Primary source: <https://arxiv.org/abs/2211.09110v2>
- Why this is worth considering: An evaluation-design counterweight to a single headline score: define the scenario population, expose coverage gaps, and preserve multiple outcome dimensions under comparable conditions. Useful alongside this lane’s grader audits and calibration work.
- Possible later exercise: After hyaku, map one existing benchmark to a scenario-by-metric sheet, explicitly marking unmeasured cells. Separate output-contract compliance, task correctness, and resource cost before interpreting a model comparison.
- Boundaries and caveats: The paper is foundational, not a current model leaderboard. Its historical results do not establish present model rankings. General research-source methodology remains chousa’s province.
- License/reuse: CC-BY-4.0 (arXiv license link verified). Evidence: <https://creativecommons.org/licenses/by/4.0/>.
- Currency/maintenance: Fixed v2, revised 2023-10-01; selected for durable method rather than recency.
- Duplicate check: no exact primary URL or source-entity match in the supplied lane context.

## 2. EvalPlus

- Type: Repository.
- Primary source: <https://github.com/evalplus/evalplus>
- Why this is worth considering: Expanded code-correctness tests and oracle corrections give a concrete reference for how underspecified or weak test suites can overstate capability. The repository also distinguishes base-model and chat-model prompting.
- Possible later exercise: After hyaku, inspect one documented oracle repair and write a hypothetical counterexample that passes the original tests but fails the strengthened contract. Keep this a grader-design comparison, not a new model result.
- Boundaries and caveats: Generated code is untrusted. Do not copy execution commands or the EvalPerf system-setting changes into a training run. Dataset terms and model terms require separate review. Current maintenance freshness is not fully established.
- License/reuse: Apache-2.0 for repository code. Evidence: <https://raw.githubusercontent.com/evalplus/evalplus/master/LICENSE>.
- Currency/maintenance: Accessible official repository; fetched commit history exposes activity on 2025-10-02, but its cached view does not prove 2026 maintenance.
- Duplicate check: no exact primary URL or source-entity match in the supplied lane context.
- Supporting evidence: <https://raw.githubusercontent.com/evalplus/evalplus/master/README.md>, <https://github.com/evalplus/evalplus/commits/master/>.
