source: S194 — https://philmcminn.com/publications/barr2015.pdf (p.1 Introduction); S195 — https://arxiv.org/html/2609.34262v1 (§1 Introduction); S196 — https://arxiv.org/html/2606.26300v1 (§2.1 Reward Faithfulness); frozen instrument and receipts in .ufo/waves/round-53/claims/
verified-at: 2026-10-30; classifier freeze d40b7055e0128d7998d09548fdeef431093ab321, label commit db90a6b7ecc9501e2e5de239a8794c5aa19cbf8d
recheck: Run python3 plans/round53_c1_triage.py --lane . on a clean clone; inspect the separate PINS, FREEZE, ORACLE, CONFIRM and PRIOR-ART verdicts. Do not infer final admission from this note.

# Presence-only tests are a bounded oracle property

S194 defines an oracle as a procedure distinguishing correct from incorrect behaviour. An existence-only assertion distinguishes missing from present artefacts; it does not establish content correctness. S195 separates observable outcomes from admissible processes. S196 separates passive false-positive verification from active reward hacking. Accordingly, a P1 label here is not a claim that an entire task can be passed without solving it, nor evidence that any model exploited it.

## Instrument and observed evidence

The exact P1 definition is `.ufo/waves/round-53/p1-spec.md`. The frozen classifier is `plans/round53_c1_classify.py`; the counter is `plans/round53_c1_triage.py`. Inputs are pinned by digest and git history; each test received two labels from distinct blind seats.

- The committed oracle receipt `.ufo/waves/round-53/claims/c1-after-oracle.txt` records 305 decided tests, 52 Y and 253 N, zero classifier disagreements, and 23 disagreements for the round-52 control. Counting command: `python3 plans/round53_c1_triage.py --lane .` on the receipt's clean revision.
- Five reader parts were integrated into `corpus/evidence/round53/confirmations.json`: 20 distinct tasks with `confirmed: true`, quotes located in their test spans, and digest-bound reader reports. Re-derive with the counter's CONFIRM leg; the source JSON is the durable population.
- Four additional blind re-labels cover 80 tests and agree with the oracle on 80. Re-derive by joining `w3/C1RelabelRev{1,2,3,4}/labels.json` with the two original label files for each id under `w1/C1Label*/labels.json` (all paths beneath `.ufo/waves/round-53/`).
- The L1's synthetic touch-run receipt `w3/C1TouchExecL1/touch-run-l1.json` records 26 selected tests passing with empty artefacts. Its script is beside it. This used pytest 9.2.0 in a scratch uv venv, bwrap without network, and stubs for unavailable module-level dependencies; it is not a task-image run or a real submission. Do not generalize it to whole-grader vacuity.

## Limits and contrary evidence

`w3/C1CritOracle2.md` found content agreement but an integrity-guarantee weakness. `w3/C1MutClassifier.md` reports 20 of 42 mutants killed and 22 survivors, including 20 with witnesses; the fixed corpus is not a completeness proof. The never-read definition excludes only the frozen text blocklist and earlier confirmations: it does not mean never mechanically examined. Prior-art pricing must distinguish the task's own source (the object under study) from independent public documentation of its weakness. Final admission is the unchanged predicate in `plans/round-53-claims.md`, not these corroborating observations.

## Tip-state calibration

`plans/round53-tipstate.json` is a self-assessment, including truthful red rows. `plans/round53_c2_tipstate.py` re-executes its declarations in isolated worker clones. A matching declaration measures calibration, not instrument quality: even an always-green gate can be described truthfully. Independent runs at b1f79a54 recorded one mismatch, the prematurely green `round53-c1` declaration (`w3/C2MeasureExecA.md`, `w3/C2MeasureExecB.md`). The final scored receipt must name its own revision.
