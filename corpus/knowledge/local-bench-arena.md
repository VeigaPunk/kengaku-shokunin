# Local bench-arena battery

Source: `~/bench-arena/` — files verified by `ls`, `csv.DictReader` on
2026-09-28: `tasks/01…33` (33 task dirs), `grade.sh`, `loop.sh`,
`report-qwenlocal.csv`, `report-qwenlocal-v2.v2.csv`, `report-grok45.csv`,
`telemetry-qwenlocal-v2.csv`.

## Corpus shape

33 single-file tasks covering: string ops (01–06 incl. regex/log-parse),
SQL (07–09), algorithms (10–12: binary search, kth-largest, knapsack),
data structures (13–15: stack-min, LRU-TTL, interval-tree), correctness
traps (16–17, 31–33: off-by-one, mutation, mutable-default, closures,
metaclass), concurrency (18, 21, 25–27), bitwise/serial (28–30), file
transforms (19–20, 23–24).

## Telemetry schema (`telemetry-qwenlocal-v2.csv`, 33 data rows)

`task, status, opencode_rc, closed_fence, output_sha256, prompt_tokens,
predicted_tokens, inference_latency_ms, tokens_per_sec, test_runtime_ns,
telemetry_source, telemetry_available`

- `telemetry_source` = `journal` for all 33 rows.
- `telemetry_available` = `n` on exactly 1 row (`20-csv-group-sum`),
  whose `inference_latency_ms` is the string `NULL` — parse defensively,
  do not assume numeric.

## Measured results (computed this round, command output)

- qwenlocal-v2: **PASS 21/33**; latency median 75.3 ms (min 6.1, max
  1157.5, n=32); tokens/sec median 129 (123.4–166.4).
- grok45 (`report-grok45.csv`, status-only): **PASS 19/33**.
- FAIL latency median 60.9 ms < PASS median 79.5 ms — failures return
  faster, consistent with early bail rather than timeout.

## Cross-model complementarity (33 common tasks)

- grok45-only wins (8): 02-parse-log-line, 04-ipv4-regex,
  06-balanced-html-regex, 08-sql-group-window, 19-batch-rename,
  23-pivot-json, 24-json-diff-patch, 31-mutable-default-arg.
- qwenlocal-only wins (10): 03-extract-isodatetimes, 10-binary-search,
  11-kth-largest, 13-stack-min, 14-lru-ttl, 15-interval-tree,
  16-off-by-one, 17-mutation-side-effect, 18-thread-counter,
  26-bounded-queue.
- Both fail (4): 05-semver-regex, 12-knapsack-reconstruct,
  27-rwlock-writer-pref, 33-metaclass-shadowing.

## Falsifiable claims

1. The two models' win-sets are near-disjoint (8 vs 10, 2 overlap-free):
   aggregate pass deltas hide per-class complementarity. Head-to-head
   pass rate alone would wrongly rank qwenlocal (21>19) as uniformly
   better.
2. Failure clusters by task class: grok45 loses on stateful/DS tasks
   (LRU, interval tree, bounded queue); qwenlocal loses on regex/format
   transforms. Prediction for next battery: a router keyed on task-class
   beats either single model — directly testable on this corpus.
3. `12-knapsack-reconstruct`, `05-semver-regex`, `27-rwlock-writer-pref`,
   `33-metaclass-shadowing` are discriminating tasks (both fail) — keep
   them in any local battery; dropping them removes headroom signal.
