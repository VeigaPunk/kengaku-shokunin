#!/usr/bin/env python3
"""Round 56, claim C1: landed-evidence verification gate (kengaku).

Re-verifies the landed r55/r56 evidence set from a clean clone with four frozen legs:

  L-reg      python3 plans/round52_c2_registry.py --lane <clone>
             -> exit 0, "MISSING 0", "PREDICATE R52-C2 pass"
  L-chess    python3 plans/round55_c3_chess_probe.py --lane <clone> --work <work>/c3
             --receipt <work>/c3.txt
             -> exit 0, summary "cases=12 observed_pass=5 observed_fail=7 mismatches=0",
                byte-equal to the summary line of the committed receipt
                corpus/evidence/round55/chess-best-move-probe.txt
  L-selftest python3 plans/round55_c2_entryargv.py --selftest --work <work>/c2st
             -> exit 0, "4/4 PASS"
  L-grader   python3 grader.py (cwd <clone>) -> exit 0, "CHECKS n=733 mismatches=0"
             and python3 grader.py --selftest -> exit 0, "[selftest] ALL PASS"

Prints one PASS/FAIL line per leg and a final verdict; exit 0 only when every leg
passes. --selftest proves the checker fails on tampered leg outputs without running
any subprocess. Scratch defaults honour TMPDIR; pass --work under $HYAKU_SCRATCH.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

COMMITTED_CHESS_RECEIPT = Path("corpus/evidence/round55/chess-best-move-probe.txt")
CHESS_SUMMARY = "cases=12 observed_pass=5 observed_fail=7 mismatches=0"
GRADER_CHECKS = "CHECKS n=733 mismatches=0"
SELFTEST_PASS = "4/4 PASS"


def _summary_line(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("cases="):
            return line.strip()
    return None


def check_reg(rc: int, out: str) -> tuple[bool, str]:
    ok = rc == 0 and "MISSING 0" in out and "PREDICATE R52-C2 pass" in out
    return ok, "registry closure (MISSING 0, PREDICATE R52-C2 pass)"


def check_chess(rc: int, out: str, committed_line: str | None) -> tuple[bool, str]:
    line = _summary_line(out)
    ok = rc == 0 and line == CHESS_SUMMARY and committed_line == CHESS_SUMMARY
    return ok, f"chess probe re-run == committed receipt ({CHESS_SUMMARY})"


def check_selftest(rc: int, out: str) -> tuple[bool, str]:
    ok = rc == 0 and SELFTEST_PASS in out
    return ok, f"entryargv selftest ({SELFTEST_PASS})"


def check_grader(rc: int, out: str, rc_st: int, out_st: str) -> tuple[bool, str]:
    ok = rc == 0 and GRADER_CHECKS in out and rc_st == 0 and "[selftest] ALL PASS" in out_st
    return ok, f"grader replay+selftest ({GRADER_CHECKS}, ALL PASS)"


def run_legs(lane: Path, work: Path) -> tuple[int, list[str]]:
    lines: list[str] = []
    fails = 0
    work.mkdir(parents=True, exist_ok=True)

    r = subprocess.run([sys.executable, "plans/round52_c2_registry.py", "--lane", str(lane)],
                       cwd=str(lane), capture_output=True, text=True, timeout=600)
    ok, why = check_reg(r.returncode, r.stdout)
    lines.append(f"[{'PASS' if ok else 'FAIL'}] L-reg {why}")
    fails += 0 if ok else 1

    c3 = work / "c3"
    r = subprocess.run([sys.executable, "plans/round55_c3_chess_probe.py", "--lane", str(lane),
                        "--work", str(c3), "--receipt", str(c3 / "receipt.txt")],
                       cwd=str(lane), capture_output=True, text=True, timeout=1800)
    committed = lane / COMMITTED_CHESS_RECEIPT
    committed_line = _summary_line(committed.read_text(errors="replace")) if committed.is_file() else None
    ok, why = check_chess(r.returncode, r.stdout, committed_line)
    lines.append(f"[{'PASS' if ok else 'FAIL'}] L-chess {why}")
    fails += 0 if ok else 1

    r = subprocess.run([sys.executable, "plans/round55_c2_entryargv.py", "--selftest",
                        "--work", str(work / "c2st")],
                       cwd=str(lane), capture_output=True, text=True, timeout=600)
    ok, why = check_selftest(r.returncode, r.stdout)
    lines.append(f"[{'PASS' if ok else 'FAIL'}] L-selftest {why}")
    fails += 0 if ok else 1

    r = subprocess.run([sys.executable, "grader.py"], cwd=str(lane),
                       capture_output=True, text=True, timeout=900)
    r2 = subprocess.run([sys.executable, "grader.py", "--selftest"], cwd=str(lane),
                        capture_output=True, text=True, timeout=900)
    ok, why = check_grader(r.returncode, r.stdout, r2.returncode, r2.stdout)
    lines.append(f"[{'PASS' if ok else 'FAIL'}] L-grader {why}")
    fails += 0 if ok else 1

    verdict = "LANDCHECK PASS n=4" if fails == 0 else f"LANDCHECK FAIL failed-legs={fails}"
    lines.append(verdict)
    return (0 if fails == 0 else 1), lines


def selftest() -> int:
    """The checker must fail on tampered leg outputs (no subprocesses)."""
    cases = [
        ("green", check_reg(0, "MISSING 0\nPREDICATE R52-C2 pass\n"), True),
        ("registry-missing-1", check_reg(0, "MISSING 1\nPREDICATE R52-C2 fail\n"), False),
        ("chess-drift", check_chess(0, "cases=12 observed_pass=6 observed_fail=6 mismatches=0\n",
                                    CHESS_SUMMARY), False),
        ("chess-committed-drift", check_chess(0, CHESS_SUMMARY + "\n", "cases=12 x\n"), False),
        ("selftest-3of4", check_selftest(0, "[selftest] 3/4 PASS\n"), False),
        ("grader-mismatch", check_grader(0, "CHECKS n=732 mismatches=0\n", 0, "[selftest] ALL PASS\n"), False),
        ("grader-selftest-fail", check_grader(0, GRADER_CHECKS + "\n", 1, "[selftest] FAIL\n"), False),
    ]
    bad = 0
    for name, (ok, _why), want in cases:
        good = ok == want
        print(f"[selftest] {'PASS' if good else 'FAIL'} {name}")
        bad += 0 if good else 1
    print(f"[selftest] {'ALL PASS' if bad == 0 else f'{bad} FAILING'} ({len(cases) - bad}/{len(cases)})")
    return 0 if bad == 0 else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", default=".", help="lane repo root or clean clone to verify")
    ap.add_argument("--work", default=None, help="scratch dir (default: fresh dir under TMPDIR)")
    ap.add_argument("--receipt", default=None, help="tee the full output to this path")
    ap.add_argument("--selftest", action="store_true", help="checker self-test, no subprocesses")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    lane = Path(a.lane).resolve()
    if not (lane / "grader.py").is_file() or not (lane / "SKILL.md").is_file():
        print(f"SETUP {lane} is not a kengaku lane tree (grader.py/SKILL.md absent)")
        return 2
    tmp = None
    try:
        if a.work:
            work = Path(a.work)
        else:
            tmp = tempfile.mkdtemp(prefix="kengaku-r56-landcheck-")
            work = Path(tmp)
        rc, lines = run_legs(lane, work)
        text = "\n".join(lines) + "\n"
        print(text, end="")
        if a.receipt:
            rp = Path(a.receipt)
            rp.parent.mkdir(parents=True, exist_ok=True)
            rp.write_text(text)
        return rc
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
