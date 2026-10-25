# Round 26 — ExecRevertHarness

Axes: novelty (C1 counter independence) and calibration (C2 counter independence).

## Change
- Added `plans/fixtures/r26/revert_test.sh` in the private clone. It accepts `LANE_TREE [BASE_COMMIT]` (default frozen base `f11bffbf9caa9c9e286fb32c568b81b97719656a`), copies the tree twice to a fresh `/tmp` directory, reverts C1 paths in one copy and C2 paths in the other, runs each original counter and its unaffected counterpart, and compares C1 family/TOTAL lines and C2's summary count line plus exit status.
- All copy edits/removals and command output are confined to `/tmp`; input lane is read-only. C1 README rows are selected by C1 path markers; C1 SOURCES rows by new IDs cited/used by its knowledge entry. C2 removes only added `R26-E<n>` lines and restores `state_check.py` from the frozen base.

## Evidence
- Clone creation `git rev-parse HEAD` → `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d`.
- Assigned dry run: `./plans/fixtures/r26/revert_test.sh /tmp/kengaku-r26-ExecRevertHarness f11bffbf9caa9c9e286fb32c568b81b97719656a` → exit 2 (`INCOMPLETE`, expected at this pre-instrument base):
  ```
  C1 counting command: python3 plans/grader_perturb.py --summary
  C2 counting command: python3 plans/state_check.py --summary
  C1 comparison=UNAVAILABLE baseline=UNAVAILABLE (counting instrument absent) reverted=UNAVAILABLE (counting instrument absent)
  C2 baseline='assertions=235 match=231 mismatch=0 superseded=1 offline_unverifiable=3'; exit=0
  C2 after_C1_revert='assertions=235 match=231 mismatch=0 superseded=1 offline_unverifiable=3'; exit=0
  C2 comparison=UNCHANGED
  RESULT=INCOMPLETE
  ```
- Clone file written: `plans/fixtures/r26/revert_test.sh` — SHA-256 `3e7dd4e903d94741573359080b57a45a9f72053f16f68f197fae29765d7de0ea`.
- No other checks run; no tools installed.

## Risk / blocker
C1 cannot be compared until `plans/grader_perturb.py` and the C1 outputs land; run this harness again against the integrated lane tree. Base dry run does show C2's summary unchanged under the C1-path revert.

VERDICT: Revert harness implemented in the assigned clone; base dry run is clean for C2 and correctly reports C1 unavailable before integration.
