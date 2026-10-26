# Block (b) — corpus/README.md §Frontier: the TB2 sub-bullet narrowed to "7 of 89 read"

Draft only. L1 applies. The parent bullet ("**Agentic benchmark task-spec audits**") and every
existing sub-bullet stay byte-identical; this adds one sub-bullet at the end of that bullet's
block and changes nothing in rounds 35-40's text, whose "N of 89 read" counts stay true of
those rounds.

Numbers: `cases=25 observed_pass=6 observed_fail=19 mismatches=2` and `regrade cases=25
differ=0` (`corpus/evidence/round41/constraints-probe.txt:33`, `:32`).

## Insert position

`corpus/README.md` line 340 is the last line of the round-40 sub-bullet ("… not model or agent
behaviour."); line 341 begins the next parent bullet ("- **Contamination transparency cards**").
Insert the block below as new lines 341-355, before that parent bullet.

## Paste

```
  - *Partly discharged round 41 (2026-10-26):* `knowledge/tb2-constraints-scheduling-grader.md` reads and executes a
    seventh Terminal-Bench 2.0 task's scoring code (`constraints-scheduling/tests/test_outputs.py` @ `2fd12b88`; S122,
    S123) against its `instruction.md`, probe `plans/constraints_probe.py`, receipt
    `corpus/evidence/round41/constraints-probe.txt`. The graded state is a class the lane had not executed before: a
    one-event ICS file at `/app/meeting_scheduled.ics` decided by a scheduling model embedded in the test file —
    `_hard_ok`, `_overlap` and a minute-granularity earliest-slot scan over three sha256-pinned input calendars — so
    the grader computes the verdict instead of asserting it over a fixed artefact, and it reads the ICS with regexes,
    not an ICS parser, so a hand-typed Wednesday 11:00 file passes 3 of 3 without opening a calendar, a decoy first
    `VEVENT` passes 3 of 3 with the attendee meeting on Friday 15:00, the earliest test passes slots that violate the
    hard constraints because no valid slot precedes them, rewriting all three inputs with CRLF line ends passes 3 of 3
    although `instruction.md:17-18` says any modification fails, `DTEND` is read only by the structure test, and three
    RFC 5545-valid output forms fail while a CRLF output passes (`cases=25 observed_pass=6 observed_fail=19
    mismatches=2`). The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the
    remaining TB2 task graders (7 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for
    runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image (never pulled) or a harness
    run (the task's own `solve.sh` is executed as one case and observed pass), not contamination, not model or agent
    behaviour.
```

Why each clause is safe:

- "three sha256-pinned input calendars" — receipt header pins all three (`:2-4`).
- "a hand-typed … passes 3 of 3" — `literal-correct-slot` `tests=PPP` (`:9`).
- "decoy first `VEVENT` … Friday 15:00" — `decoy-first-vevent` `PPP` (`:14`), described there verbatim.
- "earliest test passes slots that violate the hard constraints" — `bob-start-0900-wed` and
  `wed-1059-overlaps-alice`, both `PFP` (`:13`, `:23`); the only failing letter is test 2.
- "CRLF … passes 3 of 3 … any modification fails" — `input-crlf-rewrite` `PPP` (`:31`); the
  instruction sentence is `instruction.md:17-18`.
- "`DTEND` is read only by the structure test" — `duration-90min` `FPP` (`:15`); tests 2-3
  recompute the end as start + 1 hour (`test_outputs.py:136`).
- "three RFC 5545-valid output forms fail while a CRLF output passes" — `folded-attendee-line`
  `FPP` (`:25`), `dtstart-value-datetime` `FFF` (`:26`), `lowercase-property-names` `FPP`
  (`:30`) against `crlf-line-endings` `PPP` (`:24`).
- "7 of 89" — the round-40 sub-bullet above states "6 of 89 read"; the counts of 35-40 are
  left untouched because each is true of the round that wrote it.
