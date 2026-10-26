#!/usr/bin/env python3
"""Supplementary (OUTSIDE the frozen C2 predicate) candidates against the pinned regex-log grader.

Seat R36CritUnenforced, round 36 wave 1. Hypothesis H: the pinned grader leaves at least three
instruction requirements unenforced beyond the probe's frozen 24 cases.

Predictions below were written from a static reading of
  corpus/evidence/round36/tb2-regex-log/test_outputs.py (sha256 pinned) and instruction.md,
BEFORE the first execution of this file. This script adds nothing to the frozen probe and cannot
change it: it imports the probe's `run_grader` only, re-checks the grader digest itself, and runs a
separate table. Cases are new relative to plans/regex_log_probe.py's frozen 24 (verified at
runtime: no regex string is equal to a frozen one).

Run: python3 .ufo/waves/round-36/build/R36CritUnenforced/extra_cases.py --lane <lane root>
"""
import argparse
import hashlib
import importlib.util
import pathlib
import sys

LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/kengaku-shokunin"
PROBE_REL = "plans/regex_log_probe.py"
GRADER_REL = "corpus/evidence/round36/tb2-regex-log/test_outputs.py"
GRADER_SHA256 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"

OCT = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
NA_B = r"(?<![A-Za-z0-9])"
NA_A = r"(?![A-Za-z0-9])"
IP = NA_B + rf"(?:{OCT}\.){{3}}{OCT}" + NA_A
BASE = rf"\d{{4}}-\d{{2}}-\d{{2}}"
# reference month-aware body (February to 29, 30-day months to 30)
STRICT = (r"\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])"
          r"|(?:0[469]|11)-(?:0[1-9]|[12]\d|30)|02-(?:0[1-9]|[12]\d))")


def line(body=BASE, ipx=IP, right=NA_A):
    """Reference shape: line anchored by ^, one capture group = the date findall returns."""
    return rf"^(?=.*{ipx}).*({body}){right}"


CASES = [
    # name, regex, prediction, instruction requirement exercised, novelty note
    ("E01-feb30-apr31-range", line(
        r"\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])"
        r"|(?:0[469]|11)-(?:0[1-9]|[12]\d|3[01])|02-(?:0[1-9]|[12]\d|3[0]))"), "pass",
     "month-length validity: Feb 30 / Apr 31 / Jun 31 / Sep 31 / Nov 31 must not match",
     "confirmatory sharp of frozen reference-lenient-days (Feb capped at 30, not 31, and 30-day months at 31)"),
    ("E02-literal-2000-02-30", line(
        STRICT + r"|2000-02-30"), "pass",
     "month-length validity, spelled as a literal: 2000-02-30 must not match",
     "new form: otherwise-correct body + one literal invalid date (frozen hardcoded list holds only the nine expected)"),
    ("E03-feb-only-30-31", line(
        r"\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])"
        r"|(?:0[469]|11)-(?:0[1-9]|[12]\d|30)|02-3[01])"), "pass",
     "February allows days 01-29 in all years; a body that accepts only 30/31 and rejects 01-28 violates it",
     "new form: inverted Feb policy (frozen only shows the lenient direction)"),
    ("E04-leap-only-feb29", line(
        r"(?:\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])"
        r"|(?:0[469]|11)-(?:0[1-9]|[12]\d|30)|02-(?:0[1-9]|1\d|2[0-8]))"
        r"|[0-9]{2}(?:0[48]|[2468][048]|[13579][26])-02-29)"), "pass",
     "instruction explicitly forbids distinguishing leap years (Feb 29 in all years)",
     "new form: real Gregorian leap rule applied (a forbidden inference) still accepted"),
    ("E05-month-day-one-digit", line(
        r"\d{4}-(?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12]\d|3[01])"), "pass",
     "format YYYY-MM-DD: MM and DD are exactly two digits, so 2025-1-9 must not match",
     "new: no frozen case tolerates one-digit month/day (frozen vary month/day RANGE only)"),
    ("E06-year-four-or-five", line(r"\d{4,5}-\d{2}-\d{2}"), "pass",
     "format YYYY-MM-DD: the year is exactly four digits",
     "confirmatory sharp of frozen year-any-digit-count (2-6 digits)"),
    ("E07-ip-fourth-octet-00",
     line(ipx=NA_B + rf"(?:{OCT}\.){{3}}(?:{OCT}|00)" + NA_A), "pass",
     "IPv4 without leading zeros in each octet: a fourth octet '00' must not match",
     "new corner of frozen ip-leading-zeros-allowed: '00' accepted while '01'-'09' are rejected"),
    ("E08-dot-in-boundary-class",
     line(ipx=NA_B + rf"(?:{OCT}\.){{3}}{OCT}(?![A-Za-z0-9.])", right=r"(?![A-Za-z0-9.])"), "pass",
     "boundary clause: a date/IPv4 is not immediately preceded or followed by an alphanumeric",
     "new: '.' classed as alphanumeric on both boundaries (no log span abuts a dot)"),
    ("E09-inline-dotall-override",
     rf"(?s)^(?=.*{IP}).*?({BASE}){NA_A}", "fail",
     "one date must come from the line the IPv4 is on; the last date in that line",
     "new: submission overrides the grader's flags with inline (?s); cross-line scan"),
    ("E10-inline-multiline-disabled",
     rf"(?-m)^(?=.*{IP}).*({BASE}){NA_A}", "fail",
     "the graded call passes re.MULTILINE; disabling it must not still produce nine dates",
     "new: inline (?-m) kills the per-line anchor"),
    ("E11-cross-line-bridge",
     rf"^(?=.*{IP})[\s\S]*?({BASE}){NA_A}", "fail",
     "the matched date must be on the IPv4's own line, and the last date of it",
     "new: [\\s\\S] bridge between IP witness and date"),
    ("E12-newline-as-date-separator",
     line(r"\d{4}[\s-]\d{2}[\s-]\d{2}"), "pass",
     "format YYYY-MM-DD: the separators are '-'; a newline inside the date body is not the format",
     "new: date body tolerates whitespace separators (frozen only use '-')"),
    ("E13-newline-required-after-match",
     rf"^(?=.*{IP}).*({BASE})(?=\n)", "fail",
     "the graded log ends without a trailing newline; a pattern requiring one loses a date",
     "new: dependence on a trailing newline (fixture property baked in, unstated in instruction)"),
    ("E14-whitespace-only-adjacency",
     rf"^(?=.*{IP}).*(?<!\S)({BASE})(?=\s|\Z)", "pass",
     "boundary clause is 'not alphanumeric adjacent'; whitespace-only adjacency is stricter",
     "new: over-restrictive boundary accepted (a date followed by ',' would be missed)"),
]


def load_probe(lane):
    spec = importlib.util.spec_from_file_location("r36_probe", lane / PROBE_REL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=LANE_DEFAULT)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    gpath = lane / GRADER_REL
    digest = hashlib.sha256(gpath.read_bytes()).hexdigest()
    if digest != GRADER_SHA256:
        print(f"REFUSE grader digest {digest} != pinned {GRADER_SHA256}")
        return 2
    probe = load_probe(lane)
    frozen = {c[1] for c in probe.build_cases() if c[1] is not None}
    print(f"grader={GRADER_REL} sha256={digest} pin={probe.PIN} cases={len(CASES)}")
    dup = [n for n, rx, *_ in CASES if rx in frozen]
    print(f"duplicates_of_frozen_24={dup}")
    mism = 0
    npass = 0
    for name, rx, pred, req, note in CASES:
        obs, msg = probe.run_grader(gpath, rx, "file")
        ok = obs == pred
        mism += not ok
        npass += obs == "pass"
        print(f"case={name} predicted={pred} observed={obs} match={'yes' if ok else 'NO'} "
              f"assertion={msg!r} requirement={req!r} novelty={note!r}")
    print(f"cases={len(CASES)} observed_pass={npass} observed_fail={len(CASES) - npass} mismatches={mism}")
    return 0 if mism == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
