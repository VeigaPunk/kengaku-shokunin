#!/usr/bin/env python3
"""ReviewerC286 Q2 fixture — can round86_c2_repin.py pass with a hand-moved pin?

Four scenarios, each an extracted tree from BASE 88651a72 (so PROVINCE.md's
### Adjacent genuinely sits at 151) edited in a way that puts the pin and the
pointer at a NON-derived, wrong line:

  A  shonen 129 -> 999, pin hand-moved 129 -> 999 (both agree, both wrong)
  B  shonen unchanged at 129, pin hand-moved 129 -> 999 (pin follows nothing)
  C  pin hand-moved to 151 only (pointer-only control, rerun locally)
  D  shonen 129 -> 151, pin left at 129 (pin-only control, rerun locally)

The question the seat asks: does P1-derive read a line from the bytes (so a
tree whose PROVINCE.md was *not* re-derived defeats it), or does the counter
pass whenever pin/pointer merely agree with each other?
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
BASE = "88651a72ef112ed9f5361e1c8c197babec691f96"
COUNTER = "plans/round86_c2_repin.py"
STALE = 129
WRONG = 999

ROOTS = {
    "A-both-999": ("shonen", "pin"),
    "B-pin-999-only": ("pin",),
    "C-pin-151-only": ("pin-151",),
    "D-shonen-151-only": ("shonen-151",),
}


def tree(work: Path, name: str) -> Path:
    root = work / name
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "archive", "--format=tar", BASE], cwd=LANE,
                   capture_output=True, check=True)
    arc = subprocess.run(["git", "-C", str(LANE), "archive", "--format=tar", BASE],
                         capture_output=True, check=True)
    subprocess.run(["tar", "-x", "-C", str(root)], input=arc.stdout, check=True)
    return root


def edit(root: Path, target: str, old: str, new: str) -> None:
    path = root / target
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} missing in {target}"
    (path.parent / (path.name + ".next")).write_text(
        text.replace(old, new, 1), encoding="utf-8")
    (path.parent / (path.name + ".next")).replace(path)


def main() -> int:
    work = Path(tempfile.mkdtemp(prefix="c2attack-", dir=Path(sys.argv[1])))
    failures = 0
    for name, edits in ROOTS.items():
        root = tree(work, name)
        derived = None
        lines = (root / "PROVINCE.md").read_text(encoding="utf-8").splitlines()
        derived = next(i + 1 for i, l in enumerate(lines) if l.strip() == "### Adjacent")
        # apply edits
        if "shonen" in edits:
            edit(root, "SHONEN.md", f"PROVINCE.md:{STALE}", f"PROVINCE.md:{WRONG}")
        if "shonen-151" in edits:
            edit(root, "SHONEN.md", f"PROVINCE.md:{STALE}", f"PROVINCE.md:{derived}")
        if "pin" in edits:
            edit(root, "plans/state_check.py",
                 f'(4, "PROVINCE.md:{STALE}", {STALE}, "### Adjacent", None),',
                 f'(4, "PROVINCE.md:{WRONG}", {WRONG}, "### Adjacent", None),')
        if "pin-151" in edits:
            edit(root, "plans/state_check.py",
                 f'(4, "PROVINCE.md:{STALE}", {STALE}, "### Adjacent", None),',
                 f'(4, "PROVINCE.md:{derived}", {derived}, "### Adjacent", None),')
        # run the frozen counter bytes against this fixture tree
        out = subprocess.run(
            [sys.executable, "-I", "-B", str(LANE / COUNTER),
             "--lane", str(root), "--root", str(root),
             "--work", str(work / f"{name}-work"), "--no-selftest"],
            capture_output=True, text=True, timeout=600)
        target = None
        verdict = None
        for line in out.stdout.splitlines():
            if line.startswith("TARGET "):
                target = line
            if line.startswith("PREDICATE "):
                verdict = line
        reached = verdict is not None and "pass" in verdict
        print(f"== {name} (### Adjacent at {derived}) ==")
        print(target)
        print(verdict)
        print(f"exit={out.returncode} reached={reached}")
        print()
        if reached:
            print(f"!!!! fixture {name} REACHED THE TARGET on a hand-moved pin")
            failures += 1
    print(f"FIXTURES failed={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
