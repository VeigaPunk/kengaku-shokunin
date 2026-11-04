# README index rows for round 84 (draft for the L1 to install)

Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Target file: `corpus/README.md`. Rows only; no README byte is edited by this seat. The row shapes below are copied from the live tables in `corpus/README.md`: the lesson index table (`### Lessons index rows (36)`, header `| Entry | Covers | Pointer |`, three cells, first cell exactly the backticked `lessons/<file>` path) and the evidence index list (`### Evidence index rows (20)`, one `- \`corpus/evidence/<dir>/\` — <text>` bullet per directory).

## 1. Lesson index row (append to the lesson index table, after the `lessons/round-83.md` row)

| Entry | Covers | Pointer |
|---|---|---|
| `lessons/round-84.md` | Round 84 — the second located offline replay of the base-unexecuted `gcode-to-text` grader (R84-C1) and the round-83 admission-bar debt in `knowledge/tb2-code-from-image-offline.md` repaired under a successor Gate (R84-C2); Gate S271, corrections R83-V1/R83-V2, mined mistake M84-1 | LOG.md round 84; plans/round-84-claims.md |

The three cells are exactly the shape of the `lessons/round-83.md` row above it in the same table. The `Pointer` cell names the two surfaces a reader needs: the round's LOG entry and the frozen claims doc.

## 2. Evidence index bullet (append to the evidence index list, after the `corpus/evidence/round83/` bullet)

- `corpus/evidence/round84/` — round-84 claim receipts: the `gcode-to-text` member replay receipt, the C1 counter's before/after and control runs, the C2 admission counter's base/selftest/mutant/control runs, and the Q13 gate-timing transcripts.

This bullet is required, not optional: `plans/round75_c1_index_parity.py` enumerates `corpus/evidence/*/` from disk and reports `MISSING-EVIDENCE <dir>` for any directory the README does not mention, so a `corpus/evidence/round84/` directory installed without this bullet is an index-parity defect at the round's own gate. The bullet's wording follows the `corpus/evidence/round83/` bullet's shape (directory, then the receipt groups it holds).

## 3. The S271 knowledge-tie

**No new knowledge index row is applicable for S271, and none is proposed.** The reasoning, from the frozen claims doc `plans/round-84-claims.md` (R84-C1, "Sourced claim" paragraph) and the source seat's drafted row:

- S271 is a `corpus/SOURCES.md` row for the pinned upstream `gcode-to-text/tests/test_outputs.py`, whose scope is "member replay only — pinned grader acceptance semantics; not a solved-task, model or image claim".
- Round 84 admits no new knowledge entry for `gcode-to-text`. The only knowledge file this round touches is the already-admitted `corpus/knowledge/tb2-code-from-image-offline.md`, and the round-84 change to it is a header repair (the `recheck:` line gains a date or cadence plus a named re-check action and the pin or a re-pin cadence; a `writer:` field is added at line 4) plus a successor admission recorded in `corpus/lessons/round-84.md`'s Gate — not a new entry.
- Therefore the existing knowledge index row for `corpus/knowledge/tb2-code-from-image-offline.md` (its `Primary source` cell `S267; plans/round83-cases.json; corpus/evidence/round83/code-from-image-probe.txt`) remains accurate and is not rewritten: S267 still grounds that entry's source line, and the round-84 repair changes no source cell of it. A new `knowledge/<file>.md` row for S271 would be an orphan row under the parity gate, since no such file is on disk.
- The tie S271 does need is inside `corpus/SOURCES.md`, not inside `corpus/README.md`: the S271 row's `used-by` cell should name `corpus/lessons/round-84.md` (the lesson whose Gate records the row) and may also name the located receipt `corpus/evidence/round84/gcode-to-text-probe.txt`. The source seat's drafted row at `.ufo/waves/round-84/w1/SourceR84/S271-row.md` is the L1's to install; its `used-by` cell is the surface this tie lands on.

## 4. The `## Frontier` section — no bullet proposed, and why

`corpus/README.md`'s `## Frontier` block records each partially-discharged frontier item as a `  - *Partly discharged round N (date):* …` sub-bullet under its parent item. Round 84 proposes no such sub-bullet, for two reasons that can be checked against the lane's own history:

- The most recent TB2-grader sub-bullets stop at `*Partly discharged round 72 (2026-11-03/04):*` under the `Agentic benchmark task-spec audits` item. Round 83, which read and executed the `code-from-image` grader and did admit a knowledge entry for it (`corpus/knowledge/tb2-code-from-image-offline.md`, indexed in the knowledge index table), added **no** Frontier sub-bullet; it added the knowledge index row and the evidence index bullet instead. Round 84 admits no knowledge entry, so it has neither of those two surfaces for a Frontier bullet to point at.
- A Frontier sub-bullet's text is a claim about what a round discharged ("the clause is narrowed for that one task only"); round 84's own claims doc makes no such claim for `gcode-to-text` — the member replay is coverage, and the calibration claim is a repair of an existing entry's admission bar.

If the L1 decides a Frontier line is wanted anyway, the shape-matched one-liner under `Agentic benchmark task-spec audits` would be:

  - *Partly discharged round 84 (2026-11-04):* the `gcode-to-text` grader's two captured test functions are replayed offline over the frozen eight-case, two-leg table in `plans/round84-cases.json`, with the located receipt `corpus/evidence/round84/gcode-to-text-probe.txt` and the S271 source row; the member stays inside the existing `file-artifact` class and nothing else in the clause is discharged.

This bullet is offered as a drafting option only. It is not proposed, and no Frontier byte should be added on the strength of this seat's draft alone: the sentence must not be installed until the round's own committed receipts carry the figures it would state.

## 5. What the L1 still owns for the README

- Installing rows 1 and 2 into `corpus/README.md` (rows only; the L1 owns the edit).
- Installing the S271 row into `corpus/SOURCES.md` with the `used-by` tie named in section 3.
- The `corpus/README.md` row count headings (`### Lessons index rows (36)`, `### Evidence index rows (20)`) are denominators a reader can check; the L1 updates them when the rows land.
- `plans/round75_c1_index_parity.py --lane .` re-derives all three universes from disk after the install; this seat did not run it against a tree carrying the new rows, because the rows are drafts and no file this seat owns lands them.
