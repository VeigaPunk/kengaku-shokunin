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
| `round42-c1-mutants` | gate | `python3 plans/round42_c1_verify.py --lane .` (lane root; `--battery-dir DIR` and `--only X1,XO5` are development selectors printing `PREDICATE C1 n/a` — they still exit 1 on any survivor in the subset (measured: `--battery-dir <empty> --only X1` → `survived=1`, `PREDICATE C1 n/a`, exit 1); `--work DIR` created if absent and **refused inside the lane** (measured: exit 2); `--jobs N` parallel tool runs, default 8) | `0` frozen predicate holds: `PINS total=2 mismatched=0`, `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=9/9 order=5/5`, `PINS-AFTER mismatched=0`, then `PREDICATE C1 pass` (`:665`) · `1` any `SURVIVED` (printed `exhibits=<directions>`), any `UNATTRIBUTED` hit (a direction hit whose traced re-run neither reproduces (exit, class set) nor executes a line of the replaced span), an `invalid`, `invalid(compile)` or `invalid(variant changed during the run)` mutant, a `NULL … differs on a second unmodified run`, `wrong>0`, `tampered>0`, `sidechannel>0`, a pin mismatch before or after the run, `len(MUTANTS)!=14`, or a per-tool count other than `anchor=9/9 order=5/5` (`:660-665`) · `2` setup: `/usr/bin/bwrap` or `/usr/bin/python3` not executable, `--work` (or the scratch root) inside the lane, a battery module that breaks the contract, or a duplicate fixture id (`:530-554`) | controls `.ufo/waves/round-42/claims/control-c1-nothing.txt` (`BATTERY fixtures=0`, `survived=14`, `anchor=0/9 order=0/5`, `PREDICATE C1 fail`, `exit=1`) re-measured unchanged on the clean clone; `control-c1-attribution.txt` (`attributed span forced to line 1` → `unattributed=14`, fail — leg f can fail); `control-c1-tool-edited.txt` (`PINS mismatched=1`, 9 invalid); `control-c1-no-mutants.txt` (`MUTANTS total=0`, fail — non-vacuity); `control-c1-hostile-escape.txt` (`SETUP … breaks the contract`, exit 2); pre-freeze witness `claims/witness-run.txt` (`14/14 killed, attributed`, development mode) | `PINS` = `plans/anchor_digest_check.py` `11bb2cad…`, `plans/order_check.py` `948d5e1d…`; `TOTAL=14`, `FLOORS={anchor:9, order:5}`; the 14 frozen ids X1 X3 X6 X7 X9 X12 X13 X14 X15 (anchor) and XO1 XO3 XO5 XO6 XO7 (order), `ADVERTISED direct=13 indirect=1 none=0` (measured); counter digest `559fca0c…` in `.ufo/waves/round-42/claims/frozen-digests.txt` | scratch under `--work`/`$TMPDIR` only — every fixture build and every tool run in its own read-only `bwrap` sandbox, the lane hidden from builds; verified with the lane bound read-only (`--ro-bind`): identical predicate, lane `git status --porcelain` empty | kengaku |
| `round42-c2` | gate | `python3 plans/round42_c2_verify.py --lane .` (lane root; `--work DIR` scratch parent, **created if absent**) | `0` `checks=9 defects=0` then `PREDICATE C2 pass` (`:336-337`) · `1` any `Vn DEFECT <note>`, including a check that raises — `error <Class>: …` is a defect, never a pass (`:328-335`); V4 and V7 both report the one string `receipt or entry absent` when *either* file is missing (`:178-184`), so a landed receipt with an unlanded entry reads as absent · `2` argparse usage only — the script has no setup exit (`:318-338`; measured `--bogus` → exit 2) | itself; freeze control `.ufo/waves/round-42/claims/control-c2-nothing.txt` (`checks=9 defects=6`: V2 V3 V4 V7 V8 V9; `PREDICATE C2 fail`, `exit=1`; its gate reads `P2 DEFECT receipt unreadable`, `P9 DEFECT untracked=31`, `P10 DEFECT receipt unreadable`) — at tip `fda71ae` on a clean clone the same shape measures `checks=9 defects=5` (V2 V3 V4 V7 V9) because the receipt has since landed: `P2 ok receipt_sha256=pinned`, `P9 ok untracked=0`, `P10 ok probe_rerun=byte-equal bytes=4212`, `V8 ok order_exit=0 result=PASS`; filler control `control-c2-filler.txt` → `V9 DEFECT`, the measured content → `V9 ok` | spec `plans/pkg-spec-r42.json` `e836c425…`, gate `plans/pkg_gate.py` `ea638822…`, probe `plans/fibsqrt_probe.py` `fc58bf3f…`, dry table `corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt` `9ee60af6…`, nine captures under `corpus/evidence/round42/tb2-circuit-fibsqrt/` (`SHA256SUMS` `36b15d5b…`), receipt `corpus/evidence/round42/fibsqrt-probe.txt` `2a54ca8a…` (not digest-pinned: P10 re-runs the probe and byte-compares) | scratch under `--work` only — verified with the lane bound read-only (`defects=5`, `exit=1`, `--work` empty afterwards); reads lane bytes and git history, writes nothing in it; its gate leg re-runs the probe, so a full run costs ≈62 s (measured 61.65 s) | kengaku |
| `fibsqrt-probe` | probe | `python3 plans/fibsqrt_probe.py --lane .` (`--dry` prints the seven `TAG` lines and the 16 frozen `CASE` lines, no sandbox; `--stage-check` builds every case's end state and prints only stage exit codes, the grader module is never imported; `--dry` and `--stage-check` are mutually exclusive; `--work DIR` scratch parent, created if absent) | `0` every case yielded three test verdicts twice and both summary lines printed — **prediction mismatches are on the summary line, never in the exit code** (measured `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, exit 0; `:358-360`) · `1` `--stage-check` only: a case's setup or recipe stage exited non-zero (`stagecheck cases=16 failed=<k>`, `:328-329`) · `2` setup: duplicate or malformed case id, unknown tag, malformed prediction or `len(GRADED)!=28` (`:290-293`); a capture missing or off its pinned digest (`:305-308`); `/usr/bin/bwrap`, `/usr/bin/python3`, `/usr/bin/bash` or `/usr/bin/gcc` not executable (`:309-312`); `--work` cannot be created (`:313-318`); a case that does not yield three test verdicts twice (`SETUP case <cid> did not yield three test verdicts twice`, `:341-344`) — a recipe that exits non-zero is a probe error, never a verdict | itself; receipt `corpus/evidence/round42/fibsqrt-probe.txt` reproduced **byte-equal** by a fresh run on the clean clone (`sha256=2a54ca8a…`, `bytes=4212`, 61 s, `diff` empty, `regrade cases=16 differ=0`); `--stage-check` `stagecheck cases=16 failed=0`, exit 0; `--dry` byte-equal to the frozen dry table (`9ee60af6…`, `diff` empty) | five capture digests in `PINS` (`test_outputs.py` `6117b8ed…`, `sim.c` `700645ac…`, `gates.txt` `032786f9…`, `solve.sh` `a4ffab41…`, `instruction.md` `a7f50026…`); 16 cases, 7 tags; the 28-value `GRADED` table (1, 4, 8, 12, 41, 42, 107, 220, 209, 366 and `x²−1`, `x²`, `x²+1` for x in 12, 41, 42, 107, 220, 209; max 48401); three grader tests in file order | scratch under `--work`/`$TMPDIR`, removed on exit (`:362`); reads the lane's captures only — verified with the lane bound read-only (`stagecheck cases=16 failed=0`, exit 0) and `git status --porcelain` empty after a full run | kengaku |
| `round43-c1-mutants` | gate | `python3 plans/round43_c1_verify.py --lane .` (lane root; `--battery-dir DIR` and `--only NA1,NO5` are development selectors printing `PREDICATE C1 n/a`; `--work DIR` created if absent and refused inside the lane; `--jobs N` default 8) | `0` frozen predicate holds: `PINS total=2 mismatched=0`, `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=9 killed=9 survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=6/6 order=3/3`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass` · `1` any survivor, unattributed (span not run, site record equal to the reference's, or reference record unstable) or invalid mutant, null detection, `wrong`/`tampered`/`sidechannel` > 0, a per-tool count off the floors, a pin mismatch · `2` setup: bwrap/python missing, `--work` inside the lane, a module that fails to build, a fixture that breaks the contract or escapes its directory (repo toplevel/`core.worktree`, a symlink out of d, an order `--claims`/`--receipt` that is a tree at HEAD) | itself; freeze controls `.ufo/waves/round-43/claims/control-c1-*.txt` (nothing `killed=0 survived=9`; no-mutants, span-forced and value-forced copies fail; six hostile modules each open under the round-42 counter and closed here) | `PINS` (both tools), `TOTAL = 9`, `FLOORS = {anchor: 6, order: 3}`, the `MUTANTS` table; digest in `.ufo/waves/round-43/claims/frozen-digests.txt` | scratch only (`--work`/`$TMPDIR`); every build and tool run in `bwrap --ro-bind / /` | kengaku round 43 (limits: `R43SentinelCounter` F1–F6, `R43MutC1Counter` 8/15) |
| `round43-c2` | gate | `python3 plans/round43_c2_verify.py --lane .` (lane root; `--work DIR` scratch parent, created if absent) | `0` `checks=10 defects=0` then `PREDICATE C2 pass` · `1` any `Vn DEFECT <note>` (a check that raises is a defect); V10 = the entry's `## Mechanism` rows on the counter's frozen DECISIVE lines with a ≥2-word verbatim quote · `2` argparse usage only | itself; freeze controls `.ufo/waves/round-43/claims/control-c2-nothing.txt` (`checks=10 defects=7`) and `control-c2-informed-filler.txt` (`red-as-required`) | spec `plans/pkg-spec-r43.json`, gate, probe, dry table, twelve captures, DECISIVE; digest in `frozen-digests.txt` | scratch only | kengaku round 43 (limit: DECISIVE is readable in the counter, so V10 is a fidelity gate, not proof of reading — `R43CritClaims` §1; `R43MutC2Counter` 6/13) |
| `feal-probe` | probe | `python3 plans/feal_probe.py --lane .` (`--dry` prints the five `TAG` lines and the 12 frozen `CASE` lines, no sandbox; `--stage-check` stages every case, byte-compiles `/app/attack.py` and builds `feal_in_c`, never imports the grader; `--work DIR` scratch parent) | `0` every case graded by two fresh harness processes and both summary lines printed — prediction mismatches are on the summary line (`cases=12 observed_pass=8 observed_fail=4 mismatches=0`), never in the exit code · `1` `--stage-check` only: a stage failed · `2` setup: malformed case table, a capture off its pin, bwrap/python3/python/bash/gcc missing, a recipe that exits non-zero | receipt `corpus/evidence/round43/feal-probe.txt` re-run byte-equal (`integrate/measure-final.txt`); real pytest parity 12/12 (`R43PytestParity`) | eight captures pinned in the probe; probe digest in `frozen-digests.txt` | scratch only; each case in bwrap with private net/pid/ipc | kengaku round 43 (host python 3.14/gcc/setuptools stand in for the image; `cheat-clock-seed` is a host-libc fact) |
| `round44-c1-mutants` | gate | `python3 plans/round44_c1_verify.py --lane .` (lane root; `--battery-dir DIR` and `--only U5,U14c` are development selectors printing `PREDICATE C1 n/a`; `--work DIR` created if absent and refused inside the lane; `--jobs N` default 8) | `0` frozen predicate holds: `PINS total=2 mismatched=0`, `BATTERY fixtures=<n> wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=4/4 order=1/1`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass` · `1` any survivor, unattributed or invalid mutant, null detection, `wrong`/`tampered`/`sidechannel` > 0, a per-tool count off its floor, or a pin mismatch · `2` SETUP: a fixture breaks the module contract or escapes its directory (round-44 fences F1–F6: `.git` file or git dir outside d, argv not the exact shape, include/alternates, a parent git call that hangs past 30 s, a `--lane` whose discovered repo is outside d) | controls `.ufo/waves/round-44/claims/control-c1-*.txt` (nothing, standing batteries, witness-as-battery, no-mutants, span, value, tool-edited, mislabel, hostile f1–f6) | `PINS` (both tools), `TOTAL = 5`, `FLOORS = {anchor: 4, order: 1}`, the `MUTANTS` table; digest in `.ufo/waves/round-44/claims/frozen-digests.txt` | scratch only (`--work`/`$TMPDIR`); every build and tool run in `bwrap --ro-bind / /` | kengaku round 44 |
| `round44-c2` | gate | `python3 plans/round44_c2_verify.py --lane .` (lane root; `--work DIR` scratch parent, created if absent) | `0` `checks=11 defects=0` then `PREDICATE C2 pass` · `1` any `Vn DEFECT <note>` (a check that raises is a defect, never a pass); V11 is the held-out predictor — the entry's `## Predictor` block must agree with the captured grader on 48 generated end states with ≥8 passes and ≥8 fails · `2` argparse usage only | itself; freeze control `.ufo/waves/round-44/claims/control-c2-nothing.txt` (`PREDICATE C2 fail`, exit 1); predictor control `.ufo/waves/round-44/claims/control-c2-predictor.txt` (`red-as-required`: always-True 24 disagreements, whitespace-token-set 12, exact-lines 18, substring ok) | spec `plans/pkg-spec-r44.json`, gate, probe, dry table, eleven captures and DECISIVE pinned in the counter | scratch only | kengaku round 44 |
| `feal-linear-probe` | probe | `python3 plans/feal_linear_probe.py --lane .` (`--dry` prints the four `TAG` lines and the 14 frozen `CASE` lines, no sandbox; `--stage-check` builds every case's end state and reports whether `/app/plaintexts.txt` exists, never grading; `--work DIR` scratch parent) | `0` every case graded by two fresh harness processes and both summary lines printed — prediction mismatches are on the summary line (`cases=14 observed_pass=8 observed_fail=6 mismatches=0`), never in the exit code · `1` `--stage-check` only: a case's setup or recipe stage exited non-zero · `2` setup: a capture missing or off its pinned digest, bwrap/python3/bash/gcc not executable, an uncreatable `--work`, or a case whose recipe exited non-zero | none (`--stage-check` builds end states only) | receipt `corpus/evidence/round44/feal-linear-probe.txt` (`regrade cases=14 differ=0`), dry table `corpus/evidence/round44/feal-linear-dry-cases-freeze.txt` | scratch under `--work` | kengaku round 44 |
| `scratch-root-guard` | gate | `python3 plans/scratch_guard.py check <root>` and `python3 plans/scratch_guard.py safe-rm <root> <seat> <path>` (`--dry-run` prints `WOULD-DELETE`; `--json`; `--selftest` runs the temp-root cases) | `0` check green, or the delete performed · `1` check red (sentinel missing / unparseable / another round, or a failing selftest case) — and **`check` on an unreadable sentinel exits 1 today although `plans/scratch_guard.py:17-18` promises 2** (measured 2026-10-26, routed `R42-R6`) · `2` usage, an untrusted root, or a refused delete (`root-untrusted`, `target-outside-seat`, …) | `python3 plans/scratch_guard.py --selftest` (`SELFTEST ok=36/36`, measured; no unreadable-sentinel `check` case yet) | round-42 sentinel `/fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL` (present when the criterion was written, since deleted with that scratch root) | writes and deletes only inside `<root>/<seat>`; the root's sentinel is read, never written | kengaku |
| `adoption-check` | gate | `python3 plans/adoption_check.py --lane . --expect <expect.json> --census` (`--expect` is required; `--census` is required for a pass — without it the run prints `census=skipped` and exits 1, measured) | `0` every frozen clause holds: `entries`/`indexed`/`usedby_ok` at the entry count, `cited_rows`/`rows_present`/`rows_mined` at the declared source count, `census=ok`, plus the unprinted legs (`verified-at` date, exact id set, no duplicate ids, exactly one shaped index row) · `1` any clause false — an empty expectation prints `entries=0 … -> empty expectation is not a pass`, an unreadable expectation raises `FileNotFoundError` (both measured) · `2` argparse usage (`--expect` absent, measured) | none declared — the script carries no self-test switch and no fixture battery; falsification is external: the committed do-nothing control `.ufo/waves/round-30/claims/control-nothing.txt` (`entries=0 …`, exit 1) and the round-33 expectation fixture | the `--expect` JSON is the pin (`round`, `access_date`, per-entry `path` + `sources`); measured on `.ufo/waves/round-33/claims/adoption-expect.json` → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`, exit 0; the census helper is the hardcoded absolute `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | none — reads `corpus/SOURCES.md`, `corpus/README.md` and the expectation entries; when `--census` runs the census script as a fixed argv subprocess (no shell) | kengaku |
| `attrib-probe` | probe | `python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md` (subcommands `block-sha`, `trials`, `force-trials`, `stream-trials` and `score`, the trial modes taking `--shim ds or glm`, `--out` JSONL scratch and `--receipt` appended log) | `0` the command completed: `freeze-check` verified the pin (`FREEZE-CHECK … stable=True -> OK`), a trial mode sent its whole frozen budget, `block-sha` printed the block digest, `score` verdict `PASS` · `1` `score` verdict `FAIL` (accuracy under the frozen bar, or the r23 stream target clause missed) · `2` refusal with nothing sent: frozen-table pin failure, `--shim glm` on a ds-only forcing mode, table version other than v2/v3 for the forcing modes, a table with no forcing section, or no subcommand (measured: no subcommand, `--shim glm` on a forcing mode and a v1 table on `force-trials`, the last two creating no `--out` or `--receipt` file) | none declared — no self-test switch; the standing check is the `freeze-check` subcommand (measured `block_sha=1b2d6a01bfa431ec pinned=1b2d6a01bfa431ec stable=True -> OK`, exit 0, and `9f0244bb0aa4463c` on the r21 table); the blind rule is enforced in code, not by fixtures | `plans/attrib-r21-frozen.md` (block sha `9f0244bb0aa4463c…`), `plans/attrib-r22-frozen.md` (v2 + `leg_forcing`), `plans/attrib-r23-frozen.md` (v3 + `stream_forcing`, block sha `1b2d6a01bfa431ec…`), each carrying a `FROZEN: <utc> sha256:<64 hex>` line the instrument re-derives | writes only the caller-named `--out` JSONL and `--receipt` log (both opened append); POSTs to the localhost shims `ds-flash-shim` :8791 and `glm-flash-shim` :8793; `score` runs `journalctl --user -u <unit>`, the only ground-truth read, after every trial | kengaku |
| `catalog-probe` | probe | `python3 plans/catalog_probe.py --verify --lane .` (no flag: live probe of the two catalog URLs and a freshness read of the entry; `--capture` fetches and writes bounded raw bytes; `--diff` is accepted and does nothing, it exists for the round-32 counting command) | `0` `raw=ok … verify=ok` (offline re-derivation from committed raw bytes agrees with the receipt and the entry's re-probe block), or a live probe that reached both catalogs with a current entry (`entry=ok`) · `1` `raw=absent`, `raw=invalid`, `raw=unparsable`, `receipt=absent`, `receipt-mismatch`, `entry-mismatch`, `entry=missing`, `entry=stale`, `entry=missing-receipt`, `entry=invalid-receipt`, a capture over the 64 KiB bound, or a failed fetch · `2` argparse usage only (the script has no setup exit) | `python3 plans/catalog_probe.py --selftest` (13 cases in a temp dir: parser guards, absent and current and tampered capture, entry block, digest tamper; measured `SELFTEST checks=13 failed=0`, exit 0) | `ACCESS_DATE=2026-10-25`, the 11 Hugging Face and 12 OpenRouter schema fields, `RAW_CAP=64*1024`, `CAP_DIR=corpus/evidence/round33/catalogs/` with `SHA256SUMS` over `hf.raw.json` and `or.raw.json`; measured `hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0` | `--capture` writes four files under `corpus/evidence/round33/catalogs/` and fetches `huggingface.co/api/models` and `openrouter.ai/api/v1/models`; the default probe fetches and writes nothing; `--verify` and `--selftest` write nothing outside a `mktemp` dir | kengaku |
| `defect-ledger` | gate | `python3 plans/defect_ledger.py --lane .` (lane root; `--lane` is the only flag and defaults to `.`) | `0` every row closed, every check passing, no mismatch: `rows=5 closed=5 observed_pass=5 mismatches=0` then `PREDICATE C2 pass` (measured at the base tip) · `1` any disagreement — a `closed` row whose check fails (`agree=NO` on its line), an `open` row whose check passes, an unknown `check` name, or a check that raises (a crash is an observed failure, never a pass); an absent ledger or a failing git call also exits 1 (measured) · `2` argparse usage only | none declared — no self-test switch; the five checks are exercised by the committed ledger itself and by the round-35 do-nothing control `.ufo/waves/round-35/claims/control-c2-nothing.txt` (`rows=5 closed=0 observed_pass=0`, exit 1) | `corpus/defects.jsonl`, five rows R34-D1…R34-D5, each naming one function of the script's `CHECKS` dict; the checks read the `.ufo/waves/round-34/` captures, `SCORECARD.md` and `corpus/lessons/round-34.md` / `round-35.md`; lane branch `refs/heads/master` | none — reads lane bytes and runs `git -C <lane> ls-files` / `ls-tree` as fixed argv (no shell); writes nothing | kengaku |
| `gate-flip-check` | gate | `python3 plans/gate_flip_check.py --lesson <lesson.md>` (repeatable `--entry <file-or-dir>`; no lane and no git needed) | `0` every conditional Gate refusal is resolved by a later `Flip check (round N): <item> — fired or not fired — <evidence>` line and no accepted `not fired` resolution names a file an entry cites (`FLIPS total=<n> unresolved=0`, `FLIP-CITE … red=0`) · `1` an unresolved obligation (`FLIPS … unresolved=<u>`, `u>0`) or a citation contradiction (`FLIP-CITE … verdict=RED`) — measured red on `corpus/lessons/round-51.md`: `FLIPS total=1 unresolved=1`, exit 1 · `2` setup/usage: `SETUP no '## Gate' section`, unreadable lesson, `--lesson` absent without the self-test switch (argparse) — both setup lines measured | `python3 plans/gate_flip_check.py --selftest` (built fixtures in a temp dir, each run as a subprocess and expected red, green or setup; measured `SELFTEST ok=27/27`, exit 0) | none in the script — the lesson is the input; the lesson round is parsed from the file name and a resolution below it does not resolve; measured cases `cite-later-fired-supersedes` green and `cite-later-not-fired-reopens` red | none — reads one lesson's `## Gate` section and the `.md` entries it names under `corpus/knowledge/`; the self-test builds its fixtures in a `mktemp` dir and removes it | kengaku |
| `extraction-policy-compare` | probe | `python3 plans/parser_policy_compare.py --summary` (lane root; `--root DIR`, `--json`, `--selftest`) | `0` ran and the pins plus the E0 baseline reproduce — measured `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5`, exit 0 · `1` a defect: `DEFECT POPULATION …` (a changed or unpinned input), `BASELINE E0 != grader.extract_json_block` on any record or E0 `agree` under `n=1964`, `POLICY-RAISE`/`GRADER-RAISE` (a raise is a defect, never a FAIL), or a selftest failure · `2` argparse usage | `python3 plans/parser_policy_compare.py --selftest` (measured `SELFTEST total policies=9 cases=59 mutants=10 killed=10 failures=0`, exit 0; the pin-rejection case prints `SELFTEST pass pin-reject-before-policies summary_rc=1 json_rc=1 pin_error=True policy_calls=0`) | the 1964-record four-file population, its SHA-256 pins and the per-record grader dispatch are imported from `plans/grader_perturb.py`; E0 must equal `grader.extract_json_block` on every record; the E0–E8 policy table is frozen in `plans/round-27-claims.md` | none — repo bytes only; the selftest writes one `mktemp` tree (`r27-policy-pin-`), no network, no endpoint | kengaku |
| `password-recovery-probe` | probe | `python3 plans/password_recovery_probe.py --lane .` (`--dry` prints the frozen 16-case table with no sandbox; `--stage-check` builds each end state and reports `/app/recovered_passwords.txt` only, never grading; `--work DIR` scratch parent, default `$TMPDIR`; `--dry` and `--stage-check` are mutually exclusive) | `0` every case graded twice and the summary line printed — **prediction mismatches are on the summary line, never in the exit code** (receipt `corpus/evidence/round45/password-recovery-probe.txt`: `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0`) · `1` `--stage-check` only: a case's staged end state failed (`stagecheck cases=16 failed=<k>`) · `2` setup: a capture missing or off its pinned digest, `/usr/bin/bwrap` or a required tool (`python3`, `bash`, `zip`, `dd`, `strings`) not executable, an uncreatable `--work`, a recipe exiting non-zero, a malformed case table, or `--dry` given with `--stage-check` | none — the script has no `--selftest`; its `--dry` table is the freeze receipt and `--stage-check` is the sandbox-plumbing control, so this row claims no self-test rather than an unbacked flag | capture `corpus/evidence/round45/tb2-password-recovery/` pinned by SHA-256 in the script — `setup.sh 9fdde5d9…`, `solve.sh c5f9fc70…`, `instruction.md bc4f5011…`, `test_outputs.py 2dc14fc1…` at terminal-bench-2 `2fd12b88`; two graded tests `test_recovery_file_exists`, `test_password_match`; receipt `corpus/evidence/round45/password-recovery-probe.txt`, reproduced byte-equal by a fresh run on 2026-10-28 (exit 0, `stagecheck cases=16 failed=0` in `--stage-check`) | scratch only — per-case `mktemp` dirs under `--work`/`$TMPDIR` (`k45-prp-*`, removed in a `finally`); the lane is read-only; each case runs in its own bwrap sandbox (`--unshare-net --unshare-pid --unshare-ipc`, `/usr` and `/etc` read-only, private `/tmp`, `/dev/urandom` bound to 64 KB of zeros) | kengaku round 45 |
| `polyglot-c-py-probe` | probe | `python3 plans/polyglot_c_py_probe.py --lane .` (`--dry` prints the frozen 18-case table with no sandbox; `--stage-check` builds every end state and reports its shape plus a parse-only `pycheck`/`ccheck`, never importing or calling the grader; `--work DIR` scratch parent, default `$TMPDIR`; `--dry` and `--stage-check` are mutually exclusive) | `0` every case graded twice and the summary line printed — **prediction mismatches are on the summary line, never in the exit code** (receipt `corpus/evidence/round46/polyglot-c-py-probe.txt`: `cases=18 observed_pass=7 observed_fail=11 mismatches=0`, `regrade cases=18 differ=7`) · `1` `--stage-check` only: a case's staged end state did not match its declared `expect` (`src`/`dir`/`absent`) or a stage exited non-zero (`stagecheck cases=18 failed=<k>`) · `2` setup: a capture missing or off its pinned digest, `/usr/bin/bwrap` or a required tool (`python3`, `bash`, `gcc`) not executable, an uncreatable `--work`, a recipe exiting non-zero, a malformed case table, or `--dry` given with `--stage-check` | none — the script has no `--selftest`; `--dry` is the freeze receipt and `--stage-check` the plumbing control, so this row claims no self-test rather than an unbacked flag | capture `corpus/evidence/round46/tb2-polyglot-c-py/` pinned by SHA-256 in the script — `test_outputs.py b94a7a98…`, `instruction.md a57c0c0e…`, `solve.sh e768453a…`, `README.md 591e27f9…`, `test.sh 4770437e…`, `Dockerfile 2eb537f2…`, `task.toml d31b9f60…` at terminal-bench-2 `2fd12b88`; one graded test `test_fibonacci_polyglot`; receipt `corpus/evidence/round46/polyglot-c-py-probe.txt`, reproduced byte-equal by a fresh run on 2026-10-28 (exit 0, `stagecheck cases=18 failed=0` in `--stage-check`) | scratch only — per-case `mktemp` dirs under `--work`/`$TMPDIR` (`k46-pgp-*`, removed in a `finally`); the lane is read-only; each case runs in its own bwrap sandbox (`--unshare-net --unshare-pid --unshare-ipc`, `/usr` and `/etc` read-only, private `/tmp`), with the captured grader mounted read-only at `/tests` | kengaku round 46 |
| `round28-census` | gate | `python3 plans/round28_census.py --root . --revision REV` (`--revision` is required and caller-supplied, never inferred from HEAD; `--root` defaults to this checkout) | `0` every leg clean — `plans/benchmark_spec_audit.py --json` exit 0, `plans/registry_check.py --json` exit 0, `plans/state_check.py --json` exit 0, 0 malformed `corpus/SOURCES.md` rows, and no unindexed, dangling or duplicate `corpus/knowledge` index rows · `1` any leg unclean — **red at the base tip `30801b47`**, measured `state_check` `mismatch=1` (`P3c.box.4.pointer.1`) plus one unindexed file `knowledge/fixture-honest-geometry.md`, so it prints its JSON and exits 1 · `2` argparse usage (measured: no `--revision` → usage line, exit 2) | none — the script has no `--selftest`; its three legs are separate registry rows (`benchmark-spec-audit`, `registry-reference-check`, `state-assertion-check`) that carry their own self-tests, so this row claims none of its own | caller-supplied revision label plus the legs' own pins (`plans/fixtures/r28/webarena/manifest.json`, `plans/fixtures/r28/registry/population.json`); measured at `30801b47` — spec audit `distinct_task_ids=812 selected_count=16`, registry check `source_rows_checked=13 findings=0`, `SOURCES` rows 171 malformed 0, knowledge files 55 against 54 index rows | none — read-only; each leg runs as a subprocess with `PYTHONDONTWRITEBYTECODE=1` and `--json`, and only JSON on stdout is produced | kengaku round 28 |
| `round30-defects` | gate | `python3 plans/round30_defects.py --lane .` (lane root; `--selftest` runs the frozen-list assertion and the empty-tree reds) | `0` all five frozen checks re-derive repaired — measured `ok D1 … ok D5`, `checks=5 defects=0`, exit 0 · `1` any defect: one `DEFECT <Dn> <label>: <reason>` line per failing check then `checks=5 defects=<k>`, or the check list no longer matching the frozen five (`DEFECT registry: …`, `defects=6`); an unreadable input is a defect (`input unreadable (…)`), never a crash or a pass · `2` argparse usage | `python3 plans/round30_defects.py --selftest` (measured `SELFTEST checks=5 failed=0`, exit 0 — the frozen-list assertion plus one `Dn-red-on-empty` case per check, so a check that returns clean unconditionally fails) | the frozen five items D1–D5 with their labels (`receipt-at-cited-path`, `kappa-sweep-scope`, `s078-line75-word-count`, `uncommitted-wave-evidence`, `s091-usedby-asymmetry`); anchors `corpus/evidence/round29-attempt2/control-nothing.txt`, `corpus/lessons/round-29.md`, the 8-word S078 quote, `.ufo/waves/round-29/attempt2/adoption-expect.json` | none — reads lane bytes and Git plumbing only (`git -C <lane> cat-file -p HEAD:<path>`, `git -C <lane> status --porcelain`); writes nothing | kengaku round 30 |
| `round31-c1-literals` | gate | `python3 plans/round31_c1_verify.py --lane .` (lane root; `--lane DIR`) — second receipt for round 31's C1: the literals `adoption_check.py` does not read, as six checks V1–V6 | `0` all six checks hold (`checks=6 defects=0`, measured) · `1` any `DEFECT V<n> <label>: <reason>` with `checks=6 defects=M` (M>0), including an unreadable expect file, which prints `VERIFY expect unreadable: …` then `checks=6 defects=6` (measured) · `2` argparse usage only — the script has no setup exit | `python3 plans/round31_c1_verify.py --selftest` (measured `SELFTEST checks=6 failed=0`, exit 0: `registry-complete` plus V1–V6 each shown red against `/nonexistent-lane-31`) | entry `corpus/knowledge/benchmark-verifier-execution-model.md`; `PINS` = the three revision prefixes `6099b8cf`, `66f92766`, `2fd12b88` that the entry must name; expect `.ufo/waves/round-31/adoption-expect.json`, whose sha256 must appear in the control receipt as `expect_sha256=`; control `.ufo/waves/round-31/claims/control-nothing.txt` must record `exit=1`; entry ≥40 lines and ≥3000 bytes; index title cell ≥20 chars | none — reads committed lane bytes only (entry, `corpus/SOURCES.md`, `corpus/README.md`, the expect file, the control receipt); `--selftest` writes nothing (it has no temp tree) | kengaku round 31 |
| `round31-defects` | gate | `python3 plans/round31_defects.py --lane .` (`--lane DIR`) — re-derives the ten round-30 defects routed to the lane as R1–R10 | `0` all ten re-derive as repaired (`checks=10 defects=0`, measured) · `1` any `DEFECT R<n> <label>: <reason>` (a check that raises is a defect: `check raised <Class>: …`), or a check list that no longer matches `FROZEN`, which prints `DEFECT registry: …` then `checks=10 defects=11` · `2` argparse usage only | `python3 plans/round31_defects.py --selftest` (measured `SELFTEST checks=10 failed=0`, exit 0, over 11 `CASE` lines — the summary label counts checks, not cases) | baseline `0883e72ef8474ca42ac1a54eb0273079f1507035`, where any deleted line fails R1/R2/R3/R10 (append-only); the frozen ten-item `(id,label)` list asserted on every run; five `.ufo/waves/round-30/…` seat reports committed at HEAD at no fewer lines than at the baseline, and `HEAD`'s `R30DraftGate.md` must carry `Pass 9`; `.ufo/waves/round-30/falsify/swarm-registry.json` exactly 33 members; the read-only staged file under `/home/vgpnk/Projects/shokuknow/merge/kengaku/…` must name exactly 3 source URLs | none of its own — read-only `git -C <lane> diff --numstat`, `status --porcelain`, `cat-file`; `--selftest` builds a `tempfile` tree only; it reads (never writes) the staged file inside the shokuknow checkout | kengaku round 31 |
| `round33-c1-literals` | gate | `python3 plans/round33_c1_verify.py --lane .` (lane root; `--lane DIR`) — round 31's six checks plus V7 renumber-map and V8 refusal-rows | `0` all eight checks hold (`checks=8 defects=0`, measured) · `1` any `DEFECT V<n> <label>: <reason>`; an absent expect file prints `DEFECT V0 expect: …` then `checks=8 defects=1` (measured — V0 is not one of the eight checks, so the count starts at 1) · `2` argparse usage only | `python3 plans/round33_c1_verify.py --selftest` (measured `SELFTEST cases=11 failed=0` — the label is `cases=`, unlike its round-31 sibling's `checks=`; the battery adds a V8 green refusal fixture and a V8 teaches-erasure red) | `PINS` = `66f92766`, `9be8d8fe`, `2412.05579`; the renumber map staged `S094`→`S103` and `S097`→`S104` must appear within 80 characters of each other in `corpus/lessons/round-33.md`; refusal rows `S094`/`S097`/`S101`/`S102` must keep `supersedes <id>` in the source cell, a refusal word in `teaches` and `rejected` in status; entry `corpus/knowledge/benchmark-grader-semantics.md`; expect and control under `.ufo/waves/round-33/claims/` | none — reads committed lane bytes only; `--selftest` writes a synthetic registry under `tempfile.TemporaryDirectory()` | kengaku round 33 |
| `round33-defects` | gate | `python3 plans/round33_defects.py --lane .` (`--lane DIR`) — re-derives the six round-32 defects routed to the lane as N1–N6 | `0` all six re-derive as repaired (`checks=6 defects=0`, measured) · `1` any `DEFECT N<n> <label>: <reason>` (a raising check is a defect, never a pass) · `2` argparse usage only | `python3 plans/round33_defects.py --selftest` (measured `SELFTEST checks=14 failed=0` over 14 `CASE` lines: registry, N3 and N4 red/green pairs, four red-on-empty, four green fixtures, one N1 untracked-red) | closure tip `112091c` named in the round-32 report; phantom hash `a44b5a8` retained and superseded with `ae95fe0` named; `:35-38`→`:39-40` and `:78-81`→`:72`/`82-83`; S086 recorded as published without peer review; `## Round 32` in `SCORECARD.md`; every file under `.ufo/waves/round-32/` tracked | none of its own — `git ls-files` plus `find`; `--selftest` runs `git init` and `git add .` inside its own `tempfile` tree only. Two of the six checks (N3, N4) read absolute fleet paths `/home/vgpnk/Projects/shokunin/.ufo/reports/round-3{1,2}/kengaku.md`, so `--lane` does not redirect them (measured: on an empty lane N3/N4 stayed green and the run printed `checks=6 defects=4`) | kengaku round 33 |
| `round35-c1-coverage` | gate | `python3 plans/round35_c1_verify.py --lane .` (lane root; `--fleet DIR` defaults to `/home/vgpnk/Projects/shokunin`) — the pinned TB2 `protein-assembly` grader admission, as six checks V1–V6 | `0` `checks=6 defects=0` then `PREDICATE C1 pass` · `1` any `V<n> DEFECT <reason>` — a check that raises prints `error <Class>: …` and is a defect, never a pass — then `checks=6 defects=M` and `PREDICATE C1 fail` · `2` argparse usage only (the script has no setup exit) | none — this counter has no self-test and no fixture tree: `--selftest` is rejected by argparse (`error: unrecognized arguments: --selftest`, exit 2, measured 2026-10-28). Its only falsifier is its own `V<n> DEFECT` lines on a lane that breaks a pin; measured red today on V4 | TB2 pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` with three capture sha256: `44a05a24…` (`test_outputs.py`), `9ede4664…` (`test.sh`), `1bb2af1d…` (`instruction.md`); rows S105/S106/S107 exactly once each, 11 cells, tier A, status `mined`, opened 2026-10-25; entry head lines 1–5 (three `source:` lines, `verified-at: 2026-10-25`, `recheck:`); ≥8 located quotes of ≤25 words, each verbatim in the cited capture; `knowledge files == index rows == 42` — **stale: measured 55 files / 54 index rows at the base tip `30801b47` and at HEAD, so V4 is red by construction and this row must not be read as "lane clean"** | none of its own, but it executes two other instruments: `plans/tb2_grader_probe.py` in the lane cwd (V5, output byte-compared to `corpus/evidence/round35/tb2-grader-probe.txt`) and `scripts/sources-census.sh` (V6: `validate --root <fleet> kengaku` on the live lane, `validate --file <lane>/corpus/SOURCES.md` on a clone); when `Bio` is not importable it runs the probe under `uv run --no-project --with biopython==1.85`, which reaches the network | kengaku round 35 |
| `round35-hardening` | gate | `python3 plans/round35_hardening.py --lane .` (lane root; `--repo DIR` the git repo holding the freeze commit, default `--lane`; `--skip H1`..`H6` repeatable, prints `Hn skipped`) | `0` every run check ok (`hardening run=6 failed=0`, or `run=5 failed=0` with H6 skipped) · `1` one `Hn FAIL <note>` line per failed clause then `hardening run=<n> failed=<k>` — a check that raises prints `Hn FAIL error <Class>: …` and is a failure, never a pass · `2` argparse usage only (the script declares no setup exit) | none in the script — it declares no self-test spelling; falsifiers are external, the five seat counterexamples in `corpus/evidence/round35/hardening-counterexamples.txt` (junk package → H1 H2 H3 FAIL; false-but-labelled D4 line → H4 FAIL; erratum negation → H5 FAIL; quote injected into an altered capture → H5 FAIL; straight-quote row → H2 FAIL) | freeze commit `11d6453…` and byte-equality of `plans/tb2_grader_probe.py`, `plans/round35_c1_verify.py` and `plans/defect_ledger.py` against their blobs there; entry `corpus/knowledge/tb2-protein-assembly-grader.md` (≥8 distinct ≥3-word quotes at ≥8 distinct lines, no unparsed row); SOURCES rows S105–S107 (11 cells, ≥8-word teaches); the D4 correction line in `SCORECARD.md`; round-34 erratum plus `nec-s091-reopen.html` against `quarantine-SHA256SUMS` | none — read-only: `git -C <repo> show` and `git ls-files --others` plus lane byte reads, no file written; H6 counts untracked files lane-wide, so a wave marker makes it fail (measured at base tip on a clean clone: `hardening run=6 failed=0`, exit 0; on a lane carrying untracked wave files H6 fails, exit 1 — measured `H6 FAIL untracked_anywhere=2` in wave 1 and `untracked_anywhere=881` on the live lane during wave 2) | kengaku |
| `round36-c2` | gate | `python3 plans/round36_c2_verify.py --lane .` (lane root; `--fleet DIR` the fleet root whose `scripts/sources-census.sh` W6 runs, default `/home/vgpnk/Projects/shokunin` — a lane that is not `<fleet>/kengaku-shokunin` validates its own `corpus/SOURCES.md`) | `0` all six checks ok (`checks=6 defects=0`) then `PREDICATE C2 pass` · `1` any `Wn DEFECT <reason>` then `checks=6 defects=<n>`, `PREDICATE C2 fail` — a check that raises prints `Wn DEFECT error <Class>: …` and is a defect, never a pass · `2` argparse usage only (no setup exit declared) — measured on a clean clone at base tip `30801b4` (2026-10-28) the tip fails the structural W4 leg, `W4 DEFECT knowledge files=55 index rows=54`, `checks=6 defects=1`, exit 1 | no self-test spelling; the six-check battery is the counter itself, falsified by the freeze controls `.ufo/waves/round-36/claims/control-c2-nothing.txt` (`W2/W3/W4/W5 DEFECT`, `checks=6 defects=4`, exit 1) and `control-c2-skip.txt` (`checks=6 defects=4`, exit 1) | probe `plans/regex_log_probe.py` sha256 `d58194c8…` (amendment 1); the three captures `corpus/evidence/round36/tb2-regex-log/` at `345c3bd0…` (test_outputs.py), `4770437e…` (test.sh), `4f7ac05e…` (instruction.md) from pin `2fd12b88…`; receipt `corpus/evidence/round36/regex-log-probe.txt` byte-equal to a fresh probe run whose summary line is `cases=24` | none in the lane — the only writes are the probe's own temporary directory; W5 runs the probe and W6 runs `scripts/sources-census.sh validate` as fixed argv, no shell, and the pinned raw URL is compared as a string, never fetched | kengaku |
| `round45-c1` | gate | `python3 plans/round45_c1_verify.py --lane .` (lane root; `--work DIR` scratch parent that must lie outside the lane and is created if absent; `--jobs N` parallel fence runs, default 8) | `0` `PINS total=33 mismatched=0`, then `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, `CALIBRATION advertised=10 contradicted=0`, `PREDICATE C1 pass` · `1` any leg short (leaked/read/hung module, honest fixture refused or touching outside `d`, pin mismatch before or after the run, `contradicted>0`) then `PREDICATE C1 fail` · `2` setup: `/usr/bin/bwrap`, `/usr/bin/python3` or `/usr/bin/strace` not executable, the round-44 counter off its pin, or `--work`/the scratch root inside the lane | no self-test spelling — the 33 pins plus the refusal, honest and calibration legs are the battery; falsifiers are the round-45 freeze controls, `.ufo/waves/round-45/claims/control-c1-nothing.txt` (`REFUSALS total=10 clean=0 leaked=10`, `contradicted=10`, exit 1), `control-c1-fence-admit_all.txt` (`contradicted=10`), `control-c1-fence-refuse_all.txt` (`admitted=0 refused=104`), `control-c1-fence-static_only.txt` (`contradicted=1`), `control-c1-fence-r44.txt` (`contradicted=7`) — named limit: `control-c1-fence-keyed_name.txt` PASSES (`contradicted=0`, exit 0), the Q39 keying weakness the round-46 counter was written to catch | 33 PINS: `plans/round44_c1_verify.py` `6cf05323…` (builder, imported unchanged), the ten `plans/refusals45/` modules, the 22 standing battery modules of `plans/battery42`–`battery44`; predicate literals `REFUSAL_TOTAL=10` and `HONEST_TOTAL=104`; green receipt `corpus/evidence/round45/c1-counter-run.txt` | scratch only — `tempfile.mkdtemp` under `--work`/`$TMPDIR`, removed in a `finally`; the fence and every fixture run read-only under `bwrap` under `strace -f -y`; with `K45_KEEP_STRACE=DIR` set it also copies each strace log into DIR; lane bytes never written (clean clone `git status --porcelain` empty after the run) | kengaku |
| `round45-c2` | gate | `python3 plans/round45_c2_verify.py --lane .` (lane root; `--work DIR` scratch parent, created if absent) | `0` `V1`–`V11` all ok, then `checks=11 defects=0`, `PREDICATE C2 pass` · `1` any `Vn DEFECT <note>`, including a check that raises (`Vn DEFECT error <Class>: …` is a defect, never a pass) and including an absent `/usr/bin/bwrap`, which surfaces as a V11 defect rather than a setup exit · `2` argparse usage only (no setup exit declared) — measured on a clean clone at base tip `30801b4` (2026-10-28): `V2 DEFECT spec=frozen gate=frozen gate_exit=1` (the embedded gate's P8 prints `index_rows=54 knowledge_files=55`), `checks=11 defects=1`, exit 1, every other leg green | no self-test spelling; V11's falsifiers are the freeze controls in `.ufo/waves/round-45/claims/control-c2-predictor.txt` (always-true `disagree=30`, substring `disagree=12`, password-eq `disagree=21`, lookup table `lint DEFECT`, membership `ok`) and the package control `control-c2-nothing.txt` | spec `plans/pkg-spec-r45.json` `2f924ffa…`, gate `plans/pkg_gate.py` `ea638822…`, probe `plans/password_recovery_probe.py` `9363e03e…`, dry table `corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` `46036abe…`, nine captures under `corpus/evidence/round45/tb2-password-recovery/`; V11 generator `random.Random(45)` over 16 kinds = 48 states with `grader_pass=18 grader_fail=30`; green receipts `corpus/evidence/round45/counter-a-run.txt` and `counter-b-run.txt` | scratch only — `tempfile.TemporaryDirectory` under `--work`, holding the effective spec copy and the V11 sandbox files; the gate (`package --rerun --require-clean-tree`), `plans/order_check.py` and `scripts/sources-census.sh validate` run as fixed argv; lane bytes never written (clean clone `git status --porcelain` empty after the run) | kengaku |
| `round46-c1` | gate | `python3 plans/round46_c1_verify.py --lane .` (lane root; `--work DIR` scratch parent outside the lane, created if absent; `--jobs N` default 8; testing overrides `--refusals DIR`, `--sealed DIR`, `--fence PATH`, `--seed HEX`, and the predicate they print is the predicate of the inputs they name, never a receipt for the frozen run) | `0` `PINS total=65 mismatched=0`, `REFUSALS total=20 clean=20 leaked=0 read=0 hung=0 build_errors=0`, `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`, `CALIBRATION advertised=32 contradicted=0`, `REASON -`, `PREDICATE C1 pass` · `1` any failing leg, listed on `REASON <comma list>` (`pins=`, `pins-after=`, `refusals-total=`, `refusals-not-clean`, `sealed-total=`, `sealed-not-clean`, `honest-not-admitted`, `contradicted=`) then `PREDICATE C1 fail` · `2` setup: `/usr/bin/bwrap`, `/usr/bin/python3` or `/usr/bin/strace` not executable, the round-44 counter off its pin, or `--work`/the scratch root inside the lane | no self-test spelling — the 65 pins, the two hostile legs with their floors and the honest leg are the battery; falsifiers are the 34 `control-*.txt` files under `.ufo/waves/round-46/claims/` (generator `stage2_controls.py`), e.g. `control-c1-base-fence.txt` (`REFUSALS total=20 clean=10 leaked=10`, `SEALED total=12 clean=0 leaked=12`, `contradicted=22`, exit 1), `control-c1-fence-admit_all.txt` (exit 1), `control-c1-fence-refuse_all.txt` (exit 1), `control-c1-fence-keyed_name.txt` (`contradicted=32`, exit 1) | 65 PINS: `plans/round44_c1_verify.py` `6cf05323…`, `plans/refusals45/f1`–`f10`, `plans/refusals46/f1`–`f20` with the f1–f10 byte-copy check, the 12 `plans/sealed46/` modules, the 22 battery modules; literals `REFUSAL_FLOOR=20`, `SEALED_FLOOR=12`, `HONEST_TOTAL=104`, `PAD=24`; green receipt `.ufo/waves/round-46/integrate/c1-landing.txt` | scratch only — `tempfile.mkdtemp` under `--work`/`$TMPDIR` plus one empty sibling directory, both removed in a `finally`; `strace` runs on the host outside the sandbox with its log under the scratch root; lane bytes never written (clean clone `git status --porcelain` empty after the run) | kengaku |
| `round46-c2` | gate | `python3 plans/round46_c2_verify.py --lane .` (`--work DIR` scratch parent, created if absent; the clone needs base revision `64ba8385` in its history for leg A) | `0` pass (`checks=4 defects=0` then `PREDICATE C2 pass`; measured at tip `1315234b`: `PINS total=3 mismatched=0`, `A anchorline live=0 repaired=8 base_rows=149 base_missing=0 base_changed=0`, `B predictor states=16 grader_pass=10 grader_fail=6 disagree=0`, `C entry source_ranges=9 source_ranges_bad=0 errata_marks=5/5`, `D selftest exit=0`) · `1` fail — any `A`–`D` leg printing `DEFECT` (a leg that raises is a defect), `PINS … mismatched=<n>`, or a pinned tool off its freeze digest (`SETUP a pinned tool is not at its freeze digest` on stderr) · `2` is declared in the docstring but not implemented: every setup failure returns 1, and an unknown flag is rejected by argparse with 2 | no self-test of its own — no `--selftest` flag exists (measured: argparse exits 2 on it); leg D is the red-fixture leg and requires `plans/anchor_line_check.py --selftest` to exit 0 | sha256 pins in code: `plans/anchor_line_check.py` `35d02dc55393bea18787e35cc2827cbab65f2d645b81a3c1946722065a4fdedf`, `plans/round45_c2_verify.py` `ab6825e34596ba71f59a184a59fd4e672fd22dcf4b892c511cae5ead2b104f50`, `corpus/evidence/round45/tb2-password-recovery/test_outputs.py` `2dc14fc180734b6fbb0ee00f27c4f866071247b57a2217f579465ff8ed3bfc9e`; base revision `64ba8385ea10af1b78d367dcb242b92d97062af7` for the SOURCES base-row comparison (cells 7, 9, 10 mutable only); 16 frozen newline state shapes and the 5 errata marks in code | none in the lane — writes only a temp dir under `--work`/`TMPDIR` (leg B's `app/`, `tests/`, `states.json`, `grade.py`, `predict.py`); leg A's `git show` and the `anchor_line_check` import are read-only; leg B runs the captured grader and the entry predictor under bubblewrap via the pinned round-45 sandbox helpers; no network | kengaku |
| `round46-c3` | gate | `python3 plans/round46_c3_verify.py --lane .` (`--work DIR` scratch parent, created if absent; `--filler` measures the `plans/filler46/` control package; V6 shells to the host-absolute `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`) | `0` pass (`checks=13 defects=0` then `PREDICATE C3 pass`; under `--filler` it runs V3, V4, V6, V7, V9, V10, V12 against the do-nothing control package and is expected red — measured `checks=7 defects=6` (V3 ok; V4, V6, V7, V9, V10, V12 DEFECT), `PREDICATE C3 fail`, exit 1; a green `--filler` run would mean the content legs admit a do-nothing package) · `1` fail — any `Vn DEFECT <note>` (a leg that raises is a defect), `PACKAGE unreadable: …` (every leg except V13 then defects), or `FILLER unusable: …`; measured in the C2ExecRowFacts clone (default mode, exit 1 in 3.87 s): `V1 ok listed=8 wrong=0 extra=0`, `V2 DEFECT spec=frozen gate=frozen gate_exit=1` (in a clean clone at 87301ba the gate's `P8` fires on `knowledge files=55 index rows=54`, the round-36 W4 drift; `P9` reports `untracked=0`), `V7 DEFECT rows=5 tags=7 …`, `V8 DEFECT order_exit=1 result=not-PASS`, `V11 ok states=60 grader_pass=15 grader_fail=45 disagree=0`, `V13 ok filler_checks=7 defects=6 substantive=V4,V7,V9,V10,V12`, then `checks=13 defects=3` and `PREDICATE C3 fail` · `2` is declared in the docstring but not implemented: no code path returns 2 | no self-test of its own — no `--selftest` flag exists (measured: argparse exits 2 on it); the frozen red control is the committed do-nothing package under `plans/filler46/`, and V13 requires at least three of V3, V4, V7, V9, V10, V12 to print DEFECT on it | eight captured file digests in code (for example `test_outputs.py` `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec`); `plans/pkg-spec-r46.json` `560c7bfb3f12fcfeaed6cb33ed3adc4b881b59b1c8f5ca9e3a094f10c1513f6e` (its `receipt_sha256` masked), `plans/pkg_gate.py` `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`, `plans/polyglot_c_py_probe.py` `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`, dry table `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536`; 13 legs V1–V13 frozen in code | none in the lane — writes only the temp dir under `--work`/`TMPDIR` (an effective spec plus V11's per-run states, grader copy and predictor block); V2 runs `plans/pkg_gate.py package --rerun --require-clean-tree`, which executes the graded program probe and cannot pass on a dirty tree, and the script's docstring reserves V2 for post-stage-2 runs rather than wave-1 seats; V11 runs the captured grader and the entry predictor under `/usr/bin/bwrap`; no network | kengaku |
| `round50-c1` | gate | `python3 plans/round50_c1_verify.py --lane . --work DIR` (`--work` must already exist — measured: an absent parent raises `FileNotFoundError` from `mkdtemp`; `--fence PATH` swaps the fence under test; `--skip-mutants` and `--allow-dirty` are labelled testing-only) | `0` pass (`REV <40-hex>`, `TREE dirty=0`, `POPULATION fixtures=126 pin=b5197f94… mismatched=0 build_errors=0`, `HONEST fixtures=126 admitted=126 refused=0 error=0`, `REFUSALS total=20 clean=20 leaked=0`, two `SEALED total=12 clean=12 leaked=0` and `SEALED total=20 clean=20 leaked=0` lines, `MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met`, then `PREDICATE R50-C1 pass`) · `1` fail — any leg short of its frozen count, `TREE dirty=<n>` in default mode (measured at tip `1315234b` with 4 untracked wave files: every other leg green and the predicate still `fail` on that line alone), `POPULATION-MISMATCH`, `HONEST-REFUSED`, `MUTANT survived`, `verdict=unmet` · `2` setup (`SETUP missing <rel>` for the fence, population, builder or round-44 counter) | no self-test of its own — no `--selftest` flag exists (measured: argparse exits 2 on it); the instrument's own battery is the 15 inline-diff mutants in `plans/mutants50/c1-mutants.json` (measured `caught=15 broken=0`) against the frozen floor of 12 caught, and `--skip-mutants` / `--allow-dirty` are the labelled testing-only selectors | population pin `b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69` over `plans/honest50/population.txt`; frozen literals `HONEST_TOTAL=126`, `MUTANT_MIN=12`, `REFUSALS_TOTAL=20`, `SEALED46_TOTAL=12`, `SEALED50_MIN=6`; the docstring's predicate sentence says `MUTANTS total=23` while the committed mutants file carries 15 and the leg enforces only total>=12 and caught>=12; fence digest printed and never pinned (measured `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`) | none in the lane — builds every fixture as a fresh git repository under the `--work`/`TMPDIR` tree in a random per-module parent padded with 8 decoy siblings, applies each mutant patch to a copy of the fence, and decides one verdict per fixture in a separate `python3 -I` process with a scrubbed env (verdict carried in the exit status); no network | kengaku |
| `round50-c2` | gate | `python3 plans/round50_c2_audit.py --lane .` (lane root; `--selftest`) | `0` every pointer and hash resolves (`POINTERS total=292 paths=228 hashes=64 resolved=292 exists=216 superseded=3 never-landed=9 unresolved=0`, measured at tip `1315234b`) · `1` any unresolved pointer or hash (`UNRESOLVED <path>`, `UNRESOLVED-HASH <hash> missing` or `not-ancestor`) · `2` setup (`SETUP missing SCORECARD.md` or another scanned file, or an audit result that is not an int) | `python3 plans/round50_c2_audit.py --selftest` — appends a bogus pointer to a scratch copy and requires the pristine copy green plus the bogus pointer the only new unresolved (`SELFTEST pristine_rc=0 bogus_rc=1 new_unresolved=['plans/round50_selftest_bogus.py'] verdict=ok`, measured exit 0) | the three scanned files `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md` and the extension set (`md`, `py`, `json`, `jsonl`, `txt`, `patch`, `whl`, `sh`, `json5`, `tres`) frozen in code; corrections read only from `SUPERSEDED <pointer> -> <target>` rows; before-count 12 unresolved pointers at `71f5f5f`; no digests | none in the lane — read-only git plumbing (`rev-parse`, `log --all`, `cat-file -e`, `merge-base --is-ancestor`); `--selftest` writes only its own mkdtemp tree (symlinks to the lane plus a local `git init` and commit there) | kengaku |
| `round51-routing` | gate | `python3 plans/round51_routing.py --lane . --run-checks` (`--ledger PATH`, `--scratch DIR` keeps the scratch, `--selftest`; without `--run-checks` the `fixed-verified` checks are counted but not executed) | `0` `PREDICATE R51-C2 pass` (measured at tip `1315234b` without `--run-checks`: `LEDGER corpus/routed-findings.jsonl rows=75`, 75 complete, 75 attributed, 75 sources resolved, `VERIFIED ran=0`) · `1` fail — any `  DETAIL <LEG>` line under PARSE, FIELDS, OWNER, DISPOSITION, SOURCE, CHECK, CHECK_FAILED, CLOSE_REF or NEXT (an unreadable ledger raises and exits 1 as well) · `2` argparse usage only (measured `--bogus` → exit 2); the script declares no setup exit; an absent `--ledger` path raises `FileNotFoundError` with exit 1 (measured) | `python3 plans/round51_routing.py --selftest` — 11 frozen ledger cases on a temp lane (8 red: missing owner, foreign owner, bad disposition, absent source, empty check, failing check, absorbed routed row with no next, unresolvable close; 3 green: the baseline row, a properly routed row, a resolvable close), measured `[selftest] cases=11 failures=0` and `ALL PASS`, exit 0 | field set, status set, disposition set and the fallback owner set frozen in code; the ledger `corpus/routed-findings.jsonl` (75 rows at the tip); owner universe = fallback set plus `shokunin.conf` lane rows plus every `*-shokunin` directory beside the lane; no digests | runs each `disposition=fixed-verified` row's `check` through `bash -lc` with cwd = lane, `TMPDIR` = scratch and a 90 s timeout, so the ledger text decides what executes; the script itself writes only a mkdtemp scratch (kept with `--scratch`); the ledger `check` strings it runs under `--run-checks` execute with cwd = lane and are not sandboxed, so any write is the row's command (none at 87301ba: 41 ran, 41 passed, clean tree); `--selftest` writes only its own temp tree; no network of its own | kengaku |
| `round51-surfaces` | gate | `python3 plans/round51_surfaces.py --lane .` (lane root; `--manifest PATH` default `plans/round51-surfaces.json`, `--province PATH` default `PROVINCE.md`, `--selftest`) | `0` frozen predicate holds — every problem counter `0` and `RESOLVE … verdict=met`, then `PREDICATE R51-C1 pass` (measured at tip `1315234`: `ANCHORS total=20 dup=0 missing=0`, `PROBES run=20 present=14 absent=6 errors=0`, `RESOLVE observed_present=14 floor=13 verdict=met`, exit 0) · `1` any of DRIFT, STALE, UNVERDICTED, NUMBER-DRIFT, ANCHOR-DUP, ANCHOR-MISSING, UNCOVERED, SECTION-MISSING non-zero or `RESOLVE … verdict=violated`, each defect on a `DETAIL <KEY> …` line, then `PREDICATE R51-C1 fail` (`plans/round51_surfaces.py:219-226`) · `1` also when the manifest cannot be evaluated — an absent manifest path is a `FileNotFoundError` traceback with no `PREDICATE` line (measured, exit 1) and an unknown `probe.kind` prints `unknown probe kind '<kind>'` (`:139`, measured exit 1); a could-not-evaluate never prints `pass` · `2` argparse usage only (`:345-348`, measured `--bogus` → exit 2) | `python3 plans/round51_surfaces.py --selftest` — nine fixtures S0–S8 on one `tempfile.mkdtemp` that honours `TMPDIR` (`:352`): consistent pass, prose drift, stale manifest, unverdicted absent row, number drift, uncovered row, duplicate anchor, floor violated, missing anchor; measured `[selftest] cases=9 failures=0`, `[selftest] ALL PASS`, exit 0 | nothing pinned in code — the manifest is read by path. `plans/round51-surfaces.json` carries 20 entries in 2 sections with `resolve_floor 13`, and the per-surface values the probes compare: sha256 prefix pins `grader.py 90c87c88`, `plans/attrib_probe.py 489f938a`, `~/.local/share/ds-flash-shim/shim.py 42d86d99` (prefix match, `h.startswith(pin)` at `:108`, so a short pin accepts any digest with that prefix); `count` probe `SOURCES rows` over `corpus/SOURCES.md`; `http`/`port` targets `127.0.0.1:34113`, `127.0.0.1:45669`, `127.0.0.1:1234`, `127.0.0.1:8791` | writes no lane byte — reads `PROVINCE.md`, the manifest and every probed target; `--selftest` writes only its one `mkdtemp` dir and `rmtree`s it (`:352-358`); the `http` and `port` probe kinds open `urllib.request.urlopen(url, timeout=3)` or a 1.5 s socket connect to the manifest's loopback URLs (`:116`, `:126`); one `git -C <lane> rev-parse master` for the `REV` line (`:51`); no other network | kengaku round 51 |
| `round52-c1` | gate | `python3 plans/round52_c1_grader_audit.py --lane .` (lane root; `--selftest`) — the whole-benchmark grader-vacuity triage for Terminal-Bench 2.0: classifies each of the 89 frozen tasks' primary grader and prices the confirmations | `0` `PREDICATE R52-C1 pass`: `CAPTURES expected=184 present=184 mismatched=0`, `TASKS total=89 records=89 classified=89`, `CONFIRMED new>=2`, `PRIOR-ART ok=True` (>=3 distinct URLs) · `1` fail on the literal frozen predicate, with every leg printed first (`TASKS`, `CAPTURES`, `CLASS V1 V4 V2 V3 V0`, `TESTCLASS`, `CANDIDATES` then one `  CANDIDATE` line each, `CONFIRMED` with a `  REJECTED <task> <reason>` line per refused receipt, `PRIOR-ART`, `LABELS agree=<a> of <t>` which is evidence and not a leg) — measured on the live lane at HEAD `87301ba` before `confirmations.json`, `prior-art.md` and `labels.json` existed: `TASKS total=89 records=89 classified=88`, `CAPTURES expected=184 present=183 mismatched=0`, `CLASS V1=2 V4=0 V2=53 V3=31 V0=3`, `TESTCLASS presence_only_tests=33 tasks_with_presence_only=27`, `CANDIDATES total=29`, `CONFIRMED new=0`, `PRIOR-ART ok=False urls=0`, `PREDICATE R52-C1 fail`, exit 1; with `sanitize-git-repo/tests/test_outputs.py` operator-excluded (Amendment A5) the literal predicate cannot pass at this tip, and the additive trailer lines `A5 EXCLUDED listed=1 digest_pinned=1`, `A5 CAPTURES present+pinned_excluded=184 of 184`, `A5 TASKS classified+excluded=89 of 89`, `PREDICATE R52-C1-A5 pass` or `fail` price that exclusion but never change the exit code, which follows the literal `PREDICATE R52-C1` line · `2` setup: `SETUP plans/round52-tasks.json missing` (measured with `--lane /nonexistent`); argparse usage also exits 2 | `python3 plans/round52_c1_grader_audit.py --selftest` (measured `SELFTEST classify cases=4 failures=0`, `SELFTEST classify_test cases=4 failures=0`, `SELFTEST cases=6 failures=0`, exit 0; covers the file-level classes V1–V4 on four bodies, the per-test classes P1/P3/P2/P0 on four blocks, and the prior-art leg's absent-file and three-URL cases; limit: it does not exercise the capture count, the digest check, the CONFIRMED hardening (new-task, candidate and verbatim-quote checks) or the A5 trailer, which are re-derived only by the live run and by the round-52 controls `c1-control-*` under `.ufo/waves/round-52/claims/`) | population `plans/round52-tasks.json` (repo `harbor-framework/terminal-bench-2`, pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, `task_count` 89, `capture_file_count` 184) and the per-capture digests in `corpus/evidence/round52/graders/SHA256SUMS` (184 lines); frozen marker regexes `PRESENCE`, `CONTENT`, `BEHAVIOUR`, `VALUE`, `BEHAV_T` in code; candidate = a task with at least one P1 test or a V1/V4 file class; thresholds `CONFIRMED new>=2` and `PRIOR-ART urls>=3`; the never-read set is derived from the 12 `corpus/knowledge/tb2-*-grader.md` filenames (`git-webserver` mapped to `configure-git-webserver`); receipts read: `corpus/evidence/round52/confirmations.json`, `prior-art.md`, `labels.json`; A5 exclusion `graders/EXCLUDED.md` naming sha256 `57e4904177acac5807b51f7c32444bde1968ba0445855fa4333d9eb73865b59e` for the one absent capture | none — reads committed lane bytes only and writes nothing; no network, no git call, no subprocess; `--selftest` writes only a `tempfile.TemporaryDirectory` that it removes | kengaku round 52 |
| `round52-c2` | gate | `python3 plans/round52_c2_registry.py --lane .` (lane root; `--selftest`) — every advertised verdict instrument has a registry row: the five legs MISSING, INCOMPLETE, ENTRY-MISSING, SELFTEST-UNBACKED and DUPLICATE (Amendment A6: escape-aware cell split, duplicate row names fail) | `0` `PREDICATE R52-C2 pass`: `MISSING 0`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 0`, `DUPLICATE 0` (measured at the round-52 landing tree after the wave-2 row corrections: `ADVERTISED total=74`, `REGISTERED total=74 rows=76`, `DUPLICATE 0`, exit 0; `rows` counts the header line and the unparsed `coverage-census` row too, so it exceeds `REGISTERED`) · `1` fail, each defect on its own line (`  MISSING <path>`, `  INCOMPLETE-ROW <name>`, `  ENTRY-MISSING <path>`, `  SELFTEST-UNBACKED <name>`, `  DUPLICATE-ROW <name>`) then `PREDICATE R52-C2 fail` — measured at the base tip `30801b47`: `ADVERTISED total=72`, `REGISTERED total=44 rows=46`, `MISSING 28`, `SELFTEST-UNBACKED 1` (`order-check`, the Amendment A3 false positive), exit 1 · `2` setup: `SETUP no SKILL.md under <lane>` (measured with `--lane /nonexistent`); argparse usage also exits 2 · limits read off the code and measured: a table line is kept only if splitting it on every pipe character yields exactly 8 cells, so a row carrying an escaped pipe (the pre-round-52 `gate-flip-check` row has one in its verdict cell, between `fired` and `not fired`) is dropped without a message; the entry regex needs a `python3 plans/<name>.py`, `python3 corpus/evidence/<dir>/<name>.py` or `python3 grader.py` token with `[A-Za-z0-9_]` only, so a script under a hyphenated evidence directory (`coverage_census.py` under `round13-coverage/`) is outside the advertised universe | `python3 plans/round52_c2_registry.py --selftest` (measured `SELFTEST ok clean-fixture`, `SELFTEST ok missing-fixture`, `SELFTEST ok incomplete-fixture`, `SELFTEST cases=3 failures=0`, exit 0: three temp trees — a clean registry passes, a dropped row raises MISSING, a blank cell raises INCOMPLETE; limit: no fixture exercises ENTRY-MISSING or SELFTEST-UNBACKED, which are exercised only by the live run and by the round-52 controls `c2-control-*` under `.ufo/waves/round-52/claims/`) | frozen universe in code: command regex `python3` followed by `plans/<name>.py`, `corpus/evidence/<dir>/<name>.py` or `grader.py`, depth 1 under `plans/`; scanned files `SCORECARD.md`, `SKILL.md`, `LOG.md`, `corpus/README.md` and every `corpus/knowledge/*.md`; registry block = `SKILL.md` from the heading `## Gate/probe registry` to the next `## `; eight cells per row with none empty; a self-test cell counts as unbacked only when it names exactly one script and a `--flag` that script's bytes lack, and a flag negated by `no … --flag` within 24 characters is ignored (Amendment A3); base-tip receipt `.ufo/waves/round-52/claims/c2-before.txt` | none — reads committed lane bytes only and writes nothing; no network, no git call, no subprocess; `--selftest` writes only a `tempfile.TemporaryDirectory` that it removes | kengaku round 52 |
| `routed-findings` | gate | `python3 plans/routed_open.py --lane .` (lane root; `--file PATH` default `corpus/routed-findings.jsonl`, `--list`, `--observe`, `--timeout N` default 180 s, `--selftest`) | `0` every row valid, then `ROWS total=<n> open=… blocked=… closed=… refused=…` and `routed_open=<n> oldest_round=<r or ->` (measured at tip `1315234`: `ROWS total=75 open=31 blocked=1 closed=41 refused=2`, `routed_open=32 oldest_round=39`, exit 0) · `1` one `DEFECT line=<n> <reason>` per invalid row then `ROWS total=<n> invalid=<k>`, and the `routed_open=` line is withheld so a round close cannot quote a number off a broken file (`:226-230`; measured `DEFECT line=1 a closed row must carry closing evidence in close`, exit 1) · `1` also on any `--observe` mismatch — `OBSERVE <id> rc=… observed=… self=… MISMATCH` then `OBSERVE rows=<n> mismatched=<k>` (`:154-160`; measured at 87301ba in a clean clone: `OBSERVE rows=75 mismatched=43`, exit 1 with `LANE` unset, `mismatched=12` with `LANE` exported; host-state dependent, since the checks read host paths, loopback ports and `${LANE:?}`) or a failed `--selftest` · `2` setup: `--lane` not a directory (`:216`), a file named as a defect ledger — `corpus/defects*.jsonl` refused by name (`:48-50`, `:218-221`; measured `SETUP refusing defects.jsonl: …`, exit 2), the findings file missing (`:224`; measured exit 2), argparse | `python3 plans/routed_open.py --selftest` — 11 row cases plus a defect-ledger guard, all on `tempfile.TemporaryDirectory`: valid-closed, malformed JSON, missing key, duplicate id, closed without evidence, blocked without blocker, bad status, source past EOF, source missing file, bad opened_round, bad id; measured `SELFTEST 12/12`, exit 0 | nothing pinned in code; the population is the named JSONL (default `corpus/routed-findings.jsonl`), measured at tip `1315234`: 75 rows (75 `ROW` lines under `--list`), open 31 · blocked 1 · closed 41 · refused 2, `routed_open=32 oldest_round=39`. Schema literals in code: `STATUSES = open, closed, refused, blocked`; `REQUIRED = id, class, source, opened_round, status`; `ID_RE = [A-Za-z0-9][A-Za-z0-9._-]*`; `SOURCE_RE = <lane-relative path>:<line>` checked against real lane bytes | writes no lane byte — it reads the JSONL and every `source` file it validates. `--observe` runs each row's own `check` string through `subprocess.run(shell=True, cwd=<lane>, timeout=<--timeout>)` (`:148-149`), so any write there is the row's command, not the tool's; `--selftest` writes only inside its temp dir (`:167`, `:187`); no network, no commit, never reads or moves the pinned `corpus/defects*.jsonl` | kengaku round 41 rider (`considerthese/2026-10-26.md` proposal 1) |
| `tb2-grader-probe` | probe | `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` (the captured grader imports Biopython, which `test.sh` pins to 1.85; `--lane` is the only flag) | `0` every frozen prediction matched: `cases=18 observed_pass=5 observed_fail=13 mismatches=0` (measured at tip `1315234` under biopython 1.85, exit 0) · `1` `mismatches>0`, reported on the summary line (`:163-164`) · `2` the captured grader is not at its pin — `REFUSE grader digest <h> != pinned 44a05a24…` (`:142-144`; measured with one appended comment line: `REFUSE grader digest 70ad2697… != pinned 44a05a24…`, exit 2) — and argparse usage (`:136`; measured `--dry` → `unrecognized arguments: --dry`, exit 2) · limit: a missing Biopython is a traceback under exit `1` (`ModuleNotFoundError: No module named 'Bio'` at `:145`, measured exit 1), not `2` | no `--selftest` in the script — only `--lane` is accepted (`:136`), so this row claims none; the probe is the frozen instrument and its verification is external: the committed receipt `corpus/evidence/round35/tb2-grader-probe.txt` (sha256 `2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8`) re-runs byte-equal (measured today: `diff` empty, `BYTE-EQUAL`), and `plans/pkg_gate.py` `--rerun` byte-compares that receipt to the pin in `plans/pkg-spec-r35.json` | grader `corpus/evidence/round35/tb2-eval/test_outputs.py` sha256 `44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582` (`:24`, checked before the grader is imported); TB2 pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; the five literal components read out of the grader source (aa lengths 8, 259, 158, 235, 182 → `max_passing_nt=2766` against the grader's 3000 nt cap); 18 synthetic cases with predictions written from a static reading before the first run | writes only its own `tempfile.TemporaryDirectory` (`:122`) and monkeypatches the grader's `Path` so the hard-coded `/app/gblock.txt` resolves there; imports the captured grader through `importlib`; no network, no model, no container, no task certification, never the live `/app` | kengaku round 35 |
| `round53-c1` | gate | `python3 plans/round53_c1_triage.py --lane .` (lane root; run it on a clean clone of the landing tip, ideally under `bwrap --unshare-net` because it imports the frozen classifier `plans/round53_c1_classify.py`; `--candidates` lists the never-read tasks with a v2 P1 test and prints no predicate; `--selftest`) — Terminal-Bench 2.0 presence-only grader triage v2: five legs PINS, FREEZE, ORACLE (with ORACLE-CONTROL), CONFIRM, PRIOR-ART | `0` `PREDICATE R53-C1 pass` · `1` `PREDICATE R53-C1 fail`, each leg printing its own line (`PINS …`, `FREEZE …`, `ORACLE …`, `ORACLE-CONTROL …`, `CONFIRM …`, `PRIOR-ART …`) and one `  REJECTED <task>:<reason>` line per refused receipt; an unavailable base tip prints `BASE-TIP-UNAVAILABLE` and fails closed · exit `2` is not emitted (a setup problem surfaces as a failing leg or a traceback) | `python3 plans/round53_c1_triage.py --selftest` prints `SELFTEST cases=<n> failures=0` (forged-complete routes of round 52 and of the wave-1 attacks as named cases: shrunk population, stub capture, `confirmed:"false"`, labeller as reader, report or archive outside its directory, header URL mismatch, sweep of one file twice, classifier or freeze edited after the freeze, labels committed before the freeze, all-P1 classifier with copied labels) | digests in the script: `plans/round52-tasks.json` `0230b68c…`, `corpus/evidence/round53/pin-tree-2fd12b88.json` `96b47248…`, `tests-index.json` `579d567f…`, control module `plans/round52_c1_grader_audit.py` `0b1d4213…`; excluded capture blob `3269e74e…`; the eight label-seat files and shards pinned in `plans/round53-c1-freeze.json`, committed after the classifier | none — reads committed bytes and git history; the selftest builds fixture repositories under `$TMPDIR` | kengaku |
| `round53-c2` | gate | `python3 plans/round53_c2_tipstate.py --lane . --source <clean git clone of the landing tip> --work <scratch>` (`--jobs N` default 4, `--timeout S` default 900, `--dry` static legs only with no predicate, `--only A,B` runs a subset and never passes, `--selftest`) — every registry row has a declared tip-state in `plans/round53-tipstate.json` that the counter re-executes | `0` `PREDICATE R53-C2 pass` after `ROWS registry=<n> ledger=<n> missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok`, `SOURCE rev=… clean=yes lane_rev_equal=yes`, `RUN executed=<n> timeout=0 mismatched=0 evidence_missing=0` and `TIPSTATE declared_green=… declared_red=… observed_green=… observed_red=…` · `1` `PREDICATE R53-C2 fail` with one line per defect (`MISSING`, `EXTRA`, `ENTRY-MISMATCH`, `BAD-DECL`, `BAD-REASON`, `BAD-NAME`, `DUPLICATE`, `TIMEOUT`, `MISMATCH <row> declared exit=… observed exit=…`, `EVIDENCE-MISSING`) · `2` `SETUP` (no `SKILL.md`, or `--source`/`--work` missing without `--dry`) | `python3 plans/round53_c2_tipstate.py --selftest` prints `SELFTEST cases=<n> failures=0` (forged all-green, all-red, a shell wrapper or `python3 -c pass` as argv, a renamed or doubled heading, deleted rows, a source older than the lane, a non-git or dirty source, an environment token visible to a row, duplicate JSON keys) | row set pinned by digest `df38a8fc…` of the 75 frozen names plus `round53-c1`/`round53-c2`; ledger `plans/round53-tipstate.json` (schema `r53-tipstate-v1`); at most 10 % of rows may be `help`-kind | scratch under `--work`/`$TMPDIR` (a shared clone per worker, reset between rows; credential-shaped environment variables removed from every row) | kengaku |
| `stage-scan` | gate | `python3 plans/stage_scan.py PATH...` (files or directories; `.git` is not entered, symlinks are not followed, files with a NUL in the first 8 KiB or over 5 MiB are skipped and reported; `--selftest [--tmp DIR]`) — a pre-stage credential-pattern scan: run it over everything about to be committed, because a fake token inside a captured upstream test blocked the round-52 push (GH013) | `0` `SCAN files=<n> skipped=<n> hits=0` · `1` one `HIT <path>:<line> <rule> prefix=<4 chars>` line per match (the matched bytes are never printed), then the `SCAN` line · `2` setup error (no argument, missing or unreadable path — a scan that could not read never prints 0) | `python3 plans/stage_scan.py --selftest` prints `SELFTEST cases=<n> failures=0` (every rule positive, near-miss negatives such as a 10-character `hf_` prefix and an in-word `sk-`, a binary file, an oversized file, a nested directory, a skipped `.git`, a symlink, an unreadable file, and a self-scan) | the eleven rules and their regexes live in the script docstring: GitHub token prefixes, fine-grained PAT, Hugging Face, `sk-`/`sk-ant-`, AWS key id and secret, Slack, Google API key, private-key header, a generic quoted secret assignment, and `op://` references; the `generic` rule is the widest and gives false positives on benign key names | none — reads only; the selftest builds fixtures from string fragments under its `--tmp` or `$TMPDIR` | kengaku |

Round-43 registry addendum: `gate-flip-check` is the first row whose input is a **lesson** rather than a
package, a capture or a receipt: it reads one `## Gate` section, keeps the refusals that state a flip
condition (`Flip:`, `flips when`, `if … admit`, or a companion bullet naming a refused candidate), and
requires each to be resolved by a later line of the same file. It is red on the landing tip by
construction — 45 obligations in 18 lessons, none resolved (`.ufo/waves/round-43/build/R43FlipCheck/sweep.txt`)
— so wire it as a forward gate from round 43, never as a claim that the corpus is clean. Its verdict is a
recorded sentence, not an executed consequence: a `fired` line with the wrong evidence passes, which is
the limit the criterion (draft `QUALITY-Q35`) names. First instance closed by the tool: round-42 D3
(`corpus/lessons/round-42.md:44`, `corpus/lessons/round-42-verifier-spotcheck.md:37-42`).

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

Round-42 registry addendum (rows drafted and verified by wave-1 `R42RegistryRows`; L1 integration): `round42-c1-mutants`
is the round-41 counter's shape re-pointed at the two tools round 42 leaves unedited (`anchor_digest_check.py`,
`order_check.py`) with 14 frozen round-40 near-variants, the five `F41C1Hardened` repairs and a new **attribution** leg:
a direction hit counts only when a traced re-run on the killing fixture reproduces the result *and* executes a line of
the replaced span, so `unattributed=<n>` is a failure the counter can print (`control-c1-attribution.txt`). Limit,
measured in wave 1 (`R42CritAttribution`, `R42CritC1Counter`): for mutants whose replaced line runs on every invocation
(module-level regexes, the argparse default, an unconditional clause) the span check is vacuous, and a dishonest
battery reached the predicate with three substitute fixtures — so the counter certifies directions, not intent, and a
non-author review of `plans/battery42` stays part of admission. `round42-c2` is the round-41 counter's V1–V8
re-pointed at the `circuit-fibsqrt` package plus **V9 content** (the entry's `## Case table` equal to the receipt row
by row, every row id outside its `source:` line, PROVINCE naming the task and the entry, README `## Frontier` naming
the task); its gate leg re-runs the probe (≈62 s), and its P10 leg needs a writable `~/.cache` for `uv` (inside a
read-only-home envelope, overlay the cache from scratch: `.ufo/waves/round-42/integrate/envelope.sh`). `fibsqrt-probe`
is a `probe` row of the `constraints-probe` shape: `mismatches=` is a data line, never the exit code.

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

## Simulator-executed data-artefact TB2 grader — round 42

Before citing the pinned TB2 `circuit-fibsqrt` scorer, run `python3 plans/fibsqrt_probe.py --lane .` and read its
summary line: exit `0` means only that all 16 cases produced three test verdicts twice each — a prediction mismatch
does not change the exit code, it is printed on the summary line, and exit `2` is a setup failure (duplicate or
malformed case id, unknown tag, malformed prediction, a graded list that is not 28 long, a capture missing or off its
pinned digest, `/usr/bin/bwrap`, `python3`, `bash` or `gcc` not executable, an uncreatable `--work`, or a case that did
not yield three verdicts twice). `--dry` and `--stage-check` are not evidence. The receipt's summary
(`corpus/evidence/round42/fibsqrt-probe.txt:24`) reads `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, and a
second, same-process grading of each un-rebuilt end state agrees case by case (`regrade cases=16 differ=0`).

The class is new: the graded artefact is a **program in a data format**, and the interpreter that executes it is
owned by the grader. `/app/gates.txt` is a list of `outX = …` gate lines (`instruction.md:1-7`); test 3 compiles the
task's own simulator at grading time (`gcc -O3 /tests/sim.c -o sim`, `tests/test_outputs.py:65-67`) in the cwd —
the image `WorkingDir=/app`, which Harbor's verifier keeps (wave-1 `R42ScoutHarborCwd`) — so `./sim` and the
`/app/sim` it then runs are the same file only because of that cwd. The simulator reads `gates.txt` **relative to its
cwd** (`sim.c:319`), skips lines whose first scan as `out%d = <op>` fails (`sim.c:113-115`), keeps a scanned line
whose operator matches no form as a constant-0 gate (`sim.c:9`, `:126`, `:156`; `R42CritProbe` D1), sets signals
0-31 from `strtoul(argv[1], …)` (`:324`, `:330`), runs exactly 32000 steps (`:335`), and prints bits 0-31 of the 32
**highest-indexed** signals (`:342-345`) — three points where `instruction.md:8-9` says stdin, "the last 32 lines"
and an unnamed bit order.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| `Path("/app/gates.txt").exists()` (`test_outputs.py:7-11`) | anything that exists, including a **directory** — `gates-is-directory` passes test 1 and fails tests 2-3 (`PFF`) | `is_file()`, not `exists()`; the size test rejects a directory by raising | `gates-is-directory` (receipt:22), `no-gates-file` (`FFF`, receipt:9) |
| `sum(1 for line in f) < 32000` over the whole file (`:14-23`) | exactly 31999 lines, blank padding included (`lookup-28-padded-31999` `PPP`); 32000 fails **only** this test (`PFP`) | count every line, blanks and comments included; `sim.c` ignores both | `lookup-28-padded-31999` (receipt:15), `lookup-28-padded-32000` (receipt:16) |
| `gcc -O3 /tests/sim.c -o sim`, then `/app/sim N` (`:65-67`, `:119`) | the grader's own compile: a planted executable `/app/sim` printing the right answers is overwritten (`fake-sim-script` `PPF`) — under the verifier's cwd `/app` only | which file the binary came from; the cwd the verifier uses | `fake-sim-script` (receipt:21), `oracle-solve-sh` (`PPP`, receipt:8) |
| 28 fixed inputs, largest 48401 (`:73-102`) | a circuit right on exactly those 28 and 0 elsewhere: `lookup-28` is `PPP` at 1195 lines and prints 0 for the instruction's own examples 208 and 20000 | the 28 inputs, not the instruction's examples (prior art for the gap above 48401: S128) | `lookup-28` (receipt:11), `lookup-28-plus-examples` (receipt:13), `lookup-27-drop-48401` (`PPF`, receipt:12) |
| `fibonacci(isqrt(n)) % 2**32` computed **in the test file** (`:26-53`, `:115-117`) | the exact integer; one flipped answer bit at N=41 fails the output test (`PPF`) | recompute `fib` and `isqrt` yourself | `lookup-28-bitflip-41` (receipt:14) |
| `gates.txt` opened cwd-relative and every line whose first scan fails skipped (`sim.c:113-115`) | line order, `#` comment lines and CRLF are free (all `PPP`); `instruction.md:1`'s line form is not checked | that the file is a dependency graph over signal indices; the physical last lines mean nothing | `lookup-28-comment-lines`, `-reversed-lines`, `-crlf` (receipt:17-19) |
| the `out%d = %[^\n]` capture keeps trailing whitespace; the copy branch needs `!strstr(op, " ")` (`sim.c:113`, `:126`) | one trailing space on every line turns every copy line into a constant-0 gate and the printed word into 0 (`PPF`); binary lines are unaffected | strip the line before deciding it scans; an invisible byte flips the score | `lookup-28-trailing-space` (receipt:20) |
| `strtoul(argv[1])`, 32000 steps, result bits from `values[num_signals-32 + i]` (`:324-347`) | the printed word is the 32 highest-indexed signals, not the file's last 32 lines; the shipped 33-line example prints `argv[1] >> 1` | the index arithmetic and the argument, not the prose (`instruction.md:8-9`) | `nop` (`PPF`, receipt:7), `lookup-28-reversed-lines` (receipt:18) |
| nothing — the circuit as logic | a table, not an implementation: `lookup-28` passes 3/3 for a function it does not compute | whether the file *computes* `fib ∘ isqrt`; only 28 outputs are observed | `lookup-28` (receipt:11) |
| `int(result.stdout.strip())` and `returncode != 0` as a failed case (`:121-127`) | fewer than 32 signal indices prints nothing — `int('')` fails the case (`empty-gates-file` `PPF`); a missing file makes `sim` exit 1 (`no-gates-file` `FFF`) | "no output" and "wrong output" are the same verdict | `empty-gates-file` (receipt:10), `no-gates-file` (receipt:9) |
| the task's own oracle and the do-nothing baseline | `oracle-solve-sh` `PPP` (receipt:8); `nop` `PPF` (receipt:7): the shipped example already passes 2 of 3 | run both first: this grader starts at 2 of 3 on its own initial state | `oracle-solve-sh`, `nop` |

V7 labels from the receipt (frozen tags, `corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt:1-7`): `line-form` and
`last-32-lines` `unenforced`; `gates-file` and `line-limit` `enforced` (one or two witnesses — a property of the frozen
case set only); `output-function`, `example-208`, `example-20000` `partly`. Limits: the probe never runs the task image
or a harness; host python3/gcc stand in for the image's; recipes run unprivileged; three cases re-observe shapes graded
before the freeze (disclosed). A property of this capture at `2fd12b88`; not a task-validity, difficulty or
gameability verdict, not solver advice, not a statement about digital-logic design or C semantics in general, and not a
statement about any agent's behaviour. (Draft `R42PkgProse` block d, condensed by the L1.)

## In-process module-import TB2 grader — round 43

Before citing the pinned TB2 `feal-differential-cryptanalysis` scorer, run `python3 plans/feal_probe.py --lane .` and
read its summary line: exit `0` means only that all 12 cases produced two verdicts each — a prediction mismatch does
not change the exit code, it is printed as `match=NO` on the case line and counted in `mismatches=`; exit `1` is a
`--stage-check` failure; exit `2` is a setup failure (duplicate or malformed case id, unknown tag, malformed
prediction, a capture missing or off its pinned digest, `/usr/bin/bwrap`, `python3`, `bash` or `gcc` not executable,
an uncreatable `--work`, or a case whose recipe exited non-zero). `--dry` and `--stage-check` are not evidence. The
receipt's summary (`corpus/evidence/round43/feal-probe.txt:23`) reads `cases=12 observed_pass=8 observed_fail=4
mismatches=0`, and grading each end state a second time in a fresh harness process agrees case by case (`regrade cases=12
differ=0`, `:22`).

The class is new: the graded artefact is an **agent-authored Python module imported into the grader's own
interpreter**. One test function does everything (`tests/test_outputs.py:7-30`): it shells out to build the task's C
extension in `/tests` (`print(os.popen("(cd /tests && python setup.py build_ext --inplace)").read())`, `:20`),
appends `/app` and then `/tests` to `sys.path` (`:22-23`), runs `import attack` (`:24`) and `import feal_in_c` (`:25`),
calls `feal_in_c.create_random_keys()` (`:27`), hands the C `encrypt` to the module (`:29 stolen =
attack.attack(feal_in_c.encrypt)`) and asserts `feal_in_c.get_keys()[5] == stolen` (`:30`). `tests/test.sh:17-25` runs
that one test under `uvx -p 3.13` (pytest 8.4.1, setuptools 80.9.0) and writes `/logs/verifier/reward.txt` from
pytest's exit status — so the module runs in the same interpreter and process as the reference extension, and
`get_keys()` returns the live `uint32_t key[6]` as a six-element list (`tests/feal_module.c:25-43`, method table `:51`).
`create_random_keys()` seeds libc once per process (`srand(time(NULL))` behind a static flag) and derives each key as
`(rand() & 0xFFFF) * 1234567` (`tests/feal.c:56-67`): six 16-bit seeds, which `instruction.md:4-6` states as a hint and
which also makes the key schedule a clock read.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| `sys.path.append("/app")`, then `"/tests"`, then `import attack` (`test_outputs.py:22-24`) | a module that imports the reference implementation and returns its key: `cheat-import-get_keys` passes (`P`) | which module answered; whether the attack did any work | `cheat-import-get_keys` (receipt:15) |
| `feal_in_c.get_keys()[5] == stolen` with `stolen` any object (`:30`) | an object whose `__eq__` returns True passes: `int.__eq__` returns `NotImplemented` for a non-int and the reflected comparison decides the assert (`cheat-always-equal`, `P`) | that the returned value *is* the int — `type(stolen) is int`, or a comparison in the other direction | `cheat-always-equal` (receipt:16) |
| `import attack` runs **before** `import feal_in_c` (`:24-25`) | a module that installs a fake `feal_in_c` in `sys.modules` at import time is what `:25` binds, and every later call goes to the fake (`cheat-sysmodules-shadow`, `P`) | import order and module identity; a private name for the reference, or a fresh subprocess | `cheat-sysmodules-shadow` (receipt:17) |
| the reference module is looked up again **after** `attack()` returns (`:29-30`) | rebinding `feal_in_c.get_keys` to return a constant before returning that constant passes (`cheat-patch-get_keys`, `P`) | attribute identity before and after the call | `cheat-patch-get_keys` (receipt:18) |
| pytest's exit status as the whole verdict (`test.sh:22`, `:25`) | `os._exit(0)` inside `attack()` ends the grader process with status 0, `test.sh` writes reward 1, and the assertion never runs (`cheat-exit-zero`, `P`, `exit=no-verdict-line`) | that a verdict line exists at all — `test.sh:25` writes the reward from the exit status alone, so a process that exits before pytest reports is indistinguishable from a pass | `cheat-exit-zero` (receipt:19) |
| the SAME interpreter's libc rand state, seeded once per process (`feal.c:56-67`) | replaying `srand(time(NULL))` through libc with the current time and filtering candidates against the passed `encrypt` reproduces `key[5]` (`cheat-clock-seed`, `P`, `host=libc-rand`) | whether the "attack" is a clock read; the real entropy is 16 bits per round key | `cheat-clock-seed` (receipt:20) |
| `stolen = attack.attack(feal_in_c.encrypt)` — the call is never timed (`:29`) | the reference attack plus a 45 s sleep passes (`slow-oracle-45s`, `P`) although `instruction.md:3` asks under 30 s; the only bound in the capture is `task.toml:22`'s 1800 s verifier timeout | a wall-clock measurement inside the test; `README.md:35` claims the test confirms the limit and it does not | `slow-oracle-45s` (receipt:21), `README.md:35`, `task.toml:22` |
| the argument is the C `encrypt` bound to the six C keys (`:29`; `feal_module.c:12-22`) | the analysis must target the passed function: the shipped `/app/feal.py` keeps its own `random`-seeded keys (`feal.py:24-29`) and is not the grading cipher; the oracle's differential attack passes (`oracle-solve-sh`, `P`) | which ciphertexts came from — the passed `encrypt_fn`, not the `/app` copy | `oracle-solve-sh` (receipt:11) |
| `import attack` with no `/app/attack.py` (`:24`) | the test errors out (`ModuleNotFoundError`): `nop` fails (`F`), and the shipped `feal.py` alone is not an attack module | that a module exists at `/app/attack.py` with an `attack` callable | `nop` (receipt:10) |
| the asserted value and its type (`:30`) | a wrong int (`wrong-key`), the oracle's result plus one (`oracle-off-by-one`) and the oracle's result as a decimal string (`return-str`) all fail (`F`) | the exact integer; `uint32`, not a string | `wrong-key` (receipt:12), `oracle-off-by-one` (receipt:13), `return-str` (receipt:14) |
| the build at `:20` — printed, never asserted | no case witnesses a build failure: a broken build surfaces only as an `ImportError` at `:25` | the build's stderr; that `setup.py:3-5` names the captured sources | code read only (`test_outputs.py:20`, `setup.py:3-5`) |

V7 labels derived from the receipt (frozen tag lines,
`corpus/evidence/round43/feal-dry-cases-freeze.txt:1-5`: `chosen-plaintext` `instruction.md:1`, `recover-key5` `:1`,
`attack-file` `:3`, `return-uint32` `:3`, `time-30s` `:3`): `attack-file` **enforced** (1 case, 0 pass — `nop`);
`recover-key5` **partly** (7 cases, 4 pass — the three failing key cases plus `cheat-always-equal`,
`cheat-sysmodules-shadow`, `cheat-patch-get_keys`, `cheat-exit-zero`); `return-uint32` **partly** (2 cases, 1 pass —
`return-str` fails, `cheat-always-equal` passes); `chosen-plaintext` **unenforced** (6 cases, 6 pass);
`time-30s` **unenforced** (1 case, 1 pass — `slow-oracle-45s`). Every label is a property of this frozen 12-case set
only, not a reading of the instruction prose.

Limits: the probe never runs the task image (`task.toml:29`, `allow_internet = true` at `:34`, never pulled) or a
harness; host python3, host gcc and host setuptools stand in for the image's python 3.13 under `uvx`, Debian gcc and
setuptools 80.9.0; pytest itself is not run — the harness maps the one test function onto pytest's exit status, so
pytest parity is unverified; recipes run unprivileged; each case stages its own `/app` and `/tests`; the cases are
constructed modules, not agents. `cheat-clock-seed` is a host fact (`host=libc-rand`): the replay works because the
grader's own process seeded libc moments earlier. A property of this capture at `2fd12b88`; not a task-validity,
difficulty or gameability verdict, not solver advice, not a statement about differential cryptanalysis, the FEAL
cipher or Python's import system in general, and not a statement about any agent's behaviour. (Draft `R43PkgProse`
block d; the L1 condenses at integration.)

## Constant-compare TB2 grader — round 44

Before citing the pinned TB2 `feal-linear-cryptanalysis` scorer, run `python3 plans/feal_linear_probe.py --lane .`
and read its summary line: exit `0` means only that every one of the 14 cases produced two verdicts — a prediction
mismatch does not change the exit code, it is printed as `match=NO` on the case line and counted in `mismatches=`;
exit `1` is a `--stage-check` failure; exit `2` is a probe error (a capture missing or off its pinned digest, a
required binary not executable, an uncreatable `--work`, a case whose recipe exited non-zero — a recipe error is
never a verdict). `--dry` and `--stage-check` are not evidence. The receipt's summary
(`corpus/evidence/round44/feal-linear-probe.txt:24`) reads `cases=14 observed_pass=8 observed_fail=6 mismatches=0`,
and grading each end state a second time in a fresh harness process agrees case by case (`regrade cases=14 differ=0`,
`:23`).

The class is new: the graded artefact is an **agent-written text file judged by substring membership**, with no
grader-owned model, interpreter or import in play. `tests/test_outputs.py` holds 100 decimal constants in one
triple-quoted string (`:4-103`) and one test function (`:106-122`) that reads `/app/plaintexts.txt` whole
(`:120 data = open("/app/plaintexts.txt").read()`), then asserts `c in data` for each constant (`:121-122`). That is
membership over the entire file text: no count, no order, no format, no exactness, and no rejection of anything else
in the file. `tests/test.sh:22` runs that one test under `uvx -p 3.13` (pytest 8.4.1) and `:25-26` writes
`/logs/verifier/reward.txt` from the exit status. The expected values are reachable without an attack from the
benchmark repository: the four round keys are literals in `gen.py:12`, `gen.py:19-20` hashes them into the seed and
`:27`/`:61` derive every plaintext as `sha256(seed_hash + counter_bytes)[:8]`, and the constants are in the test file
itself — while the image deletes `gen.py` (`Dockerfile:14`), so those are public files, not image files.
`instruction.md:9-10` names the output file and no format.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| the whole file text, `open("/app/plaintexts.txt").read()` (`test_outputs.py:120`) | the correct numbers joined into one line with no separator passes (`oracle-concatenated`, `P`) | whether a line/record shape was asked for; `instruction.md` asks for no format, so nothing is enforced here | `oracle-concatenated` (receipt:14) |
| `assert c in data` per constant (`:121-122`) — membership only | the correct lines in reverse order pass (`oracle-reversed`, `P`) | a per-line comparison (`data.splitlines()` equality) | `oracle-reversed` (receipt:16) |
| the same membership, nothing else (`:122`) | the correct 100 followed by 100 decryptions under a wrong key pass — two answers per ciphertext (`oracle-plus-decoys`, `P`) | that extra tokens are rejected; nothing in the test reads a count or a second column | `oracle-plus-decoys` (receipt:15) |
| the same membership on decimal strings (`:121-122`) | the correct plaintexts as 20-digit zero-padded decimals pass (`oracle-zero-padded`, `P`); the same values in hexadecimal fail (`hex-output`, `F`) because the decimal constants are no longer substrings | that the number format is the one the task means — the test forgives decimal padding, never a change of base | `oracle-zero-padded` (receipt:17), `hex-output` (receipt:19) |
| 100 constants, each required once (`:121-122`) | all 100 to pass with one dropped fails (`one-missing`, `F`): the conjunction is complete even though nothing else about the file is checked | that each expected value is present — completeness is the only real constraint | `one-missing` (receipt:18) |
| `gen.py:12`'s four round keys, published in the repository | decrypting `ciphertexts.txt` with those keys, no attack at all, passes (`decrypt-public-keys`, `P`) | which key material the answer came from; whether the task's premise (key recovery) was touched | `decrypt-public-keys` (receipt:11) |
| `sha256(seed_hash + counter_bytes)` at `gen.py:27`/`:61`, seed from `gen.py:19-20`, published | recomputing the 100 plaintexts from the hash chain, no key and no decryption, passes (`replay-public-gen`, `P`) | whether the plaintexts are derivable from published bytes — here they are | `replay-public-gen` (receipt:12) |
| the constants themselves, in the published `tests/test_outputs.py:4-103` | copying all 100 constants into `/app/plaintexts.txt` passes (`copy-public-constants`, `P`) | that the expected values are not in the repository the agent can read (they are) | `copy-public-constants` (receipt:13) |
| nothing — no file at `/app/plaintexts.txt` (`:120`) | the test raises `FileNotFoundError` and the case fails (`nop`, `F`) | that the file exists and is the one named at `instruction.md:10` | `nop` (receipt:9) |
| values that are not the constants (`:121-122`) | a round key off by one bit (`wrong-key-decrypt`), the 32 known plaintexts (`pairs-plaintexts`) and `ciphertexts.txt` copied unchanged (`ciphertexts-copied`) all fail (`F`) | that the plaintexts are the decryption of `ciphertexts.txt`, not of `pairs.txt` and not the ciphertexts | `wrong-key-decrypt` (receipt:20), `pairs-plaintexts` (receipt:21), `ciphertexts-copied` (receipt:22) |
| pytest's exit status as the whole verdict (`test.sh:22`, `:25-26`) | the task's own oracle passes (`oracle-solve-sh`, `P`); nothing asserts that an attack file exists, that a key was recovered, or that anything was timed | what the reward actually measures — `README.md:32` states the same membership reading | `oracle-solve-sh` (receipt:10), `README.md:32` |

V7 labels derived from the receipt (frozen tag lines, `corpus/evidence/round44/feal-linear-dry-cases-freeze.txt:1-4`:
`known-plaintext-attack` `instruction.md:7`, `recover-key` `:7`, `decrypt-all` `:8`, `plaintexts-file` `:10`):
`plaintexts-file` **enforced** (1 case, 0 pass — `nop`); `decrypt-all` **partly** (7 cases, 2 pass);
`known-plaintext-attack` **partly** (6 cases, 3 pass); `recover-key` **partly** (7 cases, 3 pass). Every label is a
property of this frozen 14-case set only, not a reading of the instruction prose.

Limits: the probe never runs the task image (`task.toml:29`, `allow_internet = true` at `:34`, never pulled) or a
harness; host python3 and host gcc stand in for the image's python 3.13 under `uvx` and Debian bookworm gcc; pytest
itself is not run — the harness calls the one test function and maps its outcome onto pytest's exit status; the
image's `pip install setuptools==80.9.0` is not replayed; recipes run as the probing user; each case stages its own
`/app` and `/tests`, and `/pub` holds read-only copies of the three public files (`gen.py`, `test_outputs.py`,
`solve.sh`), so a case that reads it models an agent who read the repository; the cases are constructed end states,
not agents. A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not
solver advice, not a statement about linear cryptanalysis, the FEAL cipher or `sha256` in general, and not a
statement about any agent's behaviour.
