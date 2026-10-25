# kengaku-shokunin — round 11 report (DRAFT — L1 fills every double-brace token)

Lane: `kengaku` (child repo `kengaku-shokunin/`, axes **novelty + calibration**; domain: LLM eval/research). Report model: L1 `@m_qwen` per `MISSION.md` fleet table. L2 fleet routed per the `MISSION.md` route buckets: executor / scribe / scout → `@m_flash`; reviewer / critic / labrat / mutation-tester → `@m_zfl`; planner / connector → `@m_lunamax` (`MISSION.md` §"L2 concurrency — required", read 2026-09-28).

Axis-move: **novelty 5 → `{{N}}`** — one powered, preregistered, prior-art-priced rerun of the emission-granularity ladder (round 9's `A-CKPT4710` vs `A-CKPT710`), measuring error *severity*, not just passes.

Pre-round HEAD `0c51208` (`git rev-parse HEAD` → `0c5120844a27ae9c8656a5f470af300960dd9ad5`, commit subject "round-10"; `git -C kengaku-shokunin log --oneline -1` read 2026-09-28); child-repo round-11 commit `{{HASH}}`.

## The move — powered preregistered emission-granularity rerun

Design fixed pre-run in `corpus/evidence/round11-power/probe_plan_r11.md` (sha256 `d7fbeebe…`, full value in §Preregistration & ordering). Claim under test — **granularity–severity dose**: sparser forced-emission checkpoints increase per-problem error severity (mean wrong keys at shared checkpoints) even where pass rates tie (r9: passes `2/8 = 2/8`, final-turn severity `0.875 → 1.375`; `corpus/evidence/round9-replication/replication.md` §Observed results, §Dose-response reading — read 2026-09-28).

- **Cells**: `A-CKPT4710` (graded turns {4,7,10}) vs `A-CKPT710` (graded turns {7,10}); no INC/MONO anchors — the paired design is its own control (`probe_plan_r11.md` §2). r9/r8 anchors stay on the record for ladder context.
- **Primary endpoint** (paired): mean paired difference of per-pid mean `nwrong` at the **shared checkpoints {7,10}** (710 − 4710). Same problem graded under both schedules, so the per-pid difference removes problem difficulty; r9's headline "0.875 → 1.375" mixes denominators and is descriptive only (`power_analysis_r11.md` §"Why the shared-checkpoint paired mean").
- **Power**: n = 64 pairs (pids 201–264), two-sided paired t-test, α = 0.05, **MDE d = 0.35** at 80% power (`√(7.849/64) = 0.350`); at the r9 point estimate d = 0.519 the power is `Φ(√64·0.519 − 1.960) = Φ(2.191) ≈ 0.986` (`power_analysis_r11.md` §Sample size).
- **Problems / seeds**: pids 201–264, `gen_problem(3000 + pid*41)`, machinery byte-lineage to r9 (`probe_r11.py` = `round9-replication/replicate.py` copy, only docstring + env-overridable BASE/OUT differ — `run_r11.py:116` `probe_lineage`); seeds disjoint from r8 (`700+pid*13`, pids 1–10) and r9 (`2000+pid*29`, pids 101–108).
- **Counterbalance**: both cells run on the same problem, adjacent in time (all 20 requests of a pid back-to-back); cell order counterbalanced by **pid parity** (even pid: 4710 first; odd: 710 first); one filler request ("Reply with the single word: ready.") before each cell → 128 fillers (`probe_plan_r11.md` §2, §7.1).
- **Turn semantics**: verbatim `run_r9.py` ladder, including the post-checkpoint spillover (the turn after a checkpoint is asked for the FULL state but logged as `-ack`, raw truncated to 80 chars) — the quirk is part of the measured construct (`probe_plan_r11.md` §2, §7).
- **Settings**: temp 0.2, max_tokens 8192, system prompt verbatim (`probe_r11.py` SYSTEM), model field "local", bare `chat/completions` (`probe_plan_r11.md` §2).
- **Experimental-unit descriptors** (§Planned(b) — carried into every claim): first record pins the serving stack at run time — served model id from `/v1/models`, llama-server pid + full argv from `/proc/<pid>/cmdline` (best effort), temp/maxtok/system prompt, seed scheme, pid list, counterbalance rule. Round-10-known, expected in argv: `--cache-type-k/v q4_0` (4-bit KV), `--kv-unified`, `--parallel 2`, `--ctx-size 16384`, `--flash-attn on`, `--no-context-shift`, custom non-upstream template `qwen-coder-godspeed.jinja`. Every derived claim cites: *single served unit — Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS under this exact stack; no cross-model generalization* (`probe_plan_r11.md` §3).
- **Cost / burst budget**: 1 (descriptors) + 64×22 = **1409 endpoint requests** (1473 records total) — schema totals in `probe_plan_r11.md` §4; ≈5–8 min serial at r9's mean `wall_s` 0.215 (`power_analysis_r11.md` §Cost feasibility). n = 88 (d = 0.30) declined: marginal power gain does not justify doubling burst exposure.

## Preregistration & ordering

Bundle filed and hashed **before the first endpoint request**. `sha256sum -c corpus/evidence/round11-power/prereg-bundle.sha256` **from the repo root** → 3× `OK`, exit 0 (re-run 2026-09-28 by this scribe L2; note the F2-class cwd caveat — the file carries repo-relative paths, so `-c` must run from the repo root, per the round-10 critic's `r10-critic.md` F2):

| File | sha256 (`prereg-bundle.sha256`) |
|---|---|
| `corpus/evidence/round11-power/probe_plan_r11.md` | `d7fbeebe118ab2ea959d63c53e3f2d0a6eeec53b11dc155661d636c2a6ef27bf` |
| `corpus/evidence/round11-power/power_analysis_r11.md` | `ecfe96deb0b378303ae9a58e4445601682f0000367fdf1e75d6c4ed10176208e` |
| `corpus/evidence/round11-power/predictions-r11.md` | `e912085ce0283dd4a0cd5c2de31dde937f69d38e12e9e4970a3470d23c46a902` |

Bundle file itself: `prereg-bundle.sha256` = `bae0a5851a73b71619cfd5ab4dc2ea3027a2e4779cd60379ad5c079f18294c92` (sha256, computed 2026-09-28). Machinery as filed: `probe_r11.py` sha256 `cf754d78e9065d679aa64872766be748a9d349fc13acdc5d03c5ba41447bdaa7`, `run_r11.py` sha256 `2503ffc48bb180cbc27ac06af709ba11458f67891a9c2c118ba4c6a2945afb4f`; the run's own `descriptors` record re-derives `machinery_sha256` from `probe_r11.py` at run time (`run_r11.py:114-115`), so the run-time value is authoritative for the landed claim.

`ordering.log` (verbatim, `corpus/evidence/round11-power/ordering.log`):

```text
pre-hash 2026-09-28T23:10:20Z
post-hash 2026-09-28T23:10:20Z
bundle sha256 file prereg-bundle.sha256 (v1)
```

First endpoint `request_ts`: `{{FIRST_REQUEST_TS}}` (must postdate 23:10:20Z — the ordering half of the falsifiable target; read from the landed `results-r11.jsonl`).

Pre-run seed/schema precheck (`corpus/evidence/round11-power/prereg-precheck.log`, verbatim):

```text
generated: 64 distinct r11 problems: 64
old metas: 18 overlap with r11: 0
seed overlap r11&r9: 0 r11&r8: 0
ops-count distribution: {10: 64}
```

→ 64/64 problems generate, 0 duplicate an r8/r9 `init+ops`, both seed sets disjoint (the design-falsifier "any of the 64 seeds fails or duplicates" is unfired). Design-critic L2 (`CriticDesign`) gate verdict: **`{{VERDICT}}`** (must land before the first request per `probe_plan_r11.md` §6.2; a fatal defect → amend, re-hash v2, append new ordering lines). Wave-2 agents: `{{WAVE2}}`.

## L2 fleet (wave 1: 9 agents, one batched call)

Task column states role scope; L1 should transcribe each L2's own dispatch brief (`read history://<Id>:1-22`) at landing, as round 10 did. No L2 writes into the repo (single integration owner: L1); artifacts committed verbatim under `corpus/evidence/round11-fleet/`.

| Agent (role) | Task (dispatch brief — transcribe at landing) | Artifact (committed as `round11-fleet/…`) |
|---|---|---|
| CriticDesign (critic) | adversarial pre-run design critique of the prereg bundle; the gate that must return a verdict before the first endpoint request (`probe_plan_r11.md` §6.2) | `{{path}}` |
| ScoutGranularity (scout) | prior-art pricing of the granularity→severity construct against public literature, verdicts with fetched URLs — feeds §Prior-art pricing | `{{path}}` |
| ScoutPrereg (scout) | preregistration + ordering audit: bundle hashes, `ordering.log` timestamps, first-`request_ts` relation, pre-run seed/schema precheck | `{{path}}` |
| ConnectorFleet (connector) | sibling-lane gate conventions + overlap rulings for the r11 tree and grader extension (round-10 `r10-connector.md` lineage) | `{{path}}` |
| ReviewerBaseline (reviewer) | baseline review: r9/r8 committed bytes and cited local sources, citation resolution `≥90%` | `{{path}}` |
| ExecutorGrader (executor) | extend `grader.py` SUMMARY/check coverage to the r11 tree (parse `results-r11.jsonl` + `run.log`) so `python3 grader.py` exits 0 on the extended tree | `{{path}}` |
| ExecutorRecompute (executor) | `recompute_r11.py` — the stdlib-only analyzer producing `analysis_r11.md` in the §5 stored formats | `{{path}}` |
| ScribeReport (scribe) | this report skeleton + LOG entry skeleton (draft-only; L1 lands them — no repo writes) | `corpus/evidence/round11-fleet/r11-log-draft.md` |
| LabratMock (labrat) | mock-server smoke (`KENGAKU_R11_BASE`) — schema check only, bytes never mixed into committed results (`probe_plan_r11.md` §6.3) | `{{path}}` |

Wave 2: `{{WAVE2}}` (MISSION requires ≥8 L2/round; wave 1 alone clears it).

## Run results

Landed bytes: `corpus/evidence/round11-power/results-r11.jsonl` md5 `{{JSONL_MD5}}`, `run.log` md5 `{{RUNLOG_MD5}}` (r9 landing convention; grader pins them). Main run: `KENGAKU_R11_OUT` under `/tmp`, landed byte-identical.

- Census (`analysis_r11.md`): expected `1 descriptors, 64 meta, 320 graded, 960 ack, 128 fillers, 0 error records` → observed `{{CENSUS}}`.
- Observed analysis table (§5 stored format):

| Cell | Final passes / 64 | Mean final nwrong | Mean nwrong (all graded) |
|---|---:|---:|---:|
| A-CKPT4710 | `{{X}}`/64 | `{{a.aaa}}` | `{{b.bbb}}` |
| A-CKPT710 | `{{Y}}`/64 | `{{c.ccc}}` | `{{d.ddd}}` |

- Paired endpoint: `Paired mean difference (710 − 4710, shared checkpoints {7,10}): {{+m.mmm}} sd {{s.sss}} n=64`; `Paired t-test: t={{±t.ttt}}, df=63, two-sided p={{p.pppp}}`; `95% CI [{{l.lll}}, {{u.uuu}}]`; `Exact sign test: wins={{W}} losses={{L}} ties={{T}} two-sided p={{p.pppp}}`; `McNemar exact test on final passes: b={{B}} c={{C}} two-sided p={{p.pppp}}`.
- Finish/parse audit at graded turns: `finish=length {{L}}/320, parse fail {{P}}/320`; ack compliance `A-CKPT4710 {{a}}/{{b}} = {{c.c}}%; A-CKPT710 {{d}}/{{e}} = {{f.f}}%`.
- **Preregistered verdict**: `{{ESTABLISHED|DIRECTIONAL|FALSIFIED}}` — rule from `predictions-r11.md` §Preregistered verdict rule: `diff > 0` AND `p < 0.05` → ESTABLISHED; `diff > 0` AND `p ≥ 0.05` → DIRECTIONAL (MUST NOT be reported as established/replicated); `diff ≤ 0` → FALSIFIED. Sign test must agree in direction with the t-test, else the verdict downgrades to DIRECTIONAL regardless of the t p-value. Any significant McNemar on final passes is reported as a **new** pass-rate finding with its own prior-art pricing, never folded into the severity claim.
- Prediction scoring: point predictions `A-CKPT4710 final 15/64`, `A-CKPT710 final 13/64`, `paired severity diff +0.350` (shrinkage of r9's +0.500 by ~30% for selection bias) — scored `|predicted − observed| / 64` per `analysis_r11.md` table → `{{POINT_SCORES}}`. Probabilistic predictions scored with **Brier** = `(1/3) Σ (P − outcome)²`: P1 `mean paired diff > 0` = 0.78, P2 `two-sided p < 0.05 AND diff > 0` = 0.50, P3 `|passes(4710) − passes(710)| ≤ 8` = 0.60 → `Brier score (3 probabilistic predictions): {{0.bbb}}`; `Paired severity diff prediction: +0.350 predicted, {{±d.ddd}} observed, abs error {{e.eee}}`.

## Grader extension

`grader.py` SUMMARY/check coverage extended to the r11 tree this round, so the new numbers are recomputable at landing, not a round later (`SCORECARD.md` §Planned(c)).

- `python3 grader.py` on committed bytes → `{{CHECKS n=}}`, `mismatches={{M}} errata_pinned={{E}}`, `VERDICT: {{PASS|FAIL}}`, exit `{{0|1}}` (r10 baseline: `CHECKS n=149 mismatches=0 errata_pinned=1`).
- `python3 grader.py --selftest` → `{{SELFTEST}}` (expected exit 0, corruptions detected; r10 baseline: `S0` control + `S1` `ok`-flip, `S2` SUMMARY edit, `S3` raw-digit bump, each asserting exit code **and** check-id).
- Independent mutation battery (L2-written, executed on copies) → `{{MUTATION_BATTERY}}` (M0 control exit 0; ≥1 kill case per layer; kill rate `{{K}}`).

## Prior-art pricing

Fetched-URL verdicts per the novelty proxy (`fraction of the round's headline claims carrying a prior-art verdict with a fetched URL`, split phenomenon-new vs instrument-new). Scout: `ScoutGranularity`.

- Claims C1–C4: `{{C1–C4 verdicts + URLs}}` (phenomenon-new vs instrument-new counts `{{p/d}}`).
- Method/mechanism items M1–M3: `{{M1–M3}}` (e.g. the emission-granularity ablation construct, the paired shared-checkpoint severity unit, the non-iid-draws (llama.cpp #7052) threat carried from r9).

## SCORECARD before→after

Rows to fill from `SCORECARD.md` §Round-11 post-move (L1 owns the write):

| Axis | Before → After | What moved | Evidence |
|---|---|---|---|
| **novelty** *(owned)* | 5 → `{{N}}` | `{{novelty_move}}` | `{{ptr}}` |
| **calibration** *(owned)* | 7 → `{{N}}` | `{{calibration_move}}` | `{{ptr}}` |
| depth | 8 → `{{N}}` | `{{depth_move}}` | `{{ptr}}` |
| coverage | 7 → `{{N}}` | `{{coverage_move}}` | `{{ptr}}` |
| operability | 6 → `{{N}}` | `{{operability_move}}` | `{{ptr}}` |
| freshness | 6 → `{{N}}` | `{{freshness_move}}` | `{{ptr}}` |
| adjacency | 8 → `{{N}}` | `{{adjacency_move}}` | `{{ptr}}` |

Pre-move anchors (round-10 §Round-10 post-move): novelty 5, calibration 7, depth 8, coverage 7, operability 6, freshness 6, adjacency 8.

## Falsifiable-target checklist

Falsifiable target, quoted verbatim from `SCORECARD.md` §Planned (target sentence, pre-round `0c51208`):

> Falsifiable target: `ordering.log` predates the first `request_ts`; the predictions file states the n and effect size that would falsify the granularity-severity claim; `python3 grader.py` exits 0 on the extended tree and its `--selftest` still passes; prior-art verdicts carry fetched URLs.

| # | Clause (verbatim) | Status | Evidence |
|---|---|---|---|
| 1 | `ordering.log` predates the first `request_ts` | `{{MET/NOT-MET}}` | `ordering.log` 23:10:20Z (real); first `request_ts` `{{FIRST_REQUEST_TS}}` |
| 2 | the predictions file states the n and effect size that would falsify the granularity-severity claim | `{{MET/NOT-MET}}` | n=64, MDE d=0.35, falsifier `diff ≤ 0` (`predictions-r11.md`; real) |
| 3 | `python3 grader.py` exits 0 on the extended tree and its `--selftest` still passes | `{{MET/NOT-MET}}` | `{{CHECKS n=}}, exit {{0|1}}; selftest {{SELFTEST}}` |
| 4 | prior-art verdicts carry fetched URLs | `{{MET/NOT-MET}}` | `{{C1–C4 URLs}}` |

## Adjacency & report-outs

- `{{rulings}}` — cross-domain evidence named with owner and routed, not absorbed (round-10 tail: serving-plane config facts → integrator/unowned; `loop.sh` telemetry-source semantics → kumitate informational; operator read-only rule re-confirmed). Connector input: `ConnectorFleet` artifact.
- `{{report_outs}}` — report-outs appended to `PROVINCE.md` §Reported out.

## Confidence

- `{{graded lines}}` — one bullet per graded claim (ordering high; observed pass/`nwrong` high; paired t / sign-test high for arithmetic, medium for iid assumption across pids; granularity-severity interpretation medium — n=64 MDE d=0.35; single-served-unit descriptor high at capture, host-state caveat; Brier high for arithmetic).
- Standing caveat (round-10): grader PASS means the corpus agrees with itself, not that the model was good — no check touches the endpoint.

_Fill rule: every double-brace token is unfilled by design — L1 copies values from its own run output / the landed `analysis_r11.md` / the critic verdict; never from a second-hand artifact. Pre-run values (HEAD `0c51208`, the three bundle sha256s, `prereg-bundle.sha256` sha256, machinery sha256s, `ordering.log` 23:10:20Z pre/post, precheck 64/64 + 0 overlap) are already real and cited above. Delete a placeholder only if its line is deleted whole._