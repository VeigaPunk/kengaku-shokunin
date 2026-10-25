# kengaku round 22 — goal-wave delivery report

Status: **ADMITTED with correction** (round 22). Evidence commit: `8a08483`
(records commit follows). Baseline: `78245e1` (round-21 records). Wave: one
32-seat zai-flash call; 4 seats lost to provider empty responses (scorer /
reviewer / scribe / determinism) — scoring independently covered. Report
time: 2026-10-16 ~13:20Z. Operator routing after this wave: back to the
deepseek bucket for subsequent waves.

## Work performed

- Selected move: cover the r21-UNTESTED legs via forced fallback, and fold
  the attribution instrument into the standing battery as probe-type P10.
- The wave built instrument v2 (leg-forcing mode), froze the v2 table through
  three pins (one defective, superseded pre-request), ran 40 forced trials,
  ablated the new features, and named the opencode-go starvation gap.

## Landed changes (evidence commit `8a08483`)

- `plans/attrib_probe.py` v2 (`bb6bd919…`): `cmd_force_trials` with v2-table
  + ds-only gates, two forcing bodies, `body_schema`/`id_in_body` features,
  stream-flag GT join, per-target verdicts.
- `plans/attrib-r22-frozen.md` (live pin `77b8d4a0…`);
  `corpus/evidence/attrib-r22-legs.log` (+ `-hyper` + `-opencode-trials`);
  battery P10 fold (`plans/probe-battery-TEMPLATE.md` + battery §11);
  integrator-written r22 addendum in `corpus/knowledge/attrib-r21.md`;
  r21 lesson `attribution-freeze-surface` (backfilled).

## Before → after measurements (parent acceptance, 2026-10-16T13:15Z)

| Check | Before | After |
|---|---|---|
| hyper leg attribution | UNTESTED | COVERED: run-2 10/10 on-target = 1.000 (bar 0.80) |
| opencode-go | UNTESTED | NAMED GAP: 0 on-target (echo-bait starves vs reasoning models; T03 proved reachable) |
| overall forced trials | — | run-2 20/20 = 1.000; ablations: hdr_tells LOO 19/20 load-bearing |
| battery | 9 probe types | +P10 attribution health-check |

## Named

- Forced coverage != natural coverage (critic) — hyper validated on forced
  serves only.
- 4 provider-loss seats; r22 addendum integrator-written from authoritative
  receipt blocks.
- r23 registered: opencode-go forcing via the stream-path header
  leg-selection.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — unchanged.

Boundaries held: freeze-before-trials (three-pin history); journal GT post-
trials; 40 small requests; credentials untouched; seats committed nothing.
