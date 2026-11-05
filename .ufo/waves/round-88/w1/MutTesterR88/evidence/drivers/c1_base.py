#!/usr/bin/env python3
"""R88-C1 counter — located offline replay of the captured `fix-git` grader, at a measured revision.

Reads every frozen input from git objects at `--rev`, never from the working tree. Eight named legs,
one verdict each. One `DEFECT <leg> <detail>` line per failed leg, then one `TARGET` line and one
`PREDICATE` line:

  L1-receipt    the receipt named by RECEIPT exists at the measured revision
  L2-stamp      its stamp carries every required field and MEMBER/SUBJECT_CAPTURE/SUBJECT_SHA/
                CASE_TABLE_SHA/TOOL/TOOL_SHA/WORKTREE/EXIT agree with the bytes at the measured revision
  L3-tip        its LANE_TIP is a resolvable commit that is an ancestor of the measured revision
  L4-table      the case table at the measured revision is byte-identical to the table at FREEZE_REV
  L5-vectors    the receipt's eight CASE lines carry the frozen predicted vectors with observed == predicted,
                and its summary and PREDICATE lines read cases=8 legs=16 mismatches=0 / pass
  L6-reproduce  re-running the probe from an extraction of the measured tree reproduces the receipt's
                observation block line for line
  L7-ledger     the population ledger marks the member executed in round 88 with this receipt
  L8-subject    the captured grader bytes at the measured revision hash to the frozen SUBJECT_SHA

Honest limit: L6 reproduces the observation; it does not authenticate an author. L2/L3 are what a copy
minted elsewhere does not satisfy.

Usage:  python3 plans/round88_c1_replay.py --lane <repo> --rev <rev> --work <scratch dir>
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

FREEZE_REV = "0220c2f9f356bf032bd58b4ed39e32f6e26fa440"  # round-88 claims commit A (frozen inputs)
MEMBER = "fix-git"
CAP = "corpus/evidence/round52/graders/fix-git/tests/test_outputs.py"
TABLE = "plans/round88-cases.json"
TOOL = "plans/round88_fixgit_probe.py"
RECEIPT = "corpus/evidence/round88/fix-git-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
SUBJECT_SHA = "a8a6f51eb0d7c4ebdf0813c8f0b645edf29c995f1f9faf2aca3886a6713043f3"
LEDGER_ROUND = 88
LEDGER_SUBJECT = "tb2-header"
LEDGER_VERDICT = "cases"
FROZEN = (("exact", "P/P"), ("about-content-mismatch", "F/P"), ("layout-content-mismatch", "P/F"),
          ("both-content-mismatch", "F/F"), ("about-new-absent", "F/P"),
          ("trailing-whitespace-tolerance", "P/P"), ("about-new-is-dir", "E/P"),
          ("layout-old-is-dir", "P/E"))
REQUIRED = ("MEMBER", "SUBJECT_CAPTURE", "SUBJECT_SHA", "CASE_TABLE_SHA", "TOOL", "TOOL_SHA",
            "HOST_PYTHON", "HOST_OPENSSL", "LANE_TIP", "WORKTREE", "COMMAND", "EXIT")
CASE_RE = re.compile(r"^CASE (\S+) predicted=(\S+) observed=(\S+)$")
SUMMARY = "cases=8 legs=16 mismatches=0"
PRED_LINE = "PREDICATE R88-PROBE pass"
LEGS = ("L1-receipt", "L2-stamp", "L3-tip", "L4-table", "L5-vectors", "L6-reproduce",
        "L7-ledger", "L8-subject")


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


def ledger_row(lane: Lane) -> dict | None:
    raw = lane.blob(LEDGER)
    if raw is None:
        return None
    return json.loads(raw)["members"].get(MEMBER)


def run(lane_root: Path, rev: str, work: Path) -> int:
    lane = Lane(lane_root, rev)
    defects: list[str] = []
    try:
        rev_sha = lane.resolve()
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R88-C1 could-not-evaluate")
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

    # L8 — the captured grader bytes are the frozen subject
    if capture is None:
        defect("L8-subject", f"{CAP} absent at {rev_sha[:12]}")
    elif sha256(capture) != SUBJECT_SHA:
        defect("L8-subject", f"sha={sha256(capture)[:16]} != frozen")

    # L4 — the table is the frozen table
    if table is None or frozen_table is None:
        defect("L4-table", f"{TABLE} absent at {'measured' if table is None else 'FREEZE_REV'}")
    elif table != frozen_table:
        defect("L4-table", f"table sha={sha256(table)[:16]} != frozen {sha256(frozen_table)[:16]}")

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

    # L2 — the stamp is consistent with the measured bytes
    if receipt_raw is not None:
        missing = [key for key in REQUIRED if key not in stamp]
        if missing:
            defect("L2-stamp", f"missing {','.join(missing)}")
        expect = {
            "MEMBER": MEMBER,
            "SUBJECT_CAPTURE": CAP,
            "SUBJECT_SHA": sha256(capture) if capture is not None else "absent",
            "CASE_TABLE_SHA": sha256(table) if table is not None else "absent",
            "TOOL": TOOL,
            "TOOL_SHA": sha256(tool) if tool is not None else "absent",
            "WORKTREE": "clean",
            "EXIT": "0",
        }
        for key, value in expect.items():
            if stamp.get(key) != value:
                defect("L2-stamp", f"{key}={stamp.get(key)!r} != measured {value!r}")

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
        with tempfile.TemporaryDirectory(prefix="r88c1-tree-", dir=work) as temp:
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

    # L7 — the ledger marks the member executed in round 88 with this receipt
    row = ledger_row(lane)
    if row is None:
        defect("L7-ledger", f"{LEDGER} has no {MEMBER} row at {rev_sha[:12]}")
    elif (row.get("status"), row.get("round"), row.get("receipt"), row.get("subject"),
          row.get("verdict")) != ("executed", LEDGER_ROUND, RECEIPT, LEDGER_SUBJECT, LEDGER_VERDICT):
        defect("L7-ledger", f"row {json.dumps(row, sort_keys=True)}")

    raw_ledger = lane.blob(LEDGER)
    executed_rows = (sum(1 for v in json.loads(raw_ledger)["members"].values()
                         if v.get("status") == "executed") if raw_ledger else "absent")
    cases = len(observed_cases)
    legs = 2 * cases
    mismatches = sum(1 for _, p, o in observed_cases if p != o)
    located = int(not any(d.startswith(("L1", "L2", "L3", "L4", "L5", "L6", "L8")) for d in defects))
    executed = int(located and not any(d.startswith("L7") for d in defects))
    print(f"TARGET executed_rows={executed_rows} member={MEMBER} located={located} executed={executed} "
          f"cases={cases} legs={legs} mismatches={mismatches} defects={len(defects)}")
    verdict = "pass" if not defects else "fail"
    print(f"PREDICATE R88-C1 {verdict}")
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
