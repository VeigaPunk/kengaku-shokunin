# S6ReadmeInventory — scoped findings (round 55 w1, 2026-10-30)

Deliverable: `.ufo/waves/round-55/w1/S6ReadmeInventory/round55-artifacts.md` — the
`corpus/README.md` `## Round-55 supporting artifacts (2026-10-30)` section draft for the L1
to splice, in the Round-26 house style (`| Path | Covers |` table, corpus-relative paths).

Inventory grounded at HEAD `80afa613` (freeze; base `798f5e9e`):

- Landed rows: `plans/round-55-claims.md` (frozen claims), `plans/round55_c2_controls.py`
  (C2 laundering-fixture builder), `.ufo/waves/round-55/claims/c1-before.txt`,
  `c2-before-abbreviated-selftest.txt`, `c2-before-uv-decoy-script.txt`, `c3-before.txt`,
  `census-before.txt` (each described from its own bytes).
- **PENDING-L1** rows (explicitly tagged; nothing committed): counter
  `plans/round55_c2_entryargv.py`, probe `plans/round55_c3_chess_probe.py`, receipt
  `evidence/round55/chess-best-move-probe.txt`, entry `knowledge/tb2-chess-best-move-grader.md`.
  Draft's closing note: L1 drops a tag when the artifact lands at splice.

Defects found (reported, not fixed):

1. Spec's "five before receipts + census-before" ≠ reality: claims/ holds 4 c*-before
   receipts + census-before (5 files).
2. "README's `## Round26 supporting artifacts`" is not in lane-root README.md; it is
   corpus/README.md `## Round-26 supporting artifacts` (:456). Style split flagged: rounds
   30+ use `### Round-NN evidence` bullets (README ends at `## Round-52 evidence`); spec
   pins the Round-26 table, which I used.
3. `plans/round55_c3_chess_probe.py` exists untracked in the worktree though spec lists it
   pending; kept PENDING-L1 (not landed), noted in the draft.
4. Sibling in-flight state at report time: `M corpus/SOURCES.md`, `?? corpus/lessons/round-55.md`.

Verification: all receipts read directly; one read-only `git log/ls-tree/status` (exit 0).
No scripts run, no scratch dir, no installs, no network. Full report:
`.ufo/waves/round-55/w1/S6ReadmeInventory/report.md`.
