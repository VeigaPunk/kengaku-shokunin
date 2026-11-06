#!/usr/bin/env python3
"""R93-C1 counter — the eleventh located offline replay, `schemelike-metacircular-eval` (round 93).

Legs, every input read at the measured revision (round-92 discipline: positional case
ids, guarded host probes, no skip flags):

  L1 the receipt is committed at --rev
  L2 the captured grader, interp.py and solve.sh hash to their pins, and the receipt names
     the same subject and interpreter
  L3 the receipt's LANE_TIP is an ancestor of --rev
  L4 the case table at --rev hashes to the sha the round's frozen-instruments table holds
     at the freeze commit (the commit that added plans/round-93-claims.md)
  L5 every receipt case vector equals its frozen predicted vector (all cases, no extras)
  L6 the probe re-run from a `git archive` of --rev reproduces the receipt's observation
     block exactly; the sandbox path is injectable (--bwrap) and an unusable sandbox is
     could-not-evaluate (rc 2), never a pass
  L7 the ledger at --rev holds the member executed round 93 with its four classes, 37
     executed rows, and the four class cells at their after values
  L8 the probe bytes at --rev hash to the frozen-instruments table's probe sha
  L9 the receipt stamps (TOOL_SHA, CASE_TABLE_SHA, HOST_PYTHON) match the measured tree
     and this host

Usage:  python3 plans/round93_c1_replay.py --lane <repo> --rev <rev> --work <dir> [--bwrap PATH]
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

CAPDIR = "corpus/evidence/round93/graders/schemelike-metacircular-eval"
CAP = CAPDIR + "/tests/test_outputs.py"
INTERP = CAPDIR + "/tests/interp.py"
SOLVE = CAPDIR + "/solution/solve.sh"
TABLE = "plans/round93-cases.json"
TOOL = "plans/round93_scheme_probe.py"
RECEIPT = "corpus/evidence/round93/scheme-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
CLAIMS = "plans/round-93-claims.md"
MEMBER = "schemelike-metacircular-eval"
MEMBER_CLASSES = ["file-artifact", "stdout-inspection", "subprocess-exec", "timing-wall"]
SUBJECT_SHA = "fbb84e3c0c2f72ed7de90f54380f860052c16155e7d0c9076cd57c966e9be7ed"
INTERP_SHA = "efb8b5cdcf78b73afcf39d59600a1f355ca89b7bac9854bb01f110cc77bea2c1"
SOLVE_SHA = "e2c5b0ac2bef4801a1891e13c108813381877426c1a7f01bab86b4fc1f712510"
AFTER_CELLS = {"file-artifact": 28, "stdout-inspection": 12, "subprocess-exec": 14, "timing-wall": 4}
EXECUTED_AFTER = 37
SET_BASE = "28e9f8bf4e8a68b1a34babfa71be9de595b78c4e"  # round-93 BASE; L7 keyed to its executed set (round 96)
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
    if not added:
        return {}
    text = blob(root, added[-1], CLAIMS)
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


def host_python() -> str:
    try:
        proc = subprocess.run(["/usr/bin/python3", "-V"], capture_output=True, text=True, timeout=60)
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
    l2 = (sha(cap) == SUBJECT_SHA and sha(blob(lane, rev, INTERP)) == INTERP_SHA
          and sha(blob(lane, rev, SOLVE)) == SOLVE_SHA
          and receipt["fields"].get("SUBJECT_SHA") == SUBJECT_SHA
          and receipt["fields"].get("INTERP_SHA") == INTERP_SHA)
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
    l5 = bool(predicted) and mismatches == 0 and seen == set(predicted) and len(receipt["cases"]) == len(predicted)
    if not l5 and not any(d.startswith("L5") for d in defects):
        defects.append(f"L5 case coverage {len(receipt['cases'])} of {len(predicted)}")

    if not (Path(a.bwrap).is_file() and os.access(a.bwrap, os.X_OK)):
        print(f"DEFECT SETUP sandbox-unavailable {a.bwrap}")
        print("PREDICATE R93-C1 could-not-evaluate")
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
            print("PREDICATE R93-C1 could-not-evaluate")
            return 2
        rerun_obs = parse_receipt(rerun.stdout)["obs"]
        l6 = rerun.returncode == 0 and bool(receipt["obs"]) and rerun_obs == receipt["obs"]
        if not l6:
            defects.append(f"L6 rerun rc={rerun.returncode} obs={len(rerun_obs)} want={len(receipt['obs'])} equal={rerun_obs == receipt['obs']}")

    members = ledger.get("members", {}) if ledger else {}
    member = members.get(MEMBER, {})
    exec_total = sum(1 for v in members.values() if v.get("status") == "executed")
    cells = {cl: sum(1 for v in members.values() if v.get("status") == "executed" and cl in v.get("classes", []))
             for cl in AFTER_CELLS}
    # round-96 re-key: the executed SET must contain the round-93 set (BASE plus this member);
    # class cells may only grow — never an absolute executed total
    base_bytes = blob(lane, SET_BASE, LEDGER)
    base_set = ({n for n, v in json.loads(base_bytes.decode()).get("members", {}).items() if v.get("status") == "executed"}
                if base_bytes else set())
    rev_set = {n for n, v in members.items() if v.get("status") == "executed"}
    set_ok = bool(base_set) and MEMBER not in base_set and rev_set >= base_set | {MEMBER}
    cells_ok = all(cells[cl] >= want for cl, want in AFTER_CELLS.items())
    l7 = (member.get("status") == "executed" and member.get("round") == 93
          and member.get("classes") == MEMBER_CLASSES and set_ok and cells_ok)
    if not l7:
        defects.append(f"L7 ledger member={member.get('status')} round={member.get('round')} executed_total={exec_total} cells={cells} "
                       f"set_removed={sorted((base_set | {MEMBER}) - rev_set)}")

    tool_bytes = blob(lane, rev, TOOL)
    l8 = bool(frozen.get(TOOL)) and sha(tool_bytes) == frozen.get(TOOL)
    if not l8:
        defects.append(f"L8 probe {sha(tool_bytes)[:12]} vs frozen {frozen.get(TOOL, 'absent')[:12]}")

    f = receipt["fields"]
    l9 = (f.get("TOOL_SHA") == sha(tool_bytes) and f.get("CASE_TABLE_SHA") == sha(table_bytes)
          and f.get("HOST_PYTHON") == host_python())
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
    print("PREDICATE R93-C1 " + ("pass" if ok else "fail"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R93-C1 could-not-evaluate")
        sys.exit(2)
