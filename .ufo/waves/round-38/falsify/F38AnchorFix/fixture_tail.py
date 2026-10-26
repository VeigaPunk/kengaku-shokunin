#!/usr/bin/env python3
"""fixture_tail.py — F38AnchorFix. Two last breadth probes: row-path binding and an unbound row.

  J  S036 anchor <- S105 digest        cross-row onto a row-path (explicit lane path) binding
  K  S001 anchor <- S108 digest        cross-row onto a row that binds no capture at all

Each rewrite is applied to the scratch clone's working tree only and restored afterwards.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import subprocess
import sys

S108 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
S105 = "44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582"


def set_anchor(text: str, sid: str, digest: str) -> tuple[str, str]:
    rows = text.splitlines()
    for i, line in enumerate(rows):
        if not line.lstrip().startswith("| " + sid + " |"):
            continue
        parts = [c.strip() for c in line.strip().strip("|").split("|")]
        assert len(parts) == 11, (sid, len(parts))
        before = parts[5]
        parts[5] = "sha256 " + digest
        rows[i] = "| " + " | ".join(parts) + " |"
        return "\n".join(rows) + "\n", f"{sid} anchor {before[:110]!r} -> 'sha256 {digest}'"
    raise SystemExit("row not found: " + sid)


def run(cmd: list[str], cwd: pathlib.Path) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, "\n".join(ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip())


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--tip", required=True)
    ap.add_argument("--old", required=True)
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    src = lane / "corpus/SOURCES.md"
    pristine = src.read_text(encoding="utf-8")
    d0 = hashlib.sha256(pristine.encode()).hexdigest()
    try:
        for name, sid, dig in (("J", "S036", S105), ("K", "S001", S108)):
            text, desc = set_anchor(pristine, sid, dig)
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
    finally:
        src.write_text(pristine, encoding="utf-8")
    print(f"\nRESTORED sha256={hashlib.sha256(src.read_bytes()).hexdigest()} "
          f"equal={hashlib.sha256(src.read_bytes()).hexdigest() == d0}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
