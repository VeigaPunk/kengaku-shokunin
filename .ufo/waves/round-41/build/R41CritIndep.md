# R41CritIndep — independent re-derivation of the TB2 `constraints-scheduling` C2 probe

Seat: R41CritIndep (leaf executor, kengaku round 41 wave 1). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
was opened read-only: no lane file, index, jj state, corpus or plans entry was written. Scratch
`/fast/scratch/hyaku/kengaku-r41/R41CritIndep/` (clone `git -C "$S/lane" rev-parse --show-toplevel` →
`/fast/scratch/hyaku/kengaku-r41/R41CritIndep/lane`) is removed at the end; receipts are copied next to this
report. Tools installed: none (no install needed; `python3` 3.14.8, `bubblewrap` 0.13.1 already present).

Every run below went through the seat envelope, verbatim:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
      --proc /proc --unshare-pid --die-with-parent <command>
```

Frozen inputs this seat read and pinned digests it checked:

```
$ sha256sum plans/constraints_probe.py corpus/evidence/round41/constraints-dry-cases-freeze.txt \
            corpus/evidence/round41/constraints-probe.txt
8c471fbd0d83450793271d75fe3735a735226a725a73e0f16e02034e9d3c7242  .../plans/constraints_probe.py
a656ce9b9adb4e88bb49b6a8a45064a8c4f459cffbbf76d70cca7f43a0c77a03  .../constraints-dry-cases-freeze.txt
c5aa674277f9b9473de4c0884629c577f2b6467d8b73c3a90eec33b24b7701da  .../constraints-probe.txt
```
`plans/constraints_probe.py` and the dry table match `claims/frozen-digests.txt:4` and `:6`; the probe digest is
also what the lane file `plans/constraints_probe.py` hashes to, so the scratch copy I patched was the frozen one.

## 1. The slot model, derived with my own parser (no grader import)

`indep_slots.py` (this dir): RFC 5545 line unfolding, property names split on `;` before `:`, UTC values parsed
with `fullmatch` on `\d{8}T\d{6}Z`, overlap as half-open intervals (`t0 < busy_end and t1 > busy_start`, so a
meeting touching an event at an endpoint does not conflict), constraints read off `instruction.md`:

| instruction.md | predicate I implemented |
|---|---|
| L1 "January 15-19, 2024 … 9 AM - 6 PM, Monday-Friday" | date in 2024-01-15..19, `weekday()<5`, 09:00 <= start, end <= 18:00 |
| L5 Alice "Absolutely no meetings after 2 PM or before 9 AM" | start >= 09:00, end <= 14:00 |
| L6 Bob "No meetings before 10 AM"; "leave by 4:30 PM on Tue/Thu" | start >= 10:00; Tue/Thu end <= 16:30 |
| L7 Carol "9 AM-5 PM, lunch break 12:00-12:30 (unavailable)" | end <= 17:00; not (start < 12:30 and end > 12:00) |
| L10 "1-hour" | enumerated at 1-minute granularity, exactly 60 min |
| L12 "must not conflict with existing calendar entries" | no overlap with any VEVENT of the three captures |

Command and output (full copy in `slots-out.txt`):

```
$ python3 indep_slots.py corpus/evidence/round41/tb2-constraints-scheduling
parsed events: {'alice_calendar.ics': 8, 'bob_calendar.ics': 6, 'carol_calendar.ics': 6}
  a Mon 01-15 10:00-11:00 Monday Morning Meeting
  ... (20 events printed) ...
valid_1h_slots=2
SLOT 2024-01-17 11:00-12:00 UTC (Wednesday)
SLOT 2024-01-18 11:00-12:00 UTC (Thursday)
earliest=2024-01-17 11:00 UTC
same-minute candidates: ['Wed 11:00', 'Thu 11:00']
```

Why exactly two: Bob's 10:00 floor and Alice's 14:00 ceiling leave starts 10:00–13:00; Carol's 12:00–12:30 lunch
removes every start in (11:00, 12:30) because end = start+1h > 12:00; so the only bands are start 10:00–11:00 and
12:30–13:00. Alice is busy 10:00–11:00 every weekday (`alice_calendar.ics`, e.g. `DTSTART:20240117T100000Z`), so
the morning band collapses to exactly 11:00; at 11:00 Mon is Bob's `11:00-12:00`, Tue is Carol's `11:00-12:00`,
Fri is Carol's `11:00-12:00`, leaving Wed and Thu. In the 12:30–13:00 band every day is blocked by a 13:00 event
(Mon Alice+Bob, Tue Carol+Bob, Wed Alice, Thu Bob, Fri Alice) and Wed/Thu/Fri also by a 12:00–13:00 event.
This independently reproduces the probe docstring's ground truth ("Valid starts: Wed 2024-01-17 11:00 and Thu
2024-01-18 11:00 only; the earliest is Wed 11:00").

Reachability notes from this derivation, used in §2:
* the structure test's window (lines 128) only bounds day 15..19 and `weekday()<5`, so weekend variants fail it
  before duration is even compared (see `weekend-sat-20`);
* a 1-hour slot with end <= 14:00 always starts 9–13, so the Carol 4:45 PM buffer branches (test 3, lines 190-205)
  are dead on this dataset;
* the Monday tie-break needs a valid Monday candidate at the same minute; at 11:00 Monday is blocked by Bob, so
  it is dead too;
* `assert 9 <= sched.hour < 12` (test_outputs.py:188) makes any 12:30–13:00 slot fail test 3 even if it were free.

## 2. Hand predictions for the 25 frozen cases

Method: read `test_outputs.py` and record, per case, the first branch that decides each test. The grader's shape,
with line references: S = integrity (88-96) → headers (97-103) → `meeting = next(...)` picks the first VEVENT
block containing `SUMMARY:Team Planning Meeting` and all three emails (108-118) → `^ATTENDEE[:;].*email$`
(121-123) → `DTSTART:`/`DTEND:` regexes (125-126) → 1-hour and window (127-129). C = first `DTSTART:` in the
whole file (135), `e = s + timedelta(hours=1)` (136), `_hard_ok` (58-82), overlap vs the `/app` copies (137-143).
E = same first `DTSTART:` (151), minute scan from Mon 09:00 (158-167), same-minute tie set (170-186), morning
assert (188), Carol buffer branches (190-209).

| case | indep S/C/E | receipt `tests=` | agree | deciding branch |
|---|---|---|---|---|
| nop | FFF | FFF | yes | no file: all three read it (FileNotFoundError) |
| oracle-solve-sh | PPP | PPP | yes | solve.sh scores Wed and Thu 11:00 = 20, sorts by time → Wed 11:00 |
| literal-correct-slot | PPP | PPP | yes | Wed 11:00, 3 attendees, 1h, uppercase legacy form |
| later-valid-wed-1105 | **PFF** | PFF | yes | lunch branch 72-74 (`t1>12:00`) + Bob/Carol 12:00-13:00 overlap; E: 11:00 slot is earlier |
| later-valid-thu-1100 | P**PF** | PPF | yes | Thu 11:00 feasible; Wed 11:00 is earlier → only E |
| conflict-mon-1230 | PFF | PFF | yes | Alice Mon 13:00-14:00 overlap; E: morning assert fails (hour 12) |
| bob-start-0900-wed | PFP | PFP | yes | C: `t0.hour < 10` (63-64); E: no earlier feasible slot, 9 in [9,12) |
| decoy-first-vevent | PPP | PPP | yes | S picks the attendee block (Fri 15:00); C/E read the first DTSTART (Wed 11:00) |
| duration-90min | FPP | FPP | yes | S is the only DTEND reader (126-127); C/E use start+1h |
| missing-carol | FPP | FPP | yes | S needs all three emails in the meeting block (108-113) |
| title-wrong | FPP | FPP | yes | S needs literal `SUMMARY:Team Planning Meeting` |
| seconds-30 | **PFF** | PFF | yes | end 12:00:30 > 12:00 → lunch branch 74; E: earlier 11:00 slot (158-167) |
| tzid-form | FFF | FFF | yes | `DTSTART;TZID` has no `DTSTART:` substring → `_dt` assert in all three |
| weekend-sat-20 | FFF | FFF | yes | S window 128; C `weekday()>=5` 76; E earlier slot |
| input-appended | FPP | FPP | yes | S: sha256 branch 95-96 mismatches; C/E still see the pristine events |
| input-event-deleted-wed-1000 | FPP | FPP | yes | S digest mismatch; C/E book Wed 10:00 on the edited copy |
| wed-1059-overlaps-alice | PFP | PFP | yes | C: Alice Wed 10:00-11:00 overlap; E: no earlier feasible slot, 10 in [9,12) |
| crlf-line-endings | PPP | PPP | yes | `read_text()` universal newlines before every test |
| folded-attendee-line | FPP | FPP | yes | S: fold splits `carol@exam|ple.com`; C/E never look at ATTENDEE |
| dtstart-value-datetime | FFF | FFF | yes | `DTSTART;VALUE=DATE-TIME:` has no `DTSTART:` substring |
| no-prodid-header | FPP | FPP | yes | S needs `PRODID:`; C/E read only DTSTART |
| decoy-second-vevent | PFF | PFF | yes | S takes the first attendee block (Fri 15:00); C: Alice end > 14:00; E: earlier Wed 11:00 |
| extra-attendee-dave | PPP | PPP | yes | S checks presence, not exclusivity, of the three emails |
| lowercase-property-names | FPP | FPP | yes | S needs uppercase `SUMMARY:`; DTSTART line is uppercase |
| input-crlf-rewrite | PPP | PPP | yes | sha256 hashes `read_text()`, so CRLF normalizes to the pinned digests |

Comparison command and output (`compare-out.txt`):

```
$ python3 compare.py corpus/evidence/round41/constraints-probe.txt probe-28.txt
CMP nop indep=FFF receipt=FFF agree
... one line per case ...
AGREE 25/25 disagree=0 (receipt cases=25)
EXTRA dtend-tzid-only indep=FPP observed=FPP agree
EXTRA first-conflicting-decoy indep=PFP observed=PFP agree
EXTRA alice-wed-1000-shifted-1100 indep=FFF observed=FFF agree
```

### 2.1 The two cases where the frozen table and my reading differ

The frozen dry table carries two pilot predictions that the receipt itself marks `match=NO`
(`later-valid-wed-1105`, `seconds-30`, both predicted `PPF`, observed `PFF`). My reading gives the observed
letters, from the code:

* `later-valid-wed-1105` (Wed 11:05–12:05): test 2 computes `e = s + timedelta(hours=1)` (test_outputs.py:136), so
  `t0=11:05 < lunch1=12:30` and `t1=12:05 > lunch0=12:00` → `_hard_ok` returns False at 74; the same slot also
  overlaps Bob and Carol 12:00–13:00. Test 3 finds Wed 11:00 in its minute scan (164) and raises. → `PFF`.
* `seconds-30` (Wed 11:00:30–12:00:30): same lunch branch, `t1=12:00:30 > 12:00` → test 2 fails; test 3's scan
  reaches 11:00 first and raises. → `PFF`.

Both are explained by the frozen table's own note ("runs into lunch and Bob/Carol 12:00"); the frozen `PPF` cell
is a pilot slip, disclosed in `plans/round-41-claims.md` ("including the two the pilot observed wrong … predicted
fail set E, observed C,E"), and my re-derivation sides with the code and the receipt.

**Calibration caveat, stated plainly:** the ticket orders the comparison against `constraints-probe.txt`, so I had
read the receipt before finalising the letters. This is a code-derived re-derivation, not a blind prediction; it
can still be wrong in the same way the frozen table was, and the two contested cases are exactly where I had to
decide against a frozen cell. Nothing else in the table was ambiguous once the branch was identified.

## 3. Three added cases (not in the frozen table), predicted then run

A scratch copy of the frozen probe `probe_indep.py` (this dir, sha256
`ed3884aa3f7fab382e4a458d4add8028622794c2933afb7a209ece03d8d8064f`) differs from
`plans/constraints_probe.py` (sha256 `8c471fbd…`, the frozen digest) only by the three additions; `diff` shows
three inserted hunks and no other change. The lane probe was never edited. Predictions were fixed before the run:
`probe_indep.py` mtime 15:39:25, `predictions.py` mtime 15:39:47, probe output mtime 15:40:08 (-0300).

Definitions added:

```python
X1_ICS = GOOD_ICS.replace("DTEND:20240117T120000Z", "DTEND;TZID=UTC:20240117T120000")
X2_ICS = ics(ev("20240115T110000Z", "20240115T120000Z", summary="decoy", att=()), ev(*GOOD))

    Case("dtend-tzid-only", "FPP", ("utc-format",),
         "DTSTART plain UTC but DTEND carries ;TZID=UTC and no Z: only the structure test reads DTEND",
         meeting=X1_ICS),
    Case("first-conflicting-decoy", "PFP", ("hard-constraints", "earliest"),
         "first VEVENT a Mon 11:00 decoy (no SUMMARY/ATTENDEE); the meeting VEVENT at the correct Wed 11:00",
         meeting=X2_ICS),
    Case("alice-wed-1000-shifted-1100", "FFF", ("inputs-readonly", "no-conflict", "earliest"),
         "Alice's Wed 10:00-11:00 event moved to 11:00-12:00 in the input; meeting booked at Wed 11:00",
         meeting=GOOD_ICS, edit="alice-move-wed-1000-to-1100"),
```

with the edit branch (asserts the pair is unique before replacing):

```python
    elif edit == "alice-move-wed-1000-to-1100":
        old = "DTSTART:20240117T100000Z\nDTEND:20240117T110000Z"
        assert t.count(old) == 1
        p.write_text(t.replace(old, "DTSTART:20240117T110000Z\nDTEND:20240117T120000Z"))
```

Observed lines (full file `probe-28.txt`):

```
CASE dtend-tzid-only predicted=fail observed=fail tests=FPP predicted_tests=FPP match=yes regrade=same violates=utc-format -- DTSTART plain UTC but DTEND carries ;TZID=UTC and no Z: only the structure test reads DTEND
CASE first-conflicting-decoy predicted=fail observed=fail tests=PFP predicted_tests=PFP match=yes regrade=same violates=hard-constraints,earliest -- first VEVENT a Mon 11:00 decoy (no SUMMARY/ATTENDEE); the meeting VEVENT at the correct Wed 11:00
CASE alice-wed-1000-shifted-1100 predicted=fail observed=fail tests=FFF predicted_tests=FFF match=yes regrade=same violates=inputs-readonly,no-conflict,earliest -- Alice's Wed 10:00-11:00 event moved to 11:00-12:00 in the input; meeting booked at Wed 11:00
```

What each adds to the C2 picture:

1. `dtend-tzid-only` — a property-parameter form on DTEND only. Structure fails on the `DTEND:` regex (126),
   while tests 2 and 3 still pass because they never parse DTEND and assume `start+1h` (136). New axis:
   DTSTART and DTEND are parsed by *different* regexes, so a half-RFC-valid pair is graded 2/3.
2. `first-conflicting-decoy` — the mirror of the frozen decoy cases with the correct meeting VEVENT in second
   place and a rubbish first block at a *conflicting* time (Mon 11:00, Bob and Carol busy). S picks the second
   block and passes (PPP shape expected at S), but C and E read the first `DTSTART:` in the file, so a submission
   that is correct by the instruction fails C (overlap with Bob/Carol 11:00–12:00) and passes E only because
   Monday is not a tie candidate. This is a failure shape the frozen table lacks: `decoy-first-vevent` passes
   (decoy at the right slot) and `decoy-second-vevent` fails C on the early block (Alice ceiling). Here the
   *correct* answer fails test 2 while the file's first block is not even an attendee meeting.
3. `alice-wed-1000-shifted-1100` — edit an input (S digest mismatch → F), and notice that moving Alice's 10:00
   event to 11:00 both collides with the booked slot (C: overlap) and frees Wed 10:00, which test 3 then reports
   as an earlier valid slot (FFF). It shows test 3's verdict is computed from the *editable* `/app` copies, so an
   invented "earlier slot" can be blamed on the candidate.

## 4. Reproducibility of the frozen receipt

The same scratch copy, still carrying the frozen 25 cases verbatim, reproduces them byte for byte:

```
$ diff <(grep '^CASE ' corpus/evidence/round41/constraints-probe.txt) \
       <(grep '^CASE ' probe-28.txt | head -25) && echo "BYTE-EQUAL 25/25 case lines"
BYTE-EQUAL 25/25 case lines
$ grep -E '^(regrade|cases=)' probe-28.txt
regrade cases=28 differ=0
cases=28 observed_pass=6 observed_fail=22 mismatches=2
```
The frozen tail (`regrade cases=25 differ=0`, `cases=25 observed_pass=6 observed_fail=19 mismatches=2`) is the
same after removing my three cases (all `fail`), including the two `match=NO` rows. The pins printed by the run
are the frozen capture digests (`test_outputs.py` `1422b345…`, matching S122's sha256 prefix).

## 5. Cross-checks against the frozen artefacts

* Slot model: the probe docstring and my parser agree — two valid starts, Wed 11:00 earliest; nothing in the
  instruction (Alice's morning preference, Bob's afternoon preference, Carol's Monday avoidance) can change the
  earliest slot, because there is only one candidate in the morning band per day.
* `decoy-first-vevent` → `PPP` reproduced; my `first-conflicting-decoy` shows the same first-DTSTART read is a
  two-way hazard, not only a false pass.
* `input-crlf-rewrite` → `PPP` reproduced: the sha256 branch hashes `read_text()` output (95), i.e. after
  universal-newline translation, so CRLF rewrites are invisible to the integrity check.
* `duration-90min` → `FPP` reproduced: DTEND is read only at 126-127.

## 6. Limits and risks

* Not a blind prediction (receipt read first, §2.1); the value is that the letters are reproducible from the code
  and that the two frozen slips are identified with their branches.
* My extra cases live only in `probe_indep.py`; their `violates=` tags (`utc-format`; `hard-constraints,earliest`;
  `inputs-readonly,no-conflict,earliest`) are my reading and must not be merged into the frozen dry table or the
  V7 requirement map, which derive from the frozen 25.
* Host `python3` 3.14.8 stands in for the image's `uvx -p 3.13` interpreter, as the probe declares; the image is
  never pulled.
* The Carol 4:45 PM buffer, the Monday tie-break and the morning assert are unreachable on this dataset for the
  reasons in §1; the probe is therefore silent on three grader clauses, and my 3/3 does not price them.
* The extra edit `alice-move-wed-1000-to-1100` asserts uniqueness of the `DTSTART/DTEND` pair; it would fail
  loudly rather than edit the wrong event if the capture changed.

## 7. Files

Added only here (scratch receipts copied before `rm -rf` of
`/fast/scratch/hyaku/kengaku-r41/R41CritIndep`):

| file | sha256 |
|---|---|
| `indep_slots.py` | `882918aee891ad2b937f7c2f8fa810116b54113fdc3fb95d6bcb822a6c351171` |
| `predictions.py` | `9c131f9d9b254e5150e4f87d8a406f627eecaf837926872f412029bcd0da0ff9` |
| `compare.py` | `b4c6c5682d214d39926eed1a85f2413d081aba576fc46ce3888624639fc7966c` |
| `probe_indep.py` (modified copy) | `ed3884aa3f7fab382e4a458d4add8028622794c2933afb7a209ece03d8d8064f` |
| `slots-out.txt` | `fe2dc898a1fd46075b44146a37a1aefb0fbd003110c2004a5b1927e68961e415` |
| `probe-28.txt` | `b3a5c4ff4f489fb1d2c16e600683ba06a26488a77b120aa52bb767616ae9713f` |
| `compare-out.txt` | `10785d9c011ce3180192af4d18425f79f5149358c27eaa318b2ff1e44c902cc3` |

Lane files changed: none.

VERDICT: indep-agree-25/25-extra-3/3
