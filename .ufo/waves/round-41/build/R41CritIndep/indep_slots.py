#!/usr/bin/env python3
"""R41CritIndep: independent derivation of valid 1-hour slots for tb2 constraints-scheduling.

Own ICS parser (property name split on ';' / ':', RFC 5545 line unfolding), own constraint
model read from instruction.md, no import of the task grader. Enumerates every minute-granular
start in the Jan 15-19 2024 window that satisfies all hard constraints and conflicts with no
existing VEVENT in the three captured calendars.

  python3 indep_slots.py <capture-dir>
"""
import re
import sys
from datetime import datetime, date, timedelta

BUSY = ("alice_calendar.ics", "bob_calendar.ics", "carol_calendar.ics")


def unfold(text):
    # RFC 5545 3.1: a line starting with SP/HTAB continues the previous line.
    return re.sub(r"\r?\n[ \t]", "", text)


def prop(block, name):
    """Return the value of property `name` in an unfolded VEVENT block, or None.
    Property name is everything before the first ':' and, if present, before the first ';'
    parameter separator (so DTSTART;TZID=UTC:... is still DTSTART)."""
    for line in block.splitlines():
        if not line or line[0] in " \t":
            continue
        head, sep, value = line.partition(":")
        if not sep:
            continue
        if head.split(";", 1)[0].upper() == name:
            return value.strip()
    return None


def parse_utc(value):
    m = re.fullmatch(r"(\d{8})T(\d{6})Z", value or "")
    if not m:
        return None
    return datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S")


def events(text):
    out = []
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", unfold(text), flags=re.S):
        s, e = parse_utc(prop(block, "DTSTART")), parse_utc(prop(block, "DTEND"))
        out.append((s, e, prop(block, "SUMMARY")))
    return out


def conflicts(t0, t1, busy):
    # half-open intervals; touching endpoints do not conflict
    return any(t0 < e and t1 > s for s, e, _ in busy)


def biz_ok(t0, t1):
    """Hard constraints from instruction.md, line references: availability (L5-8), window and
    business hours (L1), one hour (L10)."""
    if t0.date() != t1.date() or t0.weekday() >= 5:            # L1 window, Mon-Fri
        return False
    if not (date(2024, 1, 15) <= t0.date() <= date(2024, 1, 19)):
        return False
    if t0.hour < 9 or t1.hour > 18 or (t1.hour == 18 and t1.minute > 0):
        return False                                            # L1 business hours 9-18
    if t0.hour < 9:
        return False                                            # Alice: not before 9 AM
    if t1.hour > 14 or (t1.hour == 14 and t1.minute > 0):
        return False                                            # Alice: no meetings after 2 PM
    if t0.hour < 10:
        return False                                            # Bob: no meetings before 10 AM
    if t0.weekday() in (1, 3):                                  # Tue/Thu
        if t1.hour > 16 or (t1.hour == 16 and t1.minute > 30):
            return False                                        # Bob: leave by 4:30 PM
    if t1.hour > 17 or (t1.hour == 17 and t1.minute > 0):
        return False                                            # Carol: available 9 AM-5 PM
    lunch0, lunch1 = t0.replace(hour=12, minute=0), t0.replace(hour=12, minute=30)
    if t0 < lunch1 and t1 > lunch0:
        return False                                            # Carol: lunch 12:00-12:30
    return True


def main():
    cap = sys.argv[1]
    busy, per = [], {}
    for name in BUSY:
        evs = events(open(f"{cap}/{name}", encoding="utf-8").read())
        per[name] = evs
        busy += evs
    print("parsed events:", {k: len(v) for k, v in per.items()})
    for name in BUSY:
        for s, e, summ in per[name]:
            print(f"  {name[0]} {s:%a %m-%d %H:%M}-{e:%H:%M} {summ}")
        if any(s is None or e is None for s, e, _ in per[name]):
            print(f"UNPARSED event in {name}"); return 2
    valid = []
    t = datetime(2024, 1, 15, 0, 0)
    while t < datetime(2024, 1, 20, 0, 0):
        t1 = t + timedelta(hours=1)
        if biz_ok(t, t1) and not conflicts(t, t1, busy):
            valid.append(t)
        t += timedelta(minutes=1)
    print(f"valid_1h_slots={len(valid)}")
    for t in valid:
        print(f"SLOT {t:%Y-%m-%d %H:%M}-{(t + timedelta(hours=1)):%H:%M} UTC ({t:%A})")
    print(f"earliest={valid[0]:%Y-%m-%d %H:%M} UTC")
    # same-minute candidates at the earliest minute (the tie-break set the grader builds)
    cand = [t for t in valid if (t.hour, t.minute) == (valid[0].hour, valid[0].minute)]
    print("same-minute candidates:", [f"{t:%a %H:%M}" for t in cand])
    return 0


if __name__ == "__main__":
    sys.exit(main())
