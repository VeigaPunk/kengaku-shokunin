# R46RevClaimsFile — claims-file review

## Review

**Axes:** calibration (C1), depth (C2), coverage (C3). The claims name three distinct surfaces and specify individually falsifiable pass predicates, aligning with the round contract’s requirement for one axis-move per distinct axis (§2, lines 14–19). C1’s frozen predicate at claims lines 46–50, C2’s at 74–77, and C3’s at 112–113 each express a single pass condition; the C2 counter docstring lines 30–35 repeats its predicate, and the C2 control receipts share the `PREDICATE C2 fail` label. No universal guarantee appears in the three predicate sentences; C1 explicitly calls io_uring a limit (line 44), C2 scopes leg A to line-cited quotes (89–90), and C3 names host/image and pytest limits (118–119).

C2 controls: I made a fresh `git clone --shared` at `/fast/scratch/hyaku/kengaku-r46/R46RevClaimsFile/lane`, verified its root, detached at base `64ba8385ea10af1b78d367dcb242b92d97062af7`, and copied in the frozen C2 counter and anchor-line gate. **I did not reproduce any of the five control transformations**: the committed receipts report expected fail lines, but they do not contain the transformation scripts, and this review did not locate usable transforms in the claims directory or reviewer artifact. Consequently the acceptance criterion requiring byte-equal verdict-line checks is not met; the five historic receipt verdicts are not treated as fresh replays.

## Findings

1. **Actionable gap — five C2 control replays unavailable.** Claims lines 78–84 describe five distinct transform controls and expected outcomes, but the available `control-c2-*.txt` files are output-only receipts. Fresh base clone setup succeeded; without exact transformations, re-running those variants would require guessing, not faithful reproduction. No verdict line was compared byte-for-byte. Repro count: 0/5.
2. **No predicate-level defect observed in reviewed frozen claims.** Claims C1/C2/C3 predicates are concise, surface-specific and not universal; controls are specified with fail labels, including C2 do-nothing. This is a textual review only, not proof that the stated controls run or that C1/C3 controls all reach their intended fail states.

## Verification record

- Read the complete frozen claims and the round prompt §2 / §6.9-related campaign material; consulted QUALITY Q37–Q39 (Q30/Q31 are referenced but their exact text was not recovered in this review). Thus compliance with those exact clauses remains a verification gap, not an asserted pass.
- Read the five frozen C2 receipt files; all show `PREDICATE C2 fail`, exit 1, with the specific expected defect counts. No fresh counter runs were performed because control transforms were unavailable.
- Clone root verified; no lane or frozen file modified. No tool installed.

VERDICT: claims-file-defects-1-c2-controls-reproduced-0/5
