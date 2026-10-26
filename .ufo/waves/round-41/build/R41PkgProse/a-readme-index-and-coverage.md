# Block (a) — corpus/README.md: knowledge index row + one coverage-map bullet

Draft only. L1 applies. Both rows are single physical lines in the target file (the repo's
style: one table row / one bullet per line, however long).

Every number below comes from `corpus/evidence/round41/constraints-probe.txt`:
summary `cases=25 observed_pass=6 observed_fail=19 mismatches=2` (receipt:33), determinism line
`regrade cases=25 differ=0` (receipt:32). Case cites are `receipt:<n>`.

## (a1) `corpus/README.md` — insert one row immediately AFTER the existing line 73

Anchor (existing line 73, the round-40 row — do not modify it):

```
| `knowledge/tb2-db-wal-recovery-grader.md` | A sixth Terminal-Bench 2.0 task grader read and executed: …
```

Paste (new line 74):

```
| `knowledge/tb2-constraints-scheduling-grader.md` | A seventh Terminal-Bench 2.0 task grader read and executed, and a grader class new to this lane: `constraints-scheduling`'s three pytest functions compute the verdict with a scheduling model embedded in the test file — `_hard_ok`, `_overlap` and a minute-granularity earliest-slot scan over three sha256-pinned input calendars — and read the graded ICS with regexes, not an ICS parser — so a hand-typed Wed 11:00 file passes 3/3 without reading a calendar, a decoy first `VEVENT` passes 3/3 with the attendee meeting on Friday 15:00 (published: TB2.1 PR #245), the earliest test passes slots that violate the hard constraints (`bob-start-0900-wed`, `wed-1059-overlaps-alice`: `PFP`), rewriting all three input calendars with CRLF line ends passes 3/3 although `instruction.md:17-18` says any modification fails, `DTEND` is read only by the structure test (`duration-90min`: `FPP`), and three RFC 5545-valid output forms fail while CRLF output passes (`cases=25 observed_pass=6 observed_fail=19 mismatches=2`, `regrade cases=25 differ=0`) | S122, S123 (terminal-bench-2 @ 2fd12b88); TB2.1 PR #245 (prior art, to open as S124); probe `plans/constraints_probe.py`, receipt `evidence/round41/constraints-probe.txt` |
```

Row discipline checked against the round-40 row it follows: one line; entry path first cell;
what the grader is and what passes it in the second cell ending with the two summary numbers;
sources + probe + receipt in the last cell. S124 is written as "to open as S124" because no
`S124` row exists in `corpus/SOURCES.md` at draft time (`grep -n "S122\|S123\|S124"
corpus/SOURCES.md` → no match, 2026-10-26 15:39) — replace that parenthetical with `S124` once
the registry rows land.

## (a2) `corpus/README.md` — insert one bullet immediately AFTER the existing line 267

Anchor (existing line 267, the round-40 bullet's last sentences — do not modify it):

```
… The passing vacuum is bounded by length, id multiset and the 22 pinned cells … Not runtime task validity, not contamination measurement, not deployment config.
```

Paste (new line 268):

```
- **Terminal-Bench 2.0 task grader (seventh task, embedded-scheduling-model class)**: covered at source-code depth and executed offline (round 41, 2026-10-26) — knowledge/tb2-constraints-scheduling-grader.md; S122, S123; probe `plans/constraints_probe.py`, receipt `evidence/round41/constraints-probe.txt`. A seventh instance of the same ground (7 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `constraints-scheduling` only: the verdict is no longer an assertion over a fixed artefact but a computation — `_hard_ok` and `_overlap` are a scheduling model embedded in the test file that rescans the three sha256-pinned calendars at minute granularity, so the graded state is a one-event ICS file and the grader's own model decides it (`cases=25 observed_pass=6 observed_fail=19 mismatches=2`, `regrade cases=25 differ=0`). The passing six are the task's own `solve.sh`, a hand-typed correct file that never reads a calendar, a decoy-first file, a CRLF-line-end file, a file with a fourth attendee, and a run that rewrote all three inputs with CRLF (`receipt:8,9,14,24,29,31`); the unanswered surfaces are whether any calendar was read, which `VEVENT` is the meeting (tests 2-3 read the file's first `DTSTART`, so `decoy-first-vevent` passes 3/3, `receipt:14`), whether an invalid-but-unpreceded slot is caught (`bob-start-0900-wed` and `wed-1059-overlaps-alice`, both `PFP`, `receipt:13,23`), byte-level input integrity (`input-crlf-rewrite` 3/3 against `instruction.md:17-18`, `receipt:31`), and RFC 5545 conformance (three valid forms fail: `folded-attendee-line`, `dtstart-value-datetime`, `lowercase-property-names`, `receipt:25,26,30`). Not runtime task validity, not contamination measurement, not deployment config.
```

Bullet discipline checked against round 39/40: bold label carrying the ordinal and a class
name, "covered at … depth and executed offline (round N, date) — entry; sources; probe,
receipt", what is discharged, the bound, the unanswered surfaces, the three refusals.

## Facts the prose relies on (each with its source)

| claim | source |
|---|---|
| 25 cases, 6 pass, 19 fail, 2 prediction mismatches | `corpus/evidence/round41/constraints-probe.txt:33` |
| second grading of every un-rebuilt end state agrees | `constraints-probe.txt:32`; mechanism `plans/constraints_probe.py` docstring (lines 23-25) |
| hand-typed file passes 3/3 | `literal-correct-slot`, `constraints-probe.txt:9` (`tests=PPP`) |
| decoy first VEVENT passes 3/3; tests 2-3 read the first `DTSTART` of the whole file | `decoy-first-vevent`, `constraints-probe.txt:14`; `test_outputs.py:135`, `:151` |
| earliest test passes invalid earlier slots | `bob-start-0900-wed` `PFP` (`:13`), `wed-1059-overlaps-alice` `PFP` (`:23`) |
| CRLF rewrite of all three inputs passes 3/3 | `input-crlf-rewrite`, `constraints-probe.txt:31`; check `test_outputs.py:88-96`; instruction claim `instruction.md:17-18` |
| DTEND read only by the structure test | `duration-90min` `FPP`, `constraints-probe.txt:15`; `test_outputs.py:127` vs `:136` |
| RFC 5545-valid forms fail | `folded-attendee-line` `FPP` (`:25`), `dtstart-value-datetime` `FFF` (`:26`), `lowercase-property-names` `FPP` (`:30`) |
| CRLF output passes | `crlf-line-endings` `PPP`, `constraints-probe.txt:24` |
| 7 of 89 | rounds 35-40 read 6 (`corpus/README.md:326-340`, "6 of 89 read"); this row adds the seventh |
