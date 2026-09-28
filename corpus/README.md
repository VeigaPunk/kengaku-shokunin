# kengaku-shokunin corpus

Domain memory for LLM/model research & evaluation. Per
`~/projects/shokunin/CORPUS.md`: `knowledge/` entries cite a source;
`lessons/` entries cite round + evidence; every entry falsifiable or
marked opinion.

## What's here

| Entry | Covers | Primary source |
|---|---|---|
| `knowledge/benchmark-selection.md` | Task-class → benchmark mapping; contamination status; minimal stack | `llm-wiki/wiki/ai/agents-and-engineering/benchmark-shortlist-for-godspeed-research.md` |
| `knowledge/godspeed-eval-findings.md` | Iteration-2 empirical results: K2 split, variant multiplier, calibration asymmetry, cost | `llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-2.md` |
| `knowledge/telemetry-run-design.md` | Per-run telemetry fields, artifact set, phase gates, run-count floor | `llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-3-alpha-shittycodex.md` |
| `knowledge/local-model-index.md` | Bailian structured model index layout and field semantics | `~/.bailian/skills/bailian-docs-llm-wiki/models/index.md`, `models.jsonl` |
| `knowledge/local-bench-arena.md` | On-host 33-task battery: schema, two-model results, complementarity split | `~/bench-arena/` CSVs, analyzed 2026-09-28 |
| `knowledge/ledger-route-telemetry.md` | Live lane-routing corpus: event taxonomy, reroute signatures, model×lane counts | `~/Projects/bounties/ledger/telemetry.jsonl` (7,218 lines), profiled 2026-09-28 |
| `knowledge/bench-arena-fresh-run.md` | Round-4 authored run: endpoint drift finding, 4-task reproduction slice, prediction error | `~/bench-arena/` + `127.0.0.1:34113` live run 2026-09-28 |
| `knowledge/eval-theory-notes.md` | Digest: yao-second-half, creative-benchmark, trueskill-sorting, rlhf, bitter-lesson | `llm-wiki/wiki/karpathy/*` + `ai/{foundations,alignment-and-training}/`, read 2026-09-28 |
| `knowledge/gemini-benchmark-suite.md` | Four-signal godspeed test suite: reframe traps, variant multiplication, discovery widening, calibration meta-test | `llm-wiki/.../gemini-3.1-pro-godspeed-{benchmarks,test-battery}.md`, read 2026-09-28 |
| `knowledge/bailian-cli-telemetry.md` | Client-side CLI telemetry: 4,274 records, quota-vs-auth failure split, poll-verb rule | `~/.bailian/telemetry.jsonl`, profiled 2026-09-28 |
| `knowledge/open-model-catalogs.md` | HF + OpenRouter API schemas, local GGUF inventory, verify-endpoint rule | Live API probes 2026-09-28 |
| `lessons/round-1.md` | Path-correction, replace-don't-append, zero-width char hazard | LOG.md round 1, commit `90a5ce8` |
| `lessons/round-3.md` | Filename-judging missed on-host surfaces; complementarity vs pass-rate; NULL parsing; FAIL-latency signature | LOG.md round 3, this round's analysis |
| `lessons/round-4.md` | Endpoint-drift trap; n=1 flip on 03; FAIL-latency is subset-level not per-task | LOG.md round 4, `/tmp/bench-r4` run |
| `lessons/round-1-aggregator-audit.md` | Aggregator audit: corpus verdict, 13 re-verified claims, 3 defects (all closed round 4) | Aggregator L1 + reviewer lane, 2026-09-28 |

## Coverage map

- **Benchmark selection**: covered (knowledge/benchmark-selection.md).
- **Search-shape mechanism evidence**: covered at iteration-2 depth (knowledge/godspeed-eval-findings.md).
- **Run harness / telemetry spec**: covered at alpha depth (knowledge/telemetry-run-design.md).
- **Model catalog access**: Bailian index + HF/OpenRouter APIs + local GGUF inventory (knowledge/local-model-index.md, knowledge/open-model-catalogs.md).
- **Eval theory**: covered at digest depth — autonomy/IID assumptions, diversity blindness, judge-vs-aggregator split (knowledge/eval-theory-notes.md).
- **Executed eval**: covered — authored 4-task slice against live local model (knowledge/bench-arena-fresh-run.md).

## Known gaps (aggregator: file as lessons if still open next round)

- Karpathy branch core-eval pages digested (yao-second-half, creative-benchmark, trueskill-sorting); `karpathy/talks/`, `projects-and-tools/`, `standards-and-specifications/` still open. `wiki/ai/foundations/complexity.md` and `wiki/ai/books/` open; audit-cited `are-we-smart-enough` lives in `wiki/biology/books/` (out of domain).
- Executed-run gap closed by authored slice (knowledge/bench-arena-fresh-run.md); full 33-task re-run under fixed endpoint config remains optional.
- `llm-wiki-site` = generated static site (html/sitemap, no knowledge layer); `llm-wiki-public` = public mirror (html+md). Neither adds corpus signal beyond llm-wiki working copy — gap resolved as inspectable-when-needed.
