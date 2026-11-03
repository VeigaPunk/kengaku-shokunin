
## Erratum (round 68)

*Dated 2026-11-03; corrections to the round-67 record, appended — never an edit of the sections above.*

1. **Probe sha miscited.** The round-67 report cited `PROBE sha 32bacf1d629e7d5809788ef7ea2183fd7b08a11b10c383cc9942e2f58842b836` for `plans/round67_c1_pipeline_probe.py`; the committed file re-hashes `PROBE sha256=03793f4f9e184e8f829916ef848e0f0d41d94b1bef8ed17eda0fe3c28b0a9f1e` (sha256 re-derived this round). `32bacf1d…` was the pre-amendment file's sha recorded in `corpus/evidence/round67/pipe/a1-mutants.txt`; the citation copied it instead of re-hashing. Class: wrong-sha citation; captured-by: none until the round-67 non-author spot-check.
2. **Mutant tally miscounted.** The round-67 report and LOG.md verification line say "8 killed, 1 accepted by design"; `corpus/evidence/round67/pipe/a1-mutants.txt` records nine rows: 7 refused (m02, m11, m12, v3, v4, v6, x_drop_junit) and 1 accepted by design (v1 line-order), plus the unmutated base line. Correction: the record is 7 refused and 1 accepted by design; the "8" counted the base line. Class: count drift; captured-by: none until the round-67 non-author spot-check.
3. **Class-row before/after.** The process-environment row's executed column: before R67-C1's predicate the member stayed `recipe-unexecuted`; after the predicate passed the row reads `executed 2 of 3` (`install-windows-3.11` remains the unexecuted member). Stated for the record — the claims doc's "stays `recipe-unexecuted` until this predicate passes" names the before-value; the round-67 closure record keeps both values straight.
