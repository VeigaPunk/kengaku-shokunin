#!/usr/bin/env python3
"""R86-C2 counter — the lane's standing self-assessment mismatch, repaired by derivation.

The lane's own offline state check (`plans/state_check.py --summary`) compares frozen
self-assessment assertions against the repo.  At the round-85 tip exactly one assertion is
red: `P3c.box.4.pointer.1`, because `SHONEN.md` box 4 points at `PROVINCE.md:129` and the
instrument's pin freezes the same line, while `### Adjacent` moved to a later line as
PROVINCE.md grew.  This counter measures the repair, not the edit:

  P1-derive    `### Adjacent` occurs exactly once in PROVINCE.md and its line is derived
               from the measured bytes (never from a constant)
  P2-shonen    SHONEN.md box 4's first evidence pointer is `PROVINCE.md:<derived line>`
  P3-pin       the box-4 entry of `P3C_PINS` in plans/state_check.py carries the same
               derived line and the same token
  P4-state     `plans/state_check.py --summary --root <tree>` prints zero `MISMATCH:` lines,
               `VERDICT: PASS`, and exits 0
  P5-selftest  `plans/state_check.py --selftest` still exits 0 (the pin edit did not break
               the instrument that holds it)

A re-pin is legitimate only because P1 derives the number from bytes: restoring the stale
line (or hand-editing the pin without moving the pointer) fails P2 or P3 and leaves P4 red.

Exit: 0 target reached, 1 a named defect, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE_REV = "88651a72ef112ed9f5361e1c8c197babec691f96"   # round-85 closure tip
STALE_LINE = 129                                        # the frozen pin this round replaces
TOKEN = "### Adjacent"
PROVINCE = "PROVINCE.md"
SHONEN = "SHONEN.md"
STATE = "plans/state_check.py"
LEGS = ("P1-derive", "P2-shonen", "P3-pin", "P4-state", "P5-selftest")
BOX_RE = re.compile(r"^- \[[ x~]\]")
REF_RE = re.compile(r"(PROVINCE\.md):(\d+)")
PIN_RE = re.compile(
    r'\(\s*4\s*,\s*"(PROVINCE\.md):(\d+)"\s*,\s*(\d+)\s*,\s*"(### Adjacent)"\s*,\s*None\s*\)')


class SetupDefect(Exception):
    """The measurement could not be taken (exit 2, never a fail)."""


def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True)


def extract(lane: Path, rev: str, work: Path) -> Path:
    """Extract the whole measured tree (minus nothing) into a fresh scratch directory."""
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    tip = proc.stdout.decode().strip()
    if proc.returncode != 0 or not tip:
        raise SetupDefect(f"unresolved-revision {rev}")
    root = Path(tempfile.mkdtemp(prefix="c2tree-", dir=work))
    arc = subprocess.run(["git", "-C", str(lane), "archive", "--format=tar", tip],
                         capture_output=True)
    if arc.returncode != 0:
        raise SetupDefect(f"archive-failed {tip[:12]}")
    tar = subprocess.run(["tar", "-x", "-C", str(root)], input=arc.stdout, capture_output=True)
    if tar.returncode != 0:
        raise SetupDefect("extract-failed")
    return root


def derive(root: Path) -> int:
    try:
        lines = (root / PROVINCE).read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise SetupDefect(f"no-province {PROVINCE}") from error
    hits = [index + 1 for index, line in enumerate(lines) if line.strip() == TOKEN]
    if len(hits) != 1:
        raise SetupDefect(f"token-count {TOKEN!r}={len(hits)}")
    return hits[0]


def shonen_pointer(root: Path) -> tuple[str | None, int | None]:
    try:
        lines = (root / SHONEN).read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise SetupDefect(f"no-shonen {SHONEN}") from error
    boxes = [index for index, line in enumerate(lines) if BOX_RE.match(line)]
    if len(boxes) < 4:
        raise SetupDefect(f"box-count={len(boxes)}")
    for line in lines[boxes[3] + 1:]:
        if not line.startswith(("  ", "\t")):
            break
        match = REF_RE.search(line)
        if match:
            return match.group(1), int(match.group(2))
    return None, None


def pin_line(root: Path) -> tuple[int | None, bool]:
    try:
        text = (root / STATE).read_text(encoding="utf-8")
    except OSError as error:
        raise SetupDefect(f"no-state-check {STATE}") from error
    matches = PIN_RE.findall(text)
    if len(matches) != 1:
        return None, False
    _, declared, _, _ = matches[0]
    return int(declared), True


def state_summary(root: Path, lane: Path) -> tuple[int, bool, str]:
    script = (lane / STATE) if (lane / STATE).is_file() else (root / STATE)
    proc = subprocess.run([sys.executable, "-I", "-B", str(script), "--summary",
                           "--root", str(root)], capture_output=True, text=True, timeout=600,
                          env={"PATH": "/usr/bin", "PYTHONDONTWRITEBYTECODE": "1"})
    mismatches = sum(1 for line in proc.stdout.splitlines() if line.startswith("MISMATCH:"))
    passed = proc.returncode == 0 and mismatches == 0 and "VERDICT: PASS" in proc.stdout
    return mismatches, passed, proc.stdout


def state_selftest(root: Path, lane: Path) -> bool:
    script = (lane / STATE) if (lane / STATE).is_file() else (root / STATE)
    proc = subprocess.run([sys.executable, "-I", "-B", str(script), "--selftest"],
                          capture_output=True, text=True, timeout=900,
                          env={"PATH": "/usr/bin", "PYTHONDONTWRITEBYTECODE": "1"})
    return proc.returncode == 0


def check(root: Path, lane: Path, work: Path, selftest: bool = True) -> tuple[list[str], dict]:
    defects: list[str] = []
    stats: dict[str, object] = {"derived_line": None, "shonen_pointer": None,
                                "pin_line": None, "state_mismatches": None,
                                "selftest": "skipped"}
    derived = derive(root)
    stats["derived_line"] = derived
    stats["shonen_pointer"] = f"{PROVINCE}:{shonen_pointer(root)[1]}" if shonen_pointer(root)[1] else "absent"
    line, pin_ok = pin_line(root)
    stats["pin_line"] = line

    if shonen_pointer(root)[1] != derived:
        defects.append(f"P2-shonen pointer={stats['shonen_pointer']} derived={PROVINCE}:{derived}")
    if not pin_ok or line != derived:
        defects.append(f"P3-pin line={line} derived={derived}")
    mismatches, passed, _ = state_summary(root, lane)
    stats["state_mismatches"] = mismatches
    if not passed:
        defects.append(f"P4-state mismatches={mismatches}")
    if selftest:
        ok = state_selftest(root, lane)
        stats["selftest"] = "pass" if ok else "fail"
        if not ok:
            defects.append("P5-selftest exit!=0")
    return defects, stats


def emit(defects: list[str], stats: dict) -> int:
    for line in defects:
        print(f"DEFECT {line}")
    print(f"TARGET derived_line={stats['derived_line']} shonen_pointer={stats['shonen_pointer']} "
          f"pin_line={stats['pin_line']} state_mismatches={stats['state_mismatches']} "
          f"selftest={stats['selftest']} defects={len(defects)}")
    ok = not defects and stats["derived_line"] is not None
    print(f"PREDICATE R86-C2 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


def setup_failure(detail: str) -> int:
    print(f"DEFECT SETUP {detail}")
    print("TARGET derived_line=None shonen_pointer=absent pin_line=None "
          "state_mismatches=None selftest=skipped defects=0")
    print("PREDICATE R86-C2 fail")
    return 2


# ---------------------------------------------------------------- fixtures

def hardlink_copy(source: Path, work: Path, name: str) -> Path:
    root = Path(tempfile.mkdtemp(prefix=f"{name}-", dir=work))
    proc = subprocess.run(["cp", "-al", f"{source}/.", str(root)], capture_output=True)
    if proc.returncode != 0:
        raise SetupDefect("hardlink-copy-failed")
    return root


def rewrite(path: Path, old: str, new: str, count: int = 1) -> None:
    """Rewrite a file through a fresh inode so a hardlinked fixture never edits its source."""
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SetupDefect(f"fixture-needle-absent {path.name}")
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text.replace(old, new, count), encoding="utf-8")
    os.replace(temp, path)


CONTROLS = ("do-nothing", "stale-pin", "pointer-only", "pin-only")


def control(lane: Path, work: Path, name: str) -> int:
    if name == "do-nothing":
        root = extract(lane, BASE_REV, work)
    else:
        root = hardlink_copy(extract(lane, "master", work), work, name)
        derived = derive(root)
        if name == "stale-pin":
            rewrite(root / SHONEN, f"{PROVINCE}:{derived}", f"{PROVINCE}:{STALE_LINE}")
            rewrite(root / STATE, f'4, "{PROVINCE}:{derived}", {derived},',
                    f'4, "{PROVINCE}:{STALE_LINE}", {STALE_LINE},')
        elif name == "pointer-only":
            rewrite(root / STATE, f'4, "{PROVINCE}:{derived}", {derived},',
                    f'4, "{PROVINCE}:{STALE_LINE}", {STALE_LINE},')
        elif name == "pin-only":
            rewrite(root / SHONEN, f"{PROVINCE}:{derived}", f"{PROVINCE}:{STALE_LINE}")
    defects, stats = check(root, lane, work, selftest=False)
    reached = not defects
    print(f"CONTROL {name} target_reached={reached} defects={len(defects)} "
          f"legs={','.join(sorted({d.split()[0] for d in defects})) or 'none'}")
    shutil.rmtree(root, ignore_errors=True)
    return 0 if not reached else 1


MUTANTS = (
    # (name, fixture, [(needle, replacement)], defect the unmutated counter must raise)
    ("no-shonen", "pointer-only", [('if shonen_pointer(root)[1] != derived:', "if False:")],
     "P2-shonen"),
    ("no-pin", "pin-only", [("if not pin_ok or line != derived:", "if False:")], "P3-pin"),
    ("no-state", "stale-pin", [("if not passed:", "if False:")], "P4-state"),
)


def mutants(lane: Path, work: Path) -> int:
    necessary = redundant = 0
    source = Path(__file__).resolve().read_text(encoding="utf-8")
    base = Path(__file__).resolve()
    tip = extract(lane, "master", work)
    for name, fixture, edits, expected in MUTANTS:
        if any(needle not in source for needle, _ in edits):
            print(f"MUTANT {name} NOT-APPLICABLE")
            redundant += 1
            continue
        root = hardlink_copy(tip, work, f"mut-{name}")
        derived = derive(root)
        if fixture == "pointer-only":
            rewrite(root / STATE, f'4, "{PROVINCE}:{derived}", {derived},',
                    f'4, "{PROVINCE}:{STALE_LINE}", {STALE_LINE},')
        elif fixture == "pin-only":
            rewrite(root / SHONEN, f"{PROVINCE}:{derived}", f"{PROVINCE}:{STALE_LINE}")
        elif fixture == "stale-pin":
            rewrite(root / SHONEN, f"{PROVINCE}:{derived}", f"{PROVINCE}:{STALE_LINE}")
            rewrite(root / STATE, f'4, "{PROVINCE}:{derived}", {derived},',
                    f'4, "{PROVINCE}:{STALE_LINE}", {STALE_LINE},')
        mutated = work / f"mutant-{name}.py"
        text = source
        for needle, replacement in edits:
            text = text.replace(needle, replacement, 1)
        mutated.write_text(text, encoding="utf-8")
        plain = subprocess.run([sys.executable, "-I", "-B", str(base), "--lane", str(root),
                                "--root", str(root), "--work", str(work / f"pw-{name}"),
                                "--no-selftest"],
                               capture_output=True, text=True, timeout=900,
                               env={"PATH": "/usr/bin", "PYTHONDONTWRITEBYTECODE": "1"})
        mutant = subprocess.run([sys.executable, "-I", "-B", str(mutated), "--lane", str(root),
                                 "--root", str(root), "--work", str(work / f"mw-{name}"),
                                 "--no-selftest"],
                                capture_output=True, text=True, timeout=900,
                                env={"PATH": "/usr/bin", "PYTHONDONTWRITEBYTECODE": "1"})
        ok_plain = plain.returncode == 1 and expected in plain.stdout
        ok_mutant = "PREDICATE R86-C2 pass" in mutant.stdout
        print(f"MUTANT {name} fixture={fixture} unmutated_defect={ok_plain} "
              f"mutant_reaches_target={ok_mutant}")
        if ok_plain and ok_mutant:
            necessary += 1
        else:
            redundant += 1
        shutil.rmtree(root, ignore_errors=True)
    print(f"MUTANTS real={len(MUTANTS)} necessary={necessary} redundant={redundant}")
    return 0 if necessary == len(MUTANTS) else 1


def selftest(lane: Path, work: Path) -> int:
    failures = 0
    checks = 0

    def check_case(identifier: str, good: bool) -> None:
        nonlocal failures, checks
        failures += not good
        checks += 1
        print(f"SELFTEST {identifier} {'pass' if good else 'FAIL'}")

    tip = extract(lane, "master", work)
    derived = derive(tip)
    check_case("derive-unique", derived > 0)
    check_case("derive-is-not-the-stale-line", derived != STALE_LINE)

    root = hardlink_copy(tip, work, "sel-no-token")
    lines = (root / PROVINCE).read_text(encoding="utf-8").splitlines()
    lines[derived - 1] = "### Adjacent-renamed"
    (root / PROVINCE).write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        derive(root)
    except SetupDefect:
        check_case("absent-token-fails-closed", True)
    else:
        check_case("absent-token-fails-closed", False)

    root = hardlink_copy(tip, work, "sel-double")
    text = (root / PROVINCE).read_text(encoding="utf-8")
    (root / PROVINCE).write_text(text + "\n### Adjacent\n", encoding="utf-8")
    try:
        derive(root)
    except SetupDefect:
        check_case("duplicate-token-fails-closed", True)
    else:
        check_case("duplicate-token-fails-closed", False)

    print(f"SELFTEST cases={checks} red={checks - failures} failures={failures}")
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", default=".")
    parser.add_argument("--root", help="measure this tree instead of extracting --rev")
    parser.add_argument("--rev", default="master")
    parser.add_argument("--work", required=True)
    parser.add_argument("--no-selftest", action="store_true")
    for flag in ("--selftest", "--mutants", "--control-do-nothing", "--control-stale-pin",
                 "--control-pointer-only", "--control-pin-only"):
        parser.add_argument(flag, action="store_true")
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    try:
        if args.selftest:
            return selftest(lane, work)
        if args.mutants:
            return mutants(lane, work)
        for flag, name in (("control_do_nothing", "do-nothing"),
                           ("control_stale_pin", "stale-pin"),
                           ("control_pointer_only", "pointer-only"),
                           ("control_pin_only", "pin-only")):
            if getattr(args, flag):
                return control(lane, work, name)
        root = Path(args.root).resolve() if args.root else extract(lane, args.rev, work)
        defects, stats = check(root, lane, work, selftest=not args.no_selftest)
        if not args.root:
            shutil.rmtree(root, ignore_errors=True)
        return emit(defects, stats)
    except SetupDefect as error:
        return setup_failure(str(error))
    except subprocess.TimeoutExpired as error:
        return setup_failure(f"timeout {error}")


if __name__ == "__main__":
    sys.exit(main())
