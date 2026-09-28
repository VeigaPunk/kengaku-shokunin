# Eval-theory digest — karpathy branch + RLHF + bitter lesson

Digest of wiki pages outside `ai/agents-and-engineering` (read 2026-09-28).
Primary sources: `yao-second-half.md`, `creative-benchmark.md`,
`llm-trueskill-sorting.md`, `rlhf.md`, `bitter-lesson.md` under
`~/Projects/webzites/repos/llm-wiki/wiki/`.

## The eval-first thesis (yao-second-half)

- Post-ReAct recipe (pretrain + scale + reasoning/acting) saturated: task-
  specific methods yield ~5% while next scale-up gives ~30% untargeted →
  marginal method research; the frontier moved to **evaluation design**.
- Two eval assumptions to break: **autonomy assumption** (real tasks need
  human-in-the-loop; tau-bench/Arena measure collaboration) and **IID
  assumption** (real tasks arrive in sequence, familiarity compounds;
  academia lacks benchmarks that would justify memory methods).
- Practitioner consequence for our batteries: same-repo multi-task
  batteries (bench-arena) reward agents with memory/context carryover that
  IID-graded runs cannot show — record run-order and reuse effects.

## Diversity is unmeasured (creative-benchmark)

- RLHF optimizes median preference → mode collapse ("ChatGPTese");
  ~35% annotator disagreement is population-diversity signal treated as
  noise. No mainstream benchmark scores output diversity.
- Two implementable primitives: ranking distance to references, pairwise
  embedding distances across samples of the same prompt. Four benchmark
  families: iteration chains, style flexibility, creative constraints,
  multi-agent diversity.
- Workarounds without retraining: higher temperature (noisy, not semantic),
  best-of-N with dissimilarity selection, base models, multi-model synthesis.
- Links to our axes: a Pareto-search directive wants *breadth*; benchmark
  suites that score single answers cannot see collapse. Add a diversity
  probe (k samples × embedding spread) to any search-shape battery.

## LLM-as-judge, algorithm-as-aggregator (llm-trueskill-sorting)

- LLMs fail global sort at 4 seams: context overflow, transitivity
  violations, attention degradation mid-list, output-token budget.
- Composition: LLM orders ~10-item batches; TrueSkill (Bradley-Terry
  Bayesian update, μ/σ per item) aggregates; sort by μ−3σ; ~1–2 matches
  per item to converge; monitor σ-tail and top-k churn.
- General rule: give the **judgment** to the model, the **aggregation** to
  a classical algorithm; pairwise > absolute scoring (same Kahneman-noise
  asymmetry RLHF exploits).
- Our use: when ranking N candidates/outputs, never ask the model to emit
  a global order; batch-compare and aggregate.

## RLHF mechanics that leak into evals (rlhf)

- Pairwise preference → Bradley-Terry reward model → PPO with KL penalty
  (`r = r_θ − λ·KL(π_RL‖π_base)`); the KL term exists because any optimizer
  finds proxy cracks → reward hacking. Costs: demonstrations $10–20,
  preference labels $0.50–2, model text ~free.
- Failure modes that surface in evaluation: reward-model overoptimization
  (Gao 2022), annotator disagreement averaged incoherently, specification
  gaming (persuasive ≠ accurate), scalable-oversight gap.
- Eval relevance: judges trained/aggregated the same way inherit the same
  proxy gap — a single scalar judge score is a reward model with KL absent.

## Bitter lesson framing (bitter-lesson)

- 70-year pattern: general methods leveraging compute (search, learning)
  beat hand-engineered domain knowledge, in chess/Go/speech/vision/games.
- Regime caveat (via gigerenzer link): inverts under small data/noisy
  signal — structured heuristics win there; don't universalize.

## Cross-cutting rule for this domain

Eval design is the research surface: prefer pairwise/comparative signals,
measure diversity explicitly, treat every scalar judge as a proxy needing
a KL-analog (fresh re-grounding in primary evidence), and expect knowledge-
heavy eval hacks to be eaten by the next scale step.
