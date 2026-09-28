# bench-arena round-5 — full 33-task battery under live endpoint

Second executed eval by this domain (2026-09-28); first full-battery authored
run. Extends `bench-arena-fresh-run.md` (4-task slice) to all 33 tasks.
Same pipeline: direct `POST /v1/chat/completions` → `127.0.0.1:34113`
(Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS), temp 0.2, max_tokens 4096,
`enable_thinking:false`, no system prompt, n=1 per task, graded by repo
`grade.sh` (BENCH_ROOT=/tmp/bench-r5). Artifacts ephemeral under `/tmp/bench-r5/`.

## Predictions vs observed

Ex-ante record: `/tmp/bench-r5/predictions.md` (written before first request).

| Level | Predicted | Observed | Hit? |
|---|---|---|---|
| Aggregate | 20/33 PASS (range 17–22) | **20/33 PASS** | exact |
| Per-task | 1 flip off v2 (21 P→F) | **8 status flips** (4 P→F, 3 F→P, 1 F→HARNESS_DEFECT) | 9/33 tasks mis-called |
| 03-repeat | (implicit) noisy | FAIL again — 2× FAIL on direct-API vs PASS on opencode v2 | consistent |

The aggregate was exactly right for the wrong reason: win-set churned by
8/33 (24%) while the count stayed at ~21. **Aggregate PASS count is not a
stability metric** — a battery can hold its headline number while a quarter
of the win-set rotates. Supports `local-bench-arena.md`'s diff-win-sets rule.

## Flips (v2 → r5)

| Task | v2 (opencode) | r5 (direct API) | Reading |
|---|---|---|---|
| 03-extract-isodatetimes | PASS | FAIL | n=2 direct-API FAILs vs n=1 opencode PASS → pipeline-sensitive, see below |
| 08-sql-group-window | FAIL | PASS | boundary task, favors bare API |
| 09-sql-top-n-per-group | PASS | FAIL | |
| 12-knapsack-reconstruct | FAIL | PASS | hardest flip — long-generation task |
| 13-stack-min | PASS | FAIL | |
| 20-csv-group-sum | PASS | FAIL | v2's NULL-telemetry row also failed-ish; now clean FAIL |
| 31-mutable-default-arg | FAIL | PASS | predict-output task, sha differs from v2 |
| 06-balanced-html-regex | FAIL | HARNESS_DEFECT | not a flip — see below |

## Harness / generation events

- **06 hit the output cap, not a wrong answer.** `finish_reason=length`,
  completion_toks=4096, wall 29.1 s — the model tried to expand a
  depth-bounded regex literally (`<(?:[^<]|<tag>...` nesting) and ran out of
  tokens; grader found no closed fence → HARNESS_DEFECT. This is a
  **truncation failure class**: the fence extractor cannot distinguish
  "no block emitted" from "block never closed because generation was cut."
  Signal: `finish=length` + fence_found=0 → treat as model-limitation FAIL,
  not harness fault; raise max_tokens or instruct compaction before
  re-running.
- **Sub-second tasks produce sub-20-token outputs on predict-* tasks.** 25
  (0.14 s, 9 tok), 31 (0.18 s, 16 tok), 33 (0.15 s, 11 tok): these tasks ask
  for printed output, not programs; the fenced block is the *predicted
  stdout*. Correct and cheap — do not conflate tiny completion counts with
  degenerate output; check task class first.
- **FAIL rows are slower than PASS at every level on this run**: median
  wall 1.71 s vs 0.84 s, median completion tokens 260 vs 128. Opposite sign
  from the v2 inference-latency signature (FAIL median 60.9 ms < PASS 79.5 ms)
  — confirming round-4 lesson 3: latency-by-status is population- and
  pipeline-dependent, never a per-task law. Direct-API FAILs cost more
  because the model generates longer wrong solutions.

## Byte-identical solutions across pipelines

Five tasks emitted `sol_sha256` identical to v2 despite different harness
(opencode + system prompt vs bare API): **16, 25, 28, 32, 33**. All are
small deterministic-output tasks (bit ops, loop closures, predict-output).
Two consequences:

1. At temp 0.2, convergent tasks collapse to a canonical solution that
   survives scaffold changes — **scaffold sensitivity is task-class-
   dependent**, concentrated in open-ended tasks (03, 09, 13, 20 all have
   non-trivial solution spaces).
2. The equality includes a *stable FAIL* (33-metaclass-shadowing): the model
   deterministically produces the same wrong answer across pipelines —
   capability gap, not sampling noise.

## Canary update (stable cross-pipeline verdicts)

| Verdict | Tasks |
|---|---|
| Stable PASS | 01, 07, 10, 11, 14, 15, 16*, 17, 18, 21, 22, 25*, 26, 28*, 29, 30, 32* (* = byte-identical) |
| Stable FAIL | 02, 04, 05, 19, 23, 24, 27 (test-timeout 124 at 60 s), 33* |
| Pipeline-sensitive | 03 (P/F/F), 06 (F/truncated), 08, 09, 12, 13, 20, 31 |

Task 27's FAIL was a **test-side 60 s timeout** (`test_rc=124`) in both runs.
Round-6 root-cause (`bench-arena-task27-timeout-anatomy.md`): not slow, and
not merely wrong — a hidden-contract deadlock. Six reader threads crashed on
the underspecified private attr `rw._active` (absent from `prompt.md`); the
main thread hung forever on `Barrier(7)` of dead parties. The reference
passes the entire test in 0.23 s, and the r5 sol was semantically broken
underneath the hang (`release unlocked lock`, writer-preference violation).

## Prediction-calibration delta

Round-4 lesson: per-task and aggregate calibrate separately. Round-5 data:
aggregate exact (20 vs 20), per-task 24/33 correct on *status* but only
~6/9 on the flip question I actually predicted. Recording a flip count
("1 predicted flip") was the wrong frame — the actionable quantity is
*per-task confidence*, since flips arrive from both directions.

## Reproduce

```
mkdir -p /tmp/X/{tasks,out/<label>}
for t in ~/bench-arena/tasks/*/; do ln -s "$t" /tmp/X/tasks/; done
# /tmp/bench-r5/run.py pattern: per task POST chat/completions, write
# content to out/<label>/<task>.txt, log wall+usage to telemetry CSV
cd ~/bench-arena && BENCH_ROOT=/tmp/X bash grade.sh <label>
```

Artifacts (ephemeral): `/tmp/bench-r5/{run.py,run.log,telemetry-kq-r5.csv,
predictions.md,out/kq-r5/,graded/kq-r5/,report-kq-r5.v2.csv}`.
