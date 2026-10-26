#!/usr/bin/env python3
"""probe_extra.py — F39AnchorFix falsification driver for the landed anchor check.

Cases mutate the scratch clone's working tree only; every case restores HEAD bytes and asserts
sha256 equality. Usage: probe_extra.py --lane DIR --landed PATH --frozen PATH [--verbose]
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

SID = "S111"
S108 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
S111 = "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37"
S110_BAD63 = "4f7ac05e70cf922ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c"
S110_GOOD = "4f7ac05e70cf9220ea0f1e5a052c5f908cd0fa884e847d80b0bd51bae2e96f9c"
URL_RAW = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
           "2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py")
ANCHOR_HEAD = " | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, tests/test_outputs.py:9-13"
ERRATUM_LESSON = "corpus/lessons/round-38.md"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def row_line(text: str, sid: str) -> tuple[int, str]:
    for i, line in enumerate(text.splitlines()):
        if re.match(r"^ {0,3}\|\s*" + sid + r"\s*\|", line):
            return i, line
    raise SystemExit(f"no row {sid}")


def edit_row(lane: pathlib.Path, sid: str, fn) -> str:
    p = lane / "corpus/SOURCES.md"
    lines = p.read_text(encoding="utf-8").split("\n")
    i, line = row_line("\n".join(lines), sid)
    new = fn(line)
    lines[i] = new
    p.write_text("\n".join(lines), encoding="utf-8")
    return new


def edit_lesson(lane: pathlib.Path, rel: str, fn) -> None:
    p = lane / rel
    p.write_text(fn(p.read_text(encoding="utf-8")), encoding="utf-8")


# --- multi-locator cases on S111 -------------------------------------------------------------
def d_rows(line):
    """append the second locator to the S111 scope cell, exactly as wave-1 case D/D2 does."""
    return line.replace(ANCHOR_HEAD, f" {URL_RAW}{ANCHOR_HEAD}")


def case_d_full(line):
    return d_rows(line).replace(S111, S108)


def case_d2(line):
    return d_rows(line).replace(f"; sha256 {S111}", f"; sha256 {S111}; sha256 {S108}")


def case_d2_abbrev(line):
    return d_rows(line).replace(f"; sha256 {S111}", f"; sha256 {S111}; sha256 {S108[:8]}…")


def case_dup(line):
    return d_rows(line).replace(f"; sha256 {S111}", f"; sha256 {S111}; sha256 {S111}")


def case_glue_own(line):
    """GLUE-OWN: second locator glued to ';' with NO token for it; the row's own token stays."""
    return line.replace(ANCHOR_HEAD, f" {URL_RAW};{ANCHOR_HEAD}")


def case_d_erratum_line(line):
    return case_d_full(line)


def case_three(line):
    """D3: two extra locators (regex-log + build-pmars), one token only -> two unanchored."""
    b = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
         "2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars/tests/test_outputs.py")
    return d_rows(line).replace(f" {URL_RAW}{ANCHOR_HEAD}", f" {URL_RAW} {b}{ANCHOR_HEAD}")


def case_token_outside(line):
    out = d_rows(line)
    return out.replace(f"; sha256 {S111}", "").replace(
        f" {URL_RAW}{ANCHOR_HEAD}", f" {URL_RAW} sha256 {S111}{ANCHOR_HEAD}")


# --- single-capture regression cases on several rows ------------------------------------------
def tok_swap(target, new):
    return lambda line: line.replace(target, new)


def tok_trunc(target):
    return lambda line: line.replace(target, target[:-1])


def tok_upper(target):
    return lambda line: line.replace(target, target.upper())


def tok_abbrev(target):
    return lambda line: line.replace(f"sha256 {target}", f"sha256 {target[:8]}…")


def tok_delete(target):
    return lambda line: line.replace(f"; sha256 {target}", "")


CASES = [
    ("CONTROL", None, None),
    ("D", SID, case_d_full),
    ("D2", SID, case_d2),
    ("D2ABBREV", SID, case_d2_abbrev),
    ("DUP", SID, case_dup),
    ("GLUE-OWN", SID, case_glue_own),
    ("D3-THREE", SID, case_three),
    ("TOK-OUTSIDE", SID, case_token_outside),
    # single-capture regressions (round-38 behaviours)
    ("S111-SWAP108", SID, tok_swap(S111, S108)),
    ("S111-63HEX", SID, tok_trunc(S111)),
    ("S111-UPPER", SID, tok_upper(S111)),
    ("S111-ABBREV", SID, tok_abbrev(S111)),
    ("S111-DELETE", SID, tok_delete(S111)),
    ("S110-63HEX-EXEMPTED", "S110", None),
    ("S110-SWAP111", "S110", tok_swap(S110_BAD63, S111)),
    ("S036-ABBREV", "S036", None),
    ("S114-SWAP108", "S114", tok_swap(
        "c217d37253c89a71d6cc4d1c14f588c02ce49039cb1118dd3694150cf4c64193", S108)),
]


def run(tool: str, lane: pathlib.Path, verbose: bool):
    cmd = [sys.executable, tool, "--lane", str(lane)] + (["--verbose"] if verbose else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, [l for l in r.stdout.splitlines() if l.startswith("DEFECT")], \
        [l for l in r.stdout.splitlines() if l.startswith("rows=")], r.stderr


def summary(rc, defects, last, err):
    return {"exit": rc, "classes": sorted({re.search(r"class=(\S+)", d).group(1) for d in defects}),
            "defects": defects, "last": last[0] if last else "", "stderr": err.strip()}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--landed", required=True)
    ap.add_argument("--frozen", required=True)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    so = lane / "corpus/SOURCES.md"
    lesson = lane / ERRATUM_LESSON
    base = {p: sha(p) for p in (so, lesson, lane / "corpus/lessons/round-37.md")}
    print(f"LANE {lane} PRISTINE SOURCES sha256={base[so]}")
    for label, sid, fn in CASES:
        print(f"\n==== {label} ====")
        try:
            if fn is not None:
                new = edit_row(lane, sid, fn)
                print(f"MUTATION {sid}: {new[:200]}…")
            if label == "S110-63HEX-EXEMPTED":
                edit_lesson(lane, "corpus/lessons/round-37.md",
                            lambda t: "\n".join(l for l in t.split("\n")
                                                if not l.startswith("Erratum (round 37): S110 ")))
            for name, tool in (("LANDED", a.landed), ("FROZEN", a.frozen)):
                rc, defects, last, err = run(tool, lane, a.verbose)
                s = summary(rc, defects, last, err)
                print(f"{name} exit={s['exit']} classes={s['classes']} {s['last']}")
                for d in s["defects"]:
                    print(f"{name} | {d}")
                if s["stderr"]:
                    print(f"{name} ! {s['stderr']}")
        finally:
            for p, h in base.items():
                rel = p.relative_to(lane).as_posix()
                p.write_bytes(subprocess.run(["git", "-C", str(lane), "show", f"HEAD:{rel}"],
                                             capture_output=True).stdout)
                assert sha(p) == h, f"{rel} not restored"
            dirty = subprocess.run(["git", "-C", str(lane), "status", "--porcelain"],
                                   capture_output=True, text=True).stdout.strip()
            print(f"RESTORED status-lines={len(dirty.splitlines()) if dirty else 0}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
