# Lessons — round 9

Source: LOG.md round-9 entry; `corpus/knowledge/bench-arena-round9-replication.md`,
`corpus/knowledge/bench-arena-round8-horizon.md`,
`corpus/knowledge/eval-prior-art-calibration.md`; evidence
`corpus/evidence/round9-{replication,fleet}/`.

- **A pre-registered decision rule has three outcomes, and "indeterminate" is
  the one that must not be laundered.** The critic fixed the replication
  falsifier before the run: claim (i) *blocks* if a checkpoint cell reaches
  ≥5/8 with MONO ≤2/8, *survives* if CKPT ≤2/8 **and** INC ≥5/8. Observed
  CKPT 2/8, 2/8; MONO 0/8; **INC 4/8** → neither branch fires. The honest
  report is "indeterminate, one problem short of the survival threshold", not
  "replicated". Writing the threshold down in advance is what made that
  verdict cheap instead of arguable.
- **Direction replicating is not magnitude replicating.** INC > CKPT ≈ MONO
  held in both seed batches (7/10 > 1/10 ≈ 0/10; 4/8 > 2/8 = 2/8 > 0/8) and
  MONO failed 0/18 problems across both rounds; but r8's Δ=6-problem gap
  became Δ=2. Report the two claims separately — the lane's r8 headline
  conflated them, which is why it looked stronger than it was.
- **A control arm must be verified to *be* the control.** The checkpoint cells
  are only a latent-maintenance arm if the ack turns actually ack. r8: 0 leaks
  beyond turn 1 (60/60 compliant). r9: 16/48 (`CKPT4710`) and 8/56
  (`CKPT710`) non-turn-1 ack turns emitted a full state, in **all 8 pids** →
  the r9 checkpoint cells carried more self-copy scaffold than r8's. Audit
  compliance per pid before using a cell as a control; the pinned system
  prompt's "unless the user asks you to reply 'ok'" exception is not enough.
- **Point predictions cannot be calibration-scored properly.** Predicting
  "6/8" forces `|pred−obs|/n` and throws away confidence; the lane has
  already digested Tetlock/Brier scoring
  (`corpus/knowledge/eval-design-digest-3.md`) and did not use it. Next probe:
  per-cell probability per problem, scored with Brier + a hit-rate, so the
  calibration axis has a real number instead of a count of misses.
- **Price novelty before claiming it.** One scout L2 with fetched primaries
  (no search-synthesis prose) downgraded 3 of 4 round-8 findings to
  known/incremental and 1 (non-iid draws) to a *direct replication* of a
  two-year-old public repro (llama.cpp #7052). What survives is
  instrument-level: no named suite ablates emission granularity on identical
  seeds, and none uses a vacuous rule with matched binding/no-rule controls.
  Cost: one agent, ~6 minutes. Do it before writing "finding".
- **An integrity claim needs a field-level diff, not a hash comparison.** The
  r8 corpus copy's md5 differed from the run artifact; one L2 read that as "a
  different execution of the same probe" and voided its own provenance
  assumption. The field-level diff (key-set delta exactly `{raw}`, 0 semantic
  differences over 268 records) showed it was the same run with a stripped
  field. Two other agents measured the same thing correctly — when L2s
  contradict, the tie-break is the finer measurement, re-run by the integrator.
- **A missing contract file is a standing calibration defect, not a neutral
  absence.** `SCORECARD.md` is required per-repo by `../AXES.md` and existed
  in three sibling lanes (`../kagi-shokunin/SCORECARD.md`,
  `../kasegi-shokunin/SCORECARD.md`, `../kake-shokunin/SCORECARD.md`) while
  this lane ran 8 rounds of prose self-assessment. Reading the sibling
  convention first costs one `ls` and prevents inventing a fourth format.
- **`SHONEN.md` boxes are byte-diffed against a canonical seed.**
  `../PROTOCOL.md`'s file contract: the seed block must match verbatim modulo
  `<name>`, marks are the box character plus one indented evidence line, and
  "no other prose, added boxes, or removed boxes". This repo had **3** boxes
  (the "instructions executable without oral context" box was dropped) and
  bare `[x]` marks with no named non-author verifier → author attestation,
  which counts as `[~]`. A subagent the lane dispatched is *still the lane*,
  so round 9's ten L2 verifications cannot promote any box to `[x]`.
