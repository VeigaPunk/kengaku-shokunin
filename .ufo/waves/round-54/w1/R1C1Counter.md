# R1C1Counter report

Axes: novelty, calibration, correctness. Recommendation only: C1 counter cannot support admission as written.

Detailed leg→function→line table, all eight selftest case assessments, controls analysis, classified findings and residual gaps: `.ufo/waves/round-54/w1/R1C1Counter/review.md`. Reproducer: `.ufo/waves/round-54/w1/R1C1Counter/probe.py`.

## BLOCKERS (pasted)

1. **B1: valid OTS proofs cannot parse.** `plans/round54_c1_anchor.py:198,256,285,356,527` passes raw streams to `DetachedTimestampFile.deserialize`, which requires `StreamDeserializationContext`. Actual probe: raw-reader `AttributeError: '_io.BytesIO' object has no attribute 'assert_magic'`; correct-context reader on identical bytes: `OK`. Canonical verify rejects honest proofs at 358.
2. **B2: independent walk cannot execute or supply caller-compatible nodes.** At 152, actual runtime raises missing `OpRipemd160`; diagnostic isolation then raises missing `OpAppend.arg` at 161. At 158 it returns integer object IDs, while consumers 200,263,293,365 require timestamp objects with `.attestations`. Isolated root walk produced `['int']`. No child.msg consistency comparison exists; adversarial unreachable-child probe crashes rather than demonstrating semantic rejection.
3. **B3: identity replaces reachability.** At 371–374 canonical verify requires derived attested digest equal original file digest, contrary to frozen op-path requirement. Normal append/hash OTS Merkle aggregation changes the digest; fixing reader/walker alone still cannot admit normal calendar proofs. Static code-path finding, not a live upgraded-proof execution.

## Other findings

MAJOR: forged control calls five-required-argument function with four arguments and swallows TypeError as required failure (216–218,272); flip at byte5 changes magic, not op path; control failure count reversed in printed receipt (188–190,435). Actual control harness prints all four failed-as-required while returning count0. External-pin block validates neither receipt freshness nor independent/public provenance (422–429); time-order check uses verification time instead of landing after-run receipt (404–409). Source is not compared to landing lane tip and anchor bytes are not checked committed in SOURCE. Failure helpers return tuples from an integer-exit API, lose expected diagnostics/setup status. MINOR: exact-byte binding uses text-mode git output; --selftest spelling unsupported; --calendar not forwarded.

## Exercised verification

Using supplied otsenv python with seat TMPDIR and bytecode disabled:
- Literal `COUNTER --selftest`: exit2, required cmd missing.
- Supported `COUNTER selftest`: exit0, `[selftest] 8/8 PASS`.
- Preserved probe: final exit0; confirms reader/walk/control defects above. Pending and forged selftests are vacuous integrity evidence: both reject for bad reader; forged starts already-invalid pending proof.

LSP device unavailable (`No such tool`); literal caller search only, not semantic proof. Full frozen claims read first; actual added-file base→freeze diff reviewed. No production edits, git mutations, installs, network, score judgment or full forged-PASS claim. No live confirmed anchor verified; latent receipt bypass is not an end-to-end success. Scratch cleaned before yield. L1 should apply frozen amendment policy rather than silently edit instrument, then exercise corrected canonical positive path and causal negative controls.

Report: .ufo/waves/round-54/w1/R1C1Counter.md
