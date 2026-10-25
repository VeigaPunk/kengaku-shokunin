# Lessons — round 3

Evidence: LOG.md round-3 entry; commit pending `round-3`; report
`~/projects/shokunin/.ufo/reports/round-3/kengaku.md`; analysis runs
documented in `knowledge/local-bench-arena.md` and
`knowledge/ledger-route-telemetry.md`.

## 1. Real telemetry surfaces were already on-host

The round-1 corpus gap "no provider-route telemetry found" was wrong in
kind: `~/Projects/bounties/ledger/telemetry.jsonl` (7,218 lines) is a
live lane-routing corpus and `~/bench-arena/` is a completed two-model
battery. Lesson: `find -iname "*telemetry*"` hit both on round 1 — the
miss was a *search-then-judge* failure (I pattern-matched filenames to
"irrelevant harness"), not a coverage failure. Follow the file list one
level deeper before declaring a gap.

## 2. Pass-rate deltas hide complementary win-sets

grok45 19/33 vs qwenlocal 21/33 looks like a 2-task edge; the per-task
diff is near-disjoint (8 vs 10 unique wins, regex/format vs DS/stateful
split). Lesson: report win-set diffs alongside pass rates; a router by
task-class plausibly beats either model alone on this corpus.

## 3. Real telemetry needs defensive parsing

`20-csv-group-sum` has `inference_latency_ms: "NULL"` (string) and
`telemetry_available: "n"` — a naive `float()` crashes the whole row
scan. Lesson: any telemetry ingestion path must treat missing/NULL
fields as a first-class row state, not an exception; `telemetry_available`
is the schema's own flag for this.

## 4. FAIL latency < PASS latency is a signature, not noise

Median 60.9 ms (FAIL) vs 79.5 ms (PASS) on the same model — failures
return earlier (early bail). Lesson: latency distribution by status is
a cheap pre-filter for "model quit early" vs "model timed out" failure
modes without opening logs.
