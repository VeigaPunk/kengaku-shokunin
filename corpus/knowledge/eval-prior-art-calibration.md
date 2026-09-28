# Prior-art calibration — how novel are this lane's local eval findings?

**Source basis:** `corpus/evidence/round9-fleet/prior-art.md` (scout L2,
round 9): ~20 `web_search` queries plus in-session fetches of every cited
primary (arXiv API, ACL Anthology, ICLR proceedings, vLLM docs, GitHub API);
search-synthesis prose was not trusted. Local side: round-8 SUMMARY
(`corpus/evidence/round8-horizon/run.log:79-91`) and round-9 replication
(`corpus/knowledge/bench-arena-round9-replication.md`). Adversarial default:
a local finding is `known` until a source *fails* to cover it.

Novelty is one of this lane's two owned axes (`../MISSION.md`); before round 9
the lane had never checked its findings against public literature, so every
"finding" in `corpus/knowledge/bench-arena-*` was implicitly presented as new.
This entry prices them.

## Verdicts

| # | Local finding | Novelty of the *claim* | Phenomenon | Stop claiming as a contribution? |
|---|---|---|---|---|
| 1 | INC 7/10 > CKPT 1/10 ≈ MONO 0/10 → incremental advantage read as **self-copy scaffold**, not planning horizon (r9: 4/8 > 2/8 = 2/8 > 0/8) | **incremental** — the emission-granularity ablation is the new part | **known**: Laban et al., *LLMs Get Lost In Multi-Turn Conversation*, ICLR 2026 (<https://arxiv.org/abs/2505.06120>) reports over-reliance on prior answers and prices the repeat-content arm (SNOWBALL +15–20%, still < single-turn FULL); Re² (<https://arxiv.org/abs/2309.06275>), RECITE (<https://arxiv.org/abs/2210.01296>), induction heads (<https://arxiv.org/abs/2209.11895>), Faith-and-Fate linearized subgraph matching (<https://arxiv.org/abs/2305.18654>) supply the mechanism; least-to-most (<https://arxiv.org/abs/2205.10625>, SCAN 16%→99%) already published "incremental > monolithic" | **Yes, as a discovery.** Keep as a controlled replication and as the design rationale for the checkpoint arm |
| 2 | Inline hint "correct it rather than propagating the error" ⇒ **zero** change (corrupt 3/8 = 3/8, clean 6/8 = 6/8) | **nil** | **known**: Huang et al., *LLMs Cannot Self-Correct Reasoning Yet*, ICLR 2024 (<https://arxiv.org/abs/2310.01798>); Laban App. G measured the closest hint at **+1%**; Lanham et al. "adding mistakes" family (<https://arxiv.org/abs/2307.13702>); RefuteBench (<https://aclanthology.org/2024.findings-acl.818/>) shows a recall-and-repeat prompt *can* help → hints are not universally inert | **Yes.** At n=8 an exact null replicates the published expectation and adds nothing; identical counts are also what near-deterministic replay yields |
| 3 | A **vacuously satisfied** late rule breaks a correct state (benign 0/4 strict vs conflict 4/4 vs norule 4/4) | **incremental (low)** — the vacuous arm appears unmeasured publicly [absence of evidence, ~20 searches] | **known in general form**: FollowBench HSR collapse under constraint accumulation (<https://arxiv.org/abs/2310.20410>); Multi-IF per-turn decay, o1-preview 0.877→0.707 (<https://arxiv.org/abs/2410.15553>); MultiChallenge versioned editing (<https://arxiv.org/abs/2501.17399>); over-editing with a preservation instruction 0.195→0.131 (<https://arxiv.org/abs/2609.04061>); IH-Benchmark subtle failures (<https://arxiv.org/abs/2607.25987>) | **Yes at this n.** Fisher exact 1/4 vs 4/4 → p≈0.143 *even assuming iid*, which this lane has falsified. Re-run ≥12 seeds before restating |
| 4 | Draws are **non-iid** on this server: lag-1 +0.26/+0.32, 5–10-request burst horizon, near-deterministic same-seed replay, interleaving mutates a replay | **incremental** — only the burst/lag-1 *quantification* on this GGUF+llama.cpp build | **known — direct replication**: llama.cpp issue #7052 (<https://github.com/ggml-org/llama.cpp/issues/7052>, 2024-05-03, reopened 2026-05-21) sends the same prompt at seed=1234, temp 0 to 8 slots and gets **5–8 unique completions**; single slot deterministic; maintainer confirms multi-slot is "not 100% deterministic". Corroborated by Thinking Machines, *Defeating Nondeterminism in LLM Inference* (<https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/>) and vLLM's shipped `VLLM_BATCH_INVARIANT=1` (<https://docs.vllm.ai/en/latest/features/batch_invariance/>, Qwen3-30B-A3B validated) | **Yes, as a contribution.** Keep as a mandatory methodological caveat, cited to #7052; #7052 also names the serving flags (`-np 1`, fixed `-b`/`-ub`) that define a defensible experimental unit |

Statistical note: significance figures quoted for the local cells (INC vs MONO
p=0.0031, INC vs CKPT p=0.0198, C contrasts p≈0.1429, B hint p=1.0) are
**upper bounds** — they assume iid draws, which
`bench-arena-round7-noise-n25.md` refutes for this server.

## Benchmark coverage — where a genuine gap remains

| Local instrument | Named public suites that already measure nearby | What is *not* covered publicly |
|---|---|---|
| Probe A (emission granularity) | MemoryAgentBench (<https://arxiv.org/abs/2507.05257>), MultiChallenge (<https://arxiv.org/abs/2501.17399>), BABILong state tracking (<https://arxiv.org/abs/2406.10149>), τ-bench `pass^k` (<https://arxiv.org/abs/2406.12045>), Multi-IF (<https://arxiv.org/abs/2410.15553>) | **No suite ablates output/emission frequency on identical problems and seeds.** Ours does; τ-bench's `pass^k` is the right unit for our replay problem, and our lag-1 estimate of the serving stack is not measured by any of them |
| Probe C (late rule) | Multi-IF, FollowBench, MultiChallenge, IH-Benchmark | **No suite uses a vacuously satisfied rule with a matched binding control and a no-rule control.** All public constraint suites inject *binding* constraints; IH-Benchmark models conflict, not redundancy |
| Probe B (corrupted prior state) | Lanham et al. "adding mistakes" family | Nothing bespoke; B is a replication-with-a-twist and round 8's version did not bind (`bench-arena-round8-horizon.md` §B) |

So the defensible novelty is **instrument-level** (two ablation designs no
named suite runs), not phenomenon-level. Both instruments are currently
under-powered (n=4 reps for C, 2/8 well-formed corruptions for B), which is
the honest reason not to publish either as a finding yet.

## Cross-cutting limit: every cell here is a sub-3-bit serving-stack observation

UD-IQ2_XXS sits below every published safe band: W8A8/W4A16 ≈ lossless
(≤0.8% drop) while 4-bit loses up to 59% and quantized models "often struggle
with instruction-following" (Liu et al. <https://arxiv.org/abs/2504.04823>;
Mekala et al. EMNLP 2025 <https://aclanthology.org/2025.emnlp-main.479/>;
Lee et al. <https://arxiv.org/abs/2409.11055>). Findings 1–4 are therefore
statements about *this quantization + this llama.cpp build*, never about
Qwen3-Coder-30B-A3B. Any corpus entry that reads as a model-capability claim
is mis-scoped and must be re-worded (sweep performed round 9: see
`bench-arena-round8-horizon.md` §"What round 8 does not license").

## Digest queue for the next rounds

1. Laban et al., *LLMs Get Lost In Multi-Turn Conversation*, ICLR 2026 —
   <https://arxiv.org/abs/2505.06120> — supplies the two controls this lane
   lacks (RECAP/SNOWBALL repeat-content arms; aptitude-vs-unreliability
   percentile decomposition), plus a system-prompt-hint null and a temperature
   ablation.
2. Lanham et al., *Measuring Faithfulness in Chain-of-Thought Reasoning* —
   <https://arxiv.org/abs/2307.13702> — the methodological template that
   upgrades probe B from bespoke cell to replication-with-a-twist.
3. llama.cpp issue #7052 — <https://github.com/ggml-org/llama.cpp/issues/7052>
   (pair with the Thinking Machines post) — falsifies residual novelty on
   finding 4 and names the serving flags that make an experimental unit
   defensible.
