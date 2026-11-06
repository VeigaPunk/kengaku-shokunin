#!/usr/bin/env python3
"""Pre-freeze standing-gate check over a candidate tree (round 100; lesson round-100 M1).

Round-99 routed defects 1 and 2 (`corpus/lessons/round-99-verifier-spotcheck.md`): two dated
corrections after T repaired candidate bytes the standing gates had flagged (typed word counts,
`plans/anchor_line_check.py` live 0 -> 5; registry selftest cells, `plans/round82_c1_plans_registry.py`
13 -> 17 DEFECT lines), because the L1 ran neither gate on the candidate tree before F, and its harm
battery compared defect COUNTS on trees that were not revision-scoped (`--tip` defaulted to master).

This tool runs both gates, each from its BASE bytes, against BASE and against the candidate revision
CAND, each on its own `git clone --shared` checkout (the line gate reads the work tree) or with an
explicit `--tip` (the registry gate reads committed bytes), and compares finding SETS:

  line gate     the set of `ROW <id> state=live …` lines
  registry gate the set of `DEFECT …` lines (the `DEFECTS n=` total line excluded)

It prints `NEW <gate> <line>` for every finding at CAND absent at BASE, `GONE <gate> <line>` for every
finding at BASE absent at CAND, then `PREFREEZE new=<n> gone=<m> line_base=… line_cand=… reg_base=…
reg_cand=…` and `VERDICT clean|red`. Exit 0 iff new == 0; 1 when a gate turned redder; 2 setup error.

Usage:  python3 plans/round100_prefreeze_check.py --lane <repo> --base <rev> --cand <rev> --work <dir>
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

LINE_GATE = "plans/anchor_line_check.py"
REG_GATE = "plans/round82_c1_plans_registry.py"


class Setup(Exception):
    pass


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=300)


def resolve(lane: Path, rev: str) -> str:
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if proc.returncode != 0:
        raise Setup(f"unresolved revision {rev}")
    return proc.stdout.decode().strip()


def gate_bytes(lane: Path, base: str, path: str, work: Path) -> Path:
    proc = git(lane, "show", f"{base}:{path}")
    if proc.returncode != 0:
        raise Setup(f"{path} absent at {base}")
    dest = work / ("base-" + path.rsplit("/", 1)[-1])
    dest.write_bytes(proc.stdout)
    return dest


def line_findings(lane: Path, rev: str, gate: Path, work: Path) -> set[str]:
    tree = work / f"tree-{rev[:12]}"
    if tree.exists():
        shutil.rmtree(tree)
    if subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", str(lane), str(tree)],
                      capture_output=True, timeout=300).returncode != 0:
        raise Setup("clone failed")
    try:
        if git(tree, "-c", "advice.detachedHead=false", "checkout", "-q", rev).returncode != 0:
            raise Setup(f"checkout {rev} failed")
        if git(tree, "rev-parse", "--show-toplevel").stdout.decode().strip() != str(tree):
            raise Setup("fixture toplevel mismatch")
        run = subprocess.run([sys.executable, "-I", "-B", str(gate), "--lane", str(tree)],
                             capture_output=True, text=True, timeout=1200, cwd=str(tree))
    finally:
        shutil.rmtree(tree, ignore_errors=True)
    if run.returncode not in (0, 1) or "ANCHORLINE " not in run.stdout:
        raise Setup(f"line gate rc={run.returncode} at {rev[:12]}")
    return {x for x in run.stdout.splitlines() if x.startswith("ROW ") and " state=live" in x}


def reg_findings(lane: Path, rev: str, gate: Path, work: Path) -> set[str]:
    w = work / f"reg-{rev[:12]}"
    w.mkdir(parents=True, exist_ok=True)
    run = subprocess.run([sys.executable, "-I", "-B", str(gate), "--lane", str(lane), "--tip", rev, "--work", str(w)],
                         capture_output=True, text=True, timeout=1200, cwd=str(lane))
    shutil.rmtree(w, ignore_errors=True)
    if run.returncode not in (0, 1) or "PREDICATE R82-C1" not in run.stdout:
        raise Setup(f"registry gate rc={run.returncode} at {rev[:12]}")
    return {x for x in run.stdout.splitlines() if x.startswith("DEFECT ") and not x.startswith("DEFECTS ")}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--cand", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve()
    if work == lane or lane in work.parents:
        raise Setup(f"--work inside the lane {work}")
    work.mkdir(parents=True, exist_ok=True)
    base, cand = resolve(lane, a.base), resolve(lane, a.cand)
    print(f"BASE {base}")
    print(f"CAND {cand}")
    lg = gate_bytes(lane, base, LINE_GATE, work)
    rg = gate_bytes(lane, base, REG_GATE, work)
    lb, lc = line_findings(lane, base, lg, work), line_findings(lane, cand, lg, work)
    rb, rc = reg_findings(lane, base, rg, work), reg_findings(lane, cand, rg, work)
    new = [("line", x) for x in sorted(lc - lb)] + [("registry", x) for x in sorted(rc - rb)]
    gone = [("line", x) for x in sorted(lb - lc)] + [("registry", x) for x in sorted(rb - rc)]
    for g, x in new:
        print(f"NEW {g} {x}")
    for g, x in gone:
        print(f"GONE {g} {x}")
    print(f"PREFREEZE new={len(new)} gone={len(gone)} line_base={len(lb)} line_cand={len(lc)} "
          f"reg_base={len(rb)} reg_cand={len(rc)}")
    print("VERDICT " + ("clean" if not new else "red"))
    return 0 if not new else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Setup as error:
        print(f"SETUP {error}")
        sys.exit(2)
