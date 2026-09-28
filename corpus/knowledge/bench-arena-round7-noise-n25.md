# bench-arena round-7 (L2) — noise tasks at n=25, non-iid draws

Executor L2 probe (2026-09-28), scoped to firm up the round-6 "sampling
noise" classification for `09-sql-top-n-per-group` and
`20-csv-group-sum`. Spec'd n=5; extended to n=25 + seed/mechanism probes
after window A looked unanimous. All artifacts under
`/tmp/bench-r7-l2-executor/` (`REPORT.md`, `matrix.md`, `summary.json`,
97 label dirs, graded reports). Same body as r6: direct API, temp 0.2,
max_tokens 4096, `enable_thinking:false`.

## Status at n=25

| Task | PASS/25 | Window fractions (A:1-5, B:6-15, C:16-20, D:21-25) | Distinct sol_sha |
|---|---|---|---|
| 09-sql-top-n-per-group | 17 (p=0.68; block-robust 95% CI ≈ 0.40–1.00) | 5/5, 6/10, 1/5, 5/5 | 13 |
| 20-csv-group-sum | 8 (p=0.32; block-robust 95% CI ≈ 0.05–0.70) | 4/5, 1/10, 3/5, 0/5 | 22 |

Cross-round pooled: 09 → 21/30 (0.70); 20 → 12/30 (0.40).

## Failure anatomy (the mode space is narrow even when text space is wide)

- **09 — one structured FAIL mode**: regex
  `WHERE[^;]*(DENSE_RANK|RANK)\s*\(\s*\)\s*OVER` matches 8/8 FAILs and
  0/12 PASSes (discordance 0/25). Error: `sqlite3.OperationalError:
  misuse of window function dense_rank()` — reproduced on the r5
  artifact. The r5 FAIL was the recurring minority strategy (~32%), not
  an anomaly.
- **20 — five FAIL modes**, all output-contract handling, not arithmetic:
  raw-header passthrough (×5, = the r5 draw), empty body (×5),
  values-into-key-0 awk slip (×4), per-row no-accumulation (×2), garbled
  multi-header (×1). **r6's 3/3 PASS was the lucky draw**; r5's FAIL was
  the modal outcome.

## Draws are NOT iid — the biggest methodological finding

- lag-1 autocorrelation: +0.32 (20), +0.26 (09); permutation test
  p ≈ 0.01 both; block means swing 0.8→0.1→0.6→0 (20) and
  1.0→0.6→0.2→1.0 (09).
- Mechanism probes (batch 1): `seed=42` twice → 09 byte-identical
  (deterministic given seed), 20 differed (even (prompt,seed)
  insufficient for 20); contiguous seed blocks flip 09 0/6→6/6 while 20
  moves the *opposite* direction — kills both "global time regime" and
  "seed-smoothness" hypotheses. Sibling-traffic contamination excluded:
  server `predicted_tokens` delta equals own-token sums exactly.
- Mechanism probes (second batch, replay/slot probe): output =
  f(prompt, seed, **burst state**), not f(prompt, seed). Evidence:
  09 `seed=42` → different texts across bursts (4ddf8915 vs 0f633119);
  20 `seed=42` replay breaks if a 09 request interleaves (b4e5d0cf →
  7f038a68, replicated twice — the interleaved run's text becomes the
  next replay's output). `/slots` polling shows slot assignment is
  task-scoped (20→slot0, 09→slot1) so slot state can't explain
  task-internal alternation. Unseeded stream is *structured*: 09 ×8
  alternates two shas period-2 — fresh per-request entropy can't do
  that; explicit seeds 1000–1005 → only 3 distinct texts (coarse
  seed→text map). Suspect `--cont-batching --parallel 2 --kv-unified`
  shared decode state; exact seed source for seed=4294967295 not
  externally observable.
- **Consequence**: n≤5 unanimity does NOT license stability —
  09 went 5/5 identical-sha then produced 8 FAILs in the next 20 draws.
  Identical-sha under the *unseeded* path is seed-stream recurrence × a
  locally peaked output function — not status stability. Report
  per-task pass-rate with block-robust intervals, not per-draw Wilson;
  never read n=3 unanimity as settled when p̂ is interior.

## Grader sanity (rules out harness artifact)

Reference sol PASS×2, mutated FAIL×2, fence-less → HARNESS_DEFECT×2
under the same `BENCH_ROOT`. 0 HARNESS_DEFECT in all 50 headline reps.

## Updates to prior corpus claims

- `bench-arena-round6-stability.md`: "sampling noise" verdict holds for
  09/20, but gains tilt — **09 PASS-tilted (0.68), 20 FAIL-tilted
  (0.32)**; and the draws are order-coupled, so n=3 unanimity was weaker
  evidence than credited.
- SKILL.md parsing rules: add the non-iid correction (see SKILL).
