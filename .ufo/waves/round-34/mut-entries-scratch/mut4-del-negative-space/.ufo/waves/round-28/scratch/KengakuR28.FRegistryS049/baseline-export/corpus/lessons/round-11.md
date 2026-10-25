# Lessons — round 11 (powered preregistered rerun)

Source: LOG.md round-11 entry; `corpus/evidence/round11-power/` +
`corpus/evidence/round11-fleet/` (critic design review, labrat mock smoke,
grader integration, mutation battery).

1. **Mock-smoke the runner before an ordering-sensitive run.** LabratMock's
   stdlib mock server caught `run_r11.py`'s missing `import json` (NameError
   at the first record) with zero real-endpoint requests — `py_compile` had
   passed because NameError is runtime-only. Failing-before evidence kept;
   fix hashed into `ordering.log` before launch. A runner defect discovered
   mid-run would have voided the preregistration window.
2. **Second-resolution timestamps break "unique first record" checks.** The
   grader draft required ALL records at min `request_ts` to be descriptors;
   at ~5 req/s the first filler/ack share the second. Causality checks over
   append-ordered JSONL must use FILE ORDER (first stamped record), not
   timestamp uniqueness. The draft form failed on real bytes; the fix is
   strictly weaker on the timestamp and strictly stronger on order.
3. **Shrinkage works on paired contrasts, not on levels.** The severity-diff
   prediction shrunk from the n=8 point estimate (+0.50 → +0.35) landed at
   +0.352 (abs err 0.002); pass-LEVEL predictions anchored to r8/r9 small-n
   rates missed by 0.13–0.22 (observed 45%/33% vs pooled prior ~20%). Same
   unchanged serving stack (pid 1299, argv re-pinned) — absolute rates are
   batch-variable while the paired contrast held across batches in this
   stack's history; claim paired contrasts within-stack, not universally.
4. **A null at small n is not equivalence.** r9's pass-rate "tie" (2/8=2/8)
   became an 8/64 gap at power (McNemar p=0.0963, still ns but directional).
   Never report an underpowered null as "no difference"; report the CI.
5. **Probabilistic predictions cost honesty, and that's the point.** Brier
   0.153 was dominated by the 0.50 on significance — the forecast was
   calibrated, not flattering. The rubric cap "point forecasts where
   probabilities are feasible" is now lifted for this lane; every future
   probe files both.
6. **Hashed bundles freeze typos.** The power analysis' d=0.35 row (exact
   n=64.07, power 0.7996) and a Φ(2.191)→2.192 typo cannot be edited in
   place — they live as adjudicated errata in INTEGRATOR-NOTES/LOG. Write
   hashed text as if a critic will read it (one did).
7. **Conditional contingencies need a pre-committed adjudication path.**
   The critic's only MAJOR was conditional (error records → §5's hardcoded
   n/df lines go false with no void-vs-complete rule). It never materialized
   (0 errors), but the next probe plan should carry the contingency rule
   INSIDE the hashed bundle, not in a critic review.
