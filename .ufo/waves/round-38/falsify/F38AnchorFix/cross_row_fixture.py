#!/usr/bin/env python3
"""cross_row_fixture.py — F38AnchorFix (kengaku round 38, wave 2 falsify).

Fixture generator for `plans/anchor_digest_check.py` (D3 fix, landing tip 8c7422d7). It rewrites
exactly ONE anchor cell of `corpus/SOURCES.md` in a scratch clone (working tree only; no git
mutation) so that the row carries another row's real committed digest, then runs the tip copy and
the round-37 copy (`e0a37853:plans/anchor_digest_check.py`) against the same tree.

Usage:
  python3 cross_row_fixture.py --lane <scratch clone> --tip <tip check.py> --old <round-37 check.py>

Fixtures (each run against both counters, pristine tree restored between them):
  CONTROL  pristine SOURCES.md                                   (no mutation)
  A        S111 anchor <- S108 digest (345c3bd0…)   round-37 M4b/M5 shape, cross-task
  B        S115 anchor <- S108 digest (345c3bd0…)   round-38 row, cross-task
  C        S113 anchor <- S111 digest (526aee3d…)   same task dir, other capture file
  D        S111 row + a second pinned regex-log URL, anchor <- S108 digest   (locator-add probe)
Exit 0 always: the fixture reports, it does not judge. Receipt text goes to stdout.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import subprocess
import sys

ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
TOKEN = re.compile(r"sha256[ \t]+`?([0-9A-Fa-f]+)`?")
ANCHOR = 5
NCELLS = 11
SOURCES = "corpus/SOURCES.md"
S108 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
S111 = "526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37"
REGEXLOG_URL = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
                "2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py")


def cells(line: str) -> list[str]:
    return line.strip().strip("|").split("|")


def rebuild(parts: list[str]) -> str:
    assert len(parts) == NCELLS, f"cells={len(parts)} expected={NCELLS}"
    return "| " + " | ".join(c.strip() for c in parts) + " |"


def edit_row(text: str, sid: str, digest: str | None, add_url: str | None) -> tuple[str, str]:
    """Return (new text, one-line description of the applied mutation)."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = ROW.match(line)
        if not m or m.group(1) != sid:
            continue
        parts = cells(line)
        before = parts[ANCHOR].strip()
        if digest is not None:
            parts[ANCHOR], n = TOKEN.subn("sha256 " + digest, parts[ANCHOR], count=1)
            assert n == 1, f"{sid}: no sha256 token in anchor cell"
        if add_url is not None:
            assert add_url not in parts[4]
            parts[4] = parts[4].rstrip() + " (also " + add_url + ")"
        lines[i] = rebuild(parts)
        return "\n".join(lines) + "\n", f"{sid} anchor {before[:200]!r} -> " \
                                         f"{parts[ANCHOR].strip()[:200]!r}" + \
                                         (f" + second URL in scope cell" if add_url else "")
    raise SystemExit(f"row {sid} not found")


def run(cmd: list[str], cwd: pathlib.Path) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    return r.returncode, out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--tip", required=True)
    ap.add_argument("--old", required=True)
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    src = lane / SOURCES
    pristine = src.read_text(encoding="utf-8")
    orig_hash = __import__("hashlib").sha256(pristine.encode()).hexdigest()
    print(f"LANE {lane}")
    print(f"PRISTINE {SOURCES} sha256={orig_hash} bytes={len(pristine)}")

    fixtures = [
        ("CONTROL", None, None, None),
        ("A", "S111", S108, None),
        ("B", "S115", S108, None),
        ("C", "S113", S111, None),
        ("D", "S111", S108, REGEXLOG_URL),
    ]
    for name, sid, digest, url in fixtures:
        text, desc = pristine, "no mutation"
        if sid is not None:
            text, desc = edit_row(pristine, sid, digest, url)
        src.write_text(text, encoding="utf-8")
        try:
            t_rc, t_out = run([sys.executable, a.tip, "--lane", "."], lane)
            o_rc, o_out = run([sys.executable, a.old, "--lane", "."], lane)
        finally:
            src.write_text(pristine, encoding="utf-8")
        assert src.read_text(encoding="utf-8") == pristine, "pristine restore failed"
        print(f"\n=== FIXTURE {name} | {desc}")
        for label, rc, out in (("TIP  ", t_rc, t_out), ("OLD  ", o_rc, o_out)):
            tail = [ln for ln in out.splitlines() if ln.strip()]
            print(f"{label} exit={rc}")
            for ln in tail:
                print(f"{label} | {ln}")
    print(f"\nRESTORED {SOURCES} sha256={__import__('hashlib').sha256(src.read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
