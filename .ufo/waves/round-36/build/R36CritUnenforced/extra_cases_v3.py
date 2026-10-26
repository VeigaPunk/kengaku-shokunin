#!/usr/bin/env python3
"""Supplementary candidates v3 (OUTSIDE the frozen C2 predicate) — seat R36CritUnenforced.

v2's V06 mixed two features (it dropped the month RANGE check while widening the month field), so it
failed on the N lines 2023-13-05 and 2022-00-15 — a seat-side witness-construction defect, not a
grader finding (diag `got` shows both). V18 keeps the range check and adds only the unreachable
3-digit month alternative. V19 varies the IPv4 separator set. Predictions written before the run.

Run: python3 .ufo/waves/round-36/build/R36CritUnenforced/extra_cases_v3.py --lane <lane root>
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
BASE = rf"\d{{4}}-{MONTH}-{DAY}"


def line(body=BASE, ipx=IP, left=NA_B, right=NA_A):
    return rf"^(?=.*{ipx}).*{left}({body}){right}"


CASES = [
    ("V18-month-three-digit-range-kept", line(rf"\d{{4}}-(?:{MONTH}|\d{{3}})-{DAY}"), "pass",
     "format YYYY-MM-DD: MM is exactly two digits; a 3-digit month branch must not be accepted",
     "new: wide month width with the range check kept (the 3-digit branch is unreachable in the log)"),
    ("V19-ip-dash-separators",
     line(ipx=NA_B + rf"(?:{OCT}[.\-]){{3}}{OCT}" + NA_A), "pass",
     "IPv4 addresses use normal decimal notation: a dash-separated '1-2-3-4' is not an IPv4",
     "new: IPv4 separator set loosened to [-.] (unreachable in the log)"),
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
    for name, rx, pred, req, note in CASES:
        obs, msg = probe.run_grader(gpath, rx, "file")
        ok = obs == pred
        mism += not ok
        print(f"case={name} predicted={pred} observed={obs} match={'yes' if ok else 'NO'} "
              f"assertion={msg!r} requirement={req!r} novelty={note!r}")
    print(f"cases={len(CASES)} mismatches={mism}")
    return 0 if mism == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
