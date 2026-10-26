#!/usr/bin/env python3
"""fixture_extra.py — F38AnchorFix. Breadth probes on the D3 binding, tip vs round-37 copy.

Cases (each rewrites one SOURCES.md row in the scratch clone's working tree, then runs both
counters, then restores the pristine bytes):

  E  S111 anchor = S108 digest's 8-hex prefix + '…'      cross-row abbreviation
  F  S111 anchor <- S108 digest, extra regex-log URL in the ANCHOR cell (not the scope cell)
  G  S070 anchor <- S105 digest                          cross-row on a provenance-row binding
  H  S111 anchor = S108 digest's UPPERCASE form          cross-row + case
  I  S111 anchor <- S108 digest, erratum for S111 citing it  erratum laundering probe
     (I writes the erratum line into the working-tree copy of corpus/lessons/round-38.md, which
      load_errata reads for committed lesson paths; restored afterwards)
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
S108 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
S105 = "44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582"
REGEXLOG_URL = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
                "2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py")


def run(cmd: list[str], cwd: pathlib.Path) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, "\n".join(ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip())


def set_anchor(text: str, sid: str, token_text: str, extra_anchor_text: str = "") -> tuple[str, str]:
    rows = text.splitlines()
    for i, line in enumerate(rows):
        if not line.lstrip().startswith("| " + sid + " |"):
            continue
        parts = [c.strip() for c in line.strip().strip("|").split("|")]
        assert len(parts) == 11, (sid, len(parts))
        before = parts[5]
        parts[5] = "sha256 " + token_text + extra_anchor_text
        rows[i] = "| " + " | ".join(parts) + " |"
        return "\n".join(rows) + "\n", f"{sid} anchor {before[:120]!r} -> {parts[5]!r}"
    raise SystemExit("row not found: " + sid)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--tip", required=True)
    ap.add_argument("--old", required=True)
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    src = lane / "corpus/SOURCES.md"
    lesson = lane / "corpus/lessons/round-38.md"
    pristine, pristine_lesson = src.read_text(encoding="utf-8"), lesson.read_text(encoding="utf-8")
    d0 = hashlib.sha256(pristine.encode()).hexdigest()
    cases = [
        ("E", lambda: set_anchor(pristine, "S111", S108[:8], "…")),
        ("F", lambda: set_anchor(pristine, "S111", S108, " " + REGEXLOG_URL)),
        ("G", lambda: set_anchor(pristine, "S070", S105)),
        ("H", lambda: set_anchor(pristine, "S111", S108.upper())),
    ]
    try:
        for name, mk in cases:
            text, desc = mk()
            src.write_text(text, encoding="utf-8")
            try:
                t_rc, t_out = run([sys.executable, a.tip, "--lane", "."], lane)
                o_rc, o_out = run([sys.executable, a.old, "--lane", "."], lane)
            finally:
                src.write_text(pristine, encoding="utf-8")
            print(f"\n=== FIXTURE {name} | {desc}")
            for label, rc, out in (("TIP", t_rc, t_out), ("OLD", o_rc, o_out)):
                print(f"{label} exit={rc}")
                for ln in out.splitlines():
                    print(f"{label} | {ln}")
        # I: erratum laundering for a cross-row anchor
        text, desc = set_anchor(pristine, "S111", S108)
        src.write_text(text, encoding="utf-8")
        lesson.write_text(pristine_lesson.rstrip("\n") + "\n\nErratum (round 38): S111 anchor sha256 "
                          + S108 + " is another row's digest; the capture's digest is sha256 "
                          + S108 + "\n", encoding="utf-8")
        try:
            t_rc, t_out = run([sys.executable, a.tip, "--lane", "."], lane)
            o_rc, o_out = run([sys.executable, a.old, "--lane", "."], lane)
        finally:
            src.write_text(pristine, encoding="utf-8")
            lesson.write_text(pristine_lesson, encoding="utf-8")
        print(f"\n=== FIXTURE I | {desc} + erratum line naming S108's digest for S111")
        for label, rc, out in (("TIP", t_rc, t_out), ("OLD", o_rc, o_out)):
            print(f"{label} exit={rc}")
            for ln in out.splitlines():
                print(f"{label} | {ln}")
    finally:
        src.write_text(pristine, encoding="utf-8")
        lesson.write_text(pristine_lesson, encoding="utf-8")
    print(f"\nRESTORED sources sha256={hashlib.sha256(src.read_bytes()).hexdigest()} equal="
          f"{hashlib.sha256(src.read_bytes()).hexdigest() == d0}")
    print(f"RESTORED lesson bytes_equal={lesson.read_text(encoding='utf-8') == pristine_lesson}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
