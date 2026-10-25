# r14 review — do the round-12 prior-art claims support the novelty pricing? (PriorArtReviewer, 2026-09-29)

**Agent:** `PriorArtReviewer` (reviewer, L2). **Scope:** `corpus/evidence/round12-fleet/r12-prior-art-ladder.md`
(337 lines, md5 `cd3166d8302e09c64eda4d0177e5e9c4`, sha256 `907a0d23c9…beba2fa`) and
`corpus/evidence/round12-fleet/r12-prior-art-transport.md` (540 lines, md5
`5db36d1b972bbd6a0e8cd9ca211a9bfe`, sha256 `457508defd…5438c1a6`) — both read in full, then a
≥8-URL sample re-fetched live and the quoted decisive lines re-extracted from the returned bytes.
**Method:** `curl -sSL -A 'Mozilla/5.0 …' -o <file> -w '%{http_code}'` into a session dir, quotes
re-extracted with tag-strip + whitespace-collapse (`re.sub(r'\s+',' ',…)`), PDFs via
`pdftotext -layout`. Zero requests to `http://127.0.0.1:34113`; no repo file outside this one was
touched; no mutating git command was run. Every quote below was re-observed in-session on
2026-09-29; a sibling reviewer (`round12-fleet/r12-review-citations.md`) independently re-fetched
all 94 distinct cited URLs the same day — this artifact quotes decisive *lines*, not just statuses.

## 1. Claim → verdict → URL triple table (all six r12 claims)

| # | Claim (per `probe_plan_r12.md` §1) | Phenomenon vs instrument | Verdict (file §) | URL(s) the verdict rests on (all HTTP 200 when cited) |
|---|---|---|---|---|
| C1 | Severity ↑ monotonically as forced-emission density ↓ over 4 ordered arms (Page's test, n=64×4) | instrument-new residue over published phenomenon-neighbourhood | **INCREMENTAL** (ladder §3/C1) | `arxiv.org/abs/2401.04925`(+v3 html), `arxiv.org/abs/2507.11538`(+v1), `arxiv.org/abs/2309.00384`(+v3), `arxiv.org/abs/2609.08589`, `arxiv.org/html/2305.02363v2`, `en.wikipedia.org/wiki/Page%27s_trend_test`, `aclanthology.org/J04-3003.pdf`, `arxiv.org/abs/2512.18456`(+v1) |
| C2 | Paired severity diff at {7,10} reproduces r11's +0.352 on identical problems/seeds | phenomenon (design class) | **INCREMENTAL** (ladder §3/C2) | `github.com/ggml-org/llama.cpp/issues/7052` (+REST +comments), `thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/`, `docs.vllm.ai/…/reproducibility.html` (200, JS shell — *not* cited as read) + `raw.githubusercontent.com/vllm-project/vllm/main/docs/usage/reproducibility.md`, `arxiv.org/abs/2602.14349`, `arxiv.org/abs/1909.06674` (html v2 recorded **404**), `arxiv.org/abs/2411.00640`(+v1), `arxiv.org/abs/2505.06120` + ICLR 2026 PDF |
| C3 | r8 `A-MONO` collapse = up-front op batching, not emission sparsity (emission count held at 1) | **instrument-new** | **NOVEL-instrument** (ladder §3/C3, negative search §4) | `aclanthology.org/2025.findings-acl.245/`(+pdf), `arxiv.org/abs/2309.00384`, `arxiv.org/abs/2507.11538`, `arxiv.org/abs/2505.06120`+ICLR26 pdf, `arxiv.org/abs/2410.15553`(+v1), `arxiv.org/abs/2608.13417`(+v1); negative cert: 24 web + 6 arXiv-API + 4 OpenReview queries, full-text greps of `arxiv.org/html/2511.10457v1` & `2605.19743v1` → 0 hits |
| C4 | Dense-vs-sparse severity dose transports to positional token-sequence editing family (n=48) | phenomenon (cross-family application of the C3-class instrument) | **INCREMENTAL** (low) (transport §3.3) | S1–S24 + S44/S45, incl. `arxiv.org/abs/2505.06120`, `2404.06654`, `2201.11903`, `2410.02810`, `2507.11538`, `2504.08312`, BIG-bench `list_functions`/`tracking_shuffled_objects` READMEs (raw.githubusercontent.com), `2107.07002`, `2511.04703`, `2310.11324`, `2603.10044` |
| C5 | Mechanical predictor on r11 bytes forecasts r12's per-problem pass outcomes, Brier/BSS/calibration vs arm climatology | instrument (borrowed canon) | **INCREMENTAL** (low) (transport §4.3) | S25–S43, incl. `arxiv.org/abs/2509.20645`(+v3), `aclanthology.org/2025.findings-acl.790/`, `arxiv.org/abs/2402.14992`, `journals.plos.org` ×2, `sites.stat.washington.edu/…/Gneiting2007jrssb.pdf`, `lirias.kuleuven.be/retrieve/577522`, `ds.data.jma.go.jp/…/TCC_Seminar_Verification(Dehara2011).pdf`, `jmlr.org/papers/v24/23-0106.pdf`, `forecastbench.org` methodology pdf, `epoch.ai/benchmarks/forecastbench` |
| C6 | Adjacent severity gaps ordered by checkpoints removed; total spread > each adjacent gap | instrument (ordering construct) | **INCREMENTAL** (ladder §3/C6) | `arxiv.org/abs/2401.04925` (§4.4), `arxiv.org/abs/2408.03314`, `arxiv.org/abs/2512.02008`, `arxiv.org/pdf/2510.06471`, `arxiv.org/abs/2507.11538` §4.4 |

## 2. Fetched-URL spot checks (14 URLs re-fetched live 2026-09-29; quote re-extracted from returned bytes)

| # | URL | Status | Decisive line as observed this session | Verdict |
|---|---|---|---|---|
| 1 | `arxiv.org/html/2401.04925v3` (C1/C6 ingredient) | 200 | "For few-shot COT, there is a direct linear correlation between step count and accuracy." + "shortening reasoning steps, even while preserving the key information, significantly diminishes the reasoning abilities of models" | REPRODUCES — supports published monotone step-count dose; also supports the artifact's recorded *attribution correction* (it's expanding/compressing demonstrations, not "removing steps from a fixed prompt") |
| 2 | `arxiv.org/abs/2507.11538` (C1/C3 density neighbour) | 200 | "…to measure how instruction-following performance degrades as instruction density increases. We evaluate 20 state-of-the-art models … even the best frontier models only achieve 68% accuracy at the max density of 500 instructions." | REPRODUCES verbatim; density-as-dose published, constraint-instruction density ≠ emission density — consistent with C3's "each axis touched, never crossed" |
| 3 | `arxiv.org/html/2309.00384v3` (C1/C3) | 200 (abs + v3 html) | "Also, with the increase of batch size, the overall accuracy decreases." + "As prompting with batched data inevitably stretches input length which decreases performance…" | REPRODUCES verbatim — published batching-dose with confound noted (input length), consistent with the artifact's use as neighbour-not-duplicate |
| 4 | `api.github.com/repos/ggml-org/llama.cpp/issues/7052` (+`/comments`) (C2 load-bearing) | 200 (+200) | Reporter body: "I get between 5 and 8 unique completion texts when using 8 slots." Maintainer JohannesGaessler 2024-05-03T07:49:31Z: "On the latest master the results for multiple slots are still not 100% deterministic." `state=closed`, `state_reason=completed`, 6 comments | REPRODUCES verbatim incl. the state_reason the artifact quotes; the artifact's caution (within-run repeat ≠ independent replication) is correctly grounded |
| 5 | `thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/` (C2) | 200 | "992 of the completions go on to generate 'Queens, New York' whereas 8 of the completions generate 'New York City'. On the other hand, when we enable our batch-invariant kernels, all of our 1000 completions are identical." | REPRODUCES verbatim |
| 6 | `raw.githubusercontent.com/vllm-project/vllm/main/docs/usage/reproducibility.md` (C2) | 200 | "vLLM does not guarantee the reproducibility of the results by default, for the sake of performance." + "In online mode, you can only enable batch invariance." | REPRODUCES verbatim; artifact's choice to cite the source markdown (the docs page is a JS shell) is confirmed correct — the `.html` page is unciteable-as-read |
| 7 | `aclanthology.org/2025.findings-acl.245/` (C3 nearest batching-interference) | 200 | "Batch prompting, which combines a batch of multiple queries sharing the same context in one inference, has emerged as a promising solution to reduce inference costs. … malicious users can inject attack instructions into a batch, leading to unwanted interference across all queries, which can result in the inclusion of harmful content, such as phishing links, or the disruption of logical reasoning." | REPRODUCES verbatim; interference-across-packed-instances published — supports "axis touched separately" half of C3 |
| 8 | `arxiv.org/abs/2505.06120` (C3 polarity foil + C4 design idiom) | 200 | "…significantly lower performance in multi-turn conversations than single-turn, with an average drop of 39% across six generation tasks. Analysis of 200,000+ simulated conversations decomposes the performance degradation into two components: a minor loss in aptitude and a significant increase in unreliability." | REPRODUCES verbatim; supports BOTH uses the artifacts make of it (merged-helps polarity vs C3's merged-hurts; six-family same-manipulation design vs C4) |
| 9 | `arxiv.org/abs/2408.03314` (C6) | 200 | "…the effectiveness of different approaches to scaling test-time compute critically varies depending on the difficulty of the prompt. This observation motivates applying a 'compute-optimal' scaling strategy…" | REPRODUCES verbatim — published non-uniform dose increments, exactly as C6's forbidden-wording table requires |
| 10 | `arxiv.org/abs/2404.06654` + `arxiv.org/abs/2410.02810` (C4 design idiom) | 200 / 200 | RULER: "…a new synthetic benchmark RULER with flexible configurations for customized sequence length and task complexity" + "We evaluate 17 long-context LMs with 13 representative tasks in RULER." StateAct: "StateAct outperforms ReAct, the previous best base agent, by over 10% on Alfworld, 30% on Textcraft, and 7% on Webshop across multiple frontier LLMs." | REPRODUCE verbatim — one-manipulation-across-families is published practice ⇒ C4 INCREMENTAL supported |
| 11 | `arxiv.org/abs/2509.20645` + `aclanthology.org/2025.findings-acl.790/` (C5 frame) | 200 / 200 | PRECOG: "We investigate whether evaluation outcomes can be forecast before any experiments are conducted." + "…yielding 2,290 instances covering 1,519 papers". PredictaBoard: "…the ability of score predictors (referred to as assessors) to anticipate LLM errors on specific task instances (i.e., prompts)…" | REPRODUCE verbatim — forecast-the-eval + per-item anticipation both published ⇒ C5 INCREMENTAL supported |
| 12 | `lirias.kuleuven.be/retrieve/577522` (C5 calibration canon) | 200 (PDF, `pdftotext`) | "We suggest a minimum of 200 events and 200 non-events." (l.124 of extracted text) + "…a calibration slope of 1" / "calibration slope smaller than one when the model is internally or externally validated" | REPRODUCES verbatim — grounds the "calibration descriptive, event-count-limited" wording constraint |
| 13 | `ds.data.jma.go.jp/tcc/tcc/library/library2011/TCC_Seminar_Verification(Dehara2011).pdf` (C5 BSS semantics) | 200 (PDF) | "Brier skill score = An improvement rate with respect to a climatic forecast … BSS<0 : inferior to the climatic forecast." | REPRODUCES verbatim — grounds "BSS is reference-relative" constraint |
| 14 | `arxiv.org/abs/2305.02363` + BIG-bench READMEs (`list_functions`, `tracking_shuffled_objects`) (C1/C4 constructs) | 200 / 200 / 200 | Entity-tracking: "…infer the final state of an entity given an English description of the initial state and a series of state-changing operations"; `list_functions` README "**10750** free text"; `tracking_shuffled_objects` "3750 multiple choice and **0** free text" + `three/five/seven_objects` dirs | REPRODUCE verbatim — probe-shape construct published (2023); family-2-shaped construct published without emission-schedule arm |

**Recorded-failure re-probe:** `arxiv.org/html/1909.06674v2` → **404** this session, matching the
ladder artifact §6's recorded failure — honest bookkeeping confirmed.

## 3. Adversarial re-probe of the one NOVEL-* verdict (C3)

C3's `NOVEL-instrument` rests on a bounded negative: *no fetched source holds emission count fixed
while varying op batching*. I re-ran the trap the artifacts warn about — search-synthesis prose that
*claims* a counterexample:

- `web_search` "state tracking LLM benchmark all operations in one prompt versus one operation per
  turn ablation monolithic incremental" returned synthesis text asserting `arXiv 2511.10457` runs a
  Monolithic-vs-Incremental ablation ("The entire sequence of state-changing operations … presented
  … within a single, static prompt" vs "one operation or event per turn").
- I fetched the primary: `arxiv.org/html/2511.10457v1` → **200, 418,146 bytes** — within ~3 kB of the
  ladder artifact's recorded 418,499 bytes for the same GET (small drift consistent with a live
  page). Tag-stripped greps: `monolithic`, `incremental`, `all operations`, `one at a time`,
  `per turn`, `frequency`, `granularity`, `density`, `severity`, `pass rate`, `emit` → **0 hits
  each**. The synthesis's "monolithic vs incremental ablation" attribution is **not in the fetched
  bytes** — a second synthesis artefact of exactly the class the ladder artifact §4 recorded for
  `2605.19743` ("Page's test on T1–T6 tiers", also refuted on fetch). **[INFERENCE]** the synthesis
  conflated this paper's "different scenarios" wording with an ablation; whatever the cause, the
  fetched primary is what counts, and it does not cross the batching/sparsity axes.

The closest published contrasts remain: monolithic-vs-sharded *content* delivery with turn count
varying (Laban, opposite polarity to C3's prediction — artifact flags this honestly), and batch
*density* degradation (BatchPrompt/IFScale/ACL'25-attack). Neither fixes emission count at 1 while
varying delivery schedule. C3's `NOVEL-instrument` **survives this re-probe**, at the artifact's own
stated confidence (medium — search-based negative, no registry sweep).

## 4. Overreach audit

The artifacts are unusually disciplined: every claim carries a "strongest permitted" AND a
"may NOT write" sentence, and the closing tables scope every negative to its search set
("have no fetched published counterpart", "no named suite … reports this decomposition" — never
"no published X exists"). Flagged items:

| # | Item | Severity | Detail / suggested scoped wording |
|---|---|---|---|
| O1 | **Stale C5 event count inside the transport artifact** | medium (numerical, verdict-neutral) | `r12-prior-art-transport.md:19,306,391,403,433` say "448 pass events" throughout; the hashed plan's §9 amendment log (`probe_plan_r12.md:120,412`) corrects this to **416** (5×64+2×48; "the earlier figure was an L1 arithmetic slip"), and `analysis_r12.md:30` + `predictions-r12-perproblem.jsonl` (416 lines) landed at 416. The artifact also misses the amendment's attribution. Wording fix: "416 pass events (7 arms × their own n)" — matching the plan's corrected text. Verdict unaffected (INCREMENTAL either way), but a reviewer quoting the artifact would propagate a falsified number. |
| O2 | C2's replication-taxonomy anchor lost to a 403 | low | ACM badging taxonomy was the natural definitional cite for "independent replication"; artifact §6 records the 403 and falls back to Raff 1909.06674 + serving docs — the conclusion (within-run repeat ≠ independent replication) is *stronger* than the taxonomy would have forced, so the fallback is conservative, not overreaching. |
| O3 | "not found" phrasing in §3 bodies | none (compliant) | C1/C2/C6 "What was not found" statements are explicitly scoped "in any fetched source" / "no fetched published counterpart" and §4 labels them absence-of-evidence at medium confidence — matches the r11 CriticLanded wording ruling the report quotes. No rewrite needed. |
| O4 | Single-line claim tables in the report quote 448 | low | `r12-report-final.md:35` quotes the artifact's permitted wording — it reproduces "416 binary pass events" correctly in its own C5 row, so the *report* is clean; only the transport artifact carries the stale figure (O1). |
| O5 | `analysis_r12.md` verdict language vs artifact caps | none observed | Headline verdicts are mechanical branch texts (LADDER ESTABLISHED / DISSOCIATION ESTABLISHED / TRANSPORT DIRECTIONAL, `analysis_r12.md:53,57,59`) — these are rule labels, not novelty assertions, and the report's claims table applies the artifacts' permitted wording. No "first-of-kind"/"novel phenomenon" phrasing found in either artifact's permitted text; the only "first-of-kind" occurrence is in a *prohibition* sentence (`r12-report-final.md`). |

## 5. Bottom-line rubric verdict

SCORECARD novelty +1 rubric: *a probe measures a construct the lane could not previously observe,
the instrument is inspectable in-repo, and the claim carries a prior-art verdict with a fetched
URL* (proxy: fraction of headline claims carrying verdict+fetched URL).

- **F fetched-URL leg:** 6/6 claims priced, every verdict rests on URLs fetched-with-status by the
  scouts; my 14-URL sample + 1 failure-reprobe all re-resolve and every quoted decisive line
  re-extracts verbatim. Sibling `r12-review-citations.md` independently covers all 94 URLs.
  **Leg met.**
- **New construct measured:** the four-arm ordered emission-density ladder with a severity endpoint
  (C1 instrument residue), the fixed-emission batching/sparsity dissociation (C3 `NOVEL-instrument`,
  re-probed §3), and the checkpoint-count ordering (C6) are constructs the lane had not measured
  (r11 priced only the middle contrast); `probe_r12.py`/`run_r12.py`/`recompute_r12.py` are in-repo
  with sha256 pins inside the hashed bundle (`analysis_r12.md:66,112`; `ordering.log`).
  **Leg met.**
- **Transport arm (C4):** INCREMENTAL (low) is the correct floor — the cross-family design idiom is
  published (S1/S4/S5/S3) and the artifact correctly forbids claiming transport-design novelty;
  observed result TRANSPORT DIRECTIONAL (diff +0.177, p=0.2571) sits comfortably inside the
  INCREMENTAL pricing, no overclaim.

**Verdict: PASS with one medium erratum candidate.** The two artifacts support a novelty +1 leg —
*ladder instrument + batching dissociation (NOVEL-instrument, confidence medium) + transport arm
(INCREMENTAL)* — provided (i) O1's stale "448" is corrected or errata'd before anyone quotes the
transport file, and (ii) all headline wording continues to use the artifacts' permitted sentences
(the report does). No fetched source I re-read contradicts a verdict; the one live counterexample
lead dissolved into a search-synthesis artefact on fetch.

## 6. Gaps

- My URL sample is 14 of ~94 cited URLs weighted toward verdict-load-bearing primaries; the
  remaining fetch statuses rest on `r12-review-citations.md` (independent same-day sweep).
- C3's negative is a search-set verdict, not a registry sweep (no Semantic Scholar bulk, no arXiv
  full-text index); one adversarial re-probe passed, but a single missed keyword family remains
  possible — this is the residual that keeps the novelty +1's confidence at medium, per
  SCORECARD's own "No published density→severity manipulation — medium" line.
- I did not re-verify the *statistics* (Page p, paired t) — that is CriticLanded's lane; this
  artifact prices only the prior-art support for the novelty claim.
