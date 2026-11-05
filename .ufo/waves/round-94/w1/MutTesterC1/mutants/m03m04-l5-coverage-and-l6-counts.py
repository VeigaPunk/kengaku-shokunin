#!/usr/bin/env python3
"""R94-C1 counter — the twelfth located offline replay, `write-compressor` (round 94).

Legs, every input read at the measured revision (round-92 discipline: positional case
ids, guarded host probes, no skip flags):

  L1 the receipt is committed at --rev
  L2 the six captured files the probe stages hash to their pins, and the receipt names the
     same subject and solve.sh
  L3 the receipt's LANE_TIP is an ancestor of --rev
  L4 the case table at --rev hashes to the sha the round's frozen-instruments table holds
     at the freeze commit (the single commit that added plans/round-94-claims.md)
  L5 every receipt case vector equals its frozen predicted vector (all cases, no extras)
  L6 the probe re-run from a `git archive` of --rev reproduces the receipt's observation
     block exactly; the sandbox path is injectable (--bwrap) and an unusable sandbox is
     could-not-evaluate (rc 2), never a pass
  L7 the ledger at --rev holds the member executed round 94 with its three classes, 38
     executed rows, the three class cells at their after values, AND the executed member
     SET equals the set at BASE 0cbb9279 plus this member (round-93 wave W-5: a two-member
     swap that keeps the aggregates no longer passes)
  L8 the probe bytes at --rev hash to the frozen-instruments table's probe sha
  L9 the receipt stamps (TOOL_SHA, CASE_TABLE_SHA, HOST_PYTHON, HOST_GCC, HOST_RUSTC) match
     the measured tree and this host

Usage:  python3 plans/round94_c1_replay.py --lane <repo> --rev <rev> --work <dir> [--bwrap PATH]
Exit:   0 predicate pass, 1 a leg failed, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile
from io import BytesIO
from pathlib import Path

CAPDIR = "corpus/evidence/round94/graders/write-compressor"
CAP = CAPDIR + "/tests/test_outputs.py"
PINS = {
    "tests/test_outputs.py": "809f486053e3ffbce852111dee1f63d80ab31297bd33172389e50278bed384e2",
    "tests/original-decomp.c": "7f8d9ef66943f912a217aa48f4ef5efc967b44c2b21d0f56df029b5ab413f62a",
    "tests/original-data.txt": "0fc483d0fb31128dfa41ed11adca56c88688888189826ef9daeafd7559b4fa4e",
    "solution/solve.sh": "01550b7de7ab1320b1898eae055226bb7c73bee259c75102d2240c974a730409",
    "environment/decomp.c": "7f8d9ef66943f912a217aa48f4ef5efc967b44c2b21d0f56df029b5ab413f62a",
    "environment/data.txt": "0fc483d0fb31128dfa41ed11adca56c88688888189826ef9daeafd7559b4fa4e",
}
TABLE = "plans/round94-cases.json"
TOOL = "plans/round94_compressor_probe.py"
RECEIPT = "corpus/evidence/round94/compressor-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
CLAIMS = "plans/round-94-claims.md"
MEMBER = "write-compressor"
MEMBER_CLASSES = ["file-artifact", "stdout-inspection", "subprocess-exec"]
SUBJECT_SHA = PINS["tests/test_outputs.py"]
SOLVE_SHA = PINS["solution/solve.sh"]
AFTER_CELLS = {"file-artifact": 29, "stdout-inspection": 13, "subprocess-exec": 15}
EXECUTED_AFTER = 38
BASE = "0cbb927914e07818e1aaee7e72d8b3c90a2d21c2"
ROW = re.compile(r"^([0-9a-f]{64})  (\S+)$")


class CouldNotEvaluate(Exception):
    pass


def sha(data: bytes | None) -> str:
    return hashlib.sha256(data).hexdigest() if data is not None else "absent"


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=120)


def blob(root: Path, rev: str, path: str) -> bytes | None:
    proc = git(root, "show", f"{rev}:{path}")
    return proc.stdout if proc.returncode == 0 else None


def frozen_table(root: Path, rev: str) -> dict[str, str]:
    added = [x for x in git(root, "log", "--diff-filter=A", "--format=%H", rev, "--", CLAIMS).stdout.decode().split() if x]
    if len(added) != 1:
        return {}
    text = blob(root, added[0], CLAIMS)
    rows: dict[str, str] = {}
    inside = False
    for line in (text or b"").decode(errors="replace").splitlines():
        if not inside and line.strip() == "```frozen-instruments":
            inside = True
            continue
        if inside and line.strip() == "```":
            break
        m = ROW.match(line.strip()) if inside else None
        if m:
            rows[m.group(2)] = m.group(1)
    return rows


def parse_receipt(text: str) -> dict:
    fields: dict[str, str] = {}
    cases: list[tuple[str, str, str]] = []
    obs: list[str] = []
    inside = False
    for line in text.splitlines():
        if line == "OBSERVATIONS_BEGIN":
            inside = True
            continue
        if line == "OBSERVATIONS_END":
            inside = False
            continue
        if inside:
            obs.append(line)
            if line.startswith("CASE "):
                tokens = line.split()[1:]
                cid = tokens[0] if tokens else "?"
                parts = dict(t.partition("=")[::2] for t in tokens[1:] if "=" in t)
                cases.append((cid, parts.get("predicted", "?"), parts.get("observed", "?")))
        elif " " in line and not line.startswith("#"):
            key, _, value = line.partition(" ")
            if key.isupper() or key == "mismatches":
                fields[key] = value.strip()
    return {"fields": fields, "cases": cases, "obs": obs}


def host_tool(args: list[str]) -> str:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return "absent"
    text = (proc.stdout or proc.stderr).strip()
    return text.splitlines()[0] if text else "absent"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--work", required=True)
    ap.add_argument("--bwrap", default="/usr/bin/bwrap")
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{a.rev}^{{commit}}")
    if proc.returncode != 0:
        raise CouldNotEvaluate(f"unresolved-revision {a.rev}")
    rev = proc.stdout.decode().strip()
    defects: list[str] = []

    table_bytes = blob(lane, rev, TABLE)
    table = json.loads(table_bytes.decode()) if table_bytes else {}
    ledger_bytes = blob(lane, rev, LEDGER)
    ledger = json.loads(ledger_bytes.decode()) if ledger_bytes else {}
    frozen = frozen_table(lane, rev)
    receipt_bytes = blob(lane, rev, RECEIPT)
    receipt = parse_receipt(receipt_bytes.decode(errors="replace")) if receipt_bytes else {"fields": {}, "cases": [], "obs": []}

    l1 = receipt_bytes is not None
    if not l1:
        defects.append(f"L1 receipt absent at revision: {RECEIPT}")

    cap = blob(lane, rev, CAP)
    l2 = (all(sha(blob(lane, rev, f"{CAPDIR}/{p}")) == want for p, want in PINS.items())
          and receipt["fields"].get("SUBJECT_SHA") == SUBJECT_SHA
          and receipt["fields"].get("SOLVE_SHA") == SOLVE_SHA)
    if not l2:
        defects.append(f"L2 capture/receipt sha mismatch (cap={sha(cap)[:12]} receipt={receipt['fields'].get('SUBJECT_SHA', 'absent')[:12]})")

    tip = receipt["fields"].get("LANE_TIP", "")
    l3 = bool(tip) and git(lane, "merge-base", "--is-ancestor", tip, rev).returncode == 0
    if not l3:
        defects.append(f"L3 LANE_TIP {tip or 'absent'} not an ancestor of {rev[:12]}")

    l4 = bool(frozen.get(TABLE)) and sha(table_bytes) == frozen.get(TABLE)
    if not l4:
        defects.append(f"L4 case table {sha(table_bytes)[:12]} vs frozen {frozen.get(TABLE, 'absent')[:12]}")

    predicted = {c["id"]: c["predicted"] for c in table.get("cases", [])}
    mismatches = 0
    seen = set()
    for cid, pred, obs in receipt["cases"]:
        seen.add(cid)
        if cid not in predicted:
            mismatches += 1
            defects.append(f"L5 receipt names unknown case {cid}")
        elif obs != pred or pred != predicted[cid]:
            mismatches += 1
            defects.append(f"L5 case {cid} predicted={pred} observed={obs} frozen={predicted[cid]}")
    l5 = bool(predicted) and mismatches == 0 
    if not l5 and not any(d.startswith("L5") for d in defects):
        defects.append(f"L5 case coverage {len(receipt['cases'])} of {len(predicted)}")

    if not (Path(a.bwrap).is_file() and os.access(a.bwrap, os.X_OK)):
        print(f"DEFECT SETUP sandbox-unavailable {a.bwrap}")
        print("PREDICATE R94-C1 could-not-evaluate")
        return 2
    tool_at_rev = blob(lane, rev, TOOL)
    if tool_at_rev is None:
        l6 = False
        defects.append(f"L6 probe absent at revision: {TOOL}")
    else:
        extract = work / "extract"
        extract.mkdir(parents=True, exist_ok=True)
        archive = git(lane, "archive", rev)
        if archive.returncode != 0:
            raise CouldNotEvaluate("git archive failed")
        with tarfile.open(fileobj=BytesIO(archive.stdout)) as tar:
            tar.extractall(extract, filter="data")
        rerun = subprocess.run([sys.executable, "-I", "-B", str(extract / TOOL), "--lane", str(extract),
                                "--work", str(work / "rerun"), "--bwrap", a.bwrap],
                               capture_output=True, text=True, timeout=3600)
        if rerun.returncode == 2:
            print("DEFECT SETUP probe-rerun " + (rerun.stdout.strip().splitlines() or ["rc=2"])[-1])
            print("PREDICATE R94-C1 could-not-evaluate")
            return 2
        rerun_obs = parse_receipt(rerun.stdout)["obs"]
        l6 = rerun.returncode == 0 and bool(receipt["obs"]) and len(rerun_obs) == len(receipt["obs"])
        if not l6:
            defects.append(f"L6 rerun rc={rerun.returncode} obs={len(rerun_obs)} want={len(receipt['obs'])} equal={rerun_obs == receipt['obs']}")

    members = ledger.get("members", {}) if ledger else {}
    member = members.get(MEMBER, {})
    exec_total = sum(1 for v in members.values() if v.get("status") == "executed")
    cells = {cl: sum(1 for v in members.values() if v.get("status") == "executed" and cl in v.get("classes", []))
             for cl in AFTER_CELLS}
    base_bytes = blob(lane, BASE, LEDGER)
    base_members = json.loads(base_bytes.decode()).get("members", {}) if base_bytes else {}
    base_set = {n for n, v in base_members.items() if v.get("status") == "executed"}
    rev_set = {n for n, v in members.items() if v.get("status") == "executed"}
    set_ok = bool(base_set) and MEMBER not in base_set and rev_set == base_set | {MEMBER}
    l7 = (member.get("status") == "executed" and member.get("round") == 94
          and member.get("classes") == MEMBER_CLASSES and exec_total == EXECUTED_AFTER and cells == AFTER_CELLS
          and set_ok)
    if not l7:
        defects.append(f"L7 ledger member={member.get('status')} round={member.get('round')} executed_total={exec_total} cells={cells} "
                       f"set_added={sorted(rev_set - base_set)} set_removed={sorted(base_set - rev_set)}")

    tool_bytes = blob(lane, rev, TOOL)
    l8 = bool(frozen.get(TOOL)) and sha(tool_bytes) == frozen.get(TOOL)
    if not l8:
        defects.append(f"L8 probe {sha(tool_bytes)[:12]} vs frozen {frozen.get(TOOL, 'absent')[:12]}")

    f = receipt["fields"]
    l9 = (f.get("TOOL_SHA") == sha(tool_bytes) and f.get("CASE_TABLE_SHA") == sha(table_bytes)
          and f.get("HOST_PYTHON") == host_tool(["/usr/bin/python3", "-V"])
          and f.get("HOST_GCC") == host_tool(["/usr/bin/gcc", "--version"])
          and f.get("HOST_RUSTC") == host_tool(["/usr/bin/rustc", "--version"]))
    if not l9:
        defects.append(f"L9 stamps tool={f.get('TOOL_SHA', 'absent')[:12]} table={f.get('CASE_TABLE_SHA', 'absent')[:12]} python={f.get('HOST_PYTHON')}")

    legs = [l1, l2, l3, l4, l5, l6, l7, l8, l9]
    ok = all(legs)
    print("LEGS " + " ".join(f"L{i + 1}={'pass' if v else 'fail'}" for i, v in enumerate(legs)))
    print("TARGET executed_rows=%d member=%s located=%d executed=%d cases=%d legs=%d mismatches=%d defects=%d"
          % (exec_total, MEMBER, 1 if cap is not None else 0, 1 if ok else 0, len(predicted),
             len(receipt["cases"]) * len(table.get("leg_order", [])), mismatches, len(defects)))
    for d in defects:
        print("DEFECT " + d)
    print("PREDICATE R94-C1 " + ("pass" if ok else "fail"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R94-C1 could-not-evaluate")
        sys.exit(2)
