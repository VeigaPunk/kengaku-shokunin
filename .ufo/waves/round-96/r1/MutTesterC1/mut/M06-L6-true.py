#!/usr/bin/env python3
"""R96-C1 counter — the fourteenth located offline replay, `multi-source-data-merger` (round 96).

Legs, every input read at the measured revision (round-92 discipline: positional case
ids, guarded host probes, no skip flags):

  L1 the receipt is committed at --rev
  L2 the seven captured files the probe stages hash to their pins, and the receipt names the
     same subject, test.sh and solve.sh
  L3 the receipt's LANE_TIP is an ancestor of --rev
  L4 the case table at --rev hashes to the sha the round's frozen-instruments table holds
     at the freeze commit (the single commit that added plans/round-96-claims.md)
  L5 every receipt case vector equals its frozen predicted vector (all cases, no extras)
  L6 the probe re-run from a `git archive` of --rev reproduces the receipt's observation
     block exactly and the same TOOL_SHA / CASE_TABLE_SHA / ENV_SIDE / GRADER_SIDE stamps
     (round-94 wave W-6: stamps sat outside the compared block); the sandbox path and both
     venvs are injectable and an unusable sandbox or venv is could-not-evaluate (rc 2)
  L7 the ledger at --rev holds the member executed round 96 with its two classes and the
     legacy-gate fields receipt=<this receipt>, subject=tb2-header, verdict=cases, and the
     executed member SET at --rev CONTAINS the set at BASE 45740a61 plus this member — keyed to
     the member set, never to an absolute executed total (round-95 routed defect 2: an
     absolute pin goes red the round any later member is added); a removed member is a fail
  L8 the probe bytes at --rev hash to the frozen-instruments table's probe sha
  L9 the receipt stamps (TOOL_SHA, CASE_TABLE_SHA, HOST_BASH) match the measured tree and
     this host

The counter refuses (rc 2) unless the process cwd is the lane root (round-95 routed defect 6:
a cwd stamp that is printed but never checked).

Usage:  python3 plans/round96_c1_replay.py --lane <repo> --rev <rev> --work <dir>
            --env-venv <dir> --grader-venv <dir> [--bwrap PATH]
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

CAPDIR = "corpus/evidence/round96/graders/multi-source-data-merger"
CAP = CAPDIR + "/tests/test_outputs.py"
PINS = {
    "tests/test_outputs.py": "a070888930cf829aeca039771260b1386bda990ea805f313468d381ba3608ca5",
    "tests/test.sh": "d5a00e64413c0e1ae452f38a1aa1a47c3ed7b4416bbfccae1a4c053025a336d1",
    "solution/solve.sh": "1b3d0d50e31930d042495d48f4c8e95f1a9c1a979c803b7f7cec651322537e1e",
    "environment/Dockerfile": "c95a40d3d35b473dc15ae1e8784ba7fb1725805c0583fc574dd2764325d75e4f",
    "environment/data/source_a/users.json": "75e51e2d3ab0bdba2269d7cf3757576f84f3ee2c13407d2db94289a5958a1778",
    "environment/data/source_b/users.csv": "8e87d16dc47d166edd8e56165955bad265b630d53d02762367c816affb5fa760",
    "environment/data/source_c/users.parquet": "23d1ea51c4170bdba53febb885a0f495e28de525a52667347b2932136b9a72fe",
}
TABLE = "plans/round96-cases.json"
TOOL = "plans/round96_merger_probe.py"
RECEIPT = "corpus/evidence/round96/merger-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
CLAIMS = "plans/round-96-claims.md"
MEMBER = "multi-source-data-merger"
MEMBER_CLASSES = ["file-artifact", "serialization-schema"]
SUBJECT_SHA = PINS["tests/test_outputs.py"]
TEST_SH_SHA = PINS["tests/test.sh"]
SOLVE_SHA = PINS["solution/solve.sh"]
BASE = "45740a616028015b5dfcf9900753e3bb5e6fe689"
RERUN_STAMPS = ("TOOL_SHA", "CASE_TABLE_SHA", "ENV_SIDE", "GRADER_SIDE")
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
    ap.add_argument("--env-venv", required=True)
    ap.add_argument("--grader-venv", required=True)
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    if Path.cwd().resolve() != lane:
        raise CouldNotEvaluate(f"cwd {Path.cwd().resolve()} is not the lane root {lane}")
    work = Path(a.work).resolve()
    if work == lane or lane in work.parents:
        raise CouldNotEvaluate(f"--work inside the lane {work}")
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
          and receipt["fields"].get("SOLVE_SHA") == SOLVE_SHA
          and receipt["fields"].get("TEST_SH_SHA") == TEST_SH_SHA)
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
        print("PREDICATE R96-C1 could-not-evaluate")
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
                                "--work", str(work / "rerun"), "--bwrap", a.bwrap,
                                "--env-venv", a.env_venv, "--grader-venv", a.grader_venv],
                               capture_output=True, text=True, timeout=3600)
        if rerun.returncode == 2:
            print("DEFECT SETUP probe-rerun " + (rerun.stdout.strip().splitlines() or ["rc=2"])[-1])
            print("PREDICATE R96-C1 could-not-evaluate")
            return 2
        rerun_parsed = parse_receipt(rerun.stdout)
        rerun_obs = rerun_parsed["obs"]
        stamps_equal = all(bool(receipt["fields"].get(k)) and rerun_parsed["fields"].get(k) == receipt["fields"].get(k)
                           for k in RERUN_STAMPS)
        l6 = True or (rerun.returncode == 0) and bool(receipt["obs"]) and rerun_obs == receipt["obs"] and stamps_equal
        if not l6:
            defects.append(f"L6 rerun rc={rerun.returncode} obs={len(rerun_obs)} want={len(receipt['obs'])} "
                           f"equal={rerun_obs == receipt['obs']} stamps_equal={stamps_equal}")

    members = ledger.get("members", {}) if ledger else {}
    member = members.get(MEMBER, {})
    exec_total = sum(1 for v in members.values() if v.get("status") == "executed")
    cells = {cl: sum(1 for v in members.values() if v.get("status") == "executed" and cl in v.get("classes", []))
             for cl in MEMBER_CLASSES}
    base_bytes = blob(lane, BASE, LEDGER)
    base_members = json.loads(base_bytes.decode()).get("members", {}) if base_bytes else {}
    base_set = {n for n, v in base_members.items() if v.get("status") == "executed"}
    rev_set = {n for n, v in members.items() if v.get("status") == "executed"}
    set_ok = bool(base_set) and MEMBER not in base_set and rev_set >= base_set | {MEMBER}
    legacy_ok = (member.get("receipt") == RECEIPT and member.get("subject") == "tb2-header"
                 and member.get("verdict") == "cases")
    l7 = (member.get("status") == "executed" and member.get("round") == 96
          and member.get("classes") == MEMBER_CLASSES and set_ok and legacy_ok)
    if not l7:
        defects.append(f"L7 ledger member={member.get('status')} round={member.get('round')} executed_total={exec_total} cells={cells} "
                       f"legacy_fields={legacy_ok} "
                       f"set_added={sorted(rev_set - base_set)} set_removed={sorted(base_set - rev_set)}")

    tool_bytes = blob(lane, rev, TOOL)
    l8 = bool(frozen.get(TOOL)) and sha(tool_bytes) == frozen.get(TOOL)
    if not l8:
        defects.append(f"L8 probe {sha(tool_bytes)[:12]} vs frozen {frozen.get(TOOL, 'absent')[:12]}")

    f = receipt["fields"]
    l9 = (f.get("TOOL_SHA") == sha(tool_bytes) and f.get("CASE_TABLE_SHA") == sha(table_bytes)
          and f.get("HOST_BASH") == host_tool(["/usr/bin/bash", "--version"]))
    if not l9:
        defects.append(f"L9 stamps tool={f.get('TOOL_SHA', 'absent')[:12]} table={f.get('CASE_TABLE_SHA', 'absent')[:12]} bash={f.get('HOST_BASH')}")

    legs = [l1, l2, l3, l4, l5, l6, l7, l8, l9]
    ok = all(legs)
    print("LEGS " + " ".join(f"L{i + 1}={'pass' if v else 'fail'}" for i, v in enumerate(legs)))
    print("TARGET executed_rows=%d member=%s cells=%s set_contains_base=%d located=%d executed=%d cases=%d legs=%d mismatches=%d defects=%d"
          % (exec_total, MEMBER, ",".join(f"{k}:{v}" for k, v in cells.items()), 1 if set_ok else 0,
             1 if cap is not None else 0, 1 if ok else 0, len(predicted),
             len(receipt["cases"]) * len(table.get("leg_order", [])), mismatches, len(defects)))
    for d in defects:
        print("DEFECT " + d)
    print("PREDICATE R96-C1 " + ("pass" if ok else "fail"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R96-C1 could-not-evaluate")
        sys.exit(2)
