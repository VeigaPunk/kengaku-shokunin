# bench-arena fresh run — round-4 reproduction slice

First end-to-end eval executed by this domain (2026-09-28), against
`~/bench-arena/` tasks. Not an analysis of prior artifacts — an authored run.

**Source availability annotation (round-13 re-dispatch, additive only — historical run, claims not re-verified):**

```
source-status: historical-unavailable
original-source: ~/bench-arena/ (tasks/, loop.sh, grade.sh, reports; run executed 2026-09-28; the round-14 record's ~/archive/bench-arena/ relocation stays historical — receipt observed both roots absent)
availability-evidence: corpus/evidence/round13-coverage/surface-receipt.json observed 2026-10-15T04:49:50Z — ~/bench-arena and ~/archive/bench-arena absent, ~/.config/systemd/user/qwen-coder.service and ~/.config/llama/qwen-coder-godspeed.jinja absent, http://127.0.0.1:34113/health connection refused (exact-path scope only)
retained-evidence: baseline 3f31e54 digest of this entry sha256=b17665c24447549fceb37c5e6cdd998ea6ef73f73c5ee1cdbdb0996c67459f0e; retained raw r10 endpoint capture corpus/evidence/round10-fleet/models-34113.json (historical, not a live model); no task/CSV bytes retained; /tmp/bench-r4 predictions not retained — no original bytes recovered
recheck: test -e ~/bench-arena/loop.sh && echo present || echo absent; test -e ~/archive/bench-arena/loop.sh && echo present || echo absent
```

## Harness facts (verified live)

- `~/bench-arena/loop.sh` runs `opencode run --agent raw --model "$MODEL"` per
  task, scrapes `/metrics` (`LLAMA_METRICS_URL`, default `127.0.0.1:8080`),
  falls back to `journalctl -u qwen-coder.service` `print_timing` lines when the
  metrics scrape fails, then calls `grade.sh` (extracts first closed fenced
  block → `timeout 60 bash tasks/<t>/test.sh`).
- **Drift finding**: `~/.config/opencode/opencode.json` provider `qwen-local`
  still points at `baseURL http://localhost:8080/v1`, but the live server
  (`qwen-coder.service`, llama-server, `Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS`)
  listens on `127.0.0.1:34113` (confirmed `/v1/models`, `/health`); `8080` is
  occupied by Jitsi. The harness's metrics fallback therefore degrades silently
  — likely origin of the `telemetry_available=n`/`"NULL"` rows in v2.
- Round-4 run used direct `/v1/chat/completions` (temperature 0.2, max_tokens
  4096, `enable_thinking:false`) — deliberately minimal, no agent scaffold.
  This is a different pipeline than opencode (`--agent raw` still injects a
  system prompt); deltas below are pipeline+sampling effects.

## Run record

Slice: 4/33 tasks chosen to mix prior-pass/prior-fail and both-model-fail.
Ex-ante predictions (recorded before run, `/tmp/bench-r4/predictions.md`):
01=PASS, 02=FAIL, 03=PASS, 05=FAIL; aggregate 2/4.

Observed (grade.sh, BENCH_ROOT=/tmp/bench-r4):

| task | v2 (Aug 29) | round-4 | wall | completion_toks |
|---|---|---|---|---|
| 01-reverse-words | PASS | PASS | 1.2 s | 135 |
| 02-parse-log-line | FAIL | FAIL | 3.0 s | 446 |
| 03-extract-isodatetimes | PASS | **FAIL** | 14.7 s | 2,151 |
| 05-semver-regex | FAIL | FAIL | 0.7 s | 81 |

Aggregate 1/4 vs predicted 2/4. Per-task predictions 3/4 correct; aggregate
missed because 03 flipped.

## Falsifiable claims

1. **01 and 02 are stable signal**: identical verdicts across Aug-29 and
   Sep-28 pipelines — usable as regression canaries; 05 stays both-model-fail.
2. **03 flip is sampling/pipeline noise, not server regression**: health and
   `/v1/models` agree with the Aug-29 config; sol_sha differs (fresh
   generation); tokenizer path unchanged. At n=1 per task, a near-boundary
   task can flip on temperature alone — per-task repeat counts matter for
   status claims.
3. **FAIL-faster-than-PASS is subset-dependent, not universal**: this slice
   breaks the pattern (01 PASS 1.2 s is fastest; 03 FAIL 14.7 s is slowest,
   driven by a 2,151-token solution). The round-3 signature (FAIL median
   60.9 ms < PASS 79.5 ms) held on that 33-row population, not per-task.
4. **Grader is transport-agnostic**: `grade.sh` accepts any
   `out/<label>/<task>.txt` shape — the telemetry pipeline and the model
   interface are separable; a broken provider entry does not invalidate
   task/test assets.
5. **Closed-fence invariant held**: 4/4 outputs carried a single closed
   ```python block; fence detection is not the fragile stage.

## Reproduce

```
mkdir -p /tmp/X/tasks && for t in <tasks>; do ln -s ~/bench-arena/tasks/$t /tmp/X/tasks/$t; done
# per task: POST 127.0.0.1:34113/v1/chat/completions with prompt.md as user msg
cd ~/bench-arena && BENCH_ROOT=/tmp/X bash grade.sh <label>
```

Artifacts (ephemeral): `/tmp/bench-r4/{run.py,telemetry-kq-r4.csv,out/,graded/,report-kq-r4.v2.csv,predictions.md}`.

## Errata (appended round 10, never an in-place edit)

- **§Harness-facts causal chain "metrics fallback degrades silently → origin of
  the `telemetry_available=n`/NULL rows" — FALSIFIED by round-10 re-derivation**
  (scout L2, `local://r10-scout-bench.md` claim C; commands re-run on this
  host). The port facts reproduce exactly (8080 is Jitsi JVB — `curl
  -s -m3 http://127.0.0.1:8080/metrics` → HTTP 200, 27461 B,
  `application/openmetrics-text`, body `jitsi_jvb_bytes_sent_total`;
  llama-server live on 34113; `opencode.json:158` baseURL
  `http://localhost:8080/v1`). But the mechanism is a **field-count bug in
  `loop.sh`**: `:32` emits 5 comma fields while `:63` reads 6 vars
  (`read -r pt et pms em tps mok`) → `tps=[1] mok=[]` → `BRANCH=journal`
  **unconditionally**, whatever `METRICS_URL` answers (proved with
  `bash -c 'IFS=, read -r pt et pms em tps mok <<< "0,0,0.000,0.000,1"; …'`
  and by running loop.sh's own `metric_snapshot`+`metric_delta` verbatim vs
  live 8080). Hence v2's `telemetry_source=journal` on 33/33 rows
  (`awk -F, 'NR>1{print $11}' telemetry-qwenlocal-v2.csv | sort | uniq -c` →
  `33 journal`) is this bug, **not** the 8080/34113 mismatch; and the premise
  "the metrics scrape fails" is false today — `curl -fsS --max-time 2
  http://127.0.0.1:8080/metrics` exits 0 (with `grep -icE 'prompt|eval'` = 0
  over the body, so a *corrected* reader pointed at 8080 would silently log
  zeros rather than fall back). NULL detail: exactly **1** row carries
  `telemetry_available=n` (`20-csv-group-sum`, 4 NULL cells); 32/33 are `y`
  — "rows" (plural) and the attribution to port drift were both imprecise.
  The `loop.sh` fix belongs to the bench-arena tooling owner; recorded here
  and reported out, not patched in-place (operator rule: domain surfaces
  read-only for this lane mid-round).
