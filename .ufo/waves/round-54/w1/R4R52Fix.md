# R4R52Fix — DO-NOT-INTEGRATE

Review: `.ufo/waves/round-54/w1/R4R52Fix/review.md`.
Evidence: `.ufo/waves/round-54/w1/R4R52Fix/evidence.json` and `independent-delta.diff`.

- P1: patched counter falsely turns the existing green `order-check` row red; old entry exits 0, patched entry exits 1. No-harm acceptance fails.
- P2: new K7 selftest passes even when ENTRY-MISSING is removed from verdict logic, because unrelated MISSING failures mask that mutation.
- Diff contains only negation handling and three added selftest cases. All three original cases remain; old selftest 3/3 and patched 6/6 pass, but K7 coverage is confounded.
- Independent same-fixture reproduction confirms old misses the intended mixed-negation defect and patched catches it.
- Neither version accepts --dry; both usage failures are not valid no-harm evidence. Supported read-only entry calls were compared instead.

Axes: novelty, calibration. Recommendation only, not admission. LSP unavailable (`No such tool: xd://lsp`), so literal source/reference checks used. No tools installed; no production edits or git mutations; scratch deleted. Full commands and limits are in review.md.
