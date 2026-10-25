# Cross-Lane Frontier Map: Terminal-Bench 2.0, Grading Code, Contamination, and Model Catalogs

Seat: `R34ConnFrontier`
Role: UFO-FSD Connector
Round: 34 (hyaku run 7, 2026-10-25)
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`

## 1. Sibling Scan Evidence

A complete scan of all 20 sibling lanes in `/home/vgpnk/Projects/shokunin/*-shokunin` (`chousa`, `kama`, `kotoba`, `kumitate`, `tameshi`, `kaidoku`, `kagi`, `kasegi`, `kotodama`, `mado`, `mori`, `tsukuroi`, `tabi`, `souji`, `kake`, `revenger`, `lore`, `audio`, `game-dev-2d`, `game-dev-3d`) was conducted over `PROVINCE.md`, `SKILL.md`, `README.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*.md`, and round-34 reports.

Eight (8) sibling lanes name the four frontier topics that kengaku narrows or references this round (`Terminal-Bench 2.0`, `benchmark grading code`, `contamination cards`, `model catalogs`):

| Sibling Lane | Frontier Topic(s) Named | Concrete Sibling Artifact / Pointer | Declared Ground & Scope Boundary | Touches Sibling Ground? |
|---|---|---|---|---|
| **kumitate** | Terminal-Bench 2.0; model catalogs | `.ufo/waves/round-61/w2/Audit14.md:43` (cites arXiv:2512.08296v3 §4.1 listing Terminal-Bench); `corpus/knowledge/queue-and-claim.md:140` ("model-catalog preflight") | Owns orchestration & tooling (OMP task/hub, ufo-fsd runtime, dispatch queue/preflight). Refuses domain evaluations and model serving. | **No** (uncontested) |
| **kotoba** | Terminal-Bench 2.0; benchmark grading code; contamination cards | `.ufo/waves/round-71/receipts/census-after.txt:28` (S100 URL); `corpus/README.md:133` & `knowledge/skill-eval-artefacts-round70.md:28` (`grading.json`); `knowledge/sibling-description-rewrites-round8.md:346` | Owns prompt & skill craft (SKILL.md/AGENTS.md quality, skill-eval run artifacts for tool affordances). Explicitly marks kengaku adjacent for model evaluation. | **No** (uncontested) |
| **kaidoku** | benchmark grading code | `corpus/knowledge/2026-10-22-r28-evm-heldout-selector-naming.md:9` ("scoring code" for held-out selector naming rules) | Owns reverse engineering of shipped binary artifacts with REA (PE/ELF/EVM bytecode). Scoring code refers to EVM ground-truth rules, not LLM benchmark task graders. | **No** (uncontested) |
| **tameshi** | benchmark grading code; contamination cards | `corpus/knowledge/regression-tally-completeness.md:60` ("scoring code" for regression tallies); `corpus/knowledge/executor-test-sufficiency.md:20` ("contamination statement — what executor read") | Owns verification-fixture craft (hermetic suites, mutation testing, gate scripts). Refuses product behavior or external domain evaluations. Contamination refers to test-runner oral context leakage. | **No** (uncontested) |
| **kama** | model catalogs | `PROVINCE.md:11-12`, `corpus/knowledge/consumer-registry.md:171`, `cross-lane-scope.md` (`GET /v1/models` served-model-id reconciliation, `endpoint-consumers.tsv`) | Owns local model serving & endpoint health (local loopback listeners `:8080`, `:34113`, baseURL drift). Explicitly **refuses** model quality/eval (routed to kengaku). | **No** (uncontested) |
| **kagi** | model catalogs | `corpus/knowledge/handler-on-disk-state.md:35` (`xdg-cache/opencode/models.json`, cached public model catalog of 222 providers / 7865 models) | Owns secrets & vault ops (credential hygiene, auth flows, token isolation). Catalog file is tracked solely for on-disk credential hygiene, not eval semantics. | **No** (uncontested) |
| **kasegi** | model catalogs (METI) | `corpus/knowledge/japanese-domestic-disclosure-workflow.md:93` (IPA & METI domestic vulnerability coordination) | Owns bounty & security research. METI reference is strictly coordinated vulnerability disclosure, not generative AI model evaluation programmes (GENIAC). | **No** (uncontested) |
| **kotodama** | contamination cards | `corpus/README.md:400` (`purity-pollution-boundary-systems.md`) | Owns linguistic-cultural worldbuilding. Uses purity/pollution/contamination strictly as cultural/anthropological fictional world systems. | **No** (uncontested) |

*(Note: `chousa`, `game-dev-3d`, and `mado` explicitly record kengaku in their `PROVINCE.md` refusal clauses: chousa-shokunin/PROVINCE.md:10-11 `Refuses: model-quality or evaluation claims (→ kengaku)`; game-dev-3d-shokunin/PROVINCE.md:17 `LLM/model research and evaluation belong to kengaku-shokunin`; mado-shokunin/PROVINCE.md:12 `Refuses: model quality (→ kengaku)`).*

## 2. Topic-by-Topic Ground Analysis

1. **Terminal-Bench 2.0**:
   - *Kengaku move:* C1 opens pinned task `protein-assembly` at Harbor commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (`tests/test.sh` + `tests/test_outputs.py`) and grounds it against expected environment inputs (`antibody.fasta` + `pdb_ids.txt`).
   - *Sibling ground:* Neither `kumitate` nor `kotoba` nor any other sibling claims ownership over Terminal-Bench 2.0 task-spec audits or scoring code.
   - *Contested scope:* None.

2. **Benchmark Grading Code**:
   - *Kengaku move:* C1 audits deterministic static sequence assertions (`Seq.translate()`, ordered component indexing, sliding 50-nt GC window 30–70%, pass/fail binary reward writing `echo 1/0 > /logs/verifier/reward.txt`) distinct from LLM-as-judge or verifier execution models.
   - *Sibling ground:* `kotoba` evaluates prompt/skill affordances; `kaidoku` reverses bytecode; `tameshi` builds verification harnesses. No sibling audits external benchmark task graders.
   - *Contested scope:* None.

3. **Contamination Cards**:
   - *Kengaku move:* In round 34, contamination cards remain explicitly **OPEN** on the frontier. C1 explicitly disclaims contamination checks; negative space in `terminal-bench-task-grader.md` notes no contamination measurement is performed.
   - *Sibling ground:* Sibling uses of "contamination" (`tameshi` test-runner context isolation, `kotodama` cultural pollution) are orthogonal.
   - *Contested scope:* None.

4. **Model Catalogs**:
   - *Kengaku move:* Adopts quarantine rows S108/S109 into `provider-selfreport-eval-limits.md` (NEC技報 RAKUDA evaluation limits and METI GENIAC hold-out benchmarks) and maintains open model catalog API documentation (`open-model-catalogs.md`: Hugging Face / OpenRouter APIs).
   - *Sibling ground:* `kama` owns local loopback serving ports and baseURL drift, refusing model eval; `kagi` tracks on-disk model json for secret hygiene; `kumitate` handles task routing preflight; `kasegi` coordinates security vulnerability disclosure.
   - *Contested scope:* None.

## 3. Connector Synthesis & Bounded Move

- **Evidence:** `R34CriticFrontier.md` observed two critical friction points: (1) round-33 frontier text was modified non-verbatim instead of preserving historical text and appending a clean round-34 narrowing; and (2) round-31 frontier text already stated "the Terminal-Bench 2.0 axis-E cell is filled by this entry" (`corpus/README.md:278`), creating a potential coverage-map ambiguity between harness-level verifier execution and task-level grader semantics. Furthermore, `R34PriorArtTB2.md` established that static sequence checking is existing prior art (DNA Chisel), so C1's move is strictly coverage, not novelty.
- **Affected Axes:** `coverage` (C1) and `calibration` (C2).
- **Proposed Move:**
  1. *Clean Ledger Separation:* In `corpus/README.md`, formulate the round-34 coverage entry as "Task-level benchmark grader semantics: protein-assembly (`knowledge/terminal-bench-task-grader.md`; S105–S107)", explicitly disambiguated from round-31's harness verifier execution entry (`knowledge/benchmark-verifier-execution-model.md`; S092, S093, S100).
  2. *Verbatim Historical Frontier Preservation:* Preserve the round-33 historical frontier bullet verbatim; append the round-34 narrowing as a distinct sub-bullet explicitly retaining all required open clauses (`SWE-bench Pro V2 graders beyond round-31`, `runtime task validity`, `hosted judges`, `contamination`) as mandated by `plans/round34_c1_verify.py:REQUIRED_FRONTIER`.
  3. *Cross-Lane Handoff Clarity:* Formally record in the round-34 report-outs that skill evaluation artifact patterns (`grading.json`) belong to `kotoba`, and local served-model discovery (`/v1/models`) belongs to `kama`, ensuring zero cross-lane domain drift.
- **Risks:** The counter check V6 in `round34_c1_verify.py` requires all substrings in `REQUIRED_FRONTIER` and the exact commit hash `PIN` to appear in the frontier section. The proposed formatting guarantees exact matching.
- **Verification:**
  - `python3 plans/round34_c1_verify.py --lane .` produces `checks=8 defects=0`.
  - `python3 plans/round34_defects.py --lane .` produces `checks=8 defects=0`.

VERDICT: conn-frontier (8 named, contested 0)
