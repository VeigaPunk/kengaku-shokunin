#!/usr/bin/env python3
"""Diagnostic (read-only) for seat R36CritUnenforced: show the grader's full `got` list per case.

Loads the pinned grader, replaces only the module-level `re` NAME with a proxy that records the
findall result while delegating to the real `re`, and prints expected vs got. The grader's own
log_text and expected_dates are used verbatim; nothing in the lane is written.
"""
import hashlib
import importlib.util
import pathlib
import re as real_re
import sys
import tempfile

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
GRADER = LANE / "corpus/evidence/round36/tb2-regex-log/test_outputs.py"
PIN_SHA = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"

OCT = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
NA_B = r"(?<![A-Za-z0-9])"
NA_A = r"(?![A-Za-z0-9])"
IP = NA_B + rf"(?:{OCT}\.){{3}}{OCT}" + NA_A
BASE = r"\d{4}-\d{2}-\d{2}"


def line(body=BASE, ipx=IP, left=NA_B, right=NA_A):
    return rf"^(?=.*{ipx}).*{left}({body}){right}"


def got_for(pattern):
    spec = importlib.util.spec_from_file_location("g", GRADER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rec = {}

    class Shim:
        MULTILINE = real_re.MULTILINE
        error = real_re.error

        @staticmethod
        def findall(pat, text, flags=0):
            out = real_re.findall(pat, text, flags)
            rec["got"] = out
            rec["text"] = text
            return out

        @staticmethod
        def compile(pat, flags=0):
            return real_re.compile(pat, flags)

    mod.re = Shim
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "regex.txt"
        p.write_text(pattern)
        mod.Path = lambda _a, _p=p: _p
        try:
            mod.test_regex_matches_dates()
            verdict = "pass"
        except AssertionError:
            verdict = "fail"
    return verdict, rec.get("got")


if __name__ == "__main__":
    src = GRADER.read_bytes()
    assert hashlib.sha256(src).hexdigest() == PIN_SHA, "grader digest mismatch"
    only = sys.argv[1] if len(sys.argv) > 1 else None
    sys.path.insert(0, str(LANE / ".ufo/waves/round-36/build/R36CritUnenforced"))
    # v1 table (fixed prefix omitted on purpose: this is the diagnostic of the v1 witnesses)
    import extra_cases as v1
    for name, rx, pred, *_ in v1.CASES:
        if only and only not in name:
            continue
        verdict, got = got_for(rx)
        print(f"{name} predicted={pred} observed={verdict}")
        print(f"  got={got}")
