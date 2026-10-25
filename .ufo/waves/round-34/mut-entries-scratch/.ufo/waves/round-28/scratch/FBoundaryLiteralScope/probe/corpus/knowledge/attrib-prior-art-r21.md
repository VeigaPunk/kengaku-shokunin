# Round-21 prior-art pricing — blind cascade-leg attribution (claim N1)

**Source basis:** the round-20 novelty scout's named paper set, relayed
through the round-21 brief, re-verified seat-side by direct fetch
(2026-10-16): every arXiv abs page fetched in-session, all 9 returning
HTTP 200 (§7 receipt), titles pulled from page headers. Local anchors:
`corpus/knowledge/probe-battery-r19.md` — §2 rows 4d/5b/7b and §5 findings
1/4, which are the receipts showing the feature classes (header tells,
burst-vs-incremental latency shape, model echoes) and the shim-journal
ground truth (`leg=1/zai OK status=200 stream=True 2.097s`) the r21
instrument will use. Adversarial default (r9/r11 convention,
`corpus/knowledge/eval-prior-art-calibration.md` §Verdicts): a claim is
KNOWN until a fetched source *fails* to cover it.

## 0. The claim as filed (N1)

> Blind cascade-leg attribution with shim-journal ground truth: a frozen
> feature-table instrument (latency band / header tells / error-wording
> shape / body schema — weights pre-registered and sha-frozen before any
> trial) attributes which cascade leg served a given response over ≥20
> blind trials per shim, at accuracy ≥ a frozen bar (80%), scored against
> operator-journal ground truth read only after trials complete; mimicry
> probes test whether attribution survives feature-profile padding.

Pricing question: is the *phenomenon* new, and is the *instrument* new?

## 1. Verdict

**INSTRUMENT-NOVEL, PHENOMENON-INCREMENTAL** (search-set verdict, §6) —
the scout's registration survives verification, with one citation
correction (§5).

- **Phenomenon — INCREMENTAL (crowded).** Identifying which model or
  serving stack produced a response from black-box interaction is heavily
  published: response-text fingerprinting (LLMmap, AdaptPrint, Kurian et
  al.), distribution-equality testing against reference weights (Model
  Equality Testing), serving-stack-component fingerprinting (2605.29979),
  timing/side-channel leakage (2411.01076, 2412.15431, 2409.20002), and
  agent-action identification (2605.14786). The overlap is direct in this
  fleet: r19 receipts show legs echoing their underlying models (zai leg →
  `glm-5.3-flash`, opencode leg → `deepseek-v4.1-flash`, battery §2 4d/7b),
  so "which leg served this" and "which model served this" largely
  coincide — a published phenomenon, instantiated fleet-locally. **No
  round-21 text may claim the phenomenon as a discovery.**
- **Instrument — NOVEL-instrument (not found in the fetched set).** No
  fetched source (i) attributes a *cascade leg* from *operational
  serving-stack artifacts* — latency bands, header families, error-wording
  shape, body schema — rather than response text or learned classifiers,
  (ii) assembles them into a *frozen, pre-registered hand-weighted feature
  table* (auditable and falsifiable by construction, not trained), or
  (iii) validates against an *operator-side shim journal* read only after
  trials complete. The blind-GT ordering is the lane's own
  freeze-before-request discipline (r19 BR-1 repair, r20 double-read
  guard) applied as a scoring protocol.
- **Where the instrument is load-bearing, not just new:** the ds cascade's
  hyper and opencode-go legs both served deepseek-family models in r19
  receipts (battery §5 finding 4 "hyper-deepseek"; §2 7b opencode echo
  `deepseek-v4.1-flash`). Where legs share a model family, response-text
  model fingerprinting alone cannot attribute the leg — the operational
  feature classes become the discriminators. This is the honest answer to
  "why not just run LLMmap".
- **Mimicry probes — phenomenon-incremental.** "Padding defeats (or fails
  to defeat) fingerprinting" is published in spirit for model-level
  features: Kurian et al.'s defense obfuscates identity via
  semantic-preserving output filtering; 2605.29979 argues prevention is
  fundamentally hard and offers only partial mitigations; 2605.14786 shows
  timing randomization degrades classifiers but a retrained classifier
  recovers. The r21 probes put that question to operational feature
  tables — a new surface for an old question.

The novelty proxy's split (phenomenon-new vs instrument-new,
SCORECARD §novelty proxy) therefore prices N1 exactly as registered. The
claim the round may make: **the instrument + the ground-truth protocol,
fleet-local** — not a new phenomenon.

## 2. The named papers (every one fetched this pass)

| Paper | Where | Fetch | What it establishes | Relation to N1 |
|---|---|---|---|---|
| **LLMmap: Fingerprinting For Large Language Models** — Pasquini, Kornaropoulos, Ateniese et al. (USENIX Security 2025 prepub) | arXiv 2407.15847 | 200 | "With as few as 8 interactions, LLMmap can accurately identify 42 different LLM versions with over 95% accuracy"; robust across application layers, unknown system prompts, sampling hyperparameters, RAG/CoT | Response-text model fingerprinting — the anchor of the crowded space. The brief's "LLMmap/2508.09021" conflates two papers (§5) |
| **Attacks and Defenses Against LLM Fingerprinting** — Kurian et al. (2025) | arXiv 2508.09021 | 200 | RL-optimized query selection fingerprints with only 3 queries; defense = semantic-preserving output filtering through a secondary LLM | Attack side crowds the phenomenon further; defense side is the mimicry-padding adjacency |
| **Model Equality Testing: Which Model is this API Serving?** — Gao, Liang, Guestrin (ICLR 2025) | arXiv 2410.20247 | 200 | Two-sample MMD tests against reference weights; 11 of 31 commercial endpoints (Summer 2024) served distributions differing from Meta's released weights | Statistical frame for "is the API what it claims". Needs reference samples from the claimed model; N1 needs no reference weights — only the operator's leg roster and journal |
| **AdaptPrint: Response-Adaptive Fingerprinting of Black-Box LLM Services** — Li et al. (2026) | arXiv 2608.22213 | 200 | Direct/Continuation/Follow-up probing; Top-1 80.6% over 27 candidate models; "strong robustness across different defense strategies and decoding parameters" | Adaptive-query fingerprinting; also the accuracy-bar neighbor (80.6% Top-1 vs the frozen 80% bar — different task, same magnitude) |
| **Fingerprinting Inference Systems** (inference engine / attention backend / hardware) — Wimbauer et al. (2026) | arXiv 2605.29979 | 200 | Stack components "can be identified reliably, even when the LLM is operated at non-zero temperature"; prevention "fundamentally hard" — numerical differences between hardware/software stacks cannot be eliminated, only partially mitigated | **Nearest published neighbor.** Delta: it fingerprints numerical deviations propagated to response *text* on fixed prompts; N1 attributes *operator-routed legs* from operational artifacts (headers, latency, error wording, body schema), validated against a journal |
| **Speculative-decoding side channel** — Saileshwar et al. (2024) | arXiv 2411.01076 | 200 | Per-iteration token counts / packet sizes fingerprint user queries (>75% over 50 prompts) and leak datastore contents >25 tok/s | Timing/traffic observables leak *inputs* — different target than server identity, same observable class as latency-band features |
| **Output-token-count side channel** — Zhang et al. (2024) | arXiv 2412.15431 | 200 | Output token count recovered via a timing channel "even over the network against a popular closed-source commercial LLM" | Network-observable timing channels on serving behavior are published |
| **Timing side channels in LLM systems** (KV/semantic cache) — Wang et al. (2024) | arXiv 2409.20002 | 200 | Cache-hit timing + classifiers infer system prompts and peer users' prompts | Timing-measurement → classifier method shape on serving infrastructure is published |
| **Known By Their Actions: Fingerprinting LLM Browser Agents via UI Traces** — Lugoloobi et al. (2026) | arXiv 2605.14786 | 200 | Passive JS tracker on agent actions + interaction timings identifies the underlying model, up to 96% F1; randomized timing delays degrade classifiers but a retrained classifier "largely recovers performance" | Timing-as-feature for model identification, and the padding-vs-retraining result — direct adjacency for the r21 mimicry probes |

## 3. What no fetched source does

- **Leg-level attribution inside an operator cascade.** Published work
  identifies *which model* (LLMmap, AdaptPrint, Kurian, Known By Their
  Actions), *whether the distribution changed* (Model Equality Testing),
  or *which stack component* (2605.29979). None attributes which leg of a
  fixed multi-leg cascade served a response, where the candidate set is
  the operator's own configured legs.
- **Operational feature classes as the discriminators.** The r21 features
  are serving-stack artifacts, not model behavior: `Server:` header
  families (r19 finding 1: `devin-openai-shim/2` vs the r18 census
  `BaseHTTP/0.6`), model-echo fields (`x-zen-model`), error-wording shape,
  body schema, and latency shape (burst vs incremental is per-leg —
  battery §5 finding 4: zai-glm span 0 ms vs hyper-deepseek 145 ms, TPS
  434.91). Closest published class: 2605.29979 (text-propagated numerical
  deviations) and the timing-channel papers (input secrecy) — neither
  uses header/error/schema artifacts for server attribution.
- **A frozen hand-weighted feature table as the classifier.** Published
  methods are trained classifiers or statistical tests. A pre-registered,
  sha-frozen weight table is a different falsifiability regime: the
  weights are inspectable before any trial and the 80% bar is frozen
  before outcomes exist.
- **Operator-journal ground truth, read after trials.** Published
  fingerprinting is evaluated against labels the experimenter controls
  (they deploy the candidate models) or self-reported IDs. N1's GT is the
  shim journal's own leg records, read only post-trial — the lane's
  freeze-before-request discipline promoted to a scoring protocol.

## 4. Honest scoping (the wording round 21 must keep)

1. The r21 claim is **INSTRUMENT + GROUND-TRUTH PROTOCOL** (fleet-local leg
   attribution validated against operator-journal GT). It is **not** a new
   phenomenon; any "models can be fingerprinted" phrasing is mis-scoped —
   that result is published and heavily cited.
2. Scope is **fleet-local and host-specific**: 2 shims, 3 legs each (r19
   live orders: ds `alibaba-token-plan → hyper → opencode-go`; glm
   `zai → devin → hyper`), one host, one day. Battery §8 limit 2 applies
   verbatim to any accuracy number the trials produce.
3. The accuracy bar (80%) sits next to AdaptPrint's 80.6% Top-1 over 27
   models — same magnitude, different task (leg attribution over 3
   candidates vs model ID over 27). The bar is a pre-registered floor for
   a fleet-local instrument, not a benchmark claim.
4. What would falsify the instrument-novelty label: a fetched source doing
   leg attribution from operational serving-stack features against
   operator-side GT. The search set is bounded (§6), so the label is a
   bounded negative, not registry proof (the r9/r11 wording convention).

## 5. Citation correction (defect — recorded, not patched)

The round-21 brief names "**LLMmap/2508.09021**". Fetched page titles:

- `[2508.09021] Attacks and Defenses Against LLM Fingerprinting` (Kurian
  et al.) — a 2025 attack/defense paper that *cites* LLMmap ("Their
  LLMmap tool represents the first systematic approach to fingerprinting
  …", search snippet).
- `[2407.15847] LLMmap: Fingerprinting for Large Language Models`
  (Pasquini et al.; USENIX Security 2025 prepub,
  `usenix.org/system/files/conference/usenixsecurity25/sec25cycle1-prepub-469-pasquini.pdf`)
  — the actual LLMmap.

Both papers are real and both support the crowded-space pricing; the
correction changes the citation, not the verdict. The brief also gave no
ID for Model Equality Testing (supplied: 2410.20247, cross-checked via
OpenReview `QCDdI7X3f9` and the ICLR 2025 proceedings page) or AdaptPrint
(supplied: 2608.22213). The conflation most plausibly arose because
2508.09021's related-work section discusses LLMmap; the scout's *verdict*
(crowded space) is unaffected — it actually strengthens it.

## 6. Limits

1. **Search-set verdict, not an exhaustive negative.** 9 fetched primaries
   + 2 web searches this pass. The scout's set arrived through the round
   brief and was treated as a lead, then verified — not as evidence. A
   counterexample would most plausibly look like 2605.29979 applied to
   multi-leg shims; none was found in this set.
2. **Citation counts seen in search snippets** (Model Equality Testing
   "Cited by 60/61"; 2508.09021 "Cited by 5") are relayed through search
   results, not independently verified — used above only as crowding
   color, never as grounding.
3. **The instrument does not exist yet.** This prices the *claim*
   pre-trial. If trials return <80% or the mimicry probes defeat
   attribution, the claim dies on accuracy/robustness, not novelty — and
   a failed instrument is still an honest negative for the corpus.
4. **Venue status is mixed.** LLMmap (USENIX Security 2025 prepub) and
   Model Equality Testing (ICLR 2025 proceedings) are venue-anchored; the
   2026-dated arXiv entries (2605.29979, 2605.14786, 2608.22213) are v1
   preprints at fetch time.
5. **No novelty-proxy exercise happened in r19/r20** (battery §8 limit 7);
   this note resumes prior-art pricing for the r21 claim. No lane files
   other than this note were touched; SCORECARD.md/LOG.md are
   parent-owned this wave.

## 7. Fetch receipt (commands + verbatim outputs)

```
$ for id in 2407.15847 2508.09021 2410.20247 2608.22213 2605.29979 \
      2411.01076 2412.15431 2409.20002 2605.14786; do \
    curl -s -o /dev/null -m 15 -w "%{http_code}" \
      "https://arxiv.org/abs/$id"; echo " <- $id"; sleep 2; done
2407.15847 -> HTTP 200
2508.09021 -> HTTP 200
2410.20247 -> HTTP 200
2608.22213 -> HTTP 200
2605.29979 -> HTTP 200
2411.01076 -> HTTP 200
2412.15431 -> HTTP 200
2409.20002 -> HTTP 200
2605.14786 -> HTTP 200

$ curl -s https://arxiv.org/abs/2605.14786 | grep -oE '<title>[^<]+</title>'
<title>[2605.14786] Known By Their Actions: Fingerprinting LLM Browser Agents via UI Traces</title>
$ curl -s https://arxiv.org/abs/2508.09021 | grep -oE '<title>[^<]+</title>'
<title>[2508.09021] Attacks and Defenses Against LLM Fingerprinting</title>
```

Every abstract quoted in §2 was read from the fetched abs page (FetchURL,
in-session), not from search snippets.
