#!/usr/bin/env python3
"""Supplementary candidates v2 (OUTSIDE the frozen C2 predicate) — seat R36CritUnenforced.

Why v2 exists (disclosed): the v1 table (extra_cases.py, sha256 c1025e9a…) built its witnesses with a
helper that omitted the reference's LEFT date boundary `(?<![A-Za-z0-9])` inside the capture, so ten
"pass"-predicted witnesses matched `2021-08-20` inside the N line `abc2021-08-20` and failed; three
also used a range-free date body, so the N lines `2023-13-05`, `2022-00-15`, `1995-06-32`,
`2001-09-00` were matched. That was a witness-construction defect on this seat's side, not a grader
finding (`extra-cases-run.txt`, `diag.py`). v1's predictions are NOT edited; v2 re-derives witnesses
from the corrected helper and STARTS FROM THE REFERENCE BODY WITH RANGE CHECKS, varying exactly one
feature per case. v2 predictions were written before the first v2 run.

Run: python3 .ufo/waves/round-36/build/R36CritUnenforced/extra_cases_v2.py --lane <lane root>
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
MONTH = r"(?:0[1-9]|1[0-2])"
DAY = r"(?:0[1-9]|[12]\d|3[01])"
BASE = rf"\d{{4}}-{MONTH}-{DAY}"          # calendar-range-checked, the frozen reference body
FEB29 = (r"\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])"
         r"|(?:0[469]|11)-(?:0[1-9]|[12]\d|30)|02-(?:0[1-9]|[12]\d))")


def line(body=BASE, ipx=IP, left=NA_B, right=NA_A):
    """Reference shape (plans/regex_log_probe.py line_rx/date), capture group = the date."""
    return rf"^(?=.*{ipx}).*{left}({body}){right}"


CASES = [
    ("V01-feb30-apr31-range", line(
        r"\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])"
        r"|(?:0[469]|11)-(?:0[1-9]|[12]\d|3[01])|02-(?:0[1-9]|[12]\d|3[0]))"), "pass",
     "month-length validity (Feb 30, 30-day month 31) must not match",
     "confirmatory sharp: Feb capped at 30 and 30-day months raised to 31 (frozen lenient-days raises every month)"),
    ("V02-literal-2000-02-30", line(FEB29 + r"|2000-02-30"), "pass",
     "month-length validity for 2000-02-30 specifically",
     "new form: otherwise-correct body plus one literal invalid date"),
    ("V03-feb-only-30-31", line(
        r"\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])"
        r"|(?:0[469]|11)-(?:0[1-9]|[12]\d|30)|02-3[01])"), "pass",
     "February accepts days 01-29; a body accepting only 30/31 and rejecting 01-28 violates it",
     "new form: inverted Feb policy (frozen shows only the lenient direction)"),
    ("V04-leap-only-feb29", line(
        r"(?:\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])"
        r"|(?:0[469]|11)-(?:0[1-9]|[12]\d|30)|02-(?:0[1-9]|1\d|2[0-8]))"
        r"|[0-9]{2}(?:0[48]|[2468][048]|[13579][26])-02-29)"), "pass",
     "instruction forbids distinguishing leap years (Feb 29 in ALL years)",
     "new form: real leap rule applied, i.e. the forbidden inference, still accepted"),
    ("V05-month-day-one-digit", line(rf"\d{{4}}-(?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12]\d|3[01])"), "pass",
     "format YYYY-MM-DD: MM and DD are exactly two digits, 2025-1-9 must not match",
     "new: no frozen case varies field WIDTH (frozen vary month/day RANGE only)"),
    ("V06-month-three-digit", line(rf"\d{{4}}-\d{{2,3}}-{DAY}"), "pass",
     "format YYYY-MM-DD: MM is exactly two digits, 2025-001-09 must not match",
     "new: wide month width (other direction of the same width face)"),
    ("V07-year-four-or-five", line(rf"\d{{4,5}}-{MONTH}-{DAY}"), "pass",
     "format YYYY-MM-DD: the year is exactly four digits",
     "confirmatory sharp of frozen year-any-digit-count (which used 2..6 digits)"),
    ("V08-ip-fourth-octet-00", line(ipx=NA_B + rf"(?:{OCT}\.){{3}}(?:{OCT}|00)" + NA_A), "pass",
     "IPv4 without leading zeros in each octet: a '00' fourth octet must not match",
     "new corner of frozen ip-leading-zeros-allowed: accepts '00' while rejecting '01'-'09'"),
    ("V09-ip-octet-zero-padded", line(
        ipx=NA_B + rf"(?:(?:0{{1,2}})?{OCT}\.){{3}}(?:0{{1,2}})?{OCT}" + NA_A), "pass",
     "IPv4 in normal decimal notation: '0255' must not be an octet",
     "new: zero-padded octets beyond the reachable form (no log octet carries padding)"),
    ("V10-dot-in-boundary-class",
     line(ipx=NA_B + rf"(?:{OCT}\.){{3}}{OCT}(?![A-Za-z0-9.])", right=r"(?![A-Za-z0-9.])"), "pass",
     "boundary clause: '.' adjacent to a match must still be graded as a non-alphanumeric",
     "new: '.' classed as alphanumeric on both boundaries (no log span abuts a dot)"),
    ("V11-whitespace-only-adjacency",
     rf"^(?=.*{IP}).*(?<!\S)({BASE})(?=\s|\Z)", "pass",
     "boundary clause is only 'not alphanumeric adjacent'; whitespace-only adjacency is stricter",
     "new: over-restrictive boundary accepted (a date followed by ',' or ')' would be missed)"),
    ("V12-slash-separator", line(rf"\d{{4}}[-/]{MONTH}-{DAY}"), "pass",
     "format YYYY-MM-DD: the separators are '-', 2025/01-09 must not match",
     "new: alternate separator character accepted"),
    ("V13-newline-as-separator", line(rf"\d{{4}}[\s-]{MONTH}[\s-]{DAY}"), "pass",
     "format YYYY-MM-DD: a newline or space inside the date body is not the format",
     "new: date body tolerates whitespace separators (frozen bodies use '-' only)"),
    ("V14-inline-dotall-override", rf"(?s)^(?=.*{IP}).*?({BASE}){NA_A}", "fail",
     "the date must come from the IPv4's line and be that line's last date",
     "new: submission overrides the grader's flags with inline (?s) -> cross-line scan"),
    ("V15-inline-multiline-scoped-off", rf"(?-m:^)(?=.*{IP}).*{NA_B}({BASE}){NA_A}", "fail",
     "the graded call applies re.MULTILINE; a pattern disabling it must not produce nine dates",
     "new: scoped (?-m:^) turns the per-line anchor into a string anchor"),
    ("V16-cross-line-bridge", rf"^(?=.*{IP})[\s\S]*?{NA_B}({BASE}){NA_A}", "fail",
     "the matched date must be on the IPv4's own line, and the last date of it",
     "new: [\\s\\S] bridge between IP witness and date"),
    ("V17-newline-required-after-match", rf"^(?=.*{IP}).*{NA_B}({BASE})(?=\n)", "fail",
     "the graded log has no trailing newline; requiring one after each match loses dates",
     "new: dependence on a trailing newline (fixture property, unstated in the instruction)"),
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
    print(f"duplicates_of_frozen_24={[n for n, rx, *_ in CASES if rx in frozen]}")
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
