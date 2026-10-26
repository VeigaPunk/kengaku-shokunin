#!/usr/bin/env python3
"""R41CritIndep: hand predictions of the three grader test verdicts for every frozen case.

Letters are in test file order: S = test_structure_event_title_attendees_duration_window,
C = test_constraints_conflicts_business_hours, E = test_earliest_tiebreakers_and_carol_buffer.
Each prediction is derived only from reading test_outputs.py and the end state the frozen
dry table describes; `why` names the deciding branch.  Readings used:

  S  : integrity (== /inputs text, else sha256 of read_text()); strip starts/ends VCALENDAR;
       VERSION:2.0, PRODID:, BEGIN/END:VEVENT; the meeting block is the first VEVENT block that
       contains the literal "SUMMARY:Team Planning Meeting" AND all three emails; each email must
       match ^ATTENDEE[:;].*<email>$ (re.I, re.M); DTSTART:/DTEND: regexes must both hit in the
       block; DTEND-DTSTART == 1h; Jan 15-19 2024, weekday.
  C  : reads the FIRST "DTSTART:<stamp>Z" in the whole output file in file order, end = start+1h
       (DTEND is never parsed); _hard_ok (Alice start>=9 end<=14, Bob start>=10, Tue/Thu end<=16:30,
       Carol end<=17, no 12:00-12:30 overlap, same date, weekday, business 9-18); then no overlap
       against the three INPUT calendars (the /app copies, which may be edited).
  E  : same first-DTSTART read; minute loop over Jan 15 09:00..sched for an earlier feasible slot;
       same-minute-per-day candidates for the Monday tie-break; then `9 <= sched.hour < 12`;
       then Carol's 4:45 PM buffer branches (unreachable for any 9-14 slot).

`violates` is my reading of the requirement tags, independent of the frozen `violates=` column.
"""
CASE_ORDER = [
    "nop", "oracle-solve-sh", "literal-correct-slot", "later-valid-wed-1105",
    "later-valid-thu-1100", "conflict-mon-1230", "bob-start-0900-wed", "decoy-first-vevent",
    "duration-90min", "missing-carol", "title-wrong", "seconds-30", "tzid-form",
    "weekend-sat-20", "input-appended", "input-event-deleted-wed-1000",
    "wed-1059-overlaps-alice", "crlf-line-endings", "folded-attendee-line",
    "dtstart-value-datetime", "no-prodid-header", "decoy-second-vevent", "extra-attendee-dave",
    "lowercase-property-names", "input-crlf-rewrite",
]

PRED = {
    "nop": ("FFF", "no meeting file: every test reads it -> FileNotFoundError in S, C and E"),
    "oracle-solve-sh": ("PPP", "solve.sh writes Wed 11:00; all three pass on it (checked: score sort -> Wed 11:00)"),
    "literal-correct-slot": ("PPP", "Wed 11:00, 3 attendees, 1h, legacy formatting: no test objects"),
    "later-valid-wed-1105": ("PFF", "11:05-12:05: S is structural; C fails the 12:00 lunch branch AND Bob/Carol 12-13 overlap; E fails on the earlier Wed 11:00 slot"),
    "later-valid-thu-1100": ("PPF", "Thu 11:00 is feasible (C passes) but Wed 11:00 is earlier -> E only"),
    "conflict-mon-1230": ("PFF", "Mon 12:30-13:30: C overlaps Alice Mon 13-14; E has no earlier slot but the morning assert (hour 12) fails"),
    "bob-start-0900-wed": ("PFP", "Wed 09:00: C fails Bob start<10; E has no earlier feasible slot and 9<=9<12 -> P"),
    "decoy-first-vevent": ("PPP", "S picks the attendee block (Fri 15:00) which is structurally fine; C and E read the first DTSTART (the Wed 11:00 decoy) and pass"),
    "duration-90min": ("FPP", "S only test that reads DTEND (1.5h); C/E use start+1h"),
    "missing-carol": ("FPP", "S needs all three emails inside the meeting block"),
    "title-wrong": ("FPP", "S needs the literal SUMMARY:Team Planning Meeting"),
    "seconds-30": ("PFF", "11:00:30-12:00:30: C fails the lunch branch (end 12:00:30 > 12:00), E fails on the earlier 11:00 slot"),
    "tzid-form": ("FFF", "DTSTART;TZID has no 'DTSTART:' substring -> _dt assert fails in all three"),
    "weekend-sat-20": ("FFF", "Jan 20: S window assert, C weekday>=5 and E earlier-slot all fail"),
    "input-appended": ("FPP", "S: sha256 branch on read_text() now mismatches; C/E book Wed 11:00 in unchanged /app copies"),
    "input-event-deleted-wed-1000": ("FPP", "S: digest mismatch; C/E pass on the edited calendar and the Wed 10:00 slot"),
    "wed-1059-overlaps-alice": ("PFP", "10:59-11:59: C overlaps Alice Wed 10-11; E: no earlier feasible slot, 10 in 9-12 -> P"),
    "crlf-line-endings": ("PPP", "read_text() universal newlines erases CRLF before every test"),
    "folded-attendee-line": ("FPP", "S: the fold splits carol@exam|ple.com so the email is not in the block; C/E never look at ATTENDEE"),
    "dtstart-value-datetime": ("FFF", "DTSTART;VALUE=DATE-TIME has no 'DTSTART:' substring -> _dt assert in all three"),
    "no-prodid-header": ("FPP", "S needs 'PRODID:'; C/E only read DTSTART"),
    "decoy-second-vevent": ("PFF", "S picks the first attendee block (Fri 15:00, structurally ok); C fails Alice end>14; E fails on the earlier Wed 11:00"),
    "extra-attendee-dave": ("PPP", "S checks the three emails are present, not that they are the only attendees"),
    "lowercase-property-names": ("FPP", "S needs literal uppercase SUMMARY:; C/E use the uppercase DTSTART line"),
    "input-crlf-rewrite": ("PPP", "sha256 branch hashes read_text() (CRLF -> LF), so the normalized inputs hash to the pinned digests"),
    # --- three added cases (not in the frozen table); predictions fixed before the scratch run
    "dtend-tzid-only": ("FPP", "S: the DTEND line is 'DTEND;TZID=UTC:...' so the DTEND: regex misses -> _dt assert; C/E use start+1h"),
    "first-conflicting-decoy": ("PFP", "S picks the second block (Wed 11:00) which is structurally fine; C reads the first DTSTART (Mon 11:00) and overlaps Bob/Carol 11-12; E: no earlier feasible slot, Monday is not a candidate at 11:00 -> P"),
    "alice-wed-1000-shifted-1100": ("FFF", "S: digest mismatch; C overlaps Alice's moved 11-12 event; E finds the now-free Wed 10:00 slot as earlier"),
}

if __name__ == "__main__":
    for cid in CASE_ORDER:
        print(f"PREDICTED {cid} tests={PRED[cid][0]}")
