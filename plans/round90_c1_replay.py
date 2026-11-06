#!/usr/bin/env python3
"""R90-C1 counter — located offline replay of the captured `merge-diff-arc-agi-task` grader, at a
measured revision.

Reads every frozen input from git objects at `--rev`, never from the working tree. Eight named
legs, one verdict each. One `DEFECT <leg> <detail>` line per failed leg, then one `TARGET` line and
one `PREDICATE` line:

  L1-receipt    the receipt named by RECEIPT exists at the measured revision
  L2-subject    the captured grader bytes at the measured revision hash to the frozen SUBJECT_SHA
                and the receipt stamp's SUBJECT_SHA equals that hash
  L3-tip        the receipt's LANE_TIP is a resolvable commit that is an ancestor of the measured
                revision
  L4-table      the case table at the measured revision is byte-identical to the table at FREEZE_REV
  L5-vectors    the receipt's eight CASE lines carry the frozen predicted vectors with
                observed == predicted, and its summary and probe-predicate lines read
                cases=8 legs=40 mismatches=0 / PREDICATE R90-PROBE pass, with stamp EXIT 0
  L6-reproduce  re-running the probe from an extraction of the measured tree reproduces the
                receipt's observation block line for line
  L7-ledger     the population ledger marks the member executed in round 90 with this receipt,
                the executed count is 34 of 88, and the five member class cells equal the frozen
                after-values (git-plumbing 2 of 3, serialization-schema 4 of 10, file-artifact
                25 of 76, stdout-inspection 10 of 29, subprocess-exec 12 of 45)
  L8-tool       the probe bytes at the measured revision hash to TRUSTED_TOOL_SHA, a constant in
                this counter (round-88 forged-probe hole; the round-89 L9 pattern)

Honest limit: L6 reproduces the observation; it does not authenticate an author. L2/L3 are what a
copy minted elsewhere does not satisfy. L8 pins the probe, not the grader's execution environment,
and the counter itself is pinned externally by plans/counter-pins-r90.json (R90-C2), not by this
constant.

Usage:  python3 plans/round90_c1_replay.py --lane <repo> --rev <rev> --work <scratch dir>
Exit:   0 target reached, 1 at least one named defect, 2 could not evaluate (unresolved revision, no git).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from io import BytesIO
from pathlib import Path

FREEZE_REV = "45171d231f0444625106abf63cd4b0804d8812bd"  # round-90 claims commit A (frozen inputs)
MEMBER = "merge-diff-arc-agi-task"
CAP = "corpus/evidence/round52/graders/merge-diff-arc-agi-task/tests/test_outputs.py"
TABLE = "plans/round90-cases.json"
TOOL = "plans/round90_polydiff_probe.py"
TRUSTED_TOOL_SHA = "2c4f0ab1e0d456416f4fe114bb47c9207a89b8a594ac80861064bad1e1ad9be3"
RECEIPT = "corpus/evidence/round90/merge-diff-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
SUBJECT_SHA = "2754ba6c5c5f75c9db5ed2c5729d9f5d7e21cb7fdb18aa0c65abdc3e7e85c149"
LEDGER_ROUND = 90
LEDGER_SUBJECT = "tb2-header"
LEDGER_VERDICT = "cases"
EXECUTED_AFTER = 34
MEMBERS_TOTAL = 88
FROZEN_CELLS = {"git-plumbing": (2, 3), "serialization-schema": (4, 10), "file-artifact": (25, 76),
                "stdout-inspection": (10, 29), "subprocess-exec": (12, 45)}
FROZEN = (("full-solution", "PPPPP"), ("no-git-dir", "FFPPP"), ("one-branch", "PFPPP"),
          ("algo-missing", "PPFEE"), ("algo-syntax-error", "PPPEE"), ("map-wrong-values", "PPPPF"),
          ("test-json-corrupt", "PPPPE"), ("map-shape-short", "PPPPF"))
REQUIRED = ("MEMBER", "SUBJECT_CAPTURE", "SUBJECT_SHA", "CASE_TABLE_SHA", "TOOL", "TOOL_SHA",
            "HOST_PYTHON", "HOST_OPENSSL", "HOST_USERNS", "LANE_TIP", "WORKTREE", "COMMAND", "EXIT")
CASE_RE = re.compile(r"^CASE (\S+) predicted=(\S+) observed=(\S+)$")
SUMMARY = "cases=8 legs=40 mismatches=0"
PRED_LINE = "PREDICATE R90-PROBE pass"
LEGS = ("L1-receipt", "L2-subject", "L3-tip", "L4-table", "L5-vectors", "L6-reproduce",
        "L7-ledger", "L8-tool")
EXECUTED_LEGS = ("L1", "L2", "L3", "L4", "L5", "L6", "L8")


class CouldNotEvaluate(Exception):
    """An input the counter needs cannot be read at all."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Lane:
    def __init__(self, root: Path, rev: str):
        self.root = root
        self.rev = rev

    def git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, timeout=120)

    def resolve(self) -> str:
        proc = self.git("rev-parse", "--verify", "--quiet", f"{self.rev}^{{commit}}")
        if proc.returncode != 0:
            raise CouldNotEvaluate(f"unresolved-revision {self.rev}")
        return proc.stdout.decode().strip()

    def blob(self, path: str, rev: str | None = None) -> bytes | None:
        proc = self.git("show", f"{rev or self.rev}:{path}")
        return proc.stdout if proc.returncode == 0 else None

    def is_ancestor(self, ancestor: str, descendant: str) -> bool:
        return self.git("merge-base", "--is-ancestor", ancestor, descendant).returncode == 0

    def resolves(self, ref: str) -> str | None:
        proc = self.git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
        return proc.stdout.decode().strip() if proc.returncode == 0 else None

    def extract(self, dest: Path) -> None:
        proc = self.git("archive", self.rev)
        if proc.returncode != 0:
            raise CouldNotEvaluate("archive-failed")
        with tarfile.open(fileobj=BytesIO(proc.stdout)) as archive:
            archive.extractall(dest, filter="data")


def parse_stamp(text: str) -> dict[str, str]:
    stamp: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("OBSERVATIONS_BEGIN"):
            break
        if " " in line:
            key, value = line.split(" ", 1)
            stamp.setdefault(key, value)
    return stamp


def observation_block(text: str) -> list[str] | None:
    lines = text.splitlines()
    if "OBSERVATIONS_BEGIN" not in lines or "OBSERVATIONS_END" not in lines:
        return None
    begin = lines.index("OBSERVATIONS_BEGIN")
    end = lines.index("OBSERVATIONS_END")
    return lines[begin + 1:end]


def ledger_doc(lane: Lane) -> dict | None:
    raw = lane.blob(LEDGER)
    if raw is None:
        return None
    return json.loads(raw)


def run(lane_root: Path, rev: str, work: Path) -> int:
    lane = Lane(lane_root, rev)
    defects: list[str] = []
    try:
        rev_sha = lane.resolve()
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R90-C1 could-not-evaluate")
        return 2

    def defect(leg: str, detail: str) -> None:
        defects.append(leg)
        print(f"DEFECT {leg} {detail}")

    frozen_table = lane.blob(TABLE, FREEZE_REV)
    table = lane.blob(TABLE)
    capture = lane.blob(CAP)
    tool = lane.blob(TOOL)
    receipt_raw = lane.blob(RECEIPT)
    receipt = receipt_raw.decode("utf-8", errors="replace") if receipt_raw is not None else ""

    # L2 — the captured grader bytes are the frozen subject, and the receipt agrees
    subject_ok = False
    if capture is None:
        defect("L2-subject", f"{CAP} absent at {rev_sha[:12]}")
    elif sha256(capture) != SUBJECT_SHA:
        defect("L2-subject", f"sha={sha256(capture)[:16]} != frozen")
    else:
        subject_ok = True

    # L4 — the table is the frozen table
    if table is None or frozen_table is None:
        defect("L4-table", f"{TABLE} absent at {'measured' if table is None else 'FREEZE_REV'}")
    elif table != frozen_table:
        defect("L4-table", f"table sha={sha256(table)[:16]} != frozen {sha256(frozen_table)[:16]}")

    # L8 — the probe bytes are the pinned probe bytes
    if tool is None:
        defect("L8-tool", f"{TOOL} absent at {rev_sha[:12]}")
    elif sha256(tool) != TRUSTED_TOOL_SHA:
        defect("L8-tool", f"probe sha={sha256(tool)[:16]} != TRUSTED_TOOL_SHA {TRUSTED_TOOL_SHA[:16]}")

    # L1 — the receipt exists
    if receipt_raw is None:
        defect("L1-receipt", f"{RECEIPT} absent at {rev_sha[:12]}")

    stamp = parse_stamp(receipt)
    observed_block = observation_block(receipt) if receipt else None
    observed_cases: list[tuple[str, str, str]] = []
    summary = ""
    predicate = ""
    for line in observed_block or []:
        match = CASE_RE.match(line)
        if match:
            observed_cases.append(match.groups())
        elif line.startswith("cases="):
            summary = line
        elif line.startswith("PREDICATE"):
            predicate = line

    # L2 (receipt half) — the stamp's SUBJECT_SHA equals the measured subject hash
    if receipt_raw is not None and subject_ok:
        if stamp.get("SUBJECT_SHA") != SUBJECT_SHA:
            defect("L2-subject", f"stamp SUBJECT_SHA={stamp.get('SUBJECT_SHA')!r} != measured")

    # L3 — the stamp's LANE_TIP is a resolvable ancestor of the measured revision
    if receipt_raw is not None:
        tip = stamp.get("LANE_TIP", "")
        resolved = lane.resolves(tip) if tip and tip != "absent" else None
        if resolved is None:
            defect("L3-tip", f"LANE_TIP {tip!r} does not resolve to a commit")
        elif not lane.is_ancestor(resolved, rev_sha):
            defect("L3-tip", f"LANE_TIP {resolved[:12]} is not an ancestor of {rev_sha[:12]}")

    # L5 — the receipt's eight CASE lines carry the frozen vectors and read clean
    if receipt_raw is not None:
        if observed_block is None:
            defect("L5-vectors", "no OBSERVATIONS block")
        else:
            if tuple((c, p) for c, p, _ in observed_cases) != FROZEN:
                defect("L5-vectors", f"case set/predicted differs: {[c for c, _, _ in observed_cases]}")
            for case_id, predicted, observed in observed_cases:
                if observed != predicted:
                    defect("L5-vectors", f"{case_id} observed={observed} predicted={predicted}")
            if summary != SUMMARY:
                defect("L5-vectors", f"summary {summary!r}")
            if predicate != PRED_LINE:
                defect("L5-vectors", f"predicate {predicate!r}")
            if stamp.get("EXIT") != "0":
                defect("L5-vectors", f"EXIT {stamp.get('EXIT')!r}")

    # L6 — the probe re-run from an extraction of the measured tree reproduces the observation block
    if receipt_raw is not None and tool is not None:
        work.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="r90c1-tree-", dir=work) as temp:
            tree = Path(temp) / "tree"
            tree.mkdir()
            lane.extract(tree)
            proc = subprocess.run(
                [sys.executable, "-I", "-B", str(tree / TOOL), "--lane", str(tree),
                 "--work", str(Path(temp) / "probe-work")],
                capture_output=True, text=True, timeout=900,
                env={"PATH": "/usr/bin", "TMPDIR": str(work)})
            rerun = observation_block(proc.stdout) if proc.stdout else None
            if rerun is None:
                defect("L6-reproduce", f"probe re-run rc={proc.returncode} produced no observation block")
            elif rerun != observed_block:
                defect("L6-reproduce", "re-run observation block differs from the receipt")
    elif receipt_raw is not None:
        defect("L6-reproduce", f"{TOOL} absent at {rev_sha[:12]}")

    # L7 — the ledger marks the member executed in round 90 with this receipt and the frozen cells
    doc = ledger_doc(lane)
    row = doc["members"].get(MEMBER) if doc else None
    if row is None:
        defect("L7-ledger", f"{LEDGER} has no {MEMBER} row at {rev_sha[:12]}")
    else:
        if (row.get("status"), row.get("round"), row.get("receipt"), row.get("subject"),
                row.get("verdict")) != ("executed", LEDGER_ROUND, RECEIPT, LEDGER_SUBJECT, LEDGER_VERDICT):
            defect("L7-ledger", f"row {json.dumps(row, sort_keys=True)}")
        if doc:
            members = doc["members"]
            executed_rows = sum(1 for v in members.values() if v.get("status") == "executed")
            if executed_rows != EXECUTED_AFTER or len(members) != MEMBERS_TOTAL:
                defect("L7-ledger", f"executed={executed_rows} members={len(members)} "
                                    f"!= frozen {EXECUTED_AFTER} of {MEMBERS_TOTAL}")
            cells: dict[str, list[int]] = {}
            for m, v in members.items():
                for c in v.get("classes", []):
                    slot = cells.setdefault(c, [0, 0])
                    slot[1] += 1
                    if v.get("status") == "executed":
                        slot[0] += 1
            for c, (want_done, want_total) in FROZEN_CELLS.items():
                got = cells.get(c, [0, 0])
                if (got[0], got[1]) != (want_done, want_total):
                    defect("L7-ledger", f"cell {c} {got[0]} of {got[1]} != frozen "
                                        f"{want_done} of {want_total}")

    raw_ledger = lane.blob(LEDGER)
    executed_print = (sum(1 for v in json.loads(raw_ledger)["members"].values()
                          if v.get("status") == "executed") if raw_ledger else "absent")
    cases = len(observed_cases)
    legs = cases * 5
    mismatches = sum(1 for _, p, o in observed_cases if p != o)
    located = int(subject_ok)
    executed = int(located and not any(d.startswith("L7") for d in defects))
    print(f"TARGET executed_rows={executed_print} member={MEMBER} located={located} executed={executed} "
          f"cases={cases} legs={legs} mismatches={mismatches} defects={len(defects)}")
    verdict = "pass" if not defects else "fail"
    print(f"PREDICATE R90-C1 {verdict}")
    return 0 if not defects else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--rev", required=True)
    parser.add_argument("--work", required=True)
    args = parser.parse_args(argv)
    return run(Path(args.lane).resolve(), args.rev, Path(args.work).resolve())


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
