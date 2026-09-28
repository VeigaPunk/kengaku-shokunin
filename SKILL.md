---
name: kengaku-shokunin
description: Domain specialist — LLM/model research & evaluation — scopes llm-wiki (~/Projects/webzites/repos/llm-wiki), route telemetry. Rank: shonen.
---

# kengaku-shokunin

LLM/model research & evaluation. Source of truth: `~/Projects/webzites/repos/llm-wiki`
(the `~/wikillm/llm-wiki` path in PROVINCE.md does not exist on this host —
verified `find -maxdepth 3` 2026-09-28; the working copy lives under
`Projects/webzites/repos/llm-wiki` with siblings `llm-wiki-site` and
`llm-wiki-public`).

Every claim below cites a local file, a command, or a named source. No
oral tradition.

## Decision table — benchmark selection

Task class → first benchmark family → what it actually measures:

| Task class | Benchmark | Measures | Source |
|---|---|---|---|
| Convergent coding (terminal) | Terminal-Bench 2.0 | Real traces, long horizons, low ambiguity | `wiki/ai/agents-and-engineering/benchmark-shortlist-for-godspeed-research.md` |
| Software engineering | SWE-Bench Pro (public) | SWE baseline; Preferred over Verified — Verified increasingly contaminated per OpenAI 2026-02-23 | same note, "Add Now" #2 |
| Desktop agency | OSWorld-Verified | Real apps, cross-app workflows, execution-based grading | same note, "Add Now" #3 |
| Browser workflows | WebArena-Verified | Deterministic browser eval, curated tasks, trace scoring | same note, "Add Now" #4 |
| MCP tool orchestration | MCP-Atlas | 36 real MCP servers / 220 tools / 1,000 tasks — tool discovery & orchestration | same note, "Add Now" #5 |
| Multi-app long-horizon ops | Toolathlon | Persistent state, retries, end-to-end verification | same note, "Add Now" #6 |
| Deep research browsing | BrowseComp | Persistence + creativity for hard-to-find facts; closest public proxy for search-path quality | same note, "Add Now" #7 |
| Economic output | GDPval | Real-world knowledge-work deliverables | same note, "Add Now" #8 |
| Security/exploit/patching | EVMbench | Non-obvious attack/repair paths | same note, "Add If Relevant" #1 |
| Shared-control trajectories | τ²-Bench | Agent must guide a user, not act alone | same note, "Add If Relevant" #2 |
| Search-shape claims | **Custom battery only** — public benchmarks systematically miss it | Off-path reframing, frontier coverage, variant multiplication | same note, "What Public Benchmarks Will Miss" |

Sequencing rule (`godspeed-umwelt-iteration-3-alpha-shittycodex.md`):
custom mechanism battery first, 1–2 public transfer slices second, heavy
public suites after the mechanism is visible. Public benchmarks are
**transfer checks, never the core proof**.

## Decision table — minimal stack when time is tight

Per the shortlist note's "Minimal Stack": Terminal-Bench 2.0 +
OSWorld-Verified + MCP-Atlas + BrowseComp + one K2-style reframe suite +
one frontier-enumeration suite. Coverage: convergent coding, desktop
agency, tool orchestration, off-path web pressure, mechanism proof.

## Benchmark anti-patterns

1. **Leaderboard worship / stale benchmark trust.** OpenAI retired
   SWE-Bench Verified as primary on 2026-02-23 due to contamination;
   a benchmark's reputation outlives its signal. Re-check contamination
   status before citing.
2. **Treat public benchmarks as mechanism proof.** They measure "can the
   agent arrive at one good answer" — they miss off-path reframing,
   variant multiplication, frontier coverage, and calibration asymmetry
   (shortlist note, lines 87–97). Single-answer scoring flattens Pareto
   task structure.
3. **Multi-variable sweeps.** Iteration 2's gradient (Sonnet-C 7 →
   Opus-UT-G 19 on T2 review) only resolved because model, thinking
   budget, and prompt regime were varied factorially. Change one lever
   at a time or pre-register the matrix.
4. **Skip ex-ante calibration.** Record framer predictions before runs;
   iteration 2 showed predictions systematically wrong in both
   directions (under-predicted control breadth, under-predicted godspeed
   divergence). Without predictions you lose the calibration-asymmetry
   signal entirely.
5. **Frozen-harness violations.** Freeze godspeed text, judge schema, and
   telemetry capture before scored runs (alpha note, Phase 0).
6. **Broken-telemetry scaling.** Promotion rule: if telemetry is broken,
   fix the harness; if correctness collapses, stop and inspect prompt
   contamination (alpha note, Phase 1). Never scale past a known-broken
   meter.
7. **Accusation counting.** Discovery tasks score *validated* findings,
   not raw accusation count (alpha note, Judging).
8. **Contamination blindness.** Memorized-data benchmarks understate
   empirical-search gains (SWE-Bench Private > Public for
   frontier-walking claims, `gemini-3.1-pro-godspeed-test-battery.md`).

## Research-note structure

Wiki convention (verified across `godspeed-umwelt-iteration-2.md`,
`benchmark-shortlist-for-godspeed-research.md`,
`godspeed-umwelt-iteration-3-alpha-shittycodex.md`):

```yaml
---
title: "<descriptive title>"
branch: ai                  # wiki/ai subtree
category: concept           # note type
source_ids:
  - <slug-of-source-evidence>
last_compiled: <ISO-8601>
related:
  - "[[<wiki-link>]]"
---
```

Body: one-line thesis → evidence tables (per-condition rows, exact
metrics, no rounding) → mechanism section (what the telemetry isolates) →
predictions / calibration deltas → what carries forward → connections
(`[[wiki-links]]` with one-line why-each).

Rules: every claim cites a file, command output, or `source_ids` entry;
tables carry raw numbers (RMSE 135,367 → 117,791), not adjectives;
negative results ("ultrathink alone does not replicate K2") get their own
sentences, not omissions.

## Route-telemetry interpretation

Per-run artifacts (alpha note, Phase 0 + iter-3 note): `response.md`,
`telemetry.json`, `judge.json` per run, written adjacent in the run dir.
Fields: final answer quality, correctness/validity, variant count,
non-dominated variant count, axis vocabulary count, unique findings,
tool calls, wall-clock, token usage, framer prediction error.

Observed godspeed deltas to calibrate against (iteration 2, effect-size
table): tool calls ~1.5×, wall-clock ~1.5–2× (1.5× convergent tasks, 2×
divergent), correctness errors 0 → 0.

Reading rule:

| Observation | Interpretation | Action |
|---|---|---|
| Breadth ↑, correctness flat | Search-shape shift, mechanism real | Expand battery |
| Breadth ↑, precision ↓ | Directive over-wide or task mis-framed | Narrow directive/task framing |
| Public slices flat, custom slices move | Benchmarks under-measure the effect | Supports iteration-2 thesis; rely on custom |
| Public slices move strongly | Effect is broader than search shape | Broaden claim before scaling |
| Telemetry missing/malformed | Harness fault, not signal | Fix harness; rerun |
| Zero shape difference CXF-C vs CXF-G | Task design too easy/convergent | Tighten task design before scaling |

Cost reading: normalize gains per dollar — +50% tool calls and +75%
wall-clock are acceptable only if information gain (variants, unique
findings, reframe discoveries) scales comparably.

### Local telemetry surfaces (verified on this host, 2026-09-28)

Two distinct corpora exist — do not conflate:

1. **Lane-routing ledger**: `~/Projects/bounties/ledger/telemetry.jsonl`
   (7,218 lines). Event taxonomy: `dispatcher_tick` (3,680),
   `mission_parked` (1,188), `mission_dispatched` (1,167),
   `fleet_synced`, `freshness_check`, `binding_verified`,
   `lease_claimed`, `attempt_reset` (68), `operator_decree` (58),
   `mission_done` (26), `lane_degraded`, `mission_failed` (21),
   `claim_rejected`. A lane's model is a **sequence** — replay
   `lane_parked`/`reroute` chains per `run_id`; `usage_limit*` causes
   are provider-meter events, not model failures; `local degrade (I3)`
   = bucket walk exhausted, lane identity preserved.
   Detail: `corpus/knowledge/ledger-route-telemetry.md`.
2. **Eval battery**: `~/bench-arena/telemetry-qwenlocal-v2.csv` (33
   rows). Schema: `task,status,opencode_rc,closed_fence,output_sha256,
   prompt_tokens,predicted_tokens,inference_latency_ms,tokens_per_sec,
   test_runtime_ns,telemetry_source,telemetry_available`.
   Detail: `corpus/knowledge/local-bench-arena.md`.

Parsing rules learned on real files:

- `telemetry_available=n` rows carry literal `"NULL"` strings in
  numeric fields — treat as a first-class row state, never `float()`
  blindly (observed: `20-csv-group-sum`).
- FAIL rows returned **faster** than PASS on the 33-row qwenlocal-v2 battery
  (median 60.9 vs 79.5 ms inference latency) — early-bail signature, that
  pipeline only. Round-5 direct-API run inverted it on wall-clock *and*
  tokens (FAIL 1.71 s/260 tok vs PASS 0.84 s/128 tok): wrong solutions are
  long. Population statistic, never a per-task law; quote with pipeline tag.
- Aggregate pass rates hide complementary win-sets: grok45 19/33 vs
  qwenlocal 21/33 with near-disjoint per-task wins (8 vs 10). Round-5 adds
  the temporal twin: 20/33 vs v2's 21/33 headline hid **8/33 status flips** —
  a stable aggregate can rotate a quarter of the win-set. Always diff
  win-sets by task, both across models and across runs.
- `fence_found=0` splits by `finish_reason`: `length` = truncation (model
  outran max_tokens mid-generation — 06 at 4096 tok, r5), `stop` = real
  format/harness defect. Check finish before filing harness bugs.
- Byte-identical `sol_sha256` across pipelines marks scaffold-insensitive
  tasks (r5: 16, 25, 28, 32, 33 — all tiny deterministic tasks, incl. one
  stable FAIL: deterministic wrong answer = capability gap, not noise).

### Running a battery against the local model (verified 2026-09-28)

1. Probe the endpoint, not the config: `GET /v1/models` + `/health` on the
   configured port. `~/.config/opencode` provider `qwen-local` still points
   at `localhost:8080` (now Jitsi — listening but wrong); the live
   llama-server is `127.0.0.1:34113` via `qwen-coder.service`.
   Listening-but-wrong beats closed-port for silent breakage.
2. Two transport paths: `loop.sh` (opencode `--agent raw`, system prompt,
   `/metrics`→journal fallback) or direct `POST /v1/chat/completions`
   (minimal, deterministic-ish). Grade identically:
   `BENCH_ROOT=<scratch> bash ~/bench-arena/grade.sh <label>` consumes any
   `out/<label>/<task>.txt` — runner and grader are separable.
3. n=1 per task flips near the boundary: `03-extract-isodatetimes` went
   PASS→FAIL across pipelines at temp 0.2. Status claims need repeats or
   pinned seed. Stable canaries: 01 (PASS×2), 02 (FAIL×2), 05 (both-fail).
4. Record ex-ante per-task *and* aggregate predictions — they calibrate
   separately (round 4: per-task 3/4, aggregate miss).

### Model catalogs (non-Bailian)

Verified live 2026-09-28, no auth: HF `api/models` (search/filter=gguf/
sort=trendingScore; `sha`, `siblings`, `pipeline_tag`); OpenRouter
`api/v1/models` (460 entries; `context_length`, `knowledge_cutoff`,
string `pricing` per token, `hugging_face_id` open-weight twin link).
Detail: `corpus/knowledge/open-model-catalogs.md`.

### Eval-theory rules (digest: corpus/knowledge/eval-theory-notes.md)

- Second-half thesis (Yao): recipe saturated; frontier is eval design —
  break the autonomy assumption (measure collaboration) and IID
  assumption (record run order; sequence-aware tasks reward memory).
- Diversity blindness (Gwern): RLHF collapses output variance; no
  mainstream benchmark scores it. Probe = k samples × pairwise embedding
  spread. Use best-of-N with dissimilarity selection, not just
  temperature.
- Judge/aggregator split (Thariq): never ask an LLM for a global order
  over large sets — batch-compare ~10 items, aggregate with TrueSkill
  (μ−3σ sort key, ~1–2 matches/item); pairwise > absolute scoring.
- RLHF proxy gap: every scalar judge is a reward model without a KL
  penalty — re-ground in primary evidence instead of trusting the score.

## Production checklist — running an eval

1. Write ex-ante predictions for every condition before runs — per-task
   *and* aggregate; they calibrate separately.
2. Probe every endpoint before freeze (`/v1/models`, `/health`); a
   listening-but-wrong service degrades telemetry silently (Jitsi on
   :8080 vs llama on :34113, 2026-09-28).
3. Freeze: prompt text, judge schema, telemetry capture. (Phase 0)
4. Smoke: 2 tasks × 2 conditions = 4 runs. Gate on telemetry validity,
   shape difference, correctness. (Phase 1)
5. Core battery: ≥4 tasks per mechanism class (K2-reframe, frontier
   enumeration, discovery) × 2 conditions. (Phase 2)
6. Public transfer slice only after mechanism visible. (Phase 3)
7. Record all 10 telemetry fields per run; keep `response.md` +
   `telemetry.json` + `judge.json` adjacent. Repeat near-boundary tasks
   (n≥2) — single-run status flips on sampling (`03` PASS→FAIL, round 4).
8. Analysis: deltas on correctness, reframes, skyline size, axis
   vocabulary, unique findings, tool calls, wall-clock, prediction error.
9. Expansion rule: keep a benchmark family only if it adds a new axis of
   signal without harness drag.

## Cited local sources

- `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/benchmark-shortlist-for-godspeed-research.md` — benchmark shortlist, anti-patterns, minimal stack (read 2026-09-28)
- `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-2.md` — 125 agents / 21 experiments; K2 clean split, calibration asymmetry, variant multiplier, effect-size table
- `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-3-alpha-shittycodex.md` — telemetry fields, Phase 0–3 gates, judging schema, run counts
- `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/gemini-3.1-pro-godspeed-benchmarks.md` — four-signal test suite design (off-path reframe / variant multiplication / discovery widening / calibration asymmetry)
- `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/gemini-3.1-pro-godspeed-test-battery.md` — external benchmark tier, SWE-bench contamination paradox, predictive calibration
- `~/Projects/webzites/repos/llm-wiki/Home.md` — wiki branch/index conventions (read 2026-09-28)
- `~/.bailian/skills/bailian-docs-llm-wiki/models/index.md` + `models.jsonl` — 180 families / 413 models structured index; `contextWindow`, `QPM`, pricing, `profile` (oneLinePositioning, scenes, notSuitableFor, familyTier) for model selection (verified 2026-09-28; index generated 2026-09-11)
- `find`/`grep` output this session — `~/wikillm/llm-wiki` absent; wiki at `~/Projects/webzites/repos/llm-wiki`
- `~/Projects/bounties/ledger/telemetry.jsonl` — live lane-routing corpus, 7,218 events; taxonomy + reroute signatures in `corpus/knowledge/ledger-route-telemetry.md` (profiled 2026-09-28)
- `~/bench-arena/` (`tasks/`, `report-grok45.csv`, `report-qwenlocal-v2.v2.csv`, `telemetry-qwenlocal-v2.csv`) — executed 33-task two-model battery; results in `corpus/knowledge/local-bench-arena.md` (analyzed 2026-09-28)
- `~/Projects/webzites/repos/llm-wiki/wiki/karpathy/**` + `wiki/ai/{foundations/bitter-lesson,alignment-and-training/rlhf}.md` — eval-first thesis, diversity blindness, TrueSkill judge/aggregator split, RLHF proxy mechanics (digested 2026-09-28 → `corpus/knowledge/eval-theory-notes.md`)
- `https://huggingface.co/api/models`, `https://openrouter.ai/api/v1/models` — live catalog schemas (probed 2026-09-28 → `corpus/knowledge/open-model-catalogs.md`)
- `127.0.0.1:34113` llama-server + `~/bench-arena/grade.sh` — authored 4-task slice, 1/4 PASS vs predicted 2/4, `03` flip PASS→FAIL (run + graded 2026-09-28 → `corpus/knowledge/bench-arena-fresh-run.md`)
- `~/bench-arena/` round-5 battery — full 33-task direct-API re-run: 20/33 PASS, 8 status flips vs v2, 5 byte-identical sol_sha, 06 truncation (`finish=length` @4096 tok), FAIL slower on wall+tokens (run + graded 2026-09-28 → `corpus/knowledge/bench-arena-round5-battery.md`)
- `~/Projects/webzites/repos/llm-wiki/wiki/karpathy/{talks,projects-and-tools,standards-and-specifications}/**` + remaining `philosophy-and-concepts/`, `gwern-essays/`, `ai/foundations/complexity.md`, `ai/books/` — second digest: sampling-proves-presence, reference-class, autonomy slider, spec-ability tiers (swept+read 2026-09-28 → `corpus/knowledge/eval-design-digest-2.md`)
