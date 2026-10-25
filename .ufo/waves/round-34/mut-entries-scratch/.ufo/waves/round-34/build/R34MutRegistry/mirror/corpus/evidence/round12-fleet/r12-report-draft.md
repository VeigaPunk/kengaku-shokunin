<!-- round-12 report DRAFT — authored by L2 scribe `ScribeDrafts` (role: scribe, wave 1).
     Task restated: draft the round-12 paperwork skeletons (report + LOG entry + doc deltas)
     so L1 only fills run values.
     L1: fill every `{{TOKEN}}` from YOUR OWN run output / the landed `analysis_r12.md` /
     the critic verdict — never from a second-hand artifact — then land this file as
     `/home/vgpnk/projects/shokunin/.ufo/reports/round-12/kengaku.md` (main repo) with the
     child-repo commit pushed first. Delete this comment. Placeholder names are canonical:
     the log draft and the doc-deltas file use the SAME names (registry below). -->

# kengaku-shokunin — round 12 report (DRAFT — L1 fills every double-brace token)

Lane: `kengaku` (child repo `kengaku-shokunin/`, axes **novelty + calibration**; domain: LLM eval/research). Report model: L1 `@m_qwen` per `MISSION.md` fleet table. L2 fleet routed per the `MISSION.md` route buckets: executor / scribe / scout → `@m_flash`; reviewer / critic / labrat / mutation-tester → `@m_zfl`; planner / connector → `@m_lunamax` (`MISSION.md` §"L2 concurrency — required", read 2026-09-28).

Axis-move: **novelty 6 → {{AXIS_NOVELTY_AFTER}}** — one powered, preregistered, prior-art-priced run that turns round 11's single powered pairwise contrast into a **four-point emission-granularity ladder** (ordered-trend test on the same problems), a **batching dissociation** that decomposes r8's `A-MONO 0/10`, a **second task family** (positional token-sequence editing), and **per-problem probabilistic forecasts** (Brier / skill score / calibration slope). Claim set **C1–C6** and verdict rules **R1–R5** are quoted verbatim from the hashed plan below; every verdict is a mechanical branch fired by `recompute_r12.py`, never a judgement made at writing time.

Pre-round HEAD `f09ff1f` (`git rev-parse HEAD` → `f09ff1fc4d9e1e106d07c02b5bf9c148579175df`, subject "round-11"; read 2026-09-28); child-repo round-12 commit `{{CHILD_COMMIT}}`; main-repo report commit `{{MAIN_REPORT_COMMIT}}` (verify: `git -C ~/projects/shokunin log -1 --format=%h -- .ufo/reports/round-12/kengaku.md`).

## Placeholder registry (canonical names — reused verbatim in `r12-log-draft.md` and `r12-doc-deltas.md`)

Scribe rule: a `{{TOKEN}}` appears only where a **run value** is genuinely unknown at draft time. Every token below is resolvable from a committed path; the command in the third column is the one L1 runs. Nothing in this file is a measured value unless it is written without braces.

| Token | Resolves from | Command |
|---|---|---|
| `{{BUNDLE_PROBE_PLAN_SHA}}` | `round12-ladder/prereg-bundle.sha256` | `grep 'probe_plan_r12.md' corpus/evidence/round12-ladder/prereg-bundle.sha256` |
| `{{BUNDLE_POWER_SHA}}` | same file | `grep 'power_analysis_r12.md' corpus/evidence/round12-ladder/prereg-bundle.sha256` |
| `{{BUNDLE_PRED_SHA}}` | same file | `grep 'predictions-r12.md' corpus/evidence/round12-ladder/prereg-bundle.sha256` |
| `{{BUNDLE_FILE_SHA}}` | bundle file itself | `sha256sum corpus/evidence/round12-ladder/prereg-bundle.sha256` |
| `{{ORDERING_PRE_TS}}`, `{{ORDERING_POST_TS}}`, `{{ORDERING_LOG}}` | `round12-ladder/ordering.log` (the third is the file's verbatim text) | `cat corpus/evidence/round12-ladder/ordering.log` |
| `{{SCRIPT_HASH_TS}}`, `{{PROBE_R12_SHA}}`, `{{RUN_R12_SHA}}`, `{{PREDICT_R12_SHA}}` | `ordering.log` script-hash lines (plan §6.5) | `grep 'probe_r12.py\|run_r12.py\|predict_r12.py' corpus/evidence/round12-ladder/ordering.log` |
| `{{FIRST_REQUEST_TS}}` | landed run bytes | `grep -o '"request_ts":"[^"]*"' corpus/evidence/round12-ladder/results-r12.jsonl \| head -1` |
| `{{PRECHECK_LOG}}` | `round12-ladder/prereg-precheck.log` | `cat corpus/evidence/round12-ladder/prereg-precheck.log` |
| `{{CRITIC_VERDICT}}` | design-critic artifact (r11 convention → `r12-critic-design.md`) | `grep -n -i 'verdict' corpus/evidence/round12-fleet/r12-critic-design.md` |
| `{{MOCK_RESULT}}`, `{{SMOKE_RESULT}}` | labrat artifact (→ `r12-mock-smoke.md`) + smoke run dir | `grep -n -i 'census\|exit' corpus/evidence/round12-fleet/r12-mock-smoke.md` |
| `{{RECORDS}}`, `{{REQUESTS}}`, `{{WALL_S}}` | `analysis_r12.md` census line + `run.log` SUMMARY tail | `head -1 corpus/evidence/round12-ladder/analysis_r12.md; tail -3 corpus/evidence/round12-ladder/run.log` |
| `{{CENSUS}}` | store | `head -1 corpus/evidence/round12-ladder/analysis_r12.md` |
| `{{SUMMARY_LINES}}` | `run.log` | `sed -n '/=== SUMMARY ===/,$p' corpus/evidence/round12-ladder/run.log` |
| `{{RESULTS_MD5}}`, `{{RUNLOG_MD5}}`, `{{ANALYSIS_MD5}}` | landed bytes | `md5sum corpus/evidence/round12-ladder/{results-r12.jsonl,run.log,analysis_r12.md}` |
| `{{ARM_TABLE}}` | seven stored rows (plan §5) | `sed -n '/^\| Arm /,/^$/p' corpus/evidence/round12-ladder/analysis_r12.md` |
| `{{E1_*}}`, `{{E2_*}}`, `{{E3_GAPS}}`, `{{E4_*}}`, `{{E5_*}}`, `{{E6_*}}` | stored endpoint lines (`{{E6_N}}`: the plan's E6 denominator is internally inconsistent — 448 at `probe_plan_r12.md:24`/`:120` vs 416 by its own arithmetic; the stored value wins, see §Errata) | `grep -n '^E1 \|^E2 \|^E3 \|^E4 \|^E5 \|^E6 ' corpus/evidence/round12-ladder/analysis_r12.md` |
| `{{VERDICT_R1}}` … `{{VERDICT_R5}}` | stored verdict lines | `grep -n '^VERDICT R' corpus/evidence/round12-ladder/analysis_r12.md` |
| `{{FINISH_AUDIT}}`, `{{ACK_COMPLIANCE}}`, `{{EXCLUDED_PIDS}}` | stored audit lines | `grep -n '^Finish audit\|^Ack compliance\|^Excluded pids' corpus/evidence/round12-ladder/analysis_r12.md` |
| `{{POINT_SCORES}}` | point-prediction scoring table | `sed -n '/^\| Quantity /,/^$/p' corpus/evidence/round12-ladder/analysis_r12.md` |
| `{{GRADER_CHECKS}}`, `{{GRADER_LINES}}`, `{{SELFTEST}}`, `{{STDOUT_MD5}}`, `{{PYHASH}}` | gate after the r12 extension | `python3 grader.py; wc -l grader.py; python3 grader.py --selftest` |
| `{{MUTATION_BATTERY}}` | wave-2 mutation artifact (→ `r12-mutation.md`) | `grep -n -i 'kill\|M0' corpus/evidence/round12-fleet/r12-mutation.md` |
| `{{C1_C6_VERDICTS}}`, `{{METHOD_ITEMS}}` | scout prior-art artifacts (→ `r12-prior-art-{ladder,transport}.md`) | `grep -n -i 'verdict\|C[1-6]' corpus/evidence/round12-fleet/r12-prior-art-*.md` |
| `{{ENDPOINT_SCOUT}}` | scout artifact (→ `r12-scout-endpoint-fresh.md`) | `grep -n -i 'models\|argv\|pid' corpus/evidence/round12-fleet/r12-scout-endpoint-fresh.md` |
| `{{REVIEW_BASELINE_VERDICT}}`, `{{CRITIC_LANDED_VERDICT}}`, `{{REVIEW_INDEX_VERDICT}}`, `{{CONNECTOR_RULING}}` | wave-1/wave-2 reviewer artifacts | `grep -n -i 'VERDICT\|BASELINE\|CLEAN' corpus/evidence/round12-fleet/r12-review-*.md corpus/evidence/round12-fleet/r12-critic-landed.md` |
| `{{AXIS_NOVELTY_AFTER}}` … `{{AXIS_ADJACENCY_AFTER}}` (7) | `SCORECARD.md` §Round 12 post-move (L1's own scoring) | `sed -n '/^## Round 12/,/^## /p' SCORECARD.md` |
| `{{KN_ROWS_AFTER}}`, `{{LS_ROWS_AFTER}}`, `{{EV_ROWS_AFTER}}` | `README.md` index after landing | `grep -c '^\| `knowledge/' corpus/README.md; ls corpus/knowledge \| wc -l; grep -c '^\| `lessons/' corpus/README.md; ls corpus/lessons \| wc -l; ls -d corpus/evidence/*/ \| wc -l` |
| `{{FLEET_FILES}}`, `{{LADDER_FILES}}` | landed dirs | `ls corpus/evidence/round12-fleet \| wc -l; ls corpus/evidence/round12-ladder \| wc -l` |
| `{{SKILL_LINES_AFTER}}`, `{{BULLETS_AFTER}}`, `{{ANTIPATTERN_AFTER}}`, `{{CITATION_RES}}` | `SKILL.md` after the round-12 edits | `wc -l < SKILL.md; awk '/^## Cited local sources/,0' SKILL.md \| grep -cE '^- '; awk '/^## Benchmark anti-patterns/,/^## Research note/' SKILL.md \| grep -cE '^[0-9]+\. '` |
| `{{CHILD_COMMIT}}`, `{{PUSH_LINE}}`, `{{MAIN_REPORT_COMMIT}}` | round-12 landing | `git rev-parse --short HEAD` (child) after commit; child `git push` stdout; `git -C ~/projects/shokunin log -1 --format=%h -- .ufo/reports/round-12/kengaku.md` |
| `{{MODELS_JSON}}`, `{{SERVER_PID}}`, `{{ARGV_TOKENS}}` | **endpoint scout only** (this lane's traffic rule: the real `:34113` is read-only `GET /v1/models` + `/health`, scout-only) | copy verbatim from the scout artifact, never re-`curl` |
| `{{LEDGER_STATUS}}`, `{{WIKI_STATUS}}` | filesystem | `test -e ~/Projects/bounties/ledger/telemetry.jsonl && echo present \|\| echo ABSENT; test -e ~/wikillm/llm-wiki && echo present \|\| echo absent` |
| `{{BRIEF_BLOCKS}}` | per-agent dispatch briefs | `read history://<AgentId>:1-22` |
| `{{BUNDLE_CHECK_RESULT}}` | `sha256sum -c` from the repo root | `sha256sum -c corpus/evidence/round12-ladder/prereg-bundle.sha256` (expect 3× `OK`) |
| `{{GRADER_EXIT}}` | gate exit code | `python3 grader.py >/dev/null; echo $?` |
| `{{MET_NOT_MET}}` (×4, checklist) | falsifiable-target status | L1's judgement against the adjacent evidence cell |
| `{{DEVIATIONS}}`, `{{AMENDMENTS}}`, `{{CONFIDENCE_BULLETS}}`, `{{NEXT_MOVE}}`, `{{REPORT_OUTS}}`, `{{ABSORBED}}`, `{{INTEGRATOR_DELTAS}}`, `{{PHENOM_INSTR_COUNTS}}` | prose slots | written from the landed artifacts named beside each slot (no command: these are paragraphs, not numbers; every number inside them must be a resolvable `{{TOKEN}}` or a committed value) |
| `{{NOVELTY_MOVE}}`, `{{NOVELTY_PTR}}`, `{{CALIBRATION_MOVE}}`, `{{CALIBRATION_PTR}}`, `{{DEPTH_MOVE}}`, `{{DEPTH_PTR}}`, `{{COVERAGE_MOVE}}`, `{{COVERAGE_PTR}}`, `{{OPERABILITY_MOVE}}`, `{{OPERABILITY_PTR}}`, `{{FRESHNESS_MOVE}}`, `{{FRESHNESS_PTR}}`, `{{ADJACENCY_MOVE}}`, `{{ADJACENCY_PTR}}` | `SCORECARD.md` §Round 12 (L1's own text) | `sed -n '/^## Round 12/,/^## Scoring/p' SCORECARD.md` |
| `{{ARM_INC_ROW}}` … `{{ARM_SPARSE_ROW}}` (7) | §5 stored per-arm rows | `sed -n '/^\| Arm /,/^$/p' corpus/evidence/round12-ladder/analysis_r12.md` |
| `{{W1_ARTIFACT_*}}` (8: `SCOUT_LADDER`, `SCOUT_TRANSPORT`, `SCOUT_ENDPOINT`, `CONNECTOR`, `REVIEW_BASELINE`, `MOCK`, `RECOMPUTE`, `GRADER_DRAFT`) and `{{W2_ARTIFACT_*}}` (3: `MUTATION`, `CRITIC_LANDED`, `REVIEW_INDEX`) | artifact **filenames**, L1 substitutes the landed names (round-11 convention `r11-*.md` → `r12-*.md`) | `ls corpus/evidence/round12-fleet/` |
| `{{PROVINCE_DRIFT}}`, `{{LESSON_BULLETS}}` | used in `r12-doc-deltas.md` | `PROVINCE_DRIFT`: drift found by the §Surfaces re-verification (`test -e` + the scout capture); `LESSON_BULLETS`: L1 writes from the round's own record |

Values already real at draft time (no braces, do **not** re-derive): pre-round HEAD `f09ff1f` / `f09ff1fc4d9e1e106d07c02b5bf9c148579175df`; the committed gate at that HEAD → `python3 grader.py` = `CHECKS n=280 mismatches=0 errata_pinned=1`, `VERDICT: PASS`, exit 0, and `python3 grader.py --selftest` = 7 scenarios (S0–S6) `ALL PASS`, exit 0 — both re-run 2026-09-28 by this scribe (`wc -l < grader.py` → 1711); plan facts cited below with `probe_plan_r12.md` line numbers; the whole of §1–§8 of the plan.

## The move — four-point ladder + batching dissociation + transport + per-problem forecasts

Design frozen pre-run in `corpus/evidence/round12-ladder/probe_plan_r12.md` (sha256 `{{BUNDLE_PROBE_PLAN_SHA}}`): one run, two families, seven arms, six claims, five mechanical verdicts.

- **Family 1 (inventory ledger, verbatim r8/r9/r11 machinery)** — pids `201–264` (n=64), `gen_problem(3000 + pid*41)` (byte-identical problems and seeds to r11 by design, so C2 is a repeated-measures replication and the C5 predictor may use r11's per-problem outcomes as legitimate prior information rather than a cross-arm leak) — `probe_plan_r12.md:36-38`.
- **Five arms on every family-1 problem** — `A-INC` (graded turns {1..10}, r8 `run_inc(proto='INC')` ask wording: every ask is "Output the FULL state after applying it."), `A-CKPT4710` ({4,7,10}), `A-CKPT710` ({7,10}), `A-CKPT10` ({10}) — all r11 `ladder()` wording — and `A-MONO` (single shot, all 10 ops listed up front, FINAL state only). `A-CKPT10` is new: it isolates *emission sparsity* from *op batching* — the two mechanisms r8 confounded — `probe_plan_r12.md:41-57`; §7 deviations 1–2 at `:302-304`.
- **Arm order** — 5-rotation Latin square, `order = ARMS[(pid-201) % 5:] + ARMS[:(pid-201) % 5]`, realized position counts recorded in `descriptors.arm_order_counts` (`probe_plan_r12.md:58-61`); one filler before each cell (5 per pid).
- **Family 2 (new machinery, same ladder)** — positional token-sequence editing: ordered token list, ops `APP/INS/DEL/SET/MOV/SWP/REV`, pids `401–448` (n=48), `gen_seq_problem(5000 + pid*37)`, arms `T-DENSE` {4,7,10} vs `T-SPARSE` {7,10}, order counterbalanced by pid parity (`probe_plan_r12.md:69-107`). Grading: `ok = (got == want)`; `nwrong = |len(got) − len(want)| + #{i < min(len) : got[i] != want[i]}`; non-list/parse failure → `ok=False, nwrong=len(want)` — the family-1 non-dict convention, so a parse failure is maximally severe in both families.
- **Endpoints E1–E6 (mechanical, no judgement at analysis time)** — E1 Page's ordered-trend test (primary, C1); E2 paired `A-CKPT710 − A-CKPT4710` at {7,10} (C2); E3 the three adjacent gaps (C6); E4 `A-MONO − A-CKPT10` final-state `nwrong` (C3); E5 `T-SPARSE − T-DENSE` at {7,10}, n=48 (C4); E6 448 pass events with per-problem predicted probabilities → Brier / BSS / calibration slope+intercept / 5-bin reliability (C5) — `probe_plan_r12.md:112-124`.
- **Error-record contingency, inside the bundle (lesson 7)** — any `cell:"error"` record listwise-deletes that pid from all paired statistics of its family; if family-1 n < **56** or family-2 n < **42** (the filed power minima) every verdict is reported `UNDERPOWERED-INDETERMINATE` regardless of p, and the run is never re-analyzed with a smaller MDE — `probe_plan_r12.md:152-160`.
- **Cost** — plan §4 pins **4 114 records / 4 002 HTTP calls** (4 000 `chat/completions` + 2 `/v1/models` GETs), est. 12–25 min at r11's measured 0.184 s/request — `probe_plan_r12.md:194-205`; the gate recomputes exactly these two totals.
- **Descriptor sentence, carried verbatim into every derived claim** — *single served unit — Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS under the stack pinned in the run's `descriptors` record (q4_0 KV cache, `--kv-unified`, `--parallel 2`, custom non-upstream chat template); no cross-model generalization* (`probe_plan_r12.md:27-30`).

### Claims under test (verbatim from `probe_plan_r12.md` §1, lines 18–25)

| # | Claim | Instrument | Status before r12 |
|---|---|---|---|
| **C1** | **Ladder monotonicity**: per-problem error severity at the final forced emission increases monotonically as forced-emission density falls across four arms on the *same* problems — `A-INC` (10 checkpoints) → `A-CKPT4710` (3) → `A-CKPT710` (2) → `A-CKPT10` (1) | Page's ordered-trend test on within-problem ranks (n=64 blocks × 4 ordered arms), one confirmatory p | r9: directional only (n=8, tie at pass level); r11: priced the *middle* contrast only (+0.352, p=0.0011). No round has tested the ladder as an ordered whole |
| **C2** | **Within-run replication of the r11 dose**: the paired severity diff `A-CKPT710 − A-CKPT4710` at shared checkpoints {7,10} reproduces r11's +0.352 on *identical problems and seeds* | paired t + exact sign test, predicted point value filed pre-request | r11 ESTABLISHED once, on a different run day; never replicated within a later run |
| **C3** | **Batching dissociation**: r8's `A-MONO 0/10` collapse is driven by *up-front op batching*, not by emission sparsity — a one-checkpoint incremental arm (`A-CKPT10`) should beat `A-MONO` on final-state severity | paired diff `A-MONO − A-CKPT10` on final-state `nwrong` (n=64) | r8 recorded MONO 0/10 vs INC 7/10 vs CKPT4710 1/10 at n=10 and attributed the spread to emission granularity; the two mechanisms were never separated |
| **C4** | **Transport**: the dense-vs-sparse severity dose transports to a structurally different task family (positional token-sequence editing: no integer arithmetic, no key set, order-carrying state) | paired diff `T-SPARSE − T-DENSE` at shared checkpoints {7,10}, n=48 | never tested; every prior severity number is inventory-ledger-only |
| **C5** | **Per-problem forecast skill**: a mechanical predictor fitted on r11's committed per-problem bytes forecasts r12 pass outcomes better than arm-level climatology | Brier over 448 pass events (7 arms), Brier skill score, calibration slope/intercept, 5-bin reliability | r11 filed 3 event-level probabilities (Brier 0.153, self-admittedly dominated by one term); the lane's own checklist prefers per-problem probabilities and has never filed them |
| **C6** | **Dose magnitude ordering**: the adjacent severity gaps are ordered by *checkpoint count removed*, i.e. the INC→4710 gap (7 checkpoints removed) and the 710→10 gap (1 removed) are both ≥0 and the ladder's total spread exceeds each adjacent gap | three adjacent paired contrasts at their shared turns, reported with the global test | never measured; r11 measured one adjacent gap |

### Preregistered verdict rules (verbatim from `probe_plan_r12.md` §2.3, lines 126–150 — applied verbatim by `recompute_r12.py`, which prints the fired branch as a comment line so the gate can re-check the rule against the numbers)

```
R1 ladder (E1):   Page p < 0.05 AND L direction = increasing severity with
                  decreasing density          -> LADDER ESTABLISHED
                  Page p >= 0.05 AND all three adjacent diffs (E3) > 0
                                              -> LADDER DIRECTIONAL
                  otherwise                   -> LADDER NOT SUPPORTED
R2 replication(E2): diff > 0 AND p < 0.05 AND sign test agrees in direction
                                              -> REPLICATED
                  diff > 0 AND p < 0.05 AND sign test disagrees
                                              -> REPLICATED-DOWNGRADED
                  diff > 0 AND p >= 0.05      -> DIRECTIONAL
                  diff <= 0                   -> NOT REPLICATED
                  |diff - 0.352| <= 0.15      -> additionally POINT-MATCHES-r11
R3 batching (E4): diff(MONO - CKPT10) > 0 AND p < 0.05
                                              -> DISSOCIATION ESTABLISHED
                  diff > 0 AND p >= 0.05      -> DISSOCIATION DIRECTIONAL
                  diff <= 0                   -> DISSOCIATION FALSIFIED
R4 transport(E5): diff > 0 AND p < 0.05       -> TRANSPORTS
                  diff > 0 AND p >= 0.05      -> TRANSPORT DIRECTIONAL
                  diff <= 0                   -> TRANSPORT NOT SUPPORTED
R5 forecast (E6): BSS > 0 AND calibration slope in [0.5, 2.0]
                                              -> FORECAST SKILLED
                  BSS > 0                     -> FORECAST SKILLED-MISCALIBRATED
                  BSS <= 0                    -> FORECAST UNSKILLED
```

## Preregistration & ordering

Bundle filed and hashed **before the first endpoint request** (plan §6.1–6.5). `sha256sum -c corpus/evidence/round12-ladder/prereg-bundle.sha256` **from the repo root** → `{{BUNDLE_CHECK_RESULT}}` (expected 3× `OK`, exit 0; F2-class cwd caveat: the bundle file carries repo-relative paths, so `-c` must run from the repo root — round-10 critic F2, `SCORECARD.md:76-90`).

| File | sha256 (`prereg-bundle.sha256`) |
|---|---|
| `corpus/evidence/round12-ladder/probe_plan_r12.md` | `{{BUNDLE_PROBE_PLAN_SHA}}` |
| `corpus/evidence/round12-ladder/power_analysis_r12.md` | `{{BUNDLE_POWER_SHA}}` |
| `corpus/evidence/round12-ladder/predictions-r12.md` | `{{BUNDLE_PRED_SHA}}` |

Bundle file itself: `prereg-bundle.sha256` sha256 `{{BUNDLE_FILE_SHA}}`. Machinery as filed: `probe_r12.py` sha256 `{{PROBE_R12_SHA}}`, `run_r12.py` sha256 `{{RUN_R12_SHA}}`, `predict_r12.py` sha256 `{{PREDICT_R12_SHA}}` — appended to `ordering.log` post-fix, i.e. **after** the bundle hash and **before** the first request (plan §6.5, `probe_plan_r12.md:286-288`); the run's own `descriptors` record re-derives the machinery hash at run time, so the run-time value is authoritative for the landed claim.

`ordering.log` (verbatim, `corpus/evidence/round12-ladder/ordering.log`):

```text
{{ORDERING_LOG}}
```

Pre/post-hash timestamps `{{ORDERING_PRE_TS}}` / `{{ORDERING_POST_TS}}`; script hashes `{{SCRIPT_HASH_TS}}`. First endpoint `request_ts`: `{{FIRST_REQUEST_TS}}` (must postdate the last hash line — clause 1 of the falsifiable target; read from the landed `results-r12.jsonl`, not from `/tmp`).

Pre-run generation/schema precheck (`corpus/evidence/round12-ladder/prereg-precheck.log`, verbatim):

```text
{{PRECHECK_LOG}}
```

Design-critic L2 (`CriticDesign`) gate verdict: **`{{CRITIC_VERDICT}}`** — must land **before** the first endpoint request; a fatal defect → amend, re-hash (v2), append new `ordering.log` lines (plan §6.4). Mock smoke (`mock_server_r12.py` on 127.0.0.1:18114 — the only permitted mock bind; the real `:34113` receives no bytes from this lane's fleet except the scout's read-only `GET /v1/models` + `/health`): `{{MOCK_RESULT}}`; real-endpoint smoke (N=1, schema check only): `{{SMOKE_RESULT}}`. No mock byte is ever mixed into the committed results (plan §6.6–6.7).

## L2 fleet (13 agents; wave 1 = 10 in ONE batched call, wave 2 = 3)

`MISSION.md` §"L2 concurrency — required": ≥8 L2 per round in one batched `task` call — wave 1 alone clears it. No L2 writes a shared file; single integration owner: L1. Artifacts committed verbatim under `corpus/evidence/round12-fleet/` (`{{FLEET_FILES}}` files); corrections/deltas only in `INTEGRATOR-NOTES.md`. Task column: L1 transcribes each L2's own dispatch brief at landing (`read history://<AgentId>:1-22`), as rounds 10–11 did — `{{BRIEF_BLOCKS}}`.

| Agent (role, wave) | Task | Artifact |
|---|---|---|
| CriticDesign (critic, 1) | falsify the hashed design pre-run: Page-test mechanics and tie handling, power arithmetic against the filed minima (family 1 n≥56 / family 2 n≥42), family-2 generator/regeneration rule, schema-vs-§4 census consistency, verdict-rule completeness (incl. the `UNDERPOWERED-INDETERMINATE` override), network-path inventory | `r12-critic-design.md` — **`{{CRITIC_VERDICT}}`** |
| ScoutPriorArtLadder (scout, 1) | prior-art pricing of the ladder claims **C1, C2, C3, C6** (ordered density ladder; within-run replication; batching-vs-sparsity dissociation; gap-magnitude ordering), verdicts with fetched URLs | `{{W1_ARTIFACT_SCOUT_LADDER}}` |
| ScoutPriorArtTransport (scout, 1) | prior-art pricing of **C4** (transport to a second task family) **and C5** (per-problem forecast skill: Brier/BSS/calibration-slope practice in agent benchmarks), fetched URLs + wording guidance | `{{W1_ARTIFACT_SCOUT_TRANSPORT}}` |
| ScoutEndpointFresh (scout, 1) | the round's only real-endpoint traffic: read-only `GET /v1/models` + `/health` on `:34113`, process pin (`/proc/<pid>/cmdline`), fresh evidence of stack drift since r11 — feeds the `descriptors` comparison and the page's freshness section | `{{W1_ARTIFACT_SCOUT_ENDPOINT}}` (**`{{ENDPOINT_SCOUT}}`**) |
| ConnectorFleet (connector, 1) | sibling-HEAD sweep: does any sibling now own a hashed preregistration, per-problem probabilistic scoring, or an evidence-replay gate? re-verify the r10/r11 no-duplicate ruling; draft the round's report-outs | `{{W1_ARTIFACT_CONNECTOR}}` (**`{{CONNECTOR_RULING}}`**) |
| ReviewerBaseline (reviewer, 1) | pre-landing baseline: committed pointers re-run, r11 ordering chain re-checked, gate control at the r12 HEAD (expected `{{GRADER_CHECKS}}` *after* extension; pre-extension control = the real value `CHECKS n=280 mismatches=0 errata_pinned=1`), endpoint/argv freshness, md5 sweep → verdict | `r12-review-baseline.md` (landed by that agent) (**`{{REVIEW_BASELINE_VERDICT}}`**) |
| LabratMock (labrat, 1) | mock-server smoke on 127.0.0.1:18114 for both families (fenced/bare/malformed parse paths; §4 census ratios at N=2/N2=2); INTERCEPT line for any non-self target host; failing-before evidence preserved if the runner breaks | `mock_server_r12.py` + `{{W1_ARTIFACT_MOCK}}` (landed by that agent) (**`{{MOCK_RESULT}}`**) |
| ExecutorRecompute (executor, 1) | `recompute_r12.py` — deterministic stdlib engine emitting **every** §5 stored line (Page L, paired t/CI via `betai`, exact sign + McNemar via `math.comb`, Brier/BSS, damped-Newton calibration slope) + the verdict-branch comment line; own selftest + mutant battery | `{{W1_ARTIFACT_RECOMPUTE}}` |
| ExecutorGrader (executor, 1) | draft the gate extension for the r12 tree: §4 census + request counts, meta/meta2 regeneration, raw re-parse/re-grade of all 1 328 graded records, both SUMMARY halves, every stored `analysis_r12.md` line, descriptors pins, bundle hash chain + ordering proof, selftest S7 | `{{W1_ARTIFACT_GRADER_DRAFT}}` |
| **ScribeDrafts (scribe, 1)** | **this page's skeleton + the `LOG.md` entry skeleton + the `corpus/README.md`/`PROVINCE.md`/`SHONEN.md`/`SCORECARD.md` doc deltas; every run value as a `{{TOKEN}}` with its resolving command; pre-run values real and cited** | `r12-report-draft.md` (this file), `r12-log-draft.md`, `r12-doc-deltas.md` |
| MutationTesterR12 (mutation-tester, 2) | pre-designed mutation battery on the extended gate (kill-rate with a control M0, layer isolation, cross-tree isolation, guarded in-place swaps md5-restored) | `{{W2_ARTIFACT_MUTATION}}` (**`{{MUTATION_BATTERY}}`**) |
| CriticLanded (critic, 2) | adversarial re-derivation of every landed number with a FRESH implementation (Page L, the five verdicts, Brier/BSS/slope, raw re-parse spot check) → verdict | `{{W2_ARTIFACT_CRITIC_LANDED}}` (**`{{CRITIC_LANDED_VERDICT}}`**) |
| ReviewerCitations (reviewer, 2) | landing integrity: index both directions, number-trace audit of every new row/entry, fleet md5 sweep, citation resolution re-measure, PROVINCE surface resolution, LOG discipline → verdict | `{{W2_ARTIFACT_REVIEW_INDEX}}` (**`{{REVIEW_INDEX_VERDICT}}`**) |

## Run results

Main run (`KENGAKU_R12_OUT` under `/tmp`, landed **byte-identical** into `corpus/evidence/round12-ladder/`): `{{RECORDS}}` records / `{{REQUESTS}}` requests / `{{WALL_S}}` (plan §4 pins 4 114 / 4 002 as the two gate-recomputed totals). Landed md5s (recorded at copy time, pinned in the gate's `PINS`): `results-r12.jsonl` `{{RESULTS_MD5}}`, `run.log` `{{RUNLOG_MD5}}`; `analysis_r12.md` `{{ANALYSIS_MD5}}` (generated by the promoted `recompute_r12.py`; regeneration from committed bytes must be byte-identical at round close).

- Census (`analysis_r12.md` line 1): expected `1 descriptors, 64 meta, 48 meta2, 1328 graded, 2256 ack, 416 fillers, 0 error records` → observed `{{CENSUS}}`.
- `run.log` SUMMARY (7 cell lines + `wall_total_s:`, must match `grader.parse_runlog_summary`'s `^(\S+): (\d+)/(\d+)$`):

```text
{{SUMMARY_LINES}}
```

- Observed per-arm table (§5 stored format; 7 rows, one per arm — `{{ARM_TABLE}}`):

| Arm | Final passes / n | Mean final nwrong | Mean nwrong (shared turns) |
|---|---:|---:|---:|
| A-INC | `{{ARM_INC_ROW}}` | | |
| A-CKPT4710 | `{{ARM_4710_ROW}}` | | |
| A-CKPT710 | `{{ARM_710_ROW}}` | | |
| A-CKPT10 | `{{ARM_10_ROW}}` | | |
| A-MONO | `{{ARM_MONO_ROW}}` | | |
| T-DENSE | `{{ARM_DENSE_ROW}}` | | |
| T-SPARSE | `{{ARM_SPARSE_ROW}}` | | |

### E1 — ladder monotonicity (C1, primary)

Stored line: `E1 Page trend: L=<int> E_L=<float> var_L=<float> z=<±f.fff> two-sided p=<f.pppp> direction=<increasing|decreasing>`. Observed: `{{E1_PAGE}}` → `L={{E1_L}}`, `E_L={{E1_EL}}`, `var_L={{E1_VAR}}`, `z={{E1_Z}}`, `two-sided p={{E1_P}}`, `direction={{E1_DIR}}`. **Preregistered verdict R1: `{{VERDICT_R1}}`** (branches quoted above; R1 fires `LADDER ESTABLISHED` only if p<0.05 *and* the signed direction is increasing severity with decreasing density).

### E2 — within-run replication of the r11 dose (C2)

Stored lines: `E2 paired diff (710 - 4710, {7,10}): <±d.ddd> sd <s.ddd> n=<n>` / `E2 paired t: t=<±t.ttt>, df=<n-1>, two-sided p=<p.pppp>` / `E2 95% CI: [<l.lll>, <u.uuu>]` / `E2 exact sign: wins=<W> losses=<L> ties=<T> two-sided p=<p.pppp>` / `E2 McNemar final passes: b=<B> c=<C> two-sided p=<p.pppp>`. Observed: diff `{{E2_DIFF}}` (sd `{{E2_SD}}`, n=`{{E2_N}}`), t=`{{E2_T}}` df=`{{E2_DF}}` p=`{{E2_P}}`, CI `{{E2_CI}}`, sign `{{E2_SIGN}}`, McNemar `{{E2_MCNEMAR}}`. r11 comparator (real, `corpus/evidence/round11-power/analysis_r11.md`; `SCORECARD.md:136-147`): **+0.352** (sd 0.820, n=64), t=+3.431, df=63, p=0.0011, CI [+0.147, +0.556], sign 26W/7L/31T p=0.0013. **Preregistered verdict R2: `{{VERDICT_R2}}`** (`REPLICATED` requires diff>0 ∧ p<0.05 ∧ sign agreement; `|diff − 0.352| ≤ 0.15` additionally stamps `POINT-MATCHES-r11`).

### E3 — adjacent gaps (C6)

Stored line: `E3 adjacent gaps: 4710-INC {4,7,10} <±d.ddd> p=<p.pppp>; 710-4710 {7,10} <±d.ddd> p=<p.pppp>; 10-710 {10} <±d.ddd> p=<p.pppp>`. Observed: `{{E3_GAPS}}`. The middle gap is E2 by construction (same shared turns) — the two stored lines must agree; a divergence is a gate failure, not a finding.

### E4 — batching dissociation (C3)

Stored line: `E4 batching diff (MONO - CKPT10, final): <±d.ddd> sd <s.ddd> n=<n> t=<±t.ttt> p=<p.pppp> sign W/L/T=<W>/<L>/<T>`. Observed: `{{E4_DIFF}}` (sd `{{E4_SD}}`, n=`{{E4_N}}`), t=`{{E4_T}}`, p=`{{E4_P}}`, sign `{{E4_SIGN}}`. **Preregistered verdict R3: `{{VERDICT_R3}}`**. `A-MONO` differs from `A-CKPT10` on two axes by construction (batched ops **and** single emission) — exactly what this contrast decomposes (`probe_plan_r12.md:330-331`); the claim is directional and must not be written as a mechanism proof.

### E5 — transport (C4)

Stored line: `E5 transport diff (SPARSE - DENSE, {7,10}): <±d.ddd> sd <s.ddd> n=<n> t=<±t.ttt> p=<p.pppp> sign W/L/T=<W>/<L>/<T>`. Observed: `{{E5_DIFF}}` (sd `{{E5_SD}}`, n=`{{E5_N}}`), t=`{{E5_T}}`, p=`{{E5_P}}`, sign `{{E5_SIGN}}`. **Preregistered verdict R4: `{{VERDICT_R4}}`**. Family-2 severity is a positional-mismatch+length scale, **not** the family-1 key-mismatch scale: the cross-family comparison is limited to the effect-size **ratio**, reported descriptively and never pooled (`probe_plan_r12.md:334-338`).

### E6 — per-problem forecast skill (C5)

Stored lines: `E6 Brier: pooled=<f.ffff> (N=<n>); per-arm A-INC=<f.ffff> ... T-SPARSE=<f.ffff>` / `E6 BSS vs arm climatology: <±f.ffff>` / `E6 calibration: slope=<±f.ffff> intercept=<±f.ffff> (Newton on logit(p), <n> events)` / `E6 reliability (5 bins): …` (×5). Observed: pooled `{{E6_BRIER_POOLED}}` (N=`{{E6_N}}`), per-arm `{{E6_BRIER_ARMS}}`, BSS `{{E6_BSS}}`, slope `{{E6_SLOPE}}` intercept `{{E6_INTERCEPT}}`, reliability `{{E6_RELIABILITY}}`. r11 comparator (real): Brier **0.153** over 3 events. **Preregistered verdict R5: `{{VERDICT_R5}}`**. Two standing caveats must travel with this number: the C5 predictor is fitted on r11 outcomes **on the same family-1 problems**, so its skill is *persistence* skill, not cold forecasting; and family-2 forecasts are constant per arm by design (a no-information comparator) — (`probe_plan_r12.md:338-341`).

### Audits, exclusions, prediction scoring

- `Finish audit at graded turns: finish=length <L>/<G>, parse fail <P>/<G>` → `{{FINISH_AUDIT}}`.
- `Ack compliance (raw lowercased startswith ok): <cell> <a>/<b> = <c.c>%` (×6) → `{{ACK_COMPLIANCE}}`; the turn-1 quirk (the opening message always asks for the full state, so every CKPT arm logs turn 1 as `-ack`) is part of the measured construct and unchanged from r9/r11.
- `Excluded pids: family1 <list|none> family2 <list|none>` → `{{EXCLUDED_PIDS}}`; if the contingency fired, every verdict in this page is rewritten `UNDERPOWERED-INDETERMINATE` (plan §3) — an inderterminate reading is never laundered into a directional one (lesson: `corpus/lessons/round-9.md`).
- Point-prediction scoring table (`| Quantity | Predicted | Observed | Abs error |`, one row per filed point prediction):

```text
{{POINT_SCORES}}
```

## Grader extension (landed in-round, per round-11 §Planned clause (d))

Committed gate at the pre-round HEAD `f09ff1f`: **1711 lines**, `CHECKS n=280 mismatches=0 errata_pinned=1`, `VERDICT: PASS`, exit 0; `--selftest` 7 scenarios S0–S6 `ALL PASS`, exit 0 (both re-measured 2026-09-28 by this scribe: `python3 grader.py`; `python3 grader.py --selftest`; `wc -l < grader.py` → 1711). After the r12 extension: `{{GRADER_LINES}}` lines, `{{GRADER_CHECKS}}` checks, replaying **four** trees (r8/r9/r11/r12) — r12 layer adds meta/meta2 regeneration, raw re-parse/re-grade of all 1 328 graded records, the §4 census and request counts, both SUMMARY halves (7 cell lines), every stored `analysis_r12.md` line, descriptors pins, and the bundle sha256 chain + ordering proof. `--selftest` → `{{SELFTEST}}` (expected S0–S7 ALL PASS, exit 0); stdout byte-identical under PYTHONHASHSEED unset/1/42/99 → `{{STDOUT_MD5}}` / `{{PYHASH}}`. Independent mutation battery (L2-written, executed on copies): `{{MUTATION_BATTERY}}` (M0 control exit 0; ≥1 kill per layer; kill rate stated as a fraction, never as "all pass"). Promotion rule from rounds 10–11: L2-drafted, L1 lands by byte-exact slice assembly, deviations recorded in `INTEGRATOR-NOTES.md` with failing-before evidence — `{{INTEGRATOR_DELTAS}}`.

## Prior-art pricing (novelty proxy — quotes the round's headline claims)

Every C-claim and every method item must carry a verdict with a fetched URL; a negative is scoped to its search set, never written as an exhaustive "no published source" (round-11 CriticLanded wording finding (b), `INTEGRATOR-NOTES.md` §Wave-2).

- **C1–C6**: `{{C1_C6_VERDICTS}}` (phenomenon-new vs instrument-new counts `{{PHENOM_INSTR_COUNTS}}`).
- **Method/mechanism items** (e.g. Page's ordered-trend test for density ladders; Brier/BSS/calibration-slope practice in agent benchmarks; transport to a non-inventory task family; the fixed-emission ladder construct): `{{METHOD_ITEMS}}`.
- Standing method context carried from r11 (real, `corpus/knowledge/eval-prior-art-calibration.md` + `r11-prior-art-prereg.md`): paired-inference/power canon (Miller `2411.00640`); n=64 in the CLT-under-coverage zone (`2503.01747`) → exact sign kept as the preregistered robustness leg; llama.cpp #7052 closed-stale with the class unfixed; q4_0-KV perturbation (PR #21038 tables) is *fetched prior-art context*, common-mode across paired cells — the paired diff is defensible, absolute `nwrong` levels are not stack-transferable.

## SCORECARD before→after (details + ceilings in `SCORECARD.md` §Round 12; pre-move anchors = `SCORECARD.md` §Round 11 post-move)

| Axis | Before → After | What moved (abridged) | Evidence |
|---|---|---|---|
| **novelty** *(owned)* | 6 → `{{AXIS_NOVELTY_AFTER}}` | `{{NOVELTY_MOVE}}` | `{{NOVELTY_PTR}}` |
| **calibration** *(owned)* | 8 → `{{AXIS_CALIBRATION_AFTER}}` | `{{CALIBRATION_MOVE}}` | `{{CALIBRATION_PTR}}` |
| depth | 9 → `{{AXIS_DEPTH_AFTER}}` | `{{DEPTH_MOVE}}` | `{{DEPTH_PTR}}` |
| coverage | 7 → `{{AXIS_COVERAGE_AFTER}}` | `{{COVERAGE_MOVE}}` | `{{COVERAGE_PTR}}` |
| operability | 7 → `{{AXIS_OPERABILITY_AFTER}}` | `{{OPERABILITY_MOVE}}` | `{{OPERABILITY_PTR}}` |
| freshness | 7 → `{{AXIS_FRESHNESS_AFTER}}` | `{{FRESHNESS_MOVE}}` | `{{FRESHNESS_PTR}}` |
| adjacency | 8 → `{{AXIS_ADJACENCY_AFTER}}` | `{{ADJACENCY_MOVE}}` | `{{ADJACENCY_PTR}}` |

## Falsifiable-target checklist (quoted verbatim from `SCORECARD.md` §Planned, lines 181–184, the pre-round target this round closes)

> Falsifiable target: `ordering.log` + bundle hash (incl. the contingency rule) predate the first `request_ts`; a per-problem probability file exists and is scored at close; `python3 grader.py` exits 0 on the extended tree and `--selftest` passes; prior-art verdicts carry fetched URLs.

| # | Clause (verbatim) | Status | Evidence |
|---|---|---|---|
| 1 | `ordering.log` + bundle hash (incl. the contingency rule) predate the first `request_ts` | `{{MET_NOT_MET}}` | pre-hash `{{ORDERING_PRE_TS}}`, script hashes `{{SCRIPT_HASH_TS}}` < first `request_ts` `{{FIRST_REQUEST_TS}}`; contingency rule is §2.3 of the hashed plan (`probe_plan_r12.md:152-160`) |
| 2 | a per-problem probability file exists and is scored at close | `{{MET_NOT_MET}}` | `corpus/evidence/round12-ladder/predictions-r12.md` (sha256 `{{BUNDLE_PRED_SHA}}`, generated by `predict_r12.py` from committed r11 bytes only); scoring table `{{POINT_SCORES}}` + E6 lines `{{E6_BRIER_POOLED}}` / `{{E6_BSS}}` |
| 3 | `python3 grader.py` exits 0 on the extended tree and `--selftest` passes | `{{MET_NOT_MET}}` | `{{GRADER_CHECKS}}`, exit `{{GRADER_EXIT}}`; selftest `{{SELFTEST}}` |
| 4 | prior-art verdicts carry fetched URLs | `{{MET_NOT_MET}}` | `{{C1_C6_VERDICTS}}` + `{{METHOD_ITEMS}}` (URLs counted with HTTP status) |

## Errata & deviations

Three kinds of entry belong here; none may be patched silently into a committed file (append-only + errata discipline, `SCORECARD.md` §Round 10 errata precedent).

- **Deviation log (run-time)** — `{{DEVIATIONS}}`. Expected candidates from the plan's own threat list: a `descriptors_end` mismatch (mid-run stack drift → the run is re-executed, never analyzed; `probe_plan_r12.md:343-348`), any `cell:"error"` record (→ listwise deletion + the `{{EXCLUDED_PIDS}}` line), a landing md5 difference, and any L1 change to L2-drafted code.
- **Design amendments** — `{{AMENDMENTS}}`: if the pre-run critic forced a change, the hashed bundle is **never** edited in place; a numbered amendment is appended to `round12-fleet/INTEGRATOR-NOTES.md` and, if it touches the design, the bundle is re-hashed (v2) with new `ordering.log` lines before the first request (`probe_plan_r12.md:8-11`).
- **Pre-run design defect candidate (for `CriticDesign` / `ExecutorRecompute`, no fix applied by this scribe):** the plan pins the E6 event denominator twice and inconsistently — `probe_plan_r12.md:24` says "Brier over **448** pass events (7 arms)" and `:120` says "**448** pass events (5 arms × 64 + 2 arms × 48)". The parenthetical evaluates to **416** (5×64 = 320; 2×48 = 96; 320 + 96 = 416); 448 is 7×64. Verify: `grep -n '448' corpus/evidence/round12-ladder/probe_plan_r12.md` (the number also occurs at `:187` as `A-CKPT4710-ack = 448 = 64×7`, a plausible copy/paste origin — [INFERENCE]). Consequence for this page: `{{E6_N}}` must be whatever the landed `recompute_r12.py` actually emits, and the gate must pin that stored value; the plan's "448" must not be written as the observed N without the run saying so. Whether the discrepancy is a typo or an intended denominator change is the critic's ruling, recorded as an amendment in `INTEGRATOR-NOTES.md` (the hashed bundle is never edited in place).
- **Erratum candidate found while drafting this page (needs L1's ruling, no fix applied by this scribe):** the round-11 gate line count is published as **1709** in three places — `LOG.md:18` ("`grader.py` 936→**1709** lines"), `SCORECARD.md:142` ("936 → **1709** lines"), and the round-11 report (".ufo/reports/round-11/kengaku.md", "`grader.py` 936 → **1709** lines"). The committed artifact at `f09ff1f` is **1711** lines: `git show f09ff1f:grader.py | wc -l` → `1711`, `wc -l < grader.py` → `1711`, `grep -c -v '^$' grader.py` → `1527`, `grep -c '^$' grader.py` → `184` — so no counting convention yields 1709. The *before* half is exact (`git show 0c51208:grader.py | wc -l` → `936`), the check count is exact (`CHECKS n=280 mismatches=0 errata_pinned=1`, exit 0, re-run 2026-09-28), and the selftest claim (7 scenarios S0–S6) is consistent with `SKILL.md` §Hermetic grader. [INFERENCE] the 1709 was probably measured before the two-line in-code comment recording the file-order-primacy ordering-check fix (`INTEGRATOR-NOTES.md` delta 2) landed in the same commit; that provenance is conjectural. Suggested handling: an errata block under `SCORECARD.md` §Round 11 post-move + one appended `LOG.md` line naming all three sites — text drafted in `r12-doc-deltas.md` §`SCORECARD.md` (optional block) and §`LOG.md`. The gate must not pin the wrong count: any r12 self-description must say `{{GRADER_LINES}}` as measured *after* the extension.

## Adjacency & report-outs (`PROVINCE.md` tail; connector rulings in the connector artifact `{{W1_ARTIFACT_CONNECTOR}}`)

- `{{REPORT_OUTS}}` — per-domain: **protocol** (the fleet preregistration-standard referral stands unchanged; `r11-connector.md`), **kotoba** (ack compliance under checkpoint schedules + the spillover-ask craft evidence, extended by the 6-cell ack table `{{ACK_COMPLIANCE}}`), **integrator / unowned serving plane** (q4_0-KV materiality for ANY cross-model number from `:34113`), **kasegi** (ledger-tree status `{{LEDGER_STATUS}}`). Each is evidence sent with an owner named, never absorbed.
- `{{ABSORBED}}` — aggregator-owned or sibling-owned artifacts this lane responded to this round (index rows only, per the round-6 convention).

## Confidence

- `{{CONFIDENCE_BULLETS}}` — one bullet per graded claim. Pre-write the shape: ordering proof high; observed passes/severity high *after* independent recomputation (landed engine + gate replay + CriticLanded fresh implementation `{{CRITIC_LANDED_VERDICT}}`); paired-t iid assumption across pids medium (burst-state coupling bounded by pairing/rotation/fillers, not eliminated); ladder interpretation medium-high **for this served unit only**; family-2 transport medium (new instrument, n=48, one run); forecast skill medium as arithmetic, low-to-medium as calibration (persistence predictor on the same problems); underpowered branches high if the contingency fired.
- Standing caveat (round 10, must be repeated): grader PASS means the corpus agrees with itself, not that the model was good — no check touches the endpoint.

## Next move (`SCORECARD.md` §Planned)

`{{NEXT_MOVE}}` — rewritten in `r12-doc-deltas.md` §`SCORECARD.md` (the draft reasons the target axis out of the rubric rather than guessing; L1 re-derives the post-move scores first, then lands the block).

## Commit & push

- Child repo (`kengaku-shokunin/`): round-12 commit `{{CHILD_COMMIT}}`; push line `{{PUSH_LINE}}` (`git push` → `f09ff1f..{{CHILD_COMMIT}} master -> master`, `VeigaPunk/kengaku-shokunin`).
- Main repo (`~/projects/shokunin`): commit adding `.ufo/reports/round-12/kengaku.md` — `{{MAIN_REPORT_COMMIT}}`.

## Appendix (scribe — delete when landing the report; canonical home `r12-doc-deltas.md` §6) — round-11 sentences deliberately NOT carried over

Deliberate omissions from `.ufo/reports/round-11/kengaku.md` when drafting the sections above:

1. **The r11 headline numbers as if they were this round's** (+0.352 / t=+3.431 / p=0.0011 / CI [+0.147,+0.556] / sign 26W/7L/31T / Brier 0.153 / 29/64 · 21/64). They are quoted **only** as the r11 comparator next to `{{E2_*}}` / `{{E6_*}}`, never as r12 results; carrying them forward as unlabelled results would be exactly the stale-count defect the round-10 critic filed (`SCORECARD.md:76-90`).
2. **"1409 requests / 1473 records / 259.1 s"** — r11 run bytes; r12's pinned totals are 4 114 records / 4 002 calls (plan §4) and the observed values are `{{RECORDS}}` / `{{REQUESTS}}` / `{{WALL_S}}`.
3. **"grader.py 936 → 1709 lines, 149 → 280 checks, three trees"** — superseded: the pre-round committed gate is 1711 lines / 280 checks / three trees (re-measured), and the round-12 figures are `{{GRADER_LINES}}` / `{{GRADER_CHECKS}}` / four trees. The 1709 claim itself is filed as an erratum candidate above rather than repeated.
4. **"selftest S0–S6 ALL PASS"** as if current — 280-check/7-scenario is the r11 state; r12 expects S0–S7 (`{{SELFTEST}}`).
5. **The r11 L2 roster and its per-agent task sentences** (ScoutGranularity / ScoutPrereg / ScribeReport / MutationGrader / ReviewerIndex) — replaced wholesale by the r12 roster; only the MISSION route buckets and the lead sentence are reused.
6. **r11-only prior-art verdicts as current novel content** (StageIF `2609.08589`, `2605.30233`, `2606.11217`, `2603.10044`, PR #21038): the r11 report presents them as that round's pricing. Here they may return only as explicitly-labelled method context against a fresh search set; the round's own pricing is `{{C1_C6_VERDICTS}}`.
7. **"route-telemetry surface ABSENT … resolved 23:32Z … 7,226 lines"** and the SHONEN box-3 flip narrative: round-11-specific events. The carried element is the *re-check*, `{{LEDGER_STATUS}}`.
8. **"41 committed pointers → BASELINE GREEN"** — r11's reviewer sweep; r12's is `{{REVIEW_BASELINE_VERDICT}}` with its own pointer count.
9. **"Ack compliance: A-CKPT4710 220/448 = 49.1%, A-CKPT710 330/512 = 64.5%"** — r11 denominators; r12's 6-cell table is `{{ACK_COMPLIANCE}}`.
10. **The sentence "Also absorbed this round: the aggregator's non-author cold run … verdicted SHONEN box 3 `[x]`"** — a round-11 event that is now permanent repo state (`SHONEN.md` line 9, `corpus/lessons/round-8-aggregator-box3-coldrun.md`); repeating it in an r12 page would restate history as this round's work.

_Fill rule: every `{{TOKEN}}` in this file is unfilled by design. Resolve it with the command in the registry (or the artifact next to it) — never from a second-hand artifact, never from `/tmp` alone. Pre-run values already written without braces (pre-round HEAD, committed gate numbers, plan line citations, r11 comparators labelled as such) are real and do not need re-derivation. Delete a placeholder only by deleting its whole line. Placeholder names are shared with `r12-log-draft.md` and `r12-doc-deltas.md`._