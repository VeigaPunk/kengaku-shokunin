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
| `knowledge/bench-arena-round5-battery.md` | Full 33-task re-run under fixed endpoint: 20/33, 8 status flips, truncation class, sha-identical set | `/tmp/bench-r5/` run vs `127.0.0.1:34113`, graded 2026-09-28 |
| `knowledge/eval-design-digest-2.md` | Second digest: sampling-proves-presence, reference-class, autonomy slider, spec-ability tiers | 22 remaining wiki files, swept+read 2026-09-28 |
| `lessons/round-1.md` | Path-correction, replace-don't-append, zero-width char hazard | LOG.md round 1, commit `90a5ce8` |
| `lessons/round-3.md` | Filename-judging missed on-host surfaces; complementarity vs pass-rate; NULL parsing; FAIL-latency signature | LOG.md round 3, this round's analysis |
| `lessons/round-4.md` | Endpoint-drift trap; n=1 flip on 03; FAIL-latency is subset-level not per-task | LOG.md round 4, `/tmp/bench-r4` run |
| `lessons/round-1-aggregator-audit.md` | Aggregator audit: corpus verdict, 13 re-verified claims, 3 defects (all closed round 4) | Aggregator L1 + reviewer lane, 2026-09-28 |
| `lessons/round-5.md` | Aggregate-correct ≠ model-right; truncation failure class; sha-identity = scaffold insensitivity | LOG.md round 5, `/tmp/bench-r5/` run |

## Coverage map

- **Benchmark selection**: covered (knowledge/benchmark-selection.md).
- **Search-shape mechanism evidence**: covered at iteration-2 depth (knowledge/godspeed-eval-findings.md).
- **Run harness / telemetry spec**: covered at alpha depth (knowledge/telemetry-run-design.md).
- **Model catalog access**: Bailian index + HF/OpenRouter APIs + local GGUF inventory (knowledge/local-model-index.md, knowledge/open-model-catalogs.md).
- **Eval theory**: covered at digest depth — autonomy/IID assumptions, diversity blindness, judge-vs-aggregator split (knowledge/eval-theory-notes.md).
- **Executed eval**: covered at battery depth — authored 4-task slice (r4) + full 33-task re-run under fixed endpoint (knowledge/bench-arena-round5-battery.md).


- **Wiki branch digest**: karpathy subtree + ai/foundations + ai/books fully swept (knowledge/eval-design-digest-2.md); remaining open surface = non-karpathy `ai/` topics beyond eval scope.
- **Cross-pipeline stability**: byte-identical solution set identified (16, 25, 28, 32, 33); flip-capable probe set is 03, 06, 08, 09, 12, 13, 20, 31.

## Open gaps

- **n≥2 on flip-capable tasks**: 8 tasks flipped between v2 and r5 at n=1 each; which flips are sampling vs pipeline needs repeats on the probe set above.
- **Planning-horizon coverage**: bench-arena is single-step; the deployed-agent bottleneck (agent-engineering note) is unmeasured locally.
- **27 test-timeout**: `test_rc=124` at 60 s in both pipelines — unclear whether solvable-but-slow or algorithmically wrong; needs a relaxed-timeout probe.
