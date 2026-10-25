# kengaku round 20 — goal-wave delivery report

Status: **ADMITTED** (round 20). Evidence commit: `af0e3e6` (records commit
follows). Baseline: `f330e2b` (round-19 records). Wave: one 32-seat zai-flash
call. Report time: 2026-10-16 ~10:00Z.

## Work performed

- Selected axis **calibration**: closed the r19 battery's 4 UNRUN probes
  against the unchanged frozen predictions.
- 32-seat wave executed P2/P3/P8/P9 (9 requests, zero retries), extended the
  scored tables + aggregate, hardened the template, and audited etiquette.

## Landed changes (evidence commit `af0e3e6`)

- 4 receipts (`probe-r19-P2-servicetier.log`, `P3.log`, `P8-kimi-code-auth.log`,
  `P9-absent-port.log`); `corpus/knowledge/probe-battery-r19.md` §10 (scored
  extension + 9/9 provenance grid); `plans/probe-battery-TEMPLATE.md` (freeze-
  after-last-edit guard, unrun-completion checklist); lesson
  `corpus/lessons/2026-10-16-round20-grid-closure.md`.

## Before → after measurements (parent acceptance, 2026-10-16T09:55Z)

| Check | Before | After |
|---|---|---|
| battery grid | 5/9 (4 UNRUN) | 9/9, per-round provenance |
| combined mean Brier | 0.1836/11 | 0.0998/46 (r20 binaries 0.1495/20) |
| P2 service-tier vector | unmeasured | [200,200,400,200,400,400,400] — all 7 legs match frozen predictions |
| 3c (used-percent) | frozen <=2 | observed 7 — FALSIFIED (route drift, scored MISS) |
| receipts | 15 | 19 |

## Named

- The 3c miss is the instrument working: it localizes a route-state change
  between r18 census and now.
- Novelty scout: latency-fingerprinting is crowded prior art; r21 registered
  as N1 (blind leg attribution with shim-journal ground truth).

## SHONEN

- [ ] · [ ] · [ ] · [ ] — unchanged (no named non-author verifier).

Boundaries held: small probes only; credentials never read; freeze verified
before every request; seats committed nothing.
