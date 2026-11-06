#!/usr/bin/env python3
"""R95-C2 counting command — how many known false freeze-integrity gates pass the lane's counter?

Population: the fourteen rows of plans/round95-false-gates.tsv (frozen at P0), each a gate the
round-94 wave built that passes the frozen round-94 counter 5/5 (BEFORE receipts
.ufo/waves/round-95/L1/controls/before-r94-counter-<id>.txt). Every file is read at --rev and must
hash to its tsv sha256.

For each row the counter under test (`--counter`, default plans/round95_c2_counter.py read at
--rev, or an older counter for the do-nothing control) runs with `--tool-file <row>`; the row
PASSES the counter iff the counter prints `PREDICATE R<n>-C2 pass` and exits 0. Each row also has a designated leg (DESIGNATED below, frozen
with this file): its RED must appear in the counter output, so a row that fails for an unrelated
reason does not count as discriminated. The honest gate (no --tool-file) must pass.

Printed:
    GATE <id> sha=<12> rc=<rc> passes=<0|1> designated=<leg> designated_red=<0|1>
    HONEST rc=<rc> predicate=<pass|fail>
    FALSEGATES total=14 passing=<n> designated_red=<n> honest=<pass|fail>
    PREDICATE R95-C2 pass|fail       pass iff passing=0, designated_red=14, honest=pass
Exit 0 pass, 1 fail, 2 could-not-evaluate (unresolved rev, missing/mismatched row file, counter absent).
Usage:  python3 plans/round95_false_gate_census.py --lane . --rev REV --work DIR [--counter PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TSV = "plans/round95-false-gates.tsv"
COUNTER = "plans/round95_c2_counter.py"
TOTAL = 14
# any counter's pass line, so a do-nothing run with an older counter is scored, not silently zero
PASS_LINE = re.compile(r"^PREDICATE R\d+-C2 pass$", re.M)
DESIGNATED = {
    "F1-paths-dup-accepted": "W2 w2-paths-dup",
    "F2-paths-absent-dropped": "W2 w2-paths-absent",
    "F3b-octopus-anchor-kept": "W2 w2-octopus",
    "F4b-touched-M-only-anchor-kept": "W2 w2-delete-readd",
    "F5-rename-intact": "W2 w2-rename",
    "F6b-entry-rc-remap": "W2 w2-paths-absent",
    "F7-spaced-row-dropped": "W2 w2-spaced-row",
    "X1-stub-battery": "W3",
    "M01-paths-dup-guard-dropped": "W2 w2-paths-dup",
    "M02-unterminated-block-accepted": "W2 w2-unterminated",
    "M07-battery-nonfatal": "W3",
    "M15-predicate-always-pass": "W2 w2-edited",
    "M19-battery-red-concealed": "W3",
    "M20-battery-broken-and-concealed": "W3",
}


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=120)


def designated_red(leg: str, out: str) -> bool:
    if leg == "W3":
        return re.search(r"^W3 fail ", out, re.M) is not None
    return re.search(rf"^{re.escape(leg)} RED ", out, re.M) is not None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--work", required=True)
    ap.add_argument("--counter")
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve()
    if work == lane or lane in work.parents:
        print(f"DEFECT SETUP --work inside the lane {work}")
        print("PREDICATE R95-C2 could-not-evaluate")
        return 2
    work.mkdir(parents=True, exist_ok=True)
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{a.rev}^{{commit}}")
    if proc.returncode != 0:
        print(f"DEFECT SETUP unresolved-revision {a.rev}")
        print("PREDICATE R95-C2 could-not-evaluate")
        return 2
    rev = proc.stdout.decode().strip()
    if a.counter:
        counter = Path(a.counter).resolve()
    else:
        b = git(lane, "show", f"{rev}:{COUNTER}")
        if b.returncode != 0:
            print(f"DEFECT SETUP counter absent at {rev[:12]}")
            print("PREDICATE R95-C2 could-not-evaluate")
            return 2
        counter = work / "counter-under-test.py"
        counter.write_bytes(b.stdout)
    print(f"COUNTER {counter.name} sha256={hashlib.sha256(counter.read_bytes()).hexdigest()} REV {rev}")
    tsv = git(lane, "show", f"{rev}:{TSV}")
    if tsv.returncode != 0:
        print(f"DEFECT SETUP {TSV} absent at {rev[:12]}")
        print("PREDICATE R95-C2 could-not-evaluate")
        return 2
    rows = []
    for line in tsv.stdout.decode().splitlines():
        if not line or line.startswith("#") or line.startswith("id\t"):
            continue
        gid, path, want = line.split("\t")
        data = git(lane, "show", f"{rev}:{path}")
        if data.returncode != 0 or hashlib.sha256(data.stdout).hexdigest() != want or gid not in DESIGNATED:
            print(f"DEFECT SETUP row {gid} file absent, sha mismatch or undesignated")
            print("PREDICATE R95-C2 could-not-evaluate")
            return 2
        f = work / f"gate-{gid}.py"
        f.write_bytes(data.stdout)
        rows.append((gid, f, want))
    if len(rows) > TOTAL or {g for g, _, _ in rows} != set(DESIGNATED):
        print(f"DEFECT SETUP population {len(rows)} != {TOTAL}")
        print("PREDICATE R95-C2 could-not-evaluate")
        return 2

    def run(tool: Path | None, tag: str) -> tuple[int, str]:
        extra = ["--tool-file", str(tool)] if tool else []
        p = subprocess.run([sys.executable, "-I", "-B", str(counter), "--lane", str(lane), "--rev", rev,
                            "--work", str(work / f"w-{tag}"), *extra], capture_output=True, text=True, timeout=3600)
        (work / f"out-{tag}.txt").write_text(p.stdout)
        return p.returncode, p.stdout

    with ThreadPoolExecutor(max_workers=8) as pool:
        honest_f = pool.submit(run, None, "honest")
        futs = {gid: pool.submit(run, f, gid) for gid, f, _ in rows}
        honest_rc, honest_out = honest_f.result()
        results = {gid: fut.result() for gid, fut in futs.items()}
    passing = red = 0
    for gid, _, want in rows:
        rc, out = results[gid]
        passes = int(rc == 0 and PASS_LINE.search(out) is not None)
        dred = int(designated_red(DESIGNATED[gid], out))
        passing += passes
        red += dred
        print(f"GATE {gid} sha={want[:12]} rc={rc} passes={passes} designated={DESIGNATED[gid].replace(' ', ':')} designated_red={dred}")
    honest = "pass" if honest_rc == 0 and PASS_LINE.search(honest_out) else "fail"
    print(f"HONEST rc={honest_rc} predicate={honest}")
    for line in honest_out.splitlines():
        if re.match(r"^(TOOL|W[1-5] (pass|fail)|TARGET)", line):
            print("HONEST " + line)
    ok = passing == 0 and red == TOTAL and honest == "pass"
    print(f"FALSEGATES total={TOTAL} passing={passing} designated_red={red} honest={honest}")
    print(f"PREDICATE R95-C2 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
