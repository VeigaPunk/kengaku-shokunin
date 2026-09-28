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
  `skill(name="min_stack")` — temp-0.2 repro held 9/9, trap is
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

### Running a battery against the local model (verified 2026-09-28)

1. Probe the endpoint, not the config: `GET /v1/models` + `/health` on the
   configured port. `~/.config/opencode` provider `qwen-local` still points
   at `localhost:8080` (now Jitsi — listening but wrong); the live
   llama-server is `127.0.0.1:34113` via `qwen-coder.service`.
   Listening-but-wrong beats closed-port for silent breakage.
2. Two transport paths: `loop.sh` (opencode `--agent raw` — sends the
   raw-agent system prompt + `<env>` + skills catalog ~4.3K tok, plus
   `tools:[janitor_auth,skill]`/`tool_choice:auto` ~400 tok, and NO
   temperature → server default 0.8) or direct `POST
   /v1/chat/completions` (minimal, deterministic-ish, temp 0.2). Grade
   identically: `BENCH_ROOT=<scratch> bash ~/bench-arena/grade.sh <label>`
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

## Hermetic grader (operability gate) — `grader.py`

`grader.py` (repo root; stdlib only; no network, no endpoint) replays the two
committed probe trees against their own stored bytes and recomputes every
number their SUMMARYs assert. Deterministic and PYTHONHASHSEED-independent —
never iterate a set where the result is order-sensitive.

| Tree | Recomputed from committed bytes |
|---|---|
| `corpus/evidence/round8-horizon/` | `meta` regenerated from seeds `700 + pid*13` (incl. the `+977` retry chain) and matched field-for-field; each of the 258 non-meta `raw` strings re-parsed through the shipped `extract_json_block` (fenced block first, brace-regex fallback — 2 r9 records only parse via the fallback) and re-graded against `meta`'s `truth`; B cells re-scored to `outcome` ∈ {corrected, propagated, other} incl. the historical-value `corrupt_from` rule; C cells re-graded via `grade_c` / `valid_latin`; all 11 `run.log` SUMMARY lines |
| `corpus/evidence/round9-replication/` | `meta` from seeds `2000 + pid*29`; the 4-cell table incl. mean final `nwrong` (4/8 · 0.500, 2/8 · 0.875, 2/8 · 1.375, 0/8 · 2.250); the 284-record census (8 `meta` / 248 scored / 28 `filler`); sign tests (math.comb exact binomial), onset ladder, failure classes, ack compliance (32/56 = 57.1%, 48/64 = 75.0%), cross-round table, prediction-scoring table vs `predictions-r9.md`, prediction sha256 chain and the ordering proof (hash time ≤ first `request_ts`) |

| Exit | Meaning |
|---|---|
| `0` | every recomputed value equals the stored one |
| `1` | ≥1 mismatch, each printed `MISMATCH <check-id>: stored=<x> recomputed=<y>` |
| `2` | a required input file is missing or unreadable |

Run `python3 grader.py` (defaults resolve beside the script); inputs overridable
via `--r8-jsonl/--r8-runlog/--r9-jsonl/--r9-md`; md5 pins on the four evidence
files fire only on the default paths, so mutated copies grade without pin
noise. `--selftest` corrupts temp copies only — one flipped stored `ok`, one
edited `run.log` SUMMARY number, one bumped digit inside a `raw` fenced block —
and exits 0 only if all three are caught (exit 1 each) **with their expected
check-ids** (kagi `drift-pins.sh` convention: assert code *and* diagnostic): a
gate that cannot fail on a deliberately broken copy is not a gate.

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
- `/tmp/bench-r7/` scaffold-delta ablation (ephemeral workdir, labelled debt per `../PROTOCOL.md`'s closure-resolvable rule — decisive numbers pasted into the knowledge entry) — verbatim opencode `raw` wire request captured via proxy provider, 5-task × 5-condition ablation (E1/E2/E3/E4 × n=3 + E0 anchor), graded 2026-09-28 → `corpus/knowledge/bench-arena-round7-scaffold-ablation.md`
- `~/bench-arena/` round-5 battery — full 33-task direct-API re-run: 20/33 PASS, 8 status deltas vs v2 (4 P→F, 3 F→P, 1 F→HARNESS_DEFECT), 5 byte-identical sol_sha, 06 truncation (`finish=length` @4096 tok), FAIL slower on wall+tokens (run + graded 2026-09-28 → `corpus/knowledge/bench-arena-round5-battery.md`)
- `~/Projects/webzites/repos/llm-wiki/wiki/karpathy/{talks,projects-and-tools,standards-and-specifications}/**` + remaining `philosophy-and-concepts/`, `gwern-essays/`, `ai/foundations/complexity.md`, `ai/books/` — second digest: sampling-proves-presence, reference-class, autonomy slider, spec-ability tiers (swept+read 2026-09-28 → `corpus/knowledge/eval-design-digest-2.md`)
- `corpus/evidence/round8-horizon/` — round-8 planning-horizon probe, run to completion 78/78 jobs: `horizon.py` (349 lines, md5 `1c157e2a…`), `results.jsonl` (268 records, md5 `df154cb5…`, `raw` restored round 9), `run.log` (SUMMARY block, md5 `fc3b232f…`), `critic-defects.md` (16 design defects) — analyzed 2026-09-28 → `corpus/knowledge/bench-arena-round8-horizon.md`
- `corpus/evidence/round9-replication/` — pre-registered probe-A replication + checkpoint-dose cell: `predictions-r9.md` (sha256 `2a4f62ef…`, hashed before the first request), `ordering.log`, `run_r9.py`, `results-r9.jsonl` (284 records: 8 meta / 248 scored / 28 filler), `replication.md` — run + scored 2026-09-28 → `corpus/knowledge/bench-arena-round9-replication.md`
- `corpus/evidence/round9-fleet/` — ten L2 artifacts behind round 9's claims: `probeA.md`/`probeB.md`/`probeC.md` (+ their scripts), `critic.md` (16-defect fix-landing audit, claim triage), `harness-mutation.md` + `test_harness.py` (50 cases, exit 0), `prior-art.md`, `sibling-overlap.md`, `review.md` (citation/state audit)
- Public prior art fetched 2026-09-28 for novelty calibration → `corpus/knowledge/eval-prior-art-calibration.md`: `arxiv.org/abs/2505.06120` (Laban et al., *LLMs Get Lost In Multi-Turn Conversation*, ICLR 2026), `2310.01798` (Huang et al., self-correction), `2307.13702` (Lanham et al., CoT faithfulness), `2309.06275` (Re²), `2210.01296` (RECITE), `2209.11895` (induction heads), `2305.18654` (Faith and Fate), `2205.10625` (least-to-most), `2310.20410` (FollowBench), `2410.15553` (Multi-IF), `2501.17399` (MultiChallenge), `2507.05257` (MemoryAgentBench), `2406.10149` (BABILong), `2406.12045` (τ-bench `pass^k`), `2504.04823` + `2409.11055` + `aclanthology.org/2025.emnlp-main.479` (quantization bands), `github.com/ggml-org/llama.cpp/issues/7052` (multi-slot non-determinism — the public antecedent of this lane's non-iid finding), `docs.vllm.ai/en/latest/features/batch_invariance/`, `thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/`
