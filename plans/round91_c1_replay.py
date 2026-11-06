#!/usr/bin/env python3
"""R91-C1 counter — the ninth located offline replay, `modernize-scientific-stack` (round 91).

Reads the receipt, case table, pin ledger and population ledger from git objects at --rev and
checks the nine frozen legs L1-L9 (`plans/round-91-claims.md`, frozen at commit A). The TARGET
line prints `executed=1` only when every leg passes (round-90 ExecC1Battery F1); a failing leg is
a DEFECT line, never a silent pass. A sandbox outage at the L6 re-run is `DEFECT SETUP
sandbox-unavailable` + `PREDICATE could-not-evaluate` exit 2 (round-90 CriticFalsify F-7), never
a pass. The receipt stamp's TOOL_SHA, CASE_TABLE_SHA, HOST_PYTHON, HOST_OPENSSL and HOST_USERNS
are verified by leg L9 (round-90 SentinelForge forgery 1b passed with a decorative stamp).

Usage:  python3 plans/round91_c1_replay.py --lane <repo> --rev <rev> --work <scratch dir>
Exit:   0 predicate pass, 1 predicate fail, 2 could-not-evaluate.
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

CAP = "corpus/evidence/round52/graders/modernize-scientific-stack/tests/test_outputs.py"
TABLE = "plans/round91-cases.json"
TOOL = "plans/round91_modernize_probe.py"
RECEIPT = "corpus/evidence/round91/modernize-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
PINS = "plans/counter-pins-r91.json"
MEMBER = "modernize-scientific-stack"
SUBJECT_SHA = "0c24195ff46527764c7f8ceda9c608a189ab4a01619282942fcd27a2ea02a977"
FREEZE_COMMIT = "cd0c116ef8c453d076031bdf5888b1e1b83bb0be"  # commit A
TABLE_SHA_A = "89fab14b457364826065b77435626e0a16669abeebe67afe93ce6d2fe198ddf8"
AFTER_CELLS = {"file-artifact": 26, "filesystem-metadata": 3, "numeric-band": 4,
               "stdout-inspection": 11, "subprocess-exec": 13}
EXECUTED_AFTER = 35
BWRAP = "/usr/bin/bwrap"


class CouldNotEvaluate(Exception):
    pass


class Lane:
    def __init__(self, root: Path):
        self.root = root

    def git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(self.root), *args],
                              capture_output=True, timeout=120)

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


def receipt_observation_lines_from_probe_stdout(text: str) -> list[str]:
    return receipt_observation_lines(text)


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
        print("PREDICATE R91-C1 could-not-evaluate")
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

    # L2: the captured grader bytes at the measured revision hash to SUBJECT_SHA and the receipt agrees
    cap_bytes = lane.blob(CAP, rev)
    l2 = (cap_bytes is not None and sha(cap_bytes) == SUBJECT_SHA
          and receipt["fields"].get("SUBJECT_SHA") == SUBJECT_SHA)
    if not l2:
        defects.append("L2 subject sha mismatch (cap=%s receipt=%s)"
                       % (sha(cap_bytes) if cap_bytes else "absent",
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
                       % (sha(table_bytes) if table_bytes else "absent", sha(a_bytes) if a_bytes else "absent"))

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
        print("PREDICATE R91-C1 could-not-evaluate")
        return 2
    extract = work / "extract"
    rerun = work / "rerun"
    extract.mkdir(parents=True, exist_ok=True)
    rerun.mkdir(parents=True, exist_ok=True)
    archive = lane.git("archive", rev)
    if archive.returncode != 0:
        print("DEFECT SETUP archive failed %s" % archive.stderr.decode(errors='replace')[:120])
        print("PREDICATE R91-C1 could-not-evaluate")
        return 2
    with tarfile.open(fileobj=BytesIO(archive.stdout)) as tar:
        tar.extractall(extract)
    rerun_proc = subprocess.run(
        [sys.executable, "-I", "-B", str(extract / TOOL), "--lane", str(extract), "--work", str(rerun)],
        capture_output=True, text=True, timeout=600)
    rerun_obs = receipt_observation_lines_from_probe_stdout(rerun_proc.stdout)
    want_obs = receipt_observation_lines(receipt_bytes.decode(errors="replace")) if receipt_bytes else []
    l6 = rerun_proc.returncode == 0 and rerun_obs == want_obs and bool(want_obs)
    if not l6:
        defects.append("L6 rerun rc=%d obs=%d want=%d" % (rerun_proc.returncode, len(rerun_obs), len(want_obs)))

    # L7: the ledger at the measured revision carries the member executed round 91 with the
    #     five class cells incremented by exactly one
    member = ledger.get("members", {}).get(MEMBER, {}) if ledger else {}
    exec_total = sum(1 for v in ledger.get("members", {}).values() if v.get("status") == "executed") if ledger else 0
    cells_ok = all(sum(1 for v in ledger.get("members", {}).values()
                       if v.get("status") == "executed" and cl in v.get("classes", [])) == want
                   for cl, want in AFTER_CELLS.items())
    l7 = (member.get("status") == "executed" and member.get("round") == 91
          and member.get("classes") == table.get("class") and exec_total == EXECUTED_AFTER
          and cells_ok)
    if not l7:
        defects.append("L7 ledger member=%s executed_total=%d cells_ok=%s"
                       % (member.get("status"), exec_total, cells_ok))

    # L8: the probe bytes at the measured revision hash to the pinned TRUSTED_TOOL_SHA
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

    # L9: the receipt stamp fields verify against the measured tree and the live host.
    # Every host probe is guarded (round-92 M12): an absent tool or a failing probe
    # degrades the stamp to "absent" instead of crashing the counter unguarded.
    def guarded_run(args: list[str], timeout: int = 60) -> str:
        try:
            proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        except (OSError, subprocess.SubprocessError):
            return "absent"
        text = (proc.stdout or proc.stderr).strip()
        return text.splitlines()[0] if text else "absent"

    _py = subprocess.run([sys.executable, "-V"], capture_output=True, text=True)
    py_now_line = ((_py.stderr or _py.stdout).strip().splitlines()[0]
                   if (_py.stderr or _py.stdout).strip() else "absent")
    oss_line = guarded_run(["openssl", "version"])
    try:
        userns_now = Path("/proc/sys/user/max_user_namespaces").read_text().strip()
    except OSError:
        userns_now = "absent"
    if "absent" in (py_now_line, oss_line, userns_now):
        # fail-closed (round-92 M12): a host probe we cannot run must become DEFECT
        # SETUP at rc 2, never a silent stamp mismatch and never a crash
        raise CouldNotEvaluate("host probe absent (python=%s openssl=%s userns=%s)"
                               % (py_now_line, oss_line, userns_now))
    stamp_ok = (receipt["fields"].get("TOOL_SHA") == (sha(lane.blob(TOOL, rev)) if lane.blob(TOOL, rev) else None)
                and receipt["fields"].get("CASE_TABLE_SHA") == (sha(table_bytes) if table_bytes else None)
                and receipt["fields"].get("HOST_PYTHON") == py_now_line
                and receipt["fields"].get("HOST_OPENSSL") == oss_line
                and receipt["fields"].get("HOST_USERNS") == userns_now)
    l9 = stamp_ok
    if not l9:
        defects.append("L9 stamp fields mismatch (tool=%s table=%s python=%s openssl=%s userns=%s)"
                       % (receipt["fields"].get("TOOL_SHA"), receipt["fields"].get("CASE_TABLE_SHA"),
                          receipt["fields"].get("HOST_PYTHON"), receipt["fields"].get("HOST_OPENSSL"),
                          receipt["fields"].get("HOST_USERNS")))

    legs = [l1, l2, l3, l4, l5, l6, l7, l8, l9]
    all_pass = all(legs)
    exec_total_ledger = exec_total
    located = 1 if cap_bytes is not None else 0
    print("TARGET executed_rows=%d member=%s located=%d executed=%d cases=%d legs=%d mismatches=%d defects=%d"
          % (exec_total_ledger, MEMBER, located, 1 if all_pass else 0,
             len(predicted), len(receipt["cases"]) * len(table.get("legs", [])), mismatches, len(defects)))
    for d in defects:
        print("DEFECT %s" % d)
    print("PREDICATE R91-C1 %s" % ("pass" if all_pass else "fail"))
    return 0 if all_pass else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print("DEFECT SETUP %s" % error)
        print("PREDICATE R91-C1 could-not-evaluate")
        sys.exit(2)
