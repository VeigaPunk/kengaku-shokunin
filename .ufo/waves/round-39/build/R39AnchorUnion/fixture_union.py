#!/usr/bin/env python3
"""fixture_union.py — round-39 R39AnchorUnion fixture driver.

Mutates ONLY the working tree of a scratch clone (`corpus/SOURCES.md`, plus for M a working-tree lesson
line), runs a list of tools on the mutated tree, restores the pristine bytes, and prints one receipt
block per (case, tool). No commit, no index, no git state change.

Usage: python3 fixture_union.py --lane DIR --tool LABEL=PATH [--tool LABEL=PATH ...] [--cases D,F,...]
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
SID = "S111"
S108_DIGEST = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
S111_DIGEST = "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37"
URL_REGEX_LOG = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
                 "2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py")
# the scope cell ends where the anchor cell begins; S111's anchor cell head is unique in its row
ANCHOR_HEAD = " | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, tests/test_outputs.py:9-13"
ERRATUM_LESSON = "corpus/lessons/round-38.md"


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_line(text: str, sid: str) -> tuple[int, str]:
    for i, line in enumerate(text.splitlines()):
        m = ROW.match(line)
        if m and m.group(1) == sid:
            return i, line
    raise SystemExit(f"no row {sid}")


def case_d(line: str) -> str:
    """D: scope cell gains the regex-log URL; the anchor carries THAT locator's real digest."""
    assert line.count(ANCHOR_HEAD) == 1
    line = line.replace(ANCHOR_HEAD, f" {URL_REGEX_LOG}{ANCHOR_HEAD}")
    return line.replace(S111_DIGEST, S108_DIGEST)


def case_f(line: str) -> str:
    """F: the same second URL, in the anchor cell instead of the scope cell."""
    line = line.replace(f"; sha256 {S111_DIGEST}", f" {URL_REGEX_LOG} ; sha256 {S111_DIGEST}")
    return line.replace(S111_DIGEST, S108_DIGEST)


def case_d2(line: str) -> str:
    """D2 (green control): two locators, one token each — a coherent multi-capture row."""
    line = line.replace(ANCHOR_HEAD, f" {URL_REGEX_LOG}{ANCHOR_HEAD}")
    return line.replace(f"; sha256 {S111_DIGEST}", f"; sha256 {S111_DIGEST}; sha256 {S108_DIGEST}")


def case_dup(line: str) -> str:
    """DUP: two locators, both tokens are the row's OWN digest -> the other capture is unanchored."""
    line = line.replace(ANCHOR_HEAD, f" {URL_REGEX_LOG}{ANCHOR_HEAD}")
    return line.replace(f"; sha256 {S111_DIGEST}", f"; sha256 {S111_DIGEST}; sha256 {S111_DIGEST}")


def case_a(line: str) -> str:
    """A (round-38 shape): anchor <- S108's digest, no second locator."""
    return line.replace(S111_DIGEST, S108_DIGEST)


def case_l(line: str) -> str:
    """L (presence limit): the anchor token is deleted, nothing else changed."""
    return line.replace(f"; sha256 {S111_DIGEST}", "")


def case_glue(line: str) -> str:
    """GLUE (adjacent quirk): F written with no space before `;`, so the URL scanner eats the `;`."""
    line = line.replace(f"; sha256 {S111_DIGEST}", f" {URL_REGEX_LOG}; sha256 {S111_DIGEST}")
    return line.replace(S111_DIGEST, S108_DIGEST)


CASES = {"D": case_d, "F": case_f, "D2": case_d2, "DUP": case_dup, "A": case_a, "L": case_l,
         "GLUE": case_glue}


def edit_row(lane: pathlib.Path, sid: str, fn) -> str:
    p = lane / "corpus/SOURCES.md"
    text = p.read_text(encoding="utf-8")
    i, line = row_line(text, sid)
    new = fn(line)
    lines = text.splitlines()
    lines[i] = new
    p.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    return new


def run(tool: str, lane: pathlib.Path, verbose: bool):
    cmd = [sys.executable, tool, "--lane", str(lane)] + (["--verbose"] if verbose else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout.rstrip("\n"), r.stderr.rstrip("\n")


def show(label: str, tool: str, rc: int, out: str, err: str, verbose: bool) -> None:
    print(f"{label} exit={rc}")
    if verbose:
        for line in out.splitlines():
            print(f"{label} | {line}")
    else:
        picks = [l for l in out.splitlines() if "DEFECT" in l or l.startswith(("rows=", "EVIDENCE"))]
        for line in picks:
            print(f"{label} | {line}")
    if err:
        for line in err.splitlines():
            print(f"{label} ! {line}")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--tool", action="append", required=True, help="LABEL=PATH")
    ap.add_argument("--cases", default="CONTROL,D,F,D2,DUP,A,L,M")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    tools = [t.split("=", 1) for t in a.tool]
    so = lane / "corpus/SOURCES.md"
    lesson = lane / ERRATUM_LESSON
    base_src, base_lesson = sha(so), sha(lesson)
    top = subprocess.run(["git", "-C", str(lane), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    print(f"LANE toplevel={top}")
    print(f"PRISTINE corpus/SOURCES.md sha256={base_src}")
    print(f"PRISTINE {ERRATUM_LESSON} sha256={base_lesson}")
    dirty0 = subprocess.run(["git", "-C", str(lane), "status", "--porcelain"],
                            capture_output=True, text=True).stdout.strip()
    print(f"PRISTINE git status --porcelain lines={len(dirty0.splitlines()) if dirty0 else 0}")
    for case in a.cases.split(","):
        print(f"\n==== CASE {case} ====")
        try:
            if case == "CONTROL":
                pass
            elif case == "M":
                edit_row(lane, SID, case_a)
                with lesson.open("a", encoding="utf-8") as fh:
                    fh.write(f"\nErratum (round 37): {SID} anchor sha256 {S108_DIGEST} is wrong; "
                             f"the correction is sha256 {S108_DIGEST}\n")
            else:
                new = edit_row(lane, SID, CASES[case])
                print(f"MUTATION {SID} -> {new.strip()}")
            for label, tool in tools:
                rc, out, err = run(tool, lane, a.verbose)
                show(label, tool, rc, out, err, a.verbose)
        finally:
            for p, base in ((so, base_src), (lesson, base_lesson)):
                rel = p.relative_to(lane).as_posix()
                p.write_bytes(subprocess.run(["git", "-C", str(lane), "show", f"HEAD:{rel}"],
                                             capture_output=True).stdout)
                assert sha(p) == base, f"{rel} not restored"
            dirty = subprocess.run(["git", "-C", str(lane), "status", "--porcelain"],
                                   capture_output=True, text=True).stdout.strip()
            print(f"RESTORED corpus/SOURCES.md sha256={sha(so)} "
                  f"git status --porcelain lines={len(dirty.splitlines()) if dirty else 0}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
