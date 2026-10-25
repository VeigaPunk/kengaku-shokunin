# State-check P2 exclusion reconstruction

Axes: **calibration** (primary); **scope integrity** (supporting). No novelty claim is assessed here.

## Finding

The exclusions were **by design under frozen P2**, not an accidental omission from the P2 implementation. They nevertheless exposed a deliberate coverage boundary: rows added after the P2 freeze were reported as out-of-population, not revalidated. The round-25 capability-row defects were therefore a real blind spot for that round's new text, subsequently assigned to P3.

## Evidence chain

- `plans/round-25-claims.md:75-86` freezes P2 from base `6180e4f` and explicitly says “any later row is out of population.” P2a names three capability rows; P2e tests frozen `knowledge/`, `lessons/`, and `evidence/` index rows in both directions.
- `plans/state_check.py:4-10,34-38` repeats the `6180e4f` freeze and fixes `CAPABILITY_IDS` to `offline-replay-gate`, `frozen-table-pin-check`, and `sources-registry`.
- `plans/state_check.py:452-475` emits `OUT_OF_POPULATION` for every other capability key, then checks only those three frozen IDs. Thus `interval-reverdict` and `state-assertion-check` were intentionally not graded as P2 capability assertions.
- `SCORECARD.md:558-559` places those two rows in the round-25 additions. The landed `corpus/evidence/round25-calibration/state-check-after-v2.txt:2-3` records both as `OUT_OF_POPULATION`; it separately reports `mismatch=0` for comparable P2 assertions. The round-25 verifier spot-check, `corpus/lessons/round-25-verifier-spotcheck.md:96-102`, explicitly identifies both rows as out-of-population and finds their stale values (`14` vs receipt `18`; `mismatch=11` vs corrected `10`).
- `plans/state_check.py:60-62` says the README path set was frozen from the fixed tables at `6180e4f`; new table entries and immediate children are OOP, not admitted to P2e. Lines `1040-1079` implement both directions: frozen rows/files are checked, later rows and on-disk paths are emitted OOP.
- `plans/state_check.py:164-168` makes an important distinction: the base file manifest includes `lessons/round-24-verifier-spotcheck.md` although it was unindexed at freeze. Its file→row defect was checkable in P2; a later README row for that path remains an OOP row. The round-25 v2 receipt lists that row plus `knowledge/attribution-interval-calibration.md`, `lessons/round-25.md`, and the round-25 evidence directories as OOP (`state-check-after-v2.txt:5-13`).
- `plans/round-25-claims.md:145-151` confirms P2e's file→row scope is the base file manifest and that files added that round are “new,” not counted. Round-26 preregistration names the escaped capability values in R26-E1/E2 (`plans/round-26-claims.md:15-16`), then freezes distinct P3a/P3e populations at `f11bffbf` (`:126-138`) and requires P2 v2 results to remain identical (`:143-147`).

## Recommendation

Keep P2's `CAPABILITY_IDS`, README row/file manifests, and verdict semantics frozen; do not append round-25 additions to those sets. Implement them as separate P3 assertions: P3a pins the two specified capability cells and re-derives every numeric token against the named committed receipts; P3e freezes the exact base-run OOP README rows and paths and checks the stated directions. Give each P3 class stable IDs and mutation coverage, while regression-checking that P2 results on its frozen base remain byte/count-identical to v2. This extends coverage without retroactively changing P2's population.

LSP was unavailable (`read xd://lsp` returned “No such tool”); evidence was read from source, preregistration, and committed receipts. Confidence: **high** (the freeze rule, explicit code branches, and recorded OOP results agree). No checks run; no tools installed.

VERDICT: P2 exclusions were intentional freeze behavior; round 25's new rows were under-covered, and separately frozen P3a/P3e is the correct repair without re-scoping P2.