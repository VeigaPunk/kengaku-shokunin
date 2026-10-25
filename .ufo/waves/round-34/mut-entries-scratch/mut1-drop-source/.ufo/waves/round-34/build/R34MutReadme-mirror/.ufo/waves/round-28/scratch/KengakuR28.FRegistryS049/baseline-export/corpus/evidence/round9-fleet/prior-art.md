# Prior-art calibration — kengaku lane round 9 (novelty axis)

Scope: novelty calibration of 4 local findings measured on Qwen3-Coder-30B-A3B UD-IQ2_XXS
(`/tmp/bench-r8/results.jsonl`, SUMMARY in `/tmp/bench-r8/run.log`). Read-only; no endpoint calls.
Method: ~20 `web_search` queries + direct fetches of every cited primary source (arXiv API, ACL
Anthology, ICLR proceedings, vLLM docs, GitHub API). Every URL below was fetched in-session and the
quoted numbers come from that fetch. Search synthesis prose was **not** trusted; only fetched primaries.
Local numbers are grounded in the round-8 SUMMARY block (`run.log:-15`) and `corpus/evidence/round8-horizon/critic-defects.md`.

Adversarial default: a local finding is `known` until a source *fails* to cover it.

---

## 1. Finding → closest public work → relation

| # | Local finding (round-8 numbers) | Closest public work (venue/year, URL) | Relation | One-line justification |
|---|---|---|---|---|
| 1 | INC 7/10 vs CKPT 1/10 vs MONO 0/10 → advantage read as SELF-COPY SCAFFOLD, not horizon | **LLMs Get Lost In Multi-Turn Conversation** — Laban et al., ICLR 2026 (<https://proceedings.iclr.cc/paper_files/paper/2026/file/59f6421e64707225fdf5b28840679a07-Paper-Conference.pdf>; <https://arxiv.org/abs/2505.06120>) | partially covered | They report models "rely too heavily on previous (incorrect) answer attempts" and that SNOWBALL (cumulative re-statement of prior context) buys +15–20% yet still trails single-turn FULL — i.e. self-repetition is a scaffold, not a capability restore. |
| 1 | same | **Re-Reading Improves Reasoning (Re²)** — Xu et al. 2023 (<https://arxiv.org/abs/2309.06275>) | anticipated | Feeding context twice ("re-reading", giving a bidirectional pass) consistently improves reasoning → the *re-read of own/prior text* is a known gain channel. |
| 1 | same | **Recitation-Augmented Language Models (RECITE)** — Sun et al., ICLR 2023 (<https://arxiv.org/abs/2210.01296>) | partially covered | "Recite first, then answer" improves accuracy; supports copy/restate-as-computation. (Their tasks are CBQA, not state tracking — link is analogical.) |
| 1 | same | **In-context Learning and Induction Heads** — Olsson et al. 2022 (<https://arxiv.org/abs/2209.11895>; <https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html>) | anticipated | Identifies an explicit *copy-and-complete* circuit that lets transformers re-emit earlier context without recomputing it — the mechanism the lane's reading assumes. |
| 1 | same | **Faith and Fate: Limits of Transformers on Compositionality** — Dziri et al., NeurIPS 2023 (<https://arxiv.org/abs/2305.18654>) | anticipated | Transformers solve multi-step composition as "linearized subgraph matching", performance decaying with complexity → latent chaining is the weak path. |
| 1 | same | **Least-to-Most Prompting** — Zhou et al. 2022 (<https://arxiv.org/abs/2205.10625>) | contradicts (mild) | Decomposed, sequentially-conditioned subproblem solving *does* beat single-pass CoT (SCAN 16%→99%), so "incremental > monolithic" is already the published direction; our probe re-attributes the gap to copying rather than planning. |
| 2 | hint ("correct, don't propagate") = zero change: corrupt 3/8 both, clean 6/8 both | **LLMs Cannot Self-Correct Reasoning Yet** — Huang et al., ICLR 2024 (<https://arxiv.org/abs/2310.01798>) | known | Intrinsic self-correction without external feedback does not help and "at times, performance even degrades"; a bare "check/correct" prompt is a known non-remedy. |
| 2 | same | **Measuring Faithfulness in CoT** — Lanham et al. 2023 (<https://arxiv.org/abs/2307.13702>) | known | Their "adding mistakes"/intervention protocol is exactly the family our corrupt-prior-state cell belongs to: models *do* often condition on injected errors, with large task variation. |
| 2 | same | **RefuteBench** — Yan et al., Findings of ACL 2024 (<https://aclanthology.org/2024.findings-acl.818/>) | partially covered | LLMs are "stubborn" to refuting feedback and roll back to their own answers as turns grow; but a *recall-and-repeat* prompt **does** help there → instruction-level hints are not universally inert. |
| 2 | same | **LLMs Get Lost…** (App. G) — Laban et al., ICLR 2026 (URL above) | known | They measured the closest thing to our hint: a system-prompt hint that the conversation is underspecified → **+1%**, "does not effectively help". |
| 3 | vacuously-satisfied late rule → C-benign 1/4; binding version C-conflict 4/4; no-rule C-norule 4/4 | **FollowBench** — Jiang et al., ACL Findings 2024 (<https://arxiv.org/abs/2310.20410>) | known (general form) | Hard Satisfaction Rate "collapses steeply as constraints accumulate" (constraint forgetting) — extra late rules costing performance is published. |
| 3 | same | **Multi-IF** — He et al. 2024 (<https://arxiv.org/abs/2410.15553>) | known (general form) | All 14 models fail more with each added turn (o1-preview 0.877→0.707); a rule that arrives late is measurably costly. |
| 3 | same | **MultiChallenge** — Scale Labs, ACL Findings 2025 (<https://arxiv.org/abs/2501.17399>; <https://aclanthology.org/2025.findings-acl.958/>) | partially covered | Has a "reliable versioned editing" axis (distinguish active from discarded versions without regressions) — nearest published analogue to over-repair. |
| 3 | same | **When Models Edit Too Much: On the Fidelity of Minimal Code Edits** — Zhu et al. 2026 (<https://arxiv.org/abs/2609.04061>) | partially covered | Names and measures "over-editing": high Pass@1 coexists with unnecessarily large edits; a preservation instruction reduces excess edit distance 0.195→0.131. Same failure class, code domain. |
| 3 | same | **IH-Benchmark** — McCauley et al. 2026 (<https://arxiv.org/abs/2607.25987>) | anticipated (narrow) | Conflict-centered hierarchy benchmark; most revealing failures are *subtle* rather than overt (injected disclaimers, small distortions) — close to "rule that doesn't obviously bind still changes behaviour". |
| 3 | same | **The Instruction Hierarchy** — Wallace et al. 2024 (<https://arxiv.org/abs/2404.13208>) | not covered | Covers conflicting instruction *priority*, not a redundant/satisfied constraint. |
| 4 | non-iid draws: lag-1 autocorr +0.26/+0.32, 5–10-request burst horizon, near-deterministic same-seed replay, interleaving changes output | **llama.cpp issue #7052 "Non-deterministic output of the llama.cpp server when using multiple slots"** (2024-05-03; reopened 2026-05-21) (<https://github.com/ggml-org/llama.cpp/issues/7052>) | **known — direct replication** | Reporter sends the *same prompt, seed=1234, temperature=0* to 8 slots on an H100 and gets **5–8 unique completions**; single slot is deterministic; maintainer: multi-slot results "still not 100% deterministic". This *is* our finding, published two years earlier. |
| 4 | same | **Defeating Nondeterminism in LLM Inference** — Thinking Machines Lab, Sep 2025 (<https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/>) | known | "The primary reason nearly all LLM inference endpoints are nondeterministic is that the load (and thus batch-size) nondeterministically varies" — non-batch-invariant kernels + load = per-user nondeterminism. |
| 4 | same | **vLLM docs — Batch Invariance** (beta) (<https://docs.vllm.ai/en/latest/features/batch_invariance/>) | known | Shipping feature (`VLLM_BATCH_INVARIANT=1`) exists precisely because default outputs depend on batch size/order; Qwen3-30B-A3B is a validated model. |
| 4 | same | **Measuring all the noises of LLM Evals** — Wang 2025 (<https://arxiv.org/abs/2512.21326>) | partially covered | Formalises prediction noise vs data noise and paired analysis — the *statistical* half of our ESS argument, but over questions, not over consecutive requests. |
| 4 | same | **Examining the robustness of LLM evaluation to the distributional assumptions of benchmarks** — Siska et al., ACL 2024 (<https://aclanthology.org/2024.acl-long.560/>) | anticipated | Cross-item correlation is non-random and changes model rankings (i.e. nominal N ≠ effective N) — but they model *item* clustering, not server-side temporal bursts. |
| 4 | same | **τ-bench** — Yao et al. 2024 (<https://arxiv.org/abs/2406.12045>) | anticipated | Introduces `pass^k` for "reliability of agent behavior over multiple trials" (pass^8 <25% retail): repeated draws of the same task are the measurement unit, not a nuisance. |
| — | quantisation backdrop for all findings (~2-bit UD-IQ2_XXS) | **Quantization Hurts Reasoning?** — Liu et al. 2025 (<https://arxiv.org/abs/2504.04823>); **Does quantization affect models' performance on long-context tasks?** — Mekala et al., EMNLP 2025 (<https://aclanthology.org/2025.emnlp-main.479/>); **Trade-Offs: Quantization, Task Difficulty, Model Size** — Lee et al. 2024 (<https://arxiv.org/abs/2409.11055>) | known | W8A8/W4A16 ≈ lossless (≤0.8% drop) while 4-bit loses up to 59% and "quantized models often struggle with instruction-following"; sub-3-bit is outside any published safe band → every cell here is a sub-3-bit observation, not a model-capability measurement. |

---

## 2. Named public benchmarks that already measure findings 1 and 3

| Local finding | Existing public benchmark (URL) | What it already covers | What our probe adds beyond it |
|---|---|---|---|
| **1** — incremental per-turn state tracking | **MemoryAgentBench** (<https://arxiv.org/abs/2507.05257>) | Incremental multi-turn information accumulation; accurate retrieval, test-time learning, long-range understanding, selective forgetting. | Nothing on *emission granularity*. Adds: same problems/seeds run under INC vs sparse-checkpoint vs monolithic, i.e. output-frequency as the manipulated variable. |
| **1** | **MultiChallenge** (<https://arxiv.org/abs/2501.17399>) | ≤10-turn trajectories, instruction retention, versioned editing, self-coherence, graded by rubric judge. | Ours is *exact-match programmatic* grading on a synthetic state machine (no judge), and it isolates the transcript-shape confound. |
| **1** | **BABILong** (<https://arxiv.org/abs/2406.10149>) | bAbI **state-tracking** tasks (object position/count/list updates) hidden in long noise; perf "declines sharply with increased reasoning complexity"; models use only 10–20% of context. | Closest public state-tracking suite; ours is short-context, so it probes maintenance *between* emissions rather than retrieval over noise. |
| **1** | **τ-bench** (<https://arxiv.org/abs/2406.12045>) | Multi-turn tool/rule interaction graded on final DB state; `pass^k` reliability. | `pass^k` is the right unit for our replay issue; we add a *lag-1 autocorrelation estimate* of the serving stack itself, which τ-bench does not measure. |
| **3** — late-arriving rule, already satisfied | **Multi-IF** (<https://arxiv.org/abs/2410.15553>) | Constraint sets grow across 3 turns; per-turn accuracy decay quantified for 14 LLMs. | Adds: an *exactly-matched triple* of identical fabricated transcripts (binding rule / vacuously-satisfied rule / no rule) isolating rule-integration from transcript-shape cost. |
| **3** | **FollowBench** (<https://arxiv.org/abs/2310.20410>) | Multi-level incremental constraint injection + HSR. | FollowBench's constraints are all *binding*; ours includes the **vacuous** arm and a no-rule control. |
| **3** | **MultiChallenge** "reliable versioned editing" (<https://aclanthology.org/2025.findings-acl.958/>) | Distinguish active vs discarded versions, avoid regressions. | Same failure class, but graded by judge on free-form editing; ours is a 4-row table with tuple-exact scoring. |
| **3** | **IH-Benchmark** (<https://arxiv.org/abs/2607.25987>) | Conflict detection/priority, subtle-vs-overt failure split. | Ours has **no conflict at all** — the rule is redundant; no public suite I found tests a *satisfied* rule as a distractor. |

Net: no public benchmark measures the *emission-granularity* ablation (finding 1) or the *vacuous-rule*
arm (finding 3). That is a genuine gap — but see §3: our n makes the second one unmeasurable anyway.

---

## 3. Verdict per finding (adversarial)

| # | Claim | Novelty grade | Phenomenon grade | Should the lane stop claiming it as a contribution? |
|---|---|---|---|---|
| 1 | INC ≫ CKPT ≫ MONO is a **self-copy scaffold**, not horizon | **incremental** (protocol ablation over emission frequency) | **known** — Laban ICLR 2026 (SNOWBALL +15–20%, over-reliance on prior answers), Re², RECITE, induction heads, Dziri | **Yes, as a discovery.** Keep only as a *controlled replication* and as the design rationale for the checkpoint arm. Note the lane's own critic already classifies INC-vs-MONO as a confound (`corpus/evidence/round8-horizon/critic-defects.md:2`; fix pre-registered at `horizon.py:4`). |
| 2 | Prompt hint ⇒ **zero** change in error recovery (3/8 = 3/8) | **nil** | **known** — Huang ICLR 2024; Laban App. G (+1%); Lanham; RefuteBench (where a repeat-prompt *did* help) | **Yes, stop claiming.** At n=8 an exact null matches the published expectation; it is a replication, not evidence. Adversarial addendum: identical 3/8 and 6/8 counts are also what a *deterministic same-seed replay* would produce [INFERENCE], so this cell must not be over-read even as a replication. |
| 3 | A **vacuously-satisfied** late rule breaks a correct state (1/4 vs 4/4 vs 4/4) | **incremental (low)** — the vacuous arm appears unmeasured publicly | **known (general form)** — FollowBench, Multi-IF, MultiChallenge, Huang, Zhu et al. over-editing | **Yes — and the numbers do not support it.** Fisher exact 1/4 vs 4/4 ⇒ p≈0.143 *even assuming iid draws* (`eval` cmd, §5); the lane's own r7 work says draws are not iid, so the true type-I rate is worse. This claim is **not publishable at n=4**. Re-run ≥12 seeds before restating. |
| 4 | Draws are non-iid; interleaving perturbs a replay (lag-1 +0.26/+0.32, 5–10-request horizon) | **incremental** (the temporal/burst *quantification*; no source found reporting lag-1 autocorrelation of a served model's consecutive outputs) | **known — direct replication** — llama.cpp #7052 (5–8 unique of 8 slots at temp 0, seed fixed), Thinking Machines, vLLM batch-invariance docs | **Yes, as a contribution.** Keep as a mandatory methodological caveat and cite #7052; the *only* defensible local novelty is the burst-horizon number on this specific GGUF/llama.cpp build. |

Cross-cutting: every finding is measured at UD-IQ2_XXS, below any published safe band
(Liu et al. 2504.04823: W8A8/W4A16 lossless, lower bits "significant accuracy risks"; Mekala et al.:
4-bit up to −59%; Lee et al. 2409.11055: quantized models "often struggle with instruction-following").
So all four are **serving-stack + sub-3-bit observations**, not statements about Qwen3-Coder-30B-A3B.

---

## 4. ≤3 public sources to digest into the corpus next round

| # | Source (URL) | Why |
|---|---|---|
| 1 | Laban et al., *LLMs Get Lost In Multi-Turn Conversation*, ICLR 2026 — <https://arxiv.org/abs/2505.06120> (camera-ready: <https://proceedings.iclr.cc/paper_files/paper/2026/file/59f6421e64707225fdf5b28840679a07-Paper-Conference.pdf>) | Highest overlap with finding 1 & 2. Directly supplies two controls the lane lacks: RECAP/SNOWBALL (repeat-the-prior-content arms) and the aptitude-vs-unreliability decomposition (percentile metrics), plus the system-prompt-hint null and the temperature ablation. |
| 2 | Lanham et al., *Measuring Faithfulness in Chain-of-Thought Reasoning* — <https://arxiv.org/abs/2307.13702> | Methodological template for probe B: the "adding mistakes" intervention family and the framing (does the model condition on the injected text?) that upgrades B from a bespoke cell to a replication-with-a-twist. |
| 3 | llama.cpp issue #7052 — <https://github.com/ggml-org/llama.cpp/issues/7052> (pair with <https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/>) | Falsifies any residual novelty claim on finding 4 with a two-year-old public repro and tells the lane exactly which serving flags (`-np 1`, fixed `-b`/`-ub`) control it — i.e. what a defensible experimental unit looks like. |

---

## 5. Verifying commands

- Round-8 SUMMARY, cited numerics: `read /home/vgpnk/projects/shokunin/kengaku-shokunin/corpus/evidence/round8-horizon/run.log:-15` → `A-INC: 7/10 … C-benign: 1/4 … C-norule: 4/4`.
- Self-copy-scaffold wording + pre-registered fix: `grep "SELF-COPY|scaffold" corpus/evidence/round8-horizon/` → matches at `critic-defects.md:2`, `critic-defects.md:50`, `horizon.py:4`.
- Significance of the C contrast (Fisher exact, iid assumption, one-sided):
  ```
  A-INC 7/10 vs A-MONO 0/10   p=0.0031
  A-INC 7/10 vs A-CKPT 1/10   p=0.0198
  C-benign 1/4 vs C-norule 4/4 p=0.1429
  C-benign 1/4 vs C-conflict 4/4 p=0.1429
  B-corrupt plain 3/8 vs hint 3/8 p=1.0000
  ```
  These are **upper bounds on significance** (they assume iid draws; the lane has measured otherwise).
- Every table URL was fetched in-session via arXiv API / ACL Anthology / ICLR proceedings / vLLM docs / GitHub API. No search-synthesis prose is cited.

---

## Confidence

| Headline claim | Grade | Reason |
|---|---|---|
| Finding 4 is a **direct replication** of a publicly documented phenomenon | **high** | Primary repro exists verbatim (llama.cpp #7052: same prompt+seed, temp 0, 8 slots → 5–8 unique completions; single slot deterministic), corroborated by Thinking Machines Lab and vLLM's shipped batch-invariance feature. |
| Finding 1's *interpretation* (self-copy scaffold) is anticipated, not novel | **high** | Laban ICLR 2026 states models "rely too heavily on previous (incorrect) answer attempts" and prices the repeat-content arm (SNOWBALL +15–20%, still < FULL); Re²/RECITE/induction-heads supply the mechanism. |
| Finding 2 is a known null, not a contribution | **high** | Huang ICLR 2024 abstract ("at times, their performance even degrades") and the closest direct measurement (Laban App. G, hint → +1%) both cover it; our 3/8 = 3/8 adds no information. |
| Finding 3 should **not** be claimed at n=4 | **high** | Arithmetic + Fisher p≈0.143 under the *optimistic* iid assumption, and the lane's own r7 noise work removes that assumption. |
| Finding 1's *protocol ablation* (emission granularity) is not covered by any named benchmark | **medium** | Based on absence of evidence across ~20 searches of the named suites (MemoryAgentBench, MultiChallenge, BABILong, Multi-IF, FollowBench, τ-bench, IH-Benchmark); a differently-named suite could exist — flagged [UNVERIFIED]. |
| Finding 3's *vacuous-rule arm* is unmeasured publicly | **medium** | Same basis: FollowBench/Multi-IF constrain only with binding rules; IH-Benchmark models conflict, not redundancy. Absence of evidence, not proof of absence. |
| Lag-1 autocorrelation / 5–10-request burst horizon as a quantified measurement is locally novel | **low–medium** | No source found reporting lag-1 autocorrelation of a *served* model's consecutive draws (Wang 2512.21326 models question-level noise; Siska et al. ACL 2024 model item clustering). Weak positive: retrieval is search-based, so a negative is weak evidence. |
| All findings are sub-3-bit + serving-stack artefacts, not model-capability claims | **medium–high** | Published quantisation bands (W8A8/W4A16 lossless; 4-bit losses up to 59%; "quantized models often struggle with instruction-following") place UD-IQ2_XXS outside any validated regime; the exact IQ2_XXS behaviour itself is unmeasured publicly [UNVERIFIED]. |