# FSHONEN — bounded falsification

Identity: KengakuR27.FSHONEN, **not** candidate writer KengakuR27. Axes: novelty (legacy 7 → canonical coverage/constructs, held) and calibration (8, frozen P4). Private clone observed at `b5f62e5e637b34a1549e3475fc58b4227ed87e5a` (`git clone --no-hardlinks ... && git switch -c r27-FSHONEN b5f62e5e637b34a1549e3475fc58b4227ed87e5a`; exit 0).

Entry reread: read all 110 lines of `.ufo/waves/round-27/drafts/extraction-policy-comparison.md`, including the complete source header. Proposed canonical `corpus/knowledge/extraction-policy-comparison.md` is absent in the clone (`test -e ...` exit 1); candidate exists (exit 0). It names `writer: KengakuR27` at candidate:4 and does not name a dispatched seat as verifier. This report is advisory, not an outside closure or an admission review.

## Findings by severity

No actionable defect found in the assigned fixed-response parser, frozen P4, or Q15 checks. No promotion, checkbox upgrade, or score increase is supported or claimed.

## Evidence

- **C1 parser replay:** In the frozen clone, `env PYTHONDONTWRITEBYTECODE=1 python3 plans/parser_policy_compare.py --root /tmp/kengaku-r27-FSHONEN --summary` → exit 0; `TOTAL population=1964 policies=8 compared_verdicts=15712 disagreements=1089 policies_with_flips=5`. Counts (agree/flip_pf/flip_fp/none) were E0 1964/0/0/0, E1 1947/17/0/0, E2 1964/0/0/0, E3 1947/17/0/0, E4 952/1012/0/1876, E5 1938/26/0/145, E6 1964/0/0/0, E7 1947/17/0/0, E8 1964/0/0/0. `policy_oracle.py --root /tmp/kengaku-r27-FSHONEN` independently returned the same per-policy counts, exit 0. These match candidate:58-78 and the pre-registration’s frozen semantics and totals (claims:35-71; Amendment 1:155-190).
- `parser_policy_compare.py --root /tmp/kengaku-r27-FSHONEN --selftest` → exit 0: 9 policy mutants killed, 58 hand cases passed, and pin-rejection-before-policy-call control passed (`policy_calls=0`). No claim beyond the pinned finite population; Amendment 1 explicitly rejects arbitrary-input safety and source-exact vendor-harness claims (claims:164-190). C1 remains “published in kind,” novelty 7; no +1 (claims:73-78; lesson:31).
- **P4:** `state_check.py --root /tmp/kengaku-r27-FSHONEN --summary` and `--selftest` → exit 0; summary `assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3`. P4 selftest red controls passed for P4a–P4e. Re-ran v4 against an archive of base `b5719440e5eee46c1886fddbdf7bdc1624829454`: summary also had `mismatch=0`, exit 0; P4b’s frozen S043–S048 erratum is superseded, not a new defect. Thus the pre-registered base `mismatch >= 1` prediction is false, as disclosed (claims:126-130; lesson:121-127).
- `p23_preservation.py --old /tmp/kengaku-r27-FSHONEN-base/plans/state_check.py --new /tmp/kengaku-r27-FSHONEN/plans/state_check.py --root /tmp/kengaku-r27-FSHONEN-base` → 298 P2/P3 record pairs, zero field/order differences, exit 0. `p4_mutate.py --checker /tmp/kengaku-r27-FSHONEN/plans/state_check.py --repo /tmp/kengaku-r27-FSHONEN` → all five P4-class mutants red for their own class, exit 0. P4 is limited to frozen P4a–P4e, not a claim to check every current assertion (claims:102-124,184-186; lesson:129-139).
- **Q15:** `python3 plans/gate_timing_check.py --selftest` → exit 0. It produced the identical-lesson early-commit report-tree control at exit 1/inventory 0 and later committed-report control at exit 0/inventory 1; the worktree-inventory mutant is rejected. This verifies structural commit-tree timing only, not source truth or an actual R27 admission (QUALITY:123-130).

## SHONEN boxes and pointers — retain [~] for all four

All four current `SHONEN.md` rows are `[~]` (`SHONEN.md:5-12`); each pointer resolves, but none is upgraded here:

1. **[~] Box 1**, `SHONEN.md:5-6` → current `SKILL.md`. Decision tables and anti-patterns are present (`SKILL.md:23-46,60-86`); the file itself says its former wiki source is absent and only retained digests/rules remain (`SKILL.md:12-18`). This is current content, not a fresh external-source or full execution review.
2. **[~] Box 2**, `SHONEN.md:7-8` → `LOG.md:7`, a dated 2026-09-28 record of a four-task executed evaluation. It is historical evidence; no live endpoint/model request was made or needed for this review.
3. **[~] Box 3**, `SHONEN.md:9-10` → `corpus/lessons/round-8-aggregator-box3-coldrun.md:48`, which resolves to the historical verdict heading; the old `[x]` is at :49. That run tested an older SKILL snapshot, not present-day executability. Current README explicitly says it is not a fresh live-source pass and box 3 is not freshly externally verified (`corpus/README.md:245`); retain `[~]`.
4. **[~] Box 4**, `SHONEN.md:11-12` → current `PROVINCE.md:129` (`### Adjacent`, with routing rows at :131-143). The pointer resolves, but the routing section alone is not proof of no cross-domain bleed; retain the author-asserted `[~]`.

No author-lane seat is presented as the outside verifier: the round-27 lesson says outside verification is the orchestrator’s roster-external closure, not a dispatched seat, and keeps all four boxes `[~]` with no promotion (`corpus/lessons/round-27.md:109-110`). The named `CloseKengaku26` verifier belongs only to the prior round-26 closure (`.ufo/reports/round-26/kengaku-closure-evidence.json:4-8`), not this candidate. Admission remains deferred and novelty +1 rejected (`corpus/lessons/round-27.md:24-35`).

## Residual risk and verification gaps

The cold-run and LOG pointer are historical; present-day end-to-end instruction executability and cross-domain absence were not established. P4 retains three offline-unverifiable assertions and its frozen scope; Q15 was exercised on its synthetic timing control, not an actual admission commit. Candidate remains a draft; no Q10/Q13/Q14 admission or outside closure is asserted. No live models/endpoints were contacted. No tools installed or updated.

VERDICT: [~] — scoped parser, P4, Q15, and pointer checks found no actionable defect; retain the four SHONEN boxes as `[~]`. No admission, promotion, or score change claimed.