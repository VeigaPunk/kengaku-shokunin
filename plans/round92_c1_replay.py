#!/usr/bin/env python3
"""R92-C1 counter — the tenth located offline replay, `llm-inference-batching-scheduler` (round 92).

Mirrors plans/round91_c1_replay.py leg-for-leg with the positional case-id parser and the
guarded host probes applied from birth (round-92 M7/M12 discipline). Every input is read at
the measured revision; every host probe degrades to a guarded value instead of crashing.

Usage:  python3 plans/round92_c1_replay.py --lane <repo> --rev <rev> --work <scratch dir>
Exit:   0 predicate pass, 1 a leg failed, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tarfile
from io import BytesIO
from pathlib import Path


def _r96_set_at(lane_root, rev: str, path: str) -> set:
    """Round-96 L7 re-key: the executed member set of the ledger at a fixed commit."""
    proc = subprocess.run(["git", "-C", str(lane_root), "show", f"{rev}:{path}"], capture_output=True, timeout=120)
    if proc.returncode != 0:
        return set()
    return {n for n, v in json.loads(proc.stdout.decode()).get("members", {}).items() if v.get("status") == "executed"}

CAP = "corpus/evidence/round92/graders/llm-inference-batching-scheduler/tests/test_outputs.py"
TABLE = "plans/round92-cases.json"
TOOL = "plans/round92_bs_probe.py"
RECEIPT = "corpus/evidence/round92/bs-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
PINS = "plans/counter-pins-r91.json"
MEMBER = "llm-inference-batching-scheduler"
MEMBER_CLASSES = ["crypto-credential", "file-artifact", "filesystem-metadata", "serialization-schema"]
SUBJECT_SHA = "80b06b7c4ba0db28832b767d48be74bb462d7f5df5798d9cb58c4f1160d96ffa"
INPUT1_SHA = "8b3cf1e2b06074162038064dd2c114abe308acd32cec7d365ee63ee81978f7de"
INPUT2_SHA = "e15e2d4c4d55f875c42a6042610d6282f6c0657c39d3e0d0f087268252525cb5"
FREEZE_COMMIT = "96f249e05a88c8a81a49a380c72e0c6bfec82480"  # commit A
TABLE_SHA_A = "2249d5c0ea90930a5c36300b47a4b991d41ae9c5ff400deba5adf9be28d5a693"
AFTER_CELLS = {"crypto-credential": 4, "file-artifact": 27, "filesystem-metadata": 4,
               "serialization-schema": 5}
EXECUTED_AFTER = 36
SET_BASE = "4ba56182307ccda1ec436bfe3d61cb3d92e56608"  # round-92 BASE; L7 keyed to its executed set (round 96)
BWRAP = "/usr/bin/bwrap"


class CouldNotEvaluate(Exception):
    pass


class Lane:
    def __init__(self, root: Path):
        self.root = root

    def git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, timeout=120)

    def resolve(self, rev: str) -> str:
        proc = self.git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
        if proc.returncode != 0:
            raise CouldNotEvaluate(f"unresolved-revision {rev}")
        return proc.stdout.decode().strip()

    def blob(self, path: str, rev: str) -> bytes | None:
        proc = self.git("show", f"{rev}:{path}")
        return proc.stdout if proc.returncode == 0 else None


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_receipt(text: str) -> dict:
    """Case ids are positional token 1 of the CASE line (round-92 M7 discipline)."""
    fields: dict[str, str] = {}
    cases: list[tuple[str, str, str]] = []
    in_obs = False
    for line in text.splitlines():
        if line == "OBSERVATIONS_BEGIN":
            in_obs = True
            continue
        if line == "OBSERVATIONS_END":
            in_obs = False
            continue
        if in_obs and line.startswith("CASE "):
            tokens = line.split()[1:]
            cid = tokens[0] if tokens else "?"
            parts = {}
            for token in tokens[1:]:
                if "=" in token:
                    key, _, value = token.partition("=")
                    parts[key] = value
            cases.append((cid, parts.get("predicted", "?"), parts.get("observed", "?")))
        elif " " in line and not line.startswith("#"):
            key, _, value = line.partition(" ")
            if key.isupper() or key in ("mismatches",):
                fields[key] = value.strip()
    return {"fields": fields, "cases": cases}


def receipt_observation_lines(text: str) -> list[str]:
    lines: list[str] = []
    in_obs = False
    for line in text.splitlines():
        if line == "OBSERVATIONS_BEGIN":
            in_obs = True
            continue
        if line == "OBSERVATIONS_END":
            in_obs = False
            continue
        if in_obs:
            lines.append(line)
    return lines


def guarded_run(args: list[str], timeout: int = 60) -> str:
    """A host probe degrades to 'absent'; it never crashes the counter (M12)."""
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return "absent"
    text = (proc.stdout or proc.stderr).strip()
    return text.splitlines()[0] if text else "absent"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--work", required=True)
    args = parser.parse_args(argv)
    lane = Lane(Path(args.lane).resolve())
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    try:
        rev = lane.resolve(args.rev)
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R92-C1 could-not-evaluate")
        return 2

    defects: list[str] = []
    table_bytes = lane.blob(TABLE, rev)
    table = json.loads(table_bytes.decode()) if table_bytes is not None else {}
    ledger_bytes = lane.blob(LEDGER, rev)
    ledger = json.loads(ledger_bytes.decode()) if ledger_bytes is not None else {}

    receipt_bytes = lane.blob(RECEIPT, rev)
    # L1: the receipt exists and is committed at the measured revision
    l1 = receipt_bytes is not None
    if not l1:
        defects.append("L1 receipt absent at revision: %s" % RECEIPT)
    receipt = parse_receipt(receipt_bytes.decode(errors="replace")) if receipt_bytes else {"fields": {}, "cases": []}

    # L2: the captured grader bytes and both pinned input files at the measured revision hash
    cap_bytes = lane.blob(CAP, rev)
    in1 = lane.blob("corpus/evidence/round92/graders/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_1.jsonl", rev)
    in2 = lane.blob("corpus/evidence/round92/graders/llm-inference-batching-scheduler/environment/task_file/input_data/requests_bucket_2.jsonl", rev)
    l2 = (cap_bytes is not None and sha(cap_bytes) == SUBJECT_SHA
          and in1 is not None and sha(in1) == INPUT1_SHA
          and in2 is not None and sha(in2) == INPUT2_SHA
          and receipt["fields"].get("SUBJECT_SHA") == SUBJECT_SHA)
    if not l2:
        defects.append("L2 subject/input sha mismatch (cap=%s in1=%s in2=%s receipt=%s)"
                       % (sha(cap_bytes) if cap_bytes else "absent",
                          sha(in1) if in1 else "absent",
                          sha(in2) if in2 else "absent",
                          receipt["fields"].get("SUBJECT_SHA", "absent")))

    # L3: the receipt's LANE_TIP is an ancestor of the measured revision
    tip = receipt["fields"].get("LANE_TIP", "")
    proc = lane.git("merge-base", "--is-ancestor", tip, rev) if tip else None
    l3 = bool(tip) and proc is not None and proc.returncode == 0
    if not l3:
        defects.append("L3 LANE_TIP %s not an ancestor of %s" % (tip or "absent", rev[:12]))

    # L4: the case table at the measured revision is byte-identical to the freeze commit's
    a_bytes = lane.blob(TABLE, FREEZE_COMMIT)
    l4 = (table_bytes is not None and a_bytes is not None
          and sha(table_bytes) == TABLE_SHA_A and sha(a_bytes) == TABLE_SHA_A)
    if not l4:
        defects.append("L4 case table not byte-identical to freeze commit (rev=%s A=%s)"
                       % (sha(table_bytes) if table_bytes else "absent",
                          sha(a_bytes) if a_bytes else "absent"))

    # L5: every case's receipt-observed vector equals its frozen predicted vector
    predicted = {c["id"]: c["predicted"] for c in table.get("cases", [])}
    mismatches = 0
    for cid, pred, obs in receipt["cases"]:
        if cid not in predicted:
            mismatches += 1
            defects.append("L5 receipt names unknown case %s" % cid)
        elif obs != pred or pred != predicted[cid]:
            mismatches += 1
            defects.append("L5 case %s predicted=%s observed=%s frozen=%s" % (cid, pred, obs, predicted[cid]))
    l5 = bool(receipt["cases"]) and mismatches == 0 and len(receipt["cases"]) == len(predicted)
    if not l5 and not any(d.startswith("L5") for d in defects):
        defects.append("L5 case coverage %d of %d" % (len(receipt["cases"]), len(predicted)))

    # L6: the probe re-run from an extraction of the measured tree reproduces the receipt's
    #     observation block; a sandbox outage is could-not-evaluate, never a pass
    if not Path(BWRAP).exists():
        print("DEFECT SETUP sandbox-unavailable %s" % BWRAP)
        print("PREDICATE R92-C1 could-not-evaluate")
        return 2
    try:
        userns_now = int(Path("/proc/sys/user/max_user_namespaces").read_text().strip())
    except (OSError, ValueError):
        userns_now = 0
    if userns_now <= 0:
        print("DEFECT SETUP user namespaces unavailable (%d)" % userns_now)
        print("PREDICATE R92-C1 could-not-evaluate")
        return 2
    extract = work / "extract"
    rerun = work / "rerun"
    extract.mkdir(parents=True, exist_ok=True)
    rerun.mkdir(parents=True, exist_ok=True)
    archive = lane.git("archive", rev)
    if archive.returncode != 0:
        print("DEFECT SETUP archive failed %s" % archive.stderr.decode(errors="replace")[:120])
        print("PREDICATE R92-C1 could-not-evaluate")
        return 2
    with tarfile.open(fileobj=BytesIO(archive.stdout)) as tar:
        tar.extractall(extract)
    rerun_proc = subprocess.run(
        [sys.executable, "-I", "-B", str(extract / TOOL), "--lane", str(extract), "--work", str(rerun)],
        capture_output=True, text=True, timeout=900)
    rerun_obs = receipt_observation_lines(rerun_proc.stdout)
    want_obs = receipt_observation_lines(receipt_bytes.decode(errors="replace")) if receipt_bytes else []
    l6 = rerun_proc.returncode == 0 and rerun_obs == want_obs and bool(want_obs)
    if not l6:
        defects.append("L6 rerun rc=%d obs=%d want=%d" % (rerun_proc.returncode, len(rerun_obs), len(want_obs)))

    # L7: the ledger at the measured revision carries the member executed round 92 with the
    #     four class cells incremented by exactly one
    member = ledger.get("members", {}).get(MEMBER, {}) if ledger else {}
    exec_total = sum(1 for v in ledger.get("members", {}).values() if v.get("status") == "executed") if ledger else 0
    cells_ok = all(sum(1 for v in ledger.get("members", {}).values()
                       if v.get("status") == "executed" and cl in v.get("classes", [])) >= want
                   for cl, want in AFTER_CELLS.items())
    # round-96 re-key: the executed SET must contain the round-92 set (BASE plus this member)
    rev_set = {n for n, v in ledger.get("members", {}).items() if v.get("status") == "executed"} if ledger else set()
    base_set = _r96_set_at(Path(args.lane).resolve(), SET_BASE, LEDGER)
    set_ok = bool(base_set) and MEMBER not in base_set and rev_set >= base_set | {MEMBER}
    l7 = (member.get("status") == "executed" and member.get("round") == 92
          and member.get("classes") == MEMBER_CLASSES and set_ok
          and cells_ok)
    if not l7:
        defects.append("L7 ledger member=%s round=%s executed_total=%s cells_ok=%s set_ok=%s"
                       % (member.get("status"), member.get("round"), exec_total, cells_ok, set_ok))

    # L8: the probe bytes at the measured revision hash to the ledger's pin for the tool
    pins_bytes = lane.blob(PINS, rev)
    tool_pin = None
    if pins_bytes is not None:
        try:
            pins = json.loads(pins_bytes.decode())
            for entry in pins.get("entries", []):
                if entry.get("path") == TOOL and entry.get("kind") == "sha":
                    tool_pin = entry.get("sha256")
        except json.JSONDecodeError:
            tool_pin = None
    tool_bytes = lane.blob(TOOL, rev)
    l8 = tool_pin is not None and tool_bytes is not None and sha(tool_bytes) == tool_pin
    if not l8:
        defects.append("L8 probe pin %s vs bytes %s"
                       % (tool_pin or "unreadable", sha(tool_bytes) if tool_bytes else "absent"))

    # L9: the receipt stamp fields verify against the measured tree and the live host
    #     (guarded probes: an absent tool degrades the stamp, never a crash)
    py_now_line = guarded_run([sys.executable, "-V"])
    _py = subprocess.run([sys.executable, "-V"], capture_output=True, text=True)
    py_now_line = ((_py.stderr or _py.stdout).strip().splitlines()[0]
                   if (_py.stderr or _py.stdout).strip() else "absent")
    oss_line = guarded_run(["openssl", "version"])
    try:
        userns_txt = Path("/proc/sys/user/max_user_namespaces").read_text().strip()
    except OSError:
        userns_txt = "absent"
    stamp_ok = (receipt["fields"].get("TOOL_SHA") == (sha(lane.blob(TOOL, rev)) if lane.blob(TOOL, rev) else None)
                and receipt["fields"].get("CASE_TABLE_SHA") == (sha(table_bytes) if table_bytes else None)
                and receipt["fields"].get("HOST_PYTHON") == py_now_line
                and receipt["fields"].get("HOST_OPENSSL") == oss_line
                and receipt["fields"].get("HOST_USERNS") == userns_txt)
    l9 = stamp_ok
    if not l9:
        defects.append("L9 stamp fields mismatch (tool=%s table=%s python=%s openssl=%s userns=%s)"
                       % (receipt["fields"].get("TOOL_SHA"), receipt["fields"].get("CASE_TABLE_SHA"),
                          receipt["fields"].get("HOST_PYTHON"), receipt["fields"].get("HOST_OPENSSL"),
                          receipt["fields"].get("HOST_USERNS")))

    legs = [l1, l2, l3, l4, l5, l6, l7, l8, l9]
    all_pass = all(legs)
    located = 1 if cap_bytes is not None else 0
    print("TARGET executed_rows=%d member=%s located=%d executed=%d cases=%d legs=%d mismatches=%d defects=%d"
          % (EXECUTED_AFTER if (ledger and exec_total == EXECUTED_AFTER) else exec_total,
             MEMBER, located, 1 if all_pass else 0,
             len(predicted), len(receipt["cases"]) * len(table.get("leg_order", [])),
             mismatches, len(defects)))
    for d in defects:
        print("DEFECT %s" % d)
    print("PREDICATE R92-C1 %s" % ("pass" if all_pass else "fail"))
    return 0 if all_pass else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print("DEFECT SETUP %s" % error)
        print("PREDICATE R92-C1 could-not-evaluate")
        sys.exit(2)
