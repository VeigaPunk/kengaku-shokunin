# Lessons — round 8 (retrospective, written round 9)

Source: LOG.md round-8 entry; artifacts `corpus/evidence/round8-horizon/`;
analysis `corpus/knowledge/bench-arena-round8-horizon.md` and the five L2
reports in `corpus/evidence/round9-fleet/`. Round 8 was retired mid-round
after the probe ran (78/78 jobs) but before it was analyzed, logged, or
committed — so these lessons are paid for twice: once in round 8's wasted
run, once in round 9's debt closure.

- **An unanalyzed run is not a result.** 268 records sat in `corpus/evidence/`
  untracked with no LOG entry and no corpus note for a full round; the fleet
  marker (`.ufo/reports/round-8/kengaku.md`) said only "retired mid-round".
  The knowledge existed only as a SUMMARY block in a `/tmp` run log — which
  `../PROTOCOL.md`'s evidence standard explicitly rejects (`/tmp` pointers are
  not evidence at closure). Rule: if a round ends mid-probe, land the raw
  artifacts **and** a one-line LOG entry with the summary numbers in the same
  commit; analysis can wait, existence cannot.
- **The lane's own written rule was violated and nothing caught it.**
  `SKILL.md` checklist item 1 and anti-pattern 4 require ex-ante predictions;
  rounds 5 and 6 filed them (`/tmp/bench-r5/predictions.md` 25 lines,
  `/tmp/bench-r6/predictions.md` 17 lines); round 8 filed none
  (`grep -ril predict` over both r8 dirs → 0 hits). A prose rule with no
  artifact gate decays silently. Round 9's fix is mechanical: hash the
  predictions file and log the timestamp before the first request
  (`corpus/evidence/round9-replication/ordering.log`).
- **"Critic accepted" ≠ "critic implemented".** 16 defects were filed against
  the design and the v2 docstring advertised 12 fixes; the line-cited audit
  found **9 landed, 5 partial, 2 not landed** — including the two that
  invalidate whole cells (#6 corrupted key must be exercised by the tail;
  #15 fixed op histogram). Audit fix-landing *in code, by line* before
  spending calls; a docstring is not evidence of a fix.
- **Verify the manipulation binds before interpreting it.** Probe B's
  corrupt arm was byte-identical to its clean arm in 3/8 pids, 4/8 corruptions
  were erased by the tail ops, and 2/8 were fabricated `true+5` rather than
  historical drift → well-formed in **2/8** pids. The "propagation" headline
  (3/8 vs 6/8) reduces to one frozen-key carry plus seed difficulty. Cheap
  pre-flight: simulate the treatment through the remaining ops and assert the
  final state differs from truth.
- **A grader's `ok` flag must be the conjunction the claim needs.**
  `grade_c` computed `over_repair` and then left it out of `ok`
  (`horizon.py:288`), and derived `preserved` from the model's *self-declared*
  violations (`:277-279`). One record rode through as a pass: C-benign 1/4 is
  0/4 under the intended rule. Mutation-test the grader against synthetic
  adversarial inputs before trusting a SUMMARY (round 9: 50 cases, 12 defect
  candidates, 1 live).
- **Never strip fields from a landed artifact.** The round-8 corpus copy of
  `results.jsonl` had `raw` removed from all 258 non-meta records
  (md5 `01547cfa…` vs run `df154cb5…`). The ack-compliance audit, the B-arm
  byte-identity check and the C benign failure-mode reading all need `raw` —
  i.e. exactly the failure-class evidence was destroyed while the graded
  fields looked intact. Land the run bytes or nothing; if size forces a
  split, keep the full artifact and index it.
- **Burst adjacency was maximal by construction.** The scheduler ran each
  problem's INC→MONO→CKPT back-to-back and each problem's four B cells and
  four C cells as adjacent blocks (`horizon.py:313-321`) on a server this lane
  had *already* measured as burst-coupled (lag-1 +0.26/+0.32). Zero fillers
  were run despite the critic asking for them. Cross-cell contrasts from that
  schedule are correlated draws; interleave **and** insert fillers.
