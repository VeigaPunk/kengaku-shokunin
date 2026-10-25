# r12 prior-art pricing — TRANSPORT (C4) and PER-PROBLEM FORECASTS (C5)

**Agent:** `ScoutPriorArtTransport` — scout (L2 / subagent), round 12.
**Task restated:** price `probe_plan_r12.md` claim **C4** (transport of the dense-vs-sparse
emission-density severity dose to a second, structurally different task family) and claim **C5**
(per-problem probabilistic forecasts of the run's own pass outcomes, scored by Brier + Brier skill
score + calibration slope + reliability bins) against public prior art, without double-counting
round 11's verdicts.

---

## 0. Method, scope, and contract compliance

**Scope of the priced claims (verbatim from the design of record):**

| # | Claim (as filed) | Local anchor |
|---|---|---|
| **C4** | **Transport**: the dense-vs-sparse severity dose transports to a structurally different task family (positional token-sequence editing: no integer arithmetic, no key set, order-carrying state) — paired diff `T-SPARSE − T-DENSE` at shared checkpoints {7,10}, n=48 | `corpus/evidence/round12-ladder/probe_plan_r12.md:23`; endpoint E5 at `:119`; verdict rule R4 at `:143-145`; scale caveat at `:334-337` |
| **C5** | **Per-problem forecast skill**: a mechanical predictor fitted on r11's committed per-problem bytes forecasts r12 pass outcomes better than arm-level climatology — Brier over 448 pass events (7 arms), Brier skill score, calibration slope/intercept, 5-bin reliability | `probe_plan_r12.md:24`; endpoint E6 at `:120`; verdict rule R5 at `:146-148`; forecast-informativeness threat at `:338-340` |

**C4/C5 as *scoped* for pricing (this matters — see §3.1/§4.1):**

- C4 is **not** a claim that "density ladders are novel"; it is a claim that a *specific paired
  severity contrast* (one forced-emission checkpoint removed, `T-DENSE` {4,7,10} → `T-SPARSE` {7,10})
  reproduces on a **second task family** under the *same* served unit and pinned seeds
  (`probe_plan_r12.md:23`, `:334-337`). The transport target is a state whose **state type** differs
  (ordered token list vs key→integer map), not a different model, prompt style, or scoring pipeline.
- C5 is **not** a claim about *model* confidence calibration (that sense is explicitly out of scope
  for this pricing, per the task brief). It is a claim about the **experimenter's** per-problem
  probabilistic forecast of *its own run's* pass outcomes, scored with forecast-verification
  instruments, against an **in-sample arm-climatology** reference (`probe_plan_r12.md:120`,
  `:338-340`: "the C5 predictor uses r11 outcomes on the same problems, so its skill is *persistence*
  skill, not cold forecasting; family-2 forecasts are constant per arm by design (a no-information
  comparator)").

**Contract compliance (round-12 hard rules):**

- **Zero requests** were issued to `http://127.0.0.1:34113` (no `/v1/models`, no `/health`, no
  `/v1/chat/completions`) and no mock server was started (the 127.0.0.1:18114 rule is therefore not
  exercised; no INTERCEPT logging applies). Every fetch below is a public HTTPS GET.
- This artifact is the **only** file written. No SSOT file (`probe_plan_r12.md`, `SCORECARD.md`,
  `LOG.md`, `PROVINCE.md`, `SHONEN.md`, `corpus/README.md`, `grader.py`, any `round8/9/10/11-*`)
  was touched. No mutating git command was run.
- Quoting convention: load-bearing sentences are reproduced from the **fetched bytes** with HTML tags
  stripped and whitespace collapsed (`re.sub(r'\s+',' ',…)` after tag removal). Stripping inserts no
  characters, but the collapse can leave a space before punctuation in HTML-derived text (e.g.
  `Full , Concat , and Sharded .`); the *words* are verbatim. PDF sources were read with
  `pdftotext -layout`.
- Statuses: every row in §2 was fetched **twice** — once as a full GET (recorded `200`) and once in a
  Range-header re-probe (recorded `206', which is partial content, not an error). The table below
  reports the full-GET status. Six fetched URLs failed and are recorded verbatim in §7; **nothing
  unfetched is cited as read anywhere in this file.**
- Determinism: all fetches are public HTTP; no `PYTHONHASHSEED`-sensitive computation is reported.
  No number in this file is computed from a non-committed path; the status table re-derives from the
  command in §8.

**Search discipline (why the verdicts are stated as floors):** search-engine *synthesis* text was used
only to *find* URLs, never as evidence. Three synthesis-claimed artifacts failed verification on
fetch and are therefore **excluded**: an asserted `BetterBench = arXiv 2305.14318` (that ID is
*CREATOR*; BetterBench is `2411.12990`, S19), an asserted `PredictaBoard` framing attributed to
`2507.08038` (that ID is *AblationBench*; PredictaBoard is the ACL Findings paper at S40), and an
asserted `StringBench/ComplexBench = arXiv 2410.01208` (that ID is *StringLLM/StringBench*, S15; it
is ***not*** ComplexBench).

---

## 1. Query log (verbatim, every `web_search` query issued this task, allocated by hunt)

### 1.1 C4 — transport / cross-task-family generality (15 queries)

1. `multi-turn degradation LLM benchmark multiple task families state tracking "tracking shuffled objects" "temporal sequences"`
2. `benchmark LLM sequence editing list operations insert delete move benchmark "list functions"`
3. `"LLMs Get Lost in Multi-Turn Conversation" arXiv 2505.06120 benchmark domains`
4. `string manipulation instruction following benchmark LLM string editing suite`
5. `chain-of-thought prompting elicits reasoning task families arithmetic commonsense symbolic same intervention transferred`
6. `"benchmark lottery" arXiv 2107.07002 ranking depends on benchmark choice generalization`
7. `benchmark LLM "sequence manipulation" tokens insert delete swap reverse order tracking evaluation suite arXiv`
8. `IFScale "How Many Instructions Can LLMs Follow at Once" instruction density 500 instructions benchmark 2507.11538`
9. `ablation "checkpoint" OR "intermediate state emission" frequency across two task families state tracking severity count benchmark suite`
10. `evaluation intervention effect generalizes across task families "does not transfer" benchmark state tracking same manipulation two domains LLM`
11. `state tracking benchmark LLM two task families key-value map versus ordered list positional editing severity`
12. `"benchmark-specificity" OR "benchmark specificity" evaluation effect does not generalize across benchmarks LLM construct`
13. `Turing "list functions" benchmark LLM apply sequence of list operations to final list BIG-bench free response`
14. `long-context benchmark suite same length manipulation across multiple task types RULER 13 tasks synthetic`
15. `"intermediate output" OR "scratchpad emission" frequency ablation two task families LLM evaluation severity wrong items`

### 1.2 C5 — per-problem probabilistic forecasts of eval outcomes (15 queries)

1. `prediction market forecasting replication outcomes scored Brier score "per-study" predictions Dreber Gordon`
2. `Metaculus Epoch AI forecasting platform probabilistic forecasts of AI benchmark results questions`
3. `"calibration slope" slope intercept logistic recalibration risk model "calibration hierarchy" Van Calster`
4. `Murphy 1973 "A New Vector Partition of the Probability Score" reliability resolution decomposition`
5. `"Brier skill score" reference forecast climatology persistence baseline definition evaluation of probabilistic predictions`
6. `preregistered "per-item" probabilistic predictions researchers forecast their own experiment outcomes Brier score machine learning evaluation`
7. `"Forecasting Research Institute" AI Frontiers forecasting report probabilistic forecasts AI milestones 2025 score`
8. `authors predict their own study results accuracy elicitation forecasting "expected results" preregistration scored Brier calibration psychology`
9. `LLM evaluation paper preregistered predictions "Brier score" predicted benchmark outcomes forecast own experiment 2026`
10. `"item-level" OR "per-item" probabilistic forecasts of an LLM evaluation's own outcomes preregistered Brier calibration slope experimenter predictions benchmark`
11. `"calibration slope" reported evaluation predictions machine learning forecast skill "Brier skill score" paper`
12. `"Precog" forecasting machine learning experiment outcomes benchmark performance prediction arXiv 2507.04562`
13. `tinyBenchmarks item response theory predicting LLM performance on individual benchmark items per-item prediction`
14. `Epoch AI "benchmarking hub" OR "AI benchmarking dashboard" forecasting model performance timeline predictions`
15. `Metaculus Epoch AI forecasting tournament`

Queries 1–3, 5–6, 8, 11–14 of §1.1 also surfaced C5-adjacent items (density instruments, prediction
platforms) and are cross-used where the register says so; no query is counted twice for the
"distinct verbatim" requirement of its own section.

---

## 2. Source register (every source fetched this session; URL + full-GET status + venue/year)

### 2.1 C4 — transport, task-family generality, sequence-editing suites, construct validity

| ID | URL(s) | HTTP | Venue / year | Load-bearing sentence(s) (verbatim from fetched bytes) |
|---|---|---|---|---|
| **S1** | `https://arxiv.org/abs/2505.06120`; `https://arxiv.org/html/2505.06120v1` | 200; 200 | Laban, Murakhovs'ka, Wu, Chen, Liu, Xiong — arXiv 2505.06120 (cs.CL), 2025-05-09 (icml'25 / preprint lineage of r9's "lost in conversation" anchor) | abs: *"Our experiments confirm that all the top open- and closed-weight LLMs we test exhibit significantly lower performance in multi-turn conversations than single-turn, with an average drop of 39% across six generation tasks."* html §5: *"We constructed sharded instructions for six tasks that we use in a large-scale simulation experiment."* and *"we leveraged the totality of instructions we sharded across six tasks (a total of 600 instructions), and simulated conversations across three types: Full , Concat , and Sharded ."* |
| **S2** | `https://arxiv.org/abs/2410.15553`; `https://arxiv.org/html/2410.15553v2` | 200; 200 | Multi-IF — arXiv 2410.15553, 2024-10-21 (rev.) | abs: *"To address this gap, we introduce Multi-IF, a new benchmark designed to assess LLMs' proficiency in following multi-turn and multilingual instructions."* |
| **S3** | `https://arxiv.org/abs/2603.10044`; `https://arxiv.org/html/2603.10044v1` | 200; 200 | pre-registered scaffold-safety study — arXiv 2603.10044, 2026-03 | abs: *"We test six leading models on four pre-registered safety benchmarks with a direct API and three scaffolds: ReAct, multi-agent, and map-reduce. We conducted 62,808 scored evaluations."* html: *"combining pre-registration, assessor blinding, equivalence testing, and specification curve analysis."* and *"pre-registered equivalence bounds of ± 2 pp"* |
| **S4** | `https://arxiv.org/abs/2410.02810` | 200 | StateAct (Rozanov & Rei) — arXiv 2410.02810, 2024-10 (EMNLP 2025 REALM per r11) | abs: *"StateAct outperforms ReAct, the previous best base agent, by over 10% on Alfworld, 30% on Textcraft, and 7% on Webshop across multiple frontier LLMs."* |
| **S5** | `https://arxiv.org/abs/2404.06654` | 200 | RULER (Hsieh et al., NVIDIA) — arXiv 2404.06654, 2024-04 | abs: *"we create a new synthetic benchmark RULER with flexible configurations for customized sequence length and task complexity"*; text: *"We evaluate 17 long-context LMs with 13 representative tasks in RULER."* |
| **S6** | `https://arxiv.org/abs/2201.11903` | 200 | Chain-of-Thought (Wei et al.) — arXiv 2201.11903, 2022-01 (NeurIPS 2022) | abs: *"Experiments on three large language models show that chain of thought prompting improves performance on a range of arithmetic, commonsense, and symbolic reasoning tasks."* |
| **S7** | `https://arxiv.org/abs/2507.11538` | 200 | IFScale (Distyl AI) — arXiv 2507.11538, 2025-07 | abs: *"We introduce IFScale, a simple benchmark of 500 keyword-inclusion instructions for a business report writing task to measure how instruction-following performance degrades as instruction density increases. We evaluate 20 state-of-the-art models across seven major providers and find that even the best frontier models only achieve 68% accuracy at the max density of 500 instructions."* |
| **S8** | `https://arxiv.org/abs/2504.08312` | 200 | SortBench (Herbold) — arXiv 2504.08312, 2025-04 | abs: *"Within this paper, we describe the new SortBench benchmark for LLMs that comes with different difficulties and that can be easily scaled in terms of difficulty."* |
| **S9** | `https://raw.githubusercontent.com/google/BIG-bench/main/bigbench/benchmark_tasks/list_functions/README.md`; `…/list_functions/c001/task.json`; `https://api.github.com/repos/google/BIG-bench/contents/bigbench/benchmark_tasks/list_functions` | 200; 200; 200 | BIG-bench `list_functions` (Srivastava et al. lineage), repo as fetched 2026-09 | README header: *"**10750** free text [queries of dummy model]"*; `c001`: *"Infer and compute a function over lists of natural numbers for a given input given a predetermined set of examples The target function is \"remove all but element 3\"."*, `task_prefix`: *"Apply a function to the final input list to generate the output list. Use any preceding inputs and outputs as examples."*; dir listing = 253 entries `README.md`,`c001`…`c252` |
| **S10** | `https://raw.githubusercontent.com/google/BIG-bench/main/bigbench/benchmark_tasks/tracking_shuffled_objects/README.md`; `https://api.github.com/repos/google/BIG-bench/contents/bigbench/benchmark_tasks/tracking_shuffled_objects` | 200; 200 | BIG-bench `tracking_shuffled_objects` | README header: *"**3750** multiple choice and **0** free text"*; dir listing = `README.md, five_objects, results, seven_objects, task.json, three_objects` ⇒ the *same* construct ships at three object counts (one family, three difficulties) |
| **S11** | `https://arxiv.org/abs/2511.10457` | 200 | "Exploring State Tracking Capabilities of LLMs" — arXiv 2511.10457, 2025-11 | abs: *"we propose a benchmark based on three well-defined state tracking tasks and analyse the performance of LLMs in different scenarios."* |
| **S12** | `https://arxiv.org/abs/2406.10149` | 200 | BABILong — arXiv 2406.10149, 2024-06 | abs: *"BABILong includes a diverse set of 20 reasoning tasks, including fact chaining, simple induction, deduction, counting, and handling lists/sets."* |
| **S13** | `https://arxiv.org/abs/2209.13331` | 200 | EditEval (Dwivedi-Yu et al.) — arXiv 2209.13331, 2022-09 | abs: *"This work presents EditEval: An instruction-based, benchmark and evaluation suite that leverages high-quality existing and new datasets for automatic evaluation of editing capabilities such as making text more cohesive and paraphrasing."* |
| **S14** | `https://arxiv.org/abs/2511.04486` | 200 | EDIT-Bench (Chi et al.) — arXiv 2511.04486, 2025-11 | abs: *"We introduce EDIT-Bench, a benchmark for evaluating LLM code editing capabilities grounded in real-world usage"*; text: *"EDIT-Bench comprises of 540 problems, multiple natural and programming languages"* |
| **S15** | `https://arxiv.org/abs/2410.01208` | 200 | StringLLM / StringBench (Wang et al.) — arXiv 2410.01208, 2024-10 | abs: *"we first propose StringLLM, a method to construct datasets for benchmarking string processing capability of LLMs. We use StringLLM to build a series of datasets, referred to as StringBench."* |
| **S16** | `https://arxiv.org/abs/2311.07911` | 200 | IFEval (Zhou et al.) — arXiv 2311.07911, 2023-11 | abs: *"We identified 25 types of those verifiable instructions and constructed around 500 prompts"* |
| **S17** | `https://arxiv.org/abs/2401.03601` | 200 | InFoBench (Qin et al.) — arXiv 2401.03601, 2024-01 | abs: *"Alongside this metric, we present InFoBench, a benchmark comprising 500 diverse instructions and 2,250 decomposed questions across multiple constraint categories."* |
| **S18** | `https://arxiv.org/abs/2107.07002` | 200 | The Benchmark Lottery (Dehghani et al.) — arXiv 2107.07002, 2021-07 | abs: *"On multiple benchmark setups that are prevalent in the ML community, we show that the relative performance of algorithms may be altered significantly simply by choosing different benchmark tasks, highlighting the fragility of the current paradigms"* |
| **S19** | `https://arxiv.org/abs/2411.12990` | 200 | BetterBench (Reuel et al.) — arXiv 2411.12990, 2024-11 | abs: *"we develop an assessment framework considering 46 best practices across an AI benchmark's lifecycle and evaluate 24 AI benchmarks against it."* [+ *"We find that there exist large quality differences and that commonly used benchmarks suffer from signific…"* — the fetched abstract is cut at the arXiv page's preview limit; only the first sentence is quoted in full] |
| **S20** | `https://arxiv.org/abs/2511.04703` | 200 | Construct Validity in LLM Benchmarks (Bean et al.) — arXiv 2511.04703, 2025-11 | abs: *"With a team of 29 expert reviewers, we conduct a systematic review of 445 LLM benchmarks from leading conferences in natural language processing and machine learning."* / *"we provide eight key recommendations and detailed actionable guidance to researchers and practitioners in developing LLM benchmarks."* |
| **S21** | `https://arxiv.org/abs/2310.11324` | 200 | Prompt-format sensitivity (Sclar et al.) — arXiv 2310.11324, 2023-10 (ICML 2024) | abs: *"We find that several widely used open-source LLMs are extremely sensitive to subtle changes in prompt formatting in few-shot settings, with performance differences of up to 76 accuracy points when evaluated using LLaMA-2-13B."* |
| **S22** | `https://arxiv.org/abs/2501.17399` | 200 | MultiChallenge (Sirdeshmukh et al.) — arXiv 2501.17399, 2025-01 | abs: *"MultiChallenge identifies four categories of challenges in multi-turn conversations that are not only common and realistic among current human-LLM interactions, but are also challenging to all current frontier LLMs."* |
| **S23** | `https://arxiv.org/abs/2602.02888` | 200 | HALT (Shapiro, Taneja, Goel) — arXiv 2602.02888, 2026-02 | abs: *"Unlike black-box approaches, it operates on log-probs rather than surface-form text, which enables stronger domain generalization"* (nearest *cross-domain generalization* study found in this hunt; it transports a *detector*, not a density dose) |
| **S24** | `https://arxiv.org/abs/2606.11217`; `https://arxiv.org/html/2606.11217v1` | 200; 200 | "in silico behavioural experiments" methodology — arXiv 2606.11217, 2026-06 (r11-carried as a preregistration *template* source; re-fetched here for this round's status) | abs: *"The proliferation of large language models (LLMs) and autonomous AI agents has given rise to a rapidly growing methodological paradigm: "in silico" behavioral experiments."* / *"While these experiments with AI agents offer unprecedented advantages in terms of scalability, cost efficiency, and experimental control, they also inherit, and in some cases amplify, methodologi[cal …]"* (sentence truncated at the fetched page's cut point) |
| **S44** | `https://arxiv.org/abs/2412.03597` | 200 | evaluation-framework vulnerability review — arXiv 2412.03597, 2024-12 | abs: *"Our systematic analysis of NLP evaluation frameworks reveals pervasive vulnerabilities across the evaluation spectrum, from basic metrics to complex benchmarks like GLUE and MMLU."* |
| **S45** | `https://arxiv.org/abs/2609.23201` | 200 | limits of general LLM rankings — arXiv 2609.23201, 2026-09 | abs: *"Yet an overall score is interpretable only in relation to the system tested, the questions included, and the conditions of evaluation. This perspective examines five connected limitations of general LLM rankings"* |

### 2.2 C5 — per-problem probabilistic forecasts, proper scoring, calibration, forecasting platforms

| ID | URL(s) | HTTP | Venue / year | Load-bearing sentence(s) |
|---|---|---|---|---|
| **S25** | `https://arxiv.org/abs/2509.20645`; `https://arxiv.org/html/2509.20645v3` | 200; 200 | PRECOG / "Anticipatory Evaluation of Language Models" (Park, Mendes, Stanovsky, Ritter) — arXiv 2509.20645, 2025-09 | abs: *"We investigate whether evaluation outcomes can be forecast before any experiments are conducted. Specifically, we study text-only performance prediction, where models estimate performance from task descriptions and experimental configurations alone, without access to dataset instances."* / *"We scrape task and configuration descriptions from arXiv, yielding 2,290 instances covering 1,519 papers"*; html: *"Confidence values are derived from a 10-bin categorical output produced by the verbalized confidence calibration."* and *"evaluate calibration by filtering to items with confidence ≥ τ"* |
| **S26** | `https://arxiv.org/abs/2409.19839` | 200 | ForecastBench (Karger et al.) — arXiv 2409.19839, 2024-09 | abs: *"we introduce ForecastBench: a dynamic benchmark that evaluates the accuracy of ML systems on an automatically generated and regularly updated set of 1,000 forecasting questions."* |
| **S27** | `https://www.forecastbench.org/assets/pdfs/forecastbench_updated_methodology.pdf` | 200 | ForecastBench updated methodology (Forecasting Research Institute), 2026 | *"Originally, ForecastBench ranked forecasters using standard Brier scores."* / *"we present the difficulty-adjusted Brier score, which decomposes forecasting performance into forecaster ability and question difficulty."* / *"outperforms alternative methods including standard Brier score, Brier Skill Score, and Peer Score."* |
| **S28** | `https://epoch.ai/benchmarks/forecastbench` | 200 | Epoch AI benchmark page (Epoch AI), undated as fetched 2026-09 | *"Forecasts are scored with a difficulty-adjusted Brier Index on an interpretable 0–100% scale, where higher is better (100% is perfect, 50% corresponds to an uninformed guess, and 0% is maximally wrong)."* |
| **S29** | `https://forecastingresearch.org/research/ai-progress-accuracy-update` | 200 | Forecasting Research Institute, "AI progress accuracy update", 2026 | *"Capabilities Across all of our AI progress work, forecasts on benchmark performance give us the clearest picture of forecaster accuracy so far."* / *"a clear trend is apparent from these resolved forecasts: the median expert and superforecaster tend to dramatically underestimate AI progress on benchmarks."* |
| **S30** | `https://leap.forecastingresearch.org/reports/waves-1-to-3-insights` | 200 | FRI LEAP panel report, waves 1–3, 2026 | *"On frontier capability milestones, 23% of experts expect saturation of the FrontierMath benchmark by 2030"*; question text: *"What will be the highest percentage accuracy achieved by an AI model on FrontierMath , by 2025, 2027, and 2030?"* |
| **S31** | `https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0248780` | 200 | Gordon, Viganola, Dreber, Johannesson, Pfeiffer — PLOS ONE 16(1): e0248780, 2021 | *"Our results show prediction markets can determine the outcomes of direct replications with 73% accuracy (n = 103)."* / *"Overall, the prediction markets had an accuracy of 73% (75 out of 103 studies), while the surveys had an accuracy of 66% (68 out of 103 studies)."* |
| **S32** | `https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0262862` | 200 | Gordon et al. — PLOS ONE 2022 (replication forecasting across projects) | *"Our primary metric of prediction skill was the Brier score (BS), a standard measure of prediction accuracy [ 14 ]."* / *"When trial results became available, prediction skill was calculated using Brier scores (BS) and compared against uninformative prediction (i."* / *"The first, the "uninformative" benchmark, reflects the Brier score that would be obtained if a forecaster always abstained from providing any information regarding whether an event was more likely to occur than not"* |
| **S33** | `https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jrssb.pdf` | 200 | Gneiting, Balabdaoui & Raftery — *J. R. Statist. Soc. B* 69(2):243–268, 2007 | *"We propose a diagnostic approach to the evaluation of predictive performance that is based on the paradigm of maximizing the sharpness of the predictive distributions subject to calibration."* / *"Like all proper scoring rules for binary probability forecasts, the Brier score allows for the distinction of a calibration component and a refinement component (Murphy, 1972; DeGroot and Fienberg, 1983; Dawid, 1986)."* / *"Murphy and Winkler (1987) proposed a general framework for the evaluation of point forecasts that uses a diagnostic approach based on graphical displays, summary measures and scoring rules."* |
| **S34** | `https://arxiv.org/abs/2005.01835` | 200 | Pohle, "The Murphy Decomposition and the Calibration-Resolution Principle" — arXiv 2005.01835, 2020-05 | abs: *"The principle is based on a fully general version of the Murphy decomposition of loss functions"* / *"It amongst others exposes the shortcomings of several widely used forecast evaluation methods."* |
| **S35** | `https://lirias.kuleuven.be/retrieve/577522` | 200 | Van Calster, Nieboer, Vergouwe, De Cock, Pencina, Steyerberg — *J. Clinical Epidemiology*, 2016 (post-refereeing author PDF) | *"The next level is to have weak calibration of predictions, defined as a calibration intercept ( ) of 0 and a calibration slope of 1."* / *"At model validation, sufficiently large datasets should be available to reliably assess moderate calibration. We suggest a minimum of 200 events and 200 non-events."* / *"calibration slope smaller than one when the model is internally or externally validated"* / *"[the flexible] calibration curve is more variable and hence requires more data than the calibration slope for a stable assessment."* |
| **S36** | `https://ds.data.jma.go.jp/tcc/tcc/library/library2011/TCC_Seminar_Verification(Dehara2011).pdf` | 200 | Dehara, "Verification of probability forecast" — Japan Meteorological Agency TCC seminar tutorial, 2011 | *"Brier skill score = An improvement rate with respect to a climatic forecast"* / *"Range: minus infinity to 1. Perfect score: 1"* / *"BSS<0 : inferior to the climatic forecast."* |
| **S37** | `https://www.jmlr.org/papers/volume24/23-0106/23-0106.pdf` | 200 | Resin, *JMLR* 24 (2023) 1–21 | *"The proposed evaluation metrics are based on symmetric proper scoring rules and admit comparison of various types of predictions ranging from single-class point predictions to fully specified predictive distributions. The Brier score yields a metric that is particularly well suited for this kind of comparison."* |
| **S38** | `https://arxiv.org/abs/1706.04599` | 200 | Guo, Pleiss, Sun & Weinberger — arXiv 1706.04599, 2017 (ICML 2017) | abs: *"Confidence calibration -- the problem of predicting probability estimates representative of the true correctness likelihood -- is important for classification models in many applications. We discover that modern neural networks, unlike those from a decade ago, are poorly calibrated."* (the **model-confidence** sense this pricing excludes) |
| **S39** | `https://arxiv.org/abs/2607.20526` | 200 | ConfidenceBench — arXiv 2607.20526, 2026-07 | abs: *"We present ConfidenceBench, a calibration benchmark that evaluates verbalized confidence estimates in 15 frontier LLMs using the Brier score, a proper scoring rule that incentivises truthful probability reporting."* / *"The benchmark comprises 200 private multiple-choice questions across four categories"* (per-item Brier in-domain, but for **model** confidence) |
| **S40** | `https://aclanthology.org/2025.findings-acl.790/` | 200 | PredictaBoard — ACL Findings 2025 | abs: *"we present PredictaBoard, a novel collaborative benchmarking framework designed to evaluate the ability of score predictors (referred to as assessors) to anticipate LLM errors on specific task instances (i.e., prompts) from existing datasets."* |
| **S41** | `https://arxiv.org/abs/2402.14992` | 200 | tinyBenchmarks (Maia Polo et al.) — arXiv 2402.14992, 2024-02 (ICML 2024) | abs: *"we show that to accurately estimate the performance of an LLM on MMLU, a popular multiple-choice QA benchmark consisting of 14K examples, it is sufficient to evaluate this LLM on 100 curated examples."* |
| **S42** | `https://arxiv.org/abs/2507.04562` | 200 | Lu, "Evaluating LLMs on Real-World Forecasting Against Expert Forecasters" — arXiv 2507.04562, 2025-07 | abs: *"I evaluate state-of-the-art LLMs on 464 forecasting questions from Metaculus, comparing their performance against top forecasters. Frontier models achieve Brier scores that ostensibly surpass the human crowd but still significantly underperform a group of experts."* |
| **S43** | `https://www.psycharchives.org/handle/20.500.12034/8644` | 200 | PRP-QUANT preregistration template (Stage-1 Registered Report) — PsychArchives, undated as fetched | page title only: *"Stage 1 Registered Report: Restriction of researcher degrees of freedom through the Psychological Research Preregistration-Quantitative (PRP-QUANT) Template"* (body text not extracted in-session; used only as a *template exists* existence claim) |

**Shared rows.** S3 and S24 are counted once in the register but are used by both sections
(S3: pre-registered four-benchmark-family study — prior art for both the multi-family transport
*design* and pre-registered eval methodology; S24: preregistration *template* for agent experiments).

**r11 sources deliberately NOT re-priced here** (double-count guard, per the task brief):
`corpus/evidence/round11-fleet/r11-prior-art-prereg.md:298-306` (M1a–M1d: paired analysis KNOWN,
filed prereg stage INCREMENTAL, **Brier-scored self-predictions INCREMENTAL**, "preregistered LLM
eval" novelty NOT SUPPORTED) and `corpus/evidence/round11-fleet/r11-prior-art-granularity.md:25-28`
(C1 INCREMENTAL-low, C2 KNOWN/INCREMENTAL, **C3 NOVEL-instrument**, C4 INCREMENTAL). This file prices
different constructs and, where it touches the same objects, it **strengthens or repeats** r11's
verdict rather than claiming a new one.

---

## 3. C4 — pricing "transport to a second task family"

### 3.1 The claim, restated and scoped

C4 asserts that the paired severity contrast produced by removing one forced emission checkpoint
(`T-DENSE` graded {4,7,10} vs `T-SPARSE` graded {7,10}, per-pid mean `nwrong` at shared turns
{7,10}, n=48) is **positive** on a task family whose state is an *ordered token list* operated on by
`APP/INS/DEL/SET/MOV/SWP/REV` — i.e. no integer arithmetic, no key set, order-carrying positional
state (`probe_plan_r12.md:23`, `§2.2`). The claim is *within-family-2 only* for its metric; the
cross-family statement is limited to the effect-size direction and never pooled (`:334-337`).
So what has to be priced is: **(i)** does a published suite already run the *same manipulation*
across ≥2 structurally different state-tracking families? **(ii)** does a published suite already
use a *positional list-editing* family with a dose/density manipulation? **(iii)** is the
"effects may not transfer across families/benchmarks" concern published (construct validity /
benchmark specificity)?

### 3.2 Evidence

**(i) "One manipulation, several task families" is a standard published design — not a novelty.**

- **S1 (Laban et al. 2025)** performs exactly this move with a *conversation-structure* manipulation:
  instructions are sharded across **six generation tasks** (600 instructions) and compared against
  `Full`/`Concat` controls, with a reported *"average drop of 39% across six generation tasks."* That
  is a same-manipulation, cross-task-family degradation study with a **magnitude** endpoint.
- **S5 (RULER)** applies one manipulation — sequence length/complexity — across **13 tasks** in 4
  categories (`"We evaluate 17 long-context LMs with 13 representative tasks in RULER."`).
- **S6 (CoT)** applies one prompting manipulation across **three** structurally different reasoning
  families (arithmetic / commonsense / symbolic).
- **S4 (StateAct)** applies one state-tracking emission manipulation across **three** agent task
  families (Alfworld / Textcraft / Webshop) with distinct effect sizes (+10 / +30 / +7).
- **S3 (arXiv 2603.10044, 2026)** is the closest *pre-registered* multi-family manipulation study:
  six models × **four pre-registered safety benchmarks** × three scaffolds, with equivalence bounds
  and specification-curve analysis.
- **S22 (MultiChallenge)** and **S2 (Multi-IF)** show the multi-turn manipulation being reused across
  four challenge categories and across languages respectively.
- **S12 (BABILong)** and **S11 (arXiv 2511.10457)** ship multi-task suites whose *tasks* vary while
  the *manipulation* (context length; construction) does not — the complement of the transport design.

**(ii) Density/difficulty ladders exist, but single-family and (mostly) pass-rate-only.**

- **S7 (IFScale)** is the closest published *density ladder*: keyword-inclusion instruction counts of
  10→500 in one writing task, with degradation curves and three decay patterns, scored as per-instruction
  compliance (a severity-like count) but **one family only**.
- **S8 (SortBench)** is an explicitly *difficulty-scalable* list-manipulation benchmark (`"can be
  easily scaled in terms of difficulty"`), one family, accuracy-style scoring.
- **S9 (BIG-bench `list_functions`)** is the published *positional/functional list-editing* family
  (Turing-list-function style: infer & apply a sequence of list operations to a final input list;
  10,750 free-text queries). It is family-2-shaped **as a construct** but has **no emission-schedule
  manipulation** and grades exact-string match, not positional severity.
- **S10 (BIG-bench `tracking_shuffled_objects`)** shows the *other* half: the ledger-style tracking
  construct ships at three object counts (`three_objects`/`five_objects`/`seven_objects`) — i.e.
  within-family difficulty variation, not cross-family transport.
- **S13/S14/S15/S16/S17** cover editing/string/instruction families (EditEval; EDIT-Bench, 540
  problems; StringLLM/StringBench; IFEval, 25 verifiable instruction types; InFoBench, 500
  instructions / 2,250 decomposed questions / "multiple constraint categories") — all single-manipulation
  published families, none ablating forced-emission *density* on identical problems with a severity
  endpoint.

**(iii) The "effects may not transfer" concern is well-published (this is the reason C4 cannot be sold
as a phenomenon discovery).**

- **S18 (Benchmark Lottery):** *"the relative performance of algorithms may be altered significantly
  simply by choosing different benchmark tasks."*
- **S19 (BetterBench):** 46 lifecycle best practices assessed over 24 AI benchmarks; large quality
  differences found.
- **S20 (Construct validity, 445 benchmarks / 29 reviewers):** the corpus's own family of concern —
  measures that do not represent the intended construct — with eight recommendations.
- **S21 (prompt-format sensitivity):** *"performance differences of up to 76 accuracy points"* from
  meaning-preserving formatting changes ⇒ single-instance effect sizes are known to be
  instrument-sensitive.
- **S44** (pervasive evaluation-framework vulnerabilities) and **S45** (*"an overall score is
  interpretable only in relation to the system tested, the questions included, and the conditions of
  evaluation"*).
- **S23 (HALT)** is the only fetched study that explicitly *transports an instrument across domains*
  (a log-prob hallucination detector, "stronger domain generalization"), which is the nearest
  "transport" precedent found and is still not an emission-density dose.

### 3.3 Verdict — **C4 = INCREMENTAL (low)**

**Reasoning.** The *design idiom* C4 reuses — one manipulation applied across ≥2 structurally
different task families — is standard published practice (S1 with six families and a quantified
39% average drop; S5 with 13 tasks; S6 with three reasoning families; S4 with three agent families;
S3 pre-registered across four benchmark families). The *second family itself* (positional/functional
list editing, order-carrying state) is a published construct (S9; S8; S12's list/set tasks; S14's
edits). The measurement-level novelty claim of this lane remains exactly what r11 priced as
`NOVEL-instrument` under *its* C3 (`r11-prior-art-granularity.md:27`) — **C4 must not restate that
verdict as its own**; C4 is a *cross-family application* of that instrument, and the cross-family
demand is published. What is **not** found: any suite that runs the *same* checkpoint-density ladder
on *identical problems+seeds* across two structurally different state-tracking families with a
severity (positional-mismatch) endpoint. That residue is real but is an *incremental application*,
not a new phenomenon and not a new instrument.
→ **VERDICT: `INCREMENTAL`** (low). No `NOVEL-*` verdict is claimed for C4.

### 3.4 Strongest permitted wording (C4)

**Permitted (use this):**
> "C4 tests whether the emission-density severity contrast observed on the inventory-ledger family
> reproduces *in the same direction* on a second, structurally different state-tracking family
> (ordered token-sequence editing: no integer arithmetic, no key set, order-carrying state) under the
> same served unit and pinned seeds — paired `T-SPARSE − T-DENSE` at shared checkpoints {7,10}, n=48.
> The *pattern* of applying one manipulation across several task families is published (Laban et al.'s
> six-task sharding study, RULER's 13-task length study, StateAct's three-agent-family state-tracking
> study, and a 2026 pre-registered four-benchmark scaffold study), and positional list editing is a
> published construct (BIG-bench `list_functions`, SortBench); so this is an **incremental
> cross-family application**, not a new phenomenon, and it generalizes only to *this* second family
> under *this* stack."

**Forbidden phrasings (would overclaim against S1/S4/S5/S9/S18/S20):**

| Do NOT write | Why | Write instead |
|---|---|---|
| "first demonstration that a degradation effect transports across task families" | S1 (six families, 39% average drop under sharding), S5 (13 tasks), S4 (three agent families), S3 (four pre-registered families) | "an incremental cross-family application of an instrument-level manipulation; the transport *design* is published" |
| "the density dose is task-general / family-agnostic" | C4 is two families, one stack; S18/S21 show effect sizes are benchmark- and format-sensitive | "the contrast reproduces in the same direction in one additional family; no claim of generality beyond these two families" |
| "a novel task family / novel benchmark" | S9 (`list_functions`, 10,750 free-text queries), S8 (SortBench), S14 (540 problems) | "the family-2 generator is *new machinery for this lane*, built on a published construct (positional list editing)" |
| "cross-family effect-size comparison" as an estimate | `probe_plan_r12.md:334-337` forbids pooling; S21 shows formatting alone moves scores by tens of points | "within-family contrast only; the cross-family statement is limited to the sign, reported descriptively" |

---

## 4. C5 — pricing "per-problem probabilistic forecasts of the run's own eval outcomes"

### 4.1 The claim, restated and scoped

C5 asserts that a **mechanical predictor** — fitted *only* on r11's committed per-problem bytes
(`probe_plan_r12.md:38-40`) — issues a **per-problem probability** of pass for each of the run's
448 (arm × problem) binary pass events, and that this forecast beats **arm-level climatology** on
Brier, with a reported Brier skill score, a logistic-calibration slope/intercept, and a 5-bin
reliability table (`:24`, `:120`, R5 at `:146-148`). It is **not** model-confidence calibration
(S38/S39 are the wrong sense) and it is **not** cold forecasting: the plan already states the skill
is *persistence* skill because the predictor consumes r11 outcomes on the same problems, and
family-2 forecasts are constant per arm by design (`:338-340`).

### 4.2 Evidence

**(a) The metrics are canon — every component is a published instrument.**

- **S33** (*JRSS-B* 2007): calibration-vs-sharpness paradigm, and the Brier score decomposes into
  calibration and refinement components, citing Murphy 1972/1987.
- **S34** (Pohle 2020): a fully general Murphy decomposition and the calibration–resolution
  principle; explicitly *"exposes the shortcomings of several widely used forecast evaluation
  methods."*
- **S35** (Van Calster et al. 2016, *J Clin Epidemiol*): the **calibration-slope/intercept** canon —
  weak calibration ≡ intercept 0 and slope 1; logistic recalibration is the standard estimator — with
  the load-bearing sample-size constraint *"We suggest a minimum of 200 events and 200 non-events"*,
  and the known attenuation (*"calibration slope smaller than one when the model is internally or
  externally validated"*), plus *"[the] calibration curve is more variable and hence requires more
  data than the calibration slope for a stable assessment."*
- **S36** (JMA verification tutorial): operational definition of the **Brier skill score** as
  *"An improvement rate with respect to a climatic forecast"*, range (−∞,1], `BSS<0` inferior — i.e.
  BSS is *reference-forecast-relative*, exactly as the plan's arm-climatology reference implies.
- **S37** (*JMLR* 2023): proper-scoring-rule framing and the Brier score as the suitable comparison
  metric across prediction types.
- **S38/S39** are the excluded sense (model confidence); S39 (ConfidenceBench) is nonetheless the
  nearest **per-item Brier in-domain** artifact: 200 private questions, per-item verbalized confidence,
  scored with Brier.

**(b) "Forecast an evaluation's outcomes before running it" is published.**

- **S25 (PRECOG, arXiv 2509.20645)** is the closest instrument: *"We investigate whether evaluation
  outcomes can be forecast before any experiments are conducted… text-only performance prediction,
  where models estimate performance from task descriptions and experimental configurations alone,
  without access to dataset instances"* — 2,290 instances / 1,519 papers. Its reported endpoints are
  point-error metrics (its own text discusses *"verbalized confidence calibration"* and calibration
  filtering by confidence threshold), **not** Brier/BSS/calibration slope, but the *frame*
  ("forecast the eval outcome before the eval") is published.
- **S40 (PredictaBoard, ACL Findings 2025)** is published **per-item** outcome anticipation:
  *"evaluate the ability of score predictors (referred to as assessors) to anticipate LLM errors on
  specific task instances (i.e., prompts)"* — per-instance prediction with rejection-rate scoring.
- **S41 (tinyBenchmarks)** is published **per-item** estimation inside LLM eval (IRT, 100 curated
  items estimating a full benchmark's per-item expectations).
- **S31/S32 (replication-forecasting literature).** S32 states the exact instrument pattern C5 uses
  at a different level of analysis: *"When trial results became available, prediction skill was
  calculated using Brier scores (BS) and compared against uninformative prediction"*, with an explicit
  *"uninformative" benchmark* baseline; S31 quantifies per-study market/survey accuracy (73% vs 66%
  over 103 studies). **Note:** the *subjects* are external forecasters predicting others' studies,
  not the experimenter predicting its own run — r11 already priced the self-scoring half of this as
  `INCREMENTAL` (`r11-prior-art-prereg.md:305`).

**(c) Probabilistic forecasts *of AI benchmark/eval outcomes* are already a scored public practice.**

- **S26 (ForecastBench)** and **S27/S28**: forecasters (human and ML) are scored on future-event and
  model-performance questions with **Brier**; the current methodology uses a *difficulty-adjusted
  Brier score* precisely because raw Brier is not comparable across non-overlapping question sets,
  and it reports having compared *"standard Brier score, Brier Skill Score, and Peer Score"* (S27).
- **S29/S30 (FRI)**: *"forecasts on benchmark performance give us the clearest picture of forecaster
  accuracy so far"*; the LEAP panel collects distributional forecasts on benchmark saturation
  (*"What will be the highest percentage accuracy achieved by an AI model on FrontierMath , by 2025,
  2027, and 2030?"*).
- **S42**: LLM-vs-expert Brier on 464 Metaculus questions — the same scoring rule used as a public
  leaderboard metric.
- **S43**: preregistration *templates* that explicitly restrict researcher degrees of freedom are a
  published artifact class (title fetched; body not read in-session → existence claim only).

**(d) The composite as executed here is not found.**

No fetched source files a **hashed-preregistered, per-item probabilistic self-forecast of its own
LLM-eval pass outcomes**, emitted by the same artifact as the run, scored by Brier + BSS against the
run's own arm-climatology + logistic-calibration slope/intercept + 5-bin reliability. The nearest
collocations are S32 (per-study Brier vs uninformative baseline, but external forecasters),
S25 (forecast-before-running, but point-error endpoints and model-generated), S40/S41 (per-item
prediction, different scoring), S3/S43 (pre-registered eval methodology without per-item probability
files).

### 4.3 Verdict — **C5 = INCREMENTAL (low)**

**Reasoning.** Every *component* is canon (S33/S34/S35/S36/S37) or in-domain practice (S26–S30, S42);
the *act* of predicting evaluation outcomes before running them is published (S25) and has a
per-item cousin (S40/S41); probabilistic per-item scoring against an explicit uninformative baseline
is published in the adjacent replication-forecasting literature (S32). r11 already reached
`INCREMENTAL` for "Brier-scored *self*-predictions + mechanical verdict rule"
(`r11-prior-art-prereg.md:305`); increasing the event count from 3 to 448 and adding
BSS-vs-climatology and a calibration slope **does not cross a novelty boundary**, because the added
instruments are themselves borrowed canon (S35, S36). A `NOVEL-instrument` verdict is therefore not
available, and `NOVEL-phenomenon` would misdescribe a *self-scoring device* (no external phenomenon
is claimed).
→ **VERDICT: `INCREMENTAL`** (low). No `NOVEL-*` verdict is claimed for C5.

### 4.4 Strongest permitted wording (C5)

**Permitted (use this):**
> "C5 reports a **lane-internal calibration instrument**: a committed mechanical predictor, fitted
> only on r11's committed per-problem bytes, files a per-problem probability for each of the run's
> 448 binary pass events, scored with published forecast-verification practice — Brier, BSS against
> the run's own arm climatology, logistic-calibration slope/intercept, 5-bin reliability. All
> components are canon (Gneiting/Balabdaoui/Raftery 2007; Van Calster et al. 2016; JMA verification
> practice), forecasting an evaluation's outcomes before running it is published (PRECOG), per-item
> anticipation of eval outcomes is published (PredictaBoard; tinyBenchmarks), and probabilistic
> forecasts of AI benchmark results are already scored publicly with Brier/BSS variants
> (ForecastBench/FRI/Epoch AI). The measured skill is **persistence** skill (r11 outcomes on the same
> problems), family-2 forecasts are constant per arm by design (a no-information comparator), and the
> calibration summary is **descriptive**: at ~45% pass rate the run supplies on the order of 200
> events — at the edge of Van Calster et al.'s suggested ≥200 events **and** ≥200 non-events for
> reliable calibration assessment — and the BSS reference is an in-sample (arm-observed) climatology."

**Forbidden phrasings (would overclaim against S25/S32/S35/S36/S37 and against r11's M1c):**

| Do NOT write | Why | Write instead |
|---|---|---|
| "novel forecasting instrument / first to apply Brier to an LLM eval" | S32 (Brier vs uninformative baseline for per-study forecasts), S26–S30 (Brier/BSS on AI-benchmark forecasts), S39 (per-item Brier in-domain), r11 `M1c` INCREMENTAL | "a lane-internal application of published forecast-verification instruments; the instrument is borrowed canon" |
| "our forecasts are calibrated / well-calibrated" | S35 requires ≥200 events **and** ≥200 non-events for reliable moderate-calibration assessment; slope attenuates toward <1 on validation | "calibration slope/intercept reported **descriptively** as a diagnostic, with the event-count caveat stated" |
| "BSS proves the predictor has skill" (unqualified) | S36: BSS is an improvement rate *relative to a reference*; here the reference is the run's own in-sample climatology | "BSS > 0 relative to the run's own arm-climatology reference; the reference is in-sample and the skill is persistence, not cold forecasting" |
| "we validate our predictions with a proper scoring rule" | S27/S34 show the scoring-rule choice itself is contested (difficulty-adjusted Brier replaced raw Brier; widely used evaluation methods have exposed shortcomings); r11's S9 addendum shows monotone transforms of Brier are not proper | "Brier/BSS are reported as descriptive self-scoring devices; no properness guarantee is claimed" |
| "cold / ex-ante forecasting of an unseen run" | `probe_plan_r12.md:338-340` (r11 outcomes on the same problems) | "persistence forecast from prior-round bytes; family-2 forecasts are constant per arm by design" |
| "model confidence calibration" framing | S38/S39 are the excluded sense (model verbalized confidence) | "experimenter's per-problem outcome forecast (not model confidence)" |

---

## 5. Closing table

| claim | verdict | n_sources_fetched | strongest permitted wording |
|---|---|---|---|
| **C4 (transport of the density→severity dose to a second task family)** | **`INCREMENTAL`** (low) | **26 works / 32 URL rows** (S1–S24, S44, S45) | "an **incremental cross-family application**: the same-direction severity contrast is re-measured on one additional, structurally different state-tracking family (ordered token-sequence editing) under the same served unit and pinned seeds (paired `T-SPARSE − T-DENSE` at {7,10}, n=48). The multi-family design idiom (Laban et al.'s six-task sharding study: 39% average drop; RULER's 13-task length study; StateAct's three agent families; a pre-registered four-benchmark scaffold study) and positional list editing as a construct (BIG-bench `list_functions`; SortBench) are published; no generality beyond these two families is claimed." |
| **C5 (per-problem probabilistic forecasts of the run's own pass outcomes)** | **`INCREMENTAL`** (low) | **21 works / 24 URL rows** (19 own works S25–S43 = 20 URL rows, plus the shared S3 and S24 = 4 URL rows; S3/S24 are counted once in the 45-work total) | "a **lane-internal, preregistered per-item self-scoring device**: a committed mechanical predictor files per-problem probabilities for 448 binary pass events, scored with borrowed canon (Brier, BSS vs the run's own arm climatology, logistic-calibration slope/intercept, 5-bin reliability). Forecasting eval outcomes pre-run (PRECOG), per-item outcome anticipation (PredictaBoard, tinyBenchmarks), and Brier/BSS-scored AI-benchmark forecasts (ForecastBench/FRI/Epoch AI, with difficulty-adjusted Brier now preferred over raw Brier) are all published; the skill measured is **persistence**, the calibration statement is **descriptive** and event-count-limited (Van Calster et al.: ≥200 events and ≥200 non-events for reliable moderate-calibration assessment)." |

**Totals:** 45 distinct works fetched this round (52 URL rows: 32 C4 + 20 C5-own; the shared S3/S24
rows appear in the C4 tally), **all HTTP 200** on full GET;
6 fetch failures recorded (§7). Verdicts claim **no** `NOVEL-*`; both are priced as floors per the
r9 adversarial default (`corpus/knowledge/eval-prior-art-calibration.md` §Verdicts routing carried in
`round11-fleet/r11-prior-art-granularity.md:1-6`).

---

## 6. Negative searches (recorded although no `NOVEL-*` verdict is claimed)

The task requires a *stated negative search* only for `NOVEL-*` verdicts; **neither C4 nor C5 is
priced `NOVEL-*`**, so the negatives below are recorded as bounded non-findings, not as novelty
claims.

**N1 — no suite found that runs a checkpoint/emission-density ladder on identical problems across
≥2 structurally different state-tracking families with a severity endpoint.** Bounded by queries
§1.1 #7,#9,#11,#15 plus the C5-side sweep, and by reading every fetched density/difficulty instrument
(S7 single-family density; S8 single-family difficulty; S9/S10 single-family constructs; S12/S11
multi-task but single-manipulation). Nearest: S3 (checkpoint *diagnosis* position, not density) and
r11's priced neighbors (`r11-prior-art-granularity.md:27`). The last such query returned only
stream-processing/Flink material and a hallucinated `AblationBench` pointer, both rejected.

**N2 — no LLM-eval paper found that files hashed, per-item probabilistic forecasts of its own
outcomes and scores them with Brier + BSS + calibration slope.** Bounded by queries §1.2 #6, #9, #10,
#11, #13 and by full-text checks of the two most likely candidates: S3 (grep for `Brier` /
`probabilistic prediction` over its HTML → 0 hits; it pre-registers hypotheses, equivalence bounds and
a specification curve, not per-item probabilities) and S24 (grep for `Brier|forecast|predict…outcome`
over its HTML → 0 hits). Nearest collocations: S32 (external forecasters, per-study Brier vs
"uninformative" baseline), S25 (pre-run forecast of eval outcomes, point-error endpoints), S40/S41
(per-item prediction, other scoring), S39 (per-item Brier, model confidence sense).

**N3 — no published "same-manipulation across families" study found for *emission density* in
instruction-following form.** S7 (IFScale) manipulates density in one family only; S16/S17 fix
constraint counts across instruction *types*; nothing combines a density ladder with a
cross-family replication. This is the residue that keeps C4 at INCREMENTAL rather than KNOWN-dup, but
it is a negative over ~30 queries, not a registry sweep — flagged as a **gap**, not a proof.

---

## 7. Fetch failures (recorded verbatim; nothing unfetched is cited as read)

| Attempt | URL | HTTP / error | Consequence for this file |
|---|---|---|---|
| F1 | `https://www.metaculus.com/futureeval/methodology/` | **403** (also `https://www.metaculus.com/api2/questions/?limit=1` → 403) | Metaculus' own methodology page could not be read; the *platform-as-instrument* claim therefore rests on S27/S28/S26/S29/S30 and S42, not on Metaculus primary text |
| F2 | `https://glossary.ametsoc.org/wiki/Skill_score` | **403** | AMS glossary definition of "skill score" unavailable; BSS definition anchored on S36 (JMA) and S33/S34 instead |
| F3 | `https://journals.ametsoc.org/abstract/journals/apme/12/4/1520-0450_1973_012_0595_anvpot_2_0_co_2.xml` (Murphy 1973) | **202** (Cloudflare interstitial; 2,228-byte body, no article text) | **Murphy (1973) was NOT read first-hand this round.** The decomposition is cited via S33 (peer-reviewed, cites Murphy 1972/1987) and S34 (Pohle 2020, formal restatement) — labelled `[not read first-hand]` |
| F4 | `https://www.pnas.org/doi/10.1073/pnas.1509757112` (Dreber et al. 2015) | **403** | Dreber 2015 not read; the replication-forecasting instrument is anchored on S31/S32 (PLOS ONE, read) |
| F5 | `https://www.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf` | **SSL `CERTIFICATE_VERIFY_FAILED`** | Gneiting & Raftery (JASA 2007) not read; proper-scoring canon anchored on S33 (JRSS-B, read) + S34 + S37 (JMLR, read) |
| F6 | `https://journals.ametsoc.org/view/journals/mwre/102/1/1520-0493_1974_102_0048_asssfp_2_0_co_2.pdf` (Murphy 1974, sample skill score) | **202** (same interstitial) | "sample skill score" not read first-hand; BSS-as-reference-relative anchored on S36 |

Verified-and-rejected (fetched 200, wrong content for the claim, recorded so no later reader repeats
the error): `https://arxiv.org/abs/2305.14318` = *CREATOR* (not BetterBench);
`https://arxiv.org/abs/2507.08038` = *AblationBench* (not PredictaBoard);
`https://arxiv.org/abs/2410.01208` = *StringLLM/StringBench* (not ComplexBench).

---

## 8. Reproduction commands

Public-web status re-derivation — **self-contained**: it re-extracts the §2 register URLs from this
committed artifact and re-probes each one (stdlib-only, no third-party imports):

```bash
python3 - <<'PY'
import re, urllib.request, urllib.error
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept":"*/*"}
txt=open("corpus/evidence/round12-fleet/r12-prior-art-transport.md",encoding="utf-8").read()
rows=[l for l in txt.split("\n") if re.match(r'^\| \*\*S\d+\*\* \|', l)]      # §2 register rows only
urls=[u for l in rows for u in re.findall(r'`(https://[^`]+)`', l)]
print("register rows:", len(rows), "url rows:", len(urls), "unique:", len(set(urls)))
for u in dict.fromkeys(urls):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as r:
            r.read(2048); print(200, u)
    except urllib.error.HTTPError as e: print(e.code, u)
    except Exception as e: print(type(e).__name__, u)
PY
```

Observed on the writing host (2026-09-28): `register rows: 45 url rows: 52 unique: 52`, then
52×`200`. Expected failures if re-run: §7's F1–F6 (403/202/SSL) are *not* in the register, so a
re-run of the block above should print **only** `200` lines.

Equivalent one-liner per URL (curl):

```bash
curl -sS -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36' \
  -o /dev/null -w '%{http_code} %{url_effective}\n' 'https://arxiv.org/abs/2505.06120'
```

PDF sources were converted with:

```bash
pdftotext -layout <downloaded>.pdf <out>.txt     # poppler, /usr/bin/pdftotext
```

arXiv abstract extraction used the `<blockquote class="abstract">` block of the `/abs/<id>` page
(status recorded on the same GET); the `arxiv.org/html/<id>vN` mirror was used for full-text
sentences where cited (S1, S2, S3, S24, S25).

**Statement of limits.** This is a search-based negative for C4's residue and C5's composite, bounded
by the 30 queries in §1 plus the corpus's carried searches; it is not a registry (OSF/ACL/arXiv
full-sweep) or citation-graph exhaustive search. Confidence: **medium** for both verdicts, rising to
**medium–high** that neither claim can be priced `NOVEL-*`, since both would require overturning a
*published* component (S1/S4/S5 for C4's design idiom; S32/S33/S35/S36/S25 for C5's instrument
chain) rather than merely finding a closer neighbour.