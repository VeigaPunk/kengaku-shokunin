# Ledger route telemetry

Source: `~/Projects/bounties/ledger/telemetry.jsonl` — 7,218 lines,
profiled 2026-09-28 with `json.loads` + `collections.Counter`. This is
the host's live **lane-routing** corpus (the "route telemetry" named in
PROVINCE.md), distinct from per-run eval telemetry
(`telemetry-run-design.md`).

**Source availability annotation (round-13 re-dispatch, additive only — historical profile, claims not re-verified):**

```
source-status: historical-unavailable
original-source: ~/Projects/bounties/ledger/telemetry.jsonl (7,218 lines profiled 2026-09-28 with json.loads + Counter)
availability-evidence: corpus/evidence/round13-coverage/surface-receipt.json observed 2026-10-15T04:49:50Z — ~/Projects/bounties/ledger/telemetry.jsonl absent (exact-path scope; per PROVINCE.md the tree went absent mid-round-11 — historical, never treat this path as live)
retained-evidence: baseline 3f31e54 digest of this entry sha256=76f6d2855c035521266dbc2c3969772a6f47fd52d4d437d58824995dc6856ae3; no raw ledger bytes retained in-corpus — retained digest and Counter-transcription are NOT recovered original bytes
recheck: test -e ~/Projects/bounties/ledger/telemetry.jsonl && echo present || echo absent
```

## Event taxonomy (top, n=7,202 events)

`dispatcher_tick` 3,680 · `mission_parked` 1,188 · `mission_dispatched`
1,167 · `fleet_synced` 249 · `freshness_check` 233 · `binding_verified`
224 · `lease_claimed` 107 · `attempt_reset` 68 · `operator_decree` 58 ·
`mission_retired` 31 · `mission_claimed` 31 · `mission_done` 26 ·
`lane_degraded` 24 · `mission_failed` 21 · `claim_rejected` 16.

Core keys present on nearly all rows: `ts`, `event`; enrichment keys:
`active`/`pending` (3,680 — dispatcher snapshots), `program` (2,742),
`model` (1,243), `adjusted_ev`/`freshness`/`pane` (~1,167 each),
`run_id` (591), `lane` (40), `cause` (14), `action` (75).

## Lane→model routing observed

`xai-oauth/grok-4.6:low` 621 · `openai-codex/gpt-daybreak-blue-latest:max`
276 · `openai-codex/gpt-6-astra:max` 123 · `xai-oauth/grok-4.6:xhigh` 91 ·
`alibaba-token-plan/qwen3.8-max:xhigh` 42 · `kimi-code/k3:max` 24 ·
plus long tail. Named lanes: `mission_l1`, `executor`, `scout`,
`labrat`, `judge`.

## Reroute/degrade signatures (the interpretation layer)

- `lane_parked` with `cause` ∈ {`usage_limit`, `usage_limit_until_*`,
  `empty_output`, `read_only_sandbox_EROFS`, `subagent exit 1`,
  provider-specific notes} → `action: reroute` with `to:` target;
  scope `GROUP` means lane identity preserved across provider swap.
- `lane_degraded` + `local degrade (I3)` = bucket walk exhausted all
  primaries; lane falls back to a local model **while keeping lane
  identity**.
- `attempt_reset` 68 vs `mission_done` 26 vs `mission_failed` 21 —
  resets are 3× completions; the ledger measures a fleet where retries
  dominate finishes.
- `operator_decree` 58 — human overrides are first-class events, not
  exceptions; any auto-interpretation must respect them.

## Falsifiable claims

1. A lane's effective model is a *sequence*, not a scalar: correct
   attribution of a mission's outcome requires replaying `lane_parked`/
   `reroute` chains for that `run_id`, not reading the last `model`
   field.
2. `usage_limit*` causes are provider-meter events, not model
   failures — count them separately when scoring model quality from
   this ledger.
3. `dispatcher_tick` rows carry `active`/`pending` counts; ratio of
   `mission_dispatched` (1,167) to `mission_parked` (1,188) ≈ 1.018 —
   parking and dispatch are near-symmetric, i.e. congestion, not
   starvation, dominates throughput.

## Errata + drift note (appended round 9)

- **`:3` "7,218 lines" is a point-in-time count of a live, growing surface.**
  Re-counted round 9 (2026-09-28): `wc -l < ~/Projects/bounties/ledger/telemetry.jsonl`
  → **7,224** (+6 since profiling). The taxonomy and routing counts below are
  frozen at the 7,218-line snapshot and are *not* re-derived; treat every number
  here as snapshot-scoped and re-run the counting command before citing a total.
  Routed by the round-6 aggregator audit
  (`corpus/lessons/round-6-aggregator-audit.md` defect 7: a count needs a
  re-runnable command, and this surface drifts).
- Ownership reminder (round 9 sibling map,
  `corpus/evidence/round9-fleet/sibling-overlap.md`): this lane reads the ledger
  for **model×lane and reroute inference** only; mission-state/dispatcher
  semantics belong to kasegi and route-resolution/failure taxonomy to kumitate.
