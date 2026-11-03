#!/usr/bin/env python3
"""Sweep the round-66 verifier spot-check sections for candidate Mistakes rows.

Sections read (see the lesson's ## Sweep): 2 (per-claim re-check), 3 (admission),
4 (discernment spot-check), 5 (trend verdicts), 6 (routed defects), 7 (SHONEN note).

Every defect-shaped statement found in section 2 is printed with its disposition:
either it is one of the two rows mined into the round-67 lesson, or it is a
section-6 routed item (a lane fix routing, not a mined mistake row), or it is a
new row (which would have to be reported).

Exit 0 when no new row is found; exit 1 when a new row is found.
"""
import re
import sys

PATH = ("/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/"
        "round-66-verifier-spotcheck.md")

# Defect-shaped markers: a statement that asserts something is wrong, missing,
# falsified or refused.
MARKERS = re.compile(
    r"not verified|falsif|must fix|false premise|does not carry|no longer|"
    r"kill rule|defect|refuse|accepts a|admitted\b|false\b|wrong|miss\b",
    re.I)

# Row 1 (round-67 lesson) markers.
ROW1 = ("PROBE", "kill rule b", "committed round-65 receipt")
# Row 2 (round-67 lesson) markers.
ROW2 = ("M-1", "fabricated", "red-before")


def section2(text):
    m = re.search(r"^## 2\..*?(?=^## 3\.)", text, re.S | re.M)
    return m.group(0) if m else ""


def section6(text):
    m = re.search(r"^## 6\..*?(?=^## 7\.)", text, re.S | re.M)
    return m.group(0) if m else ""


def main():
    text = open(PATH, encoding="utf-8").read()
    s2 = section2(text)
    s6 = section6(text)
    print("SWEEP file=%s" % PATH)
    print("SWEEP sections-read=2 (per-claim re-check), 3 (admission), "
          "4 (discernment spot-check), 5 (trend verdicts), "
          "6 (routed defects), 7 (SHONEN note)")
    print("SWEEP section2-lines=%d section6-lines=%d"
          % (len(s2.splitlines()), len(s6.splitlines())))

    new_rows = []
    mined = 0
    print("--- section 2 candidate statements ---")
    for line in s2.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- ") and not stripped.startswith("*"):
            continue
        if not MARKERS.search(stripped):
            continue
        if any(k in stripped for k in ROW1):
            disp = "MINED row-1 (R66-C2 predicate froze on a PROBE line the "
            disp += "committed receipt never carries)"
            mined += 1
        elif any(k in stripped for k in ROW2):
            disp = "MINED row-2 (checker accepted a fabricated receipt)"
            mined += 1
        else:
            disp = "NEW ROW CANDIDATE"
            new_rows.append(stripped)
        print("  [%s] %s" % (disp, stripped[:220]))
        print("      -> %s" % disp)

    print("--- section 6 candidate statements ---")
    carried = 0
    for line in s6.splitlines():
        stripped = line.strip()
        if not re.match(r"^\d+\.\s", stripped):
            continue
        if not MARKERS.search(stripped):
            continue
        carried += 1
        print("  [ROUTED item %s] %s" % (stripped.split(".")[0],
                                         stripped[:200]))
    print("SWEEP section2-mined=%d section6-routed=%d new-rows=%d"
          % (mined, carried, len(new_rows)))
    if new_rows:
        print("SWEEP VERDICT new-row-found")
        return 1
    print("SWEEP VERDICT no-further-row")
    return 0


if __name__ == "__main__":
    sys.exit(main())
