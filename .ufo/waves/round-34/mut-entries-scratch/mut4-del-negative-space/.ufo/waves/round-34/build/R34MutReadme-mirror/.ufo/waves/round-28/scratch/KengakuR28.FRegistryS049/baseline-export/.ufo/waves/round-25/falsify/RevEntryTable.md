ATTACKS: Attribution interval-calibration Claim and table — summary totals and cited receipt-line anchors.

## Result
- Ran `python3 plans/attrib_calibration.py --summary` in the lane; exit 0. Its complete persisted output is `corpus/evidence/round25-calibration/attrib-calibration-summary.txt:3-50`.
- No numeric or receipt-line mismatch found in the Claim/table.

## Table cross-checks
- Knowledge doc:20 ↔ `attrib-r21-impl-ds-trials.log:297` ACCURACY 20/20 PASS; summary:3 gives CP95 [0.831567,1], PASS.
- Doc:21 ↔ `attrib-r21-impl-glm-trials.log:173` ACCURACY 22/22 PASS; summary:13 gives [0.845627,1], PASS.
- Doc:22 ↔ `attrib-r22-opencode-trials.log:234` ACCURACY 20/20 PASS; summary:25 gives [0.831567,1], PASS.
- Doc:23 ↔ same receipt:236 TARGET hyper 10/10 PASS; summary:32 gives [0.691503,1], INDETERMINATE, need_n=17.
- Doc:24 ↔ same receipt:237 TARGET opencode-go 0/0 FAIL; summary:33 gives UNTESTED.
- Doc:25 ↔ `attrib-r23-stream.log:298` ACCURACY 30/30 PASS; summary:38 gives [0.884297,1], PASS.
- Doc:26 ↔ same receipt:303 STREAM TARGET opencode-go 0/0 FAIL; summary:45 gives UNTESTED. The additional cited line 239 also contains the stated 0/0 FAIL.

## Remaining Claim numbers
- Doc:14-16's four unique samples, 92 trials/92 correct, one PASS→INDETERMINATE, and two FAIL→UNTESTED match summary:49 (`unique_samples=4`, `scored_trials=92`, `correct=92`, transition counts); the four accuracy PASS rows plus one target PASS row are also represented there.
- Doc:28-36's duplicate and per-leg figures match summary:24, :37-48: r22 is deduplicated once; pooled-if-distinct is 40/40, CP95 [0.911903,1]; recall totals are 12 = 2 PASS + 5 INDETERMINATE + 5 UNTESTED; opencode-go shares are 0/20 (r21), 0/20 (r22), 0/30 (r23), each RG bound [0,1]. The distinct request windows and frozen-table hashes are recorded at r22-legs:313-316 and r22-opencode:205-208.
- Doc:39-44's totals match summary:49 exactly: estimates=35, PASS=12, FAIL=0, INDETERMINATE=11, UNTESTED=12, stored_verdicts=7, transitions `FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4`, stored_checks=119, mismatches=0.

Residual risk / verification gap: this attack checks the requested Claim/table arithmetic and receipt anchors, not the external statistical source claims or journal-to-GT provenance. No tools installed.
VERDICT: SURVIVES — no requested numeric or receipt-line mismatch found; installs: none.