#!/usr/bin/env python3
"""R98-C1 counter — the sixteenth located offline replay, `regex-chess` (round 98).

Legs, every input read at the measured revision (round-92 discipline: positional case ids,
guarded host probes, no skip flags):

  L1 the receipt is committed at --rev
  L2 the seven flat captures the probe stages hash to their pins, and the receipt names the same
     subject, test.sh and solve.sh
  L3 the receipt's LANE_TIP is an ancestor of --rev
  L4 the case table at --rev hashes to the sha the round's frozen-instruments table holds at the
     freeze commit (the single commit that added plans/round-98-claims.md)
  L5 every receipt case vector equals its frozen predicted vector (all cases, no extras)
  L6 the probe re-run from a `git archive` of --rev reproduces the receipt's observation block
     exactly (CASE and DETAIL lines) and the same TOOL_SHA / CASE_TABLE_SHA / GRADER_SIDE stamps;
     the sandbox is fixed at /usr/bin/bwrap (round-97 MutC1: no injectable sandbox path)
  L7 the ledger at --rev holds the member executed round 98 with its two classes and the
     legacy-gate fields receipt=<this receipt>, subject=tb2-header, verdict=cases, and the executed
     member SET at --rev EQUALS the set at BASE 49a1c4f1 plus this member — an extra unearned
     member or a removed one is a fail (round-97 MutC1: superset let an extra member pass)
  L8 the probe bytes at --rev hash to the frozen-instruments table's probe sha
  L9 the receipt stamps (TOOL_SHA, CASE_TABLE_SHA, HOST_BASH) match the measured tree and host
  L10 the BASE bytes of `plans/anchor_digest_check.py`, run on a `git clone --shared` checkout of
     --rev, print no DEFECT line for any SOURCES row absent at BASE (this claim's own rows)

The counter refuses (rc 2) unless the process cwd is the lane root.

Usage:  python3 plans/round98_c1_replay.py --lane <repo> --rev <rev> --work <dir> --grader-venv <dir>
Exit:   0 predicate pass, 1 a leg failed, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
from io import BytesIO
from pathlib import Path

CAPDIR = "corpus/evidence/round98/tb2-regex-chess"
CAP = CAPDIR + "/test_outputs.py"
PINS = {
    "test_outputs.py": "4983c44d21c56dd8191381eff0304afc8b87bb714527ea9036b3319c015a30b4",
    "test.sh": "8f7f00a1c4dde7fcca6c918c768f2aba432b8c4007c15989716c68091950da87",
    "solve.sh": "b728bf0ea392a3d244afbd0818d36933c8d3e190e47743c1382cd518d518a2e9",
    "Dockerfile": "2616cd775252303839dfda0ee2f047eb862952b053b0103bd6b2460ef90c11b7",
    "check.py": "f9c416ae9ea01dcdd5f6a43170c8434b8c0a0b389a4a30876a2048e277d191c7",
    "task.toml": "07fe52636fcc4bc9fff25d5630af145b97a5331219d719cc8decb4ca67ea21d4",
    "instruction.md": "a6ed3fcc54fc92d71a84af921942422d299ca89b410dcd92cd05a53d0d06436c",
}
TABLE = "plans/round98-cases.json"
TOOL = "plans/round98_regexchess_probe.py"
RECEIPT = "corpus/evidence/round98/regexchess-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
CLAIMS = "plans/round-98-claims.md"
SOURCES = "corpus/SOURCES.md"
GATE = "plans/anchor_digest_check.py"
MEMBER = "regex-chess"
MEMBER_CLASSES = ["file-artifact", "serialization-schema"]
SUBJECT_SHA = PINS["test_outputs.py"]
TEST_SH_SHA = PINS["test.sh"]
SOLVE_SHA = PINS["solve.sh"]
BASE = "49a1c4f1097db7c923da56d4213cad75772ed1c0"
BWRAP = "/usr/bin/bwrap"
RERUN_STAMPS = ("TOOL_SHA", "CASE_TABLE_SHA", "GRADER_SIDE")
ROW = re.compile(r"^([0-9a-f]{64})  (\S+)$")
ROWID = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|", re.M)
DEFECT = re.compile(r"^DEFECT (S\d{3,}) ")


class CouldNotEvaluate(Exception):
    pass


def sha(data: bytes | None) -> str:
    return hashlib.sha256(data).hexdigest() if data is not None else "absent"


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=300)


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


def new_row_defects(lane: Path, rev: str, work: Path) -> tuple[list[str], list[str]]:
    """(rows added after BASE, those of them the BASE gate flags at rev)."""
    base_ids = set(ROWID.findall((blob(lane, BASE, SOURCES) or b"").decode(errors="replace")))
    rev_ids = set(ROWID.findall((blob(lane, rev, SOURCES) or b"").decode(errors="replace")))
    added = sorted(rev_ids - base_ids, key=lambda s: int(s[1:]))
    gate_bytes = blob(lane, BASE, GATE)
    if gate_bytes is None:
        raise CouldNotEvaluate("gate absent at BASE")
    gate = work / "gate-base.py"
    gate.write_bytes(gate_bytes)
    tree = work / "gate-tree"
    if tree.exists():
        shutil.rmtree(tree)
    proc = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", str(lane), str(tree)],
                          capture_output=True, timeout=300)
    if proc.returncode != 0 or git(tree, "-c", "advice.detachedHead=false", "checkout", "-q", rev).returncode != 0:
        raise CouldNotEvaluate("gate fixture checkout failed")
    if git(tree, "rev-parse", "--show-toplevel").stdout.decode().strip() != str(tree):
        raise CouldNotEvaluate("gate fixture toplevel mismatch")
    try:
        run = subprocess.run([sys.executable, "-I", "-B", str(gate), "--lane", str(tree)],
                             capture_output=True, text=True, timeout=1200, cwd=str(tree))
    finally:
        shutil.rmtree(tree, ignore_errors=True)
    if run.returncode not in (0, 1):
        raise CouldNotEvaluate(f"gate rc={run.returncode}")
    flagged = sorted({m.group(1) for m in map(DEFECT.match, run.stdout.splitlines()) if m and m.group(1) in added},
                     key=lambda s: int(s[1:]))
    return added, flagged


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--work", required=True)
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

    if not (Path(BWRAP).is_file() and os.access(BWRAP, os.X_OK)):
        print(f"DEFECT SETUP sandbox-unavailable {BWRAP}")
        print("PREDICATE R98-C1 could-not-evaluate")
        return 2
    tool_at_rev = blob(lane, rev, TOOL)
    if tool_at_rev is None:
        l6 = False
        defects.append(f"L6 probe absent at revision: {TOOL}")
    else:
        extract = work / "extract"
        if extract.exists():
            shutil.rmtree(extract)
        extract.mkdir(parents=True)
        archive = git(lane, "archive", rev)
        if archive.returncode != 0:
            raise CouldNotEvaluate("git archive failed")
        with tarfile.open(fileobj=BytesIO(archive.stdout)) as tar:
            tar.extractall(extract, filter="data")
        try:
            rerun = subprocess.run([sys.executable, "-I", "-B", str(extract / TOOL), "--lane", str(extract),
                                    "--work", str(work / "rerun"), "--grader-venv", a.grader_venv],
                                   capture_output=True, text=True, timeout=7200)
        finally:
            shutil.rmtree(extract, ignore_errors=True)
            shutil.rmtree(work / "rerun", ignore_errors=True)
        if rerun.returncode == 2:
            print("DEFECT SETUP probe-rerun " + (rerun.stdout.strip().splitlines() or ["rc=2"])[-1])
            print("PREDICATE R98-C1 could-not-evaluate")
            return 2
        rerun_parsed = parse_receipt(rerun.stdout)
        rerun_obs = rerun_parsed["obs"]
        stamps_equal = all(bool(receipt["fields"].get(k)) and rerun_parsed["fields"].get(k) == receipt["fields"].get(k)
                           for k in RERUN_STAMPS)
        l6 = rerun.returncode == 0 and bool(receipt["obs"]) and rerun_obs == receipt["obs"] and stamps_equal
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
    set_ok = bool(base_set) and MEMBER not in base_set and rev_set == base_set | {MEMBER}
    legacy_ok = (member.get("receipt") == RECEIPT and member.get("subject") == "tb2-header"
                 and member.get("verdict") == "cases")
    l7 = (member.get("status") == "executed" and member.get("round") == 98
          and member.get("classes") == MEMBER_CLASSES and set_ok and legacy_ok)
    if not l7:
        defects.append(f"L7 ledger member={member.get('status')} round={member.get('round')} executed_total={exec_total} cells={cells} "
                       f"legacy_fields={legacy_ok} "
                       f"set_added={sorted(rev_set - base_set)} set_removed={sorted(base_set - rev_set)}")

    l8 = bool(frozen.get(TOOL)) and sha(tool_at_rev) == frozen.get(TOOL)
    if not l8:
        defects.append(f"L8 probe {sha(tool_at_rev)[:12]} vs frozen {frozen.get(TOOL, 'absent')[:12]}")

    f = receipt["fields"]
    l9 = (f.get("TOOL_SHA") == sha(tool_at_rev) and f.get("CASE_TABLE_SHA") == sha(table_bytes)
          and f.get("HOST_BASH") == host_tool(["/usr/bin/bash", "--version"]))
    if not l9:
        defects.append(f"L9 stamps tool={f.get('TOOL_SHA', 'absent')[:12]} table={f.get('CASE_TABLE_SHA', 'absent')[:12]} bash={f.get('HOST_BASH')}")

    added, flagged = new_row_defects(lane, rev, work)
    l10 = bool(added) and not flagged
    if not l10:
        defects.append(f"L10 new SOURCES rows={len(added)} gate-flagged={','.join(flagged) or '-'}")

    legs = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]
    ok = all(legs)
    print("LEGS " + " ".join(f"L{i + 1}={'pass' if v else 'fail'}" for i, v in enumerate(legs)))
    print("TARGET executed_rows=%d member=%s cells=%s set_equals_base_plus_member=%d located=%d executed=%d cases=%d legs=%d mismatches=%d new_rows=%d new_rows_flagged=%d defects=%d"
          % (exec_total, MEMBER, ",".join(f"{k}:{v}" for k, v in cells.items()), 1 if set_ok else 0,
             1 if cap is not None else 0, 1 if ok else 0, len(predicted),
             len(receipt["cases"]) * len(table.get("leg_order", [])), mismatches, len(added), len(flagged),
             len(defects)))
    for d in defects:
        print("DEFECT " + d)
    print("PREDICATE R98-C1 " + ("pass" if ok else "fail"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R98-C1 could-not-evaluate")
        sys.exit(2)
