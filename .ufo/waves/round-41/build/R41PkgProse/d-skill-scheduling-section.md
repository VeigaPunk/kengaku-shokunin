# Block (d) — SKILL.md: decision-table section "Scheduling-constraint TB2 grader — round 41"

Draft only. L1 applies. Append at the end of `SKILL.md` (after existing line 1030) as a new
`##` section carrying a `### Decision table` subsection, in the shape of `## Database-recovery TB2
grader — round 40` (lines 958-1030): when to run the probe and what its exit code means → the
class in one paragraph → the decision table → "what a green means here" → the requirement-label
paragraph derived by the C2 counter's V7 rule → limits → the closing property line.

Every number cites `corpus/evidence/round41/constraints-probe.txt` (`cases=25 observed_pass=6
observed_fail=19 mismatches=2` at `:33`; `regrade cases=25 differ=0` at `:32`), and every quote
carries `file:line`.

## Paste (append at end of file)

```
## Scheduling-constraint TB2 grader — round 41

Before citing the pinned TB2 `constraints-scheduling` scorer, run `python3 plans/constraints_probe.py --lane .` and
read its summary line: exit `0` means only that all 25 cases produced three test verdicts twice each; prediction
mismatches are on the summary line, never in the exit code, and exit `2` is a setup failure — a duplicate or
malformed case id, an unknown tag, a malformed prediction, a capture missing or not at its pinned digest,
`/usr/bin/bwrap` or python3/bash not executable, a `--work` directory that cannot be created, or a case that did not
yield three verdicts twice (a recipe error is never a verdict) (`plans/constraints_probe.py:291-345`). `--dry` prints
the frozen case table with no sandbox and `--stage-check` builds each case's end state and prints only stage exit
codes, the grader never imported (`plans/constraints_probe.py:4-8`), so neither is evidence. The receipt's summary
(`corpus/evidence/round41/constraints-probe.txt:33`) reads `cases=25 observed_pass=6 observed_fail=19 mismatches=2`,
and a second, same-process grading of each un-rebuilt end state agrees case by case (`regrade cases=25 differ=0`,
`:32`) — a determinism read of the probe, not re-run stability (entry §Regrade).

The class differs from rounds 35-40: the verdict is **computed**, not asserted over a fixed artefact. Three pytest
functions carry a scheduling model — `_hard_ok` (Bob start, Alice end, Tue/Thu early end, Carol day end and lunch,
same-day, weekday), `_overlap` (a zip of two independent `DTSTART`/`DTEND` `findall`s per calendar) and a
minute-granularity earliest-slot scan — and apply it to three sha256-pinned input calendars
(`corpus/evidence/round41/tb2-constraints-scheduling/test_outputs.py:46-83`, `:158-167`; calendar digests in the
receipt header, `:2-4`). The graded artefact is a one-event ICS file at `/app/meeting_scheduled.ics`, read with
regexes (`_dt`, `:40-43`), never with an ICS parser. The probe seeds `/app` as the task Dockerfile does
(`Dockerfile:14`), runs a frozen recipe under `bash -euo pipefail`, then imports the captured module and calls its
three functions in file order inside a per-case bubblewrap sandbox (`plans/constraints_probe.py:10-21`), so
`tests/test.sh`'s `uvx -p 3.13`/pytest path and its `/logs/verifier/reward.txt` write (`test.sh:18-22,25-29`) are
read, not run.

### Decision table — what the grader reads, and what passes it

| what the grader actually reads | what passes | what a reviewer should check instead | cite |
|---|---|---|---|
| the three `/app/*_calendar.ics` as *decoded text* — `app_text == repo_path.read_text()`, or, when the repo copy is absent, `sha256(app_text)` (`test_outputs.py:88-96`) | a rewrite that changes bytes but not the newline-normalized text: `input-crlf-rewrite` passes 3/3 while `input-appended` and `input-event-deleted-wed-1000` fail (`tests=FPP`) | the bytes and the line endings, not the decoded string; `instruction.md:17-18` promises "Any modification will cause the tests to fail" | `input-crlf-rewrite` (receipt:31), `input-appended` (receipt:21) |
| `BEGIN:VCALENDAR`…`END:VCALENDAR` after `strip()`, `VERSION:2.0`, `PRODID:`, `BEGIN/END:VEVENT` (`:97-103`), then the block containing `SUMMARY:Team Planning Meeting` and all three emails (`:106-118`) | a file whose first `VEVENT` is a decoy elsewhere in the block list — tests 2-3 never open this block, so `decoy-first-vevent` passes 3/3 with the attendee meeting on Friday 15:00 | locate the meeting the way tests 2-3 do, then compare; the structure test is the only one that looks at the meeting block at all | `decoy-first-vevent` (receipt:14), `decoy-second-vevent` (receipt:28) |
| `^ATTENDEE[:;].*<email>$` under `re.I \| re.M` inside that block (`:120-123`) | the three emails each on their own unfolded line; a fourth attendee is free — `extra-attendee-dave` passes 3/3, and a folded `ATTENDEE` line (RFC 5545 3.1) fails the structure test | an ICS parser, or a fold-aware regex; the check is line-anchored text | `extra-attendee-dave` (receipt:29), `folded-attendee-line` (receipt:25) |
| `_dt(r"DTSTART:(\d{8}T\d{6}Z)", meeting)` and the same for `DTEND`, then `e - s == timedelta(hours=1)`, `2024-01-15..19`, `weekday() < 5` (`:125-129`) | the exact flat `DTSTART:…Z` spelling for one hour in that week — `duration-90min` fails only this test (`FPP`), `weekend-sat-20` fails all three, `no-prodid-header` and a wrong or partial attendee set fail only here | `DTEND` and the window yourself: tests 2-3 never read `DTEND` and recompute the end as start + 1 hour | `duration-90min` (receipt:15), `weekend-sat-20` (receipt:20), `no-prodid-header` (receipt:27) |
| tests 2 and 3 take the **first** `DTSTART:` of the whole file, not of the meeting block (`:135`, `:151`) | any file whose first `DTSTART` is not the meeting's: `decoy-first-vevent` 3/3 (receipt:14); the mirror `decoy-second-vevent`, with the attendee meeting first at Friday 15:00, is `PFF` | that the graded slot is the meeting's; both constraint tests are file-first-`DTSTART` tests (published as TB2.1 PR #245) | `decoy-first-vevent` (receipt:14), `decoy-second-vevent` (receipt:28) |
| `_hard_ok(start, start+1h)` then `_overlap` against the three calendars (`:58-83`, `:46-55`, called at `:137-143`) | the model's rules, minute-exact: `seconds-30` is `PFF` — test 1 accepts a `:30` start, test 2 fails because the end crosses into Carol's 12:00-12:30 lunch | the model's window, not the instruction's prose: Alice's "no meetings after 2 PM" becomes `t1.hour < 14 or (14,0)`, and the Bob Tue/Thu 4:30 branch (`:65-68`) is dead code once the Alice-end check (`:61`) has passed | `seconds-30` (receipt:18), `conflict-mon-1230` (receipt:12) |
| the earliest scan: every minute from Mon 09:00 to the graded start, `_hard_ok` and no overlap, raised as `Found earlier valid slot` (`:158-167`) | a slot that is itself invalid but has no *valid* predecessor: `bob-start-0900-wed` and `wed-1059-overlaps-alice` both fail only test 2 (`PFP`), so "earliest" cannot catch a wrong slot it never compares against a valid one | recompute the true earliest valid slot and compare equality; the test asserts absence of a valid *earlier* slot, not validity | `bob-start-0900-wed` (receipt:13), `wed-1059-overlaps-alice` (receipt:23) |
| `9 <= sched.hour < 12` as an unconditional assert (`:188`), plus the Monday tie-break (`:180-186`) and Carol's late buffer (`:190-208`) | a morning start; on the pinned calendars the only valid starts are already morning (`plans/constraints_probe.py:30-31`), so no frozen case witnesses the tie-break or the buffer | that the morning preference is a hard assert, not a tie-break, and that the tie-break/buffer branches are unfalsified by this case set | `later-valid-thu-1100` (receipt:11) fails only the earliest test |
| nothing — the three input calendars as *events* and the ICS as a dialect | the inverse of a green: RFC 5545-valid output forms fail (`folded-attendee-line` `FPP`, `dtstart-value-datetime` `FFF`, `lowercase-property-names` `FPP`) while a CRLF output and a hand-typed file pass | parse the output as iCalendar; "valid ICS format" (`instruction.md:21`) is enforced only as five substring/structure checks | `crlf-line-endings` (receipt:24), `folded-attendee-line` (receipt:25), `dtstart-value-datetime` (receipt:26), `lowercase-property-names` (receipt:30) |
| nothing — the calendars themselves | `literal-correct-slot` passes 3/3 with a hand-typed Wednesday 11:00 file that never reads a calendar | open the calendars and derive the slot yourself before crediting a solve | `literal-correct-slot` (receipt:9) |
| the task's own oracle and the do-nothing baseline | `oracle-solve-sh` is 3/3 and `nop` is `FFF` — all three tests read the output file, so its absence fails all of them (`error=FileNotFoundError` in each) | run both first: unlike round 40's grader this one starts at 0 of 3 | `oracle-solve-sh` (receipt:8), `nop` (receipt:7) |

What a green means here: in the probe's staged state, `/app/meeting_scheduled.ics` contained a `VEVENT` with
`SUMMARY:Team Planning Meeting`, all three attendee emails, a flat `DTSTART:…Z` and a one-hour `DTEND` inside
15-19 January 2024, the model accepted the first `DTSTART` of the file, no valid slot preceded it, and it started
before noon — on states the probe built, not states an agent built. What it does not mean: that any calendar was
read (`receipt:9`), that the graded slot belongs to the meeting VEVENT (`receipt:14`), that the input calendars are
byte-identical to the repo copies (`receipt:31`), that an invalid slot is caught when no valid slot precedes it
(`receipt:13,23`), that a 90-minute meeting is caught by any test but the first (`receipt:15`), that the tie-break
and Carol-buffer branches work (no case), or that the output is valid iCalendar (`receipt:25,26,30`).

Of the eleven frozen instruction tags (`plans/constraints_probe.py` `TAGS`, frozen lines in
`corpus/evidence/round41/constraints-dry-cases-freeze.txt:1-11`), the round-41 counter's V7 rule
(`plans/round41_c2_verify.py:232-272`, label rule `:224-229`; label = the observed verdicts of every receipt case whose `violates=` carries
the tag) gives: `window` (`instruction.md:1`) `enforced` — 1 case, 0 observed pass; `output-file` (`:10`)
`enforced` — 1, 0; `meeting-title` (`:10`) `enforced` — 1, 0; `attendees` (`:10`) `enforced` — 1, 0; `one-hour`
(`:10`) `enforced` — 1, 0; `hard-constraints` (`:12`) `partly` — 5, 1 pass (`decoy-first-vevent`); `no-conflict`
(`:12`) `enforced` — 5, 0; `inputs-readonly` (`:15`) `partly` — 3, 1 pass (`input-crlf-rewrite`);
`version-prodid` (`:23`) `enforced` — 1, 0; `utc-format` (`:25`) `enforced` — 1, 0; `earliest` (`:27`) `partly` —
10, 1 pass (`decoy-first-vevent`). `enforced` is a property of the frozen case set only: seven of the eleven tags
rest on a single witness, so the label means "every frozen case that violates it is observed fail", not "no
improving agent can violate it". `hard-constraints` and `earliest` are `partly` for the same case — the decoy's
Friday 15:00 meeting sits outside Alice's 14:00 limit and after every valid slot; `inputs-readonly` is `partly`
because the CRLF rewrite passes the text comparison the tag's line promises to fail. The entry's `## Requirement
map` carries one row per tag in the counter's row shape, and V7 re-derives all eleven labels from the receipt.

Limits named at freeze: the probe never runs Terminal-Bench, the task image (`task.toml:30` names
`alexgshaw/constraints-scheduling:20251031`; `allow_internet = true` at `:35`; `Dockerfile:3` builds it on
`ubuntu:24.04`) or a harness. Host python3 stands in for pytest under `uvx -p 3.13` (`test.sh:18-22`), which needs
the network; recipes run as the probing user rather than root; each case stages its own `/app`, so no case observes
the image's tree; and the grader is bound at `/cap/test_outputs.py`, so the `inputs/` sibling the integrity check
prefers is absent and its sha256 branch runs, as in the image (`plans/constraints_probe.py:10-21`). The ground-truth
valid-slot table is hand-read from the three captured calendars, not from the grader
(`plans/constraints_probe.py:27-31`: valid starts Wed 2024-01-17 11:00 and Thu 2024-01-18 11:00, earliest Wed
11:00). 16 of the 25 cases are the round-40 planning seat's pilot, graded before this freeze, with predictions
carried verbatim; the two it observed wrong (`later-valid-wed-1105`, `receipt:10`, and `seconds-30`, `receipt:18`)
were both predicted `PPF` — only the earliest test failing — and were observed `PFF`, test 2 failing as well, and
are reported, never edited out. The decoy finding (tests 2-3 read the first `DTSTART`) is published as TB2.1 PR
#245, so this entry claims a probed instance, not a discovery.

A property of this capture at `2fd12b88`; not a task-validity, difficulty or gameability verdict, not solver
advice, not a statement about RFC 5545 conformance in general, and not a statement about any agent's behaviour.
```

## Derivation of the label paragraph (reproducible)

```
python3 - <<'EOF'
import re
rec = open('corpus/evidence/round41/constraints-probe.txt').read().split('\n')
tags = [l.split()[1] for l in open('corpus/evidence/round41/constraints-dry-cases-freeze.txt') if l.startswith('TAG ')]
line = {l.split()[1]: l.split()[2] for l in open('corpus/evidence/round41/constraints-dry-cases-freeze.txt') if l.startswith('TAG ')}
cases = []
for l in rec:
    if not l.startswith('CASE '): continue
    m = re.search(r'violates=(\S*)', l); v = m.group(1) if m else ''
    cases.append((l.split()[1], re.search(r'observed=(\w+)', l).group(1),
                  set() if v in ('', '--') else set(v.split(','))))
for t in tags:
    v = [o for _c, o, vv in cases if t in vv]
    lab = 'enforced' if set(v) == {'fail'} else ('unenforced' if set(v) == {'pass'} else 'partly')
    print(t, line[t], lab, len(v), v.count('pass'))
EOF
```

Output at draft time (2026-10-26 15:44), matching the paragraph above and the counter's
`derive()` (`plans/round41_c2_verify.py:224-229`):

```
window instruction.md:1 enforced 1 0
output-file instruction.md:10 enforced 1 0
meeting-title instruction.md:10 enforced 1 0
attendees instruction.md:10 enforced 1 0
one-hour instruction.md:10 enforced 1 0
hard-constraints instruction.md:12 partly 5 1
no-conflict instruction.md:12 enforced 5 0
inputs-readonly instruction.md:15 partly 3 1
version-prodid instruction.md:23 enforced 1 0
utc-format instruction.md:25 enforced 1 0
earliest instruction.md:27 partly 10 1
```

## Open item for L1 (not drafted here — outside the four named blocks)

Two constraints the C2 counter puts on the entry author, recorded here so the prose above cannot
drift from what V7 will demand:

- V7 (`plans/round41_c2_verify.py:232-272`) parses the entry's `## Requirement map` with
  `MAP_ROW` (`:85`): every row must read exactly ``| `instruction.md:<L>` | `<tag>` | <label> |
  <cases> |`` with `<label>` one of `enforced`/`unenforced`/`partly`, `<L>` the tag's frozen line
  from the dry table, and `<cases>` citing at least one backticked case id that is one of that
  tag's violating cases. The eleven labels and their counts are the derived list above.
- V4 (`:179-221`) fails unless both `match=NO` ids (`later-valid-wed-1105`, `seconds-30`) appear
  in the entry in backticks.

`SKILL.md`'s tool-registry table (rows like `| `db-wal-probe` | probe | … |` at lines 587-594)
has no row for `plans/constraints_probe.py`, so a reader of the registry cannot find the probe the
section above tells them to run. The row would follow the `db-wal-probe` shape (command with
`--dry`/`--stage-check`/`--work`, exit 0/1/2 as in the opening paragraph, `itself;` the freeze
control `.ufo/waves/round-41/claims/control-c2-nothing.txt;` red at freeze). Not written because
this seat's four blocks are the ones the assignment names; flagged so it is routed rather than lost.
