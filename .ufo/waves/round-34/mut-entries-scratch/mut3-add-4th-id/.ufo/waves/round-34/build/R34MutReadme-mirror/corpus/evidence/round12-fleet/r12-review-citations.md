# r12 review — citation & pointer verification (ReviewerCitations, reviewer, wave 2a)

**Agent:** ReviewerCitations. **Task restated:** re-fetch every distinct external URL cited in
`r12-prior-art-ladder.md` and `r12-prior-art-transport.md`; re-verify the load-bearing quotes;
audit the `NOVEL-*` negative-search certificates; re-run/re-read every `file:line`, backticked
command and committed-path citation in the round-12 fleet artifacts (incl. the two prior-art
artifacts' `probe_plan_r12.md` line claims, classified `STALE-LINE-NUMBER` where the pre-hash
amendment moved them); and check every r12 verdict against the taxonomy of record.
**No fixes applied.**

## 0. Method, authority, and limits

- **Zero requests to `http://127.0.0.1:34113`** in this task (the endpoint is owned by the run).
  All external checks are public HTTPS `HEAD`-then-`GET` (browser UA, 12 threads, 25–60 s
  timeouts); all local checks are read-only (`git`, `read`, `grep -n`, `sed -n`, `sha256sum`,
  `test -e`, `python3 <script> --selftest`, …). No repo file was written except this one; no
  mutating git command was run. Stdlib-only Python; checksums/pipelines are integer/byte
  accumulations (no hash-order-sensitive arithmetic).
- **Measurement date:** 2026-09-29 (host clock `-03`). Repo `HEAD` at measurement =
  `e171cdfbdb350ee90bfc1c66dac54106a3a5e2ca` ("corpus: round-9 aggregator corpus-verdict
  lesson…"), i.e. the round-12 tree has landed on top of the pre-round `f09ff1f`
  (`git rev-parse HEAD`); `f09ff1f` is still addressable (`git show f09ff1f:…`).
- **State change observed while reviewing:** the main run has landed
  (`corpus/evidence/round12-ladder/ordering.log` → `main-run-launch 2026-09-29T01:19:59Z`,
  `landed 2026-09-29T01:32:44Z results-r12.jsonl md5 9dd8aa2b6a7aa7890aa802c37d5af0f9`,
  `run.log md5 700d1ddd2ece50d7bdedd55859c59f3a`), and the tree kept moving under this review
  (L1 landing): `round12-ladder/` held 15 files at first read, **18** at final read;
  `analysis_r12.md` appeared mid-review (md5 `fd3ca422189ded336525a1361234c0fe`, first line
  “# Round 12 analysis — powered emission-granularity ladder + transport”); the promoted
  `recompute_r12.py` sha changed twice in-session; `grader.py` went from `CHECKS n=280` (pre-round,
  exit 0) to `n=693 mismatches=28 VERDICT: FAIL` on the worktree with `--selftest` S0–S7 but
  `FAILURES PRESENT`. **All such values in this artifact are timestamped snapshots**; the r12 gate
  state is L1/ExecutorGrader/CriticLanded territory, not this lane's to adjudicate (see O6).
  Per this task's contract **no run bytes were read** (`results-r12.jsonl`, `run.log`;
  `analysis_r12.md` is cited only by md5/first line, never by value).
- **Authority order for line numbers:** `probe_plan_r12.md` (hashed v1, incl. its §9 pre-hash
  amendment log) → `round12-fleet/INTEGRATOR-NOTES.md` → L2 drafts. Both prior-art artifacts were
  drafted against an earlier state of the plan; §9 is the tie-breaker, and this artifact classifies
  the drift rather than assuming a single line map.

---

## 1. External URL resolution

**Scope.** 94 distinct external URLs are cited across the two prior-art artifacts (36
ladder-only, 61 transport-only, 3 shared: `2505.06120`, `2507.11538`, `2410.15553`). The ladder
artifact's `http://127.0.0.1:34113` mention and its partial/ellipsized API endpoints
(`export.arxiv.org/api/query`, `api2.openreview.net/notes/search?term=`,
`api.semanticscholar.org/graph/v1/paper/search?query=emission granularity LLM…`) are excluded from
the count: the first is the local endpoint (no traffic, by rule), the last is not a fetchable URL
(ellipsis inside the backticks); the Semantic Scholar *host* was re-probed separately (§1.3).

Re-fetched 2026-09-29 with `HEAD` then `GET` fallback. `claimed status` = the status printed in
the artifact for that URL (transport register rows carry `200` in the HTTP column; failure rows
carry their recorded code; `SSL` = recorded `CERTIFICATE_VERIFY_FAILED`).

| url | cited-by | claimed status | your status | verdict |
|---|---|---|---|---|
| `https://aclanthology.org/2025.findings-acl.245/` | L§2.3 | 200 | 200 | REPRODUCES |
| `https://aclanthology.org/2025.findings-acl.790/` | T§2 S40 | 200 | 200 | REPRODUCES |
| `https://aclanthology.org/J04-3003.pdf` | L§2.1 | 200 | 200 | REPRODUCES |
| `https://api.github.com/repos/google/BIG-bench/contents/bigbench/benchmark_tasks/list_functions` | T§2 S9 | 200 | 200 | REPRODUCES |
| `https://api.github.com/repos/google/BIG-bench/contents/bigbench/benchmark_tasks/tracking_shuffled_objects` | T§2 S10 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/1706.04599` | T§2 S38 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/1909.06674` | L§2.2 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2005.01835` | T§2 S34 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2107.07002` | T§2 S18 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2201.11903` | T§2 S6 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2209.13331` | T§2 S13 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2305.14318` | T§7 rejected | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2309.00384` | L§2.1 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2310.11324` | T§2 S21 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2311.07911` | T§2 S16 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2401.03601` | T§2 S17 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2401.04925` | L§2.1 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2402.14992` | T§2 S41 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2404.06654` | T§2 S5 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2406.10149` | T§2 S12 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2408.03314` | L§2.4 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2409.19839` | T§2 S26 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2410.01208` | T§2 S15; T§0 rejected | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2410.02810` | T§2 S4 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2410.15553` | L§2.3; T§2 S2 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2411.00640` | L§2.2 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2411.12990` | T§2 S19 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2412.03597` | T§2 S44 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2501.17399` | T§2 S22 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2504.08312` | T§2 S8 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2505.06120` | L§2.2; T§2 S1; L§8 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2507.04562` | T§2 S42 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2507.08038` | T§7 rejected | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2507.11538` | L§2.1; T§2 S7 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2509.20645` | T§2 S25 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2511.04486` | T§2 S14 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2511.04703` | T§2 S20 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2511.10457` | T§2 S11 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2512.02008` | L§2.4 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2512.18456` | L§2.1 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2602.02888` | T§2 S23 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2602.14349` | L§2.2 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2603.10044` | T§2 S3 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2606.11217` | T§2 S24 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2607.20526` | T§2 S39 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2608.13417` | L§2.3 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2609.08589` | L§2.1 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/abs/2609.23201` | T§2 S45 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/1909.06674v2` | L§6 | 404 | 404 | REPRODUCES |
| `https://arxiv.org/html/2305.02363v2` | L§2.1 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2309.00384v3` | L§2.1 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2401.04925v3` | L§2.1 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2410.15553v1` | L§2.3 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2410.15553v2` | T§2 S2 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2411.00640v1` | L§2.2 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2505.06120v1` | T§2 S1 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2507.11538v1` | L§2.1 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2509.20645v3` | T§2 S25 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2511.10457v1` | L§4 | 200 (418 499 B) | 200, 418 499 B | REPRODUCES |
| `https://arxiv.org/html/2512.18456v1` | L§2.1 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2603.10044v1` | T§2 S3 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2605.19743v1` | L§4 | 200 (787 479 B) | 200, 787 479 B | REPRODUCES |
| `https://arxiv.org/html/2606.11217v1` | T§2 S24 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/html/2608.13417v1` | L§2.3 | 200 | 200 | REPRODUCES |
| `https://arxiv.org/pdf/2510.06471` | L§2.4 | 200 | 200 | REPRODUCES |
| `https://docs.vllm.ai/en/latest/usage/reproducibility.html` | L§2.2; L§6 | 200 (JS shell) | 200 | REPRODUCES |
| `https://ds.data.jma.go.jp/tcc/tcc/library/library2011/TCC_Seminar_Verification(Dehara2011).pdf` | T§2 S36 | 200 | 200 | REPRODUCES |
| `https://en.wikipedia.org/wiki/Page%27s_trend_test` | L§2.1 | 200 | 200 | REPRODUCES |
| `https://epoch.ai/benchmarks/forecastbench` | T§2 S28 | 200 | 200 | REPRODUCES |
| `https://forecastingresearch.org/research/ai-progress-accuracy-update` | T§2 S29 | 200 | 200 | REPRODUCES |
| `https://github.com/ggml-org/llama.cpp/issues/7052` | L§2.2 | 200 | 200 | REPRODUCES |
| `https://glossary.ametsoc.org/wiki/Skill_score` | T§7 F2 | 403 | 403 | REPRODUCES |
| `https://journals.ametsoc.org/abstract/journals/apme/12/4/1520-0450_1973_012_0595_anvpot_2_0_co_2.xml` | T§7 F3 | 202 | 202 | REPRODUCES |
| `https://journals.ametsoc.org/view/journals/mwre/102/1/1520-0493_1974_102_0048_asssfp_2_0_co_2.pdf` | T§7 F6 | 202 | 202 | REPRODUCES |
| `https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0248780` | T§2 S31 | 200 | 200 | REPRODUCES |
| `https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0262862` | T§2 S32 | 200 | 200 | REPRODUCES |
| `https://leap.forecastingresearch.org/reports/waves-1-to-3-insights` | T§2 S30 | 200 | 200 | REPRODUCES |
| `https://lirias.kuleuven.be/retrieve/577522` | T§2 S35 | 200 | 200 | REPRODUCES |
| `https://openreview.net/forum?id=PV5xSw4n6y` | L§6 | 200 (4.8 kB shell) | 200 | REPRODUCES |
| `https://proceedings.iclr.cc/paper_files/paper/2026/file/59f6421e64707225fdf5b28840679a07-Paper-Conference.pdf` | L§2.2 | 200 | 200 | REPRODUCES |
| `https://raw.githubusercontent.com/google/BIG-bench/main/bigbench/benchmark_tasks/list_functions/README.md` | T§2 S9 | 200 | 200 | REPRODUCES |
| `https://raw.githubusercontent.com/google/BIG-bench/main/bigbench/benchmark_tasks/tracking_shuffled_objects/README.md` | T§2 S10 | 200 | 200 | REPRODUCES |
| `https://raw.githubusercontent.com/vllm-project/vllm/main/docs/usage/reproducibility.md` | L§2.2 | 200 | 200 | REPRODUCES |
| `https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jrssb.pdf` | T§2 S33 | 200 | 200 | REPRODUCES |
| `https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/` | L§2.2 | 200 | 200 | REPRODUCES |
| `https://www.forecastbench.org/assets/pdfs/forecastbench_updated_methodology.pdf` | T§2 S27 | 200 | 200 | REPRODUCES |
| `https://www.jmlr.org/papers/volume24/23-0106/23-0106.pdf` | T§2 S37 | 200 | 200 | REPRODUCES |
| `https://www.mdpi.com/2674-113X/4/3/17` | L§6 | 403 | 403 | REPRODUCES |
| `https://www.metaculus.com/api2/questions/?limit=1` | T§7 F1 | 403 | 403 | REPRODUCES |
| `https://www.metaculus.com/futureeval/methodology/` | T§7 F1 | 403 | 403 | REPRODUCES |
| `https://www.pnas.org/doi/10.1073/pnas.1509757112` | T§7 F4 | 403 | 403 | REPRODUCES |
| `https://www.psycharchives.org/handle/20.500.12034/8644` | T§2 S43 | 200 | 200 | REPRODUCES |
| `https://www.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf` | T§7 F5 | SSL | TLS verify FAIL (`curl: (60) … unable to get local issuer certificate`); 200 only with verification off | REPRODUCES |
| `https://www.acm.org/publications/policies/artifact-review-and-badging-current` | L§6 | 403 | 200 | DRIFTED |

*(The two `raftery` PDFs are distinct: `sites.stat.washington.edu/…/Gneiting2007jrssb.pdf` = S33,
plain 200; `www.stat.washington.edu/…/Gneiting2007jasa.pdf` = F5, TLS-verify failure as recorded.
`curl` with system CA store reproduces `curl: (60) SSL certificate … unable to get local issuer
certificate`.)*

### 1.1 Resolution rates

| set | n | strict (status == claim) | lenient (resource exists at all) |
|---|---:|---|---|
| ladder-only | 36 | 35/36 = **97.2%** | 36/36 = **100%** |
| transport-only | 61 | 61/61 = **100%** | 61/61 = **100%** |
| **combined (distinct)** | **94** | **93/94 = 98.9%** | **94/94 = 100%** |

- **Strict** = my status string equals the artifact's recorded status. **Lenient** = the resource
  exists at that URL (any 2xx/3xx, or a reproduced 403/202/404 challenge exactly as recorded);
  paywalled/403 sources count as resolving because the artifact recorded them as 403, which is
  what I observed).
- **Broken = 0.** The single non-REPRODUCES row (`acm.org`) drifted *in the artifact's favour*
  (403 → 200); the artifact did not cite it as read, so no verdict rests on it.
- **Rubric floor.** `SCORECARD.md` §Scoring rubric, depth row (`SCORECARD.md:152`) — “citation
  resolution stays ≥90%”. **The r12 prior-art set meets the floor at either measure** (98.9%
  strict / 100% lenient ≥ 90%).

### 1.2 Transport §8 reproduction block (the artifact's own re-probe command, re-run verbatim)

Its committed script (register rows only) now prints:

```
register rows: 45 url rows: 52 unique: 52
non-200: none (all 200)
```

which matches the artifact's recorded observation exactly (`52×200`; §5's “45 distinct works /
52 URL rows” tally also re-derives: §2.1 = 32 URL rows, §2.2 = 20, S-rows = 45).

### 1.3 Excluded / partial URLs (recorded so they are not read as failures)

- `api.semanticscholar.org/graph/v1/paper/search?query=emission granularity LLM…` (ladder §6,
  claimed 429): the cited string is **ellipsized inside the backticks** and cannot be re-fetched
  verbatim; the base endpoint re-probed → **HTTP 429** again (`python3 …urllib…`), so the claimed
  status reproduces at the host level.
- `export.arxiv.org/api/query` and `api2.openreview.net/notes/search?term=` (ladder §5): partial
  endpoints (no scheme/query); re-run as API queries in §3.
- `http://127.0.0.1:34113`: local endpoint — **zero traffic by contract**, excluded from the table.

### 1.4 Census arithmetic (internal consistency of the ladder artifact)

- §0 claims “**56 distinct URLs** fetched this session … **53 returned 200**; **3 failures**”
  (acm 403, mdpi 403, arxiv/html/1909.06674v2 404). §6's table also records the Semantic Scholar
  **429** (and two JS-shell 200s). 53+3 = 56 is internally consistent *only if the 429 attempt is
  not counted among the 56 `curl -L -A …` fetches*; the artifact's own §6 shows four nonzero
  statuses. Only **37** of the claimed 56 fetches are enumerable from the artifact (36 external +
  localhost), so the census cannot be independently re-derived. Filed as **O1** (observation).
- §0 “22 distinct sources are cited in §2” **reproduces**: §2 has 26 bold source rows, 22 distinct
  names (IFScale ×3, BatchPrompt ×2, 2401.04925 ×2, 2505.06120 ×2). §7's per-claim counts are
  8/7/7/5 = 27 row-uses, but C3's `7` exceeds §2.3's **6** rows → **O2**.

---

## 2. Quote fidelity — the load-bearing passages, re-fetched

Re-fetch 2026-09-29, tag-stripped + whitespace-collapsed (the artifacts' own declared pipeline),
PDF text via `pdftotext -layout` (poppler, present). **10 load-bearing quotes (Q1–Q10) plus 5
supporting probes (S1–S5).**

| # | quote (source) | supports | result |
|---|---|---|---|
| **Q1** | “For few-shot COT, there is a direct linear correlation between step count and accuracy.” (2401.04925v3) | C1/C6 monotone-dose precedent (**INCREMENTAL**) | **VERIFIED** |
| **Q2** | “T12. Longer functions improve vulnerability detection. Page's Trend Test (Page, 1963) shows statistically significant positive trends (p = 1.26 × 10⁻⁸ for C, p = 4.20 × 10⁻⁷ for C++).” (2512.18456v1) | C1 instrument is live in LLM-era work; NOVEL-instrument residue | **VERIFIED** (rendering-normalized: source has `Page’s`, `( Page, 1963 )` and a duplicated LaTeX-mirror span `p=1.26\times 10^{-8}`; every quoted word/number present) |
| **Q3** | “the Page test for Rule 2 (Siegel and Castellan 1988)” + “The Page test for ordered alternatives (Siegal and Castellan 1988, pages 184–188) indicates a chance of less than .001 that the four transitions are equally likely.” (J04-3003.pdf) | C1 instrument inside the ACL family | **VERIFIED** (both spellings `Siegel`/`Siegal` occur as quoted) |
| **Q4** | “between 5 and 8 unique completion texts when using 8 slots”; “On the latest master the results for multiple slots are still not 100% deterministic”; “floating point operations only return bit-for-bit identical results…” (gh #7052 body + comments API) | C2's serving premise (**high** confidence line) | **VERIFIED** |
| **Q5** | “vLLM does not guarantee the reproducibility of the results by default, for the sake of performance.” (vLLM `reproducibility.md` raw) | C2 serving premise | **VERIFIED** |
| **Q6** | “992 of the completions … whereas 8 of the completions …”; “when we enable our batch-invariant kernels, all of our 1000 completions are identical.” (Thinking Machines blog) | C2 serving premise | **VERIFIED** |
| **Q7** | “with an average drop of 39% across six generation tasks”; “decomposes the performance degradation into two components: a minor loss in aptitude and a significant increase in unreliability” (ICLR 2026 proceedings PDF) | C3 polarity contrast (**NOVEL-instrument** tension note) | **VERIFIED** |
| **Q8** | “the relative performance of algorithms may be altered significantly simply by choosing different benchmark tasks” (2107.07002) | C4 `INCREMENTAL (low)` (transfer concern published) | **VERIFIED** |
| **Q9** | “Our primary metric of prediction skill was the Brier score (BS), a standard measure of prediction accuracy”; “When trial results became available, prediction skill was calculated using Brier scores (BS) and compared against uninformative prediction” (PLOS 0262862) | C5 `INCREMENTAL (low)` (Brier-vs-baseline already published) | **VERIFIED** (the artifact's cut “(i.” is a verbatim prefix of the source sentence) |
| **Q10** | “We suggest a minimum of 200 events and 200 non-events.”; “calibration slope smaller than one when the model is internally or externally validated” (Van Calster, lirias PDF) | C5's calibration caveat in the strongest permitted wording | **VERIFIED** |
| S1 | “An improvement rate with respect to a climatic forecast” (JMA Dehara PDF) | C5 BSS reference-relative | **VERIFIED** |
| S2 | “We investigate whether evaluation outcomes can be forecast before any experiments are conducted.” (PRECOG 2509.20645 abs) | C5 frame published | **VERIFIED** |
| S3 | “We test six leading models on four pre-registered safety benchmarks with a direct API and three scaffolds: ReAct, multi-agent, and map-reduce. We conducted 62,808 scored evaluations.” (2603.10044 **abs** page — where the artifact attributes it) | C4 design idiom + C5 negative N2 | **VERIFIED** (exact on `/abs/`; the `/html/2603.10044v1` full text words it differently — “N = 62,808; six frontier models, four deployment configurations” — so this is a *page-scope* note, not a quote defect) |
| S4 | “We evaluate 17 long-context LMs with 13 representative tasks in RULER.” (2404.06654 abs text) | C4 one-manipulation-many-tasks idiom | **VERIFIED** |
| S5 | C3 negative greps: `2511.10457v1` 0 hits × `frequency|granularity|density|severity|pass rate`, 418 499 B; `2605.19743v1` 0 hits for `Page's Trend`/`Page, 1963`/`T1…T6` tiers, 787 479 B | C3 **NOVEL-instrument** certificate | **VERIFIED** (byte counts exact; `T1` substring hits are HTML anchors `S2.T1`, not complexity tiers) |

**NOT-FOUND count = 0; PARAPHRASE count = 0.** No verdict is undermined by quote infidelity —
including the two the task singled out (C3's `NOVEL-instrument` and C4/C5's `INCREMENTAL (low)`).

Checksums of the check (byte-identical re-derivations available on request): the two text-grep
targets re-fetch to **exactly** the artifact's recorded sizes (418 499 / 787 479 bytes).

---

## 3. Negative-search audit

**Requirement:** every `NOVEL-*` verdict must list the queries that returned nothing relevant, and
3 of them must be re-run.

- **`NOVEL-*` inventory:** ladder **C3 = NOVEL-instrument** (only). Ladder C1/C2/C6 and transport
  C4/C5 are `INCREMENTAL`; the transport artifact claims **no** `NOVEL-*` (§6 states this), so
  nothing further is owed — its N1–N3 are explicitly recorded as bounded non-findings.
- **Certificate exists?** Yes: ladder §4 lists, for C3, the empty queries
  (#3, #7, #13, #18, #23 batching/packing/density; #1, #8, #15, #16 emission/checkpoint
  schedule; #25 severity-vs-pass-rate) plus three targeted full-text greps. Scope is declared
  (search-based, no registry sweep; Semantic Scholar 429).

**Re-run by me (3 web queries + 2 arXiv API queries + 2 full-text greps):**

| re-run | result | contradicts C3? |
|---|---|---|
| ladder q#23 `single prompt all operations at once versus one operation per turn state tracking LLM which is harder ablation` | generic multi-turn-degradation commentary (Reddit/Substack/Confident-AI/DeepEval + the same ICLR 2026 Laban PDF); no named suite holding emission count at 1 while varying op batching | no |
| ladder q#16 `agent long-horizon evaluation checkpoints every N steps versus only final answer forced intermediate state emission ablation` | returns 2609.29875, EACL 2026 findings, 2608.13417 (already priced as non-ablating in ladder §2.3) — checkpoint *intervention* vs forced-emission *trace*; no batching-vs-sparsity decomposition | no |
| ladder q#18 `state tracking operations given all at once versus one at a time LLM entity tracking sequential updates versus batched` | returns 2511.10457 (priced: 0 hits for the five emission/severity terms), 2605.30233 (last-token aggregation) and 2305.02363 — the *neighbours* the artifact already priced, none an emission-count-fixed batching dissociation | no |
| `export.arxiv.org/api/query` `all:"emission granularity"` | 0 entries | no |
| `export.arxiv.org/api/query` `all:"Page test" AND all:"ordered"` | 0 entries | no |
| grep the 5 terms in `html/2511.10457v1` | 0 hits each, 418 499 B | no |
| grep `Page's Trend` / `Page, 1963` / tier labels in `html/2605.19743v1` | 0 hits (the ladder's “synthesis artefact” finding) | no |

**Audit verdict:** certificate present, scoped, and re-runnable; **no query re-run returns
anything that contradicts C3 = NOVEL-instrument.** (Residual risk unchanged: search-based
negative, not a registry sweep — the artifact says so.)

---

## 4. Internal pointer resolution

Verdicts: `REPRODUCES` / `FALSIFIED` / `STALE-LINE-NUMBER` (content moved by the pre-hash
amendment; current line given) / `SUPERSEDED` (true at its pin, moved since by the landing) /
`UNRUNNABLE` (endpoint-forbidden or host-state).

### 4.1 The two prior-art artifacts' `probe_plan_r12.md` line claims

| artifact | cited | cited content | current line(s) | verdict |
|---|---|---|---|---|
| ladder | `probe_plan_r12.md:11-13` | C1 claim row (+E1 §2.3) | **:20** (C1); §2.3 = :108 | **STALE-LINE-NUMBER** |
| ladder | `probe_plan_r12.md:14-16` | C2 claim row (+E2, R2) | **:21** (C2); R2 = :136-143 | **STALE-LINE-NUMBER** |
| ladder | `probe_plan_r12.md:17-19` | C3 claim row (+E4, R3) | **:22** (C3); E4 = :118 | **STALE-LINE-NUMBER** |
| ladder | `probe_plan_r12.md:24-26` | C6 claim row (+E3, R1) | **:25** (C6); E3 = :117; R1 = :132-135 | **STALE-LINE-NUMBER** |
| transport | `probe_plan_r12.md:23` | C4 claim | **:23** | **REPRODUCES** |
| transport | `probe_plan_r12.md:24` | C5 claim | **:24** | **REPRODUCES** |
| transport | E5 at `probe_plan_r12.md:119` | E5 endpoint row | **:119** | **REPRODUCES** |
| transport | R4 at `probe_plan_r12.md:143-145` | R4 verdict block | **:148-150** | **STALE-LINE-NUMBER** |
| transport | R5 at `probe_plan_r12.md:146-148` | R5 verdict block | **:151-154** | **STALE-LINE-NUMBER** |
| transport | scale caveat `probe_plan_r12.md:334-337` | family-2 metric not poolable | **:376-379** | **STALE-LINE-NUMBER** |
| transport | forecast informativeness `probe_plan_r12.md:338-340` | persistence-not-cold | **:380-383** | **STALE-LINE-NUMBER** |
| transport | C5 predictor `probe_plan_r12.md:38-40` | r11 bytes as legitimate prior | **:39-41** | **REPRODUCES** (range overlaps the sentence; `:38` alone is the preceding clause) |

Reading: the two scouts were drafted against **different plan states** — the ladder's §1 anchors
are uniformly pre-amendment (all four shifted by the amendments absorbed into §1–§5), while the
transport's anchors match the hashed v1 for the unchanged rows and drift only where the amendment
grew a block (R4/R5 by +5; §8 threats by +42). `probe_plan_r12.md` §9 is the authority and no
cited *content* is missing — only line numbers moved.

### 4.2 `r12-critic-design.md`

| pointer | expected | observed | verdict |
|---|---|---|---|
| `run_r12.py:29-39` reads `KENGAKU_R11_*`, imports `probe_r11.py`, writes `results-r11.jsonl` | pre-fix r11 copy | 29-40 = docstring + import block; `RESULTS = "results-r12.jsonl"` (`:48`); imports `probe_r12.py` (`:58`); no `probe_r11` reference anywhere | **STALE-LINE-NUMBER** (defect absorbed: plan §9 row D1; `INTEGRATOR-NOTES.md` L1-D1) |
| `run_r12.py:119-147` runs only two r11 arms | pre-fix two-arm runner | 119-147 = family-2 ask assembly + `filler()` | **STALE-LINE-NUMBER** (same absorption) |
| `probe_r12.py:415-461` still has the r8 A/B/C schedule | pre-fix `main()` | file is 426 lines; `:415-426` = die-guard comment “The round-8 A/B/C schedule that used to live here is deliberately GONE … (round-12 design critic D1)” | **STALE-LINE-NUMBER** (absorbed; §7 deviation 12) |
| `probe_plan_r12.md:2.3` defines midranks, `L = Σ j·R_j`; `:5` requires `L=<int>` | D2 | §2.3 @:108-115 now pins `L = Σ_j (j+1)·R_j`; §5 @:255 pins `L=<f.1>` | **STALE-LINE-NUMBER + absorbed** (§9 D2) |
| `:5` says `Ack compliance … (×6)` | D7 | current §5 @:274 pins `(×5: A-CKPT4710-ack, …, T-SPARSE-ack)`; §4 `A-INC-ack` = 0 @:206 | **STALE-LINE-NUMBER + absorbed** (§9 D7) |
| `:8` says “~3.7k requests, 12–20 min” | D10 | §8 @:385-386 now quotes §4: 4 000 chat / 4 002 HTTP / 12–25 min | **STALE-LINE-NUMBER + absorbed** (§9 D10) |
| `corpus/evidence/round11-power/analysis_r11.md` mean/sd 0.352/0.820 | D3 | `analysis_r11.md:18` “+0.352 sd 0.820 n=64” | **REPRODUCES** |
| D3's arithmetic `python3 -c 'import math; d=.352/.820; print(d,((1.959964+0.841621)/d)**2, …)'` | required normal n≈42.6; exact t ≈44 | `0.4292682926829268 42.594152824929715 0.37437781718472585 0.43229426706045193` | **REPRODUCES** |
| “the requested paired effect is `d_z=0.4293`” | D3 | plan §9 D3 + `power_analysis_r12.md` use **0.4288** (n=44 → 0.810, n=42 → 0.791) | **REPRODUCES** (0.4293 vs 0.4288 = r11's sd rounded at different precision; the floors 44/44 are the amended values, §9 D3) |
| D-table's `probe_plan_r12.md:4` (five non-empty ack cells) / `:2.1-2.2` arithmetic | D7 + census check | §4 ack rows @:206-210; §2.1/§2.2 arithmetic re-derives 4 000 chat / 4 002 HTTP / 4 114 records / 2 256 ack / 1 328 graded — all five sums confirmed by hand | **REPRODUCES** (content; line numbers pre-amendment) |
| critic verdict `DO-NOT-RUN` | plan §6 step 4 | `probe_plan_r12.md:305-312` records it and “no v2 chain” | **REPRODUCES** |

### 4.3 `r12-connector.md`

| pointer | expected | observed | verdict |
|---|---|---|---|
| sibling HEAD table (5 × `git log -1`) | kasegi `b7180b0`, kake `a209441`, kumitate `e0e5de1`, kotoba `63ceba7`, kagi `4391b3b` | kasegi `b021dc9`, kake `4214101`, kumitate `637d181`, kotoba `0f658ff`, kagi `2486643` — every pinned commit still resolves in its repo's history, but all five HEADs have moved (kumitate round-14 close; kagi round-14 freshness) | **SUPERSEDED** (pins true at write time) |
| instrument grep 1 (`Brier|BSS|calibration slope|…`) → ∅ ×5 | NO-DUPLICATE | re-run at current HEADs: 0 hits ×5 | **REPRODUCES** |
| task-family grep (`task.?family|external.validity|transport…`) → ∅ ×5 | NO-DUPLICATE | re-run: 0 hits ×5 | **REPRODUCES** |
| replay-gate grep → only `kagi-shokunin/corpus/lessons/round-11.md:184` | kengaku owns it | re-run: identical single hit at `:184` | **REPRODUCES** |
| kotoba framer-prediction hit `…/sibling-description-rewrites-round8.md:371` | one adjacent idea | re-run: same line (`L62 4. **Skip ex-ante calibration.** Record framer predictions before runs`) | **REPRODUCES** |
| `kumitate-shokunin/LOG.md:393`, `SCORECARD.md:190/203/213`, `corpus/knowledge/executable-scorecard.md:178`, `corpus/lessons/round-12.md:135`, `kotoba…/checklist-execution-round15.md:56` | preregistered route/outcome-band rows | all six lines match the described content (`:393` = “Deviated from the pre-registered route on evidence…”; `:56` = “## Outcome bands (pre-registered)”) | **REPRODUCES** |
| `.ufo/reports/round-12/protocol.md:56-57` (`kagi ok` / `kagi in-flight`) | report/lifecycle status | identical | **REPRODUCES** |
| `.ufo/reports/round-12/kagi.md:1-5` (“Repo commit: round-12”, follows `4391b3b`) | kagi r12 exists in the main repo | identical | **REPRODUCES** |
| `.ufo/reports/round-13/kasegi.md:56-59`, `.ufo/reports/round-14/kotoba.md:113-114`, `AGGREGATE.md:1201-1202` (D-98/D-99), `round-10/kengaku.md:23/57/58`, `round-10/protocol.md:223/359-362`, `round-11/kengaku.md:45/47/48/60`, `round-11/kasegi.md:20-21`, `round-12/protocol.md:116-149/276-280/354-357` | as quoted | every cited line carries the described content (incl. +0.352/sd 0.820/n=64 at `round-11/kengaku.md:45`, 220/448 = 49.1% at `:48`) | **REPRODUCES** |
| ladder dir listing “only `probe_plan_r12.md`, `probe_r12.py`, `run_r12.py`; no committed `results-r12.jsonl`, `analysis_r12.md`, `run.log`” | at write time | 15 files at my first read (incl. `results-r12.jsonl`, `run.log`; `analysis_r12.md` appeared later, md5 `fd3ca422…`), **18** at final read | **SUPERSEDED** |
| `probe_plan_r12.md:27-30, 36-40, 21, 45-56, 58-61, 64-67, 69-105, 108-149, 116-120, 152-158` | as cited | all resolve in the current plan (descriptor @27-30; pids @36-39; C2 @21; arms @42-56; rotation @57-61; settings @64-67; §2.2 @69-107; §2.3 @108-155; E2/E6 rows @116-120; contingency @167-179) | **REPRODUCES** |
| `probe_plan_r12.md:164-172, 191` (descriptors) | §3 fields | **:182-191** (§3 moved by the amendment) | **STALE-LINE-NUMBER** |
| `probe_plan_r12.md:183-192` (response fields / ack metadata) | §4 rows | **:197-213** | **STALE-LINE-NUMBER** |
| `probe_plan_r12.md:194-205` (cost/schema) | §4 + pinned totals | §4 @194; pinned totals @**218-226** | **STALE-LINE-NUMBER** |
| `probe_plan_r12.md:244-247` + “448 pass events” (E6) | E6 lines | E6 stored lines @**264-272**; and the plan now pins **416**, not 448 (§9 L1-E6; §1 C5 @:24, §2.3 E6 @:120) | **STALE-LINE-NUMBER** + **stale content** (see D2) |
| `probe_plan_r12.md:249` (ack-compliance line) | analysis contract | **:274** | **STALE-LINE-NUMBER** |

### 4.4 `r12-endpoint-freshness.md`

| pointer | expected | observed | verdict |
|---|---|---|---|
| `GET /v1/models` + `/health` on `:34113`; `curl` commands | 200, 872 B; `{"status":"ok"}` | endpoint traffic **forbidden to this review** | **UNRUNNABLE** (rule) |
| `/proc/1299/cmdline` = unit `ExecStart` = r11 `descriptors.server.argv`, 41 tokens | 3-way EXACT_MATCH | `pgrep -f llama-server` → **1299** still; `ps -o lstart` → `Mon Sep 28 02:55:28 2026`; `systemctl --user show -p ExecMainPID -p ActiveEnterTimestamp` → `1299`, `Mon 2026-09-28 02:55:28 -03`; r11 first-line `server.argv` = **41 tokens**, `pid` 1299 | **REPRODUCES** |
| `/tmp/r12f-models.json` 872 B, md5 `cd90917cebd85cf9102bb97ec3f5fa50`, sha256 `9267e1ee…` | byte-for-byte copy | file still present (872 B); md5/sha256 **exact match** | **REPRODUCES** |
| `data[0].id` / `models[]` / `meta` equal to r11 `descriptors`; only `created` differs | EXACT_MATCH except `created` | re-derived: `id` equal, `meta` equal, `models[]` equal, `created` 1790642665 (live) vs 1790638137 (r11) | **REPRODUCES** |
| `created` = request time: r10 capture `created=1790633228` ↔ `2026-09-28T22:07:08Z`; r11 `↔ 23:28:57Z` | in-band timestamps | re-computed from committed bytes / capture: **22:07:08Z** and **23:28:57Z** exactly | **REPRODUCES** |
| `~/.config/llama/qwen-coder-godspeed.jinja` 6818 B, mtime 2026-08-29 03:35:28 | unchanged | `stat` → 6818 bytes, `2026-08-29 03:35:28 -0300` | **REPRODUCES** |
| `systemctl --user cat qwen-coder.service` (unit body) | as quoted | re-run: unit body matches the quoted `ExecStart`/`[Unit]`/`[Service]` text | **REPRODUCES** |
| `PROVINCE.md:8-20`, `:15` (surfaces; route-telemetry ABSENT) | 9 surface rows; bounties absent | `PROVINCE.md:8` header + 9 rows (baseline command → 10 counting the header); `:15` = route-telemetry ABSENT row | **REPRODUCES** |
| r10 capture `corpus/evidence/round10-fleet/models-34113.json` `created=1790633228` | as quoted | JSON parse → `1790633228` | **REPRODUCES** |
| /tmp hash-file claims for the md5/sha of the capture (`wc -c 872`) | 872 | `ls -l` → 872 B | **REPRODUCES** |

### 4.5 `r12-review-baseline.md` (41 pointers)

Re-ran every row whose command is stated exactly; rows whose command is only *described* are
marked as such.

| rows | pointer | observed now | verdict |
|---|---|---|---|
| 1 | `git ls-tree -r 2575be6 --name-only \| grep -cE '\.(py\|sh)$'` → 12 | 12 | **REPRODUCES** |
| 1b | `find . \( -name '*.py' -o -name '*.sh' \) \| wc -l` → 27 | 34 (r12 scripts landed) | **SUPERSEDED** (row says “includes current untracked r12 ladder scripts”) |
| 2/20/25/30/38 | `python3 grader.py` → exit 0, `n=280 mismatches=0 errata_pinned=1`, PASS | identical (exit 0) | **REPRODUCES** |
| 3 | `sha256sum grader.py` → `14d54051…` | identical | **REPRODUCES** |
| 4 | `wc -l grader.py` → 1711; header round-11 tree | 1711 at `f09ff1f` (`git show`); **5554** on the worktree (r12 extension) | **SUPERSEDED** |
| 5/6 | r8 `horizon.py` md5 `1c157e2a…`, `results.jsonl` md5 `df154cb5…` | identical | **REPRODUCES** |
| 7/8 | r9 `predictions-r9.md` sha256, `replication.md` md5 | identical | **REPRODUCES** |
| 9 | `wc -l horizon.py` → 349 | 349 | **REPRODUCES** |
| 10 | `wc -l SKILL.md` → 518 | 518 at `f09ff1f`; **577** on the worktree | **SUPERSEDED** |
| 11 | cited-source bullets → 23 | 23 (also at `f09ff1f`) | **REPRODUCES** |
| 12/13 | “cited `~/` extractor” 15; “backtick path-token extractor” 113 | command described only (no exact regex); my closest readings give 14 `~/…` tokens | **UNRUNNABLE** (underspecified command) |
| 14 | `ls ~/Projects/webzites/repos/llm-wiki/wiki/karpathy/** \| wc -l` → 34 | 34 | **REPRODUCES** |
| 15/16 | path-by-path `test -e` incl. `~/wikillm/llm-wiki` absent | all OK except the two documented absences (`~/wikillm/llm-wiki`; bounties) | **REPRODUCES** |
| 17 | `find ~/bench-arena /tmp/bench-r8 …` → 0 lines; bench-arena mtime 2026-08-29 03:58 | bench-arena CSVs dated 2026-08-29 03:06–03:30 | **REPRODUCES** |
| 18 | `ls /tmp/bench-r7-l2-executor/graded \| wc -l` → 125 | 125 | **REPRODUCES** |
| 19 | `sha256sum /tmp/bench-r8/results.jsonl` → `bd986e5e…` | identical | **REPRODUCES** |
| 21 | `grep -c 'seed *= *2000 *+ *pid *\* *29' run_r9.py` → 0 | 0 | **REPRODUCES** |
| 22 | `grep -o 977 grader.py \| wc -l` → 2 | 2 | **REPRODUCES** |
| 23 | A-CKPT counts `24`/`16` | 24/16 against `round9-replication/results-r9.jsonl` (r11 file: 192/128 graded) | **REPRODUCES** (r9 tree; row's source is ambiguous) |
| 24 | `grep -c '"pid":104' results-r9.jsonl` → 32 | 32 | **REPRODUCES** |
| 26/39 | `--selftest` S0–S6 ALL PASS | S0–S6 (7 scenarios) ALL PASS, exit 0 | **REPRODUCES** |
| 27 | PROVINCE surface rows → 10 | 10 (header + 9 surfaces) | **REPRODUCES** |
| 28 | `find corpus/evidence/round10-fleet -maxdepth 1 -type f \| wc -l` → 22 | 22 | **REPRODUCES** |
| 29 | README rows 22/13 = files 22/13 | 22/22 ✓; rows 13 vs 14 lesson files (new r12 lesson) | **REPRODUCES** (pre-landing) / superseded count |
| 31 | PROVINCE paths; bounties ledger missing | bounties missing (documented) | **REPRODUCES** |
| 32 | `grep -rln 2505.06120 llm-wiki \| wc -l` → 0 | 0 | **REPRODUCES** |
| 33 | `grep -c '2505.06120\|2307.13702' eval-prior-art-calibration.md` → 4 | 4 | **REPRODUCES** |
| 34 | `head -4 url-status.txt` → 4×200 | identical | **REPRODUCES** |
| 35 | bench-arena `*.csv` dated 2026-08-29 03:06–03:30 | identical | **REPRODUCES** |
| 36 | r9 `ordering.log` 2 lines; r11 `7` | 2 / 7 | **REPRODUCES** |
| 37 | `sha256sum round11-power/prereg-bundle.sha256` → `bae0a585…` | identical; `sha256sum -c` → 3× OK | **REPRODUCES** |
| 40 | `find …/wiki/ai -name '*.md' \| wc -l` → 23 | 23 | **REPRODUCES** |
| §2 gate determinism | `/tmp/r12-bl-g{1,99,u}.out` byte-identical, sha256 `88aa3089…` | files still present; identical sha256; `PYTHONHASHSEED` variants re-verified by me via `python3 grader.py` (exit 0) | **REPRODUCES** |
| §2 r11 ordering chain | pre/post-hash `23:10:20Z`; script hashes `23:28:37Z`; first `request_ts` `23:28:57Z`; bundle `-c` exit 0 | `ordering.log` identical; `grep -m1 request_ts` → `2026-09-28T23:28:57Z`; `-c` exit 0 | **REPRODUCES** |
| §1 `git rev-parse HEAD` → `f09ff1fc…` | pre-round HEAD | history-addressable; current HEAD `e171cdf` | **SUPERSEDED** |
| §4 verdict `BASELINE: GREEN` | no new defect | still no r11-tree defect; the r12 tree is being landed concurrently and the current worktree gate reports `n=693 mismatches=28 FAIL` (see §6 O6 — L1's integration state, not a baseline-audit falsification) | **REPRODUCES** (scope: pre-round) |

### 4.6 `r12-mock-smoke.md`

| pointer | expected | observed | verdict |
|---|---|---|---|
| `run_r12.py` “committed lines 35–39 import `…/probe_r11.py`, which does not exist”; `RC=1` `FileNotFoundError` | failing-before evidence | current `run_r12.py` imports `probe_r12.py` (`:58`); `probe_r11.py` exists only in `round11-power/`; the D1 rewrite landed (plan §9 D1) | **SUPERSEDED** (accurate as failing-before, fixed since) |
| `probe_r12.py:51-60` includes the fallback alternation `…\{|…\[` (bare arrays parse) | parser check | `:51-61` = exactly that regex incl. `\[…\]`; `probe_r11.py:47-56` identical | **REPRODUCES** |
| expected census: 142 records / 138 HTTP calls at N=2/N2=2; per-cell 34/10/48/30/14 + 1+1+2+2 | arithmetic | re-derived all sums by hand: 1+1+2+2+34+10+48+30+14 = **142**; 92+44+2 = **138**; and the committed mock run (`/tmp/kengaku-r12-mock/results-r12.jsonl`) counts **142** with exactly `{descriptors 1, descriptors_end 1, meta 2, meta2 2, A-INC 20, A-CKPT4710 6, -ack 14, A-CKPT710 4, -ack 16, A-CKPT10 2, -ack 18, A-MONO 2, T-DENSE 6, -ack 14, T-SPARSE 4, -ack 16, filler 14}` | **REPRODUCES** |
| mock policy claims (port 18114 default; `/v1/models` → `{"data":[{"id":"mock-r12"}]}`; INTERCEPT log) | as quoted | `mock_server_r12.py:21` `PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18114`; `/tmp/r12-intercept.log` = `INTERCEPT GET 127.0.0.1:34113/v1/models -> models`; `/tmp/r12_driver.py` present (1004 B) | **REPRODUCES** |
| “No process remains running after the smoke” | cleanup | `pgrep -f mock_server_r12` → none | **REPRODUCES** |
| interpreter attempt command (`KENGAKU_R12_N=2 … run_r12.py`) | failing-before | re-running it would re-attempt the endpoint path (mock-mediated) — not re-run here | **UNRUNNABLE** (rule/scope) |

### 4.7 `r12-recompute-notes.md`

| pointer | expected | observed | verdict |
|---|---|---|---|
| draft `sha256 = 7d76224395716259d65b9e3ec2981a6e8e0c3f6cb30b118a859a5e22f9434d76`, 2722 lines, `--selftest` → `SELFTEST 127/127 PASS` exit 0 | hand-off pin | current `recompute_r12_draft.py` = **`883981e0cbaf1572105ff9b2710fcb3594c0a66f993dea089c01a4efb03873ce`, 2967 lines**, `--selftest` → **exit 1**, `TypeError: analyze() got an unexpected keyword argument 'probs'` (0 PASS lines) | **FALSIFIED** (see D1) |
| promotion: `cp … draft … recompute_r12.py` | promoted engine exists | `corpus/evidence/round12-ladder/recompute_r12.py` exists (sha `26772be8…` → re-measured `3798c57e…` mid-session, i.e. L1 was still editing/regenerating it; the promoted engine is *not* byte-identical to the draft — 295 diff lines; per `INTEGRATOR-NOTES.md` §1 the adjudications were applied to the promoted copy only) | **REPRODUCES** (promotion) / **SUPERSEDED** (hashes still moving) |
| promoted engine `--selftest` | the pipeline the gate depends on | `python3 corpus/evidence/round12-ladder/recompute_r12.py --selftest` → same `TypeError` traceback, **exit 1** on a direct run | **FALSIFIED** (see D1) |
| `power_r12.py` sha256 `7816b9638dab31213e08ab397df8226f06c9040f24415c00a340dd1ade200690`, 219 lines | corroboration source | exact match, 219 lines | **REPRODUCES** |
| toy assertions (Section 1): `L=71 E_L=75 var_L=25 z=−0.8 p=0.4237107971667933`; tied `L=51.5 E_L=50 var_L=12.5 z=0.4242640687` | two-module agreement | `power_r12.page_L([[3,2,1,0],[0,1,2,3],[2,3,1,0]])` → `(71.0, 75.0, 25.0, -0.8)`; `recompute_r12_draft.page_test(…)` → same + `p=0.4237107971667934`; tied toy → `51.5/50.0/12.5/0.4242640687` | **REPRODUCES** |
| §2 tolerance/format pins (`L=<f.1>`, `E_L=<f.1>`, `var_L=<f.3>`, `p` clip `1e-6`, `slope=… intercept=…`) | plan §5/§2.3 | plan §5 @:255-272 and §2.3 @:120/§9 D2/D5 pin exactly these | **REPRODUCES** |
| §5 interfaces: `predictions-r12-perproblem.jsonl` (416 lines) & `…signevents.jsonl` (304) — INTEGRATOR-NOTES “OVERRULED … exact names and schemas pinned” | landed files | both exist; `wc -l` = **416** / **304**; `sha256` = `bac550c7fc5e887da93e81369c63f839be080a52e1dfd211b7072446ef825e24` and `1d99040c39d59863023d9b9b0f2e2b6486d4ac772c2daaf0f75d09858990314c`, both matching `predictions-r12.md:102/127` | **REPRODUCES** |
| §6 provenance (`grader.py` r11 block `:862-953`; `recompute_r11.py` `:103,:134,:170,:183,:198,:239,:250`; `probe_r12.py:358` `grade_seq`) | ports | all lines carry the named functions/constants (`_betacf`@134, `betai`@170, `t_two_sided_p`@183, `t_crit`@198, `binom_two_sided`@239, `mcnemar_exact`@250, `extract_json_block`@103); `probe_r12.py:358` = `def grade_seq(got, want)` | **REPRODUCES** |
| plan cites `:115` (midranks), `:235` (L line), `:246` (slope), `:266-267` (Newton), `:120` (BSS), `:24`/`:120`/`:187` (448), `:230`/`:232`/`:244`/`:249`/`:252-256`/`:152-158` | §5 stored lines | current: midranks **:115** ✓; L line **:255**; E6 Brier **:266?** (E6 lines **:262-272**); Newton **§2.3 :120**; 448 → **416** everywhere (§9 L1-E6; `:24`, `:120`); census **:250**; arm table **:252**; ack **:274**; verdicts **:278-282**; contingency **:167-179** | **STALE-LINE-NUMBER** (+ one stale *number*, D2) |

### 4.8 `r12-report-draft.md`, `r12-log-draft.md`, `r12-doc-deltas.md`

| pointer / command | expected | observed | verdict |
|---|---|---|---|
| `git show f09ff1f:grader.py \| wc -l` → 1711; `0c51208` → 936; non-blank 1527; blank 184 | erratum F-R12-1 | identical (1711 / 936 / 1527 / 184) | **REPRODUCES** |
| `SCORECARD.md:142` contains “936 → **1709**” | erratum site 1 | yes (`SCORECARD.md:142` = operability row with `936 → **1709** lines`) | **REPRODUCES** |
| `LOG.md:18` round-11 entry; `LOG.md:19` = round 12; `awk 'NR==18' LOG.md \| wc -l` → 1 | log discipline | 18 lines, line 18 = round-11 bullet, single physical line | **REPRODUCES** |
| `sed -n '136,147p' SCORECARD.md` = r11 post-move w/ +0.352 sd 0.820 n=64 t=+3.431 df=63 p=0.0011 CI [+0.147,+0.556] sign 26W/7L/31T p=0.0013 | r11 comparator | exact | **REPRODUCES** |
| `SCORECARD.md:148-161` rubric (depth row “citation resolution stays ≥90%” @:152) | rubric | exact | **REPRODUCES** |
| `SCORECARD.md:163-184` §Planned + falsifiable target @181-184 | r12 target | exact | **REPRODUCES** |
| `SCORECARD.md:76-90` round-10 F1 errata | precedent | exact | **REPRODUCES** |
| `sha256sum -c corpus/evidence/round12-ladder/prereg-bundle.sha256` → “expected 3× OK” | bundle | bundle is now **9 files** (v1, `ordering.log` line 3: “v1: 9 files, design-critic DO-NOT-RUN absorbed pre-hash”) → **9× OK** | **SUPERSEDED** (token-level, L1 fills) |
| `corpus/evidence/round12-ladder/{ordering.log,prereg-precheck.log}` tokens | ordering proof + precheck | `ordering.log` = pre/post `2026-09-29T01:16:08Z`, script hashes `1871697f…`/`3beb91ea…`, launch `01:19:59Z`, landed `01:32:44Z`; `prereg-precheck.log` = `[PASS]` lines incl. 64/64 r11-meta identity, 48/48 family-2, 0 cross-family collisions | **REPRODUCES** |
| plan cites `:18-25`, `:126-150`, `:36-38`, `:41-57`, `:58-61`, `:69-107`, `:112-124`, `:27-30`, `:45-56`, `:334-338`, `:343-348`, `:8-11` | as cited | `:18-25` ✓ claims table; `:126-150` → **:130-155**; `:36-38` ✓; `:41-57` ✓; `:58-61` ✓; `:69-107` ✓; `:112-124` ✓; `:27-30` ✓; `:45-56` ✓; `:334-338` → **:376-379**; `:343-348` → **:385-392**; `:8-11` ✓ | mix: **REPRODUCES** (most) / **STALE-LINE-NUMBER** (R-block, §8, §6.5 `:286-288`→**:319-322**, contingency `:152-160`→**:167-179**) |
| `python3 grader.py --selftest` → S0–S7 | r12 gate | pre-round `f09ff1f`: S0–S6 (7 scenarios) ALL PASS, exit 0 — **reproduces**; current worktree: selftest emits **S0–S7** (8 scenarios) but ends `FAILURES PRESENT`, and `python3 grader.py` = `CHECKS n=693 mismatches=28 VERDICT: FAIL` exit 1 (r12 layer live; mismatches in `meta2` regeneration/retry-chain, two arm `mean_shared` cells, run-level Brier recomputation, a missing `e6_brier_all` line, the R2 trailing-text parse, `realized_positions`, and score-row identification) | **REPRODUCES** (pre-round scope) / **SUPERSEDED** (r12 state; see O6) |
| doc-deltas counts: knowledge 22/22, lessons 13/13, evidence 6/6 (`git ls-tree f09ff1f` → 6 dirs), SKILL 518 lines / 15? anti-patterns / 23 bullets, PROVINCE 9 surfaces, grader 1711, LOG 18 | pre-round table | all confirmed at `f09ff1f`; **anti-pattern count**: with the section actually named `## Research-note structure` (`SKILL.md:166`) the count is **19**, not 15 (reported elsewhere in the same file as 15) — an internal count ambiguity | **REPRODUCES** (except the anti-pattern count: **O3**) |
| report-draft `r12-mutation.md` / `r12-critic-landed.md` / `r12-review-index.md` | wave-2 artifacts | not present at my read (`{{W1_ARTIFACT_*}}`/`{{W2_ARTIFACT_*}}` are tokens by design) | **SUPERSEDED**/N-A |
| report-draft `<agent> r12-scout-endpoint-fresh.md` | artifact filenames | landed name is `r12-endpoint-freshness.md` | **UNRUNNABLE**? → **O8** (naming drift, placeholder) |

### 4.9 Committed-path citations (existence)

All resolve: `probe_plan_r12.md`, `power_analysis_r12.md`, `predictions-r12.md`,
`predict_r12.py`, `power_r12.py`, `precheck_r12.py`, `prereg-precheck.log`,
`prereg-bundle.sha256`, `ordering.log`, `probe_r12.py`, `run_r12.py`, `recompute_r12.py`,
`predictions-r12-perproblem.jsonl`, `predictions-r12-signevents.jsonl`;
`round12-fleet/{r12-*.md, mock_server_r12.py, grader_r12_draft.py, recompute_r12_draft.py,
INTEGRATOR-NOTES.md}`; `round11-power/{probe_r11.py, recompute_r11.py, results-r11.jsonl,
analysis_r11.md, power_analysis_r11.md, predictions-r11.md, prereg-bundle.sha256, ordering.log}`;
`round8-horizon/*`, `round9-replication/*`, `round10-fleet/*`, `round11-fleet/*`; `grader.py`,
`SKILL.md`, `LOG.md`, `SCORECARD.md`, `PROVINCE.md`, `corpus/README.md`,
`corpus/knowledge/eval-prior-art-calibration.md`, `corpus/lessons/round-9.md`,
`r10-review-cites.md`. **INTEGRATOR-NOTES.md exists** (93 lines) — all fleet artifacts'
references to it resolve. Two documented host absences remain: `~/wikillm/llm-wiki`,
`~/Projects/bounties/ledger/telemetry.jsonl` (both explicitly marked absent in the artifacts).

---

## 5. Taxonomy consistency (vs `eval-prior-art-calibration.md`, r11's two artifacts)

| r12 claim | r12 verdict | overlapping r11 entry (verified line) | weaker/stronger without reason? |
|---|---|---|---|
| ladder C1 (ordered ladder) | INCREMENTAL (low) | r11 C1 INCREMENTAL (low) `r11-prior-art-granularity.md:25`; r9 row 1 “incremental — the emission-granularity ablation is the new part” (`eval-prior-art-calibration.md` §Verdicts row 1) | **No.** Ladder states “unchanged in kind from r11, strengthened by the ordered test” and re-fetched new sources (`2512.18456`, Poesio). Consistent. |
| ladder C2 (within-run repeatability) | INCREMENTAL | no direct r11 twin (r11 C2 = ladder direction: KNOWN/INCREMENTAL `:26`; r11 M1b filed-prereg INCREMENTAL `:303`) | **No double-count** — different claim object (repeatability of a prior local effect), priced against Raff/2602.14349; the artifact explicitly notes its wording is *stronger* than r11's and re-checked it. |
| ladder C3 (op-batching vs sparsity dissociation) | **NOVEL-instrument** | r11 C3 **NOVEL-instrument** `:27` | **Adjacency note (not a defect):** two NOVEL-instrument verdicts in adjacent rounds on the same *instrument family*. The r12 certificate is for a **different construct** (emission count held at 1, op batching varied) and the artifact says the candidate phenomenon is “INCREMENTAL-adjacent”; defensible, but a reader must not read it as a second, independent discovery. Recorded as O4. |
| ladder C6 (gap-magnitude ordering) | INCREMENTAL | no r11 twin | **No.** |
| transport C4 (transport to a 2nd family) | INCREMENTAL (low) | r11 C4 INCREMENTAL (`:28`, prereg instrument — different claim) | **No.** Transport explicitly forbids restating r11's C3 NOVEL-instrument as C4's own (“C4 must not restate that verdict as its own”) — verified at `:222-226`. |
| transport C5 (per-problem forecasts) | INCREMENTAL (low) | r11 M1c “Brier-scored *self*-predictions … **INCREMENTAL**” (`r11-prior-art-prereg.md:305`, verified verbatim) | **No silent reversal.** The artifact cross-references `:305` and argues the event count (3 → 416) + BSS/slope do not cross a boundary. Consistent (if anything, *more* conservative than a bump would be). |
| method items (Page's test, hashed prereg bundle, replay gate) | carried as method context | r11 M1a KNOWN, M1b INCREMENTAL, r11 C4 INCREMENTAL | **No.** |

**Double-count / silent-reversal finding: none.** Two watch-items recorded (O4 above; and the
stale `448` → see D2). Also checked: no r12 claim *reprices* an r11 URL as new prior art without
labelling it method context (transport's r11 guard block `:317-323` names the r11 files and lines).

---

## 6. Defect table

| id | item | expected | observed | severity |
|---|---|---|---|---|
| **D1** | `r12-recompute-notes.md` pinned draft state + its selftest (and the promoted engine's) | sha `7d762243…`, 2722 lines, `--selftest` → `SELFTEST 127/127 PASS` exit 0 | draft = `883981e0…`, **2967** lines, `--selftest` **exit 1** `TypeError: analyze() got an unexpected keyword argument 'probs'` (0 PASS lines); same crash in the promoted `round12-ladder/recompute_r12.py` (sha `3798c57e…`). Measured inside the landing window (the file's sha was still changing), so the *crash* may be transient; the **pin falsification stands either way** — the committed draft no longer matches its recorded hand-off state, and the checked-in `--selftest` is not green | **high** |
| **D2** | E6 event count in the fleet artifacts | hashed plan pins **416** (C5 @:24, E6 @:120, §5 @:264; §9 L1-E6) and the landed predictions file says 416 | transport §0/§4.1/§5 say “**448** pass events (7 arms)”; connector row repeats “448 pass events”; report-draft flags the plan-side only | **medium** |
| **D3** | ladder §7 per-claim source counts | C1 8, C2 7, C3 6, C6 5 (26 rows; 22 distinct names as §0 claims) | §7 prints C3 = **7** (one more than §2.3's 6 rows) | **low** |
| **D4** | ladder §0 URL census | “56 distinct URLs fetched … 53 × 200; 3 failures (403/403/404)” | §6 also records a **429** (Semantic Scholar) and two JS-shell 200s; only 37 of the claimed 56 fetches are enumerable | **low** |
| **D5** | transport S1 venue annotation | ICLR 2026 (fetched proceedings header “Published as a conference paper at ICLR 2026”; `eval-prior-art-calibration.md` row 1) | transport labels 2505.06120 “(icml'25 …)” | **medium** (venue is a taxonomy input) |
| **D6** | `r12-review-baseline.md` HEAD pin `f09ff1f` | pre-round HEAD, all hashes true | still true at that commit; current HEAD `e171cdf`; `wc -l grader.py` 1711→5554 | **low** (superseded, labelled) |
| **D7** | mock-smoke failing-before evidence | runner imports `probe_r11.py`, RC=1 | defect fixed (D1 rewrite); the artifact's own census (142) and parser claims still reproduce | **low** (superseded, labelled) |
| **D8** | fleet artifact naming | report-draft refers to `r12-scout-endpoint-fresh.md`, `r12-mutation.md`, `r12-critic-landed.md`, `r12-review-index.md` | landed: `r12-endpoint-freshness.md`; wave-2 names not yet present | **low** |
| **O1–O8** | observations (not necessarily defects) | — | O1 ladder census (§1.4); O2 §7 C3 count (=D3); O3 `SKILL.md` anti-pattern count 15 vs section-scoped 19 (`doc-deltas` vs `report-draft` section names); O4 C3 NOVEL-instrument adjacency (§5); O5 doc-deltas' round12-ladder row text places mock/logs under `round12-ladder/` while `mock_server_r12.py` is in `round12-fleet/` and smoke logs live only in `/tmp`; O6 **the r12 gate state moved twice during this review** — first `python3 grader.py` exit 2 `r12_md: no such file`, then (after `analysis_r12.md` appeared, md5 `fd3ca422…`) `CHECKS n=693 mismatches=28 VERDICT: FAIL` exit 1 with `--selftest` S0–S7 ending `FAILURES PRESENT`; the named mismatches are in the r12 layer (`r12.meta2.regenerate.ops`/`retry_chain` 48/48, `arm.A-INC.mean_shared`, `arm.T-DENSE.mean_shared`, every `e6.brier_runlevel.RL*`, missing `e6_brier_all`, `verdict_r2` trailing text, `realized_positions`, score-row identification). **Not adjudicated here** — L1/ExecutorGrader/CriticLanded own that check; recorded because the report-draft's clause (3)/(4) expects exit 0 + `--selftest` PASS and that expectation is not yet met on the worktree; O7 `recompute_r12.py` sha changed twice within my session (L1 still regenerating); O8 baseline rows 12/13 are described-only commands (not verbatim re-runnable) | informational (O6 = landing-in-progress, not a citation defect) |

**Not defects (recorded so they are not re-filed):** the `acm.org` 403→200 drift is in the
artifact's favour and uncited; the JASA SSL failure reproduces exactly; the 202/403 paywalls,
`arxiv `/html/1909.06674v2` 404, the JS-shell pages (vLLM docs, OpenReview) all reproduce their
recorded statuses; every quoted sentence verified; every `NOVEL-*` certificate re-runnable.

**Lane rubric floor.** `SCORECARD.md:152` (depth row) requires citation resolution ≥90%: the r12
prior-art set is **98.9% strict / 100% lenient → floor met**.

CITATION RESOLUTION: 98.9% strict / 100.0% lenient, 0 broken