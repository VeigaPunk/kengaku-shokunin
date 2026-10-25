# R32ConnSibling — sibling-overlap scan, round 32 claims

Role: leaf connector (UFO-FSD). Access date for every source opened: **2026-10-25**.
Scope: read-only scan of the 20 sibling lane repos under `/home/vgpnk/Projects/shokunin/`
(all `*-shokunin/` except kengaku itself) — `SKILL.md`, `PROVINCE.md`, `corpus/`
per the dispatch. No tools installed or updated (nothing was needed; grep/read only).
No production edits; this report is the only file written.

Claims in scope: C1 (benchmark grader semantics — Toolathlon scoring code, SWE-bench Pro V2
held since round 31, and the deterministic-grader-vs-LLM-judge survey frame), C2 (calibration
defect closures — internal to kengaku bytes, no sibling ground), C3 (public model catalog
freshness — HF `api/models` + OpenRouter `api/v1/models` schema re-probe).

## Fleet-wide negative evidence (strong tokens)

- `Toolathlon` / `toolbench` / `tau-bench` / `pass@1` / `gold patch` / `test patch`: **zero**
  hits in any sibling `SKILL.md`/`PROVINCE.md`/`corpus/`.
- `SWE-bench`: exactly one sibling occurrence — kotoba's routing table, which names kengaku as
  the owner (see §1).
- `G-Eval` / `MT-Bench` / `PandaLM` / `LLM-as-(a-)judge`: zero hits except lore's domain-local
  rejection rows (see §2).
- HF `api/models` + OpenRouter `api/v1/models` as *probed live catalog schemas*: present only in
  kengaku's own `SKILL.md:662` (round-9 probe provenance). No sibling has a probe or receipt for
  either public API schema (see §3).

## 1. Axis (a) — benchmark grader semantics / Toolathlon scoring code

Closest sibling surfaces, with non-absorption rulings:

- **chousa** — explicitly routes this ground to kengaku. `corpus/knowledge/scope-refusal-r12.md:22`
  maps `model quality`, `model evaluation(s)`, `model eval`, `model benchmark(s)`, `model scoring`,
  `llm quality/evaluation/eval`, `language model quality/evaluation` → `SCOPE_MODEL_QUALITY_ABSORBED`
  → kengaku. `corpus/knowledge/archived-export-intake.md:103` (RJ-03): "model-quality and benchmark
  claims are kengaku province" (MINT.md:14-18,46-47). `corpus/knowledge/claim-support-states-r24.md:77-79`:
  "No benchmark scores or model rankings are imported as claims — kengaku province"; its S006/S007
  arXiv citations are used *for method distinctions only*. Ruling: chousa is a *declared non-owner*;
  it neither holds nor builds grader-semantics ground. Non-absorption.
- **kagi** — its lessons inventory sibling verifiers and explicitly exclude kengaku's grader.
  `corpus/lessons/round-13.md:112`: "kengaku `grader.py` has a prediction score table … None
  implements an `R-…-…` row-id or score-cell contract, so nothing is duplicated".
  `corpus/lessons/round-14.md:148-149`: "kengaku `grader.py` (replays hard-coded report tables). All
  *adjacent*: different unit, none binds an entry to a re-runnable claim row." Ruling: kagi
  monitors but does not own any benchmark grader; its ground is its own citation-durability ledger.
  Non-absorption.
- **souji** — `corpus/SOURCES.md:127-128` (S107/S108) use "result grading" for their own Python
  JSON-decoder census semantics (RecursionError vs depth). Same word, different phenomenon — their
  tool's verdict contract, not any public benchmark's scoring code. Non-absorption.
- **mori** — "r1 grader / window grader" (`corpus/knowledge/silence-grading-r2.md:19-29`,
  `lane-silence-r2.md:12-30`) is the fleet watchdog's lane-silence window detector, not benchmark
  grading. Non-absorption.
- **kumitate / kasegi / tsukuroi / mado / tabi / audio / game-dev-2d/3d / kaidoku / revenger /
  tameshi / kake / kotodama** — no hits on any axis-(a) token; their "judge/evaluator/grader"
  vocabulary is internal gate/runtime tooling (e.g. kumitate's native Rust ParetoGate judge,
  `SKILL.md:20,231-241,346-350`; kasegi's bounty `K3_SEATS=['judge','planner']`,
  `SKILL.md:327,361-376,997-1001`; tsukuroi's revision-binding judge, `SKILL.md:1948-1994`;
  mado's chain-integrity rows, `SKILL.md:1442-1443`; tabi's "trend grading" L0 ruling,
  `corpus/README.md:433-434`). Zero intersection with benchmark grader semantics.

**Axis (a) finding:** no sibling owns or is building Toolathlon/SWE-bench Pro V2 scoring-code
ground. The only fleet-relevant grader bytes are kengaku's own (kagi's lessons cite them as such),
and two siblings (chousa, kotoba) record that benchmark/eval claims are kengaku province.

## 2. Axis (b) — LLM-as-judge survey structure

- **lore** — `corpus/SOURCES.md:25` (S017): "an automated LLM-as-judge pipeline for scalable and
  auditable consistency evaluation" (§2.3, arXiv 2603.05890) — **REJECTED** as authority on in-world
  canon; `corpus/lessons/round-103.md:84-85,169` documents the same. Ruling: domain-local rejection
  rows for fiction continuity (a *use* stance), not a survey of LLM-judge literature; none of the
  survey-frame structure C1 adds (deterministic-grader vs LLM-judge separation across benchmarks)
  exists there. Non-absorption.
- **kotoba** — `corpus/knowledge/skill-eval-artefacts-round70.md:25-29` (F2, F5) digests the Agent
  Skills vendor docs' eval artifacts (`grading.json`/`timing.json`/`benchmark.json`; "scripts are
  more reliable than LLM judgment for mechanical checks"); `corpus/lessons/round-70.md:183-187`
  records a wording fix where a scout called an LLM judge "the fallback" vs the page's "the simplest
  approach". Ruling: a vendor-doc digest about *skill* eval artifacts, not a survey of LLM-as-judge
  structures; C1's survey frame targets benchmark grading entries and is not present. Non-absorption.
- **kumitate** ("native judge"), **tsukuroi** (evaluator/judge selftest), **chousa** (verifier
  "judges span identity, not meaning", `SKILL.md:463-491,488-491`), **game-dev-3d** (verb sense,
  `SKILL.md:76-80`), **kake** (verb sense, `SKILL.md:137-141,579-583`), **mado** (`SKILL.md:1442`),
  **kasegi** (`SKILL.md:50-52` mission "L1 judge prompt"), **audio** ("canonical judge" = fleet Rust
  runtime, `corpus/live/r84-scribe/labrat-r84-headline-advisory.txt:47`), **tameshi** (interop
  judge, `PROVINCE.md:117-118`), **kaidoku** (`SKILL.md:737-740`), **mori**, **tabi**, **souji**,
  **kotodama**, **revenger** — all internal adjudication/gate vocabulary; no survey structure.

**Axis (b) finding:** no sibling holds an LLM-as-judge survey. Nearest neighbors (lore, kotoba)
are single-domain rejection rows / vendor-doc digests, disjoint from C1's survey frame.

## 3. Axis (c) — public model catalog freshness (HF/OpenRouter API schema)

- **kama** — the closest surface, and deliberately not the same claim. kama probes `/v1/models`
  **on local serving endpoints** (llama.cpp, Ollama, vLLM, SGLang, Alibaba Cloud EAS/ACK) for
  *served-model identity/readiness*: `SKILL.md:75-76,132-136,152-155,164-165,171-177,223,254-258,518-529,552-556,562-576,686-689`;
  `PROVINCE.md:11-15` (served-model-id reconciliation, liveness/readiness probe conventions);
  `corpus/SOURCES.md:13-14,21-25,33,51-53,209,211,228-229` (S001/S002, S009-S012, S021, S039-S041,
  S206, S223, community sweep). Its one Hugging Face row (S039, `SOURCES.md:51`) is a *file-identity*
  row for a pinned GGUF fixture — not the `api/models` schema, no freshness probe, no schema-delta
  receipt. Ruling: kama's ground is endpoint identity on local servers; C3's ground is the public
  catalog schema probes. Disjoint surfaces; no absorption either way. Non-absorption.
- **kagi** — `corpus/surface-census.tsv:40` + `corpus/knowledge/handler-on-disk-state.md:35`
  record a cached *public model catalog* from opencode (`xdg-cache/opencode/models.json`, 0600,
  222 providers / 7865 models) — a tool cache inventory, not an API-schema probe;
  `corpus/transcript-scan.sh:89` + `corpus/knowledge/credential-isolation.md:18-21` use OpenRouter
  only as a credential-prefix/env-var cut. Ruling: cache + secret hygiene; no catalog-schema ground.
  Non-absorption.
- **kotoba** — `corpus/knowledge/sibling-citation-routing-round16.json:764,844,2255` resolves tokens
  for `corpus/knowledge/open-model-catalogs.md` — i.e. kotoba's verifier treats kengaku's catalog
  entry as a citable kengaku artifact; it does not hold or probe the catalogs itself. Non-absorption.
- All other siblings: zero hits on `api/models`/`api/v1/models`/OpenRouter/HuggingFace schema
  probes ("catalogs" in kotodama/chousa/mori corpora is museum/excavation/journal vocabulary).

**Axis (c) finding:** no sibling probes HF `api/models` or OpenRouter `api/v1/models` schemas or
holds a freshness claim over them. kama (local endpoint identity) and kagi (tool cache/credentials)
are the only adjacent surfaces, both non-overlapping.

## Synthesis

- No sibling owns or is building any of the three claim grounds. The fleet's own routing records
  the same split: chousa `scope-refusal-r12.md:22` and `archived-export-intake.md:103`; kotoba
  `sibling-overlap-census-round49.md:78` (kengaku = "eval design, benchmark selection, offline
  replay grading … interval-calibrated verdicts"); kengaku `webarena-task-spec-audit.md:164-166`
  ("Benchmark evaluation stays kengaku … general research method stays chousa, reusable testing
  patterns stay tameshi, prompt-writing advice stays kotoba, actual web-property operations stay
  kake").
- kagi's round-13/14 lessons independently rule that kengaku's `grader.py` is not duplicated by any
  sibling verifier — direct precedent for the same conclusion about C1's grader-semantics bytes.
- C2's defect closures read only kengaku round bytes and its own plans/SKILL.md; no sibling file
  intersects R1-R7.

VERDICT: no-contest
