# Eval-design digest — karpathy branch remainder + ai books/foundations

Second digest pass (round 5), covering what `eval-theory-notes.md` left open:
`karpathy/talks/`, `karpathy/projects-and-tools/`, `karpathy/standards-and-specifications/`,
unread `philosophy-and-concepts/` and `gwern-essays/` pages, `ai/foundations/complexity.md`,
`ai/books/`. Read 2026-09-28 via targeted `grep -n` + `sed` against the working copy
(`~/Projects/webzites/repos/llm-wiki/wiki/`). Line numbers below are from that read.

Rules extracted, ranked by how directly they change how this domain runs evals:

## Epistemics of failure claims

1. **"Sampling can prove presence, never absence"** — `gwern-essays/gpt-3-nonfiction.md:19,23-27`.
   A task FAIL at temp=0/n=1 is evidence of *insufficient sampling exploration*,
   not absent capability. Direct consequence for the bench-arena n=1 flip rule
   (`bench-arena-fresh-run.md` claim 2): a FAIL status is weaker evidence than a
   PASS. PASS proves the capability exists (modulo test integrity); FAIL only
   bounds it at that sampling budget. Asymmetric weights: PASS rows are
   near-falsifiable claims; FAIL rows are priors to re-probe at n≥2 or higher
   temperature before citing.
2. **Silent failure needs an expected number** — `philosophy-and-concepts/karpathy-recipe-neural-networks.md:25,31-33`.
   "Every component reports success… the only evidence is the gap between the
   number you got and the number you should have gotten." This is the ex-ante
   prediction discipline re-derived: without a recorded expectation there is no
   error signal. Also Stage-3 ("overfit one batch first") maps to the smoke-
   gate rule in SKILL.md's production checklist — prove capacity on the minimum
   viable slice before scaling.
3. **Systematic bias is a floor, not a fix** — `gwern-essays/replication-crisis.md:22,28-29`.
   Preregistration fixes random error only; selection bias in what gets
   measured/accepted is structural. Applies to corpus work: self-selected
   task batteries (we chose 33 tasks) carry an unmeasurable selection floor;
   per-round claims stay valid only as *relative* deltas on a fixed battery.
4. **Reference-class substitution** — `ai/foundations/complexity.md:32,109`.
   Gwern's refutation of worst-case-complexity pessimism: measuring against an
   adversarial reference class instead of the natural distribution. Eval
   analogue: a benchmark suite is a chosen reference class; a model that looks
   weak on adversarial task selection may dominate the natural task
   distribution, and vice versa. When comparing models, state which
   distribution the battery samples.
5. **Small per-instance edges compound to dominance** — `complexity.md` premise-3
   refutation (~line 40-52, chess 94%→99.8% match rate). Single-task deltas
   understate match-level differences; win-set complementarity
   (`local-bench-arena.md`) matters more than headline pass-rate gaps.

## Eval as a product/architecture surface

6. **Autonomy is continuous and task-varying** — `philosophy-and-concepts/partial-autonomy.md`
   (slider table at :56–65; optimal-per-task rationale :67; trust calibration :81). The eval-design consequence:
   scoring autonomy as binary agentic/not-agentic misses the real variable —
   the *optimal slider position per task class*. τ²-bench (shared control) is
   the only shortlist benchmark touching this axis; SKILL.md's decision table
   already lists it, this note grounds *why* it's irreplaceable.
7. **Planning, not step execution, is the reliability bottleneck** —
   `agent-engineering.md:76` ("a model that can execute individual steps
   perfectly may still fail at planning"). Eval consequence: single-step task
   batteries (like bench-arena's 33) cannot measure the failure mode that
   dominates deployed agents; treat them as execution-floor probes only.
8. **Evals are part of intent, not an afterthought** — `agent-engineering.md:61`:
   intent spec = goals + evals + environments. A task without a scoring rule
   is an underspecified intent, not a benchmark.
9. **"Correct but unacceptable" is a real verdict class** —
   `guo-software-abundance.md:34-36,54` (tier table: test-anchored → taste-heavy).
   Code that passes tests but violates unstated invariants is rejected by
   owners. Grader-visible PASS/FAIL is only tiers 1–3 of Guo's spec-ability
   spectrum; anything tier 4+ (refactors, APIs, abstractions) is ungradeable
   by `test.sh`-style harnesses — name that ceiling when reporting coverage.

## Mechanism notes (weaker claims, flagged opinion-by-source)

- **Jagged intelligence** — `software-three-point-zero.md:74-76`: capability
  boundary is non-intuitive; "test at the boundaries." Supports the
  boundary-task-repeat rule.
- **Steering is range-bounded, not continuous** — `interpretability-for-builders.md:79`:
  the usable control range is discovered empirically by finding the cliff;
  same epistemics as temperature sweeps.
- **Index files > RAG at ~400K words** — `llm-knowledge-bases.md:102,138`
  + `karpathy-qa.md:72,75,101`: at small-medium corpus scale, the model
  reading maintained index files beats embedding retrieval; embedding
  drift/chunking/retrieval-miss are the failure modes removed. Corpus
  consequence (already obeyed): this corpus's README index *is* the retrieval
  layer; do not build a vector index for ~25 entries.
- **DDL (daydreaming) loop** — `gwern-essays/ai-daydreaming.md` (loop stages
  :36–39; "~20:1 compute overhead" figure at :45): random
  concept pair → generator pass → critic filter → memory writeback.
  The critic-filter stage is an LLM-as-judge instance with
  the same RLHF-proxy caveat as any scalar judge (`eval-theory-notes.md`).
- **Turing test measures the apparatus, not the mind** — `ai/books/how-we-became-posthuman.md:35-43`:
  the observer is inside the circuit being measured. Soft warning for
  LLM-judged evals: the judge's framing shapes the result before scoring starts.
- **nanochat superseded nanoGPT** — `projects-and-tools/karpathy-projects.md:55`
  (Nov 2025, ~8k-line full-stack pipeline). Catalog fact: cite nanochat, not
  nanoGPT, as the current minimal full-stack reference.
- **LM Studio→Ollama workflow** — `projects-and-tools/local-first-ai-tools.md:67-71`:
  evaluate visually in LM Studio, deploy winner via Ollama. On this host the
  equivalent path is llama-server + direct API probes (`open-model-catalogs.md`).

## Skimmed, no durable rule extracted

`gpt-3-nonfiction.md` (beyond #1), `scaling-hypothesis.md` (capability gaps
are temporary → re-baseline each generation; `llms-txt.md`,
`willison-llm-cli.md`, `karpathy-deep-dive-llms.md`, `karpathy-intro-to-llms.md`
(context-window-as-RAM framing), `vibe-coding.md`, `builder-philosophy.md`,
`context-engineering.md` (tool-selection RAG 3× claim, LangChain — unverified
secondary), `knowledge-management-patterns.md` (Zettelkasten/PARA failure
modes are maintenance discipline, not eval), `thousand-brains.md`
(neuroscience theory, out of eval scope).

Sweep command used (for the "no durable rule" claim):
then `sed` reads on hits — run 2026-09-28 against the **25** files listed
above (corrected round 7: the count was written as 22; the enumeration
above contains 25 distinct wiki files).
