# Lessons — round 12 (powered ladder, dissociation, transport)

Source: `LOG.md` round-12 entry; `corpus/evidence/round12-ladder/`;
`corpus/evidence/round12-fleet/`; independent verification in
`corpus/evidence/round14-fleet/r14-critic-landed.md` and
`corpus/knowledge/bench-arena-round12-ladder.md`.

Round 12 extended one powered pairwise contrast into an ordered four-point
emission-density ladder, isolated batching from emission sparsity, tested the
contrast on a second task family, and filed 416 per-problem forecasts.

1. **Ordered alternatives need ordered tests.** Page's trend test over
   within-problem midranks used the prespecified order directly. Three paired
   tests would multiply decisions; Friedman plus post-hoc would discard the
   order. The landed result was `L=1773.0`, `z=+9.452`,
   `LADDER ESTABLISHED`.
2. **A power floor is a measurement.** The draft's unsupported floors 56/42
   were falsified. Committed seeded simulation produced 44/44; the contingency
   rule and floors were then hashed before the run.
3. **Do not pool heterogeneous forecasts without naming the mixture.** The
   416 pass events, 304 sign events, and 7 run-level events have different
   reference classes. Report each separately; the pass-event result was Brier
   `0.1288`, BSS `+0.0447`, calibration slope `+0.8427`.
4. **Per-item probability tilts must preserve group marginals.** The first
   difficulty tilt moved arm means away from their filed base rates. A per-arm
   logit offset, solved with the clipping rule inside the target, restored
   agreement between point forecasts and per-problem probabilities.
5. **Repeatability is not replication.** The r11 contrast was re-measured on
   the same unit, problems, and seeds: r12 `+0.297` versus r11 `+0.352`.
   Multi-slot generation is not deterministic, but this still is
   `REPEATS-r11`, not an independent replication.
6. **A floor is a result.** The transport family landed at `2/48` in both arms.
   Its severity contrast was directional (`+0.177`, `p=0.2571`), not positive
   transport; the floor also exposed the predictor's failed family-2 base-rate
   transfer (BSS `-3.1474`).
7. **Decompose confounded arms before assigning mechanism.** `A-MONO` differed
   from incremental arms in both batching and emission frequency. Adding
   `A-CKPT10` held emission count at one; `MONO-CKPT10=+0.656` established the
   batching/emission dissociation on this unit and problem set.
8. **Critic defects belong before the hash.** The design critic returned
   DO-NOT-RUN (1 FATAL, 5 MAJOR, 4 MINOR). Every defect was absorbed before
   `prereg-bundle.sha256` v1, with the amendment log inside the hashed plan.
9. **Pin landed bytes, not draft bytes.** Fleet drafts recorded stale
   `analysis_r12.md` hashes after the file was regenerated. Round 14 pins the
   landed md5 `029c3bcd…`; regeneration remains path-dependent by one
   `Generator source` line although every statistic reproduces.
