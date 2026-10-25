# Lessons — round 12 (powered four-point ladder, batching dissociation, transport)

Source: LOG.md round-12 entry (once landed); `corpus/evidence/round12-ladder/`
(bundle `prereg-bundle.sha256`, `analysis_r12.md`, `power_analysis_r12.md`,
`recompute_r12.py`, `predictor`/`predict_r12.py`) + `corpus/evidence/round12-fleet/`
(`r12-critic-design.md`, `r12-prior-art-{ladder,transport}.md`, `r12-mutation.md`,
`r12-report-final.md`, `INTEGRATOR-NOTES.md`). Numbers quoted from
`analysis_r12.md` / `power_analysis_r12.md`; the round-14 re-derivation is in
`corpus/knowledge/bench-arena-round12-ladder.md` §Independent verification.

The round narrative: r11 had *one* powered pairwise contrast. r12 turned it into
an **ordered four-point ladder** (E1 Page `z=+9.452`, `LADDER ESTABLISHED`),
**dissociated** the eight-round-old `A-MONO` collapse (E4 `+0.656`,
`DISSOCIATION ESTABLISHED`), repeated the r11 dose on identical problems
(E2 `+0.297` vs r11's `+0.352`, `REPEATS-r11; POINT-MATCHES-r11`), carried the
dose to a second task family (E5 `+0.177`, `TRANSPORT DIRECTIONAL`), and filed
416 per-problem forecasts (Brier `0.1288`, BSS `+0.0447`, slope `+0.8427`).
Four things it taught that are now `SKILL.md` anti-patterns 16–19 / measurement
rules 11–12:

1. **An ordered alternative gets an ordered test.** One Page's trend test over
   within-pid midranks replaced what would otherwise have been three paired
   t-tests (multiplicity) or Friedman + post-hoc (discards the ordering). The
   critic's D2/D9 forced the storage to be *representable*: a tied block
   `(1,2.5,2.5,4)` contributes `29.5` to `L`, so `L` had to be a fixed decimal,
   and the all-tied block had to have a pinned `z=0,p=1` convention. Seeded MC:
   power 1.000 at n=44–64, 0.989 at n=48 with the alternative halved, minimum
   n for 80% power = 12 — so the binding risk is **anchor validity, not power**
   (the anchor's densest leg is r8's n=10 gap). Measurement rule 11.
2. **An asserted power floor is a measurement.** The draft filed "family 1
   n ≥ 56, family 2 n ≥ 42" with no derivation; the critic recomputed and
   falsified it (42 pairs → 0.791, below the 0.80 target), and the floor became
   **44/44** from a committed, seeded Monte-Carlo script (`power_r12.py` →
   `power_analysis_r12.md` §2), re-measured at 20 000 sims. The search-then-
   remeasure convention also showed its own noise: the first n clearing 0.80 at
   4 000 sims re-measures just under it. Anti-pattern 17.
3. **Heterogeneous forecast events must not be pooled into one skill score.**
   Three event classes with different reference classes were scored separately —
   416 per-problem pass events (fitted predictor), 304 per-problem sign events
   (mostly an uninformative 0.50, Brier `0.2469` ≈ the 0.25 of a coin), 7
   run-level judgement events — and the pooled `+0.0049`/`0.1796` figures are
   labelled for what they measure (`persistence + arm-rate transport`), with
   subgroups reported (family1-replicate `+0.4751`, family1-novel `+0.0173`,
   family2 `-3.1474`). Anti-pattern 18.
4. **A per-item probability tilt must be renormalized to its own marginals.**
   The fitted difficulty slope `c = −5.03` saturated the sigmoid, so `A-MONO`'s
   mean predicted probability drifted to 0.372 against a 0.143 base rate
   (23.8 predicted passes instead of 9.1). The fix — a per-arm mean-preserving
   logit offset solved by bisection with the clip inside the target — is now
   required for any per-item tilt, or the point predictions and the filed
   probabilities contradict each other. Anti-pattern 19; `INTEGRATOR-NOTES.md`
   §2 L1-tilt.
5. **Repeatability is not replication on a non-deterministic server.** Same
   unit, same problems, same seeds ⇒ *within-run repeatability*, and R2's
   branches are named `REPEATS-*` accordingly (the C2 wording was rewritten
   pre-hash, §9 rows L1-C2/D4). llama.cpp #7052 documents multi-slot draws as
   not bit-reproducible; vLLM's docs agree. Never write "replicated".
   Measurement rule 12.
6. **A floor is a result, and an honest negative is load-bearing.** Family 2
   landed `2/48` in *both* arms, so E5 is a floor-level contrast, not positive
   transport — reported as such. The same floor falsified the transported-base-
   rate null the predictor used for family 2 (predicted ≈21.8/15.8 passes vs
   observed 2/48), and that falsification is exactly why `family2` BSS is
   `-3.1474`; hiding the floor would have hidden the predictor's defect.
7. **Absorb critic defects pre-hash and log them inside the hashed document.**
   The design critic returned DO-NOT-RUN with 1 FATAL (D1: the landed runner was
   still the r11 runner) + 5 MAJOR + 4 MINOR; all of it was fixed before
   `prereg-bundle.sha256` v1 was written, with a numbered amendment log (§9) in
   the hashed plan, so there is no v2 chain for a later round to reconstruct.
   The FATAL was found by reading `run_r12.py` against the plan — a pre-run
   critic is worth more than a post-run audit. Measurement rule 13.
8. **A pinned hash goes stale the moment an artifact is regenerated.**
   `analysis_r12.md` was regenerated after the fleet drafts were written: the
   drafts pin md5 `ddfe60d2…`/sha256 `ef1e69db…`, the tree satisfies md5
   `029c3bcd…`/sha256 `1ceebd75…` (F-R12-2 in the r12 knowledge entry). The same
   file is also not byte-reproducible on this host — line 66 carries
   `/home/vgpnk/projects/…`, a path that does not exist (F-R12-1), while every
   statistic reproduces. Pin hashes at landing time from the bytes that are
   being landed, and make generated files path-insensitive; a draft's hash is
   evidence of what the drafter saw, not of what will be committed.
9. **A round can be complete and still invisible.** Rounds 12 and 13 sat
   uncommitted and unindexed for a full round: no LOG entry, no SCORECARD move,
   no README index row, no knowledge/lessons entries. See
   `lessons-round-14.md` — the r12 numbers above were only durable because the
   round-14 landing made them so.