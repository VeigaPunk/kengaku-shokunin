# Prior-art pricing — round-12 LADDER claims C1 / C2 / C3 / C6

**Agent:** `ScoutPriorArtLadder` (scout, L2 prior-art). **Role:** price the round-12 ladder claims
against public literature, using fetched primaries only.
**Task restatement:** price C1 (ladder monotonicity), C2 (within-run replication of the r11 +0.352
severity dose), C3 (batching dissociation: up-front op batching vs emission sparsity) and C6
(dose-magnitude ordering) of `corpus/evidence/round12-ladder/probe_plan_r12.md` §1; one taxonomy
verdict each; strongest permitted wording per claim.

**Provenance discipline.** Zero requests to `http://127.0.0.1:34113` in this task (the served
endpoint was never contacted); no mock server was started. Every claim below rests on bytes fetched
in-session with a recorded HTTP status, or on a `file:line` in this repo. The search engine's
synthesis prose was used **only** to generate candidate URLs; any sentence I quote was re-extracted
from the fetched bytes. Method is all-stdlib: `curl` for fetches, a 20-line `re`/`html.unescape`
extractor for quotes (`PYTHONHASHSEED`-insensitive — no hash-ordered structure is used anywhere in
the analysis).

---

## 0. Census of this round's fetches

- **56 distinct URLs** fetched this session (`curl -L -A … -o <file> -w '%{http_code}'`), of which
  **53 returned 200**; **3 failures** recorded (§6): `acm.org` 403, `mdpi.com` 403,
  `arxiv.org/html/1909.06674v2` 404.
- **22 distinct sources are cited** in §2 (all fetched 200 this session); the rest were
  identification-only fetches (title checks) or verified non-counterexamples (§4).
- Auxiliary read-only APIs used: `export.arxiv.org/api/query`, `api2.openreview.net/notes/search`
  (`term=`), `api.github.com` (issue + comments), `raw.githubusercontent.com` (vLLM docs source).
- Repo reads: `corpus/evidence/round12-ladder/probe_plan_r12.md` §1, §2, §7, §8;
  `corpus/knowledge/eval-prior-art-calibration.md`;
  `corpus/evidence/round11-fleet/r11-prior-art-granularity.md`. r11's priced material is **not**
  re-litigated here; where r12's wording is **stronger** than r11's (C1: *monotone over four ordered
  arms* instead of a two-point dose; C2: *reproduces* instead of *measured once*) I re-checked with
  new fetches (§3).

---

## 1. The four claims as scoped by the plan (verbatim anchors)

Every sentence below carries the plan's §1 descriptor verbatim: *single served unit —
Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS under the stack pinned in the run's `descriptors` record
(q4_0 KV cache, `--kv-unified`, `--parallel 2`, custom non-upstream chat template); no cross-model
generalization.*

| # | Claim as scoped by `probe_plan_r12.md` §1 | Local anchor |
|---|---|---|
| **C1** | Per-problem error severity at the final forced emission **increases monotonically as forced-emission density falls** across four arms on the same problems — `A-INC`(10 checkpoints) → `A-CKPT4710`(3) → `A-CKPT710`(2) → `A-CKPT10`(1); graded by **Page's ordered-trend test** on within-problem ranks (n=64 blocks × 4 ordered arms), one confirmatory p | `probe_plan_r12.md:11-13`; E1 `probe_plan_r12.md` §2.3 |
| **C2** | The paired severity diff `A-CKPT710 − A-CKPT4710` at shared checkpoints {7,10} **reproduces r11's +0.352** on *identical problems and seeds* (pid 201–264, `gen_problem(3000+pid*41)`), within one later run | `probe_plan_r12.md:14-16`; E2, R2 |
| **C3** | r8's `A-MONO 0/10` collapse is driven by **up-front op batching**, not by emission sparsity — a one-checkpoint incremental arm (`A-CKPT10`, emission count = 1) should beat `A-MONO` (ten ops listed up front, emission count = 1) on final-state `nwrong` | `probe_plan_r12.md:17-19`; E4, R3 |
| **C6** | The **adjacent severity gaps are ordered by checkpoint count removed** — the INC→4710 gap (7 removed) and the 710→10 gap (1 removed) are both ≥0 and the ladder's **total spread exceeds each adjacent gap** | `probe_plan_r12.md:24-26`; E3, R1 |

---

## 2. Source ledger (every URL fetched this round, with status and the sentences that matter)

### 2.1 C1 — ordered dose in intermediate/intermediate-report quantity

| Source | Fetch | Venue + year | Sentence(s) that matter |
|---|---|---|---|
| **The Impact of Reasoning Step Length on Large Language Models** — Jin et al., arXiv 2401.04925 | `https://arxiv.org/abs/2401.04925` **200**; full text `https://arxiv.org/html/2401.04925v3` **200** | arXiv cs.CL, v3 20 Jan 2024 (§4.2 "Relationship Between Steps and Accuracy", §4.4 "Compressing Reasoning Steps") | "We design experiments that expand and compress the rationale reasoning steps within CoT demonstrations, while keeping all other factors constant." — "**For few-shot COT, there is a direct linear correlation between step count and accuracy.**" — "lengthening the reasoning steps in prompts considerably enhances LLMs' reasoning abilities across multiple datasets. **Alternatively, shortening reasoning steps, even while preserving key information, significantly diminishes the reasoning abilities of models.**" ⇒ a **monotone dose–response in the number of intermediate steps**, with the dose manipulated by adding/removing steps *of the demonstration*, response graded as accuracy. |
| **How Many Instructions Can LLMs Follow at Once? (IFScale)** — Jaroslawicz et al., arXiv 2507.11538 | `https://arxiv.org/abs/2507.11538` **200**; `https://arxiv.org/html/2507.11538v1` **200** | arXiv cs.AI, 15 Jul 2025 (§4.3 "Performance Analysis", §4.4 "Degradation Pattern Analysis") | "We introduce IFScale, a simple benchmark of 500 keyword-inclusion instructions for a business report writing task **to measure how instruction-following performance degrades as instruction density increases.**" — "we find that **even the best frontier models only achieve 68% accuracy at the max density of 500 instructions**." ⇒ density is a *published* independent variable and degradation is *quantified as a function of density*, but density = simultaneous **constraints in one prompt**, and the response is aggregate accuracy — no severity count, no emission schedule. |
| **BatchPrompt: Accomplish More with Less** — Lin et al., arXiv 2309.00384 | `https://arxiv.org/abs/2309.00384` **200**; `https://arxiv.org/html/2309.00384v3` **200** | arXiv cs.CL (ICLR'24 submission form), 2023/24 | "**Also, with the increase of batch size, the overall accuracy decreases.**" — "As prompting with batched **data inevitably stretches input length which decreases performance**, finding a better batch prompting strategy instead of naively batching data is necessary." ⇒ batching more items into one prompt is a published *monotone* accuracy-degrading dose. |
| **The Unreliable Progress Bar …** — Wang et al., arXiv 2609.08589 (r11 anchor, re-fetched to confirm status only) | `https://arxiv.org/abs/2609.08589` **200** | arXiv cs.SE, 8 Sep 2026; evaluated on τ²-bench + StageIF | "We evaluate this ability on the public benchmark $\tau^2$-bench and on StageIF, **a controlled testbed in which reporting checkpoints are placed across the task's lifecycle.** Both settings require reports at multiple task stages. We find that **reporting reliability depends on the stage a task has reached**, and that almost every deployed model we test is reliable at some stages and unreliable at others." ⇒ intermediate-report correctness is a *published* graded construct; the manipulated variable is report **position in the lifecycle**, not report **density** (r11 §2.4 already recorded the "frequency" attribution as a synthesis artefact and this re-fetch is consistent with that). |
| **Entity Tracking in Language Models** — Kim & Schuster, arXiv 2305.02363 (ACL 2023) | `https://arxiv.org/html/2305.02363v2` **200** | ACL 2023 (verbatim abstract, v2 HTML) | "we present a task probing to what extent a language model can infer **the final state of an entity given an English description of the initial state and a series of state-changing operations**." — "**While performance degrades for more complex splits**, we find that even when evaluated on a different set of entities from training or longer operation sequences, a finetuned model can perform non-trivial entity tracking." ⇒ the lane's probe *shape* (init + ops → final state) is a 2023 published construct; complexity is varied, **emission density is not**. |
| **Page's test for ordered alternatives** — method provenance | `https://en.wikipedia.org/wiki/Page%27s_trend_test` **200** | tertiary (encyclopedia), fetched only to pin the statistic's name/assumptions | "the Page test for multiple comparisons between ordered correlated variables … **It is also known as Page's trend test or Page's L test. It is a repeated measure trend test.**" (Assumptions quoted: ≥3 conditions, all subjects observed in each.) |
| **Centering: A Parametric Theory and Its Instantiations** — Poesio et al. | `https://aclanthology.org/J04-3003.pdf` **200** (PDF text extracted with `pdftotext`) | *Computational Linguistics* 30(3), 2004 (ACL journal) | "the tests we used are the sign test for Constraint 1 and Rule 1, and **the Page test for Rule 2 (Siegel and Castellan 1988)**." — "The **Page test for ordered alternatives** (Siegal and Castellan 1988, pages 184–188) indicates a chance of less than .001 that the four transitions are equally likely." ⇒ Page's ordered-trend test is **published inside the ACL family** (as the confirmatory test for an a-priori ordered hypothesis), four decades before this lane. |
| **SoK: Understanding (New) Security Issues Across AI4Code Use Cases** — Wu et al., arXiv 2512.18456 | `https://arxiv.org/abs/2512.18456` **200**; full text `https://arxiv.org/html/2512.18456v1` **200** | arXiv cs.CR (SoK), 20 Dec 2025 | "**T12. Longer functions improve vulnerability detection. Page's Trend Test (Page, 1963) shows statistically significant positive trends (p = 1.26 × 10⁻⁸ for C, p = 4.20 × 10⁻⁷ for C++).**" ⇒ a 2025 LLM-evaluation paper uses **Page's ordered-trend test as its confirmatory ordered-hypothesis statistic** — the instrument is live in LLM evaluation, not just in 2004 CL. |

### 2.2 C2 — repetition/self-replication, and what this server's draws are

| Source | Fetch | Venue + year | Sentence(s) that matter |
|---|---|---|---|
| **llama.cpp issue #7052** — "Non-deterministic output of the llama.cpp server when using multiple slots" | HTML `https://github.com/ggml-org/llama.cpp/issues/7052` **200**; REST `api.github.com/repos/ggml-org/llama.cpp/issues/7052` **200**; REST comments `…/issues/7052/comments` **200** | GitHub issue, opened 2024-05-03T01:06:01Z | **Reporter (body, verbatim):** "When running the script multiple times, I get **between 5 and 8 unique completion texts when using 8 slots**. If everything were completely deterministic, there should only be a single unique completion text in this case. When using a single slot, I always get the same answer, but still small variations in the logits." **Maintainer (JohannesGaessler, 2024-05-03T07:49:31Z):** "On the latest master **the results for multiple slots are still not 100% deterministic**. The problem mainly has to do with the use of > 1 slots … Generally speaking, floating point operations only return bit-for-bit identical results if the exact same operations are executed in the exact same way." **State, from the REST payload:** `state=closed`, `state_reason=completed`, `closed_at=2024-06-17T01:06:57Z`, `updated_at=2026-05-21T14:50:10Z`, `comments=6`, labels `bug-unconfirmed`, `stale`. The closing comment is the stale bot ("This issue was closed because it has been inactive for 14 days since being marked as stale."); the 2026-05-21T14:50:09Z comment is a user saying "this issue does exist, i just encountered it. **reopening**" — the API still reports `state=closed`. (Consistent with the round-10 note in `corpus/knowledge/eval-prior-art-calibration.md`: cite the *content*, never the open/closed state.) |
| **Defeating Nondeterminism in LLM Inference** — Thinking Machines Lab blog | `https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/` **200** | vendor engineering post, Horace He, 10 Sep 2025 | "However, **992 of the completions** go on to generate 'Queens, New York' whereas **8 of the completions** generate 'New York City'. On the other hand, **when we enable our batch-invariant kernels, all of our 1000 completions are identical.**" ⇒ run-to-run/host-state dependence of identical prompts on a *different* stack is published and quantified; the residual variance is a serving property, not a task property. |
| **vLLM docs — Reproducibility** (page + source markdown) | `https://docs.vllm.ai/en/latest/usage/reproducibility.html` **200** (JS-rendered MkDocs; no determinism text extractable — see §6); source `https://raw.githubusercontent.com/vllm-project/vllm/main/docs/usage/reproducibility.md` **200** | vLLM project docs (main branch, fetched 2026-09-28) | "**vLLM does not guarantee the reproducibility of the results by default, for the sake of performance.** To achieve reproducible results: In offline mode, you can either set `VLLM_ENABLE_V1_MULTIPROCESSING=0` which makes scheduling deterministic, or **enable batch invariance** … In online mode, you can only enable batch invariance." — "If a specific seed value is provided, the random states for `random`, `np.random`, and `torch.manual_seed` will be set accordingly." ⇒ a seeded, non-batch-invariant server is **documented** as not bit-reproducible; this is the engine-side analogue of the llama.cpp finding. |
| **Same Prompt, Different Outcomes: Evaluating the Reproducibility of Data Analysis by LLMs** — Cui & Alexander, arXiv 2602.14349 | `https://arxiv.org/abs/2602.14349` **200** | arXiv (stat/CS), 15 Feb 2026 | "We systematically evaluate the reproducibility of data analysis conducted by LLMs. We evaluate two prompting strategies, six models, and four temperature settings, **with ten independent executions per configuration, yielding 480 total attempts**. We assess the completion, concordance, validity, and consistency of each attempt." ⇒ same-prompt repetition studies exist publicly; the unit is *across* models/API configs, with 10 repeats per cell — not a same-run, same-seed, single-served-unit re-measurement. |
| **A Step Toward Quantifying Independently Reproducible Machine Learning Research** — Raff, arXiv 1909.06674 | `https://arxiv.org/abs/1909.06674` **200** (HTML v2 form **404**, §6) | arXiv cs.LG, 14 Sep 2019 (NeurIPS'19 Datasets & Benchmarks-track genre) | "What makes a paper independently reproducible? **Debates on reproducibility center around intuition or assumptions but lack empirical results.** Our field focuses on releasing code, which is important, but **is not sufficient for determining reproducibility.**" ⇒ the replication/reproduction *design class* is a published, quantitatively studied contribution; that class is defined by **third-party** implementation of **other** papers. |
| **Adding Error Bars to Evals** — Miller, arXiv 2411.00640 | `https://arxiv.org/abs/2411.00640` **200**; `https://arxiv.org/html/2411.00640v1` **200** | arXiv stat.AP, 1 Nov 2024 (Anthropic) | Section structure fetched verbatim: "2 Analysis framework … 4 Comparing models 4.1 Unpaired analysis **4.2 Paired analysis** **5 Power analysis** … A Clustered standard errors". ⇒ the *analysis kit* r12 uses (paired contrasts + power/sample-size contract) is published methodology for language-model evals. |
| **LLMs Get Lost In Multi-Turn Conversation** — Laban et al. (ICLR 2026 proceedings PDF; r9/r11 anchor re-fetched to pin **venue**) | `https://arxiv.org/abs/2505.06120` **200**; `https://proceedings.iclr.cc/paper_files/paper/2026/file/59f6421e64707225fdf5b28840679a07-Paper-Conference.pdf` **200** | **ICLR 2026** conference paper (header "Published as a conference paper at ICLR 2026") | "all the top open- and closed-weight LLMs we test exhibit significantly lower performance in multi-turn conversations than single-turn, **with an average drop of 39% across six generation tasks**. Analysis of 200,000+ simulated conversations **decomposes the performance degradation into two components: a minor loss in aptitude and a significant increase in unreliability**." ⇒ repeated-turn delivery is a published reliability-degrading factor; the paper's own aptitude/unreliability decomposition is the nearest published *decomposition* idiom to C2's replication question. |

### 2.3 C3 — batching vs sparsity (the dissociation)

| Source | Fetch | Venue + year | Sentence(s) that matter |
|---|---|---|---|
| **Efficient but Vulnerable: Benchmarking and Defending LLM Batch Prompting Attack** — Yue & Yao | `https://aclanthology.org/2025.findings-acl.245/` **200**; PDF `…245.pdf` **200** | Findings of ACL 2025 | "**Batch prompting, which combines a batch of multiple queries sharing the same context in one inference, has emerged as a promising solution to reduce inference costs.** … malicious users can inject attack instructions into a batch, leading to **unwanted interference across all queries**, which can result in the inclusion of harmful content … **or the disruption of logical reasoning.**" ⇒ cross-instance interference inside one packed prompt is published; the manipulated variable is batching *of independent instances*, with no emission-schedule arm. |
| **BatchPrompt** (arXiv 2309.00384, §2.1) | **200** ×2 | arXiv, 2023/24 | batch size ↑ ⇒ accuracy ↓ (verbatim in §2.1). |
| **IFScale** (arXiv 2507.11538, §2.1) | **200** ×2 | arXiv, Jul 2025 | instruction density ↑ ⇒ adherence ↓ (verbatim in §2.1). |
| **LLMs Get Lost In Multi-Turn Conversation** (2505.06120 + ICLR 2026 PDF, §2.2) | **200** ×2 | ICLR 2026 | The *sharding* contrast: identical information split across turns performs far worse than when it is supplied together; degradation is attributed to lost-aptitude + unreliability, **not** to emission count. Polarity relative to C3's prediction: in Laban, **merging** the content into one message *helps*; in C3's predicted direction, **merging the ops** into one message (`A-MONO`) *hurts*. |
| **Multi-IF** — He et al., arXiv 2410.15553 | `https://arxiv.org/abs/2410.15553` **200**; `https://arxiv.org/html/2410.15553v1` **200** | arXiv cs.CL, 21 Oct 2024 (Meta GenAI) | "**All the models tested showed a higher rate of failure in executing instructions correctly with each additional turn.** For example, **o1-preview drops from 0.877 at the first turn to 0.707 at the third turn** in terms of average accuracy over all languages." ⇒ turn-count dose is published — but as a **multi-turn** effect with per-turn emissions; it is not a batching-vs-sparsity decomposition. |
| **Beyond Final Scores: A Systematic Evaluation of Agents for Long-Horizon AI Research and Development** — arXiv 2608.13417 | `https://arxiv.org/abs/2608.13417` **200**; `https://arxiv.org/html/2608.13417v1` **200** | arXiv cs.AI, 13 Aug 2026 | "we present a systematic evaluation … based on a new framework that uses **rule-based metrics to characterize within-run behavior through Solution Framing, Execution, and Feedback Control** … For each capability, we design a rule-based metric computed **deterministically from verifier outcomes and recorded trajectory signals rather than LLM judgments**." ⇒ within-run, deterministic, non-LLM-judge instrumentation is published; the ablation is of *capabilities*, not of emission/batching schedule. |

### 2.4 C6 — magnitude ordering of adjacent dose gaps

| Source | Fetch | Venue + year | Sentence(s) that matter |
|---|---|---|---|
| **The Impact of Reasoning Step Length…** (2401.04925, §2.1) | **200** ×2 | arXiv, Jan 2024 | §4.4 is titled "**Compressing Reasoning Steps**"; the paper's RO3 is "**Will compressing reasoning steps in few-shot demonstrations hurt LLM performance?**" and its findings state that shortening steps "significantly diminishes" ability while lengthening enhances it. ⇒ removing intermediate steps is a **monotone** severity dose with an explicit *direction* per removed step. |
| **Scaling LLM Test-Time Compute Optimally…** — Snell et al., arXiv 2408.03314 | `https://arxiv.org/abs/2408.03314` **200** | arXiv cs.LG, 2024 | "We find that **in both cases, the effectiveness of different approaches to scaling test-time compute critically varies depending on the difficulty of the prompt.** This observation motivates applying a '**compute-optimal**' scaling strategy, which acts to most effectively allocate test-time compute adaptively per prompt." ⇒ more compute does **not** buy uniform increments; dose-response *magnitude* is explicitly heterogeneous in published scaling work. |
| **The Art of Scaling Test-Time Compute for LLMs** — Agarwal et al., arXiv 2512.02008 | `https://arxiv.org/abs/2512.02008` **200** | arXiv cs.CL, 1 Dec 2025 | "Test-time scaling (TTS) — the dynamic allocation of compute during inference — is a promising direction … However, **a systematic comparison of well-known TTS strategies …**" ⇒ the 2025 state of the art on dose-response *shape* comparisons for inference-time budget. |
| **Test-Time Scaling of Reasoning Models for Machine Translation** — Li et al., arXiv 2510.06471 | `https://arxiv.org/pdf/2510.06471` **200** (PDF, first page extracted) | arXiv cs.CL, v2 11 Jan 2026 | "Test-time scaling (TTS) has enhanced the performance of Reasoning Models (RMs) on various tasks such as math and coding …" ⇒ a *non-ledger* task family (MT) is publicly used for TTS dose-response — relevant to C6's "second task family" framing, though graded as translation quality, not key-count severity. |
| **IFScale** (2507.11538, §2.1) | **200** ×2 | arXiv, Jul 2025 | Its §4.4 "Degradation Pattern Analysis" is reported as **three distinct degradation patterns** (later reported as threshold/linear/exponential in the paper's own analysis) — i.e. the *shape* of the density response differs by model class, which is the published precedent for expecting non-equal adjacent gaps. |

---

## 3. Verdicts and permitted wording (one taxonomy verdict per claim)

### C1 — **INCREMENTAL** *(low; unchanged in kind from r11, strengthened by the ordered test)*

**Why.** The *ingredients* are published: a monotone dose in the number of intermediate steps with
an accuracy response (2401.04925, verbatim "direct linear correlation between step count and
accuracy"), density-manipulated degradation with a quantified curve (IFScale 2507.11538), the
decoupling of aggregate success from intermediate-report correctness (2609.08589), the lane's
probe shape (2305.02363) and the ordered-trend *instrument* itself, both inside the ACL family
(Poesio et al., CL 2004) and in a 2025 LLM-era SoK (2512.18456, p = 1.26 × 10⁻⁸). What was **not
found** in any fetched source: a monotone dose in **forced full-state emission density** on
identical problems, with the response graded as **error severity (count of wrong state entries)**
rather than accuracy, and priced with a single confirmatory ordered-trend p over four ordered arms.

**Strongest defensible sentence this lane may write.**
> On one served sub-3-bit unit (Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS; q4_0 KV; `--kv-unified`;
> custom chat template) and one inventory-ledger problem set, final-turn error severity increased
> monotonically as forced full-state emissions were removed from a ten-turn ladder
> (10 → 3 → 2 → 1 checkpoints; Page's ordered-trend test, n = 64 blocks, p = …). The dose variables
> (intermediate-step count, instruction/instance density) and their monotone effects are published;
> what is new here is the *emission-density* parameter and the severity (wrong-entry count) endpoint.

**Sentence this lane may NOT write.**
> ~~"Checkpoint density causally drives state-tracking error severity in LLMs"~~ — forbidden: it
> generalizes off the served unit, and it converts an ordered association within one
> preregistered run into a mechanism claim. Also forbidden: ~~"the first demonstration that reducing
> intermediate reporting degrades performance"~~ (2401.04925, 2507.11538 and 2309.00384 all report
> monotone degradation under a reduced-supply manipulation).

### C2 — **INCREMENTAL** *(self-replication design class published; the within-run / same-seed / single-unit instantiation and its point prediction are the added parameters)*

**Why.** Repetition-and-replication as a studied design is published (Raff 1909.06674: independent
reproduction of *other* authors' 255 papers; 2602.14349: 480 repeated executions across models and
temperatures; Miller 2411.00640: paired analysis + power). The *serving* premise is published and
sharp for this stack class: llama.cpp #7052 (multi-slot: "between 5 and 8 unique completion texts
when using 8 slots"; maintainer: "results for multiple slots are still not 100% deterministic"),
plus the same phenomenon quantified off-stack by Thinking Machines (992 vs 8 of 1000 completions
diverge; 1000/1000 identical with batch-invariant kernels) and documented by vLLM ("does not
guarantee the reproducibility of the results by default"). **Not found:** a preregistered
*self*-re-measurement of one's own published effect, within one run, on byte-identical problems and
seeds, with the effect size and the point value filed before the requests — i.e. the *replication
of a prior local effect on the same unit* is the added parameter.

**Interpretation constraint from #7052 (bears directly on C2).** The issue's `state` is `closed`
with `state_reason=completed` (stale-bot close 2024-06-17), updated 2026-05-21 by a user comment
claiming a reopen; the *content* is unaffected and never cites the state. Because draws on a server
of this family are documented as not independent across slots/composition, **a within-run
same-seed re-measurement is a repeated measure, not an independent replication**: R2's branch text
must not be read as "the effect survived a second experiment".

**Strongest defensible sentence this lane may write.**
> The r11 checkpoint-sparsity severity dose was re-measured in a later run on the *same* problems
> and seeds and on the *same* served unit: paired diff (710 − 4710) = …, p = …, sign test agrees
> (E2/R2 verdict …), and this repeated measure reproduces r11's point value to within …. Because
> draws from a server of this family are documented as not fully deterministic across slot
> composition (llama.cpp #7052; Thinking Machines; vLLM docs), this is a within-run repeatability
> check on one stack, not an independent replication.

**Sentence this lane may NOT write.**
> ~~"We independently replicated (or: reproduced) the emission-granularity effect"~~ — forbidden:
> the design shares problems, seeds, unit and run-day lineage, and the served stack is publicly
> documented as non-iid across slot composition. Also forbidden: any claim that the effect is
> robust across models, quantizations, host states, or run days, and any wording that cites #7052's
> open/closed state rather than its content.

### C3 — **NOVEL-instrument** *(no named suite and no fetched paper decomposes a monolithic collapse into up-front op batching vs emission sparsity with the emission count held at 1; the candidate phenomenon's direction is `INCREMENTAL`-adjacent)*

**Why.** Two published contrasts touch each axis separately but never cross them:
`A-MONO − A-CKPT10` holds emission count constant (both arms emit exactly one final state) and
varies whether the ten ops are delivered up front or one per turn. The nearest published items are
(a) batching *density* effects — BatchPrompt batch-size ↑ ⇒ accuracy ↓ (2309.00384),
IFScale density ↑ ⇒ adherence ↓ (2507.11538), BatchPrompt-attack cross-instance interference
(2025.findings-acl.245); and (b) delivery-pattern effects — Laban's merged-vs-sharded multi-turn
contrast (ICLR 2026), whose polarity is the *opposite* of C3's prediction, and which varies turn
count rather than emission count. No fetched source holds emission frequency fixed while varying op
batching, and no named suite reports this decomposition. If E4 fires in the "batching hurts"
direction, the *direction* is a replication-of-neighbouring-evidence; the **dissociation** is what
is new.

**Strongest defensible sentence this lane may write.**
> In a two-arm decomposition that holds forced-emission count at one, final-state error severity was
> higher in the monolithic arm (all ten ops up front) than in the one-op-per-turn arm by … (paired t,
> p = …; sign W/L/T = …), i.e. on this served unit and problem set r8's `A-MONO` collapse is
> attributable to the up-front batching of operations rather than to emission sparsity. Density- and
> batching-induced degradation are published (BatchPrompt; IFScale; Laban et al. ICLR 2026); the
> *dissociation between op batching and emission sparse* is not.

**Sentence this lane may NOT write.**
> ~~"batching instructions is the general cause of state-tracking failure in LLMs"~~ (off-unit,
> mechanism-generalizing), and ~~"we show that merged single-message delivery is worse than
> turn-by-turn delivery"~~ as a general claim — Laban et al. (ICLR 2026) report the opposite
> ordering for merged-vs-sharded *content* delivery, so the lane must localize the result and note
> the tension explicitly rather than assert a general law.

### C6 — **INCREMENTAL** *(dose-magnitude ordering is published for removed reasoning steps and for compute budgets; ordering by *emission checkpoint count*, and the "total spread exceeds each adjacent gap" inequality, are the added parameters)*

**Why.** Monotone magnitude with removed intermediate steps is published (2401.04925 §4.4
"Compressing Reasoning Steps"; "shortening reasoning steps, even while preserving key information,
significantly diminishes the reasoning abilities of models"), and non-uniform adjacent increments
under a scaled budget are published (2408.03314: effectiveness "critically varies depending on the
difficulty of the prompt"; IFScale's three degradation patterns; 2512.02008's strategy comparison).
**Not found:** any source that (i) orders adjacent severity gaps by the number of *emission
checkpoints removed*, or (ii) asserts the ladder-level inequality *total spread > each adjacent
gap* — an additive-consistency claim about gaps that the fetched scaling literature actively
argues against assuming (non-uniform compute-optimal allocation).

**Strongest defensible sentence this lane may write.**
> Both adjacent severity gaps in the four-arm ladder were positive at their shared turns and the
> total INC→CKPT10 spread exceeded each adjacent gap (E3: …; global Page test E1: …); this ordered
> magnitude pattern is consistent with the published step-count dose-response (2401.04925) while
> ordering effect magnitude by *emission checkpoint count* — and the additivity-style inequality
> reported here — have no fetched published counterpart.

**Sentence this lane may NOT write.**
> ~~"severity scales linearly (or additively) in the number of checkpoints removed"~~ — forbidden:
> E3 tests ordering (≥0 gaps, total > adjacent), not linearity; and the published budget-scaling
> literature (2408.03314, 2512.02008) reports non-uniform increments. Also forbidden: framing the
> ordering as a law across task families (C4's transport is a separate, unpriced-here claim).

---

## 4. Negative-search log (required for the NOVEL verdict)

**C3 (the only NOVEL-* verdict here).** Negative claim: *no named suite or paper separates up-front
op batching from emission sparsity while holding emission frequency fixed.* Queries issued that
returned no such artifact (all verbatim in §5): #3, #7, #13, #18, #23 (batching/packing/density);
#1, #8, #15, #16 (emission/checkpoint schedule); #25 (severity-vs-pass-rate dissociation). And the
targeted greps that came back empty on fetched full texts:

- `frequency|granularity|density|severity|pass rate` in `https://arxiv.org/html/2511.10457v1`
  (*Exploring State Tracking Capabilities of Large Language Models*, r11's instrument-nearest
  neighbour): re-fetched this round **HTTP 200, 418 499 bytes**, **0 hits for each of the five
  terms** — matching r11 §2.3.
- `Page's Trend`, `Page, 1963`, `T1…T6` in `https://arxiv.org/html/2605.19743v1` (*EngiAI: A
  Multi-Agent Framework and Benchmark Suite for LLM-Driven Engineering Design*; **HTTP 200**,
  787 479 bytes): **0 hits each**. The search engine had attributed a "Page's test on T1–T6
  complexity tiers" claim to this paper; the fetched bytes do not support it ⇒ **synthesis
  artefact**, recorded so it is not re-imported (r11 §2.4 style).
- `checkpoint density|reporting frequency|emission frequency` across the 22 cited sources ⇒ the
  only "density" hits are *instruction/instance* density (2507.11538, 2309.00384) and *function
  length* (2512.18456); none is emission density.

**C1/C2/C6** are **not** NOVEL-*, so no negative-search certificate is owed; the "not found"
statements in §3 are scoped to the cited corpus and are absence-of-evidence at **medium**
confidence (search-based retrieval only; no Semantic Scholar bulk sweep — the API answered
**HTTP 429** on the one attempt, §6; no exhaustive OpenReview sweep, whose `notes/search?term=`
endpoint returned review records rather than papers).

---

## 5. Query log (verbatim; 24 distinct web-search queries + 6 arXiv API + 4 OpenReview term queries = 34)

Web search (engine: the session's `web_search`; used for discovery only):

1. `"show your work" forced intermediate output dose-response LLM accuracy ablation`
2. `"Page's test" ordered trend test natural language processing evaluation multiple systems`
3. `batched prompting single prompt multiple instances versus sequential LLM accuracy comparison`
4. `replication study LLM evaluation same lab reproduces own published effect rerun`
5. `multi-turn instruction following benchmark performance decay over turns LLM`
6. `"Page's trend test" information retrieval evaluation Sakai significance testing ordered alternatives`
7. `decomposed prompting modular versus monolithic single prompt comparison LLM`
8. `impact of reasoning step length on large language models accuracy increasing steps`
9. `conversation state tracking benchmark degradation needle in a haystack multi-turn long context`
10. `"replication" study of the authors' own prior result machine learning internal replication LLM benchmark rerun same seed`
11. `"Page's test" OR "Jonckheere-Terpstra" used in machine translation evaluation OR LLM benchmark trending monotonic order paper`
12. `vLLM reproducibility determinism batch invariance documentation sampling temperature nondeterminism`
13. `"how many instructions" LLM follow at once IFScale instruction density degradation number of instructions`
14. `"Page's test" OR "Page test" statistical significance information retrieval TREC evaluation ordered hypothesis paper ijcnlp`
15. `removing reasoning steps degrades LLM accuracy monotone number of steps removed ablation scratchpad`
16. `agent long-horizon evaluation checkpoints every N steps versus only final answer forced intermediate state emission ablation`
17. `site:aclanthology.org "Page's test" OR "Page test" ordered alternatives trend`
18. `state tracking operations given all at once versus one at a time LLM entity tracking sequential updates versus batched`
19. `"trend test" monotonic scaling hypothesis test language model evaluation arxiv "Page's L" OR "Jonckheere" 2025 2026`
20. `reproducibility study large language model benchmark results rerun same prompts different results meta-evaluation reliability`
21. `"we replicate our own" OR "internal replication" OR "self-replication" authors rerun their published experiment machine learning LLM evaluation paper`
22. `"page_trend_test" OR "Page's trend test" applied large language model benchmark scores ordered hypothesis 2024 2025 paper`
23. `single prompt all operations at once versus one operation per turn state tracking LLM which is harder ablation`
24. `"error severity" OR "number of wrong" graded metric increases with prompt manipulation identical questions pass rate unchanged study`
25. `state tracking operations given all at once versus one at a time LLM entity tracking sequential updates versus batched` (derived re-issue, retained for the count)

arXiv API (`export.arxiv.org/api/query`, 200 each): `all:"emission granularity"` (0 hits);
`all:"checkpoint density" AND all:"language model"` (0 hits); `abs:"forced intermediate"` (3 hits,
all physics/materials); `abs:"monolithic" AND abs:"incremental" AND abs:"prompting"` (1 hit,
class-incremental learning); `all:"Page test" AND all:"ordered"` (**0 hits**); `all:"Jonckheere-Terpstra" AND all:"NLP"` (**0 hits**).

OpenReview (`api2.openreview.net/notes/search?term=`): `emission granularity`;
`checkpoint frequency language model`; `ordered trend test evaluation`;
`replication large language model evaluation` — all **200**, all returning review/edit notes for
submissions whose titles are `None` in the API payload, i.e. **no usable paper-level result**;
recorded as a dead end, not as evidence.

---

## 6. Failures and non-citations (nothing fetched is cited as read unless it was read)

| URL | Result | Handling |
|---|---|---|
| `https://www.acm.org/publications/policies/artifact-review-and-badging-current` | **403** | Not cited. The ACM repeatability/reproducibility/replication taxonomy would have been the natural definitional cite for C2; without a fetch, §3 C2 rests on Raff 1909.06674 + the fetched serving docs instead. |
| `https://www.mdpi.com/2674-113X/4/3/17` | **403** | Not cited (surfaced by the reproducibility query; not needed). |
| `https://arxiv.org/html/1909.06674v2` | **404** | The *abs* page (`/abs/1909.06674`, 200) is the cited evidence; the HTML version does not exist at that path. |
| `https://docs.vllm.ai/en/latest/usage/reproducibility.html` | **200** but JS-rendered | Fetch succeeded, text not extractable (MkDocs SPA shell); the *cited* vLLM bytes are the project's own source markdown (`raw.githubusercontent.com/vllm-project/vllm/main/docs/usage/reproducibility.md`, **200**), quoted in §2.2. |
| `https://api.semanticscholar.org/graph/v1/paper/search?query=emission granularity LLM…` | **429** | No result usable; negative-search confidence is bounded accordingly (§4). |
| `https://openreview.net/forum?id=PV5xSw4n6y` | **200**, 4.8 kB JS shell | No content; not cited. |
| Attribution checks that **failed** (recorded so they are not re-imported) | — | (i) "arXiv 2605.19743 uses Page's test on T1–T6 tiers" → fetched HTML contains no Page/T1–T6 text. (ii) "arXiv 2607.20473 studies graded error severity" → it is *Incomplete Prompt Jailbreaks*; no severity-of-state metric. (iii) "arXiv 2401.04925 reports *removing* demonstration steps from a fixed prompt" vs *expanding/compressing the demonstrations* — the verbatim text supports the latter framing only; the C6 wording above follows the verbatim text. |

---

## 7. Closing table

| claim | verdict | n_sources_fetched | strongest permitted wording |
|---|---|---|---|
| **C1** ladder monotonicity (severity ↑ as forced-emission density ↓, 4 ordered arms, Page's test) | **INCREMENTAL** | 8 | "On one served sub-3-bit unit and one ledger problem set, final-turn error severity increased monotonically as forced full-state emissions were removed (10→3→2→1; Page's ordered-trend p = …). The monotone dose in intermediate-step/instruction density is published; the *emission-density* parameter and the *severity* endpoint are new here." |
| **C2** within-run replication of the r11 dose on identical problems/seeds | **INCREMENTAL** | 7 | "A later run on the same problems, seeds and served unit re-measured the r11 checkpoint-sparsity severity dose (paired diff …, R2 = …), reproducing r11's point value within …. Draws on this server family are documented as not fully deterministic across slot composition (llama.cpp #7052; Thinking Machines; vLLM docs), so this is within-run repeatability on one stack, not an independent replication." |
| **C3** batching dissociation (MONO collapse = op batching, not emission sparsity) | **NOVEL-instrument** (negative search §4) | 7 | "In a two-arm decomposition holding forced-emission count at one, the monolithic all-ops-up-front arm was worse than the one-op-per-turn arm by … (p = …), so on this unit and problem set r8's MONO collapse is attributable to up-front op batching rather than emission sparsity. Density/batching degradation is published (BatchPrompt; IFScale; Laban ICLR 2026); the *dissociation* is not." |
| **C6** dose-magnitude ordering (adjacent gaps ≥ 0, total spread > each adjacent gap) | **INCREMENTAL** | 5 | "Both adjacent severity gaps were positive and the total INC→CKPT10 spread exceeded each adjacent gap (E3 …; E1 …), consistent with the published step-count dose-response; ordering effect magnitude by *emission checkpoint count*, and the additive-style spread inequality, have no fetched published counterpart." |

---

## 8. Confidence lines and limits

| Item | Grade | Reason |
|---|---|---|
| C1's *instrument* status (ordered-trend test on an emission-density ladder) | **medium–high** | Positive: Page's ordered-trend test is published inside the ACL family (CL 2004) and used as a confirmatory statistic in a 2025 LLM-era SoK with reported p-values (2512.18456). Negative: no fetched source ablates *emission density* with a severity endpoint. |
| C1/C6's *phenomenon* neighbourhood | **medium–high** | Verbatim monotone dose-responses fetched (2401.04925 "direct linear correlation between step count and accuracy"; IFScale density⇒68% at 500; BatchPrompt batch-size⇒accuracy↓), all on *other* dose variables. |
| C2's serving premise (non-iid / non-bit-reproducible draws) | **high** | Three independent fetched sources (llama.cpp #7052 body + maintainer comment via REST; Thinking Machines 992/1000 divergence; vLLM's own docs "does not guarantee the reproducibility"). Issue *state* deliberately not relied on. |
| C3 = **NOVEL-instrument** | **medium** | Search-based negative over 24 distinct web queries (25 issued) + 6 arXiv API queries + targeted full-text greps; no Semantic Scholar sweep (429) and no arXiv full-text index ⇒ absence of evidence, not verified absence. |
| C6 = **INCREMENTAL** | **medium** | The nearby dose-magnitude literature is fetched and quoted; the negative half ("ordered by *checkpoint* count"; "total > each adjacent gap") is a search-based negative of the same class. |
| All findings remain **single-unit, sub-3-bit serving-stack observations** | **medium–high** | The plan's descriptor pins Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS, q4_0 KV, `--kv-unified`, `--parallel 2`, custom chat template; no fetched source licenses any cross-model reading. |
| Every quoted sentence came from bytes fetched **this round** with a recorded status | **high** | §2 + §6: statuses are per-fetch; three synthesis-engine attributions failed text verification and are recorded as artefacts. |

**Blocking issues:** none. No fetched source contradicts a preregistered r12 claim; the effect on
landing is **framing only** — C1/C2/C6 must be written as *incremental* (parameter/endpoint
additions, plus a published design class), C3 as an *instrument-level* dissociation, and **no**
r12 claim may be written as a first-of-kind demonstration of intermediate-emission effects.