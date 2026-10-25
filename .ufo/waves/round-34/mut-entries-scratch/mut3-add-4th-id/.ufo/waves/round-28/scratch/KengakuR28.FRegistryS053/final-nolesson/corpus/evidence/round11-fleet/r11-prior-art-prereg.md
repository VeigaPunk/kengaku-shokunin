# r11 prior-art pricing — METHOD claims (M1–M3)

Scout L2 (ScoutPrereg), 2026-09-28. Public web only. **Zero requests were issued to
`http://127.0.0.1:34113/...`** (no `/v1/chat/completions`, no `/v1/models`, no `/health`) —
the entire artifact is built from public fetches (`read` tool, `curl`, GitHub REST API).

Binding targets: `corpus/evidence/round11-power/probe_plan_r11.md` (§1 claim, §3 descriptors,
§7 deviations, §8 threats), `power_analysis_r11.md`, `predictions-r11.md`,
`SCORECARD.md` §Planned. Prior-round ground truth re-read: `corpus/knowledge/eval-prior-art-calibration.md`,
`corpus/evidence/round9-fleet/prior-art.md`, `corpus/evidence/round10-fleet/r10-scout-wiki.md`,
`corpus/evidence/round10-fleet/url-status.txt`.

Every claim below carries a source ID (`S<n>`) resolved in §2 with URL + HTTP status + title +
verbatim grounding sentence. Unfetched material is marked `[unverified]`.

---

## 1. Query log (every search issued)

`web_search` (16 queries, in order):

1. `"Adding Error Bars to Evals" Miller arXiv 2411.00640`
2. `llama.cpp issue 7052 same prompt seed temperature 0 different results multiple slots`
3. `"Adding Error Bars to Evals" cited follow-up 2025 statistical rigor LLM benchmark position paper`
4. `Thinking Machines "Defeating Nondeterminism in LLM Inference" batch invariance`
5. `llama.cpp q4_0 KV cache quantization accuracy degradation benchmark perplexity`
6. `"Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints" arXiv Bowyer Ivanova`
7. `Dror "Hitchhiker's Guide to Testing Statistical Significance in Natural Language Processing" ACL 2018`
8. `llama.cpp kv cache quantization q4_0 quality degradation discussion kawrakow perplexity github`
9. `preregistration LLM evaluation benchmark statistical power "preregistered" analysis plan 2025`
10. `"pre-registration" predictive modeling arXiv 2311.18807 preregistration machine learning experiments`
11. `llama.cpp determinism batch invariance issue 2025 --cont-batching same results different batch size`
12. `KIVI 2bit KV cache quantization accuracy drop downstream tasks arXiv 2402.02750`
13. `ForecastBench Brier score LLM evaluation calibration preregistered predictions`
14. `llama.cpp pull request "quantized KV cache" kawrakow perplexity 8-bit 4-bit cache results`
15. `KV cache quantization degrades long-context task accuracy needle retrieval paper 2025 quantized cache reasoning drop`
16. `NeurIPS paper checklist "statistical significance" error bars reproducibility ICLR evaluation practices statement`

GitHub REST searches (3, `api.github.com/search/issues`):

17. `repo:ggml-org/llama.cpp determinism in:title` (total_count 2)
18. `repo:ggml-org/llama.cpp batch invariant` (total_count 78)
19. `repo:ggml-org/llama.cpp quantized KV cache in:title` (total_count 28)

HTTP status probes (`curl -L -o /dev/null -w '%{http_code}'`, 2 batches covering the 31 URLs in §2).

Source-discovery note: all §2 numbers come from the fetched page text, never from a search
snippet. Search snippets were used only to *find* URLs (e.g. `arxiv.org/abs/2511.04703` on
S7, `arxiv.org/abs/2511.18643` and `aclanthology.org/2025.emnlp-main.479` on S22/S23).

---

## 2. Source register (in-session fetch: URL, status, title, grounding)

| ID | URL | HTTP | Title (as fetched) | Fetch route |
|---|---|---|---|---|
| S1 | `https://arxiv.org/abs/2411.00640` + `/html/2411.00640v1` | 200 / 200 | Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations (Evan Miller, Anthropic; 2024-11-01) | arXiv API + native HTML |
| S2 | `https://arxiv.org/abs/2503.01747` | 200 | Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints (Bowyer, Aitchison, Ivanova; 2025-03-03) | arXiv API |
| S3 | `https://aclanthology.org/P18-1128/` | 200 | The Hitchhiker's Guide to Testing Statistical Significance in Natural Language Processing (Dror et al., ACL 2018, pp. 1383–1392) | jina/HTML |
| S4 | `https://arxiv.org/abs/2511.04703` + `/html/2511.04703v1` | 200 / 200 | Measuring what Matters: Construct Validity in Large Language Model Benchmarks (Bean et al.; 2025-11-03) | arXiv API + HTML |
| S5 | `https://arxiv.org/abs/2311.18807` | 200 | Pre-registration for Predictive Modeling (Hofman, Chatzimparmpas, Sharma, Watts, Hullman; 2023-11-30) | arXiv API |
| S6 | `https://arxiv.org/abs/2512.21326` | 200 | Measuring all the noises of LLM Evals (Sida Wang; 2025-12-24) | arXiv API |
| S7 | `https://statsforevals.com/` | 200 (`curl -L`, browser UA; bare `curl` → 406) | Statistics for LLM Evals — "A Living Reference · evalstats Project" (Ian Arawjo; "Last updated: August 2026") | native HTML |
| S8 | `https://arxiv.org/abs/2409.19839` | 200 | ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities (Karger et al.; 2024-09-30) | arXiv API |
| S9 | `https://forecastingresearch.substack.com/p/introducing-the-brier-index` | 200 | Making Forecasting Scores Easier to Interpret: Introducing the Brier Index (Forecasting Research Institute, 2026-03-04) | native HTML |
| S10 | `https://neurips.cc/public/guides/PaperChecklist` | 200 | NeurIPS Paper Checklist Guidelines (item 7) | native HTML |
| S11 | `https://openreview.net/forum?id=YhZ2PY2nZa` | 200 (content **not retrievable**: "Verifying your browser" interstitial) | — | native HTML (blocked) |
| S12 | `https://github.com/ggml-org/llama.cpp/issues/7052` | 200 (+ API) | Non-deterministic output of the llama.cpp server when using multiple slots | GitHub API (issue + comments) |
| S13 | `https://github.com/ggml-org/llama.cpp/pull/6835` | 200 | Server: fix seed for multiple slots | GitHub API (PR) |
| S14 | `https://github.com/ggml-org/llama.cpp/pull/6950` | 200 | Server: add test for num slots, fails on master | GitHub API (PR) |
| S15 | `https://github.com/ggml-org/llama.cpp/issues/2838` | 200 | CUDA non-determinism on identical requests | GitHub API (issue) |
| S16 | `https://github.com/ggml-org/llama.cpp/pull/22224` | 200 | server : fix CUDA non-determinism with fixed seed (#2838) | GitHub API (PR) |
| S17 | `https://github.com/ggml-org/llama.cpp/issues/28527` | 200 | Eval bug: Quantized K cache makes deterministic prefix-cache repeats produce different output | GitHub API (issue) |
| S18 | `https://github.com/ggml-org/llama.cpp/issues/28656` | 200 | server: multimodal /embeddings are not deterministic within a batch under the default unified KV cache (CUDA builds) | GitHub API (issue) |
| S19 | `https://github.com/ggml-org/llama.cpp/issues/28111` | 200 | CUDA: mul_mat is not batch-invariant for IQ quants at n=5 and n=8 on SM120 | GitHub API (issue) |
| S20 | `https://github.com/ggml-org/llama.cpp/issues/29002` | 200 | hybrid (LFM2) models: co-batching sequences corrupts the recurrent/short-conv state — greedy output diverges and can stop mid-sentence | GitHub API (issue) |
| S21 | `https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/` | 200 | Defeating Nondeterminism in LLM Inference (Horace He / Thinking Machines Lab, Sep 10 2025) | native HTML (2 reads, lines 1–411) |
| S22 | `https://docs.sglang.io/advanced_features/deterministic_inference.html` | 200 | Deterministic Inference (SGLang docs) | markdown alternate |
| S23 | `https://docs.vllm.ai/en/latest/features/batch_invariance/` | 200 | Batch Invariance (vLLM docs; footer "September 27, 2026") | content-negotiated markdown |
| S24 | `https://github.com/thinking-machines-lab/batch_invariant_ops` | 200 | thinking-machines-lab/batch_invariant_ops (1079 stars, MIT) | GitHub API (repo) |
| S25 | `https://github.com/ggml-org/llama.cpp/pull/21038` | 200 | llama : rotate activations for better quantization (ggerganov, 2026-03-26 → closed 2026-04-26) | GitHub API (PR) |
| S26 | `https://localbench.substack.com/p/kv-cache-quantization-benchmark` | 200 | Gemma 4 and Qwen 3.6 with q8_0 and q4_0 KV cache: KL divergence results (oobabooga, Apr 24 2026) | native HTML |
| S27 | `https://sotaaz.com/post/llamacpp-kv-cache-quantization-bench-en` | 200 | llama.cpp KV Cache Quantization, Measured on One A100 — q8_0 Is Free at 4K and Costs Half Your Decode Speed at 64K (SOTAAZ, 2026-09-15, llama.cpp `69320fe`) | native HTML |
| S28 | `https://particula.tech/blog/kv-cache-quantization-accuracy-loss-benchmarks` | 200 | KV Cache Quantization: What FP8 and q8_0 Cost in Accuracy (Particula Tech, 2026-08-03) | `curl` + tag-strip extraction |
| S29 | `https://arxiv.org/abs/2402.02750` | 200 | KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache (Liu et al.; 2024-02-05) | arXiv API |
| S30 | `https://arxiv.org/abs/2511.18643` | 200 | Kitty: Accurate and Efficient 2-bit KV Cache Quantization with Dynamic Channel-wise Precision Boost (Xia et al.; 2025-11-23) | arXiv API |
| S31 | `https://aclanthology.org/2025.emnlp-main.479/` | 200 | Does quantization affect models' performance on long-context tasks? (Mekala et al., EMNLP 2025, pp. 9422–9470) | native HTML |

### Grounding sentences (verbatim, from the fetches above)

**S1** abstract: *"Conceptualizing evaluation questions as having been drawn from an unseen
super-population, we present formulas for analyzing evaluation data, measuring differences
between two models, and planning an evaluation experiment."* Recommendations list (§1):
*"1. Computing standard errors of the mean using the Central Limit Theorem 2. When questions are
drawn in related groups, computing clustered standard errors 3. Reducing variance by resampling
answers and by analyzing next-token probabilities 4. When two models are being compared,
conducting statistical inference on the question-level paired differences, rather than the
population-level summary statistics 5. Using power analysis to determine whether an eval (or a
random subsample) is capable of testing a hypothesis of interest."* Table 4 caption:
*"Analyzing the same data, clustered standard errors can be over 3X larger than naive standard
errors."* (§2.2 real numbers: DROP ratio 3.05, RACE-H 1.10, MGSM 1.88.) §2.1:
*"it is common practice to compute the standard error of the mean by bootstrapping; see, for
instance, the OpenAI evals frameworks. … The Inspect framework correctly computes SE_C.L.T. with
its built-in stderr() metric."* §3.3 heading: *"Don't touch the thermostat!"*
→ **Paired analysis ✔, power analysis ✔, clustered errors ✔, all in the anchor paper.**

**S2** abstract: *"we argue that while CLT-based methods for uncertainty quantification are
appropriate when benchmarks consist of thousands of examples, they fail to provide adequate
uncertainty estimates for LLM evaluations that rely on smaller, highly specialized benchmarks.
In these small-data settings, we demonstrate that CLT-based methods perform very poorly, usually
dramatically underestimating uncertainty (i.e. producing error bars that are too small)."*
→ The anchor's own formula is already contested for n in the tens; r11 is n=64.
(S11 unverified: "featured as a spotlight position paper at ICML" `[unverified]` — OpenReview
served a bot-check page.)

**S3** abstract: *"we survey recent empirical papers published in ACL and TACL during 2017 and
show that while our community assigns great value to experimental results, statistical
significance testing is often ignored or misused."* (Non-parametric tests incl. Wilcoxon
signed-rank and McNemar's are catalogued; `testSignificanceNLP` companion repo.)

**S4** abstract: *"With a team of 29 expert reviewers, we conduct a systematic review of 445 LLM
benchmarks from leading conferences"*; HTML line 130 verbatim: *"At present, only 16.0% of
reviewed benchmarks conducted any statistical testing. Increasing the use of robust statistical
methods for LLM benchmarking is critical."* (HTML line 73: *"Once the responses were scored,
16.0% used uncertainty esti…"*.)

**S5** abstract: *"we propose adapting pre-registration practices from explanatory modeling to
predictive modeling. We discuss current best practices in predictive modeling and their
limitations, introduce a lightweight pre-registration template, and present a qualitative study
with machine learning researchers…"*

**S6** abstract: *"We clearly define and measure three types of noise: prediction noise from
generating different answers on a given question, data noise from sampling questions… To
emphasize relative comparisons and gain statistical power, we propose the all-pairs paired
method… Second, paired prediction noise typically exceeds paired data noise, which means
reducing prediction noise by averaging can significantly increase statistical power."*
→ Directly relevant: for a **paired** design on a stochastic served model, prediction noise
(the lane's non-iid/burst term) is the *dominant* paired noise component.

**S7**: *"It's not right that out of 445 benchmarks, only 16% conducted any statistical tests"*
(links `arxiv.org/abs/2511.04703` = S4); *"In January 2024, I did some deep thinking about this
issue when trying to add error bars to ChainForge's plots… Come 2026, we're still in the same
situation."*; ships `evalstats` (`pip install evalstats`) with `compare_models`/`compare_prompts`
and auto method selection.

**S8** abstract: *"To avoid any possibility of data leakage, ForecastBench is comprised solely of
questions about future events… expert forecasters outperform the top-performing LLM
($p$-value $<0.001$)."*

**S9**: *"The Brier Index, defined as (1 − √Brier score) × 100%, fixes this problem… We've adopted
the Brier Index as the primary metric on the ForecastBench leaderboard."*; addendum (2026-03-05):
*"We made a technical error in the initial post. Specifically, we claimed that 'Because the Brier
Index is a monotonic transformation of the Brier score, it is also strictly proper.' This claim is
incorrect"*. → Brier scoring is established practice for **forecasters' probabilistic predictions**;
the addendum is a live reminder that scoring-rule transformations are easy to get wrong.

**S10**, checklist item 7 verbatim: *"**Experiment Statistical Significance:** Does the paper
report error bars suitably and correctly defined or other appropriate information about the
statistical significance of the experiments?"* plus *"The factors of variability that the error
bars are capturing should be clearly stated"* and *"It is OK to report 1-sigma error bars, but
one should state it."*

**S12** (#7052): API `state=closed`, `state_reason=completed`, `closed_at=2024-06-17T01:06:57Z`,
`labels=[bug-unconfirmed, stale]`, `comments=6`. Reporter body: *"I therefore set the temperature
to 0 and disable other samplers… I get between 5 and 8 unique completion texts when using 8
slots. … When using a single slot, I always get the same answer, but still small variations in
the logits."* @JohannesGaessler (maintainer), 2024-05-03: *"On the latest master the results for
multiple slots are still not 100% deterministic. The problem mainly has to do with the use of
> 1 slots"*. Close comment (bot): *"This issue was closed because it has been inactive for 14
days since being marked as stale."* Last comment @MannyKayy 2026-05-21: *"this issue does exist,
i just encountered it. reopening"*.

**S13** (#6835, closed): *"On master the server currently does not produce reproducible results
for a given seed. The problem is that all slots use a common RNG in `llama_context`. This PR
fixes this by adding a separate RNG to each `llama_sampling_context`."*

**S14** (#6950, closed): *"for a given seed and a varying number of slots the results produced by
the server are **not** deterministic. What I think is happening is that llama.cpp does not produce
bit-for-bit identical results as the batch size is changed."* @compilade: *"This is related to
using a unified KV cache."*

**S15/S16** (#2838 → PR #22224, both closed 2026-04-21): PR body: *"When a seed is explicitly set,
`llama-server` produces non-deterministic output on CUDA backends due to prompt cache reuse
changing the effective batch size between evaluations, which exposes batch-size-dependent FP
ordering in CUDA Flash Attention."*

**S17** (#28527, **open**, created 2026-09-07, `bug-unconfirmed`): *"Quantized K cache makes
deterministic prefix-cache repeats produce different output"*; repro uses
`--cache-type-k iq4_nl --no-kv-offload` and *"Send the same deterministic long-prefix request
three times."* → quantized **K** cache + prefix-cache reuse is a *current* repeat-divergence path.

**S18** (#28656, **open**, 2026-09-09): *"Two identical multimodal inputs sent in a single
`/embeddings` request return different embeddings when the server runs with a unified KV cache,
which is the default when `--parallel` is not given."* Reproduced on CUDA; *"a CPU-only build of
the same commit, where it does **not** occur"*.

**S19** (#28111, **open**, 2026-08-31): *"On SM120, `mul_mat` with IQ quants is not
batch-invariant for `n` of 5 and 8: evaluating `n` columns in one call gives a bitwise different
result from `n` calls of one column. `n` of 1 through 4 agree."*

**S20** (#29002, **open**, 2026-09-16, CPU-only): *"decoding **more than one sequence in the same
ubatch** changes the output… single-sequence decode vs the same prompt co-batched with three
others: **divergent**"* (hybrid LFM2 recurrent state).

**S21**: *"the primary reason nearly all LLM inference endpoints are nondeterministic is that the
load (and thus batch-size) nondeterministically varies!"*; experiment (Qwen3-235B-A22B-Instruct-2507,
1000 completions, temp 0): *"we generate 80 unique completions, with the most common of these
occuring 78 times"*, and *"the completions are actually identical for the first 102 tokens! The
first instance of diverging completions occurs at the 103rd token"*; with batch-invariant kernels
*"all of our 1000 completions are identical"*. Performance: vLLM default 26 s, unoptimized
deterministic vLLM 55 s, +improved attention kernel 42 s. Also quoted: *"Many optimized GPU
kernels… are not batch-invariant"* and *"batch invariance for attention… requires some internal
FlexAttention changes that are not included in our code release."*

**S22**: *"Even with `temperature=0`, standard LLM inference can produce different outputs due to
dynamic batching and varying reduction orders in GPU kernels. … The main source is **varying batch
sizes**."* Flag `--enable-deterministic-inference`, backends FlashInfer / FA3 / Triton; *"Building
on Thinking Machines Lab's batch-invariant operators"*.

**S23**: *"Batch invariance ensures that the output of a model is deterministic and independent of
the batch size or the order of requests in a batch."*; *"Batch invariance is currently in beta"*
(tracking issue #27433); `VLLM_BATCH_INVARIANT=1`; tested-model list includes
**`Qwen/Qwen3-30B-A3B`** (MoE) — the lane's model class.

**S24**: *"Without the upstream PR, we see that out of 1000 random length 100 completions we see
18 unique samples. After the upstream PR, there is only one unique sample."*

**S25** (#21038, merged 2026-04-26): *"Rotate input Q, K, V and store in cache… This works because
Rotation does not affect the dot product of 2 vectors"*; includable opt-out env
`LLAMA_ATTN_ROT_DISABLE`. PPL tables, Qwen3-0.6B BF16, `-f wiki.test.raw --chunks 128` baseline
F16 = 13.6711: **q4_0 62.0161 (master) → 46.2503 (PR)**; Qwen3-8B baseline 7.3203: q4_0 7.6451 →
7.5012; Gemma3 4B baseline 7.6905: q4_0 7.8535 → 7.7928. Commenter @ubergarm on
Qwen3.5-35B-A3B (Q4_0 weights): f16/f16 6.5788, **q4_0/q4_0 master 6.6148, PR 6.5962**.
Commenter @AesSedai on Qwen3.5-9B (mean KLD vs f16/f16): f16/f16 0.000782; **q4_0/q4_0 master
0.007979 → attn-rot 0.005059**; f16 K with q4_0 V: 0.003747.

**S26**: *"q8_0 is practically lossless is wrong for Gemma."* … *"Qwen handles it much better: both
Qwen models stay below KL 0.04 at q8_0, and even q4_0 cache (KL 0.087-0.117) is usable."* …
*"Qwen concentrates nearly all damage in long documents (KL 0.581 at q4_0) and tool calling
(0.086), with other categories staying near zero."* Methodology: ~250k tokens over 6 categories;
KL computed token-by-token against the f16-cache top-40 logprob distributions.

**S27** (llama.cpp `69320fe`, Qwen3-8B Q4_K_M, A100): PPL table — f16 8.319 (4K) … 9.089 (32K);
q8_0 *"inside the error bar at every context length"*; **q4_0 "+0.7% … +1.1% … +0.5%"**;
*"q5_1 prefills 8K tokens at 43 tokens per second"* and the K q8_0 / V q4_0 mix at 63 (CPU
fallback, GPU utilisation 2–4%); decode at 64K: f16 81.6, q8_0 44.7, q4_0 41.2 tok/s.

**S28**: header/description: *"On a 128k needle test, FP8 KV cache fell from 91% to 13% with no
error raised."*; body (extracted): *"KV cache quantization accuracy loss is real,
model-dependent, and invisible to latency"*; *"An independent KL-divergence run at the identical
q8_0 setting measured 0.108 for a Gemma 4 31B dense model against 0.377 for the 26B A4B MoE and
under 0.04 for both Qwen 3.6 models"*; section heading *"The q4_0 cliff your dashboard will not
show"*. Blog (not peer-reviewed) — corroborates S26, do not cite alone.

**S29** abstract: key cache *"should be quantized per-channel"*, value cache *"per-token"*; with
that granularity *"KIVI can enable Llama, Falcon, and Mistral models to maintain almost the same
quality while using 2.6× less peak memory"* → the 2-bit near-lossless claim is **conditional on
per-channel/per-token granularity**; per-tensor uniform quantization is the failure mode.

**S30** abstract: *"While 4-bit KV quantization preserves accuracy, 2-bit often degrades it,
especially on long-context reasoning."*

**S31** abstract: *"8-bit quantization preserves accuracy (~0.8% drop), whereas 4-bit methods lead
to substantial losses, especially for tasks involving long-context inputs (drops of up to 59%)."*
**Important scope limit:** S31 quantizes **model weights** (FP8, GPTQ-int8, AWQ-int4, GPTQ-int4,
BNB-nf4) — *not* the KV cache. It brackets the lane's "below any published safe band" note
(UD-IQ2_XXS) but is **not** direct prior art for a KV-cache confound.

---

## 3. M1 — preregistration + statistical power analysis in LLM/agent evals (2024–2026)

**How standard is it?**

- The *methods* are standard and named canonically as of Nov 2024: paired question-level
  inference, clustered SEs, variance reduction, and **power analysis** are Miller's explicit
  recommendations (S1). Tooling implements them (Inspect `stderr()`, `evalstats`, `bayes_evals`;
  S1, S2, S7).
- The *reporting practice* is still rare: of 445 reviewed LLM benchmarks, **16.0% conducted any
  statistical testing** (S4; corroborated by S7). Dror et al.'s 2017 ACL/TACL audit found the same
  "often ignored or misused" (S3). Conference-level mandates exist — NeurIPS checklist item 7 asks
  precisely the error-bar question (S10) — but a checklist item is not a preregistration.
- **Preregistration as a *filed* practice exists only as a proposal in ML/predictive modeling**
  (S5: a "lightweight pre-registration template" + qualitative study, not a deployed norm). I found
  **no** in-session source reporting a *hashed* preregistration bundle whose sha256 is recorded
  before the run, nor any LLM eval that scores its own probabilistic predictions with a Brier score.
- **Brier scoring** is established practice for *forecasters'* probabilistic predictions (S8, S9),
  in a benchmark where the scoring subject is the model/human, not the experimenter. Applying
  Brier to the *experimenter's own* preregistered predictions is a step outside the found evidence.
- **Relevant to r11's paired design:** S6 shows that in paired analysis the **prediction-noise**
  component (different answers on the same question) typically *exceeds* data noise — i.e. on a
  stochastic local server, pairing does not remove the dominant noise term unless prediction noise
  is averaged. That is exactly the channel r11's non-iid threat uses (§8 of the plan).

**Verdict (M1):** components **KNOWN**; the *composition* as a lane-operated routine is
**INCREMENTAL**; no basis for a **NOVEL** claim.

| Sub-claim | Status | Basis |
|---|---|---|
| Paired per-item analysis of eval differences | **KNOWN** | S1 rec. 4; S6 "all-pairs paired method" |
| Clustered/robust SEs for non-independent items | **KNOWN** | S1 §2.2 (3.05× on DROP) |
| Pre-run power analysis / MDE targeting | **KNOWN** | S1 rec. 5; S2; S7 |
| Filed preregistration in LLM evals | **INCREMENTAL** (proposed for ML at S5; no deployed eval instance found) | S5; absence of finding across queries 9–10, 16 |
| Hashed prereg bundle + ordering proof (hash-then-run commitment) | **INCREMENTAL** — standard in registered-report/OSF practice, no eval-literature instance found | S5 (template only) |
| Brier-scored *self*-predictions + mechanical verdict rule | **INCREMENTAL** — Brier is standard for forecasters (S8, S9); self-scoring not found | S8, S9 |
| Freshness argument: "this makes our eval rigorous" | **must be weakened** | S2 says CLT-based CIs are anti-conservative at n ≪ a few hundred; n=64 is inside that zone |

---

## 4. M2 — non-iid sampling from local servers (llama.cpp #7052 and current status)

**#7052 current state (fetched today).** `state=closed`, `state_reason=completed`,
`closed_at=2024-06-17`, `labels=[bug-unconfirmed, stale]` (S12). It was closed by the **stale bot**
after 14 days of inactivity — *not* fixed. A 2026-05-21 comment says *"this issue does exist, i
just encountered it. reopening"*; GitHub state is still `closed` (the comment is intent, not a
state change). This confirms round 10's flag (`r10-scout-wiki.md:11`) and means the corpus sentence
"reopened 2026-05-21" is wrong about GitHub state (corpus correction already requested there).

**What was actually fixed, and what was not.**

- Fixed: shared RNG across slots (S13, PR #6835) — *"all slots use a common RNG in
  `llama_context`"*.
- Not fixed, documented at the time: varying slot count / batch size changes results bit-for-bit
  (S14, PR #6950) — *"does not produce bit-for-bit identical results as the batch size is
  changed"*; @compilade ties it to *"a unified KV cache."*
- Fixed later, narrow scope: CUDA non-determinism caused by prompt-cache reuse changing effective
  batch size (S15 → S16, Apr 2026).

**2026 state: still open in this class, with four open issues fetched today.**

| Issue | State | Date | Mechanism |
|---|---|---|---|
| #28527 | **open** | 2026-09-07 | quantized **K** cache + prefix-cache repeats → different output (S17) |
| #28656 | **open** | 2026-09-09 | unified KV cache (the `--parallel`-absent default) → non-deterministic `/embeddings` within a batch; CUDA-only (S18) |
| #28111 | **open** | 2026-08-31 | CUDA `mul_mat` **not batch-invariant for IQ quants** at n=5, 8, SM120 (S19) |
| #29002 | **open** | 2026-09-16 | hybrid models: co-batching corrupts recurrent state, CPU-only, greedy divergence (S20) |

**External/industry state (2025–2026).** Thinking Machines Lab diagnosed the general mechanism —
not concurrency, but **lack of batch invariance** + varying load (S21) — and shipped batch-invariant
kernels (S24); vLLM has a **beta** `VLLM_BATCH_INVARIANT=1` with `Qwen/Qwen3-30B-A3B` on its
validated list (S23), and SGLang exposes `--enable-deterministic-inference` (S22). Both build on
S24. **None of this is a llama.cpp feature:** my title-scoped repo search (`batch invariant`, 78
hits) surfaced only *bugs about* non-invariance (S19 etc.); no shipped llama.cpp flag or doc was
found. The lane's queue note "control flags `-np 1`, fixed `-b`/`-ub`" (README:100) remains the
only llama.cpp-side mitigation and is **not equivalent** to batch invariance [moderate].

**Verdict (M2):** the r7 finding is a **KNOWN phenomenon — genuine replication**, exactly as
round 9 priced it (`corpus/knowledge/eval-prior-art-calibration.md:23`,
`round9-fleet/prior-art.md:34`, `:109`). But three wording corrections are required:
1. #7052 is **stale-closed, not resolved**; cite it as *unfixed/unconfirmed* (`bug-unconfirmed`).
2. The closest analogue to the lane's stack in 2026 is **#28527** (quantized K cache + prefix cache),
   not #7052 (8 slots, temp 0, H100) — the lane runs `--cache-type-k/v q4_0`, `--parallel 2`.
3. The phenomenon is **solved elsewhere (vLLM/SGLang/TM), unsolved in llama.cpp** — so "our server
   is non-deterministic" is a *known infrastructure property*, not a lane contribution, and the
   lane's countermeasures (pairing, pid-parity counterbalance, pre-cell filler) are
   **design mitigations that reduce, not remove, the threat** (S6 says the paired dominant term is
   prediction noise; S21 shows temp-0 completions diverge after ~100 tokens).

---

## 5. M3 — quantized-KV effects on measured accuracy

**Does q4_0 KV change task-level behaviour in a way that would confound a severity dose? Yes.**

- **Direct llama.cpp PPL/KLD evidence (primary, S25).** On Qwen3-8B, q4_0 KV raises wikitext PPL
  7.3203 → 7.6451 (master), reduced to 7.5012 by the attention-rotation PR — which is applied
  automatically in current llama.cpp (S26 refers to "the recently added TurboQuant-inspired
  attention rotation that llama.cpp applies automatically"; S25 was closed 2026-04-26 with env
  opt-out `LLAMA_ATTN_ROT_DISABLE`). So **the lane's build is one of the two regimes depending on
  when the server binary was built**. On a Qwen3.5-9B the mean
  KLD against the f16-cache reference is **0.007979 for q4_0/q4_0 vs 0.000782 for f16/f16** (~10×),
  i.e. quantized KV measurably moves the logit distribution, not just memory.
- **Qwen-family category pattern (S26, S28).** q8_0 is near-lossless for Qwen; **q4_0 is "usable"
  but concentrates damage in long documents (KL 0.581) and tool calling (0.086)**, other categories
  ≈ 0. That is precisely the regime a multi-turn state-tracking probe exercises.
- **Granularity/2-bit context (S29, S30).** 2-bit is lossy unless per-channel/per-token (S29);
  S30: *"4-bit KV quantization preserves accuracy, 2-bit often degrades it, especially on
  long-context reasoning."* → q4_0 is the *first lossy* rung; q8_0 is the safe default (S27: "inside
  the error bar at every context length"; S25 tables: q8_0 within +0.03% of f16 on Gemma3 4B and
  Qwen3.5 4B, −0.04% on Qwen3 8B, but +1.76% on the tiny Qwen3 0.6B — so "q8_0 is free" is
  model-size-dependent, not universal).
- **Adjacent, not direct (S31).** The "up to 59%" long-context drop is **weight** quantization
  (FP8/GPTQ/AWQ/BNB), 4-bit; useful only as the lane's sub-bit weight band context.
- **Second-order effect worth recording (S17).** Quantized K cache + prefix-cache reuse is an
  **open** repeat-divergence path in llama.cpp. So KV quantization is not only a *level shift* on
  accuracy; under prefix caching it can also inject **run-to-run variance** — an extra, unpriced
  noise term for any design that relies on replayed identical prompts.

**Verdict (M3):** **KNOWN and documented**, with an important structural reading for r11 — the
q4_0 KV stack is a **common-mode confound**: it is present in *both* cells, so it does not bias a
paired difference, but it (a) sets the accuracy/severity ceiling, (b) does not drift with context
(S27: q4_0 "does not drift with context"), and (c) may add variance if prefix caching is active
(S17). Therefore **absolute `nwrong` levels are stack-specific and non-transferable**; only the
paired contrast is defensible — which is exactly what the plan's §3 descriptor discipline already
requires.

---

## 6. Verdict table

| ID | Method claim under test | Status | Anchor sources | Strongest counter-evidence / caveat |
|---|---|---|---|---|
| **M1a** | Paired per-pid analysis + power-targeted n (MDE d=0.35) | **KNOWN** | S1 (rec. 4–5), S6, S7 | S2: CLT-based CIs under-cover at n ≪ few hundred → r11's own CI/t-test at n=64 sits in the contested zone; sign test is the right robustness partner (plan already includes it) |
| **M1b** | Filed preregistration of the design (hashed bundle + ordering log) | **INCREMENTAL** | S5 (proposal/template) | No LLM-eval instance found; **filing is rare, not novel in science** (registered reports) |
| **M1c** | Brier-scored probabilistic self-predictions + mechanical verdict rule | **INCREMENTAL** | S8, S9 | Brier is standard for forecasters; self-scoring found nowhere in-session |
| **M1d** | "Preregistered LLM eval" as a novelty claim | **NOT SUPPORTED** | S4 (16.0% do any stats at all), S3 | Would collide with S5 and with the generic registered-report lineage |
| **M2** | r7 non-iid draw finding = direct replication of llama.cpp #7052 | **KNOWN (replication confirmed)** | S12, S13, S14, S21 | #7052 **stale-closed, not fixed**; 4 **open** 2026 analogues (S17–S20); no llama.cpp determinism flag; TM shows 80/1000 unique at temp 0 (S21) |
| **M2b** | The lane's countermeasures (pairing, counterbalance, fillers) neutralize non-iid | **DESIGN MITIGATION, not a fix** | S6, S21 | Paired prediction noise dominates (S6); divergence can appear ~100 tokens in (S21); `--parallel 2` + q4_0 KV + prefix cache keeps S17-style paths in scope |
| **M3** | q4_0 KV cache is a known confound for task-level accuracy/severity | **KNOWN** | S25 (KLD 0.008 vs 0.0008), S26 (KL 0.581 long docs), S27 (+0.5–1.1% PPL), S29/S30, S28 | Common-mode across cells → paired diff OK, **absolute levels not transferable**; S17 adds a variance path; the 59% figure (S31) is weight-quant, not KV |

---

## 7. What this means for round-11 claim wording

Phrasings that **overclaim** given S1–S31, and the defensible rewrite:

| Do NOT write | Why (source) | Write instead |
|---|---|---|
| "preregistered LLM evaluation" as a novel contribution | M1b/M1d: preregistration is a published proposal (S5) and eval statistics are canon (S1, S2, S7) | "preregistered **lane-operated probe**; the preregistration is a process commitment recorded by hash, not a methodological contribution" |
| "first powered/rigorous eval on this server" | S1/S2/S7 predate and define the method | "powered to the preregistered MDE d=0.35 at n=64; method follows Miller (S1) with the small-n caveat of Bowyer et al. (S2)" |
| "we fix / control non-determinism" | M2b: no llama.cpp determinism feature exists; TM/vLLM/SGLang fixes are elsewhere (S21–S24) | "we **mitigate** non-iid contamination by per-pid pairing, pid-parity counterbalanced cell order and a filler before each cell; the server remains non-deterministic (S12, S17–S20)" |
| "a direct replication of issue #7052" (unqualified) | #7052 is stale-closed/unconfirmed (S12); the lane's stack matches #28527 better (S17) | "a replication of the publicly reported class (llama.cpp #7052, stale-closed/unconfirmed) on a different stack; the closest live analogue is #28527 (quantized K cache + prefix cache)" |
| "severity dose D under q4_0 KV" as a stack-transferable effect size | M3: q4_0 KV sets the ceiling, is model/category-dependent (S25, S26, S27), and there are two build regimes around PR #21038 | "paired mean severity difference **under this exact stack** (single served unit: Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS, q4_0 K/V, `--kv-unified`, `--parallel 2`, custom template), n=64" |
| "error bars" alone as evidence of rigor | S10 requires stating *what variability the bars capture*; S1/S2 disagree on the estimator at small n | state the estimator explicitly (paired t on 64 per-pid differences, df=63; exact sign test as the assumption-light partner) and name the captured variability (problem draw + non-iid request noise) |
| "Brier score validates our predictions" as a scoring-rule claim | S9 addendum: monotone transforms of Brier are **not** proper; properness arguments are easy to botch | "Brier score of 3 preregistered probabilistic predictions (a descriptive self-scoring device), not a proper-scoring-rule guarantee" |
| "non-iid ⇒ our p-values are conservative" | S6: **prediction noise usually exceeds data noise** in paired designs — the direction of the bias needs stating, not hand-waving | "p-values are **anti-conservative** under positive serial dependence; the exact sign test is reported as the lower-assumption check" |

Also required in every derived claim (plan §3, confirmed as externally necessary by M3): the
**single-served-unit qualifier** and the **no-cross-model-generalization** clause.

---

## 8. Residual uncertainty / defects (nothing here blocks the main run)

- **GAP:** no in-session source states whether *any* LLM-eval paper files a hashed preregistration
  bundle. Absence is bounded by queries 9–10 and 16 only — treat M1b as "incremental, possibly
  merely rare", not "unprecedented".
- **GAP:** `openreview.net/forum?id=YhZ2PY2nZa` (S11) is unreachable in-session (bot check), so the
  "ICML 2025 spotlight" status of S2 is `[unverified]`.
- **Cite-with-care:** S26/S28 are vendor/blog measurements (not peer-reviewed); they are used only
  to corroborate the primary llama.cpp PPL/KLD numbers in S25 and the peer-reviewed framing in
  S30/S31.
- **Stack-specific finding worth pinning in the descriptors:** PR #21038 (attention rotation for KV
  quantization) was closed 2026-04-26 and is described by S26 as applied automatically, with an env
  opt-out (`LLAMA_ATTN_ROT_DISABLE`); the lane's run records server argv, so the
  regime is recoverable — but any cross-round comparison of `nwrong` levels against r8/r9 must check
  whether those runs predate the merge.
- **Non-blocking risk to record in `analysis_r11.md`:** if the served `llama-server` has prompt
  caching enabled (server default) while K is q4_0, the S17 mechanism (quantized K + prefix-cache
  repeats) applies to the identical filler prompts and repeated system prefixes; the `descriptors`
  record should be read post-run for the relevant flags before any "identical requests produced
  identical outputs" statement is made.