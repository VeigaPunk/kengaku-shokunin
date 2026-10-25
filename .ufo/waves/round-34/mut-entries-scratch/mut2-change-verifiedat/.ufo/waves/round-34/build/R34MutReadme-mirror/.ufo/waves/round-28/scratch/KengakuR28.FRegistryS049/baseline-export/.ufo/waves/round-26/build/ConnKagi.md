# ConnKagi — sibling-overlap scan: kagi lessons → kengaku Q13 + P3c/P3d

Scope: read-only kagi `corpus/QUALITY.md` + lessons r17–r24; live kengaku glob shows `gate_timing_check.py` and `grader_perturb.py` absent and `state_check.py` present (tools in flight). No installs.

## Evidence and alignment

- kagi `corpus/QUALITY.md:14-16` (r21 bar): “An entry is admitted only when every row below holds”; a failing candidate is rejected “with that row's id as the reason, in the round lesson's `## Gate`.” Closure is per-candidate, reasoned, and checkable.
- kagi `QUALITY.md:43` (QM5): artifact and claim row update “in the same commit”; “a pin that lags the artifact's bytes is a defect.” This is the same-commit family Q13 extends to admit↔cited re-read report (`kengaku/corpus/QUALITY.md:97-101`).
- kagi `QUALITY.md:48` (QM10): re-run an absence claim “on the tree that contains the claiming sentence, with a needle that excludes it.” This supports Q13's lesson-as-of-landing-commit check; generic-reference patterns must not self-match or count as report evidence.
- kagi `QUALITY.md:72` (QM13): calibration “must fail a known bad admit while retaining a bounded valid control.” Claims red-before `8ea41f9` is the known-bad case (`kengaku/plans/round-26-claims.md:23-24`), but its Q13 spec does not name a green control.
- kagi `QUALITY.md:41,99` (QM3/QM17): count skips, unverified branches and failures; a Gate records each admitted/rejected/superseded/withdrawn candidate and its basis, not only an aggregate. kagi `round-21.md:118-121` adds that should-fail mutants must be exercised; proving only that findings fire does not show unseen cases cannot pass.
- kagi `round-17.md:83-85`: a same-cardinality delete/add swap remained invisible under a “breadth, not identity” claim. `round-17.md:100-103` also removes a false citation because D-96 concerned other files, not the attributed ownership surface.
- kagi `round-19-recensus.md:30-41`: superseded counts, absent-file hash prefixes and an unfilled `<FILL ON STAMP>` survived as current-looking assertions; `:49` reports self-matching needles that made empty-grep claims false.
- kagi `QUALITY.md:98` (QM16): distinguish current captures from historical pins and use one committed, selftested normalizer with explicit rules. `QUALITY.md:100` (QM18) says membership pins identity, not cardinality; kagi `round-24.md:149` reports 15/15 count-preserving swaps survived at BASE.
- kagi `round-24.md:130-137` C3 binds `count=N sha256=…` to the actual membership and pairs fifteen swap mutants with fifteen pristine controls; `round-24.md:152` says a failing control invalidates the run. This is the mature endpoint of the r17→r19 pin failure.
- Kengaku P3c/P3d (`plans/round-26-claims.md:134-136`) replace line/range-only assertions with frozen content tokens. Identity-sensitive tokens plus a count-preserving swap mutant are the relevant QM18 check shape; QM16 cautions against unspecified normalization.

## One bounded proposal

Pair the Q13 red-before fixture with one known-good lesson/landing-commit control, and require the existing P3 selftest to pair each content-pin mutation with a pristine control; use one explicit, byte-exact token comparison rule. This carries kagi's fail-known-bad + valid-control pattern into Q13/P3 without changing populations or claims.

Affected axis: calibration (P3 / check validity); novelty unaffected. Risks: kagi r17:83-85 declined name-pinning for privacy, whereas kengaku pins content; this is not directly transferable across domains, so record why corpus prose has no equivalent privacy boundary. P3c checks that a current tree still carries a base token, not that the underlying source remains current; a PASS must not imply source freshness.

Verification: gate-timing selftest returns failure on `8ea41f9`'s Q10 cell and success on a bounded valid control; state-check selftest kills a same-line content swap and passes its pristine control; each reports failures/skips explicitly. These are proposed checks, not run here.

VERDICT: align Q13 with kagi QM5/QM10/QM13 and P3c/P3d with QM16/QM18; the concrete gap is Q13's unspecified green control. No installs.