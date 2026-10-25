# FxGateLate — Q13 commit-tree timing

## Scope and evidence
- Reviewed integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` against base `f11bffbf9caa9c9e286fb32c568b81b97719656a`; the diff adds `plans/gate_timing_check.py` and registers Q13 in `plans/round-26-claims.md:20-26`.
- LSP was unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; no references/definition/diagnostics request could be made. No grep was used as semantic proof.

## Same-lesson missing → present commit attack
Scratch Git repo: `/tmp/fxgate-late-sff730n5`. Commit A `98666ea873d634c13631ab319fd5f286305ae6f3` contains an admit for `corpus/knowledge/grader-perturbation-audit.md`, a writer field, and a registered reviewer, but not the cited `.ufo/waves/round-26/falsify/FxLate.md`. Child B `6218affdaf70f87de1d1a072551dbe44ae1c259b` adds only that report. At B the working tree contains the report while A's tree does not. Lesson blob IDs are identical at A and B: `23815f3dc075cf8677a645433e260968f04cb647`.

Exact checks (checker `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py`):
```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --lesson corpus/lessons/round-26.md --commit 98666ea873d634c13631ab319fd5f286305ae6f3 --repo /tmp/fxgate-late-sff730n5
# exit 1; invalid cited report: absent from commit tree; missing report; admissions=1 passed=0 failed=1 second-seat-reports=0
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --lesson corpus/lessons/round-26.md --commit 6218affdaf70f87de1d1a072551dbe44ae1c259b --repo /tmp/fxgate-late-sff730n5
# exit 0; existing returned report FxLate.md; admissions=1 passed=1 failed=0 second-seat-reports=1
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --selftest
# exit 0; [selftest] ALL PASS (arbitrary lesson basename, generic-only/variant red, explicit/bare citation, missing/unresolved citation, registry/mode/return/self-review/unknown-writer checks)
```

## Q13 historical red-before
Fetched `8ea41f9ed8ba0ee8dd1bcf31cb83d9b5c589092b` into scratch repo `/tmp/fxgate-r25-scratch-4tyfr0bo`; fetch and test did not write to the lane repository.
```
python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_timing_check.py --lesson corpus/lessons/round-25.md --commit 8ea41f9ed8ba0ee8dd1bcf31cb83d9b5c589092b --repo /tmp/fxgate-r25-scratch-4tyfr0bo
# exit 1; FAIL line 29 Gate admit; output names the Q10 cell and reports generic seat reference 'wave-2 seats'; second-seat-reports=0
```

## Review and residual risk
`gate_timing_check.py:568-598,610-623` reads the requested lesson, tree inventory and blobs through `git show`/`git ls-tree` at the supplied revision; `:316-339,352` rejects absent, empty/non-regular, unregistered, self-review, candidate-missing and no-verdict reports. The commit pair demonstrates the observable distinction despite identical lesson bytes and a report present in the child working tree. Q13's separate 8ea41f9 red-before also reproduces.

Residual scope: Q13 is expressly structural, not an interpreter of contradictory reviewer findings (`corpus/lessons/round-26.md:39-41`); this check does not establish that a report's verdict is substantively correct. No actionable timing/support defect observed in this assignment.

VERDICT: scoped pass — Q13's commit-tree timing and required red-before behavior reproduce; no actionable in-scope finding.