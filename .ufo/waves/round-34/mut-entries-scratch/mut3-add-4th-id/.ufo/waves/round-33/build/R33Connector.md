# R33Connector — Sibling-Overlap Scan & Connector Synthesis

Round 33, hyaku run 7, 2026-10-25.
Role: UFO-FSD connector (`R33Connector`).
Report target: `.ufo/waves/round-33/build/R33Connector.md`.
Lane repo: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

VERDICT: connector-clean

---

## 1. Scoped Findings on Core Questions

### (a) Ownership of round-33 core concepts

1. **Benchmark grader semantics:**
   - **Owner:** `kengaku-shokunin` uniquely owns LLM/model evaluation, benchmark selection, and grader semantics (`kengaku-shokunin/PROVINCE.md:3`, `SKILL.md:3`, and round-28/29 admissions at `PROVINCE.md:194-222`).
   - **Siblings:** Every sibling explicitly refuses or routes out model evaluation: `kama` refuses model quality/eval (`kama-shokunin/PROVINCE.md:40`, `SKILL.md:27`); `kasegi` routes LLM eval to kengaku (`kasegi-shokunin/PROVINCE.md:50`); `kumitate` excludes eval craft, routing model serving to kama and method to chousa (`kumitate-shokunin/PROVINCE.md:27`); `kotoba` keeps prompt craft and routes measured capability effects to kengaku (`kotoba-shokunin/PROVINCE.md:59`, `SKILL.md:10-13`); `kagi` routes eval to kengaku (`kagi-shokunin/PROVINCE.md:67`); `chousa` explicitly refuses model-quality or evaluation claims (`chousa-shokunin/PROVINCE.md:10-11`, `SKILL.md:10-11, 58`); `souji` and `tabi` claim no evaluation domain.
   - **Verdict:** Unowned by any sibling; held exclusively by kengaku.

2. **Source-adoption gates:**
   - **Owner:** Fleet census and SOURCES contract-v1 are fleet-wide standards governed at the protocol/integrator level (`kengaku-shokunin/PROVINCE.md:139, 227`). General research method and claim verification stay with `chousa` (`chousa-shokunin/PROVINCE.md:5-8`, `SKILL.md:8-12`).
   - **Lane-local gates:** The pre-append adoption gate `plans/sources_adopt.py` and counter `plans/adoption_check.py` are lane-local operability instruments (`kengaku-shokunin/PROVINCE.md:224-228`) that compose with the fleet census without superseding it. Sibling lanes have their own local gate equivalents (`kagi-shokunin/PROVINCE.md:55` `sources-census.sh`, `kumitate-shokunin/PROVINCE.md:15` `sources-check.mjs`).
   - **Verdict:** No sibling owns kengaku's lane-local source-adoption gates; the underlying research method belongs to chousa and registry authority belongs to the fleet census.

3. **Public model-catalog probing:**
   - **Owner:** `kengaku-shokunin` has governed public model catalog endpoints (`https://huggingface.co/api/models`, `https://openrouter.ai/api/v1/models`) since round 14 (`kengaku-shokunin/PROVINCE.md:17, 163`, `corpus/knowledge/open-model-catalogs.md`).
   - **Siblings:** `kama` owns local model-serving runtime inspection (`llama-server`, loopback ports 8080/34113; `kama-shokunin/PROVINCE.md:3, 10-15`) and explicitly refuses remote web surfaces (`kama-shokunin/PROVINCE.md:40-43`); `kake` owns web properties, but `kengaku-shokunin/PROVINCE.md:33, 143` confirms the shared word "probe" carries no scope; `tabi` drives real browsers via CDP and handles dynamic web interactions (`tabi-shokunin/PROVINCE.md:3-14`), not public REST catalog APIs.
   - **Verdict:** Unowned by any sibling; held by kengaku.

---

### (b) Sibling contest analysis

Does any sibling contest round 33's frozen claim scope (C1 coverage, C2 calibration, C3 freshness)?
- **C1 (Coverage):** Admitting `corpus/knowledge/benchmark-grader-semantics.md` under S103 (Toolathlon `tasks/finalpool/ab-testing/evaluation/main.py`) and S104 (arXiv 2412.05579v2), with S093 updated in `used-by`. Sibling domain boundaries surveyed (kama, kasegi, kumitate, kotoba, kagi, chousa, souji, tabi) show zero competing claims on benchmark grader code analysis or LLM-as-judge survey literature.
- **C2 (Calibration):** Closing six routed defects N1–N6 (`.ufo/waves/round-32/` git tracking, SCORECARD Round 32, fleet report round-31/32 errata, round-30/31 lesson line references and S086 status). All six are lane-internal or kengaku fleet-report errata; no sibling governance is modified or contested.
- **C3 (Freshness):** Live re-probing HF and OpenRouter public APIs with raw JSON capture and sha256 digests. This touches public REST endpoints outside kama's local-serving loopback boundary and outside tabi's browser/CDP boundary.
- **Verdict:** `VERDICT: connector-clean` (0 contests across all 8 surveyed siblings).

---

### (c) Sibling report-outs (path:line anchors)

Facts in round 33's work that touch adjacent sibling domains, reported out rather than absorbed:

1. **Local model serving & endpoint runtime:** Serving-plane runtime health and loopback listener inspection belong to kama (`../kama-shokunin/PROVINCE.md:10-15`, `../kama-shokunin/SKILL.md:8-9`), while flag-change authority stays unowned/integrator (`kengaku-shokunin/PROVINCE.md:24-25, 136`).
2. **Grader harness execution & retry semantics:** Multi-agent operational failure taxonomy, execution idempotency, and client-side retry/timeout budgets belong to kumitate (`../kumitate-shokunin/PROVINCE.md:22`, `../kumitate-shokunin/SKILL.md:114-129`); kengaku keeps only static benchmark grader comparison semantics (`benchmark-grader-semantics.md:57-60`).
3. **Model routing & fallback chains:** Seat route resolution, model alias resolution, and fallback chains belong to kumitate (`../kumitate-shokunin/SKILL.md:284-302`, `../kumitate-shokunin/PROVINCE.md:27`); kengaku keeps public model catalog schema/field metadata only.
4. **Harness storage credentials & authentication:** Machine credential custody, secret tokens, and vault lifecycle belong to kagi (`../kagi-shokunin/PROVINCE.md:3, 27-30`, `../kagi-shokunin/SKILL.md:14-18`); kengaku observes only static AST control-flow fall-through (failing closed on absent credentials; `benchmark-grader-semantics.md:52-55`).
5. **Research method & citation verification:** Question framing, source hierarchy, citation chaining, and claim verification method belong to chousa (`../chousa-shokunin/PROVINCE.md:5-8`, `../chousa-shokunin/SKILL.md:8-12`); kengaku applies them to LLM evaluation domain sources and reports research-method findings out.
6. **Prompt craft & trigger fidelity:** Prompt craft rules, system prompt framing, and trigger fidelity belong to kotoba (`../kotoba-shokunin/PROVINCE.md:12-13`, `../kotoba-shokunin/SKILL.md:10-14`); kengaku retains only measured capability effects and static grader code evaluation.
7. **Workspace hygiene & artifact lifecycle:** Fleet repository hygiene, dead worktree pruning, and removal receipting belong to souji (`../souji-shokunin/PROVINCE.md:8-17`, `../souji-shokunin/SKILL.md:7-10`); kengaku tracks its own lane-internal wave tree (N1) without assuming fleet cleanup authority.
8. **Browser execution & dynamic interaction:** Real browser driving, CDP session discipline, and dynamic web capture belong to tabi (`../tabi-shokunin/PROVINCE.md:6-14`, `../tabi-shokunin/SKILL.md:8-11`); kengaku retains static benchmark spec audits and configuration projections.

---

### (d) arXiv survey adoption vs chousa research-method scope

**Finding:** Adopting S104 (arXiv 2412.05579v2, "A Survey on Large Language Model (LLM)-as-a-Judge") does **not** duplicate chousa's research-method scope.
- **Domain distinction:** S104 is primary literature on the *LLMs-as-judges paradigm* (evaluator architectures, meta-evaluation vs methodology), which is squarely inside kengaku's LLM evaluation domain (`kengaku-shokunin/PROVINCE.md:3, 20`). Chousa explicitly refuses model-quality and evaluation claims (`../chousa-shokunin/PROVINCE.md:10-11`, `../chousa-shokunin/SKILL.md:10-11, 58`).
- **Usage boundary:** Kengaku cites S104 exclusively for domain-level grading taxonomy in `corpus/knowledge/benchmark-grader-semantics.md:62-73` (distinguishing deterministic state comparison from LLM-as-judge meta-evaluation). It does not derive, assert, or govern general research methods, source ladders, or citation resolution rules.
- **Methodological compliance:** Kengaku verifies S104 using chousa's established method (primary source pin, byte-located quote under 25 words, access date recording) without usurping chousa's authority over the research-method craft.

---

## 2. Sibling Overlap Table

| Sibling | Domain | Round-33 Overlap Surface | Contest Status | Boundary & Report-Out Anchor |
|---|---|---|---|---|
| **kama** | Local model serving & endpoint health | C3 public model catalogs (HF/OpenRouter) vs local loopback endpoints | Clean (no contest) | Local serving discovery belongs to kama (`kama-shokunin/PROVINCE.md:10-15`); remote catalog API probing belongs to kengaku; serving flag authority stays unowned (`kengaku-shokunin/PROVINCE.md:24-25`). |
| **kasegi** | Bounty & security research | None (domain disjoint) | Clean (no contest) | Kasegi routes LLM eval to kengaku (`kasegi-shokunin/PROVINCE.md:50`). |
| **kumitate** | Orchestration & dispatch runtime | Toolathlon evaluator retry wrapper (`retry.py`) & failure behavior in C1 | Clean (no contest) | Multi-agent failure taxonomy, timeout dead-letters, and retry budgets belong to kumitate (`kumitate-shokunin/PROVINCE.md:22`, `SKILL.md:114-129`); kengaku holds static grading code interpretation only (`benchmark-grader-semantics.md:57-60`). |
| **kotoba** | Prompt & skill craft | Evaluator prompt/judge scan in C1 (`main.py`) | Clean (no contest) | Prompt craft rules belong to kotoba (`kotoba-shokunin/PROVINCE.md:12-13`); kengaku keeps measured capability effects and static grading code interpretation (`kengaku-shokunin/PROVINCE.md:138`). |
| **kagi** | Secrets & vault ops | Cloud logging credential fall-through in C1 (`main.py`) | Clean (no contest) | Credential custody and vault ops belong to kagi (`kagi-shokunin/PROVINCE.md:3, 27-30`); kengaku observes only static AST control-flow fall-through without holding secrets (`benchmark-grader-semantics.md:52-55`). |
| **chousa** | Deep-research method (調査) | arXiv 2412.05579v2 (S104) literature adoption in C1 | Clean (no contest) | Research method, source hierarchy, and verification belong to chousa (`chousa-shokunin/PROVINCE.md:5-8`); chousa refuses model-quality claims (`chousa-shokunin/PROVINCE.md:10-11`); S104 evaluation taxonomy belongs to kengaku. |
| **souji** | Fleet repository & workspace hygiene | N1 git-tracking of `.ufo/waves/round-32/` tree in C2 | Clean (no contest) | Fleet repo hygiene belongs to souji (`souji-shokunin/PROVINCE.md:8-17`); souji refuses live lane work products (`souji-shokunin/PROVINCE.md:42`); lane-internal wave history tracking is kengaku's own responsibility. |
| **tabi** | Browser & web-interaction craft | Public REST catalog fetching in C3 vs browser driving | Clean (no contest) | Driving real browsers and CDP interaction belong to tabi (`tabi-shokunin/PROVINCE.md:6-14`); headless public REST API catalog probing belongs to kengaku. |

---

## 3. UFO-FSD Connector Proposal

### Synthesis: Hermetic Tip-Receipt Verifier Synthesis (Q22 Enforcement)

- **Evidence:**
  1. `considerthese/2026-10-25.md` Lesson 3 documented round 31 defect D3: `corpus/evidence/round31/gate-cli-exits.txt` at tip was written with invalid relative paths (`can't open file` / `exit=2`), while SCORECARD C3 asserted clean execution. Proposal 2 in that reflection established: *"a receipt is only evidence if something re-runs it at the tip"*, formalised as `QUALITY.md` Q22 (`plans/round-33-claims.md:154-156`).
  2. In round 33, three separate verification instruments operate in silos:
     - `plans/round33_defects.py --lane .` checks N1–N6 (C2).
     - `plans/round33_c1_verify.py --lane .` and `plans/adoption_check.py` check adoption and AST tolerance (C1).
     - `plans/catalog_probe.py --verify --lane .` checks offline catalog numbers against committed raw JSON (C3).
  3. Sibling boundary fences require that kengaku's offline verification never accidentally triggers network requests (violating docs-only policy), loopback port bindings (colliding with kama), or credential probes (colliding with kagi).

- **Affected axes:**
  - **Calibration (C2):** Directly improved by preventing receipt-to-reality skew and mechanically enforcing Q22 across all round-33 deliverables.
  - **Coverage (C1) & Freshness (C3):** Preserved and protected against post-integration regression without expanding runtime scope or inflating scores.

- **Proposed move:**
  Synthesize the tip-verification pass by having the final round-33 defect verification script (`plans/round33_defects.py` or the L1 integration wrapper) execute `plans/catalog_probe.py --verify --lane .` and `plans/round33_c1_verify.py --lane .` as mandatory sub-checks of the tip calibration state. If any offline re-derivation fails or produces empty/unbound output, C2 fails closed with exit 1. This binds C1 adoption truth and C3 catalog freshness directly into C2 calibration proof, guaranteeing that all receipts re-derive mechanically from committed bytes at the final tip before closeout.

- **Risks:**
  - *Risk:* Coupling could cause a C3 network/probe artifact issue to report as a C2 calibration defect.
  - *Mitigation:* The verification mode (`--verify`) is strictly offline and reads only committed bytes (`hf.raw.json`, `or.raw.json` ≤ 64 KiB) and `SHA256SUMS`. It requires zero network connectivity and zero runtime services, ensuring hermetic local execution.

- **Verification:**
  Execute `python3 plans/round33_defects.py --lane .` at tip after landing commits; verify that defect count reaches 0, that `catalog_probe.py --verify` exits 0 with `hf_models` and `or_models` matching raw capture digests, and that `round33_c1_verify.py` exits 0 with `checks=8 defects=0`.
