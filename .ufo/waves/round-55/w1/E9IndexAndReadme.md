# E9IndexAndReadme — scoped findings (round 55, w1)

Seat scope: index parity + frontier narrowing in `corpus/README.md` and `PROVINCE.md` for the
R55-C3 landing (13th TB2 grader, chess-best-move). Both files edited, acceptance greps green.

## Changes (files this seat wrote)

`corpus/README.md` (+14 lines):
1. Knowledge index row for `knowledge/tb2-chess-best-move-grader.md` — 3-column shape matched —
   after the `external-anchor-freeze` row, before the lessons rows.
2. Frontier: new sub-bullet `Partly discharged round 55 (2026-10-30)` under
   `Agentic benchmark task-spec audits` (after the round-46 sub-bullet): full-multiset token
   equality class, distinct from round 45's line-split membership; clause narrowed for that one
   task only; "13 of 89 read".
3. New `### Round-55 evidence (2026-10-30)` section after `### Round-52 evidence`: dir
   `corpus/evidence/round55/` + probe receipt bullet.

`PROVINCE.md` (+22 lines): appended `## Round55 partial frontier admission (2026-10-30)` —
Core-addition paragraph (static interpretation + offline synthetic-fixture execution at the pin;
owns reading/executing captured scoring code; refuses task image, harness, real submissions,
runtime validity, contamination, model behaviour, remaining 86 unread graders; 12→13 narrowing,
"13 of 89 read") + `Reported out: none absorbed.` Style matches round 37/38 sections.

## Counts

Written first with "receipt pending at index time" placeholders (receipt absent at seat start),
then filled from the landed receipt `corpus/evidence/round55/chess-best-move-probe.txt:13`:
`cases=12 observed_pass=5 observed_fail=7 mismatches=0`, `PREDICATE R55-C3 pass`.
Filled in all four spots (README knowledge row, Frontier bullet, evidence section; PROVINCE).

## Verification exercised

- `grep -c chess-best-move corpus/README.md` → 5 (acceptance ≥3).
- `grep -c "13 of 89 read" PROVINCE.md` → 1 (acceptance: contains).
- Python per-table-block pipe-count scan of both files: all inconsistencies pre-existing
  (README :73, :532–544, :551–554; PROVINCE :10–21, :107–118); added rows are shape-consistent.
- `git diff --stat`: PROVINCE.md +22, corpus/README.md +14. (`corpus/SOURCES.md` +2 is a
  concurrent sibling edit — E8SourcesRows owns that file; not touched by this seat.)

## Defects / notes for L1

- Self-defect fixed post-landing (scout `SC1UpstreamContext-3`): "remaining 86 unread" →
  "remaining 76 unread" (89 − 13 = 76) in the PROVINCE round-55 paragraph. Scout's second note
  (literal "12 of 89 read" is README's string; PROVINCE uses its own "(M are read)" convention)
  assessed informational — the frozen narrowing is satisfied by "13 of 89 read" in the new section.

- `corpus/knowledge/tb2-chess-best-move-grader.md` (E7KnowledgeEntry's file) still absent at seat
  end; README/PROVINCE reference it per the frozen claims — confirm it lands at integrate.
- No installs/upgrades needed. Scratch dir `/fast/scratch/hyaku/kengaku-r55/E9IndexAndReadme/`
  created and deleted. No git/jj mutation performed (read-only `git diff`/`grep` only).
