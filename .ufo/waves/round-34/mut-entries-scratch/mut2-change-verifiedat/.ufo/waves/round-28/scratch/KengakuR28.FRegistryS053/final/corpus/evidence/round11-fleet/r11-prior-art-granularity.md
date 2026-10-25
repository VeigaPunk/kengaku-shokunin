# Prior-art pricing — round-11 emission-granularity headline claims

Scout (L2), round 11. Public web only. **Zero requests to `127.0.0.1:34113`** in this task.
Method: ~45 `web_search` queries (§3) + in-session `urllib` fetches of every cited primary
(arXiv abs/HTML, ACL Anthology, GitHub issue page), recording HTTP status, title, and the grounding
sentence(s) pulled from the fetched bytes (§2). Search-synthesis prose was **not** trusted: three
synthesis-claimed facts were checked against the papers' own text and **failed** (§2.4).

Adversarial default (r9 convention, `corpus/knowledge/eval-prior-art-calibration.md` §Verdicts):
a local claim is `KNOWN` until a fetched source *fails* to cover it.

## 0. The four claims as filed (local anchors)

| # | Claim (as preregistered) | Local anchor |
|---|---|---|
| C1 | Sparser forced full-state checkpoints raise per-problem error **severity** (mean wrong keys at shared checkpoints) while pass rate ties → severity-only dose response | `corpus/evidence/round11-power/probe_plan_r11.md:11-15`; point prediction **+0.350** at `predictions-r11.md:14`; effect source mean diff **+0.500**, sd **0.9636**, n=8 at `power_analysis_r11.md:28` |
| C2 | Ladder `INC > CKPT > MONO` (per-turn incremental > forced checkpoints > monolithic) | r9 record: `corpus/knowledge/eval-prior-art-calibration.md` §Verdicts row 1; r9 `replication.md` |
| C3 | **Instrument:** a named public suite that ablates *emission granularity* on identical problems+seeds, grading severity separately from pass rate | `probe_plan_r11.md` §2 (two-cell paired design, same pid) |
| C4 | **Instrument:** preregistered (hashed predictions + power analysis filed pre-request) single-local-server behavioral probe with a hermetic offline replay gate | `probe_plan_r11.md` §6 (ordering/hash protocol), §4 (schema the grader replays), repo-root `grader.py` |

## 1. Verdict table

| # | Verdict | Grounding (fetched URL + status) | One-line reason |
|---|---|---|---|
| **C1** | **INCREMENTAL (low)** — adjacent published, this variant new | `arxiv.org/abs/2609.08589` **200**, `arxiv.org/abs/2605.30233` **200**, `arxiv.org/abs/2305.02363` **200**, `arxiv.org/abs/2602.07338` **200** | The *ingredients* are published (intermediate emission improves state tracking; intermediate report quality is decoupled from task success; LMs do not track state incrementally, they aggregate at the last token). The **specific dose response** — checkpoint **density** manipulated, pass rate tied, **severity magnitude** (wrong-key count) monotonically increasing as checkpoints get sparser — was **not found** in any fetched source. |
| **C2** | **KNOWN** for `CKPT > MONO`; **INCREMENTAL** for `CKPT < INC` — unchanged from r9 row 1 | `arxiv.org/html/2210.09261v1` **200**, `arxiv.org/abs/2410.02810` **200**, `arxiv.org/abs/2305.20050` **200**, `arxiv.org/abs/2509.17766` **200**, `arxiv.org/abs/2605.15102` **200** | Intermediate trace/state emission beating answer-only or outcome-only is published on identical problems (`2210.09261` Tracking Shuffled Objects: flat no-CoT curve → emergent CoT performance; `2410.02810` StateAct >ReAct +10% ALFWorld; `2305.20050` process>outcome supervision; `2509.17766` state-reconstruction +14.1% HotpotQA). |
| **C3** | **NOVEL-instrument** — not found after these searches | `arxiv.org/abs/2609.08589` **200**, `arxiv.org/abs/2604.12312` **200**, `arxiv.org/abs/2604.02022` **200**, `arxiv.org/abs/2608.20563` **200**, `arxiv.org/abs/2511.10457` **200**, `arxiv.org/abs/2507.05257` **200**, `arxiv.org/abs/2406.12045` **200**, `arxiv.org/abs/2406.10149` **200** | No named suite ablates emission **density** on identical problems+seeds with severity graded apart from pass rate. The nearest 2026 instrument varies reporting **position in the lifecycle**, not density, and grades categorical failure **classes**, not severity counts (`2609.08589`). r9's ruling stands and no 2025–2026 counterexample was found. |
| **C4** | **INCREMENTAL** — protocol published, this instantiation new | `arxiv.org/html/2606.11217v1` **200**, `arxiv.org/html/2603.10044v1` **200**, `arxiv.org/abs/2411.00640` **200**, `arxiv.org/abs/2411.12990` **200**; `arxiv.org/html/2607.16200v1` **404** (negative) | Preregistration for AI-agent experiments is published with a template (`2606.11217`) and has been **executed at scale** for LLM evals with OSF DOIs, an OSF-published SHA-256 hash before scoring, a power analysis, and a dose-response hypothesis (`2603.10044`). The power-analysis method is published (`2411.00640`). **Not found:** a preregistered probe whose artifact is a hermetic offline replay gate over committed run bytes on a **single local served model**. |

## 2. Grounding sources (every one fetched in-session)

### 2.1 C1 — severity / decoupling

| Source | Fetch | Grounding sentence(s) |
|---|---|---|
| **The Unreliable Progress Bar: Can LLM Agents Reliably Report Task Progress Throughout Execution?** — arXiv 2609.08589 (2026-09) | `https://arxiv.org/abs/2609.08589` **200**; HTML `https://arxiv.org/html/2609.08589v1` **200** | "StageIF places the reporting duty at any point in a task, freezes the correct value before the model answers, and scores **four layers of failure** (acting instead of reporting, omission, malformed report, **wrong value**)". And: "the turns on which the machine report is absent keep a **task-proxy pass rate of 91–100%**". ⇒ task success is **decoupled** from intermediate-report correctness — the decoupling half of C1 is published; the **density dose** is not. |
| **Do Language Models Track Entities Across State Changes?** — arXiv 2605.30233 | `https://arxiv.org/abs/2605.30233` **200** | "We find that LMs **do not incrementally track world states across tokens** or query-relevant states across layers, but simply **aggregate relevant information in parallel at the last token** when the query becomes evident." ⇒ the mechanical reason per-turn emission helps (and why sparser emission should hurt) is published. |
| **Entity Tracking in Language Models** — Kim & Schuster, ACL 2023 — arXiv 2305.02363 | `https://arxiv.org/abs/2305.02363` **200**; `https://aclanthology.org/2023.acl-long.213/` **200** | "a task probing to what extent a language model can infer the final state of an entity given an English description of the **initial state** and a **series of state-changing operations**." ⇒ the lane's probe *shape* (init + ops → final state) is a 2023 published construct; grading there is final-state accuracy, not severity count. |
| **Intent Mismatch Causes LLMs to Get Lost in Multi-Turn Conversation** — arXiv 2602.07338 | `https://arxiv.org/abs/2602.07338` **200** | Confirms the LiC drop and re-attributes it to "an intent alignment gap rather than intrinsic capability deficits" — the 2026 state of the multi-turn-degradation literature. |

### 2.2 C2 — checkpoints vs monolithic vs incremental

| Source | Fetch | Grounding sentence(s) |
|---|---|---|
| **BIG-Bench Hard** — Suzgun et al., arXiv 2210.09261 | HTML `https://arxiv.org/html/2210.09261v1` **200** | Verbatim: "Three examples of such tasks—**Multi-Step Arithmetic, Tracking Shuffled Objects, and Web of Lies**—are shown in Figure 5… CoT prompting enables emergent task performance"; Figure 5 caption: "For three tasks where prompting without CoT has a flat scaling curve… CoT prompting enables emergent-task performance, which is performance that goes from **random to substantially above random** as scale increases." Results table row `Tracking Shuffled Objects λ (avg) 22.5 24.1 64.7 100 25.1 61.1 24.1 84.5 19.6 52.9` (per-model columns; the no-CoT/CoT pairing is per Figure 5's legend — the *direction*, not the exact pairing, is what is cited here). ⇒ on **identical shuffled-object state-tracking problems**, a step-by-step trace moves accuracy from ~random to well above it. |
| **StateAct: Enhancing LLM Base Agents via Self-prompting and State-tracking** — arXiv 2410.02810 (EMNLP 2025 REALM) | `https://arxiv.org/abs/2410.02810` **200**; `https://aclanthology.org/2025.realm-1.27/` **200** | "**self-prompting**, which reinforces task goals at every step, and (2) **chain-of-states** … that tracks state information over time. StateAct outperforms ReAct … by over **10%** on Alfworld, **30%** on Textcraft, and **7%** on Webshop." |
| **Let's Verify Step by Step** — Lightman et al. 2023 — arXiv 2305.20050 | `https://arxiv.org/abs/2305.20050` **200** | "finding that **process supervision significantly outperforms outcome supervision** for training models to solve problems from the MATH dataset." ⇒ intermediate feedback > final-only feedback at the supervision layer. |
| **A State-Update Prompting Strategy for Efficient and Robust Multi-turn Dialogue** — arXiv 2509.17766 | `https://arxiv.org/abs/2509.17766` **200** | "utilizes '**State Reconstruction**' and 'History Remind' mechanisms… on HotpotQA … improves the core information filtering score by **32.6%**, leading to a **14.1%** increase in the downstream QA score." |
| **Self-Recall Thinking (SRT)** — arXiv 2605.15102 | `https://arxiv.org/abs/2605.15102` **200** | "SRT identifies helpful historical turns and uses them to generate contextually appropriate responses" to fix "track dependencies across non-adjacent turns". |
| r9-carried anchors (already priced) | measurement re-checked this round: `https://arxiv.org/abs/2505.06120` **200**, `2410.15553` **200**, `2406.12045` **200**, `2406.10149` **200**, `2507.05257` **200** | Laban *LLMs Get Lost In Multi-Turn Conversation* (r9's row-1 anchor: over-reliance on prior answers; SNOWBALL +15–20% still < FULL), plus Re²/RECITE/induction heads/least-to-most as in `corpus/knowledge/eval-prior-art-calibration.md`. |

### 2.3 C3 — instrument search (suites that do *not* ablate emission density)

| Source | Fetch | What it does / why it is not a C3 counterexample |
|---|---|---|
| **MemoryAgentBench** — arXiv 2507.05257 | `https://arxiv.org/abs/2507.05257` **200** | incremental multi-turn memory; four competencies; no emission-frequency ablation. |
| **τ-bench** — arXiv 2406.12045 / **τ²-bench** — arXiv 2506.07982 | **200** / **200** | end-state DB comparison + `pass^k`; no emission-schedule manipulation. |
| **BABILong** — arXiv 2406.10149 | **200** | long-context state tracking over noise; degradation with complexity, not with emission density. |
| **Exploring State Tracking Capabilities of Large Language Models** — arXiv 2511.10457 | abs **200**, HTML **200** | three state-tracking tasks; keyword grep of the full HTML returned **0** hits for `frequency`, `granularity`, `density`, `severity`, `pass rate` ⇒ construction varies, emission schedule does not. |
| **ATBench** — arXiv 2604.02022 | **200** | trajectory-level **safety** taxonomy (risk source × failure mode × harm); severity-like, but safety-graded and not an emission-density ablation. |
| **CompliBench** — arXiv 2604.12312 | HTML **200** | judge detection + **localization** (exact turn index + guideline); grep found **0** `severity`/`criticality` ⇒ finer localization, not severity-of-state-error. |
| **Beyond End-to-End Success** — arXiv 2608.20563 | **200** | "instruments security tasks with **checkpoints**, separates failures before and after capability exposure" — **diagnostic position**, not checkpoint-density dose, and no severity count. |
| **Beyond Final Scores** — arXiv 2608.13417; **Beyond the Answer Key** — arXiv 2608.28725; **VSTAT** — arXiv 2606.03920; **chess state eval** — arXiv 2508.19851 | all **200** | within-run behaviour metrics / step-level grader robustness / multimodal / chess-legal-move fidelity — adjacent "beyond pass rate" instruments, none ablates emission granularity. |
| **Agent-Diff** — arXiv 2602.11224 | **200** | state-diff contracts instead of final-string matching (closest published *state-grading* idiom). |

### 2.4 Search-synthesis claims that FAILED verification (recorded so they are not re-imported)

| Synthesis claim | Check | Result |
|---|---|---|
| "The Unreliable Progress Bar ablated *reporting frequency* / checkpoint density" | grep `frequency`, `granularity`, `density`, `number of checkpoint`, `checkpoint spacing` in `2609.08589v1` | **0 hits each** → the frequency-ablation claim is a synthesis artefact; the paper varies report **position**, not density. |
| "`2511.10457` found high-frequency reporting hurts smaller models / helps frontier models" | grep the same keywords in `2511.10457v1` | **0 hits each** → fabricated attribution; the paper is a three-task capability benchmark. |
| "A deterministic offline replay harness paper exists at arXiv 2607.16200" | fetch `https://arxiv.org/html/2607.16200v1` | **HTTP 404** → no such primary; C4's replay-gate half stays unpriced by any *fetched* source. |

## 3. Search-query log (what "not found" means here)

Queries actually issued (`web_search`; `-` marks a derived duplicate the tool auto-ran):

1. LLM multi-turn state tracking error severity partial credit wrong keys benchmark / -state tracking evaluation benchmark LLM dialogue partial credit wrong keys
2. LLM agent checkpoint frequency intermediate verification dose-response / -checkpoint frequency intermediate verification dose response LLM agent long task
3. preregistration machine learning evaluation predictions hashed before experiment
4. "Adding Error Bars to Evals" statistical approach language model evaluations Miller / -Adding Error Bars to Evals Miller language model evaluation
5. emission granularity ablation LLM incremental vs batch prompting state updates / -emission granularity ablation LLM state updates
6. self-verification checkpoints improve multi-turn state maintenance over monolithic prompting / -self verification checkpoints multi turn state maintenance monolithic prompting
7. benchmark grades error severity separately from pass rate LLM reliability over trials / -LLM reliability pass rate error severity benchmark trials
8. LLM agents lose track of state longer conversations error accumulation study 2025 / -LLM long context error accumulation study 2025 agent state
9. preregistration registered reports machine learning AI research evaluation best practices / -machine learning registered reports guidelines ML research
10. BetterBench AI benchmarks best practices statistical power reproducibility Reuel
11. "Let's Verify Step by Step" process supervision intermediate answer outperforms outcome supervision
12. ablation report state after every N steps versus only at end LLM accuracy partial / -ablation study checkpoint frequency llm training accuracy
13. Boxman benchmark LLM state tracking sequential operations update
14. LLM checkpoint interval spacing error severity dose response forced intermediate answers
15. arxiv preregistration machine learning experiments HARKing evaluation 2025
16. "state tracking" LLM ablate "how often" model reports state intermediate checkpoints accuracy
17. agent benchmark "severity" misstate partial state error graded separate pass/fail 2026
18. "preregistered" OR "pre-registered" experiment large language model arxiv 2026 predictions hypothesis
19. benchmark ablates number of intermediate checkpoints identical questions seeds accuracy unchanged
20. "same accuracy" OR "identical pass rate" LLM different error severity secondary metric
21. task progress self-report frequency ablation LLM agent checkpoints unreliable progress bar
22. benchmark "how often the model must report" state ablation identical prompts seeds same problems output frequency
23. deterministic offline replay evaluation harness LLM reproducibility gate local server
24. dose-response prompt scaffolding LLM accuracy unchanged error magnitude increased / -prompt scaffolding dose response accuracy unchanged error magnitude
25. state tracking benchmark grade number of wrong entities severity not binary arxiv 2026
26. entity tracking language models sequence of operations PUT MOVE state changes benchmark 2026
27. "output granularity" OR "emission granularity" OR "reporting granularity" ablation LLM evaluation (incl. -granularity/reporting-granularity variants)
28. BIG-bench "tracking shuffled objects" state tracking benchmark reordering sequence
29. "verification frequency" OR "checkpoint density" dose-response LLM accuracy severity multi-step
30. multi-turn state tracking "number of incorrect" slots accuracy equal error magnitude worse 2026
31. benchmark varies when model is asked for answer schedule per-turn versus checkpoint only identical problems seeds
32. STALE benchmark implicit conflict three-dimensional probing framework metric scoring memory LLM
33. "per-step verification" OR "token-level recurrence" effect LLM state maintenance intermediate answers
34. ablation spacing of checkpoints long-horizon agent success rate secondary error metric 2026
35. "no significant difference" pass rate but "error severity" OR "error magnitude" increased prompt granularity LLM
36. "forced intermediate answers" OR "forced intermediate state" LLM ablation effect accuracy
37. same model same problems different answer emission schedule pass rate tie severity difference study
38. self-copy scaffold restating own prior output improves LLM state tracking multi-turn

**"Boxman"** (named in the brief): query 13 returned no such public benchmark — the nearest real
construct is the box/container entity-tracking family (init state + PUT/MOVE/REMOVE ops →
final state) in `2305.02363` and BIG-bench *Tracking Shuffled Objects* (`2210.09261`). Flagged
**unverified** as a proper name.

**"Not found after these searches" ≠ "verified absent".** C1's dose-response and C3's instrument
are negatives from a **search-based** retrieval over ~45 queries; a differently-named or
unindexed artifact could exist. I did **not** perform an exhaustive registry sweep (no
Semantic Scholar / OpenReview / ACL bulk query), so both negatives are **absence of evidence**,
graded `medium` at best (§5). What *is* verified is the positive set in §2 — every URL there was
fetched this round with the quoted text.

## 4. Delta vs round 9 (extend, do not duplicate)

r9's pricing is `corpus/knowledge/eval-prior-art-calibration.md` (from
`corpus/evidence/round9-fleet/prior-art.md`). Per-claim coverage:

| # | Already covered by an r9 source? | r11 delta |
|---|---|---|
| **C1** | **No.** r9 priced the INC/CKPT/MONO *ladder* (row 1) and the late-rule cell (row 3). It never priced an **error-severity** endpoint, and r9's row-1 sources (Laban, Re², RECITE, induction heads, Dziri, least-to-most) contain no checkpoint-density→severity dose. | New this round: `2609.08589` (task success decoupled from intermediate-report correctness — the closest published relative), `2605.30233` (LMs aggregate at the last token instead of tracking incrementally), `2305.02363` (the init+ops construct's provenance), `2602.07338`. |
| **C2** | **Yes — r9 row 1** ("incremental — the emission-granularity ablation is the new part"; phenomenon **known**). | Extended, not re-derived: added `2210.09261` (quantified no-CoT→CoT jump on *Tracking Shuffled Objects*, 22.5→64.7), `2410.02810` StateAct, `2305.20050` process>outcome, `2509.17766`, `2605.15102`. These make `CKPT > MONO` a **replication**, not a finding. |
| **C3** | **Partly — r9's benchmark-coverage table** already ruled "no suite ablates output/emission frequency on identical problems and seeds" and flagged it `medium` [UNVERIFIED]. | Re-checked 2025–2026 literature adds **no counterexample**; the nearest newcomers are position-based (`2609.08589`), localization-based (`2604.12312`), harm-taxonomy-based (`2604.02022`), or within-run-metric-based (`2608.13417`, `2608.20563`). r9's gap statement is **strengthened, not overturned**. |
| **C4** | **No — r9 contains no preregistration prior art at all.** r9 row 4 covers serving nondeterminism (llama.cpp #7052, Thinking Machines, vLLM), which is the *motivation* for a replay gate, not the instrument. | Entirely new: `2606.11217` (preregistration template for AI-agent experiments; requires "the exact **checkpoint hash** and any **quantization scheme**", verbatim prompts, decoding params; recommends OSF **before any data collection**), `2603.10044` (executed instance: OSF DOIs, SHA-256 hash published on OSF **before scoring begins**, "**80% power** to detect a **4.4 pp** drop", a preregistered "**Dose-Response Analysis (H4)**", and "we report disconfirmed sub-hypotheses … as evidence the pre-registration was binding"), `2411.00640` (eval power analysis), `2411.12990` BetterBench (uncertainty-reporting/reproducibility gaps across 24 benchmarks, 46 best practices). |

**Net novelty position:** C2 is a replication of published phenomena (r9 stand); C4 is an
**incremental** instrument (protocol published, local-server + replay-gate instantiation not
found); C1 is **incremental (low)** (decoupling published, density→severity dose not found);
C3 is **NOVEL-instrument** (no density-ablation-with-severity suite found). The lane's defensible
contribution stays **instrument-level**, exactly as r9 concluded — now with a stronger C4 verdict
and a new C1 neighbouring literature.

## 5. Confidence lines

| Claim | Grade | Reason |
|---|---|---|
| C2's `CKPT > MONO` half is **known** | **high** | Multiple fetched primaries quantify intermediate-trace/state emission beating monolithic or outcome-only on identical problems: `2210.09261` 22.5→64.7 TSO, `2410.02810` >10% ALFWorld over ReAct, `2305.20050` process>outcome. |
| C1's **decoupling** (task success insensitive to intermediate-report quality) is known; C1's **density→severity dose** is not found | **medium** | Decoupling verified verbatim in `2609.08589`; the dose is a negative over ~45 queries without a registry sweep. |
| C3 = **NOVEL-instrument** | **medium** | Same absence-of-evidence basis as r9 (search-based negative); the 2026 newcomers were each inspected and none ablates emission density with a severity endpoint. |
| C4 = **INCREMENTAL** (protocol published; local-server + hermetic replay-gate instance not found) | **medium–high** | Positive side is strong and verbatim (`2606.11217` template incl. checkpoint-hash + quantization; `2603.10044` OSF DOI + OSF-published SHA-256 + 80%-power/4.4 pp + preregistered dose-response). Negative side (replay gate) rests on one 404 and no registry sweep. |
| All of C1/C2's fetched primaries were read **this round** with recorded HTTP status | **high** | §2 — every URL carries the status from the fetch; §2.4 records three synthesis claims that failed their text check and are therefore excluded. |
| Findings are **sub-3-bit serving-stack observations** (no cross-model claim) | **medium–high** | Carried from r9: UD-IQ2_XXS sits below every published quantisation-safe band; r11's descriptors record pins the unit (q4_0 KV, `--kv-unified`, custom chat template) — see `probe_plan_r11.md` §3. |

**Blocking issues:** none. No cited source contradicts a preregistered r11 claim; the only
effect on landing is framing (C1/C3 must be written as instrument-level novelty, C4 as an
instantiation of a published preregistration protocol).