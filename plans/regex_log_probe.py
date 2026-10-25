#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `regex-log` grader (round 36, C2).

Loads the captured `tests/test_outputs.py` (terminal-bench-2 @ 2fd12b88) from the lane's committed
capture, refuses unless its SHA-256 equals the pinned digest, and runs its single test function on a
frozen table of candidate `/app/regex.txt` contents. Each case names the `instruction.md`
requirement it exercises and a prediction (pass/fail) written from a static reading of the grader
and the instruction BEFORE the first run (the reading also included the task's oracle `solve.sh`,
captured beside the grader). Output is deterministic; the C2 counter re-runs it and byte-compares
the committed receipt. A case whose observation differs from its prediction prints `match=NO` and
is counted in `mismatches`; predictions are never edited after the first run.

The grader imports only `re` and `pathlib`. Run as:
  python3 plans/regex_log_probe.py --lane .
This executes scoring code on synthetic candidate regexes only: no model, no container, no task
certification.
"""
import argparse
import hashlib
import importlib.util
import pathlib
import sys
import tempfile

PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
GRADER_REL = "corpus/evidence/round36/tb2-regex-log/test_outputs.py"
GRADER_SHA256 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"

OCT = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"          # 0-255, no leading zero
OCT_LZ = r"(?:25[0-5]|2[0-4]\d|[01]?\d?\d)"            # 0-255, leading zeros allowed
OCT_ANY = r"\d{1,3}"                                   # no range check
NOT_ALNUM_B = r"(?<![A-Za-z0-9])"
NOT_ALNUM_A = r"(?![A-Za-z0-9])"
MONTH = r"(?:0[1-9]|1[0-2])"
DAY = r"(?:0[1-9]|[12]\d|3[01])"
# month-aware day ranges, February up to 29 as the instruction says
DATE_BODY_STRICT = (r"\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])"
                    r"|(?:0[469]|11)-(?:0[1-9]|[12]\d|30)|02-(?:0[1-9]|[12]\d))")
DATE_BODY_FEB28 = (r"\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])"
                   r"|(?:0[469]|11)-(?:0[1-9]|[12]\d|30)|02-(?:0[1-9]|1\d|2[0-8]))")
EXPECTED = ("2025-01-09", "2024-11-01", "2020-01-01", "2019-06-15", "2018-06-06",
            "2017-03-03", "2016-12-31", "2024-11-11", "1999-03-05")


def ip(octet=OCT, left=True, right=True):
    return (NOT_ALNUM_B if left else "") + rf"(?:{octet}\.){{3}}{octet}" + (NOT_ALNUM_A if right else "")


def date(body=rf"\d{{4}}-{MONTH}-{DAY}", left=NOT_ALNUM_B, right=NOT_ALNUM_A):
    return f"{left}({body}){right}"


def line_rx(ipx, datex, lazy=False, ip_first=False):
    star = ".*?" if lazy else ".*"
    if ip_first:
        return rf"^.*{ipx}{star}{datex}"
    return rf"^(?=.*{ipx}){star}{datex}"


def build_cases():
    base_ip = ip()
    out = []

    def add(name, regex, pred, req, mode="file"):
        out.append((name, regex, pred, req, mode))

    add("reference-lenient-days", line_rx(base_ip, date()), "pass",
        "all bullets with day 01-31 in every month (no month-length check)")
    add("reference-month-aware", line_rx(base_ip, date(DATE_BODY_STRICT)), "pass",
        "February up to 29, 30-day months capped at 30")
    add("first-date-only", line_rx(base_ip, date(), lazy=True), "fail",
        "match only the last date in a line")
    add("no-ip-condition", rf"^.*{date()}", "fail", "only lines that contain an IPv4 address")
    add("ip-octets-unbounded", line_rx(ip(OCT_ANY), date()), "fail", "valid IPv4 range 0-255")
    add("ip-leading-zeros-allowed", line_rx(ip(OCT_LZ), date()), "pass",
        "IPv4 octets carry no leading zeros (oracle itself allows them)")
    add("month-13-allowed", line_rx(base_ip, date(r"\d{4}-(?:0[1-9]|1[0-9])-" + DAY)), "fail",
        "month 01-12")
    add("month-00-allowed", line_rx(base_ip, date(r"\d{4}-(?:0[0-9]|1[0-2])-" + DAY)), "fail",
        "month 01-12 (00 rejected)")
    add("day-32-allowed", line_rx(base_ip, date(rf"\d{{4}}-{MONTH}-(?:0[1-9]|[12]\d|3\d)")), "fail",
        "day 01-31 (32 rejected)")
    add("day-00-allowed", line_rx(base_ip, date(rf"\d{{4}}-{MONTH}-(?:0[0-9]|[12]\d|3[01])")), "fail",
        "day 01-31 (00 rejected)")
    add("date-no-left-boundary", line_rx(base_ip, date(left="")), "fail",
        "dates not immediately preceded by an alphanumeric")
    add("date-no-right-boundary", line_rx(base_ip, date(right="")), "fail",
        "dates not immediately followed by an alphanumeric")
    add("date-boundary-letters-only", line_rx(base_ip, date(left=r"(?<![A-Za-z])", right=r"(?![A-Za-z])")), "pass",
        "dates not adjacent to an alphanumeric (digit adjacency, e.g. 1134-12-1234, is unobserved)")
    add("ip-no-left-boundary", line_rx(ip(left=False), date()), "fail",
        "IPv4 not immediately preceded by an alphanumeric")
    add("ip-no-right-boundary", line_rx(ip(right=False), date()), "fail",
        "IPv4 not immediately followed by an alphanumeric")
    add("ip-before-date-only", line_rx(base_ip, date(), ip_first=True), "fail",
        "a line qualifies when the IPv4 is anywhere in it, including after the date")
    add("hardcoded-expected-dates", "|".join(EXPECTED), "pass",
        "none: the nine expected strings, no pattern logic (the test log is fixed and visible in the test file)")
    add("year-any-digit-count", line_rx(base_ip, date(rf"\d{{2,6}}-{MONTH}-{DAY}")), "pass",
        "YYYY is four digits (other widths are unobserved)")
    add("empty-pattern", "", "fail", "the regex file holds a pattern")
    add("invalid-regex", "(", "fail", "the regex compiles")
    add("regex-file-absent", None, "fail", "the regex is saved in /app/regex.txt", mode="absent")
    add("extra-capture-group", rf"^(?=.*({base_ip})).*{date()}", "fail",
        "findall returns the dates only (an extra capture group yields tuples)")
    add("padded-file", "  " + line_rx(base_ip, date()) + " \n\n", "pass",
        "the file is read and stripped")
    add("feb-29-rejected", line_rx(base_ip, date(DATE_BODY_FEB28)), "pass",
        "February can have up to 29 days (the permitting side is unobserved)")
    return out


def run_grader(mod_path, regex, mode):
    spec = importlib.util.spec_from_file_location("tb2_regex_log_grader", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / ("regex.txt" if mode == "file" else "absent-regex.txt")
        if mode == "file":
            p.write_text(regex)
        real = pathlib.Path
        mod.Path = lambda _arg: real(p)  # the grader hard-codes /app/regex.txt
        try:
            mod.test_regex_matches_dates()
            return "pass", "-"
        except AssertionError as e:
            first = (str(e).splitlines() or ["AssertionError"])[0]
            return "fail", first if len(first) <= 160 else first[:157] + "..."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--dry", action="store_true", help="print the frozen cases without running the grader")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane)
    gpath = lane / GRADER_REL
    src = gpath.read_bytes()
    digest = hashlib.sha256(src).hexdigest()
    if digest != GRADER_SHA256:
        print(f"REFUSE grader digest {digest} != pinned {GRADER_SHA256}")
        return 2
    cases = build_cases()
    if a.dry:
        for name, regex, pred, req, mode in cases:
            print(f"case={name} predicted={pred} mode={mode} regex={regex!r} requirement={req!r}")
        print(f"cases={len(cases)} predicted_pass={sum(c[2] == 'pass' for c in cases)}")
        return 0
    print(f"grader={GRADER_REL} sha256={digest} pin={PIN}")
    mism = 0
    npass = 0
    for name, regex, pred, req, mode in cases:
        obs, msg = run_grader(gpath, regex, mode)
        ok = obs == pred
        mism += not ok
        npass += obs == "pass"
        print(f"case={name} predicted={pred} observed={obs} match={'yes' if ok else 'NO'} "
              f"assertion={msg!r} requirement={req!r}")
    print(f"cases={len(cases)} observed_pass={npass} observed_fail={len(cases) - npass} mismatches={mism}")
    return 0 if mism == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
