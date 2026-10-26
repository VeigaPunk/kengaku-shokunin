#!/usr/bin/env python3
"""fixture_d_verbose.py — F38AnchorFix. Fixture D held open long enough to show the binding.

Applies the fixture-D mutation (S111 anchor <- S108's committed digest, plus a second pinned
regex-log URL appended to S111's scope cell; the row's original configure-git-webserver URL and
subject are untouched), then runs the tip check with --verbose, the binding probe, and the
round-37 copy, restoring the pristine file afterwards.

Usage: python3 fixture_d_verbose.py --lane <scratch clone> --tip <tip check.py> --old <old check.py>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
S108 = "345c3bd09ab6f6fe8c8361a58c0a47bf0a13b3fcb38a5ac7824e44ff855e8f72"
REGEXLOG_URL = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
                "2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py")


def load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(cmd: list[str], cwd: pathlib.Path) -> None:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    print(f"$ {' '.join(cmd)}   (cwd={cwd})  exit={r.returncode}")
    for ln in (r.stdout + r.stderr).splitlines():
        if ln.strip():
            print(f"| {ln}")
    print()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--tip", required=True)
    ap.add_argument("--old", required=True)
    a = ap.parse_args(argv)
    lane = pathlib.Path(a.lane).resolve()
    fix = load("crf", HERE / "cross_row_fixture.py")
    src = lane / "corpus/SOURCES.md"
    pristine = src.read_text(encoding="utf-8")
    digest0 = hashlib.sha256(pristine.encode()).hexdigest()
    text, desc = fix.edit_row(pristine, "S111", S108, REGEXLOG_URL)
    src.write_text(text, encoding="utf-8")
    try:
        print(f"FIXTURE D applied to corpus/SOURCES.md (pristine sha256={digest0})")
        print(f"MUTATION {desc}\n")
        run([sys.executable, a.tip, "--lane", ".", "--verbose"], lane)
        run([sys.executable, str(HERE / "probe_bind.py"), "--lane", ".",
             "--check", a.tip], lane)
        run([sys.executable, a.old, "--lane", "."], lane)
    finally:
        src.write_text(pristine, encoding="utf-8")
    print(f"RESTORED corpus/SOURCES.md sha256={hashlib.sha256(src.read_bytes()).hexdigest()} "
          f"equal={hashlib.sha256(src.read_bytes()).hexdigest() == digest0}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
