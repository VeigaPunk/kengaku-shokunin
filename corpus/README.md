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
| `lessons/round-1.md` | Path-correction lesson, citation-vs-generic lesson, non-ASCII write hazard | LOG.md round 1, commit `90a5ce8` |

## Coverage map

- **Benchmark selection**: covered (knowledge/benchmark-selection.md).
- **Search-shape mechanism evidence**: covered at iteration-2 depth (knowledge/godspeed-eval-findings.md).
- **Run harness / telemetry spec**: covered at alpha depth (knowledge/telemetry-run-design.md).
- **Model catalog access**: covered for Bailian index only (knowledge/local-model-index.md).

## Known gaps (aggregator: file as lessons if still open next round)

- No pages digested from `wiki/ai/alignment-and-training/`, `wiki/ai/foundations/`, `wiki/karpathy/` — eval-relevant pages likely exist there (e.g. `karpathy/creative-benchmark`, `ai/books/are-we-smart-enough`).
- No executed benchmark run in this repo yet — all evidence is second-hand from wiki notes (SHONEN.md promotion item still open).
- Route-telemetry section in SKILL.md interprets *agent run* telemetry; no local provider-route telemetry corpus found (`find -iname "*telemetry*"` hits were unrelated harness/CLI files, e.g. `~/.bailian/telemetry.jsonl` unexamined).
- `llm-wiki-site` / `llm-wiki-public` siblings uninspected — may hold generated/index layers over the working copy.
