# Bailian CLI telemetry corpus

Source: `~/.bailian/telemetry.jsonl` — 4,274 JSONL records, span
2026-08-21 → 2026-09-16, profiled 2026-09-28 (audit-requested
route/provider telemetry entry; distinct from the bounties ledger —
this is **client-side CLI telemetry**, not lane routing).

**Source availability annotation (round-13 re-dispatch, additive only — original path and read date above are historical):**

```
source-status: historical-unavailable
original-source: ~/.bailian/telemetry.jsonl (client CLI telemetry, 4,274 records; profiled 2026-09-28 under the absent ~/.bailian root)
availability-evidence: corpus/evidence/round13-coverage/surface-receipt.json observed 2026-10-15T04:49:50Z — ~/.bailian absent (exact-path scope; entry claims not re-verified here)
retained-evidence: baseline 3f31e54 digest of this entry sha256=3a95b8e49ffc3253c65275803530631138ee27afddbd2b008cb3a0804d9b08c6; no raw telemetry bytes retained in-corpus — retained digest and transcription are NOT recovered original bytes
recheck: test -e ~/.bailian/telemetry.jsonl && echo present || echo absent
```

## Record shape

Flat per-invocation record: `command`, `timestamp`, `durationMs`,
`success`, `cliVersion` (1.17.0), `nodeVersion`, `os`, `authMethod`,
plus conditional `errorMessage`, `httpStatus`, `requestId`,
`exitCode`, `params`. No `type`/`event` discriminator — every row is
one command invocation.

## Distribution (computed)

| command | calls | failures |
|---|---|---|
| `usage token-plan` | 3,202 | 2,733 (85%) |
| `video task get` | 665 | 500 (75%) |
| `video generate` | 227 | 163 (72%) |
| `video download` | 38 | 10 |
| `auth status` / `config show` | 30 / 25 | ~0 |
| `text chat` | 18 | 5 |

- `httpStatus`: **429 × 675** (all `usage token-plan` — "token-plan
  1-week quota exhausted"), 404 × 8.
- Top error messages: "Console session is not logged in or has
  expired" × 2,685; quota-exhausted × 675; "No console access token"
  × 62.
- `durationMs` median 2,571 / p90 3,082 / max 1,045 s (a video task).
- Poller signature: `video task get` is the async-task poll verb —
  its 75% failure rate is task-pending noise, not service failure.

## Interpretation rules

1. **Distinguish meter events from model events** (same rule as the
   bounties ledger): a 429 quota row is provider-side capacity, not
   evidence about model quality; a `video task get` failure row is
   async-pending, not an error. Group by `command` before reading
   `success`.
2. **Auth expiry is the dominant failure class** (2,685/3,434 rows
   with `errorMessage`) — when this corpus shows mass failure, check
   `authMethod`/console-session errors first, quota second.
3. **Poll verbs need separate treatment**: rate-limit the reading of
   `task get` rows; their failure rate carries task-state, not
   service-health information.
4. Absence of `model` fields: this corpus cannot rank models — it
   ranks *endpoints/commands*. Model attribution needs the lane
   ledger (`corpus/knowledge/ledger-route-telemetry.md`).
