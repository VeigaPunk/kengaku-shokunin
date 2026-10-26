source: S122 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/tests/test_outputs.py — the three pytest functions that are this task's whole score, lines 1-209, commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-26
source: S123 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/constraints-scheduling/instruction.md — the request the grader is mapped against, lines 1-30, same commit, accessed 2026-10-26
verified-at: 2026-10-26
recheck: 180d — from the lane root run `(cd corpus/evidence/round41/tb2-constraints-scheduling && sha256sum -c SHA256SUMS)` (green as written), re-fetch the two pinned URLs, and re-run `plans/constraints_probe.py --lane .`; any digest or receipt change supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed: `constraints-scheduling`

## Summary

At terminal-bench-2 commit `2fd12b88`, the `constraints-scheduling` task is scored by **three** pytest functions in
`tests/test_outputs.py`, all three required for the reward bit (`test.sh:18-22`, `:25-29`), and the verdict is not a
comparison against a reference answer: it is **computed by a scheduling model embedded in the grader** — nine clauses
in `_hard_ok` (five that can decide: Alice's 09:00 start and 14:00 end, Bob's 10:00 start, Carol's 12:00-12:30 lunch,
a same-date/weekday test; and four that cannot: a duplicate of the start bound, a Tue/Thu 16:30 rule, Carol's 17:00
end and an 18:00 end, all dominated by the 14:00 cap), an interval `_overlap` against each of three input calendars,
and a **minute-by-minute scan from Monday 09:00** that fails the run if any *earlier* slot also satisfies both
(`:158-167`). The graded artefact is a one-event ICS file that the grader reads with regexes
(`BEGIN:VEVENT(.*?)END:VEVENT`, `DTSTART:(\d{8}T\d{6}Z)`), not an ICS parser, and the three input calendars are pinned
twice — by sha256 literals in the grader (`:29`, `:32`, `:35`) and by the lane's captures, whose digests those literals
equal.

On this task's data the model admits exactly **two** 1-hour slots, Wed 17 Jan 11:00 and Thu 18 Jan 11:00, so the
earliest valid answer is **Wed 11:00** — the value the probe's saved ground-truth paragraph derives by hand from the
three captured calendars, and the value the task's own `solve.sh` must produce, since its case passes 3 of 3 and a
Thursday slot would fail the earliest test. Offline execution of the captured grader over 25 frozen end states
reproduced the reward bit on 23 and was wrong on 2; the two are the round-40 planning seat's pilot errors, carried
verbatim:

`cases=25 observed_pass=6 observed_fail=19 mismatches=2`

Five results organise the rest of the entry. (1) The score depends on **VEVENT order**: an unrelated decoy VEVENT
placed first, at the right time, passes 3 of 3 while the requested meeting sits at Fri 15:00 (`decoy-first-vevent`,
`PPP`); its mirror, with the requested meeting first, fails 2 of 3 (`decoy-second-vevent`, `PFF`). That defect is
published (S124, TB2.1 PR #245) and this entry claims **no** novelty for it. (2) The earliest test cannot reject an
invalid submitted slot: the slot itself is never passed through the hard model there, only the slots before it
(`bob-start-0900-wed` and `wed-1059-overlaps-alice`, both `PFP`). (3) The input-integrity check compares **decoded
text**, so all three pinned calendars can be rewritten with CRLF line ends and the run still passes 3 of 3
(`input-crlf-rewrite`, `PPP`) although `instruction.md:17-18` says any modification fails. (4) RFC 5545-valid forms
fail the structure test — a folded `ATTENDEE` (`folded-attendee-line`, `FPP`), lowercase property names
(`lowercase-property-names`, `FPP`), an explicit `VALUE=DATE-TIME` parameter (`dtstart-value-datetime`, `FFF`) — while
the task's own CRLF line breaks pass (`crlf-line-endings`, `PPP`). (5) `DTEND` is read by **one** test, so a 90-minute
event fails only the structure test and is graded as 60 minutes by the other two (`duration-90min`, `FPP`).

This entry extends `knowledge/benchmark-grader-semantics.md` and
`knowledge/benchmark-verifier-execution-model.md` (S122 is the same repository at the same commit) and the six earlier
TB2 grader entries (`tb2-protein-assembly-grader.md`, `tb2-regex-log-grader.md`, `tb2-git-webserver-grader.md`,
`tb2-build-pmars-grader.md`, `tb2-git-leak-recovery-grader.md`, `tb2-db-wal-recovery-grader.md`). It records one edge
class new to the lane's **executed** grader sample: the pass/fail bit is produced by a **constraint-satisfaction model
the grader carries itself**, evaluated over sha256-pinned inputs, with the agent's artefact read by regular expressions
rather than a format parser — so a correct answer is one of a small set of times and the grader both **decides the
answer** and **checks the submission**. It is not a new verdict channel (per-line regexes, interval arithmetic and a
scan are old) and not a new reading. It **narrows** the `corpus/README.md` §Frontier "Terminal-Bench 2.0's" clause for
this one task only; the clause stays open for the remaining TB2 task graders (7 of 89 read at `2fd12b88`).

## Source labels

S122 and S123 are the benchmark maintainers' own task files: primary for *what this grader checks* and for the
requirement text the map is drawn against, and a self-report for everything else. `task.toml` (captured, not a
registry row) is the authors' own metadata, read only for the declared image (`:30`), the verifier and agent timeouts
(`:23`, `:26`), difficulty (`:15`) and the internet policy (`:35`). The three input calendars (`alice_calendar.ics`,
`bob_calendar.ics`, `carol_calendar.ics`) are captures of the maintainers' task inputs; the grader's own
`_EXPECTED_SHA256` literals (`:29`, `:32`, `:35`) equal their capture digests, which is the measured proof that the
lane captured the pristine inputs rather than an agent-modified copy. `test.sh` and `Dockerfile` are captures of the
maintainers' harness and environment, read for the reward mapping and the initial state, not run. The captured
`solve.sh` oracle is **own reading, tier C** — not a registry row; the probe executes it once, as the
`oracle-solve-sh` case's recipe inside the sandbox, and no finding rests on its correctness. The probe receipt
(`corpus/evidence/round41/constraints-probe.txt`) is the lane's own re-runnable gate output (tier A for its own scope:
these 25 states against these captures under host python3 and the captured grader).

Disclosure: the case predictions were written from a static reading of `tests/test_outputs.py` and `instruction.md`
**before the first recorded run**, and the frozen case table (`corpus/evidence/round41/constraints-dry-cases-freeze.txt`,
digest in `plans/pkg-spec-r41.json`) carries them. The first 16 of the 25 cases are the round-40 planning seat's pilot,
already graded on this host (`.ufo/waves/round-40/build/R40PlanNext/cs/run1.txt`, `cases=16 observed_pass=3
observed_fail=13 mismatches=2`); their predictions are carried verbatim, including the two the pilot observed wrong,
`later-valid-wed-1105` and `seconds-30`, so the first recorded run re-observes those 16. The 9 new cases were never
graded before the freeze.

## What is graded (static reading)

| Step | Mechanism | Lines |
|---|---|---|
| Entry point | `uvx -p 3.13` + `pytest==8.4.1` + `pytest-json-ctrf==0.3.5` over `/tests/test_outputs.py`; all three functions are collected | `test.sh:18-22` |
| Reward | the shell maps the pytest exit status to `/logs/verifier/reward.txt`: `1` on 0, `0` otherwise — one bit, no partial credit | `test.sh:25-29` |
| Initial state | `COPY inputs/ /app/` seeds the three calendars; nothing else is pre-placed, and no `meeting_scheduled.ics` exists | `Dockerfile:14` |
| Input integrity | per file: text equality with `../inputs/<name>` when the repo has it, else `sha256(read_text().encode())` against three literals — both branches compare **decoded** text | `test_outputs.py:88-96` |
| Structure | after `strip()`: starts `BEGIN:VCALENDAR`, ends `END:VCALENDAR`, contains `VERSION:2.0`, any `PRODID:`, at least one VEVENT; the meeting block is the first VEVENT containing `SUMMARY:Team Planning Meeting` **and** all three emails; one `re.I` line-match per attendee; `DTSTART`/`DTEND` from **that block**; exactly 1 hour; 2024-01-15..19; weekday | `test_outputs.py:97-129` |
| Constraints | `DTSTART` from the **whole file**; `e = s + 1h`; `_hard_ok(s, e)`; no overlap with any of the three calendars | `test_outputs.py:132-143` |
| Earliest | a minute-by-minute scan from Mon 2024-01-15 09:00 to the submitted start; any earlier slot passing `_hard_ok` **and** the conflict test raises `Found earlier valid slot`; then the same-minute Monday tie-breaker and an unconditional `9 <= hour < 12` | `test_outputs.py:146-188` |
| Carol buffer | runs only when the meeting ends after 16:45; 15-minute windows before and after, against Carol's late-ending events | `test_outputs.py:190-209` |

Five structural consequences follow from the reading alone:

- **Only the first test binds the requested meeting.** Tests 2 and 3 call `_dt` on the whole file (`:135`, `:151`), so
  the interval they judge is the file's first `DTSTART`; test 1 is the only function that selects a VEVENT by summary
  and attendees (`:108-115`), and it takes the **first** match (`next(...)`) rather than failing closed on duplicates.
- **`DTEND` is graded once.** Test 1 asserts `e - s == 1h` (`:127`); tests 2 and 3 discard `DTEND` and recompute
  `e = s + 1h` (`:136`, `:191`), so the 90-minute state is graded as a 1-hour meeting outside the structure test.
- **The earliest test cannot ask whether the submission is valid.** It scans strictly below `sched`; the submitted
  slot is never passed to `_hard_ok`, so a start of 09:00 — invalid under Bob's bound — satisfies it whenever nothing
  earlier is valid.
- **Integrity is a text comparison.** `read_text()` decodes with universal newlines, and the fallback digest is taken
  over the decoded text re-encoded (`app_text.encode()`), so a CRLF rewrite of a calendar is the same input as the LF
  original to both branches.
- **Timestamps are matched by one unparameterised regex.** `DTSTART:(\d{8}T\d{6}Z)` (`:48`, `:125-126`, `:135`, `:151`)
  requires the bare property name with no parameters, the uppercase form, and a literal `Z`; there is no unfolding
  step, so a folded content line is simply text the patterns do not see.

## Located quotes

Quotes are byte-exact from the round-41 captures (`corpus/evidence/round41/tb2-constraints-scheduling/`, identical to
the pinned raw files at `2fd12b88`), each 3-25 words, verified line by line and by the gate's `P4` clause. Straight
double quotes inside a quote are the file's bytes.

| Claim supported | “Quote” | `capture:line` |
|---|---|---|
| the integrity check compares decoded text, not bytes | “assert app_text == repo_path.read_text(), f"Input modified: {fname}"” | `test_outputs.py:93` |
| the fallback digest is taken over the decoded text | “digest = hashlib.sha256(app_text.encode()).hexdigest()” | `test_outputs.py:95` |
| the VEVENT split is the only structure the reader knows | “vevents = re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", c, flags=re.S)” | `test_outputs.py:106` |
| the meeting is selected by summary plus all three emails | “if "SUMMARY:Team Planning Meeting" in b and all(e in b for e in EMAILS)” | `test_outputs.py:112` |
| attendees are one-line, case-insensitive, parameters optional | “rf"^ATTENDEE[:;].*{re.escape(email)}$", meeting, re.I | re.M” | `test_outputs.py:122` |
| duration is asserted once, on the selected block | “assert e - s == timedelta(hours=1)” | `test_outputs.py:127` |
| the second test parses the file, not the meeting block | “s = _dt(r"DTSTART:(\d{8}T\d{6}Z)", c)” | `test_outputs.py:135` |
| the second test recomputes the end from the start | “e = s + timedelta(hours=1)” | `test_outputs.py:136` |
| the hard model is one call over the interval | “assert _hard_ok(s, e)” | `test_outputs.py:137` |
| conflicts are tested against all three calendars | “assert not any(_overlap(s, e, cal) for cal in (A, B, C))” | `test_outputs.py:143` |
| the earliest scan starts at Monday 09:00 | “t = datetime(2024, 1, 15, 9, 0)” | `test_outputs.py:158` |
| an earlier valid slot is a hard failure, not a comparison | “f"Found earlier valid slot at {t:%Y-%m-%d %H:%M} UTC"” | `test_outputs.py:165` |
| the morning preference is an unconditional window assertion | “assert 9 <= sched.hour < 12, "Prefer Alice's morning (9-12) when possible"” | `test_outputs.py:188` |
| the defined-but-unused repo-input helper | “def _repo_input(name: str) -> str:” | `test_outputs.py:22` |
| the conflict helper takes naive datetimes and a calendar string | “def _overlap(a0: datetime, a1: datetime, cal: str) -> bool:  # any conflict” | `test_outputs.py:46` |
| Bob's start bound is the clause that rejects 09:00 | “if t0.hour < 10:  # Bob start” | `test_outputs.py:63` |
| the lunch window is a bare interval test | “if t0 < lunch1 and t1 > lunch0:” | `test_outputs.py:74` |
| the Carol-buffer block is gated on an end after 16:45 | “if end.hour > 16 or (end.hour == 16 and end.minute >= 45):” | `test_outputs.py:192` |
| the buffer is fifteen minutes, inside that block only | “b1 = ee + timedelta(minutes=15)” | `test_outputs.py:206` |
| the runner is pytest over the one test file under uvx | “pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA” | `test.sh:22` |
| the reward is one bit from the pytest exit status | “echo 1 > /logs/verifier/reward.txt” | `test.sh:26` |
| the inputs arrive by copy into /app | “COPY inputs/ /app/” | `Dockerfile:14` |
| the graded path and object are named in the request | “Output: Create `/app/meeting_scheduled.ics` with a 1-hour "Team Planning Meeting"” | `instruction.md:10` |
| the request declares the inputs read-only | “- Treat the provided calendar files as read-only. Do not modify” | `instruction.md:15` |
| the request says any modification fails | “repo inputs. Any modification will cause the tests to fail.” | `instruction.md:18` |
| the request fixes the UTC timestamp form | “- All times must be in UTC format (YYYYMMDDTHHMMSSZ)” | `instruction.md:25` |
| the request fixes minute granularity | “- Earliest valid slot is evaluated at minute granularity” | `instruction.md:28` |
| the oracle scans a 30-minute grid | “current_time += timedelta(minutes=30)” | `solve.sh:112` |
| the oracle ranks by preference score, then by time | “valid_slots.sort(key=lambda x: (-x[1], x[0]))” | `solve.sh:118` |

## Requirement map

Labels are **derived**, not chosen: `enforced` iff every receipt case whose `violates=` set carries the tag is
observed `fail`, `unenforced` iff every such case is observed `pass`, `partly` otherwise — the rule the round-41
counter `V7` applies, computed over **all** violating cases and not from one convenient witness. The frozen table
carries eleven tags on seven instruction lines; every tag has at least one violating case. Three tags are wide:
`earliest` (10 cases), `hard-constraints` (5), `no-conflict` (5); seven have exactly one violating case (`window`,
`output-file`, `meeting-title`, `attendees`, `one-hour`, `version-prodid`, `utc-format`), and `inputs-readonly` has
three.

| Instruction line | Tag | Label | Receipt cases cited (violating, both directions) |
|---|---|---|---|
| `instruction.md:1` | `window` | enforced | `weekend-sat-20` |
| `instruction.md:10` | `output-file` | enforced | `nop` |
| `instruction.md:10` | `meeting-title` | enforced | `title-wrong` |
| `instruction.md:10` | `attendees` | enforced | `missing-carol` |
| `instruction.md:10` | `one-hour` | enforced | `duration-90min` |
| `instruction.md:12` | `hard-constraints` | partly | `bob-start-0900-wed`, `decoy-first-vevent`, `seconds-30`, `weekend-sat-20`, `decoy-second-vevent` |
| `instruction.md:12` | `no-conflict` | enforced | `later-valid-wed-1105`, `conflict-mon-1230`, `seconds-30`, `input-event-deleted-wed-1000`, `wed-1059-overlaps-alice` |
| `instruction.md:15` | `inputs-readonly` | partly | `input-appended`, `input-event-deleted-wed-1000`, `input-crlf-rewrite` |
| `instruction.md:23` | `version-prodid` | enforced | `no-prodid-header` |
| `instruction.md:25` | `utc-format` | enforced | `tzid-form` |
| `instruction.md:27` | `earliest` | partly | `later-valid-wed-1105`, `later-valid-thu-1100`, `conflict-mon-1230`, `bob-start-0900-wed`, `decoy-first-vevent`, `seconds-30`, `weekend-sat-20`, `input-event-deleted-wed-1000`, `wed-1059-overlaps-alice`, `decoy-second-vevent` |

Eight tags are enforced and three are not (`hard-constraints`, `inputs-readonly`, `earliest`). The per-line reading:

- **12 (`hard-constraints`, `partly`).** Five violating cases, four observed `fail` and one observed `pass`: the decoy
  case submits a meeting at Fri 15:00 (`_hard_ok` returns False on the 14:00 bound) and passes because tests 2-3 read
  the decoy's 11:00 `DTSTART` instead. The label is `partly` because the frozen rule counts a passing violator, and
  the passing violator is the order defect (finding 3), not a hole in the model.
- **15 (`inputs-readonly`, `partly`).** `input-appended` (one byte of trailing whitespace) and
  `input-event-deleted-wed-1000` (an event removed) both fail; `input-crlf-rewrite` (all three calendars rewritten)
  passes. The instruction says any modification fails (`:18`); the check is decoded-text equality, so a line-ending
  rewrite is invisible to it.
- **27 (`earliest`, `partly`).** Ten violating cases, nine `fail` and one `pass` (`decoy-first-vevent`, again the order
  defect). The tag is wide because "earliest" is the property every late-but-valid slot violates
  (`later-valid-thu-1100`) and the property that `bob-start-0900-wed` and `wed-1059-overlaps-alice` do **not** violate
  despite being invalid: their `PFP` letters say the earliest test passed.
- **12 (`no-conflict`, `enforced`).** Five violating cases, all `fail`, for two different reasons:
  `conflict-mon-1230` and `wed-1059-overlaps-alice` overlap an input event; `seconds-30` and `later-valid-wed-1105`
  cross Carol's lunch window, which the grader models in the same interval test. The tag reads "conflict or
  unavailable", not "an input event was hit".
- **1, 10, 23, 25 (single-witness, `enforced`).** `window` (`weekend-sat-20`), `output-file` (`nop`),
  `meeting-title` (`title-wrong`), `attendees` (`missing-carol`), `one-hour` (`duration-90min`), `version-prodid`
  (`no-prodid-header`) and `utc-format` (`tzid-form`) each rest on one case. For `one-hour` that is the whole
  enforcement surface (finding 7); for `utc-format` the single witness is a `TZID` local-time form, and the tag does
  *not* cover RFC-valid parameter forms — `dtstart-value-datetime` carries no tag although it is a valid UTC timestamp
  written with `VALUE=DATE-TIME`.

Two instruction requirements have **no** frozen tag and therefore no row: Carol's 15-minute buffer after a meeting
ending at 16:45 or later (`:6`) and the preference sentences used as tie-breakers (`:29-30`). The buffer is
implemented (`:190-209`) but unreachable on the pinned data (finding 9). The preferences are graded asymmetrically:
the Monday avoidance is a conditional tie-breaker (`:180-185`) and the Alice-morning sentence is an **unconditional**
assertion — `assert 9 <= sched.hour < 12` (`:188`) — so a valid afternoon slot would fail a requirement the request
calls a preference; Bob's afternoon sentence (`:30`) is read by no test, as the request instructs. On this dataset the
only valid starts are 11:00, so no receipt case separates the two readings: the tag set has nothing to hang this on,
and it is left as a reading with a code cite rather than a case.

### Contestable tags

The `violates=` tags are frozen with the predictions and are not edited; three are worth naming:

- **`hard-constraints` → `decoy-first-vevent`.** The case's *requested* meeting does violate the model; the case's
  *graded interval* does not. The tag is on the end state the agent would have produced, which is the rule the probe
  docstring states; the passing verdict is the order defect's, not the model's.
- **`no-conflict` → `seconds-30`.** A slot ending at 12:00:30 is inside Carol's lunch by 30 seconds, so the tag is
  honest; but the case was frozen to test minute granularity (`:28`) and it fails as a lunch-boundary case instead, so
  no case demonstrates a sub-minute rule.
- **`inputs-readonly` → `input-crlf-rewrite`.** The agent "modified" all three inputs in the only sense the grader can
  see; the tag stays because the instruction sentence stays. The label `partly` is the correct description, and it is
  the entry's clearest divergence between a stated requirement and the assertion behind it.

## Findings, each tied to its receipt cases

1. **A do-nothing agent scores 0 of 3 (`nop`, `FFF`).** All three functions open `/app/meeting_scheduled.ics`
   (`:97`, `:134`, `:150`), and the receipt records `FileNotFoundError` per test. Unlike the round-39
   repository-history grader (whose untouched state passes 4 of 5) this grader's initial state fails everything.
2. **There is one answer up to the day, and it is Wed 11:00 (`literal-correct-slot` `PPP`, `oracle-solve-sh` `PPP`,
   `later-valid-thu-1100` `PPF`).** With start ≥ 10:00, end ≤ 14:00 and no 12:00-12:30 overlap, every Monday, Tuesday
   and Friday candidate is blocked by an input event — Mon: Alice 10-11 and 13-14, Bob 11-12 and 13-15, Carol 11-12;
   Tue: Alice 10-12, Carol 11-12, Bob and Carol 13-14; Fri: Alice 10-11 and 13-14, Carol 11-12, Bob 12-13 — and
   Wednesday and Thursday admit exactly 11:00-12:00 (Alice's 10-11 blocks 10:00 and 10:30 there, Carol's and Bob's
   12-13 block 12:30, Alice's 13-14 on Wed and Bob's 13-14 on Thu block 13:00). The probe's ground-truth paragraph
   states this reading of the three captures; the probe itself did not derive it from the grader.
   `later-valid-thu-1100` is that same slot one day late and fails only the earliest test.
3. **The score depends on VEVENT order, not on the requested meeting (`decoy-first-vevent` `PPP`;
   `decoy-second-vevent` `PFF`).** With an unrelated decoy VEVENT placed first at Wed 11:00 and the attendee meeting at
   Fri 15:00, the run passes 3 of 3: test 1 selects the attendee block (`:112`) and judges only its structure, while
   tests 2-3 parse the file's first `DTSTART` (`:135`, `:151`) — the decoy's 11:00 — and find it valid, conflict-free
   and earliest. The mirror case puts the attendee meeting (Fri 15:00) first: test 1 still passes, and tests 2-3 now
   see 15:00, which fails the 14:00 bound and is later than the valid 11:00 slot. So the same two VEVENTs score `PPP`
   or `PFF` depending on their order. This defect is **published**: S124 (below) describes it, with a minimal
   reproduction of the same shape. **No novelty is claimed for it**, and the round's plan prices it as prior art
   rather than a finding.
4. **The earliest test cannot reject an invalid submission (`bob-start-0900-wed` `PFP`; `wed-1059-overlaps-alice`
   `PFP`).** The scan raises only for a slot *strictly earlier* than the submission that passes `_hard_ok` and the
   conflict test (`:159-166`). A submitted 09:00 fails Bob's 10:00 bound (`:63`) and therefore passes the earliest
   test, because 09:00 is itself not a valid earlier slot; a submitted 10:59 overlaps Alice's 10:00-11:00 event and
   fails the conflict test, yet every slot before it overlaps the same event, so nothing qualifies as an earlier valid
   slot and the earliest test passes too. Both cases fail the constraint test only. The `PFP` letters are the
   measurement: the earliest test is a property of the neighbourhood, not of the answer.
5. **Input integrity is textual, so a full CRLF rewrite of the inputs passes (`input-crlf-rewrite` `PPP`), while an
   appended newline and a deleted event fail (`input-appended` `FPP`; `input-event-deleted-wed-1000` `FPP`).**
   `Path.read_text()` normalises line endings, and the fallback branch hashes `app_text.encode()` — the decoded text
   re-encoded (`:90-96`). The image invokes the grader as `/tests/test_outputs.py` (`test.sh:22`), so
   `Path(__file__).resolve().parent.parent / "inputs"` is `/inputs`, which does not exist; the probe binds it at
   `/cap/test_outputs.py`, whose parent.parent is also `/`. The **sha256 branch** is therefore the one that runs, on
   the decoded text. `instruction.md:17-18` promises the opposite. This is the sharpest requirement/assertion
   divergence in the receipt, and it is not covered by S124.
6. **RFC 5545-valid syntax fails, and the task's own line breaks pass (`folded-attendee-line` `FPP`;
   `lowercase-property-names` `FPP`; `dtstart-value-datetime` `FFF`; `crlf-line-endings` `PPP`).** The request asks for
   "valid ICS format" (`:21`), and RFC 5545 §3.1 says “When parsing a content line, folded lines MUST first be
   unfolded” and that property names are case-insensitive; §3.8.2.4 lists “value data type” among the parameters
   allowed on `DTSTART`. The grader has no unfolding step, requires the exact-case `SUMMARY:`/`ATTENDEE:` names, and
   matches `DTSTART:` literally, so those forms give `F` (structure) or `FFF` (no timestamp found at all). CRLF, by
   contrast, is invisible because `read_text()` normalises it — the grader is simultaneously stricter than RFC 5545 on
   three syntax points and indifferent to the one the instruction treats as fatal (finding 5).
7. **Duration is graded by one test only (`duration-90min`, `FPP`).** Test 1 asserts `e - s == 1h` on the selected
   block (`:127`); tests 2-3 rebuild the interval as `s + 1h` (`:136`, `:191`) and never compare it with `DTEND`, so a
   90-minute VEVENT is a 1-hour meeting to two thirds of the score.
8. **`_hard_ok` carries nine clauses, five of which can decide anything (`bob-start-0900-wed` `PFP`;
   `later-valid-wed-1105` `PFF`; `seconds-30` `PFF`; `weekend-sat-20` `FFF`; `conflict-mon-1230` `PFF`).** The live
   clauses are Alice's start (`:59`), Alice's end (`:61`), Bob's start (`:63`), the lunch interval (`:74`) and the
   same-date/weekday test (`:77`). `:79` is a byte-duplicate of `:59`; `:65-68` (Tue/Thu 16:30), `:69-70` (Carol 17:00)
   and `:81-82` (18:00) can never fire, because `:61` already returns `False` for any end after 14:00. The probes'
   consequences: 09:00 is rejected by `:63`, a 12:30 start is accepted by the model and rejected by the overlap test
   alone (`conflict-mon-1230`), and both sub-hour cases fail on the lunch interval rather than on a boundary rule.
   `:59`'s `t0.minute >= 0` is always true, so the "no meetings before 9 AM" sentence is enforced as `hour >= 9`.
9. **The Carol 15-minute buffer is vacuous on the pinned inputs.** The block runs only when the meeting ends after
   16:45 (`:192`), a time `_hard_ok` forbids in test 2 (`:61`), and Carol's latest input `DTEND` is 14:00
   (`carol_calendar.ics:28`), so the inner assertion (`:207`) is never evaluated for any receipt case. No frozen tag
   names the buffer and no case exercises it, so it is a graded rule that cannot change a verdict here.
10. **The attendee test is a superset check and its case sensitivity is asymmetric (`extra-attendee-dave` `PPP`;
    `title-wrong` `FPP`; `lowercase-property-names` `FPP`).** `all(e in b for e in EMAILS)` (`:112`) admits a fourth
    attendee, and the per-email line match is case-insensitive (`re.I`, `:122`) while the summary match at `:112` is
    exact-case: the same file can fail on lowercase `summary:` and would still pass a lowercase `attendee:`.
11. **The oracle is a preference-ranked 30-minute grid, and its "earliest" result is incidental
    (`oracle-solve-sh` `PPP`).** `solve.sh` walks `current_time` in 30-minute steps (`solve.sh:112`), scores candidates
    by an Alice-morning / Bob-afternoon / not-Monday sum and sorts by `(-score, time)` (`:118`) before taking the first.
    On this dataset the two valid slots tie on score, so time breaks the tie and it lands on Wed 11:00 — the same
    answer as the earliest-first rule, for a different reason. A valid 11:05 slot would be invisible to the oracle's
    grid while the grader, at minute granularity (`instruction.md:28`), would grade it. The case shows the oracle
    passes; it does not show the oracle solves the stated problem.

## Regrade (second grading of the same end state)

The harness imports the grader once with `exec_module` and calls the three functions twice in the same process on the
same built state (`plans/constraints_probe.py` `HARNESS_PY`, `for tag in ("TEST", "REGRADE")`); the second pass is
reported, never used for the verdict: `regrade cases=25 differ=0`. Because every function only re-reads
`/app/meeting_scheduled.ics` and the three calendars (`:97`, `:134`, `:150`) and reads no clock, environment or network,
a second read of unchanged files cannot differ: the column is a determinism read of this probe, nearly tautological for
this grader, and **not** re-run stability. It could only catch a writer left running inside the sandbox, and this
grader writes nothing. The two `match=NO` cases (`later-valid-wed-1105`, `seconds-30`) are **prediction** errors across
runs — the frozen `predicted_tests=PPF` against `tests=PFF` — not regrade differences; both re-graded `same`.

## What the probe does not show

- **The task image is never pulled; the host's tools stand in.** `Dockerfile:3` says `FROM ubuntu:24.04` and `:7-11`
  installs `python3` and `python3-pip` from apt; `test.sh:8` installs uv 0.9.5 from the network and runs pytest under
  `uvx -p 3.13`. The probe uses host `/usr/bin/python3` and imports the captured module directly, so the image's
  python build, the pinned `pytest==8.4.1` and `pytest-json-ctrf==0.3.5`, and the ctrf report are untested. The task
  declares `docker_image = "alexgshaw/constraints-scheduling:20251031"` (`task.toml:30`) and `allow_internet = true`
  (`:35`); neither was exercised.
- **`tests/test.sh` was not executed.** The reward mapping is read (`test.sh:18-29`), not run: `apt-get`, the network uv
  install and `/logs/verifier/` are outside the sandbox; the probe calls the three test functions itself.
  `observed_pass` means "pytest would exit 0", not "reward.txt was written".
- **The probe always took the sha256 integrity branch.** The grader is bound at `/cap/test_outputs.py`, so
  `Path(__file__).resolve().parent.parent / "inputs"` is `/inputs` and the repo-inputs branch (`:92-93`) never ran.
  Finding 5 holds for both branches by reading (each compares decoded text), but only the digest branch is measured.
- **The 25 cases are the claim's whole surface.** They were fixed before the first recorded run. States outside them —
  a `DURATION` property instead of `DTEND`, a `VTIMEZONE`/`TZID` UTC calendar, a meeting VEVENT spanning two days,
  duplicate meeting VEVENTs (the fail-closed policy S124 proposes is not tested here), a second decoy at the same
  minute, an ICS with `PRODID` but no `VERSION`, extra `VALARM` blocks, a symlinked `meeting_scheduled.ics`, and every
  AI-agent trajectory — are not covered and are not claimed.
- **The 16 pilot cases are copies, and two of their predictions were wrong.** `later-valid-wed-1105` and `seconds-30`
  are carried verbatim with the pilot's error; both are named where the map cites them and neither was corrected.
- **Not a statement about the task's validity, difficulty or solvability.** That is PROVINCE's question, not this
  lane's; `difficulty = "medium"` (`task.toml:15`) and the 15/30-minute estimates (`:19-20`) are the authors' metadata,
  read only.
- **The oracle row is one execution, not a correctness claim.** `oracle-solve-sh` runs the captured `solve.sh` as a
  case recipe and passes 3 of 3; it says nothing about other inputs, about `tests/test.sh`, or about the image.

## Prior art

- **The order defect is published, by the benchmark's own repository.** S124: Terminal-Bench 2.1 pull request #245,
  "Bind constraints-scheduling checks to the requested event" (author `camirian`, opened 2026-10-05, **closed**
  2026-10-08T19:02:36Z, `merged=false`, one commit `ca2256bb`, 4 files changed, +253/−39; read live 2026-10-26). Its
  body states the same mechanism as finding 3: “the constraint and earliest-slot tests parse the first DTSTART in the
  entire output calendar”, and “This lets the unrelated event provide the time evidence for a different target event.”
  Its minimal reproduction uses the supplied calendars and two VEVENTs, and it reports that with the context event
  first "the current verifier passes all three checks" — the `decoy-first-vevent` result. It changes `tests/` only, is
  closed unmerged, and the defect is therefore live; this entry claims **no novelty** for it, and the round-41 plan
  prices it as prior art rather than a claim.
- **The same PR is prior art for three of the syntax findings.** It proposes a parser that “accepts CRLF, folded
  lines, case-insensitive property names, attendee parameters, and explicit UTC value parameters”. Three of those
  classes are finding 6's failures (folding, case sensitivity, the `VALUE` parameter); the fourth, CRLF, the current
  grader accepts for an unrelated reason. It also makes multiple matching target events “fail closed”, which is the
  policy the current `next(...)` (`:108-115`) does not have. So finding 6 is a probed instance of a syntax gap the
  benchmark's own repository had already written down; the receipt supplies the cases, not the idea. What the PR does
  **not** contain is the integrity finding (5), the earliest-test blind spot (4), the duration split (7) or the dead
  `_hard_ok` clauses (8); a text search for those in the PR body returned nothing.
- **TB2.1 `main` carries the same bytes.** Fetched live on 2026-10-26,
  `terminal-bench-2-1/main/tasks/constraints-scheduling/tests/test_outputs.py` and `instruction.md` hash to
  `1422b345…` and `342def78…` — the same digests as this entry's pins — so the grader read here is the grader both
  repositories ship, and the closed PR changed nothing upstream.
- **The RFC forms, from the RFC.** `https://www.rfc-editor.org/rfc/rfc5545.txt` §3.1: “When parsing a content line,
  folded lines MUST first be unfolded”; §3.1: “Property names, parameter names, and enumerated parameter values are
  case-insensitive.”; §3.8.2.4 lists “value data type” among the parameters allowed on `DTSTART`. No SOURCES row is
  taken for these: they are the format standard the instruction's "valid ICS format" points at, read once, not a
  benchmark artefact.
- **The decoy's prevalence is not measured, by anyone opened here.** The PR body says of itself: “This report concerns
  one task's verifier behavior. It does not measure prevalence across Terminal-Bench” (S124). The PR also records that
  a GitHub tracker search on 2026-10-04 “returned no matching bug report”. This lane ran no tracker search of its own
  and claims nothing about how often agents produce multi-VEVENT output.

The claim this entry makes stays the narrow one: **a probed instance of the TB2 `constraints-scheduling` grader** — 25
frozen states executed offline against these captures, a requirement map derived from them, and the answer the model
admits read out of three pinned calendars. It is not a first-instance claim for scheduling, ICS or constraint
grading, not a novelty claim, and not a claim about how agents solve the task.

source-note: S124 https://github.com/harbor-framework/terminal-bench-2-1/pull/245 (tier B, cited by §Prior art only).

## Negative space

This entry does **not** establish: that the task is invalid, mis-calibrated or too easy (no image run, no agent, no
trajectory); that the grader should bind every check to the requested VEVENT (S124's proposal, described, not judged);
that any agent can or would produce a passing decoy output in a real run — nothing here is a gameability,
solver-strategy or reward-hacking-in-the-wild claim; that Wed 11:00 is the answer the authors intended rather than the
answer their model admits; or anything about how Harbor executes this verifier
(`benchmark-verifier-execution-model.md` covers where it runs and what it restores).

Nor: **contamination** — `test_outputs.py:1-2` and `Dockerfile:1-2` carry the canary banner and these captures exist
for digest-pinned re-execution, not as a contamination measurement; **the image's python** — host `/usr/bin/python3` is
the probe's instrument; **the oracle's correctness** — `solve.sh` runs as one case's recipe and passes, which says
nothing about other inputs (finding 11 shows its grid is coarser than the grader's rule); **prevalence** — one task, 25
states, no tracker sweep; **deployment or packaging guidance** — the ICS shapes in the cases are the probe's own
constructions, not a format this lane recommends.

**Falsifier.** This entry is falsified if (a) a re-fetch of the two pinned URLs yields bytes whose SHA-256 differs from
`corpus/evidence/round41/tb2-constraints-scheduling/SHA256SUMS`; (b) a fresh run of
`plans/constraints_probe.py --lane .` prints anything other than `cases=25 observed_pass=6 observed_fail=19
mismatches=2` and `regrade cases=25 differ=0` — in particular if `decoy-first-vevent`, `literal-correct-slot`,
`crlf-line-endings`, `extra-attendee-dave`, `input-crlf-rewrite` or `oracle-solve-sh` is observed `fail`, or if `nop`,
`later-valid-thu-1100`, `conflict-mon-1230`, `bob-start-0900-wed`, `duration-90min`, `missing-carol`, `title-wrong`,
`tzid-form`, `weekend-sat-20`, `input-appended`, `input-event-deleted-wed-1000`, `wed-1059-overlaps-alice`,
`folded-attendee-line`, `dtstart-value-datetime`, `no-prodid-header`, `decoy-second-vevent` or
`lowercase-property-names` is observed `pass`; (c) a line of `test_outputs.py` is shown to pass the submitted interval
through `_hard_ok` in the earliest test, to compare `DTEND` in tests 2 or 3, to unfold folded content lines, to compare
input bytes rather than decoded text, or to select a meeting VEVENT by anything other than the first match; or (d) the
captured grader applied to the `decoy-first-vevent` state fails any test, or applied to the `duration-90min` state
passes the structure test.
