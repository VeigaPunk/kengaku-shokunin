---
name: kengaku-shokunin
description: "Domain specialist — LLM/model research & evaluation — eval design, benchmark selection, offline replay grading, blind shim-cascade leg attribution and interval-calibrated verdicts; llm-wiki (~/Projects/webzites/repos/llm-wiki) and route telemetry (~/Projects/bounties/ledger/telemetry.jsonl) are historical, absent since 2026-10-15, digests retained in corpus/knowledge/. Triggers: 'model evaluation', 'benchmark selection', 'eval calibration', 'benchmark grader', 'attribution probe', 'novelty pricing'. Anti-trigger: not serving-flag changes, endpoint remediation or model-serving config. Sibling arbitration: kotoba owns prompt and skill craft (kengaku keeps only measured capability effects); kumitate owns OMP route resolution and fallback policy; kama owns local endpoint health and identity; chousa owns research method; tameshi owns verification-fixture craft. Rank: shonen."
---

# kengaku-shokunin

LLM/model research & evaluation. The 2026-09-28 source of truth was
`~/Projects/webzites/repos/llm-wiki` (the `~/wikillm/llm-wiki` path never
existed on this host — verified `find -maxdepth 3` 2026-09-28, when the
working copy resolved under `Projects/webzites/repos/llm-wiki` with siblings
`llm-wiki-site` and `llm-wiki-public`). **Status 2026-10-15: that wiki path
is ABSENT** (`corpus/evidence/round13-coverage/surface-receipt.json`) — every
wiki citation below is a dated historical observation; what this lane retains
is the digest set in `corpus/knowledge/` (derived evidence, not original wiki
bytes) plus the rules in this file. Current offline entry point for the lane's
numbers: `python3 grader.py` (§Hermetic grader; row in §Gate/probe registry).

Every claim below cites a local file, a command, or a named source — host-absolute
paths are dated historical since the 2026-10-15 receipt (§Cited local sources). No
oral tradition.

## Decision table — benchmark selection

Task class → first benchmark family → what it actually measures:

Source status (2026-10-15): the wiki notes named in the Source column live under
the ABSENT `~/Projects/webzites/repos/llm-wiki` tree (receipt:
`corpus/evidence/round13-coverage/surface-receipt.json`); the selections are
retained as in-repo digests — `corpus/knowledge/benchmark-selection.md`
(shortlist note) and `corpus/knowledge/godspeed-eval-findings.md` (iteration-2
note). Read this table against those digests, not against the originals.

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
9. **Reading a multi-turn advantage as planning ability.** Emitting the full
   state every turn beat sparse checkpoints and one-shot chaining on
   *identical* problems (r8 7/10 > 1/10 ≈ 0/10; r9 fresh seeds 4/8 > 2/8 =
   2/8 > 0/8). The gap is largely **self-copy scaffold** — each turn re-reads
   the model's own previous answer — not horizon maintenance. Ablate emission
   granularity (INC ⊃ CKPT-dense ⊃ CKPT-sparse ⊃ MONO) before claiming
   planning; the phenomenon is publicly anticipated (Laban et al. ICLR 2026
   SNOWBALL +15–20%; induction heads).
   (`corpus/knowledge/bench-arena-round8-horizon.md`,
   `corpus/knowledge/eval-prior-art-calibration.md`)
10. **One strictness level for state-match grading.** Of 19 failing r8 `A-INC`
   records (each `nwrong=1`), **15** were the MOV-zero convention (9 dropped a
   zero-valued key, 6 left the MOV source at its pre-MOV value) and only **4**
   were genuine value drift; strict 7/10 vs convention-tolerant 9/10. Grade
   both, report the composition, or a spec-convention miss masquerades as a
   capability failure. (`corpus/knowledge/bench-arena-round8-horizon.md` §A)
11. **Trusting a manipulation because the design says so.** r8's injected
   corruption was structurally inert in 4/8 problems (tail ops `DEL`/`SET`/
   clobbered the key), fabricated `true_mid+5` in 2/8, and landed on a key the
   tail never touched in 1/8 → **well-formed in 2/8**; corrupt and clean arms
   were byte-identical in 3/8 problems per arm. Pre-flight: simulate the
   treatment through the remaining ops and assert the final state differs from
   truth. (`corpus/knowledge/bench-arena-round8-horizon.md` §B)
12. **A control arm that is not the control.** Checkpoint cells measure latent
   maintenance only if ack turns actually ack. r8 leaked 0 states beyond the
   harness-demanded turn 1; r9 leaked full states in **16/48** (`CKPT4710`)
   and **8/56** (`CKPT710`) non-turn-1 ack turns, across all 8 problems. Audit
   compliance per problem, then filter — a leaky checkpoint cell is a partial
   INC cell. (`corpus/knowledge/bench-arena-round9-replication.md`)
13. **Assuming a grader's `ok` is the conjunction your claim needs.** r8's
   `grade_c` computed `over_repair` and then left it out of `ok`
   (`horizon.py:288`), and derived `preserved` from the model's *self-declared*
   violations (`:277-279`) → `C-benign` 1/4 was really 0/4. Mutation-test
   graders against synthetic adversarial inputs before trusting a SUMMARY
   (round 9: 50 cases → 12 defect candidates, 1 live).
   (`corpus/evidence/round9-fleet/harness-mutation.md`)
14. **A stored SUMMARY no one can re-derive is a claim, not a measurement.**
    Round 8's SUMMARY spent a round un-recomputable from the repo — the run
    artifact was uncommitted and `raw`-stripped, so ack compliance could not
    be re-audited until round 9 re-landed the bytes; round 10 found a stored
    failure-class count (12/32) that no one had ever recomputed — the
    committed bytes give **24/32**. Commit the bytes, then commit the command
    that recomputes every number from them, and prove it can fail.
    (`python3 grader.py --selftest`;
    `corpus/evidence/round9-fleet/harness-mutation.md`)
15. **A causal-order check keyed on timestamp uniqueness.** `request_ts` is
    second-resolution and a fast local server issues ~5 requests/s, so the
    first filler/ack share the descriptors record's second (r11: three cells
    at `23:28:57Z`). A gate that asserts "all records at min `request_ts` are
    the first-injected one" FALSE-FAILS on clean bytes. Order causal proofs by
    **file position** in the append-ordered JSONL, not by timestamp
    uniqueness; use the timestamp only for the coarser hash-before-first-request
    bound. (`corpus/evidence/round11-fleet/INTEGRATOR-NOTES.md` delta 2;
    `grader.py` `check_r11_ordering`)
16. **A two-mechanism arm read as a one-mechanism finding.** r8's `A-MONO 0/10`
    (vs `A-INC 7/10`, `A-CKPT 1/10`) spent eight rounds as emission-granularity
    evidence, but MONO differs from every incremental arm on **two** axes at
    once: all ten operations are listed up front *and* only one state is ever
    emitted. Any arm that differs from its comparator on more than one axis
    needs a third arm holding one axis fixed — round 12 adds `A-CKPT10`
    (incremental ops, exactly one forced emission) so the contrast
    `A-MONO − A-CKPT10` isolates batching. (`corpus/evidence/round8-horizon/run.log:81-83`;
    `corpus/evidence/round12-ladder/probe_plan_r12.md` §1 C3, §2.1)
17. **An asserted power floor.** The r12 draft plan filed "family 1 n ≥ 56,
    family 2 n ≥ 42" as its underpowered-verdict trigger with no derivation;
    the design critic recomputed it — 42 pairs do **not** reach 80% power at
    the filed dz (MC: n=42 → 0.791, n=44 → 0.810). A floor is a measurement:
    compute it with a committed, seeded script and cite the number
    (`corpus/evidence/round12-ladder/power_r12.py` → `power_analysis_r12.md` §2;
    `r12-critic-design.md` D3).
18. **Pooling heterogeneous forecast events into one skill score.** Round 12
    scores three event classes — 416 per-problem pass events (fitted
    predictor), 304 per-problem sign events (mostly an uninformative 0.50),
    7 run-level judgement events. One Brier-skill number over all 727 mixes
    reference classes and is uninterpretable; report per set and per subgroup
    (replicate arms / novel arms / new family) and label the pooled figure with
    what it actually measures (`persistence + arm-rate transport`).
    (`r12-critic-design.md` D6; `probe_plan_r12.md` §2.3 E6)
19. **A probability tilt that breaks its own marginals.** Fitting a difficulty
    slope on prior per-problem outcomes gave c = −5.03; applied raw, the
    sigmoid saturated and the arm-mean predicted probability drifted off the
    arm base rate (A-MONO mean p 0.372 against a 0.143 base rate, i.e. 23.8
    predicted passes instead of 9.1). Any per-item tilt must be renormalized so
    each group's mean predicted probability equals that group's base rate
    (round 12: a per-arm logit offset solved by bisection with the clip inside
    the target), or the point predictions and the probabilities contradict each
    other. (`corpus/evidence/round12-fleet/INTEGRATOR-NOTES.md` §2 L1-tilt)

## Research-note structure

Wiki convention (verified 2026-09-28 across `godspeed-umwelt-iteration-2.md`,
`benchmark-shortlist-for-godspeed-research.md`,
`godspeed-umwelt-iteration-3-alpha-shittycodex.md` in the llm-wiki tree — ABSENT
since 2026-10-15, so the originals cannot be re-checked; the convention below is
retained in-repo knowledge):

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

### Local telemetry surfaces (profiled on this host 2026-09-28 — HISTORICAL: both corpora absent as of the 2026-10-15 receipt)

Two distinct corpora existed when profiled — do not conflate their retained digests:

1. **Lane-routing ledger**: `~/Projects/bounties/ledger/telemetry.jsonl`
   (7,218 lines at the 2026-09-28 profile; path ABSENT 2026-10-15, reconfirming
   the round-11 loss). Event taxonomy: `dispatcher_tick` (3,680),
   `mission_parked` (1,188), `mission_dispatched` (1,167),
   `fleet_synced`, `freshness_check`, `binding_verified`,
   `lease_claimed`, `attempt_reset` (68), `operator_decree` (58),
   `mission_done` (26), `lane_degraded`, `mission_failed` (21),
   `claim_rejected`. A lane's model is a **sequence** — replay
   `lane_parked`/`reroute` chains per `run_id`; `usage_limit*` causes
   are provider-meter events, not model failures; `local degrade (I3)`
   = bucket walk exhausted, lane identity preserved.
   Detail: `corpus/knowledge/ledger-route-telemetry.md`.
2. **Eval battery**: `~/archive/bench-arena/telemetry-qwenlocal-v2.csv` (33
   rows at profile time; both bench-arena paths ABSENT 2026-10-15). Schema: `task,status,opencode_rc,closed_fence,output_sha256,
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
  the temporal twin: 20/33 vs v2's 21/33 headline hid **8/33 status deltas** —
  a stable aggregate can rotate a quarter of the win-set. Always diff
  win-sets by task, both across models and across runs.
- `fence_found=0` splits by `finish_reason`: `length` = truncation (model
  outran max_tokens mid-generation — 06 at 4096 tok, r5), `stop` = real
  format/harness defect. Check finish before filing harness bugs.
- Byte-identical `sol_sha256` across pipelines marks scaffold-insensitive
  tasks (r5: 16, 25, 28, 32, 33 — all tiny deterministic tasks, incl. one
  stable FAIL: deterministic wrong answer = capability gap, not noise).
  Round 6 adds: identical *status* ≠ identical sha — 08 passed 3/3 with two
  shas; sha-identity at temp 0.2 is reserved for the smallest output spaces.
- **Unanimity ≠ attribution (r7 correction of the r6 "n≥2 rule"):** a
  one-shot status flip between harnesses that stays unanimous across n=3
  direct-API reps is *stable under that API* — it is not yet attributed to
  the scaffold. r7 ablated the 5 "scaffold-determined" tasks component-
  wise (E1 full replay / E2 −system / E3 −tools / E4 +temp0.2): only
  13-stack-min is genuinely scaffold-caused; 03, 08, 31 decomposed to
  sampling noise, 12 weakly scaffold-pulled. Attribute flips only after a
  component ablation, not after endpoint re-runs.
- **Draws are non-iid; n≤5 unanimity is weak evidence (r7, n=25):**
  consecutive identical-request reps at temp 0.2 are order/state-coupled
  (lag-1 autocorr +0.26/+0.32, permutation p≈0.01, ~5–10 request
  horizon). 09-sql went 5/5 identical-sha PASS then 8 FAILs in the next
  20 (p̂=0.68, single discrete FAIL mode: window-fn-in-WHERE, 8/8 regex
  match); 20-csv is FAIL-tilted (p̂=0.32, 5 contract-handling modes —
  r6's 3/3 PASS was lucky). For interior-p̂ tasks report pass-rate with
  block-robust intervals, not per-draw Wilson; a "noise" label needs
  tilt + mode census, not just non-unanimity.
- **Tools-without-system is a trap condition (r7):** forwarding `tools` +
  `tool_choice:auto` while stripping the system prompt produced
  `finish=tool_calls` in 14/15 cells (13/15 with empty content; one
  emitted unfenced prose; observed call on repeat probe:
  `skill(name="min_stack")`, `min_stack` being the emitted tool-call name of
  the minimal-stack skill in the captured r7 wire probe (semantics:
  `corpus/knowledge/bench-arena-round7-scaffold-ablation.md`) — temp-0.2
  repro held 9/9, trap is
  temperature-invariant). A bare-API probe must strip `tools`/
  `tool_choice` too, or keep the output-contract system text; never
  compare "API no-system" against "harness with-system+tools" and read
  the delta as model behavior.
- **Context mass shifts solution strategy; temperature is a bare-prompt
  lever (r7, factorial on 13-stack-min):** bare@0.2 → sorted-stack
  attractor 5/5 (byte-identical sha); bare@0.8 → 1/3 escapes to
  canonical; scaffold@0.8 and @0.2 → canonical 10/10. The +4.7K-token
  opencode envelope (~4.3K system text: skills catalog + env +
  powered-by; +0.4K tool-format block) dominates family selection;
  temperature only moves it when the envelope is absent. "Same model,
  same prompt" claims require same envelope AND same decode params.
- **`enable_thinking` is a no-op on this host's endpoint (r7):**
  `qwen-coder-godspeed.jinja` has no think branch; r5/r6 "thinking off"
  described the template, not the flag. Verify template branches before
  crediting request parameters.
- `finish=length` that recurs at a **doubled** cap is strategy-bounded, not
  budget-bounded: 06 truncated at 4096 and again at 8192 (exponential
  regex expansion); raising max_tokens only doubles wall-clock.
- `test_rc=124` after bounded joins ⇒ suspect **crashed worker threads**,
  not slow code: exceptions in `threading.Thread` fail open toward hang
  (r5 task 27: six readers died on `rw._active` AttributeError, main
  blocked forever on `Barrier(7)` — the 60 s timeout was an exception
  deadlock, and `_active` is a hidden contract absent from prompt.md).
  Instrument with `faulthandler.dump_traceback_later`; diff test attribute
  accesses vs prompt API before crediting/blaming the model.

### Running a battery against the local model (historical procedure — verified 2026-09-28; **not runnable as written since 2026-10-15**: endpoint, battery tree, unit and template absent per `corpus/evidence/round13-coverage/surface-receipt.json`; the current offline entry point for everything this section produced is `python3 grader.py`)

1. Probe the endpoint, not the config: `GET /v1/models` + `/health` on the
   configured port. Historical: the 2026-10-15 receipt found `:34113/health`
   refusing connections and the unit deleted (serving-plane health/detection:
   kama, `../kama-shokunin/PROVINCE.md`; restoration: operator-owned). At
   profile time `~/.config/opencode` provider `qwen-local` still pointed at
   `localhost:8080` (Jitsi then — listening but wrong); the llama-server
   live at the time served `127.0.0.1:34113` via `qwen-coder.service`.
   Listening-but-wrong beats closed-port for silent breakage.
2. Two transport paths: `loop.sh` (opencode `--agent raw` — sends the
   raw-agent system prompt + `<env>` + skills catalog ~4.3K tok, plus
   `tools:[janitor_auth,skill]`/`tool_choice:auto` ~400 tok, and NO
   temperature → server default 0.8) or direct `POST
   /v1/chat/completions` (minimal, deterministic-ish, temp 0.2). Grade
   identically (historical command — `~/archive/bench-arena/` ABSENT 2026-10-15;
   archived scripts keep their bytes in `corpus/evidence/`, this is a citation,
   not a runnable entry point): `BENCH_ROOT=<scratch> bash ~/archive/bench-arena/grade.sh <label>`
   consumes any `out/<label>/<task>.txt` — runner and grader are
   separable. Verbatim request captured once via a proxy provider
   (`/tmp/bench-r7/capture/`); see
   `corpus/knowledge/bench-arena-round7-scaffold-ablation.md`.
3. n=1 per task flips near the boundary: `03-extract-isodatetimes` went
   PASS→FAIL across pipelines at temp 0.2. Status claims need repeats or
   pinned seed. Stable canaries: 01 (PASS×2), 02 (FAIL×2), 05 (both-fail).
4. Record ex-ante per-task *and* aggregate predictions — they calibrate
   separately (round 4: per-task 3/4, aggregate miss).

### Model catalogs (non-Bailian)

Verified live 2026-09-28, no auth (public URLs not re-fetched by the 2026-10-15
receipt — dated observation): HF `api/models` (search/filter=gguf/
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

## Planning-horizon & transcript-shape probes (verified 2026-09-28)

Cell semantics for the r8/r9 instruments (`corpus/evidence/round8-horizon/horizon.py`,
`corpus/evidence/round9-replication/run_r9.py`); record schemas are in
`corpus/knowledge/bench-arena-round8-horizon.md` §Design.

| Cell | Protocol | Graded turns | What it isolates |
|---|---|---|---|
| `A-INC` | full state emitted every turn | all 10 | incremental tracking **with** self-copy scaffold |
| `A-CKPT4710` | `ok` acks except turns 4,7,10 | 4,7,10 | ≤3-op latent gaps |
| `A-CKPT710` | `ok` acks except turns 7,10 | 7,10 | ≤6-op latent gaps (r9 dose cell) |
| `A-*-ack` | ungraded ack turns | – | compliance audit input (`raw` truncated to 80 chars in r8) |
| `A-MONO` | all 10 ops in one prompt, final state only | 1 | pure latent chaining |
| `B-{corrupt,clean}-{plain,hint}` | fabricated transcript with a corrupted mid state; optional "correct, don't propagate" hint | 1 | error propagation vs recovery vs capability ceiling |
| `C-{conflict,benign,norule,MONO}` | 4×4 grid, fabricated rows, late rule that binds / is vacuous / is absent / one-shot | 1 | rule-integration cost vs transcript-shape cost |
| `meta` / `filler` | problem definition (init, ops, truth, tail_touched) / burst-decorrelation request | – | reproduction input; `request_ts` ordering evidence |

Measurement rules (all four were violated at least once in r8; each cites the
round that established it):

1. **Unit = problem/seed, never request.** Draws on this server are non-iid
   (lag-1 +0.26/+0.32, 5–10-request burst horizon,
   `corpus/knowledge/bench-arena-round7-noise-n25.md`).
2. **Discount power for ESS.** At ρ≈0.3, ESS≈0.54·n: a sign test at α=0.05
   needs **n≥10** unanimous pairs or **n≥17** with one discordance
   (`corpus/evidence/round9-fleet/critic.md` §4). Report exact binomial p as an
   *upper bound* and say so.
3. **Interleave cells per problem AND insert filler requests** between
   consecutive same-cell draws; r8 did the first only, which left each
   problem's three A-cells back-to-back (`horizon.py:314`).
4. **Separate failure classes, never merge them**: parse failure (`got` null /
   non-dict), `finish=length` truncation, output-convention miss (MOV-zero),
   genuine state error. r8: 0 parse failures, 0 truncations at max_tokens 8192,
   15/19 INC failures convention-class.
5. **Grade twice** (strict + convention-tolerant) and report both.
6. **Pre-flight the manipulation**: assert the injected error survives the
   remaining ops and changes the truth final state (r8: 2/8 well-formed).
7. **Audit the control**: count ack-turn compliance per problem before treating
   a checkpoint cell as latent maintenance (r9: 16/48 and 8/56 leaks).
8. **Pre-register a decision rule with three outcomes** — blocks / survives /
   **indeterminate** — and report which fired. r9's replication returned
   indeterminate (INC 4/8 vs a ≥5/8 survival threshold); rounding that to
   "replicated" is the calibration failure the rule exists to prevent.
9. **Land the run bytes.** Strip nothing from a committed `results.jsonl`; the
   `raw` field is the only evidence for compliance, byte-identity and
   failure-mode audits (r8's landed copy had it stripped — see
   `corpus/knowledge/bench-arena-round8-horizon.md` §provenance).
10. **Report paired contrasts, never raw levels, across batches.** Absolute
   pass rates on the *same unchanged serving stack* (pid 1299, argv re-pinned
   every round) swung across rounds — r8 CKPT 1/10, r9 2/8+2/8, r11 29/64+21/64
   — but the *paired* severity contrast (same problem, both schedules) replicated
   at +0.352. Batch is a nuisance factor; the within-problem paired difference
   is the transportable quantity. Shrink the planning effect size from the
   prior small-n estimate (r9 d=0.52 → r11 MDE d=0.35), size n for it, and let
   the verdict rule fire. (`corpus/knowledge/bench-arena-round11-power.md`)
11. **An ordered alternative gets an ordered test.** For a k-arm dose ladder on
    the same problems, one **Page's trend test** on within-block ranks
    (midranks for ties; per-block null variance `[Σj² − (Σj)²/k]·S²_block`,
    = `5·S²_block` at k=4; `L = Σ_j (j+1)·R_j`; direction ≡ `L > E_L`) beats
    k−1 paired t-tests (multiplicity) and Friedman + post-hoc (discards the
    ordering). Seeded MC on this lane's anchored alternative: power 1.000 at
    n=44–64, 0.989 at n=48 even with the effect halved, minimum n for 80%
    power = 12 — so at n=64 the binding risk is **anchor validity, not power**
    (the anchor's densest leg came from r8 at n=10). (`probe_plan_r12.md` §2.3 E1;
    `power_analysis_r12.md` §3)
12. **Repeatability is not replication on a non-deterministic server.** A later
    run over the *same* problems, seeds and served unit re-measures; it does not
    independently replicate. llama.cpp documents multi-slot draws as not
    bit-reproducible (issue #7052: 5–8 unique completions from 8 slots at
    temp 0; maintainer: "results for multiple slots are still not 100%
    deterministic"), vLLM's docs say the same, and this lane measured the
    batch-level swing itself (r8 1/10, r9 2/8+2/8, r11 29/64+21/64 on an
    unchanged argv). Name it *within-run/later-run repeatability*, cite the
    source, and never write "replicated". (`corpus/evidence/round12-fleet/r12-prior-art-ladder.md` §2.2, §7 C2)
13. **Absorb critic defects pre-hash and log them inside the hashed document.**
    When the design critic lands before the first bundle hash, fix in place and
    add a numbered amendment log (§9) to the document being hashed: the hash
    then covers the corrections and there is no v2 chain for a later round to
    reconstruct. Round 12: 1 FATAL + 5 MAJOR + 4 MINOR from the critic, plus 5
    L1-found defects, all recorded with their disposition before
    `prereg-bundle.sha256` was written. (`probe_plan_r12.md` §6 step 4, §9)
14. **A pass bar on a binary rate is interval-gated (round 25; QUALITY Q11).**
    PASS only when the exact two-sided 95% Clopper–Pearson lower bound reaches
    the bar; with 0 / 1 / 2 errors at bar 0.80 that needs n ≥ 17 / 26 / 34
    (`plans/fixtures/r25/power_table.tsv`). A target with 0 ground-truth trials
    is UNTESTED, not FAIL; a leg share is reported as a Rogan–Gladen bound,
    [0, 1] when the leg was never observed. Repeated sends of a few prompt
    bodies make the interval trial-level only — print `bodies=m`. Applies to
    every bar this lane sets, not only the r8/r9 probe family above. Runnable:
    `python3 plans/attrib_calibration.py --summary`.
    (`corpus/knowledge/attribution-interval-calibration.md`; S027–S030, S011)
15. **Audit the response grader, not only the model (round 26).** When extraction policy changes or a new
    response format appears, run `python3 plans/grader_perturb.py --summary` and `--selftest`. FAMILY MP
    counts verdict invariance; MC counts rejection of a provably changed graded answer; PC counts policy
    conformance (D1 is not an MP defect). Require the frozen 1964-record baseline to replay with 0 exclusions.
    Inspect format strata and pid-composite sensitivity: a pooled nominal CP95 PASS against 0.95 is not
    a future-response guarantee and does not erase MULTI's 17 PASS→FAIL flips under F1/F2. Preserve the exact
    transform span and task contract. The method already exists as tooling (evalmut 0.1.0, S045); this is a
    lane-specific audit, not a novel testing method. (`plans/round-26-claims.md` Amendment 1; Q13 governs
    admission evidence before landing; source-opening record `corpus/lessons/round-26.md`.)

Scope limit: every number from these probes is a **sub-3-bit (UD-IQ2_XXS) +
llama.cpp serving-stack** observation, not a Qwen3-Coder-30B-A3B capability
measurement (published safe bands: W8A8/W4A16 ≈ lossless, 4-bit up to −59%;
`corpus/knowledge/eval-prior-art-calibration.md` §cross-cutting).
Serving-stack facts are process-pinned as of round 10 (pid 1299; `/proc/<pid>/cmdline`
== `~/.config/systemd/user/qwen-coder.service` ExecStart, 41 tokens, EXACT_MATCH):
the stack also carries `--cache-type-k/v q4_0` (4-bit KV cache — an unstated premise
of every r8/r9 number), `--kv-unified` with `--parallel 2` (each of 2 slots reports
the full 16384 ctx; slot draws do not share a halved context), `--no-context-shift`
(long transcripts hard-stop rather than slide — relevant to truncation semantics),
and a custom non-upstream chat template (`--jinja --chat-template-file
~/.config/llama/qwen-coder-godspeed.jinja`). `PROVINCE.md` §Surfaces records the pin;
a hermetic gate must never read `/proc` — pin committed bytes instead.

**Currency 2026-10-15:** the pin above is historical process identity, not a live
process — `/proc/1299/cmdline`, the unit, the chat template and the `:34113`
endpoint are unavailable per `corpus/evidence/round13-coverage/surface-receipt.json`,
and kama's snapshot `20261014T124232Z` independently records the unit deleted
with no listener (`../kama-shokunin/PROVINCE.md`). Serving-plane health and
detection belong to kama; restoration is operator-owned. The durable copy of
the pin is the committed `descriptors` record named below.
Round 11 landed the durable form of this pin: the r11 `descriptors` record
(first line of `corpus/evidence/round11-power/results-r11.jsonl`) re-captures
pid + full argv + served-model id **inside committed bytes** — a service
restart invalidates the live pid but never the record (box-3 break B3).

## Hermetic grader (operability gate) — `grader.py`

`grader.py` (repo root; stdlib only; no network, no endpoint) replays four
committed probe trees against their stored bytes and recomputes every asserted
SUMMARY/analysis value. Deterministic and PYTHONHASHSEED-independent — never
iterate a set where output order matters. Round 12 extended the gate from 280
to 732 checks by adding its two-family tree; round-14 landing added the missing
analysis-byte pin, yielding **733 checks**. `--selftest` is S0–S7.

| Tree | Recomputed from committed bytes |
|---|---|
| `corpus/evidence/round8-horizon/` | `meta` regenerated from seeds `700 + pid*13` (incl. the `+977` retry chain) and matched field-for-field; each of the 258 non-meta `raw` strings re-parsed through the shipped `extract_json_block` (fenced block first, brace-regex fallback — 2 r9 records only parse via the fallback) and re-graded against `meta`'s `truth`; B cells re-scored to `outcome` ∈ {corrected, propagated, other} incl. the historical-value `corrupt_from` rule; C cells re-graded via `grade_c` / `valid_latin`; all 11 `run.log` SUMMARY lines |
| `corpus/evidence/round9-replication/` | `meta` from seeds `2000 + pid*29`; the 4-cell table incl. mean final `nwrong` (4/8 · 0.500, 2/8 · 0.875, 2/8 · 1.375, 0/8 · 2.250); the 284-record census (8 `meta` / 248 scored / 28 `filler`); sign tests (math.comb exact binomial), onset ladder, failure classes, ack compliance (32/56 = 57.1%, 48/64 = 75.0%), cross-round table, prediction-scoring table vs `predictions-r9.md`, prediction sha256 chain and the ordering proof (hash time ≤ first `request_ts`) |
| `corpus/evidence/round11-power/` | `meta` from seeds `3000 + pid*41` (pids 201–264); the 1473-record census (1 descriptors / 64 meta / 320 graded / 960 ack / 128 filler / 0 error) and 1409-request count; each graded `raw` re-parsed and re-graded against `meta`'s `truth`; both `run.log` SUMMARY lines (29/64, 21/64); every `analysis_r11.md` stored line — observed table (both mean columns), paired diff +0.352 / sd 0.820, `t=+3.431`/`p=0.0011` (NR betai t-CDF, df=63), CI, exact sign (26/7/31, `math.comb`) + McNemar (b=13 c=5), verdict-rule consistency incl. the sign-agreement downgrade, Brier 0.153, point-scoring table; descriptors serving-stack pins; the preregistration-bundle sha256 chain and the ordering proof (bundle-hash time ≤ first `request_ts`, descriptors first in file order) |
| `corpus/evidence/round12-ladder/` | family-1 metas from `3000 + pid*41` and family-2 metas from `5000 + pid*37` (including retry chains); 4,114-record census; all 1,328 graded raws re-parsed/re-graded; seven run-log SUMMARY cells; E1 Page trend, E2–E5 paired/sign/McNemar statistics, E6 Brier/BSS/calibration/reliability tables, R1–R5 branch consistency; all 727 forecast events and three prediction-file hashes; descriptor start/end equality; bundle/run-script ordering chain; md5 pins for results, run log, and generated analysis |

| Exit | Meaning |
|---|---|
| `0` | every recomputed value equals the stored one |
| `1` | ≥1 mismatch, each printed `MISMATCH <check-id>: stored=<x> recomputed=<y>` |
| `2` | a required input file is missing or unreadable |

Run `python3 grader.py` (defaults resolve beside the script); inputs are
overridable via `--r8-jsonl/--r8-runlog/--r9-jsonl/--r9-md`,
`--r11-jsonl/--r11-md/--r11-runlog`, and
`--r12-jsonl/--r12-md/--r12-runlog`. Ten md5 pins fire only on default paths,
so deliberate copies grade without pin noise. `--selftest` uses temp copies:
S0 clean control; S1/S4 stored-`ok` flips; S2/S5 SUMMARY edits; S3 raw-digit
corruption; S6 known-value t/Beta anchors; S7 r12 Page/sequence/Brier/Newton
anchors. It exits 0 only when every corruption is caught with the expected
check-id (assert code **and** diagnostic). Round-14 mutation verification also
killed 4/4 fresh r12 corruptions: SUMMARY count, stored raw, probability hash,
and missing ordering sidecar.

Falsification (round 10, both runs recorded in `LOG.md`): committed tree →
**exit 0**, `CHECKS n=149 mismatches=0`; independent mutation battery
(`/tmp/kengaku-r10/mutate_test.sh`, written by an L2 before the grader
existed, then executed) → M0 control exit 0; M1 `ok`-flip exit 1 with exactly
`r8.replay.A-INC.ok` (layer isolation proven: the flip is summary-insensitive
because SUMMARY counts last-graded-turn oks); M2 SUMMARY edit exit 1
(`r8.summary.A-INC` + 2 cross-round checks); M3 `raw` corruption exit 1
(7 mismatches) — 4/4 expectations met. One stored value is
adjudicated-defective and pinned as an erratum pair (`ERRATA` in `grader.py` +
`corpus/evidence/round9-replication/replication.md` §Errata): the r9
final-turn state-error count, stored 12/32, recomputes to **24/32**; editing
either side without a recorded ruling fails the gate.

## Gate/probe registry (PROTOCOL §Gate standard)

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `hermetic-grader` | gate | `python3 grader.py` (repo root; `--r8-*`/`--r9-*`/`--r11-*`/`--r12-*` overrides) | `0` clean · `1` failed (`MISMATCH <check-id>`) · `2` could-not-evaluate (required input missing/unreadable) | `python3 grader.py --selftest` (S0–S7, temp copies) | committed trees `corpus/evidence/round8-horizon/`, `round9-replication/`, `round11-power/`, `round12-ladder/` + md5/sha pins inside `grader.py` | none — repo bytes only; no network, no endpoint, never `/proc` | kengaku |
| `coverage-census` | probe | `python3 corpus/evidence/round13-coverage/coverage_census.py [--revision REV]` | `0` census completed even with gaps · `2` could-not-evaluate | none declared at write time (spelling owned by the census seat) | fixed candidate paths from `corpus/evidence/round13-coverage/surface-receipt.json` | none — read-only path/index census | kengaku |
| `interval-reverdict` | gate | `python3 plans/attrib_calibration.py --summary` (lane root; `--root DIR`, `--json`) | `0` every stored line re-derives · `1` failed (`MISMATCH …`, incl. a P1 receipt whose sha256 left the frozen manifest) · `2` could-not-evaluate (`SETUP`: no or unreadable receipts) | `python3 plans/attrib_calibration.py --selftest` (18 checks incl. red runs R1–R6, temp copies) | nine r21–r23 receipts in `corpus/evidence/` pinned by sha256 in the script; `plans/fixtures/r25/cp_reference.tsv` | none — repo bytes only; imports `grader.py` betai, no network | kengaku |
| `state-assertion-check` | gate | `python3 plans/state_check.py --summary` (lane root; `--root DIR`, `--json`) | `0` all comparable frozen assertions match (superseded counted apart) · `1` failed (`MISMATCH …`) · `2` could-not-evaluate (`SETUP`: unreadable lane file, empty population, broken seed pin) | `python3 plans/state_check.py --selftest` (mutation cases on temp trees) | frozen P2 population in the script (base `6180e4f`); SHONEN seed `plans/fixtures/r25/shonen-seed.txt` sha256-pinned | runs `python3 grader.py` and `freeze-check` as fixed argv (no shell); no network | kengaku |
| `grader-perturb` | probe | `python3 plans/grader_perturb.py --summary` (`--root DIR`, `--json`) | `0` audit completed, including family FAIL findings · `1` population pin/baseline/selftest failure · `2` usage/setup | `python3 plans/grader_perturb.py --selftest` (family red mutations) | four r8/r9/r11/r12 result-file SHA-256 pins; 1964 raw+ok records, 0 exclusions | none — committed bytes, no endpoint | kengaku |
| `gate-timing` | gate | `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-26.md --commit REV` | `0` explicit returned report support present in requested tree · `1` missing/invalid support · `2` setup/usage | `python3 plans/gate_timing_check.py --selftest`; red `--lesson corpus/lessons/round-25.md --commit 8ea41f9` | commit-tree lesson, candidate writer and wave registries/reports; presence does not imply endorsement | none — read-only Git plumbing | kengaku |
| `benchmark-spec-audit` | gate | `python3 plans/benchmark_spec_audit.py --summary` (`--root DIR`, `--json`) | `0` pinned static schema inventory clean, NOT task validity · `1` structural finding · `2` could-not-evaluate, including missing/tampered snapshot/manifest/selection | `python3 plans/benchmark_spec_audit.py --selftest` (isolated miniature cases plus real CLI pin failures) | `plans/fixtures/r28/webarena/manifest.json`, selected-task-ids.json; both digests independently pinned in code, original upstream files retained with LICENSE | read-only; selftest uses temporary trees, no upstream execution/network | kengaku |
| `registry-reference-check` | gate | `python3 plans/registry_check.py --summary` (`--root DIR`, `--json`) | `0` frozen literal-reference coverage clean, NOT source truth · `1` mismatch · `2` could-not-evaluate, including missing/tampered population | `python3 plans/registry_check.py --selftest` (isolated hand-expected references and CLI population controls) | `plans/fixtures/r28/registry/population.json` digest in code;13 rows and35 baseline knowledge paths, new files excluded | read-only; selftest uses temporary trees | kengaku |
| `config-projection` | gate | `python3 plans/config_projection.py --summary` (`--root DIR`, `--json`) | `0` pinned 812×3 projection with expected structural identities, NOT deployment configs or task validity · `1` projection/invariant finding · `2` could-not-evaluate, including missing/tampered manifest/input, unrecognized generator contract, internal error or `python -O` | `python3 plans/config_projection.py --selftest` (hand cases, digest-pinned seat fixtures, isolated CLI pin failures); `python3 plans/fixtures/r29/mutation_witness.py` (12 persisted mutants) | `plans/fixtures/r29/manifest.json` digest and exact generator statements in code; hand-fixture digests in code | read-only; selftest and witness write only under /tmp; generator never imported or executed | kengaku |
| `sources-adopt` | gate | `python3 plans/sources_adopt.py` (lane root; `--registry`, `--package`, `--admit-ids`, `--entries`, `--access-date`, `--recheck`, `--scope-to-admit`, `--attest-opened`, `--quote-file`, `--artifact`, `--url-map`, `--out`) | `0` gates an append and prints the append block · `2` usage error or unreadable quote artifact · `3` staged/registry id collision · `4` malformed staged row (escaped pipe, column count, quote spans) · `5` requested id absent · `6` quote over the 25-word cap · `7` quote absent from artifact bytes · `8` quote bound to a mismatched URL · `9` quote has no url-map entry | `python3 plans/sources_adopt.py --selftest` (17 cases: registry/package shapes, quote-location pins, misused flags) | committed lane registry `corpus/SOURCES.md`, read-only staged package `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`, pinned captures under `.ufo/waves/round-32/assimilation/captures/` | reads lane registry + staged rows; writes only under `--out`; quote mode reads artifact + url-map; no network | kengaku |
| `package-gate` | gate | `python3 plans/pkg_gate.py package --root DIR --spec plans/pkg-spec-r35.json [--rerun] [--require-clean-tree]` (subcommands `d4-line --file F --spec SPEC`, `d5-line --file F --capture-dir D --spec SPEC`) | `0` accept · `1` reject (a hardened check fails) · `2` usage/setup (unreadable spec/root, unevaluable) | `python3 plans/round36_c1_verify.py --lane .` (14-fixture battery: P0 genuine, P1–P7 junk packages, L1/L4 genuine and L2/L3/L5/L6 labelled-but-false lines; green means `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`) | `plans/pkg-spec-r35.json` sha256 `e085b435…` pins rows S105–S107 with their capture digests, receipt `corpus/evidence/round35/tb2-grader-probe.txt` sha256 `2359d906…`, and three frozen instruments (`tb2_grader_probe.py`, `round35_c1_verify.py`, `defect_ledger.py`); `corpus/evidence/round35/tb2-eval/SHA256SUMS` | reads ROOT + spec; `--rerun` re-executes the package's own `probe_cmd` inside ROOT and byte-compares the receipt to its pinned sha256; `--require-clean-tree` reads `git -C ROOT ls-files --others --exclude-standard`; no network, no commit, no lane write | kengaku |
| `round36-c1-battery` | gate | `python3 plans/round36_c1_verify.py --lane .` (`--legacy`: the seven junk fixtures against the round-35 counter of record) | `0` C1 predicate holds (`FIXTURES … false_green=0 false_red=0 unevaluated=0`, `rows=4 closed=4 observed_pass=4 mismatches=0`, `PREDICATE C1 pass`) · `1` any fixture wrong or unevaluated, any ledger row disagreeing with its check, predicate fail · `2` usage | none declared beyond itself (the battery is the self-test; `--legacy` is the pre-fix control) | `plans/round36_c1_verify.py` sha256 `d7c3687c…`; `plans/pkg-spec-r35.json` sha256 `e085b435…`; `corpus/defects-round35.jsonl` four rows R35-D1…D4, each closed only while its check passes | none — fixtures are index-only git repos under `mktemp`, built from committed round-35 bytes; reads `git ls-files --others` and `git ls-tree`; no network | kengaku |
| `regex-log-probe` | probe | `python3 plans/regex_log_probe.py --lane .` (`--dry` prints the 24 frozen cases, regexes and predictions without running the grader) | `0` all 24 predictions matched · `1` a mismatch (`match=NO` on the differing case) · `2` grader digest refused (`REFUSE grader digest …`) | `python3 plans/round36_c2_verify.py --lane .` W5 (probe digest, fresh run byte-equal to the receipt, summary line `cases=24`; red until the C2 entry lands) | grader `corpus/evidence/round36/tb2-regex-log/test_outputs.py` sha256 `345c3bd0…` pinned in the probe; probe digest `d58194c8…` pinned in `plans/round36_c2_verify.py` (amendment 1); receipt `corpus/evidence/round36/regex-log-probe.txt` | writes only its own `mktemp` dir and monkeypatches the grader's `Path` so `/app/regex.txt` resolves there; imports the captured grader with `importlib`; no network, no model, never the live `/app` | kengaku |
| `git-webserver-probe` | probe | `python3 plans/git_webserver_probe.py --lane .` (`--dry` prints the 22 frozen cases, their servers and predictions with no sandbox; `--smoke` exercises the bubblewrap plumbing only; `--work DIR` scratch parent) | `0` every case yielded exactly one verdict and the summary line printed — **mismatches are on the summary line, never in the exit code** (`mismatches=1` still exits 0, measured) · `1` `--smoke` only: the sandbox did not answer 200 · `2` setup (a capture not at its pinned digest, `/usr/bin/bwrap` not executable, a case yielding no single verdict) | `python3 plans/round37_c2_verify.py --lane .` V1 (capture manifest) and V5 (probe at its freeze digest, `--dry` byte-equal to `corpus/evidence/round37/git-webserver-dry-cases-freeze.txt`): on a clean clone 2026-10-26, `V1 ok` and `V5 ok probe=frozen dry_byte_equal=True`. The 22-case reproduction is the package gate's P10 (`--rerun`), which byte-compares the fresh receipt: `P10 ok probe_rerun=byte-equal bytes=8443` (same run, 53 s wall) | captures `corpus/evidence/round37/tb2-git-webserver/` with `test_outputs.py` sha256 `526aee3d…`, `verify.sh` `1dc44c92…`, `instruction.md` `62151b73…` (probe `PINS`); probe sha256 `63cb75cf…`; receipt `corpus/evidence/round37/git-webserver-probe.txt` sha256 `83550712…`, summary `cases=22 observed_pass=9 observed_fail=13 mismatches=0` | needs `/usr/bin/bwrap`; one sandbox per case with `--unshare-net --unshare-pid --unshare-ipc` (`plans/git_webserver_probe.py:204`), `HOME=/work/home` (`:235`), `/tests` bound read-only to the captures (`:209-213`); writes only under `--work`/`$TMPDIR` and removes it; imports the captured grader function; no network beyond the case's private loopback, never the host's :8080 | kengaku |
| `round37-c1-mutants` | gate | `python3 plans/round37_c1_verify.py --lane .` (`--battery r36` the frozen 14-fixture battery only; `--battery-dir DIR` and `--only M01,M02` development selectors; `--work DIR`) | `0` predicate holds: `GATE plans/pkg_gate.py sha256=frozen`, `BATTERY fixtures=<n> wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass` · `1` any survivor, invalid mutant, null detection, wrong declaration or renamed disagreement, or the gate not at `ea638822…` (`sha256=NOT-AT-FREEZE-DIGEST`) · `2` usage, duplicate fixture id, or a fixture returning a forbidden argv (a `--spec`, or a first token other than `package`/`d4-line`/`d5-line`); the development selectors print `PREDICATE C1 n/a` and exit by the wrong/renamed/survived rule alone | none beyond itself; `--battery r36` is the do-nothing control (`MUTANTS total=55 killed=5 survived=50` in `control-c1-nothing.txt`), and a fixture must declare `expect` plus its exact `DEFECT` clause set or it counts `wrong` | gate `plans/pkg_gate.py` sha256 `ea638822…`; counter sha256 `dbc9f719…`; `plans/pkg-spec-r35.json` sha256 `e085b435…`; 55 mutants M01–M55 frozen in the counter with clause and advertised class; `plans/round-37-claims.md` at freeze | fixtures and gate copies under `--work`/`$TMPDIR` (`gates/ref.py`, `null.py`, `Mxx.py`); `git init` + index-only `git add` inside fixture dirs only; read-only on the lane, no commit, no network | kengaku |
| `round37-c2` | gate | `python3 plans/round37_c2_verify.py --lane .` (`--work DIR`) | `0` `checks=7 defects=0` then `PREDICATE C2 pass` · `1` any `Vn DEFECT <note>`, including a check that raises (`error …` is a defect, never a pass) · `2` usage | itself; freeze control `control-c2-nothing.txt` is `checks=7 defects=4` (V2, V3, V4, V7), exit 1. Re-measured on a clean clone of `44b7298` 2026-10-26: `V1 ok`, `V2 DEFECT gate_exit=1`, `V3 DEFECT rows=3 bad=['S111:row','S112:row','S113:row']`, `V4 DEFECT receipt or entry absent`, `V5 ok`, `V6 ok census_exit=0`, `V7 DEFECT receipt or entry absent`, `checks=7 defects=4`, exit 1 — the reds are the entry and the index rows, not the probe | capture `SHA256SUMS` sha256 `e70bb662…` (six files: S111 `526aee3d…`, S112 `1dc44c92…`, S113 `62151b73…`, plus `test.sh`, `task.toml`, `solve.sh`); probe `63cb75cf…`; dry table `0095e591…`; `plans/pkg-spec-r37.json` sha256 `4c61d103…`; receipt `83550712…`. V6 shells out to the absolute `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate` | writes one effective spec copy in its scratch dir; V2 runs `plans/pkg_gate.py package --root <lane> --require-clean-tree --rerun` (timeout 900 s), so P10 executes the frozen probe (bubblewrap, 22 cases, ~58 s measured) and byte-compares to the receipt; reads the lane only, never edits it | kengaku |
| `anchor-digest-check` | gate | `python3 plans/anchor_digest_check.py --lane DIR [--evidence-ref head or index] [--verbose]` — landed from wave-1 seat R37AnchorSweep (`.ufo/waves/round-37/build/R37AnchorSweep.md`) | `0` no defect · `1` one `DEFECT <Sid> anchor token=<hex> class=<cls> detail=<why> loc=<file>:<n>` line per defect, then `rows=<n> tokens=<n> defects=<n>` · `2` usage or a check that cannot run (`USAGE:`, lane not a directory, no `corpus/SOURCES.md`, not a git work tree, unreadable evidence, `--evidence-ref bogus`) — a check that cannot run never passes | none in the script; falsifiers are external (11-case matrix `fixture_matrix.py`, receipt `fixture-receipt.txt`, 5/5 mutants killed by distinct classes), so this row claims no `--selftest`. Measured on the lane tip `44b7298`: `rows=103 tokens=11 defects=5`, exit 1 (S110 `class=digest-short`; S070/S072/S073/S074 `class=digest-unknown`); `0` only after the erratum plus `corpus/evidence/round37/anchor-captures/` land (5 captures, `sha256sum -c` clean) | no constants in code: every `sha256 <hex>` token in the anchor cell (6th cell, 0-3 leading spaces, 11 cells, as the census reads them) must be 64 lowercase hex and equal a committed `git ls-tree -r <evidence-ref> -- corpus/evidence` blob digest or a 64-hex line of a committed `SHA256SUMS`, unless a `corpus/lessons/*.md` line `Erratum (round 37): S<id> anchor sha256 …` carries both the token and a resolvable digest; `--evidence-ref` reach is `corpus/evidence/` only, default `head` | none at runtime — read-only `git ls-tree`, no temp files, `TMPDIR` untouched | kengaku |
| `ledger-tip` | gate | `python3 plans/ledger_tip.py --source <lane> --work <scratch>` (clean shared clone of the tip; `--lane <clone>` control mode) | `0` every closed ledger row's check passes at the tip and no open row passes · `1` a mismatch (`agree=NO` on the row) · `2` usage/clone refusal | controls `.ufo/waves/round-37/build/R37LedgerTip/control-ctl*.txt` (each check shown able to fail on a broken clone) | ledgers `corpus/defects.jsonl` (checks `plans/defect_ledger.py`) and `corpus/defects-round35.jsonl` (checks `plans/round36_c1_verify.py`) | writes only `<work>/lane` | kengaku |
| `build-pmars-probe` | probe | `python3 plans/build_pmars_probe.py --lane .` (`--dry` prints the 22 frozen cases, `violates=` tags and predictions with no sandbox; `--smoke` exercises the bubblewrap plumbing only; `--work DIR` scratch parent) | `0` every case yielded four verdicts (the receipt's `match=` column carries prediction agreement) · `2` setup (capture digest, `bwrap` or `gcc` missing, a case without four verdicts) | receipt `corpus/evidence/round38/build-pmars-probe.txt` (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`, first recorded run `e95cf550`, second run byte-equal) | captures `corpus/evidence/round38/tb2-build-pmars/` (S115, S116); frozen digest `32f0771c…` (`plans/round38_c2_verify.py`) | scratch under `--work`/`$TMPDIR` only | kengaku |
| `round38-c1-mutants` | gate | `python3 plans/round38_c1_verify.py --lane .` (`--battery r37` the round-36+37 battery only; `--battery-dir DIR`, `--only N01,N02` development selectors; `--work DIR`) | `0` predicate holds: `PINS total=14 mismatched=0`, `BATTERY … wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=22 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass` · `1` otherwise · `2` setup | controls `.ufo/waves/round-38/claims/control-c1-nothing.txt` (`killed=0 survived=22`), `control-c1-gate-edited.txt` (`invalid=22`) | 14 input digests in its `PINS`; mutant list N01–N22 | scratch under `--work` | kengaku |
| `round38-c2` | gate | `python3 plans/round38_c2_verify.py --lane .` (`--work DIR`) | `0` `checks=7 defects=0` then `PREDICATE C2 pass` · `1` any `Vn DEFECT` (a check that raises is a defect) | controls `.ufo/waves/round-38/claims/control-c2-nothing.txt` (`defects=4`), `control-c2-skip.txt` (`defects=2`) | spec, gate, probe, dry table and five captures pinned in the counter | scratch under `--work` | kengaku |
| `mutant-direction-check` | gate | `python3 plans/mutant_direction_check.py --lane . [--counter plans/round38_c1_verify.py] [--work DIR]` | `0` every frozen mutant's declared kill direction is observed or unwitnessed · `1` a `MISLABELLED` mutant | shown able to fail on the round-38 list: `DIR N21 D5 declared=silence observed=mirror MISLABELLED` (`.ufo/waves/round-38/integrate/direction-check.txt`) | reads the counter's MUTANTS and battery | scratch under `--work` | kengaku |
| `tip-receipts` | gate | `python3 plans/tip_receipts.py --lane DIR [--work DIR] [--list] [--tamper REL] [--only SUBSTR]` — assimilated from `considerthese/2026-10-25.md` proposal 2(c), drafted by wave-1 seat R38TipReceipts | `0` every committed `probe*` receipt with a committed re-run command is byte-equal at the tip and the tamper control answers `differ` · `1` a `differ` or a failed control · `2` setup | `.ufo/waves/round-38/build/R38TipReceipts/tip-receipts-tamper-control.txt` (one flipped byte → `differ`) | population `corpus/evidence/**/probe*.{txt,log}` at HEAD | scratch under `--work`/`$TMPDIR` | kengaku |
| `git-leak-probe` | probe | `python3 plans/git_leak_probe.py --lane .` (`--dry` prints the 25 frozen cases, `violates=` tags and predictions with no sandbox; `--stage-check` builds each case's repository state and prints only stage exit codes, the grader module never imported; `--work DIR` scratch parent) | `0` every case yielded five test verdicts and the summary line printed — **prediction mismatches are on the summary line, never in the exit code** (`cases=25 … mismatches=0` is a data line; the probe exits 0 either way) · `1` `--stage-check` only: a case's setup or recipe stage exited non-zero · `2` setup (a capture not at its pinned digest, `/usr/bin/bwrap` or `/usr/bin/git` not executable, a case without five verdicts, duplicate case id / unknown tag / malformed prediction; the per-case child's internal exit `3` surfaces here, never as a verdict) | `python3 plans/round39_c2_verify.py --lane .` V1 (capture manifest, 7 files) and V5 (probe at its freeze digest, `--dry` byte-equal to the frozen table) | captures `corpus/evidence/round39/tb2-git-leak-recovery/` (S117 `test_outputs.py` `dc7b01c1…`, S118 `instruction.md` `54ac693f…`, plus setup/oracle/test/Dockerfile/task.toml + `SHA256SUMS`); its own `PINS` for the three captures it executes (`test_outputs.py`, `challenge-setup.sh`, `solve.sh`); probe digest `4961a50f…` and dry table `e92a5d6d…` pinned in `plans/round39_c2_verify.py` | scratch under `--work`/`$TMPDIR`, removed on exit; per-case `/app` and `/cap` exist only inside the sandbox | kengaku |
| `round39-c1-mutants` | gate | `python3 plans/round39_c1_verify.py --lane .` (`--battery r38` the round-36+37+38 battery only — the do-nothing control; `--battery-dir DIR` and `--only M01,M02` development selectors, which print `PREDICATE C1 n/a`; `--work DIR`) | `0` predicate holds: `PINS total=26 mismatched=0`, `BATTERY fixtures=<n> wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass` · `1` any survivor (which prints `exhibits=<directions>`), invalid mutant, null detection, `wrong>0`, `renamed_disagree>0`, `sidechannel>0`, a pin mismatch, or a gate digest change during the run (`invalid(gate file changed during the run)`) · `2` setup/usage (duplicate fixture id, a fixture returning a forbidden argv — a first token other than `package`/`d4-line`/`d5-line`, or a `--spec` outside the fixture dir — a module import/build failure) | controls `.ufo/waves/round-39/claims/`: `control-c1-nothing.txt` (`BATTERY fixtures=86`, `MUTANTS total=7 killed=3 survived=4`, `PREDICATE C1 fail`, `exit=1`), `control-c1-gate-edited.txt` (`PINS mismatched=1`, `invalid=7`), `control-c1-hostile-inproc.txt` (the round-38 in-process `run_gate` patch shipped as a battery39 module: `BATTERY fixtures=88`, unchanged `killed=3 survived=4`) | 26 input digests in its `PINS` (gate `ea638822…`, round-37/36 counters, round-35 spec, round-37 attribution audit, 9 battery37 and 12 battery38 modules); frozen MUTANTS M01–M07 with `adv`/`witness` cells; directions `silence`/`mirror`/`rc-silence`/`rc-mirror` | scratch under `--work`; gate copies written only after every child process exits and digest-checked after every muted run | kengaku |
| `round39-c2` | gate | `python3 plans/round39_c2_verify.py --lane .` (`--work DIR`) | `0` `checks=7 defects=0` then `PREDICATE C2 pass` · `1` any `Vn DEFECT <note>` (a check that raises prints `error <Class>: …` and is a defect, never a pass) · `2` usage (argparse) | itself; freeze control `control-c2-nothing.txt` is `checks=7 defects=4` (V2, V3, V4, V7), `PREDICATE C2 fail`, `exit=1`, and its embedded gate dispatch prints eight `P#` defects (P2, P3, P4, P6, P7, P8, P9, P10) because the receipt, entry and index rows are absent at freeze | spec `plans/pkg-spec-r39.json` `f62163ce…`, gate `ea638822…`, probe `4961a50f…`, dry table `e92a5d6d…` and the seven captures (`CAPTURES`) pinned in the counter | scratch under `--work` | kengaku |
| `order-check` | gate | `python3 plans/order_check.py --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt` (lane root; all three flags are required, `plans/order_check.py:143-145`) — Q30's order-of-operations gate | `0` order holds: `ORDER ok no claims file committed at or before the receipt shows the frozen probe executed`, then `ORDER RESULT PASS` (`plans/order_check.py:204-206`) · `1` order broken: one `ORDER FAIL <clause> …` line per broken clause (`freeze-contains-receipt`, `receipt-before-claims`), one `ORDER HIT <path>@<commit>:<n> kind=<kind> …` line per claims blob that shows the probe executed, then `ORDER FAIL <clauses> hits=<n>` and `ORDER RESULT FAIL` (`plans/order_check.py:184-202`) · `2` could-not-evaluate: `ORDER ERROR <reason>` on stderr then `ORDER RESULT ERROR` — not a git work tree, claims or receipt never committed in HEAD, claims file not named `round-NN-claims.md`, path outside the lane, mid-scan `git cat-file` failure, argparse (`plans/order_check.py:151-175`, handler `:207-210`) | no `--selftest` in the script; falsifiers are external — `plans/round40_c1_verify.py` mutants `O04` (`rc-silence`), `O12` (`rc-error`), `O14` (`error`), each witnessed pre-freeze (`.ufo/waves/round-40/claims/witness/`), and the measured controls `--receipt corpus/evidence/round39/git-leak-probe.txt` → `ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0`, exit 1; `--claims plans/round-99-claims.md` → `ORDER ERROR claims not committed in HEAD`, exit 2 | reads committed history only and pins nothing itself; the population is the claims file and the receipt named per run; the round-40 pair is `freeze bbb1095`, `receipt_commit 055748f`, `claims_dir .ufo/waves/round-40/claims/` | none — `rev-parse`, `log`, `rev-list`, `ls-tree`, `cat-file`, `merge-base --is-ancestor` only; writes nothing, imports no probe/gate/counter, never runs the probe it polices | kengaku |
| `round39-c1-audit` | gate | `python3 plans/round39_c1_audit.py --lane .` (lane root; `--battery r38` the do-nothing control; `--battery-dir DIR` and `--only M01,M02` development selectors, which print `PREDICATE C1 n/a`; `--work DIR` scratch parent, must already exist — see limits) | `0` frozen predicate holds plus the audit's extra evidence: `PINS total=26 mismatched=0`, `BATTERY … wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`, `PINS final … mismatched=0`, `AUDIT nondeterministic_kills=0`, `AUDIT C1 clean`, `PREDICATE C1 pass` (`plans/round39_c1_audit.py:418-428`) · `1` any survivor, invalid mutant, null detection, wrong/renamed/disagree/sidechannel count, a post-run pin mismatch (`PINS final`), a nondeterministic kill, `AUDIT C1 dirty`, `PREDICATE C1 fail` (`:420-428`); also a development subset whose killed set is not clean (`:423-425`) · `2` an unpinned `plans/battery37`/`battery38` module present (`AUDIT unpinned battery module present; refusing to import it`, `:286-287`), a child build/parse failure (`:303`, `:315`, `:328`, `:333`), or argparse — **`--work` absent is not `2`**: `tempfile.mkdtemp(dir=…)` raises `FileNotFoundError` at `:293` and the process exits 1, which reads as a verdict failure | no `--selftest`; the audit *is* the soundness self-test of the round-39 counter and its controls are external — `--only M01` (dev, `PREDICATE C1 n/a`) and `--battery r38` (do-nothing); measured full run at the lane tip is green (§2.5), 55 s | 26 digests in its own `PINS` (gate, round-36 and round-37 counters, round-35 spec, round-37 attribution audit, nine `battery37` modules, twelve `battery38` modules), re-hashed after the run as `PINS final`; the `battery37`/`battery38` directories must hold exactly the pinned module names | scratch under `--work`; gate copies and fixture dirs are counter-owned and removed on exit; writes no lane byte | kengaku |
| `round40-c1-mutants` | gate | `python3 plans/round40_c1_verify.py --lane .` (lane root; `--battery-dir DIR` and `--only A01,L05` development selectors print `PREDICATE C1 n/a`; `--work DIR` created if absent; `--jobs N` parallel tool runs, default 8) | `0` frozen predicate holds: `PINS total=3 mismatched=0`, `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass` (`plans/round40_c1_verify.py:458,557-570`) · `1` any survivor (printed with `exhibits=<directions>`), invalid mutant, null detection, `wrong>0`, `tampered>0`, `sidechannel>0`, a pin mismatch before or after the run, or `PREDICATE C1 fail` (`:557-570`) · `2` setup/usage: `/usr/bin/bwrap` not executable (`:460-461`), lane clone failure (`:471`), a battery build that raises (`:478`), duplicate fixture id (`:482`), argparse | itself plus the freeze controls `.ufo/waves/round-40/claims/control-c1-nothing.txt` (no `plans/battery40`: `killed=0 survived=21`, exit 1), `control-c1-tool-edited.txt` (`PINS mismatched=1`, the 11 anchor mutants `invalid`), `control-c1-hostile-daemon.txt` (a detached child that rewrites its fixture is killed with the build pid namespace, nothing killed); dev selector `--only A01` prints `PREDICATE C1 n/a` | the three tool digests in `PINS` (anchor `11bb2cad…`, ledger `853bcb2a…`, order `948d5e1d…`, re-hashed as `PINS-AFTER`); the 21 frozen mutant ids and their `old -> new` strings live in the counter's `MUTANTS` | fixtures are counter-owned dirs under `--work`; battery modules are built in `bwrap --unshare-pid` children and every tool run is sandboxed with the variant bound read-only at one fixed path; writes no lane byte | kengaku |
| `round40-c2` | gate | `python3 plans/round40_c2_verify.py --lane .` (lane root; `--work DIR` scratch parent, **must already exist** — the counter does not create it) | `0` `checks=7 defects=0` then `PREDICATE C2 pass` (`plans/round40_c2_verify.py:278-280`) · `1` any `Vn DEFECT <note>` — including a check that raises, which prints `error <Class>: …` and is a defect, never a pass (`:271-277`) · `2` argparse usage only: the script has no setup exit (`:262-284`), and an absent `--work` is a `FileNotFoundError` traceback under exit 1 (measured, §2.3) | itself; the freeze control `.ufo/waves/round-40/claims/control-c2-nothing.txt`; red at the freeze (`checks=7 defects=4`, V2 V3 V4 V7) because the package had not landed; measured green at the landing tip (`.ufo/waves/round-40/integrate/measure-final.txt`) | `plans/pkg-spec-r40.json` `4af78f4f…`, `plans/pkg_gate.py` `ea638822…`, `plans/db_wal_probe.py` `69af65df…`, dry table `corpus/evidence/round40/db-wal-dry-cases-freeze.txt` `688f3475…`, and the eight captures in `CAPTURES` (`test_outputs.py 88dc5c2a…`, `instruction.md 5a203751…`, `main.db 68cb288e…`, `main.db-wal.encrypted 68753bdc…`, `solve.sh ed8530c9…`, `task.toml 1cdc2c61…`, `test.sh 4770437e…`, `Dockerfile 63a26053…`) | scratch under `--work` only; the gate it dispatches writes nothing in the lane | kengaku |
| `db-wal-probe` | probe | `python3 plans/db_wal_probe.py --lane .` (`--dry` prints the 28 frozen cases, `violates=` tags and predictions with no sandbox; `--stage-check` builds each case's end state and prints only stage exit codes, the grader module is never imported; `--work DIR` scratch parent, created if absent) | `0` every case yielded seven test verdicts twice and both summary lines printed — **prediction mismatches are on the summary line, never in the exit code** (`cases=28 … mismatches=N` still exits 0, `plans/db_wal_probe.py:378-380`) · `1` `--stage-check` only: a case's setup or recipe stage exited non-zero (`stagecheck cases=<n> failed=<k>`, `:349`) · `2` setup: duplicate case id, unknown tag or malformed prediction (`:314-315`); a capture missing or not at its pinned digest (`:327-328`); `/usr/bin/bwrap`, `sqlite3`, `xxd` or `python3` not executable (`:331-332`); `--work` cannot be created (`:337-338`); a case that did not yield seven verdicts twice (`:362-364`) | `python3 plans/round40_c2_verify.py --lane .` V5 (probe at its freeze digest and `--dry` byte-equal to the frozen table) and V2's gate `P10` (a fresh run byte-compared to the receipt — measured `gate: P10 ok probe_rerun=byte-equal bytes=8257`, §2.3); the probe's own `--dry`/`--stage-check` modes are not a self-test of its verdicts | `PINS` in the probe: the eight captures (`test_outputs.py` `88dc5c2a…`, `solve.sh` `ed8530c9…` and six more, each checked before any case); the frozen dry table and the receipt digest are pinned by `plans/round40_c2_verify.py` (V4, V5) | scratch under `--work`/`$TMPDIR` only; per case a private `/app`, private network/pid/ipc namespaces, `/usr` and `/etc` read-only; writes no lane byte | kengaku |
| `round41-c1-mutants` | gate | `python3 plans/round41_c1_verify.py --lane .` (lane root; `--battery-dir DIR` and `--only T01,S02` are development selectors printing `PREDICATE C1 n/a`; `--work DIR` created if absent and **refused inside the lane**; `--jobs N` parallel tool runs, default 8) | `0` frozen predicate holds: `PINS total=2 mismatched=0`, `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0`, `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass` · `1` any survivor (printed `exhibits=<directions>`), invalid mutant, null detection, `wrong>0`, `tampered>0`, `sidechannel>0`, a pin mismatch before or after the run, `len(MUTANTS)!=23` or a per-tool count other than 13/10, or `PREDICATE C1 fail` · `2` setup/usage: `/usr/bin/bwrap` or `/usr/bin/python3` not executable, `--work` or the scratch root inside the lane, duplicate fixture id, a module that fails to compile or breaches the `build()` contract (argv tail must be a list of str, every absolute path inside its fixture dir), a battery load error; a development selector exits 0 only with no survivor/invalid/null/tamper/sidechannel and no pin drift, and never prints `pass` | itself, plus `.ufo/waves/round-41/claims/`: `control-c1-nothing.txt` (`BATTERY fixtures=0`, `MUTANTS total=23 killed=0 survived=23`, exit 1), `control-c1-no-mutants.txt` + `control-c1-no-mutants.patch` (`MUTANTS total=0` with `fixtures=22`, exit 1 — the non-vacuity control), `control-c1-witness-as-battery.txt` (pass reachable by witnessed work), `control-c1-tool-edited.txt` (`PINS mismatched=1 first=plans/tip_receipts.py`, 13 receipts mutants `invalid`), `control-c1-hostile.txt` (`fixtures=1 wrong=0 tampered=0 sidechannel=1`, `n/a`) | the two tool pins in code — `plans/tip_receipts.py` sha256 `e4f49714299ca1f2…`, `plans/sources_adopt.py` sha256 `38492bf175e0c619…` — plus the counter's own digest `8835a94b…` in `claims/frozen-digests.txt`; literals `TOTAL=23`, `FLOORS={receipts:13, sources:10}`; printed `ADVERTISED direct=21 indirect=2 none=0` | fixtures built and every tool run inside `bwrap --ro-bind / /` (lane hidden, fixed system PATH with no `~/.local/bin`, `--unshare-pid --unshare-net`, `HOME=/nonexistent`); scratch only under `--work`/`$TMPDIR`, removed on exit; the lane is read-only; a battery module's source carrying any SIDECHANNEL token is counted in `sidechannel=` | kengaku |
| `round41-c2` | gate | `python3 plans/round41_c2_verify.py --lane .` (lane root; `--work DIR` scratch parent, **created if absent**) | `0` `checks=8 defects=0` then `PREDICATE C2 pass` · `1` any `Vn DEFECT <note>`, including a check that raises (`error <Class>: …` is a defect, never a pass) · `2` argparse usage only | itself; freeze control `.ufo/waves/round-41/claims/control-c2-nothing.txt` (`checks=8 defects=5`: V2, V3, V4, V7, V8; `PREDICATE C2 fail`, `exit=1`) | spec `plans/pkg-spec-r41.json` `8e96421d…`, gate `plans/pkg_gate.py` `ea638822…`, probe `plans/constraints_probe.py` `8c471fbd…`, dry table `corpus/evidence/round41/constraints-dry-cases-freeze.txt` `a656ce9b…`, ten captures under `corpus/evidence/round41/tb2-constraints-scheduling/` (`SHA256SUMS` `9aafc9a0…`), order tool `plans/order_check.py` `948d5e1d…`, claims `plans/round-41-claims.md` `3b239b50…` — all pinned in the counter and in `claims/frozen-digests.txt` | scratch under `--work` only (created if absent, removed on exit); runs `pkg_gate.py package --rerun --require-clean-tree` (which re-runs the probe in a per-case `bwrap` sandbox) and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md`; the lane is read-only | kengaku |
| `constraints-probe` | probe | `python3 plans/constraints_probe.py --lane .` (`--dry` prints the 25 frozen cases, their `violates=` tags and predictions with no sandbox; `--stage-check` builds every case's end state and prints only stage exit codes, the grader module is never imported; `--work DIR` scratch parent, created if absent) | `0` every case yielded three test verdicts twice and both summary lines printed — **prediction mismatches are on the summary line, never in the exit code** (`cases=25 observed_pass=6 observed_fail=19 mismatches=2`, measured, exit 0) · `1` `--stage-check` only: a case's setup or recipe stage exited non-zero (`stagecheck cases=<n> failed=<k>`) · `2` setup: a capture missing or off its pinned digest, `/usr/bin/bwrap` or `/usr/bin/python3`/`/usr/bin/bash` missing, `--work` uncreatable, duplicate case id / unknown tag / malformed prediction, or a case that did not yield three verdicts twice (`SETUP case <id> did not yield …`) | `plans/round41_c2_verify.py` V5 (probe at its freeze digest, `--dry` byte-equal to the dry table); the probe's own second grading of the same end state (`regrade cases=25 differ=0`) | captures `corpus/evidence/round41/tb2-constraints-scheduling/` — `test_outputs.py` `1422b345…`, `solve.sh` `802d81ec…`, `alice_calendar.ics` `5a5d4580…`, `bob_calendar.ics` `c97e85db…`, `carol_calendar.ics` `32a0f868…` — pinned in the probe; dry table `a656ce9b…`; probe digest `8c471fbd…` (`PROBE_SHA256` in `plans/round41_c2_verify.py`, `frozen_instruments` in `plans/pkg-spec-r41.json`) | scratch under `--work`/`$TMPDIR`, removed on exit; one `bwrap` sandbox per case (`--unshare-pid --unshare-net`, `/app` fresh and writable, `/usr` and `/etc` read-only, `/tmp` private); the receipt carries no temp path, timing or host version | kengaku |
| `round-close-check` | gate | `python3 plans/round_close.py --lane . --round N [--census PATH]` (`--lane` must be the git work-tree top; `--selftest` runs five fixture repos; `--work DIR` is `--selftest` scratch only; `--census` else `$SHOKUNIN_ROOT`, else the lane's parents, `plans/round_close.py:138-150`) | `0` every leg passed (`ROUND-CLOSE RESULT PASS exit=0`) · `1` a leg FAILED — `ORDER RESULT FAIL` for the round's receipt(s), or the census leg exiting non-zero (`ROUND-CLOSE RESULT FAIL exit=1`) · `2` setup: `--round` absent (argparse), no census script, no claims file, no order tool, no `corpus/SOURCES.md`, `--lane` not a git work tree or not its top, the claims naming no readable receipt, or a leg exiting outside {0,1} (`ERROR`, `plans/round_close.py:200-213`) | `--selftest` (five two-commit fixture repos differing only in commit order: `A-excused-p10` 0, `B-executed-p10` 1, `C-receipt-first` 1, `D-receipt-uncommitted` 2, `E-no-receipt-named` 2; measured `SELFTEST checks=5 ok=5 failed=0`) | nothing pinned in code: the command prints the digests it evaluated — `claims=… sha256=…`, `order-tool=plans/order_check.py sha256=948d5e1d…`, `census tool=… sha256=3fb72615…`; the order tool is separately pinned by the round's own counter | none — one `git rev-parse`, one `git cat-file -e`, the order tool's own read-only git reads, the census script's read of `corpus/SOURCES.md`; `--selftest` writes only under `--work` or a fresh temp dir; no probe, gate or counter is imported or executed (`plans/round_close.py:42-45`) | kengaku |

The `coverage-census` row records the interface declared in the round-13
re-dispatch (parent, 2026-10-15); the script lands with the census seat's
artifact in this wave and the parent verifies it before commit — this row does
not assert it has run. No entry here claims a live host probe: since 2026-10-15
these entries read only committed in-repo bytes; every external surface (model
endpoint, wiki, bench-arena battery, Bailian directory, bounties ledger,
systemd unit, chat template) is absent per the receipt (§Cited local sources).

Round-26 registry addendum: `state-assertion-check` now checks frozen **P2 + P3**, P3 enumerated at base
`f11bffbf` (round-25 capability/PROVINCE assertions, SHONEN content pins, strict axis-table anchors and
round-25 index additions). P3b uses exact S001–S042, not total later sources; new rows remain out of that
population. The row's P2-only pin description is superseded, not a claim to cover every current assertion.

Round-36 registry addendum: `package-gate` (`plans/pkg_gate.py`) is the hardened admitted-entry package gate; `round36-c1-battery` builds 14 fixtures in `mktemp` index-only git repos from the committed round-35 package bytes and is the gate's self-test. The gate may not recognise a fixture by name, path or marker string — the battery's roots are named `k36-P0…k36-P7`, so a path or marker check would pass the battery while hardening nothing; this was planned for a wave-2 mutation pass that was not dispatched (`.ufo/waves/round-36/falsify-spec.json`), so the gate's clauses are untested beyond wave-1 candidates and the battery. `regex-log-probe` imports only committed capture bytes and its receipt is byte-reproducible (fresh run `cmp`-equal, 2026-10-25); no row here makes a live host or network claim.

Round-37 registry addendum: `git-webserver-probe` is the first **service-class** entry here — it starts HTTP
servers inside a per-case network namespace and reads a grader's verdict off a shell script's stdout, so it
needs `/usr/bin/bwrap` and is the only registry row with a runtime cost outside its own temp dir (~58 s for
22 cases, measured). Its exit code does not encode disagreement: a run with one flipped prediction printed
`cases=22 observed_pass=9 observed_fail=13 mismatches=1` and exited 0, so wire it by the summary line or by
the gate's P10 byte-comparison, never by `$?`. `round37-c1-mutants` is the first row whose failure mode is
"the lane's own self-assessment is wrong" rather than "a check broke": 50 of 55 advertised gate clauses were
undemonstrated at freeze (`control-c1-nothing.txt`), and the frozen mutant list, not the battery, defines
what counts. `round37-c2` bundles the package gate over the frozen template, and `anchor-digest-check`
`plans/anchor_digest_check.py` (draft) is the mechanical fix for the round-36 S110 mistyped anchor; on the
lane tip `44b7298` its draft prints `rows=103 tokens=11 defects=5` and exits 1 (S110 `class=digest-short`,
S070/S072/S073/S074 `class=digest-unknown`), and reaches `defects=0` only once the draft erratum and
`corpus/evidence/round37/anchor-captures/` are both landed — so this row records a red state, not a green one. `ledger-tip` realises `considerthese/2026-10-25.md` proposal 2(a): every closed routed-defect row's check re-runs on a clean clone of the tip.

Round-40 registry addendum: `round40-c1-mutants` mutation-tests the lane's three tripwire tools
(`anchor-digest-check`, `ledger-tip`, `order-check`) — 21 frozen mutants, each `adv` cell quoting the tool's own
docstring with file:line; its battery `plans/battery40/` is built by children in a dying pid namespace, and every
tool run is sandboxed at one fixed variant path, so a fixture cannot tell reference from mutant by path. Its limits
(wave-1 `R40RevCounters`, `R40SentinelCounter`): the bwrap sandbox isolates pids only (host fs writable, network
open), the fixture fingerprint is metadata-only, a module's build child could write into another module's fixture
before the fingerprints are taken, and a `build()` that returns a bare string is char-split before validation — so
admission keeps resting on non-author review of `plans/battery40/`. Run it only with `--lane` on a disposable clone.
`order-check` is Q30's gate; from round 40 `plans/round_close.py --lane . --round N` invokes it once per receipt the
round's claims name, then runs the sources census, and exits 0 only when every leg passes (1 a leg failed, 2 setup;
`--selftest` runs five fixture repos) — measured red on round 38 and green on rounds 39 and 40 (wave-1
`R40CloseCheck`). `tip-receipts` now also derives a receipt's probe from the receipt's own stem when the RECEIPTS
table does not name it (`--list` prints `origin=derived`), so the round-39 and round-40 receipts are re-run instead
of skipped (wave-1 `R40TipReceipts`: both `equal`, tamper controls `differ`). R2 of the round-39 closure:
`plans/git_leak_probe.py` does not create `--work` (an absent dir is a `FileNotFoundError` traceback, exit 1, a code
its row maps to `--stage-check` only); the probe is pinned by `plans/round39_c2_verify.py` `PROBE_SHA256` and
`plans/pkg-spec-r39.json` `frozen_instruments`, so it is not edited — create `--work` first (`R40RegistryRows` §3,
measured: a one-line edit reds the round-39 C2 counter's V2 and V5). The same precondition holds for `round39-c2`,
`round40-c2` and `round39-c1-audit`.

Round-41 registry addendum: `round41-c1-mutants` is the round-41 C1 counter over the two tools round 41 leaves
unedited (`tip_receipts.py`, the `sources_adopt.py` CLI): 23 frozen mutants, 21 `direct` and 2 `indirect`
advertised behaviours, and a predicate that binds both the total and a per-tool floor, so an empty mutant list
fails. At the freeze it was the do-nothing control (`fixtures=0`, `survived=23`); it turns green only with
`plans/battery41/`, built in wave 1 under the counter's sandbox contract — run it with `--lane` on a disposable
clone and only inside the host-guard bwrap envelope. `round41-c2` is the round-40 C2 counter's V1–V7 re-pointed
at the `constraints-scheduling` package plus V8, the order gate on `plans/round-41-claims.md` and its receipt; it
needs the entry (`corpus/knowledge/tb2-constraints-scheduling-grader.md`) and the two index rows as well as the
receipt, and its gate leg re-runs the probe, so a full run costs a probe run (≈16 s measured). `constraints-probe`
is a `probe` row of the round-37 `git-webserver-probe` shape: `mismatches=` is a data line and the exit code never
carries prediction disagreement. `round-close-check` gives `plans/round_close.py` the row round-40 closure D2
asked for: its two legs are the round's order gate and the fleet sources census, the census needs `--census PATH`
when the lane is not inside the fleet (a clone under `/fast/scratch` is not), and warnings (W-codes) do not fail
the leg. The `tip-receipts` derived mapping (round 40) is strict: a receipt the `RECEIPTS` table does not name is
re-run byte-for-byte (`kind=byte`) iff its basename, non-alphanumerics dropped and case folded, equals the stem of
exactly one committed top-level `plans/*.py`; `--list` prints `origin=derived` for it and
`skip reason=no-committed-re-run-command` for zero or two matches, so ambiguity fails closed and the table stays
the override list. Measured 2026-10-26 on tip `fc79f2a4`: 3 derived receipts (`round39/git-leak-probe.txt`,
`round40/db-wal-probe.txt`, `round41/constraints-probe.txt`), `compared=7 declared_bounded=1 no_command=19`,
`byte_equal=7 differ=0`; the round-41 receipt reproduces `equal bytes=5775` in ~54 s, and a fixture lane with
`plans/foo_probe.py` beside `plans/foo-probe.py` leaves `corpus/evidence/round99/foo-probe.txt` unmapped while
`bar-probe.txt` resolves.

## Production checklist — running an eval

1. Write ex-ante predictions for every condition before runs — per-task
   *and* aggregate; they calibrate separately. **Make the ordering provable:**
   write the predictions file, `sha256sum` it into a sibling `.sha256`, log
   `date -u +%FT%TZ` before and after into `ordering.log`, stamp every request
   record with `request_ts`, and commit all four (round 9:
   `corpus/evidence/round9-replication/` — hash `2a4f62ef…` at 21:17:48Z,
   first request 21:17:58Z). Score them at close: `|predicted−observed|/n` for
   point forecasts, Brier for probabilities — prefer **per-problem
   probabilities**, because point counts cannot be calibration-scored. Report
   the pre-registered decision rule's verdict even when it is *indeterminate*
   (round 9: INC 4/8 missed its own ≥5/8 survival threshold by one problem).
   **Size the run before requesting it:** derive the planning effect size from
   committed prior bytes (with the derivation command), shrink it for
   selection bias, file a power analysis fixing n and the MDE, and hash it
   with the predictions (round 11: r9 d=0.52 → MDE d=0.35 → n=64, all inside
   the pre-request bundle). **Mock-smoke the runner before the first real
   request** — a stdlib mock server catches runtime defects (`py_compile`
   cannot) without spending a live draw or breaking the ordering window
   (round 11: LabratMock's mock caught a missing `import json`; fix hashed
   into `ordering.log` pre-launch). Carry the serving-stack descriptors
   (model id, KV quant, `--parallel`, template) as an in-band run record so
   every derived claim names its experimental unit (round 11: the
   `descriptors` jsonl record).
2. Probe every endpoint before freeze (`/v1/models`, `/health`); a
   listening-but-wrong service degrades telemetry silently (Jitsi on
   :8080 vs llama on :34113, 2026-09-28).
3. Freeze: prompt text, judge schema, telemetry capture. (Phase 0)
4. Smoke: 2 tasks × 2 conditions = 4 runs against a **mock endpoint first**
   (schema/census/ordering), then the live endpoint. Gate on telemetry
   validity, shape difference, correctness. (Phase 1)
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

Status note (2026-10-15 re-dispatch census — evidence:
`corpus/evidence/round13-coverage/surface-receipt.json`, `observed_at`
`2026-10-15T04:49:50Z`, method `Path.expanduser().exists()` + `urlopen`
`/health` timeout 3 s): every host-absolute `~/…` path and `/proc` entry in
this section is a **dated historical observation**. The receipt found absent:
`~/Projects/webzites/repos/llm-wiki`, `~/archive/bench-arena`,
`~/bench-arena`, `~/.bailian`, `~/Projects/bounties/ledger/telemetry.jsonl`,
`~/.config/systemd/user/qwen-coder.service`,
`~/.config/llama/qwen-coder-godspeed.jinja`, `/proc/1299/cmdline`; and
`http://127.0.0.1:34113/health` refused the connection (ECONNREFUSED).
In-repo pointers (`corpus/knowledge/`, `corpus/evidence/`, `grader.py`)
resolve and carry the retained evidence — a digest is derived evidence, not
the original bytes, and a committed response is run history, not a live
model. Public URLs cited here were not re-fetched by the receipt and are not
claimed current. Current offline entry point for the numbers in this section:
`python3 grader.py` (§Hermetic grader; registry row §Gate/probe registry).
Where to learn next (round 24): `corpus/SOURCES.md` (tiered, opened sources and
study paths); admission bar: `corpus/QUALITY.md`.

- `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/benchmark-shortlist-for-godspeed-research.md` — benchmark shortlist, anti-patterns, minimal stack (read 2026-09-28)
- `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-2.md` — 125 agents / 21 experiments; K2 clean split, calibration asymmetry, variant multiplier, effect-size table
- `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-3-alpha-shittycodex.md` — telemetry fields, Phase 0–3 gates, judging schema, run counts
- `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/gemini-3.1-pro-godspeed-benchmarks.md` — four-signal test suite design (off-path reframe / variant multiplication / discovery widening / calibration asymmetry)
- `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/gemini-3.1-pro-godspeed-test-battery.md` — external benchmark tier, SWE-bench contamination paradox, predictive calibration
- `~/Projects/webzites/repos/llm-wiki/Home.md` — wiki branch/index conventions (read 2026-09-28)
- `~/.bailian/skills/bailian-docs-llm-wiki/models/index.md` + `models/models.jsonl` — 180 families / 413 models structured index; `contextWindow`, `QPM`, pricing, `profile` (oneLinePositioning, scenes, notSuitableFor, familyTier) for model selection (verified 2026-09-28; index generated 2026-09-11; cite path fixed round 11 per box-3 break B1 — `models.jsonl` lives one level deeper; `~/.bailian` **ABSENT 2026-10-15** — index bytes not retained here, so the counts are historical; shape digest: `corpus/knowledge/local-model-index.md`)
- `find`/`grep` output of the 2026-09-28 session — `~/wikillm/llm-wiki` absent then and still; wiki resolved at `~/Projects/webzites/repos/llm-wiki` — that path itself **ABSENT 2026-10-15** (receipt path 1)
- `~/Projects/bounties/ledger/telemetry.jsonl` — lane-routing corpus (live when profiled), 7,218 events; taxonomy + reroute signatures in `corpus/knowledge/ledger-route-telemetry.md` (profiled 2026-09-28). **Path ABSENT as of round 11** (resolved at 23:32Z mid-round — aggregator box-3 cold run counted 7,226 live lines — and was gone minutes later; whole `~/Projects/bounties/` tree absent, no relocation found): counts are historical, routed to kasegi in `PROVINCE.md` round-11 report-outs; absence reconfirmed by the 2026-10-15 receipt (path 5)
- `~/archive/bench-arena/` (relocated intact from `~/bench-arena/` in round 14; `tasks/`, `report-grok45.csv`, `report-qwenlocal-v2.v2.csv`, `telemetry-qwenlocal-v2.csv` — frozen round-14 inventory; **both paths ABSENT 2026-10-15**, receipt paths 2–3) — executed 33-task two-model battery; results in `corpus/knowledge/local-bench-arena.md` (analyzed 2026-09-28)
- `~/Projects/webzites/repos/llm-wiki/wiki/karpathy/**` + `wiki/ai/{foundations/bitter-lesson,alignment-and-training/rlhf}.md` — eval-first thesis, diversity blindness, TrueSkill judge/aggregator split, RLHF proxy mechanics (digested 2026-09-28 → `corpus/knowledge/eval-theory-notes.md`)
- `https://huggingface.co/api/models`, `https://openrouter.ai/api/v1/models` — live catalog schemas (probed 2026-09-28 → `corpus/knowledge/open-model-catalogs.md`)
- `127.0.0.1:34113` llama-server (historical identity — endpoint refuses connections since 2026-10-15) + `~/archive/bench-arena/grade.sh` (ABSENT 2026-10-15) — authored 4-task slice, 1/4 PASS vs predicted 2/4, `03` flip PASS→FAIL (run + graded 2026-09-28, frozen result → `corpus/knowledge/bench-arena-fresh-run.md`)
- `/tmp/bench-r7/` scaffold-delta ablation (ephemeral workdir, labelled debt per `../PROTOCOL.md`'s closure-resolvable rule — decisive numbers pasted into the knowledge entry) — verbatim opencode `raw` wire request captured via proxy provider, 5-task × 5-condition ablation (E1/E2/E3/E4 × n=3 + E0 anchor), graded 2026-09-28 → `corpus/knowledge/bench-arena-round7-scaffold-ablation.md`
- `~/archive/bench-arena/` round-5 battery (then located at `~/bench-arena/`) — full 33-task direct-API re-run: 20/33 PASS, 8 status deltas vs v2 (4 P→F, 3 F→P, 1 F→HARNESS_DEFECT), 5 byte-identical sol_sha, 06 truncation (`finish=length` @4096 tok), FAIL slower on wall+tokens (run + graded 2026-09-28 → `corpus/knowledge/bench-arena-round5-battery.md`)
- `~/Projects/webzites/repos/llm-wiki/wiki/karpathy/{talks,projects-and-tools,standards-and-specifications}/**` + remaining `philosophy-and-concepts/`, `gwern-essays/`, `ai/foundations/complexity.md`, `ai/books/` — second digest: sampling-proves-presence, reference-class, autonomy slider, spec-ability tiers (swept+read 2026-09-28 → `corpus/knowledge/eval-design-digest-2.md`)
- `corpus/evidence/round8-horizon/` — round-8 planning-horizon probe, run to completion 78/78 jobs: `horizon.py` (349 lines, md5 `1c157e2a…`), `results.jsonl` (268 records, md5 `df154cb5…`, `raw` restored round 9), `run.log` (SUMMARY block, md5 `fc3b232f…`), `critic-defects.md` (16 design defects) — analyzed 2026-09-28 → `corpus/knowledge/bench-arena-round8-horizon.md`
- `corpus/evidence/round9-replication/` — pre-registered probe-A replication + checkpoint-dose cell: `predictions-r9.md` (sha256 `2a4f62ef…`, hashed before the first request), `ordering.log`, `run_r9.py`, `results-r9.jsonl` (284 records: 8 meta / 248 scored / 28 filler), `replication.md` — run + scored 2026-09-28 → `corpus/knowledge/bench-arena-round9-replication.md`
- `corpus/evidence/round9-fleet/` — ten L2 artifacts behind round 9's claims: `probeA.md`/`probeB.md`/`probeC.md` (+ their scripts), `critic.md` (16-defect fix-landing audit, claim triage), `harness-mutation.md` + `test_harness.py` (50 cases, exit 0), `prior-art.md`, `sibling-overlap.md`, `review.md` (citation/state audit)
- Public prior art fetched 2026-09-28 for novelty calibration → `corpus/knowledge/eval-prior-art-calibration.md`: `arxiv.org/abs/2505.06120` (Laban et al., *LLMs Get Lost In Multi-Turn Conversation*, ICLR 2026), `2310.01798` (Huang et al., self-correction), `2307.13702` (Lanham et al., CoT faithfulness), `2309.06275` (Re²), `2210.01296` (RECITE), `2209.11895` (induction heads), `2305.18654` (Faith and Fate), `2205.10625` (least-to-most), `2310.20410` (FollowBench), `2410.15553` (Multi-IF), `2501.17399` (MultiChallenge), `2507.05257` (MemoryAgentBench), `2406.10149` (BABILong), `2406.12045` (τ-bench `pass^k`), `2504.04823` + `2409.11055` + `aclanthology.org/2025.emnlp-main.479` (quantization bands), `github.com/ggml-org/llama.cpp/issues/7052` (multi-slot non-determinism — the public antecedent of this lane's non-iid finding), `docs.vllm.ai/en/latest/features/batch_invariance/`, `thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/`
- `corpus/evidence/round11-power/` — powered preregistered emission-granularity rerun (n=64, pids 201–264, seeds `3000+pid*41`): `probe_plan_r11.md` + `power_analysis_r11.md` + `predictions-r11.md` (bundle sha256 hashed 23:10:20Z, `ordering.log`), `probe_r11.py` (= `replicate.py` copy) + `run_r11.py`, `results-r11.jsonl` (1473 records, md5 `c42fe3d1…`), `run.log` (md5 `281cb530…`), generated `analysis_r11.md` (md5 `14663359…`), `recompute_r11.py` — severity dose **ESTABLISHED** (paired +0.352, p=0.0011) 2026-09-28 → `corpus/knowledge/bench-arena-round11-power.md`
- `corpus/evidence/round11-fleet/` — twelve L2 artifacts behind round 11: `r11-critic-design.md` (0 FATAL design gate), `r11-prior-art-{granularity,prereg}.md` (C1–C4 + M1–M3 fetched-URL verdicts), `r11-connector.md`, `r11-review-baseline.md` (BASELINE GREEN), `r11-mock-smoke.md` + `mock_server_r11.py` (caught the runner's missing `import json`), `grader_r11_draft.py` + `recompute_r11_draft.py`, `r11-{critic-landed,mutation,review-index}.md` (wave 2), `INTEGRATOR-NOTES.md`
- Public prior art fetched 2026-09-28 for round-11 novelty/method pricing → `corpus/evidence/round11-fleet/r11-prior-art-{granularity,prereg}.md`: `arxiv.org/abs/2411.00640` (Miller, *Adding Error Bars to Evals* — paired inference, power), `2503.01747` (Bowyer et al., CLT CI under-coverage at small n), `2606.11217` + `2603.10044` (agent-experiment preregistration template + at-scale execution), `2609.08589` (StageIF layered reporting-failure scoring), `2605.30233` (last-token state aggregation), `github.com/ggml-org/llama.cpp/issues/7052` (closed-stale; multi-slot non-determinism class unfixed) + PR #21038 (q4_0-KV PPL/KLD perturbation tables)

## Task-spec/scorer observability — round28

For a pinned benchmark, separate authored task intent, consumed scorer predicates and unverified
runtime state. `corpus/knowledge/webarena-task-spec-audit.md` records the source-anchored decision table.
Run `python3 plans/benchmark_spec_audit.py --summary` (`--json` preserves raw per-task data).
Exit0 certifies only the declared pinned schema inventory; it is not task validity, model accuracy
or contamination freedom. Preserve evaluator order, distinguish raw/effective defaults, and treat
helper/hosted-judge outcomes as unverified. Current source: dce04686, not an interchangeable release.

For inward source-reference calibration run `python3 plans/registry_check.py --summary`:13 frozen
source rows over35 baseline knowledge paths. Literal corrective mentions count; used-by is not
endorsement of every source sentence. New files/rows stay outside that diagnostic. QUALITY Q17 and
the round28 lesson name its red/green evidence and limits; whole-registry census remains separate.

Round28 historical-state scope correction: the P4a round26 revision parser ends at the next H2;
later rounds' score prose cannot change a frozen offline disclosure. `python3 plans/state_check.py
--selftest` includes the later-round-score witness. This repairs extraction scope only: P4 retains
two offline groups and one superseded ID, never a whole-current-tree assertion guarantee.

## Generated-config projection — round29

Before interpreting a WebArena run that consumes `generate_test_data.py` output by file index, run
`python3 plans/config_projection.py --summary`: it projects the pinned raw specs by the generator's six
ordered serialized-text replacements under three synthetic profiles. Exit0 means 812 tasks parse with zero
remaining tokens and every changed leaf carries a token; it is not a deployment config, task validity or
scoring result. Global replacement reaches non-URL fields (61 leaves); frozen data cannot reveal order or
positional naming, so rely on the selftest's witnesses and `plans/fixtures/r29/mutation_witness.py`.
`corpus/knowledge/webarena-config-projection.md` holds the decision rule; ID-selecting harnesses (S074)
need no filename check.

## TB2 regex-log grader — round36

Before citing the pinned TB2 `regex-log` scorer, run `python3 plans/regex_log_probe.py --lane .`: exit `0`
means all 24 frozen predictions matched, `1` a mismatch, `2` the capture no longer hashes to `345c3bd0…`
(TB2 `2fd12b8`, rows S108–S110). The grader compiles `/app/regex.txt` and applies `re.findall(…,
re.MULTILINE)` to one fixed 25-line log, asserting exact equality with nine dates
(`corpus/evidence/round36/tb2-regex-log/test_outputs.py:34-90`); the receipt's summary line
(`corpus/evidence/round36/regex-log-probe.txt:26`) reads `cases=24 observed_pass=8 observed_fail=16
mismatches=0`, and `--dry` prints predictions without running anything, so it is not evidence.

Observed enforcement is narrower than the instruction. Enforced: last date per line (`:4`), a valid IPv4
anywhere in the line (`:17`), octets 0-255 (`:6`), months 01-12 (`:8-9`), days 01-31 (`:10-11`),
letter-adjacency on both date and IP (`:12-13,15-16`), and the file/compile/findall mechanics including an
extra capture group (`:20-23`) and a padded pattern file (`:24`). Not enforced: a literal alternation of
the nine expected dates passes with no pattern logic (`:18`); leading-zero octets pass though the
instruction forbids them (`:7`, `instruction.md:4`); digit-adjacent dates — the instruction's own
`1134-12-1234` example — are unobserved, so a letters-only boundary passes (`:14`, `instruction.md:6`);
year widths other than four are unobserved (`:19`); month-length validity is unobserved because the
Feb 30 and Apr 31 lines sit on invalid-IP lines (`:2`, `test_outputs.py:65,67`); and a regex that rejects
Feb 29 still passes, so the instruction's permission (`instruction.md:3`) is untested (`:25`).

What to do: when interpreting a reported pass, check which instruction bullets this fixture can decide, and treat a green fixed log as evidence about that log
only — never as evidence of instruction compliance. `test.sh:26-28` writes reward 1/0 from pytest's exit
alone, so a green fixed log cannot distinguish a stated-rule regex from a literal alternation of the expected values (a property of `regex-log` at `2fd12b88`, not a task-validity or agent-behaviour verdict).

## Service-class TB2 grader — round 37

Before citing the pinned TB2 `configure-git-webserver` scorer, run `python3 plans/git_webserver_probe.py
--lane .` and read its summary line, not its exit code: exit `0` means only that every case produced one
verdict (`plans/git_webserver_probe.py:303-304`), exit `1` is reserved for `--smoke`, exit `2` for setup.
The receipt's summary (`corpus/evidence/round37/git-webserver-probe.txt:49`) reads `cases=22
observed_pass=9 observed_fail=13 mismatches=0`, and `--dry` prints predictions without a sandbox, so it is
not evidence. The class differs from rounds 35–36: the pytest verdict is a substring of a helper script's
stdout (`corpus/evidence/round37/tb2-git-webserver/test_outputs.py:13`), and the helper probes a live
service the probe starts; the capture does not show what state the task's run leaves.

### Decision table — when the verdict is a substring of a helper's stdout

| what the verdict actually depends on | what the frozen run tested | what the frozen run showed | cite |
|---|---|---|---|
| the helper echoes untrusted content before it decides | a body equal to the verdict token was served | `token-in-body`: `observed=pass` although `❌ TEST FAILED` was printed | `test_outputs.py:13`; `verify.sh:62`; receipt:35 |
| the helper's exit status is never read | a case ran with the required tool absent from PATH | `static-file-no-git`: `observed=pass` with no repository, hook or push | `verify.sh:5-6,49`; `test_outputs.py:11`; receipt:7 |
| one verdict is assembled from two HTTP requests | the status request was answered `200`; the content request supplied the body | `status-then-content-split`: `observed=pass`; the first body `not the content` is never compared | `verify.sh:57,60`; receipt:37 |
| `curl` runs with no `-L` and no timeout | a 301 to the right body; a 3 s delay before the right body | `redirect-301`: `observed=fail`; `slow-server-3s`: `observed=pass` | `verify.sh:57` (and `:75` for `wget`); receipt:29,41 |
| the compare is exact after command substitution | trailing newlines; CR, BOM, a leading space, `Hello World` | trailing newlines stripped: `observed=pass`; the other four `observed=fail` | `verify.sh:63`; receipt:11,13,15,19,21 |
| any path is served | a server answered every path with the same body | `catch-all-200`: `observed=pass` | `verify.sh:57,60`; receipt:31 |
| the instructed port is tested at all | the server listened on `:8081` and 8080 was empty | `wrong-port-8081`: `observed=fail` | `instruction.md:7`; receipt:33 |

### Sandboxing it (each item is required, not stylistic)

- Private network namespace: `verify.sh:57` asks `localhost:8080`, so without `--unshare-net` the probe
  reads whatever the host serves. The probe uses `--unshare-net --unshare-pid --unshare-ipc`
  (`plans/git_webserver_probe.py:204`).
- Scratch `HOME`: `verify.sh:9-13` writes `~/.ssh/config`; an unsandboxed run edits the operator's home
  (`plans/git_webserver_probe.py:11,235`).
- `/tests` bound read-only to the captures: `test_outputs.py:11` invokes the absolute `/tests/verify.sh`.
- Writable, disposable cwd: `verify.sh:16` writes `git_test.exp` into the current directory.
- A `PATH` holding only the tools the case names: `verify.sh:55` branches on `command -v curl`, so the
  runner decides which of the two compare paths executes.
- `apt-get` and `expect` absent, as in any container where they fail: `verify.sh:5-6` and `:49` then fail
  observably and silently; nothing in the script reads their status.

What a green means here: in the probe's state, the service answered two requests and the content
body equalled `hello world` after command substitution. What it does not mean: that a git server, a
clone, a commit or a push happened (`static-file-no-git`, receipt:7), that the body is exactly the file the
instruction asked to publish (`status-then-content-split`, receipt:37), or that a success message the
helper printed is the thing being read (`token-in-body`, receipt:35). Treat a reported pass as a statement about
two HTTP responses, never as evidence of instruction compliance (`instruction.md:1-9`).

Limits named at freeze: the probe never executes the oracle and no case performs a real git push, because
`expect` and `apt-get` are absent (`plans/git_webserver_probe.py:21-23`); the probe shows what the verdict
depends on, never that the intended path passes.

A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not solver
advice, and not a statement about any agent's behaviour. Case-independence limits (`wrong-port-8081` reads as
`no-server`; the git step never executes in the sandbox; two body echoes at `verify.sh:62,68`) are recorded in
`corpus/knowledge/tb2-git-webserver-grader.md` §What the probe does not show.

## Build-provenance TB2 grader — round 38

Before citing the pinned TB2 `build-pmars` scorer, run `python3 plans/build_pmars_probe.py --lane .` and read
its summary line: exit `0` means only that all 22 cases produced four verdicts each, exit `2` a setup failure
(capture digest, `bwrap` or `gcc` missing, a case that did not return four verdicts)
(`plans/build_pmars_probe.py:301-306,328-333`). The receipt's summary
(`corpus/evidence/round38/build-pmars-probe.txt:26`) reads `cases=22 observed_pass=7 observed_fail=15
mismatches=0`, and `--dry` prints predictions against the frozen table without staging anything, so it is not
evidence. The class differs from rounds 35–37: the graded state is a compiled binary plus a source tree, and the
whole score is four assertions over file existence, `ldd` stdout, `glob()` results and program stdout
(`corpus/evidence/round38/tb2-build-pmars/test_outputs.py:23-85`); the probe imports that module and calls the
four functions directly in a per-case bubblewrap sandbox (`plans/build_pmars_probe.py:239-272`), so
`tests/test.sh`'s `uvx`/pytest path and its reward write (`test.sh:18-28`) are read, not run.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| `Path("/usr/local/bin/pmars").exists()`, then the program's own stdout for two debugger runs and one battle (`test_outputs.py:23-46`) | a canned 21-line C program printing two 5-digit address lines and one `Results:` line, with `debian/` an empty directory and `src/dummy.c` zero bytes — `canned-shape` observed `pass`, all four tests | that a binary exists *because a build ran*: rebuild from the staged tree and compare `sha256sum` of the artefact; existence plus plausible stdout is not provenance | `canned-shape` (receipt:5); `plans/build_pmars_probe.py:151-172` |
| `exists()` only — no execute bit, no real invocation of the installed file (`:24`, `:53`) | nothing passes, but the install assertion is satisfied by a file the shell cannot run (`nonexec-binary`, `test_pmars_works:error=CalledProcessError`) and by one that prints nothing (`silent-binary`) | `test -x` plus one direct absolute-path invocation; the grader cannot tell "installed" from "planted" | `nonexec-binary` (receipt:17), `silent-binary` (receipt:18) |
| `subprocess.check_output` returns `e.output` when it is non-empty (`:12-15`) | a program that exits 3 after printing correct stdout — `canned-exit-nonzero` observed `pass` | read the process exit status yourself when a failing build must be red; the grader swallows any non-zero exit that printed anything | `canned-exit-nonzero` (receipt:16) |
| the three behaviour commands run bare `pmars` (PATH-resolved) while `ldd` runs the absolute path (`:27-28,44,53`) | a script at `/usr/local/sbin/pmars`, earlier in `PATH`, answers the behaviour checks while `/usr/local/bin/pmars` stays silent — `path-split` observed `pass` | invoke the absolute installed path everywhere, or check `command -v pmars`; two programs can be graded as one | `path-split` (receipt:19) |
| a substring scan of `ldd` stdout for `libX11 libXt libXext libXaw` (`:53-57`) | a program that `dlopen()`s `libX11.so.6` at run time — no `DT_NEEDED` entry for `ldd` to print — `canned-x11-dlopen` observed `pass`; the same program linked with `-lX11` fails (`canned-x11-linked`) | `readelf -d` `DT_NEEDED`, plus the binary's own `dlopen` strings or an `LD_DEBUG=libs` run; `ldd` text is a link-time view only | `canned-x11-dlopen` (receipt:9), `canned-x11-linked` (receipt:8) |
| `ldd` must print something: a script is "not a dynamic executable" on stderr, a `-static` binary makes `ldd` exit 1 with empty stdout (`:12-15,53`) | nothing — `canned-script` and `canned-static` both fail, but only the X11 test does | that a static or scripted build may be a legitimate headless answer and is red here for a different reason than X11 linkage; do not read these fails as "X11 present" | `canned-script` (receipt:6), `canned-static` (receipt:7) |
| `re.match(r"Results: \d+ \d+ \d+", tail -n 1)` — prefix anchor, two-character separators (`:43-46`) | `Results: 12 34 78 forged` observed `pass`; two integers (`results-two-ints`) and a negative integer (`results-negative`) fail | compare the whole expected line (`fullmatch` or equality after `strip`); the integer count and the sign are enforced, trailing garbage is not | `results-trailing-text` (receipt:11), `results-two-ints` (receipt:10), `results-negative` (receipt:13) |
| `tail -n 1` of the battle command (`:44`) | the `Results:` line must be last: a following line fails (`results-not-last`) | that the grader's "output" is one line of a longer transcript; a program printing warnings after the result is red | `results-not-last` (receipt:12) |
| `re.findall(r"\b(\d{5})\s+\w+\.\w+", stdout)` with `len >= 2` on each of two runs (`:31-39`) | nothing — one address line fails (`one-address`) and four-digit addresses fail (`four-digit-address`) | that address width and step count are properties of this pMARS build's debugger format, not of "the debugger works"; a real build with a different format is red | `one-address` (receipt:14), `four-digit-address` (receipt:15) |
| `Path("/app").glob("pmars-*")`, first match only, one level deep (`:62,75`) | nothing extra passes, but a tree at `/app/src/pmars-0.9.4` fails both source tests (`pmars-dir-elsewhere`) | that extraction depth is an instruction-shaped requirement, not a build defect; check the tree the instruction actually named | `pmars-dir-elsewhere` (receipt:25) |
| `(source_dirs[0] / "debian").exists()` (`:69-70`) | `debian` as a zero-byte regular file observed `pass` (`debian-is-file`); no `debian/` fails (`no-debian-dir`) | that `debian/control`, `debian/rules` and the package metadata exist as a directory; `exists()` accepts a file | `debian-is-file` (receipt:21), `no-debian-dir` (receipt:20) |
| `list((source_dirs[0] / "src").glob("*.c"))` non-empty (`:82-85`) | a directory named `src/sim.c` counts as C source — `c-is-dir` observed `pass`; a header-only `src/` (`src-no-c`) and a missing `src/` (`no-src-dir`) fail | count regular files and read the Makefile's source list; the glob returns directories too | `c-is-dir` (receipt:23), `src-no-c` (receipt:22), `no-src-dir` (receipt:24) |
| nothing — do-nothing baseline, empty `/app`, no binary | nothing: `empty-tree` fails all four, the first failure being `test_headless_no_x11:error=CalledProcessError` | run the baseline first: it shows which tests carry the score and that an absent binary errors rather than asserts | `empty-tree` (receipt:4) |

What a green means here: in the probe's staged state, a dynamically linked program at
`/usr/local/bin/pmars` printed two 5-digit address lines and a `Results:` line, `ldd` did not print four
library names, `/app/pmars-*` held a `debian` entry and a non-empty `src/*.c` glob — and nothing was built.
What it does not mean: that pMARS came from Debian source, that X11 is absent, that the `Results:` line is
well formed, or that the debugger works in any sense beyond the two regexes. Of the seven instruction tags the
probe maps (`from-source`, `no-x11`, `debian-source`, `extract-to-app`, `install-path`, `results-format`,
`debugger-works` — `plans/build_pmars_probe.py:66-75`), each has at least one
state that violates it and is still observed `pass`, so no instruction line is `enforced` by this grader
alone; the entry's §Requirement map carries the derived labels.

Limits named at freeze: the probe never runs the oracle (`solve.sh` is captured, not executed), the task image
(`task.toml:29` names it, `allow_internet = true` at `:34`) or Terminal-Bench; host `gcc` compiles the canned
artefacts, host bash stands in for the image's shell, and host glibc/`ldd` stand in for the image's. Each case
stages its own `/app` and `/usr/local/{,s}bin`, so no case observes the image's tree or a network build
(`plans/build_pmars_probe.py:239-252`). `tests/test.sh`'s pytest/`uvx` path and reward file are read, not run.

A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not solver
advice, and not a statement about any agent's behaviour.

## Repository-history TB2 grader — round 39


Before citing the pinned TB2 `git-leak-recovery` scorer, run `python3 plans/git_leak_probe.py --lane .` and read
its summary line: exit `0` means only that all 25 cases produced five test verdicts each, exit `2` a setup
failure (a capture not at its pinned digest, `/usr/bin/bwrap` or `/usr/bin/git` not executable, a case that did
not return five verdicts) (`plans/git_leak_probe.py:226-301`). `--stage-check` builds each case's repository
state and prints only stage exit codes (the grader module is never imported), and `--dry` prints predictions
without a sandbox, so neither is evidence. The receipt's summary
(`corpus/evidence/round39/git-leak-probe.txt:30`) reads `cases=25 observed_pass=13 observed_fail=12
mismatches=0`, and a second run is byte-equal. The class differs from rounds 35–38: the graded state is a git
repository's object store and refs plus one flag file at `/app/secret.txt`, and the whole score is five
assertions over that state (`corpus/evidence/round39/tb2-git-leak-recovery/test_outputs.py:11-113`); the probe
runs the task's own `challenge-setup.sh` first, then a frozen recipe, then imports the module and calls the five
functions in file order inside a per-case bubblewrap sandbox (`plans/git_leak_probe.py:1-35`), so
`tests/test.sh`'s `uvx`/pytest path and its reward write (`test.sh:18-28`) are read, not run.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| `Path("/app/secret.txt").exists()`, then `read_text().strip() == "secret[lost_and_found_in_git]"` (`test_outputs.py:11-17`) | any end state that writes that exact literal at that path — including states whose repository still leaks: `echo-only` and `echo-gc-only` are PPPPP | that the assertion checks path and value only, never provenance: the value must come from somewhere, and `instruction.md` gives the *format* only (`secret[...]`), so a state that plants the literal satisfies test 1 with no recovery | `echo-only` (receipt:8), `echo-gc-only` (receipt:10) |
| `.strip()` before the equality (`:15`) | leading spaces and a CRLF are forgiven — `flag-padded-crlf` is PPPPP | byte equality when whitespace is part of the value; `strip()` also removes a trailing newline the instruction never promised | `flag-padded-crlf` (receipt:27) |
| the equality covers the **whole** line (`:16`) | nothing extra: `flag-extra-text` is FPPPP | whether a labelled answer is a legitimate reading of "write it to a /app/secret.txt file"; this grader says no | `flag-extra-text` (receipt:26) |
| `exists()` is true for a directory, and `read_text()` then raises (`:14-15`) | nothing — `flag-is-directory` is FPPPP and the receipt names `test_flag_file_exists_and_correct:error=IsADirectoryError` | that this is an exception, not an assertion: only the receipt names the class, so wire the case, not the exit code | `flag-is-directory` (receipt:28) |
| the literal's **location** (`:14`) | `flag-in-repo-only` (literal written inside the repo work tree) is FPPPF — test 1 fails and the checksum moves | where the instruction says the flag file lives; a correct literal in the wrong directory is red for two different reasons | `flag-in-repo-only` (receipt:29) |
| `git log --all --grep 'secret\[' --regexp-ignore-case` over commit messages (`:19-38`) | a ref pinning a *blob* (`blob-ref-keeps-secret`), an annotated tag message (`tag-message-secret`) and the secret in `.git/config` (`config-secret`) are all PPPPP — none of them is a commit message | enumerate the refs the initial state leaves behind (`for-each-ref`) and grep the tag/stash/config holders yourself; a non-commit holder is outside this assertion | `blob-ref-keeps-secret` (receipt:15), `tag-message-secret` (receipt:16), `config-secret` (receipt:22) |
| the same grep, on any commit reachable from any ref (`:19-38`) | nothing for these — `branch-keeps-leak`, `commit-message-secret` and `notes-secret` are PFPPP | that `refs/notes/commits` is under `--all` and so counted as commit history; whether a note is "a commit message" is the author's call, not the grader's | `branch-keeps-leak` (receipt:14), `commit-message-secret` (receipt:17), `notes-secret` (receipt:18) |
| `git log --all -p -S secret[` over reachable content (`:39-49`) | `echo-only`, `echo-reflog-expire` and `echo-gc-only` are PPPPP — the reflog is not a ref for `--all`; `stash-secret` is PPPPP because `refs/stash` is a merge and `-S` without `-m` does not diff merges (the receipt's own static reading, marked uncertain there) | `git log --all --reflog -p -S` (or `git rev-list --reflog --objects`) when "gone" must mean absent from what git can still restore | `echo-only` (receipt:8), `echo-reflog-expire` (receipt:9), `stash-secret` (receipt:19) |
| `git fsck --lost-found`, then `cat-file -p` on every line containing `dangling`, asserting `secret[` is absent (`:66-92`) | only a dangling blob (`dangling-secret-blob`, PPPFP) or a dangling commit whose message carries the secret (`dangling-secret-commit`, PPPFP) is caught; `echo-reflog-expire` is PPPPP because a dangling commit's `cat-file -p` prints a commit header and tree hash, not file content | the object store directly — `git cat-file --batch-all-objects --batch-check` plus a byte search — if every leftover object must be shown clean; this loop reads five top-level texts | `dangling-secret-blob` (receipt:12), `dangling-secret-commit` (receipt:13), `echo-reflog-expire` (receipt:9) |
| `git log --oneline --all` must contain the substring `chore: init e665d1a2-…` (`:51-64`) | `message-rewritten` is PPPPP (the setup commits that message twice, `challenge-setup.sh:12,22`, so rewriting the tip leaves the substring) and `history-rebuilt` is PPPPP (one rebuilt init commit) | set equality: compare `git log --format=%s --all` before and after; "commit messages remain untouched" is asserted as one substring of one line | `message-rewritten` (receipt:24), `history-rebuilt` (receipt:25) |
| a work-tree checksum: `find /app/repo -type f -not -path '*/\.*' -exec sha256sum {} + \| sort \| sha256sum`, compared with `expected in output` (`:95-113`) | `dotfile-in-worktree` PPPPP (dot paths skipped) and `config-secret` PPPPP (`.git/config` is a dot path); `readme-edited` and `untracked-file-secret` are PPPPF | run the same `find` **without** the dot-path exclusion, and hash `.git` too if repository state must be shown unchanged: one digest over non-dot files cannot localise a change and never reads the object store | `dotfile-in-worktree` (receipt:20), `readme-edited` (receipt:23), `untracked-file-secret` (receipt:21) |
| nothing — do-nothing baselines and the task's own oracle | `empty-app` (no repo, no flag) is FFFFF; `untouched` (the setup's own end state) is FPPPP — only test 1 fails; `oracle-solve-sh` is PPPPP | run all three first: `untouched` shows that four of five tests already pass before any work, and the oracle's pass shows the intended path clears them | `empty-app` (receipt:5), `untouched` (receipt:6), `oracle-solve-sh` (receipt:7) |

What a green means here: in the probe's staged state, `/app/secret.txt` held exactly the literal, two `git log
--all` greps printed nothing, `--oneline` carried the init message, `fsck`'s `dangling` lines held no `secret[`,
and the non-dot work-tree checksum matched — on states the probe built, not states an agent built. What it does
not mean: that the secret is gone from the repository (a reflog-reachable commit, a blob pinned by a non-branch
ref, a tag message, a stash and `.git/config` all survive as PASS), that the work tree is unchanged at dot
paths, that the object store is clean beyond five `cat-file` reads, that history is the history the task
started with, or that the literal is *the* secret rather than a value the probe's recipe planted (the assertion
reads one path and one value; `instruction.md` states the format only).

Of the four frozen instruction tags (`plans/git_leak_probe.py` `TAGS`, frozen lines in
`corpus/evidence/round39/git-leak-dry-cases-freeze.txt:1-4`), the round-39 counter's V7 rule (label = the
observed verdicts of every receipt case whose `violates=` carries the tag) gives: `recover-secret`
(`instruction.md:3`) `enforced`, `secret-gone` (`:4`) `partly`, `files-untouched` (`:5`) `enforced`,
`messages-untouched` (`:5`) `partly`. `enforced` here is a property of the frozen case set only: one of the two
`files-untouched` witnesses is the empty-`/app` baseline (`receipt:5`), so the label means "every frozen case
that violates it is observed fail", not "no improving agent can violate it". The entry's `## Requirement map`
carries one row per tag in the counter's row shape, and V7 re-derives all four labels from the receipt.

Limits named at freeze: the probe never runs Terminal-Bench, the task image (`task.toml:30` names it;
`Dockerfile:3` builds it on `ubuntu:24.04`) or a harness; `tests/test.sh`'s pytest/`uvx` path and its
`/logs/verifier/reward.txt` write are read, not run. The task's own `solve.sh` **is** executed, as the single
`oracle-solve-sh` case (`receipt:7`), and observed pass; its mechanism is not printed — that it found a dangling
commit is inferred from `solve.sh:11-24`, which writes the literal only inside that branch. Host git 2.56.0 and
host bash stand in for the image's Ubuntu 24.04 git and dash (the checksum runs `sh -c`), the setup script runs
unprivileged rather than as root, `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null` keep host git
configuration out of a case, and commit object ids differ per run and are never printed
(`plans/git_leak_probe.py:1-35`). Each case stages its own `/app` and `/cap`, so no case observes the image's
tree.

A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not solver
advice, not a statement about git's storage semantics or about any agent's behaviour.

## Database-recovery TB2 grader — round 40

Before citing the pinned TB2 `db-wal-recovery` scorer, run `python3 plans/db_wal_probe.py --lane .` and read its
summary line: exit `0` means only that all 28 cases produced seven test verdicts twice each, exit `2` a setup
failure (a capture not at its pinned digest, `/usr/bin/bwrap` not executable, a `--work` directory that cannot be
created, a case that did not yield seven verdicts twice, or a recipe that exited non-zero — a recipe error is never
a verdict) (`plans/db_wal_probe.py:1-20,314-364`). `--dry` prints the frozen case table with no sandbox and
`--stage-check` builds each case's end state and prints only stage exit codes, the grader never imported
(`plans/db_wal_probe.py:3-10`), so neither is evidence. The receipt's summary
(`corpus/evidence/round40/db-wal-probe.txt:35`) reads `cases=28 observed_pass=8 observed_fail=20 mismatches=0`,
and a second, same-process call of the seven functions on each un-rebuilt end state agrees case by case
(`regrade cases=28 differ=0`, `:34`) — a determinism read of the probe, not re-run stability (entry §Regrade).
The class differs from rounds 35–39: the graded state is one JSON export at `/app/recovered.json` whose source of
truth is a binary database file pair — `main.db` plus an XOR-encrypted `main.db-wal` — and the whole score is seven
pytest functions over that export (`corpus/evidence/round40/tb2-db-wal-recovery/test_outputs.py:7-107`); the probe
seeds `/app` as the task Dockerfile does (`Dockerfile:14-15`), runs a frozen recipe under `bash -euo pipefail`,
then imports the captured module and calls the seven functions in file order inside a per-case bubblewrap sandbox
(`plans/db_wal_probe.py:10-20`), so `tests/test.sh`'s `uvx`/pytest path and its `/logs/verifier/reward.txt` write
(`test.sh:18-29`) are read, not run.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| `os.path.exists("/app/recovered.json")` and nothing else (`test_outputs.py:7-9`) | any file at that path, including one that is not JSON: `truth-trailing-garbage` passes test 1 and fails the other six (`PFFFFFF`) | parse the file before crediting it; test 1 is a path test, not a recovery test | `truth-trailing-garbage` (receipt:26) |
| `json.load` of the whole file plus `isinstance(data, list)` and `len(data) > 0` (`:12-18`) | a list of any content — `empty-list` clears tests 1, 3, 4 and 6 (`PFPPFPF`) | that "valid JSON" means one parse of one file; a JSON object raises `TypeError` in tests 4 and 6 instead of asserting (`truth-wrapped-object`, `PFFFFFF`) | `empty-list` (receipt:28), `truth-wrapped-object` (receipt:23) |
| `required_fields.issubset(item.keys())` over `{"id","name","value"}` (`:27-32`) | extra keys are free: `truth-extra-field` adds a `note` to every record and passes 7/7 | the exact key set, when the instruction's `[{"id":…,"name":…,"value":…}]` line is meant as the format | `truth-extra-field` (receipt:22) |
| `isinstance(item["id"], int)`, `["value"], int`, `["name"], str` (`:33-35`) | `True` passes as an int (`truth-bool-value-id5`, 7/7); floats fail only here (`truth-value-float-id1` and `truth-ids-as-floats` are `PPFPPPP`, because `1.0 == 1` still clears tests 4-6) | `type(x) is int` and `not isinstance(x, bool)` if the export must be machine-readable, not merely JSON-shaped | `truth-bool-value-id5` (receipt:31), `truth-value-float-id1` (receipt:18), `truth-ids-as-floats` (receipt:25) |
| `ids == sorted(ids)` (`:43-44`) | monotone ids of any length and with duplicates: `empty-list` passes it (`PFPPFPF`), as do `truth-plus-duplicate-id11` and `truth-dup-id10-no-id11` (`PPPPFFP`) | set equality against `1..11`; sortedness is neither completeness nor uniqueness | `truth-reversed-order` (receipt:19), `truth-plus-duplicate-id11` (receipt:20) |
| `len(data) == 11` then `ids == list(range(1, 12))` (`:53-58`) | eleven ids in order, and nothing about where they came from: `literals-never-open-db` types them by hand and is 7/7 | open the database yourself; an eleven-id list is not evidence of a WAL read | `literals-never-open-db` (receipt:15), `truth-drop-id11` (receipt:29), `empty-list` (receipt:28) |
| `len(ids) == len(set(ids))` (`:83-89`) | nothing extra — it cannot fail alone, since both duplicate states already fail the count and id-equality assertions (`PPPPFFP`) | that this assertion is redundant: "no duplicate ids" is enforced only through test 5's count and id list | `truth-plus-duplicate-id11` (receipt:20), `truth-dup-id10-no-id11` (receipt:21) |
| `id_to_item[1]["value"] == 150` and `id_to_item[2]["value"] == 250` (`:64-67`) | 2 of the 33 id/name/value cells: values of ids 3-11 are never read — `truth-value-id3-wrong` writes `301` for id 3 and passes 7/7 | compare the whole exported table with the decrypted rows, not the two cells the grader sampled | `truth-value-id3-wrong` (receipt:30), `literals-never-open-db` (receipt:15) |
| `id_to_item[3..11]["name"] == cherry…mango` (`:70-80`) | 9 more of those cells: names of ids 1-2 are never read (`literals-names-1-2-wrong`, 7/7) while id 3's name is (`literals-id3-name-wrong`, `PPPPFPP`) | the whole name column; the gate is asymmetric between ids 1-2 and 3-11 | `literals-names-1-2-wrong` (receipt:16), `literals-id3-name-wrong` (receipt:17) |
| `test_wal_was_decrypted`: `len(data) > 5`, then two `if`-guarded re-reads of id 1's value and id 6's name (`:92-107`) | a state that never touched `/app/main.db-wal` — `literals-never-open-db` passes it — and `truth-ids-as-strings` passes it on an export whose keys are strings, because `1 in id_to_item` is false (`PPFFFPP`) | stat, `xxd -l 32` and read-only-open the WAL and the database; the test named for decryption reads only the export and skips when a key is missing | `literals-never-open-db` (receipt:15), `truth-ids-as-strings` (receipt:24), `decrypt-in-place-no-json` (receipt:14) |
| nothing — the WAL and the database themselves | the inverse of a green: a genuinely repaired WAL with no export is `FFFFFFF` (`decrypt-in-place-no-json`) | that the graded artefact is the export alone, so "Fix the WAL file so SQLite can read it" (`instruction.md:7`) has no assertion behind it | `decrypt-in-place-no-json` (receipt:14) |
| nothing — a wrong-key XOR over the WAL (key 0x43 instead of 0x42), then a read-write extraction (which also discards the log; entry finding 6) | the 5 base rows: `xor-wrong-key` is `PPPPFPF`, failing only completeness and the WAL test — 5 of 7 assertions are satisfied by an untouched database | check the WAL magic (`37 7f 06 82`) yourself; those two failures are the only signal that the WAL was ignored | `xor-wrong-key` (receipt:11), `base-only-ro` (receipt:9) |
| nothing — a plain read-write open before the repair | the same shape: `plain-read-then-solve` is `PPPPFPF`, because the first open deleted the undecryptable WAL and the task's own `solve.sh` then had nothing to decrypt | back the WAL up before any open and read via `file:…?mode=ro` (the oracle's own comment, `solve.sh:8-10`); the destructive first read is invisible to every assertion | `plain-read-then-solve` (receipt:10) |
| nothing — do-nothing baselines and the task's own oracle | `empty-app` and `untouched` are both `FFFFFFF` (the image ships no `recovered.json`), `oracle-solve-sh` is 7/7, and `decrypt-then-extract` and `decrypt-checkpoint-truncate` are both 7/7 | run all five first: unlike round 39's grader this one starts at 0 of 7, and it cannot tell a WAL-applied read from a checkpointed-truncated one | `empty-app` (receipt:6), `untouched` (receipt:7), `oracle-solve-sh` (receipt:8), `decrypt-then-extract` (receipt:12), `decrypt-checkpoint-truncate` (receipt:13) |

What a green means here: in the probe's staged state, `/app/recovered.json` parsed as a list of eleven dicts with
integer `id`/`value` and string `name`, ids `1..11` in order, id 1's value `150`, id 2's value `250`, and the names
`cherry…mango` for ids 3-11 — on states the probe built, not states an agent built. What it does not mean: that the
WAL was repaired (a hand-typed export scores 7/7, `receipt:15`), that the database was read at all, that the values
of ids 3-11 or the names of ids 1-2 are the ones in the database (`receipt:16,30`), that values are integers rather
than booleans (`receipt:31`), that the record has no extra fields (`receipt:22`), or that an agent's first open did
not destroy the WAL it was asked to fix (`receipt:10`).

Of the six frozen instruction tags (`plans/db_wal_probe.py` `TAGS`; frozen lines in
`corpus/evidence/round40/db-wal-dry-cases-freeze.txt:1-6`), the round-40 counter's V7 rule
(`plans/round40_c2_verify.py:209-214`; label = the observed verdicts of every receipt case whose `violates=` carries
the tag) gives: `fix-wal` (`instruction.md:7`) `partly` — 23 cases, 5 observed pass; `extract-all` (`:8`) `partly` —
15 cases, 4 observed pass; `json-at-path` (`:9`) `enforced` — 5 cases, 0 observed pass; `record-format` (`:12`)
`partly` — 8 cases, 2 observed pass; `sorted-by-id` (`:13`) `enforced` — 1 case, 0 observed pass; `eleven-records`
(`:13`) `enforced` — 10 cases, 0 observed pass. `enforced` here is a property of the frozen case set only: one of
`eleven-records`' ten witnesses is the empty-`/app` baseline (`receipt:6`) and two are the untouched and base-only
states (`receipt:7,9`), so the label means "every frozen case that violates it is observed fail", not "no
improving agent can violate it". `sorted-by-id` rests on a single witness (`truth-reversed-order`, `receipt:19`),
and `json-at-path` on five that include the empty-list and non-JSON states (`receipt:28,26`). The entry's
`## Requirement map` carries one row per tag in the counter's row shape, and V7 re-derives all six labels from the
receipt.

Limits named at freeze: the probe never runs Terminal-Bench, the task image (`task.toml:29` names
`alexgshaw/db-wal-recovery:20251031`; `allow_internet = true` at `:34`; `Dockerfile:3` builds it on `ubuntu:24.04`)
or a harness, and `tests/test.sh`'s `uvx`/pytest path and its `/logs/verifier/reward.txt` write (`test.sh:18-29`)
are read, not run. Host sqlite3 3.54.0, python3 and xxd stand in for the image's Ubuntu 24.04 packages, recipes run
as the probing user rather than root, and each case stages its own `/app`, so no case observes the image's tree. The
ground-truth table the recipes copy (eleven rows, values `100*id` except id 1 → `150` and id 2 → `250`) is computed
from the two captured files under XOR key `0x42`, not from the grader (`plans/db_wal_probe.py:25-29`). The
destructive-read behaviour is published in the oracle's own comment (`solve.sh:8`), so the cases that depend on it
probe an already-documented property.

A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not solver
advice, not a statement about SQLite's WAL semantics or about any agent's behaviour.

## Scheduling-constraint TB2 grader — round 41

Before citing the pinned TB2 `constraints-scheduling` scorer, run `python3 plans/constraints_probe.py --lane .` and
read its summary line: exit `0` means only that all 25 cases produced three test verdicts twice each; prediction
mismatches are on the summary line, never in the exit code, and exit `2` is a setup failure — a duplicate or
malformed case id, an unknown tag, a malformed prediction, a capture missing or not at its pinned digest,
`/usr/bin/bwrap` or python3/bash not executable, a `--work` directory that cannot be created, or a case that did not
yield three verdicts twice (a recipe error is never a verdict) (`plans/constraints_probe.py:291-345`). `--dry` prints
the frozen case table with no sandbox and `--stage-check` builds each case's end state and prints only stage exit
codes, the grader never imported (`plans/constraints_probe.py:4-8`), so neither is evidence. The receipt's summary
(`corpus/evidence/round41/constraints-probe.txt:33`) reads `cases=25 observed_pass=6 observed_fail=19 mismatches=2`,
and a second, same-process grading of each un-rebuilt end state agrees case by case (`regrade cases=25 differ=0`,
`:32`) — a determinism read of the probe, not re-run stability (entry §Regrade).

The class differs from rounds 35-40: the verdict is **computed**, not asserted over a fixed artefact. Three pytest
functions carry a scheduling model — `_hard_ok` (Bob start, Alice end, Tue/Thu early end, Carol day end and lunch,
same-day, weekday), `_overlap` (a zip of two independent `DTSTART`/`DTEND` `findall`s per calendar) and a
minute-granularity earliest-slot scan — and apply it to three sha256-pinned input calendars
(`corpus/evidence/round41/tb2-constraints-scheduling/test_outputs.py:46-83`, `:158-167`; calendar digests in the
receipt header, `:2-4`). The graded artefact is a one-event ICS file at `/app/meeting_scheduled.ics`, read with
regexes (`_dt`, `:40-43`), never with an ICS parser. The probe seeds `/app` as the task Dockerfile does
(`Dockerfile:14`), runs a frozen recipe under `bash -euo pipefail`, then imports the captured module and calls its
three functions in file order inside a per-case bubblewrap sandbox (`plans/constraints_probe.py:10-21`), so
`tests/test.sh`'s `uvx -p 3.13`/pytest path and its `/logs/verifier/reward.txt` write (`test.sh:18-22,25-29`) are
read, not run.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| the three `/app/*_calendar.ics` as *decoded text* — `app_text == repo_path.read_text()`, or, when the repo copy is absent, `sha256(app_text)` (`test_outputs.py:88-96`) | a rewrite that changes bytes but not the newline-normalized text: `input-crlf-rewrite` passes 3/3 while `input-appended` and `input-event-deleted-wed-1000` fail (`tests=FPP`) | the bytes and the line endings, not the decoded string; `instruction.md:17-18` promises "Any modification will cause the tests to fail" | `input-crlf-rewrite` (receipt:31), `input-appended` (receipt:21) |
| `BEGIN:VCALENDAR`…`END:VCALENDAR` after `strip()`, `VERSION:2.0`, `PRODID:`, `BEGIN/END:VEVENT` (`:97-103`), then the block containing `SUMMARY:Team Planning Meeting` and all three emails (`:106-118`) | a file whose first `VEVENT` is a decoy elsewhere in the block list — tests 2-3 never open this block, so `decoy-first-vevent` passes 3/3 with the attendee meeting on Friday 15:00 | locate the meeting the way tests 2-3 do, then compare; the structure test is the only one that looks at the meeting block at all | `decoy-first-vevent` (receipt:14), `decoy-second-vevent` (receipt:28) |
| `^ATTENDEE[:;].*<email>$` under `re.I \| re.M` inside that block (`:120-123`) | the three emails each on their own unfolded line; a fourth attendee is free — `extra-attendee-dave` passes 3/3, and a folded `ATTENDEE` line (RFC 5545 3.1) fails the structure test | an ICS parser, or a fold-aware regex; the check is line-anchored text | `extra-attendee-dave` (receipt:29), `folded-attendee-line` (receipt:25) |
| `_dt(r"DTSTART:(\d{8}T\d{6}Z)", meeting)` and the same for `DTEND`, then `e - s == timedelta(hours=1)`, `2024-01-15..19`, `weekday() < 5` (`:125-129`) | the exact flat `DTSTART:…Z` spelling for one hour in that week — `duration-90min` fails only this test (`FPP`), `weekend-sat-20` fails all three, `no-prodid-header` and a wrong or partial attendee set fail only here | `DTEND` and the window yourself: tests 2-3 never read `DTEND` and recompute the end as start + 1 hour | `duration-90min` (receipt:15), `weekend-sat-20` (receipt:20), `no-prodid-header` (receipt:27) |
| tests 2 and 3 take the **first** `DTSTART:` of the whole file, not of the meeting block (`:135`, `:151`) | any file whose first `DTSTART` is not the meeting's: `decoy-first-vevent` 3/3 (receipt:14); the mirror `decoy-second-vevent`, with the attendee meeting first at Friday 15:00, is `PFF` | that the graded slot is the meeting's; both constraint tests are file-first-`DTSTART` tests (published as TB2.1 PR #245) | `decoy-first-vevent` (receipt:14), `decoy-second-vevent` (receipt:28) |
| `_hard_ok(start, start+1h)` then `_overlap` against the three calendars (`:58-83`, `:46-55`, called at `:137-143`) | the model's rules, minute-exact: `seconds-30` is `PFF` — test 1 accepts a `:30` start, test 2 fails because the end crosses into Carol's 12:00-12:30 lunch | the model's window, not the instruction's prose: Alice's "no meetings after 2 PM" becomes `t1.hour < 14 or (14,0)`, and the Bob Tue/Thu 4:30 branch (`:65-68`) is dead code once the Alice-end check (`:61`) has passed | `seconds-30` (receipt:18), `conflict-mon-1230` (receipt:12) |
| the earliest scan: every minute from Mon 09:00 to the graded start, `_hard_ok` and no overlap, raised as `Found earlier valid slot` (`:158-167`) | a slot that is itself invalid but has no *valid* predecessor: `bob-start-0900-wed` and `wed-1059-overlaps-alice` both fail only test 2 (`PFP`), so "earliest" cannot catch a wrong slot it never compares against a valid one | recompute the true earliest valid slot and compare equality; the test asserts absence of a valid *earlier* slot, not validity | `bob-start-0900-wed` (receipt:13), `wed-1059-overlaps-alice` (receipt:23) |
| `9 <= sched.hour < 12` as an unconditional assert (`:188`), plus the Monday tie-break (`:180-186`) and Carol's late buffer (`:190-208`) | a morning start; on the pinned calendars the only valid starts are already morning (`plans/constraints_probe.py:30-31`), so no frozen case witnesses the tie-break or the buffer | that the morning preference is a hard assert, not a tie-break, and that the tie-break/buffer branches are unfalsified by this case set | `later-valid-thu-1100` (receipt:11) fails only the earliest test |
| nothing — the three input calendars as *events* and the ICS as a dialect | the inverse of a green: RFC 5545-form output forms fail (`folded-attendee-line` `FPP`, `dtstart-value-datetime` `FFF`, `lowercase-property-names` `FPP`) while a CRLF output and a hand-typed file pass | parse the output as iCalendar; "valid ICS format" (`instruction.md:21`) is enforced only as five substring/structure checks | `crlf-line-endings` (receipt:24), `folded-attendee-line` (receipt:25), `dtstart-value-datetime` (receipt:26), `lowercase-property-names` (receipt:30) |
| nothing — the calendars themselves | `literal-correct-slot` passes 3/3 with a hand-typed Wednesday 11:00 file that never reads a calendar | open the calendars and derive the slot yourself before crediting a solve | `literal-correct-slot` (receipt:9) |
| the task's own oracle and the do-nothing baseline | `oracle-solve-sh` is 3/3 and `nop` is `FFF` — all three tests read the output file, so its absence fails all of them (`error=FileNotFoundError` in each) | run both first: unlike round 40's grader this one starts at 0 of 3 | `oracle-solve-sh` (receipt:8), `nop` (receipt:7) |

What a green means here: in the probe's staged state, `/app/meeting_scheduled.ics` contained a `VEVENT` with
`SUMMARY:Team Planning Meeting`, all three attendee emails, a flat `DTSTART:…Z` and a one-hour `DTEND` inside
15-19 January 2024, the model accepted the first `DTSTART` of the file, no valid slot preceded it, and it started
before noon — on states the probe built, not states an agent built. What it does not mean: that any calendar was
read (`receipt:9`), that the graded slot belongs to the meeting VEVENT (`receipt:14`), that the input calendars are
byte-identical to the repo copies (`receipt:31`), that an invalid slot is caught when no valid slot precedes it
(`receipt:13,23`), that a 90-minute meeting is caught by any test but the first (`receipt:15`), that the tie-break
and Carol-buffer branches work (no case), or that the output is valid iCalendar (`receipt:25,26,30`).

Of the eleven frozen instruction tags (`plans/constraints_probe.py` `TAGS`, frozen lines in
`corpus/evidence/round41/constraints-dry-cases-freeze.txt:1-11`), the round-41 counter's V7 rule
(`plans/round41_c2_verify.py:232-272`, label rule `:224-229`; label = the observed verdicts of every receipt case whose `violates=` carries
the tag) gives: `window` (`instruction.md:1`) `enforced` — 1 case, 0 observed pass; `output-file` (`:10`)
`enforced` — 1, 0; `meeting-title` (`:10`) `enforced` — 1, 0; `attendees` (`:10`) `enforced` — 1, 0; `one-hour`
(`:10`) `enforced` — 1, 0; `hard-constraints` (`:12`) `partly` — 5, 1 pass (`decoy-first-vevent`); `no-conflict`
(`:12`) `enforced` — 5, 0; `inputs-readonly` (`:15`) `partly` — 3, 1 pass (`input-crlf-rewrite`);
`version-prodid` (`:23`) `enforced` — 1, 0; `utc-format` (`:25`) `enforced` — 1, 0; `earliest` (`:27`) `partly` —
10, 1 pass (`decoy-first-vevent`). `enforced` is a property of the frozen case set only: seven of the eleven tags
rest on a single witness, so the label means "every frozen case that violates it is observed fail", not "no
improving agent can violate it". `hard-constraints` and `earliest` are `partly` for the same case — the decoy's
Friday 15:00 meeting sits outside Alice's 14:00 limit and after every valid slot; `inputs-readonly` is `partly`
because the CRLF rewrite passes the text comparison the tag's line promises to fail. The entry's `## Requirement
map` carries one row per tag in the counter's row shape, and V7 re-derives all eleven labels from the receipt.

Limits named at freeze: the probe never runs Terminal-Bench, the task image (`task.toml:30` names
`alexgshaw/constraints-scheduling:20251031`; `allow_internet = true` at `:35`; `Dockerfile:3` builds it on
`ubuntu:24.04`) or a harness. Host python3 stands in for pytest under `uvx -p 3.13` (`test.sh:18-22`), which needs
the network; recipes run as the probing user rather than root; each case stages its own `/app`, so no case observes
the image's tree; and the grader is bound at `/cap/test_outputs.py`, so the `inputs/` sibling the integrity check
prefers is absent and its sha256 branch runs, as in the image (`plans/constraints_probe.py:10-21`). The ground-truth
valid-slot table is hand-read from the three captured calendars, not from the grader
(`plans/constraints_probe.py:27-31`: valid starts Wed 2024-01-17 11:00 and Thu 2024-01-18 11:00, earliest Wed
11:00). 16 of the 25 cases are the round-40 planning seat's pilot, graded before this freeze, with predictions
carried verbatim; the two it observed wrong (`later-valid-wed-1105`, `receipt:10`, and `seconds-30`, `receipt:18`)
were both predicted `PPF` — only the earliest test failing — and were observed `PFF`, test 2 failing as well, and
are reported, never edited out. The decoy finding (tests 2-3 read the first `DTSTART`) is published as TB2.1 PR
#245, so this entry claims a probed instance, not a discovery.

A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not solver
advice, not a statement about RFC 5545 conformance in general, and not a statement about any agent's behaviour.
