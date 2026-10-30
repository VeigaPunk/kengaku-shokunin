# Seat E9IndexAndReadme — round 55 wave 1 (v2) seat report

Seat: `E9IndexAndReadme` (leaf, index parity + frontier narrowing for R55-C3 landing).
Scope written: `corpus/README.md`, `PROVINCE.md` only. Reports under
`.ufo/waves/round-55/w1/E9IndexAndReadme/`. No other lane file touched; `corpus/SOURCES.md`
shows 2 added lines in `git diff --stat` from a concurrent sibling seat (E8SourcesRows owns it) —
not this seat's edit.

## What I ran (commands + exit codes)

All read-only inspection plus four `edit` calls and one append; no git/jj mutation.

1. Read frozen claims: `plans/round-55-claims.md` (commit 80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb) — exit 0 (read tool).
2. `mkdir -p /fast/scratch/hyaku/kengaku-r55/E9IndexAndReadme .ufo/waves/round-55/w1/E9IndexAndReadme` — exit 0.
3. Inventory probes (`ls`/`grep` on the lane repo): established that at seat start
   `corpus/evidence/round55/` and `corpus/knowledge/tb2-chess-best-move-grader.md` were ABSENT
   (receipt and entry are sibling-owned, written concurrently).
4. `edit corpus/README.md` — added knowledge index row after the `external-anchor-freeze` row — exit 0.
5. `edit corpus/README.md` — appended the round-55 sub-bullet under the Frontier
   `Agentic benchmark task-spec audits` item, after the round-46 sub-bullet — exit 0
   (first attempt failed on fuzzy-match threshold; retried with a longer unique anchor — success).
6. `edit corpus/README.md` — appended `### Round-55 evidence (2026-10-30)` section after
   `### Round-52 evidence` — exit 0.
7. `cat >> PROVINCE.md` — appended `## Round55 partial frontier admission (2026-10-30)` — exit 0.
8. Re-checked: `corpus/evidence/round55/chess-best-move-probe.txt` had landed (sibling seat);
   read its summary line `cases=12 observed_pass=5 observed_fail=7 mismatches=0`,
   `PREDICATE R55-C3 pass`; filled those counts into all three README spots + PROVINCE
   (four `edit` calls, all exit 0), replacing the "receipt pending at index time" placeholders
   per the seat spec's conditional.
9. Acceptance greps: `grep -c chess-best-move corpus/README.md` → **5** (≥3 required), exit 0;
   `grep -c "13 of 89 read" PROVINCE.md` → **1**, exit 0.
10. Table parse check: python per-table-block pipe-count scan over both files — the only
    inconsistent blocks are pre-existing (README lines 73, 532–544, 551–554; PROVINCE lines 10–21,
    107–118); every line this seat added is pipe-consistent with its table (knowledge row: 4 pipes,
    3 columns, same as its neighbours). No new broken tables.
11. `git diff --stat` — PROVINCE.md +22, corpus/README.md +14 (a sibling's concurrent +2 in
    corpus/SOURCES.md is not mine).

## Files written

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md`
  - knowledge index row for `knowledge/tb2-chess-best-move-grader.md` (3-column shape matched);
  - Frontier sub-bullet `Partly discharged round 55 (2026-10-30)` under agentic-benchmark item;
  - `### Round-55 evidence (2026-10-30)` section (dir + probe receipt bullet).
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/PROVINCE.md`
  - `## Round55 partial frontier admission (2026-10-30)` (Core-addition paragraph + reported-out).
- Reports: this file and `report.md` in this directory.

## Counts filled (from the landed receipt)

`corpus/evidence/round55/chess-best-move-probe.txt:13` —
`cases=12 observed_pass=5 observed_fail=7 mismatches=0`, `PREDICATE R55-C3 pass`.
Case list cross-checked (both-lowercase-two-lines P, reversed-order P, single-move-only F,
uppercase-white F, extra-decoy-move F, duplicate-move F, whitespace-padded P, empty-file F,
crlf-line-endings P, instruction-example-h1h8 F, fullwidth-unicode-digit F, + both-space-separated P).

## Defects found

- One defect in this seat's own text, caught post-landing by scout `SC1UpstreamContext-3`:
  the PROVINCE round-55 paragraph said "the remaining 86 unread TB2 task graders"; 89 − 13 = 76.
  Corrected in place to "remaining 76 unread TB2 task graders" and the scout acknowledged.
  The scout's second note (the literal "12 of 89 read" lives in `corpus/README.md`, not
  PROVINCE.md, whose convention is "(89 carry tests/test.sh; M are read)") was assessed as
  informational: the frozen claim's narrowing is satisfied by the new section's "13 of 89 read",
  no edit made.
- Observed: `corpus/knowledge/tb2-chess-best-move-grader.md` (E7KnowledgeEntry's
  file) was still absent at seat end — the README index row and PROVINCE paragraph reference it as
  the round's admitted entry per the frozen claims; the L1 integrate step should confirm the entry
  lands or adjust the row.

## Dead ends

- First Frontier edit attempt failed (fuzzy whitespace match below 95% against a long line);
  resolved by anchoring on a longer unique substring. No other dead ends; no installs/upgrades
  were needed (no tool installs this seat).

## Scratch

`/fast/scratch/hyaku/kengaku-r55/E9IndexAndReadme/` was created empty and deleted at seat end
(nothing needed staging; receipts live in the lane repo).
