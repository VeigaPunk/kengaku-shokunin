# kengaku round 21 — goal-wave delivery report

Status: **ADMITTED** (round 21). Evidence commit: `0d23c61` (records commit
follows; r20 evidence backfill `96b8962` precedes). Baseline: `3688f76`
(round-20 records). Wave: one 32-seat zai-flash call, 31/32 (scorer seat
failed — remit covered by the instrument's adjudicated scoring + an
independent recount; named in the verdict). Report time: 2026-10-16 ~11:15Z.

## Work performed

- Selected axis **novelty** (N1 from the r20 scout): blind cascade-leg
  attribution with shim-journal ground truth, prior-art scoped honestly.
- 32-seat wave built the frozen feature-table instrument, ran 42 blind
  trials across both shims, ablated it 11 ways, and priced its novelty.

## Landed changes (evidence commit `0d23c61`)

- `plans/attrib_probe.py` (stdlib-only: block-sha / freeze-check / trials /
  score — journal access structurally post-trials only) +
  `plans/attrib-r21-frozen.md` (FROZEN 10:20:08Z `9f0244bb…`);
  `corpus/evidence/attrib-r21-{impl-ds,impl-glm,ds,glm}-trials.log`;
  `corpus/knowledge/attrib-r21.md` + `attrib-prior-art-r21.md`.

## Before → after measurements (parent acceptance, 2026-10-16T11:10Z)

| Check | Before | After |
|---|---|---|
| blind leg attribution | no instrument exists | 100% ds (20/20), 100% glm (22/22; GT zai 13/devin 9) |
| ablations / mimicry | n/a | 11/11 at 1.000 (8 LOO + header-strip, latency-pad, echo-spoof) |
| freeze discipline | r19 TOCTOU lesson | frozen 10:20:08Z < trials < first journal read 10:25:25Z |
| requests | — | 44 small localhost calls, >=2.5s spacing, no credentials |

## Named

- hyper/opencode-go legs: 0 GT trials — UNTESTED, r22's registered coverage
  move; the battery-fold (attrib as standing probe P10) is r22's second act.
- Novelty scoping: instrument + GT-protocol, phenomenon-incremental (prior
  art cited: LLMmap, Model Equality Testing, AdaptPrint, 2605.29979,
  2411.01076, 2412.15431, 2409.20002, 2605.14786).
- Adjacency: critic's mori-province pass answered in-note (measurement, read-
  only journal, no remediation).

## SHONEN

- [ ] · [ ] · [ ] · [ ] — unchanged (no named non-author verifier).

Boundaries held: freeze-before-trials; journal GT post-trials only; small
requests; credentials never read; seats committed nothing.
