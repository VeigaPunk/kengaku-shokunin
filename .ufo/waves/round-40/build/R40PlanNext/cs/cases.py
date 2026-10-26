"""R40PlanNext constraints-scheduling probe: cases + predictions (written BEFORE the first run).
pred = set of test names predicted to FAIL (test_ prefix dropped): S=structure, C=constraints, E=earliest."""
HDR = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//probe//EN\n"
def ev(s, e, summary="Team Planning Meeting", att=("alice","bob","carol")):
    a = "".join(f"ATTENDEE;CN={x}:mailto:{x}@example.com\n" for x in att)
    return f"BEGIN:VEVENT\nDTSTART:{s}\nDTEND:{e}\nSUMMARY:{summary}\n{a}END:VEVENT\n"
def ics(*evs, extra=""): return HDR + "".join(evs) + extra + "END:VCALENDAR\n"
GOOD = ("20240117T110000Z", "20240117T120000Z")
CASES = {
 "nop": dict(pred="S,C,E", file=None, note="no output file: all three tests read it"),
 "oracle-solve.sh": dict(pred="-", file="ORACLE", note="task's own solve.sh"),
 "literal-correct-slot": dict(pred="-", file=ics(ev(*GOOD)), note="hand-typed ICS for Wed 11:00, never reads calendars"),
 "later-valid-wed-1105": dict(pred="E", file=ics(ev("20240117T110500Z","20240117T120500Z")), note="valid but 5 minutes after the earliest"),
 "later-valid-thu-1100": dict(pred="E", file=ics(ev("20240118T110000Z","20240118T120000Z")), note="valid, a day late"),
 "conflict-mon-1230": dict(pred="C,E", file=ics(ev("20240115T123000Z","20240115T133000Z")), note="overlaps Alice 13:00 event"),
 "bob-start-0900-wed": dict(pred="C", file=ics(ev("20240117T090000Z","20240117T100000Z")), note="Bob no meetings before 10; earliest test passes because _hard_ok rejects 9:00 too"),
 "decoy-first-vevent": dict(pred="-", file=ics(ev(*GOOD, summary="decoy", att=()), ev("20240119T150000Z","20240119T160000Z")), note="tests 2-3 read the first DTSTART in the file, test 1 reads the attendee VEVENT"),
 "duration-90min": dict(pred="S", file=ics(ev("20240117T110000Z","20240117T123000Z")), note="DTEND ignored by tests 2-3"),
 "missing-carol": dict(pred="S", file=ics(ev(*GOOD, att=("alice","bob"))), note="attendee missing"),
 "title-wrong": dict(pred="S", file=ics(ev(*GOOD, summary="Team Meeting")), note="summary differs"),
 "seconds-30": dict(pred="E", file=ics(ev("20240117T110030Z","20240117T120030Z")), note="minute granularity: 11:00:30 > earlier 11:00:00"),
 "tzid-form": dict(pred="S,C,E", file=HDR + "BEGIN:VEVENT\nDTSTART;TZID=UTC:20240117T110000\nDTEND;TZID=UTC:20240117T120000\nSUMMARY:Team Planning Meeting\nATTENDEE:mailto:alice@example.com\nATTENDEE:mailto:bob@example.com\nATTENDEE:mailto:carol@example.com\nEND:VEVENT\nEND:VCALENDAR\n", note="no Z-timestamp -> regex miss"),
 "weekend-sat-20": dict(pred="S,C,E", file=ics(ev("20240120T110000Z","20240120T120000Z")), note="outside Jan 15-19"),
 "input-appended": dict(pred="S", file="MODIFY:alice-append", note="calendar byte-modified, slot correct"),
 "input-event-deleted-wed-1000": dict(pred="S", file="MODIFY:alice-delete-wed-1000", note="remove Alice's Wed 10:00 event then book Wed 10:00; only the sha256 integrity check sees it"),
}
