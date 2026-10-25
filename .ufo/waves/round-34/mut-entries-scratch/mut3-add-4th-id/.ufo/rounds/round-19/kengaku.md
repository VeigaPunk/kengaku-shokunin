# kengaku round 19 — goal-wave delivery report

Status: **ADMITTED with correction** (round 19 — the operator stopped the
10-round run here; rounds 20-28 do not run). Evidence commit: `0671bb0`
(records commit follows). Baseline: `05cb955`. Wave: one 32-seat flash call
on the zai bucket per the operator routing directive. Report time:
2026-10-16 ~08:45Z.

## Work performed

- Selected axis **calibration**: the first standing pre-registered probe
  battery (predictions frozen before any request, scored at close).
- 32-seat wave authored/froze/executed/scored the battery, built the
  reusable template, and audited its own freeze chain.

## Landed changes (evidence commit `0671bb0`)

- `plans/probe-battery-r19.md` — 9 probes / 30 components, FROZEN
  2026-10-16T07:55:58Z sha256 `e1a86777…`; `plans/probe-battery-TEMPLATE.md`
  (standing instrument); `corpus/knowledge/probe-battery-r19.md` (design +
  scored tables + limits); 15 receipts `corpus/evidence/probe-r19-*`.

## Before → after measurements (parent acceptance, 2026-10-16T08:40Z)

| Check | Before | After |
|---|---|---|
| standing battery / template | none | 1 / 1 |
| probes frozen pre-request | ad hoc (0/1, 1/1, 0/0, 1/1) | 9 frozen; 5 executed; ordering gate adjudicated |
| scored close | last in r11 | in-round: mean Brier 0.1836/11 (9 hit/2 miss); seat pool 0.0617/26 |
| receipts | — | 15, timestamp-ordered, audited |

## Corrections folded at admission

BR-1 freeze TOCTOU breached-and-repaired (re-freeze 07:55:58Z; stale-window
runs adjudicated unaffected); runner-leg-opencode DEFECT-0 (pre-battery
requests, self-filed, excluded); bookkeeping defects recorded; premise
correction — operator reordered both cascades post-r18, P4/P5 re-based
pre-freeze; P2/P3/P8/P9 UNRUN (named).

## SHONEN

- [ ] · [ ] · [ ] · [ ] — unchanged (no named non-author verifier).

Boundaries held: small probes only; credentials untouched; no fabricated
knowledge; no scalar axis scores; seats committed nothing.
