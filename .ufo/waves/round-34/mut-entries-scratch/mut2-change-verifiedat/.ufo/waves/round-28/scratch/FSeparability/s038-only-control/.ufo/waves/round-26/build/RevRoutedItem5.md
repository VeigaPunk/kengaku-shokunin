# RevRoutedItem5 — P3 coverage review (calibration)

## Finding — Medium: round-25 self-assertions remain outside P2∪P3

- The routed item itself is covered, with one dependency: `plans/state_check.py:465-469` emits `OUT_OF_POPULATION` for every capability row outside frozen `CAPABILITY_IDS`; the preregistration requires unchanged P2 results on the base tree (`plans/round-26-claims.md:143-146`). P3a explicitly freezes the two named round-25 capability cells and checks every numeric token against named receipts (`:128-130`). P3e separately covers README out-of-population rows/files in both directions (`:137-138`). Together these cover item 5's two row identities, OOP reporting, and numeric pins.
- Duplicate C2 summaries are not covered: `SCORECARD.md:704` repeats base/tip mismatch counts (`10→0`, plus `6→0` under the narrower P2c reading), and `:719` repeats base/tip capability results. P3a scopes numeric checks to the two capability cells, not these summaries; P2 does not parse these claims.
- The round-25 axis score tuple at `SCORECARD.md:721-722` is also unverified. P2's axis parser locates only the round-24 table and checks rows/anchors (`plans/state_check.py:521-568`); P3d pins the targets of backticked line anchors, not the axis-value cells themselves (`plans/round-26-claims.md:136`).
- The round-25 lesson's correction claims remain outside the checker: `corpus/lessons/round-25.md:94-99` states the corrected 10 mismatch / 4 PROVINCE path-row / 6 narrow-P2c counts and unchanged revert-test counts; `:103-104` states two of three L0 questions were re-filed. P3e only checks README index/file membership, not lesson contents (`plans/round-26-claims.md:137-138`); P2 likewise does not parse these lesson assertions.

## Verification gaps

- Reviewed the frozen preregistration, P2 source, relevant Scorecard/Province/lesson text, and the committed v2 base receipt. No tests/builds were run (review-only assignment).
- `read xd://lsp` returned `No such tool: xd://lsp`; no LSP server/status or semantic queries were available. No grep-based semantic proof used.
- No tools installed or updated.

VERDICT: P3a plus unchanged P2 OOP reporting and P3e cover routed item 5; add explicit checks or document as out of scope for the uncovered C2 summaries, round-25 axis values, and lesson correction assertions above.