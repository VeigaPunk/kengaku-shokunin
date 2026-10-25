# FxConnector — post-draft sibling-overlap verification (round 32)

Role: leaf connector (UFO-FSD). Access date for every source opened: **2026-10-25**.
Scope: read-only re-scan of the 20 sibling lane repos under `/home/vgpnk/Projects/shokunin/`
(all `*-shokunin/` except kengaku) for overlap with (a) the drafted
`corpus/knowledge/benchmark-grader-semantics.md` entry (C1), (b) the C3 catalog refresh
(HF `api/models` + OpenRouter `api/v1/models`, `open-model-catalogs.md`), and (c) the round-32
claims wording. This is the post-draft pass: the entry and rows are on disk uncommitted and the
build-wave reports are about to land. No tools installed or updated (grep/read only; nothing
needed). No production edits; this report is the only file written.

Method: (1) full-tree greps of all 20 sibling repos for strong tokens from the draft entry, the
catalog refresh, and the frozen claims wording; (2) greps restricted to live surfaces
(`SKILL.md`, `PROVINCE.md`, `corpus/knowledge/`, `corpus/SOURCES.md`, `considerthese/`) to
separate active claims from archived wave state; (3) targeted re-reads of every adjacency surface
found. Every negative is a zero-hit over the scanned paths, not a skim.

## 1. Axis C1 — grader semantics (Toolathlon scoring code, SWE-bench Pro V2, judge survey frame)

Frozen/claim tokens scanned (full tree, all 20 siblings): `Toolathlon`, `toolbench`,
`tau-bench`, `ab-testing`, `validate_record_data`, `expected_ratio.csv`, `9be8d8fe`
(Toolathlon pin), `SWE-bench_Pro-os`, `v2/tasks`, `66f92766` (SWE-bench Pro V2 pin),
`grader-semantics`, `scoring code`, `deterministic grader`, `grading semantics`,
`2412.05579`, `LLM-as-judge`, `LLMs-as-judges`, `PandaLM`, `G-Eval`, `MT-Bench`.

Result: **zero siblings claim any of this ground.** All hits are adjacency or verbatim-mismatch
evidence, each ruled non-absorption:

- `tau-bench` occurs in one sibling, kumitate, inside an arXiv abstract for a durable-execution
  safety paper (SOUNDGATE), **not** Toolathlon or any benchmark grader:
  `kumitate-shokunin/.ufo/waves/round-60/build/ScoutArxivStopMeansStop/body.html:30` ("on
  naturalistic tau-bench episodes models serialize writes …"). Toolathlon is a different
  benchmark; the draft entry does not claim tau-bench.
- `ab-testing` occurs in one sibling, kake, as a Cloudflare Functions docs sidebar link ("A/B
  testing with middleware"): `kake-shokunin/.ufo/waves/round-46/sources/S135.html:134`. This is
  a vendor docs page for a web-functions framework, not Toolathlon's `ab-testing` task family.
- `SWE-bench` occurrences (none claim grader code):
  - kumitate round-35: Anthropic multi-agent research-system docs — the row explicitly EXCLUDES
    the tool-specific "SWE-bench figures": `kumitate-shokunin/.ufo/waves/round-35/build/ScribeSrcBuildingAgents.md:35`.
  - kumitate round-59/61: arXiv 2512.08296 (multi-agent configuration effects) names
    "SWE-bench Verified" as one of six benchmarks in a *paper quote*; no scoring code, no
    compare semantics: `kumitate-shokunin/.ufo/waves/round-61/w2/Audit14.md:43-44,64-66`.
  - kotodama round-65 connector names kengaku's OWN SWE-bench evidence note
    (`corpus/evidence/round28-calibration/prior-art-reopen.txt`) as an evaluation-calibration
    access note — an attestation of kengaku's holding, not a competitor:
    `kotodama-shokunin/.ufo/waves/round-65/w1/ConnectorSiblings.md:56`.
  - `SWE-bench_Pro-os`, `v2/tasks`, `66f92766`, `scaleapi`, `webarena…` grader reading: zero.
- LLM-as-judge mentions (none is the C1 survey frame):
  - chousa round-29 falsify: `"via LLM-as-a-judge"` is used to report a missing verbatim quote
    in its own lesson — a freshness finding: `chousa-shokunin/.ufo/waves/round-29/falsify/HeldOut02.md:25`.
  - kumitate round-41: MAST paper annotation pipeline ("LLM-as-a-judge" accuracy 94%, Kappa
    0.77) — a paper reading about dataset annotation, not a judge survey:
    `kumitate-shokunin/.ufo/waves/round-41/falsify/ScoutMAST.md:140`.
  - kumitate round-58: LangSmith vendor docs sidebar ("How to define an LLM-as-a-judge
    evaluator") — vendor tool docs: `kumitate-shokunin/.ufo/waves/round-58/build/ScoutLangGraph/body.html:1859`.
  - lore: S017 (ConStory-Checker, arXiv 2603.05890) is REJECTED as authority — domain-local
    rejection rows, explicitly not a survey:
    `lore-shokunin/corpus/SOURCES.md:25`; `lore-shokunin/corpus/lessons/round-103.md:84-85`.
  - `2412.05579` (the exact arXiv id C1's S097 cites): zero sibling hits.
- Fleet routing confirms non-ownership (unchanged since the pre-draft scan):
  - chousa maps `model quality/evaluation(s)/eval/benchmark(s)/scoring` and `llm
    quality/evaluation/eval` → `SCOPE_MODEL_QUALITY_ABSORBED` → kengaku:
    `chousa-shokunin/corpus/knowledge/scope-refusal-r12.md:22`; selftest now also pins `llm
    benchmark|llm benchmarks|llm scoring` at `chousa-shokunin/corpus/README.md:680-681`.
  - chousa intake RJ-03: "model-quality and benchmark claims are kengaku province":
    `chousa-shokunin/corpus/knowledge/archived-export-intake.md:103`; echoed in
    `chousa-shokunin/corpus/knowledge/claim-support-states-r24.md:67-68`.
  - kagi's round-13/14 lessons rule kengaku's `grader.py` is duplicated by no sibling verifier
    (precedent recorded in the pre-draft scan; no grader-semantics bytes today).

## 2. Axis C3 — public model catalog freshness (HF `api/models`, OpenRouter `api/v1/models`)

Tokens scanned (full tree): `openrouter`, `openrouter.ai`, `huggingface.co/api/models`,
`api/models`, `api/v1/models`, `catalog_probe`, `catalogs_probe`, `schema-delta`,
`verified-at: 2026-10-25`, `S101`, `S102`, `open-model-catalogs`, `model-catalogs`.

Result: **no sibling probes either public catalog schema or holds a freshness claim over them.**

- `openrouter` (case-insensitive, full tree, all 20 siblings): **zero occurrences**. No sibling
  references the OpenRouter API at all — not even the credential/env-var cut the pre-draft scan
  reported in kagi (that file's current tree carries no such token today; the earlier reference
  is superseded by absence).
- Hugging Face `api/models` hits exist in exactly one sibling, kama, and are **file-identity**
  probes of a single pinned repo (`ggml-org/models-moved`, GGUF fixture S037–S039) — not the
  list-endpoint schema, no freshness probe, no schema-delta:
  `kama-shokunin/.ufo/waves/round-20/build/out/FreshnessS039/upstream-hf-stories260K.json:16-19`;
  `kama-shokunin/.ufo/waves/round-16/advice/ScoutModelProvenance.md:26-41`;
  `kama-shokunin/.ufo/waves/round-16/drafts/sources-rows.md:12`.
- kama probes `/v1/models` on **local serving endpoints** (OpenAI-compatible local servers, LM
  Studio `/api/v1/models` with `loaded_instances`) for served-model identity/readiness — a
  different phenomenon, and kama's own overlap table explicitly rules kengaku's catalog fields
  non-overlapping: `kama-shokunin/.ufo/waves/round-25/build/out/ConnectorSiblingOverlap/overlap-scan.tsv:10`
  ("kengaku … open-model-catalogs.md:23 … catalog-declared; no overlap"); also
  `kama-shokunin/.ufo/waves/round-16/advice/ScoutLmStudioServer.md:26-28,82-83`.
- `verified-at: 2026-10-25` stamp occurrences in siblings are unrelated run receipts (mori's
  own census equipment runs: `mori-shokunin/.ufo/waves/round-44/evidence/c2-after.txt:4`,
  `count-c3.py:161`); none is attached to a catalog probe.
- kotoba's verifier routes kengaku's `open-model-catalogs.md` as a **citable kengaku artifact**
  (it does not hold or probe catalogs): `kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.json:764,844,2255-2257`.
- kumitate round-44 ConnSiblingOverlap names kengaku's `local-model-index.md:19-22` as the only
  `models.jsonl` claims (Bailian), a different path/substrate — attestation, not overlap:
  `kumitate-shokunin/.ufo/waves/round-44/controls/ConnSiblingOverlap.md:18`.
- Live `considerthese/` proposals: `catalog/catalogs/grader/benchmark` hits are kama's
  provider wire-id catalog rejection (`kama-shokunin/considerthese/2026-10-20.md:16`), revenger's
  ISO/IEC 27042 catalog abstract rejection (`revenger-shokunin/considerthese/2026-10-20.md:53`),
  game-dev-2d's lesson catalogue (`game-dev-2d-shokunin/considerthese/2026-10-20.md:8`). None
  proposes catalog probing or grading ground.

## 3. Axis — round-32 claims wording

Tokens scanned (full tree): `round32_defects`, `adoption_check`, `round32_c1_verify`,
`defects=7`, `entries=1 indexed=1 cited_rows=3`, `probed=2026-10-25 hf=ok openrouter=ok`,
`f20a1097`, `0d32691d`, `S093`, `S094`, `S097`, `S101`, `S102`.

Result: zero siblings reference any round-32 claim artifact or counter. The only `S###` hits
are each sibling's **own registry row ids** (the per-lane source-id namespace reuses `S###`):
mori's round-25 batch ran S097→S102 (`mori-shokunin/.ufo/waves/round-25/w1/SrcClampSite.md:200-205`,
`SrcBinaryOwnWork.md:199-200`); mado's round-18/19 waves re-opened its own S093/S094/S097 rows
(`mado-shokunin/.ufo/waves/round-19/w2/dispatch.json` seat names). These are namespace
coincidences, not citations of kengaku's rows; no sibling's text names kengaku's S093/S094/S097
(C1) or S101/S102 (C3) as its own or as a source.

## 4. Attack-items ledger (probes executed)

| # | Item | Result |
|---|---|---|
| A01 | `Toolathlon` full-tree, 20 siblings | 0 hits |
| A02 | `toolbench` full-tree | 0 hits |
| A03 | `tau-bench` full-tree | 1 hit: kumitate arXiv abstract (unrelated paper) |
| A04 | `ab-testing` full-tree | 1 hit: kake Cloudflare docs sidebar link |
| A05 | `validate_record_data` / `expected_ratio.csv` full-tree | 0 hits |
| A06 | `9be8d8fe` (Toolathlon pin) full-tree | 0 hits |
| A07 | `SWE-bench_Pro-os` / `scaleapi` full-tree | 0 hits |
| A08 | `v2/tasks` / `66f92766` (SWE-bench Pro V2 pin) full-tree | 0 hits |
| A09 | `grader-semantics` / `benchmark-grader` full-tree | 0 hits |
| A10 | `scoring code` / `deterministic grader` / `grading semantics` live surfaces | 0 hits |
| A11 | `2412.05579` (arXiv judge-survey id) full-tree | 0 hits |
| A12 | `LLM-as-judge`/`LLMs-as-judges` full-tree | 3 siblings, all non-survey (chousa quote-check, kumitate MAST/LangSmith docs) |
| A13 | `PandaLM` / `G-Eval` / `MT-Bench` full-tree | 0 hits |
| A14 | `SWE-bench` full-tree | 3 siblings, none grading code (kumitate paper/docs, kotodama attestation) |
| A15 | `openrouter` full-tree (case-insensitive) | 0 hits |
| A16 | `huggingface.co/api/models` full-tree | kama only, file-identity probes |
| A17 | `api/v1/models` full-tree | kama only, local-server introspection docs |
| A18 | `open-model-catalogs` / `model-catalogs` full-tree | kotoba routing (citable artifact) + kama overlap table (excluded) |
| A19 | `catalog_probe` / `catalogs_probe` / `schema-delta` full-tree | 0 hits |
| A20 | `verified-at: 2026-10-25` full-tree | mori run receipts only; none catalog-tied |
| A21 | `round32_defects` / `adoption_check` / `round32_c1_verify` full-tree | 0 hits |
| A22 | `defects=7` full-tree | 0 hits |
| A23 | `f20a1097` / `0d32691d` (freeze commits) full-tree | 0 hits |
| A24 | `S093`/`S094`/`S097`/`S101`/`S102` full-tree | sibling-local registry ids only (mori, mado) |
| A25 | Live SKILL/PROVINCE ×20, C1 tokens | 0 hits |
| A26 | Live SKILL/PROVINCE ×20, C3 tokens (openrouter/huggingface) | 0 hits |
| A27 | Live corpus-knowledge ×20, C1/C3 tokens | 0 hits |
| A28 | Live considerthese ×20, catalog/grader/benchmark (case-insensitive) | 3 unrelated uses |
| A29 | chousa routing rows re-verified | `scope-refusal-r12.md:22`, `archived-export-intake.md:103` hold |
| A30 | chousa r18 selftest `llm scoring` pin | holds (`corpus/README.md:680-681`) |
| A31 | kama overlap table ruling on kengaku catalog fields | holds (`overlap-scan.tsv:10`) |
| A32 | kotoba routing of `open-model-catalogs.md` | holds (`sibling-citation-routing-round16.json:764,2255`) |
| A33 | kumitate ConnSiblingOverlap on `local-model-index.md` | attestation, different substrate (`ConnSiblingOverlap.md:18`) |
| A34 | kotodama connector on kengaku SWE-bench evidence note | attestation (`ConnectorSiblings.md:56`) |
| A35 | kumitate SWE-bench paper quote (2512.08296) | paper read, excluded from row scope |
| A36 | lore S017 judge-pipeline rejection | holds (`SOURCES.md:25`) |
| A37 | kagi grader.py non-duplication precedent | holds (round-13/14 lessons) |
| A38 | claims-wording literal receipt strings (`entries=1 …`, `probed=… hf=ok`) | 0 sibling hits |

## 5. Synthesis

No sibling owns or is building any of the three claim grounds, before or after the drafts landed.
The closest surfaces — kama (local served-model identity + file-identity HF probes), kagi
(formerly a credential/env-var OpenRouter cut; zero `openrouter` tokens today), kotoba (vendor
eval-artifact digest + citation routing), lore (rejected judge-pipeline row), chousa (model-quality
scope refusal), kumitate (multi-agent paper figures, vendor docs) — are each disjoint on the
specific ground C1/C3 claim, and two siblings' own connector tables explicitly rule kengaku's
catalog/grading fields non-overlapping. Sibling `S###` matches are namespace coincidences in each
lane's own registry. C2 (defect closures) reads only kengaku round bytes; no sibling file
intersects R1–R7 by construction, and no sibling text references any C2 artifact.

VERDICT: no-contest
