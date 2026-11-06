#!/usr/bin/env python3
"""R100-C1 counter — the eighteenth located offline replay, `financial-document-processor` (round 100).

Successor of plans/round99_c1_replay.py (not edited, Q79). Legs, every input read at the measured
revision (round-92 discipline: positional case ids, guarded host probes, no skip flags):

  L1  the receipt is committed at --rev
  L2  the capture and solution-fixture pins (each directory's SHA256SUMS included) hash at --rev, every
      SHA256SUMS line hashes to its committed file and lists every file of its directory, and the
      receipt names the same subject, test.sh, solve.sh and the two SHA256SUMS digests
  L3  the receipt's LANE_TIP EQUALS the freeze commit F (the single commit that added
      plans/round-100-claims.md) — round-99 CriticClaims F1 / MutC1 M04b: ancestry alone let a receipt
      claim BASE as its run identity
  L4  the case table at --rev hashes to the sha the round's frozen-instruments table holds
  L5  every receipt case vector equals its frozen predicted vector (all cases, no extras)
  L6  the probe re-run from a `git archive` of --rev reproduces the receipt's observation block
      exactly (CASE and DETAIL lines) and the same TOOL_SHA / CASE_TABLE_SHA / GRADER_SIDE stamps;
      the sandbox is fixed at /usr/bin/bwrap
  L7  the ledger at --rev holds the member executed round 100 with its frozen classes and the
      legacy-gate fields receipt=<this receipt>, subject=tb2-header, verdict=cases, and the executed
      member SET at --rev EQUALS the set at BASE plus this member
  L8  the probe bytes at --rev hash to the frozen-instruments table's probe sha
  L9  the receipt stamps (TOOL_SHA, CASE_TABLE_SHA, HOST_BASH) match the measured tree and host
  L10 the BASE bytes of `plans/anchor_digest_check.py`, run on a `git clone --shared` checkout of
      --rev, print no DEFECT line for any SOURCES row absent at BASE, and EXACTLY NEW_ROWS rows were
      added (round-99 MutC1 M13/M14: the leg was flag-only)
  L11 this counter's own bytes at --rev hash to the frozen-instruments table's row for it
  L12 file set (round-99 MutC1 M31-M33, CriticClaims F3/F5): every path that differs between F and
      --rev is in the frozen candidate-bytes table or is the receipt, and every C1-owned candidate
      (SKILL.md, the ledger, SOURCES.md) differs F..rev and hashes at --rev to its table sha
  L13 the BASE bytes of `plans/anchor_line_check.py`, run on a checkout of --rev, print no `ROW <id>
      state=live` line for a row absent at BASE (round-99 ScoutSources SS-18 / lesson M3: typed word
      counts on new rows went unchecked by every C1 leg)

The first output line is `REV <full hash>`. The counter refuses (rc 2) unless the process cwd is the
lane root.

Usage:  python3 plans/round100_c1_replay.py --lane <repo> --rev <rev> --work <dir> --grader-venv <dir>
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

CAPDIR = "corpus/evidence/round100/tb2-financial-document-processor"
FIXDIR = "corpus/evidence/round100/fdp-solution"
CAP = CAPDIR + "/test_outputs.py"
PINS = {
    "test_outputs.py": "978f506ad5c1bfaf28f9bc774dfe4347d33d046ca009b8496eb513956b7f5a9a",
    "test.sh": "48abbda713ace5cee00dd28c7398959f28280062350eb88206a6697a28c72790",
    "solve.sh": "90861b79c4bd7733909616ffa058151847eb67a4d43395a964c449cf7e24c4fb",
    "Dockerfile": "2ea485aead008998d7a551e8c80b6bd354a74cbffc310a1f4b88d0b7c53d23ff",
    "task.toml": "163ee252895c05d36ca37137dba4d6c24b46be28d56ce84ef8bb35bb5b894bda",
    "instruction.md": "b21cf2af1891922732327bf586d14b250d36d96de7867479c15bd1c58ef0db58",
    "README.md": "32438e7780d235dd609f4740e36512c4cd2f34ef26842ea52c5bbde46fcf5e86",
    "randomize_filenames.py": "09828ee53e8f2165a9888c5de84e40fcb057bb889d93bfc90d9aeca8c4e23be4",
    "SHA256SUMS": "0a137bdb179c5d4e9056565e8fa18725bf94f56b43fa78547db888bb1cb46fa3",
}
FIX_PINS = {
    "placement.tsv": "32518f87d43be98e862086e6dd847538b3d2800ad9f083ff3994826a1fb48209",
    "summary.csv": "08724ad988ea1fe13804ddaf85da9b3731289ac5b9a9e730117b9134c3e977b2",
    "document_processor.py": "db4f841e7dc0b3c846fc1e37f37ee3a0e28f3601b055afa1fec00b269e8d937a",
    "SHA256SUMS": "97fbf7930b838bc28556a67ba296b131660b8d1e18272b288c169e9a5183ed6f",
}
TABLE = "plans/round100-cases.json"
TOOL = "plans/round100_fdp_probe.py"
SELF = "plans/round100_c1_replay.py"
RECEIPT = "corpus/evidence/round100/fdp-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
CLAIMS = "plans/round-100-claims.md"
SOURCES = "corpus/SOURCES.md"
GATE = "plans/anchor_digest_check.py"
LINE_GATE = "plans/anchor_line_check.py"
OWNED = ("SKILL.md", LEDGER, SOURCES)
MEMBER = "financial-document-processor"
MEMBER_CLASSES = ["crypto-credential", "file-artifact"]
NEW_ROWS = 8
SUBJECT_SHA = PINS["test_outputs.py"]
TEST_SH_SHA = PINS["test.sh"]
SOLVE_SHA = PINS["solve.sh"]
CAPTURE_SUMS_SHA = PINS["SHA256SUMS"]
FIXTURE_SUMS_SHA = FIX_PINS["SHA256SUMS"]
BASE = "7846037679de77d050141c785996471801e5a19a"
BWRAP = "/usr/bin/bwrap"
RERUN_STAMPS = ("TOOL_SHA", "CASE_TABLE_SHA", "GRADER_SIDE")
ROW = re.compile(r"^([0-9a-f]{64})  (\S+)$")
LIVE_ROW = re.compile(r"^ROW (S\d{3,}) state=live\b")
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


def freeze_commit(root: Path, rev: str) -> str | None:
    added = [x for x in git(root, "log", "--diff-filter=A", "--format=%H", rev, "--", CLAIMS).stdout.decode().split() if x]
    return added[0] if len(added) == 1 else None


def fenced(root: Path, commit: str | None, name: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    if not commit:
        return rows
    inside = False
    for line in (blob(root, commit, CLAIMS) or b"").decode(errors="replace").splitlines():
        if not inside and line.strip() == "```" + name:
            inside = True
            continue
        if inside and line.strip() == "```":
            break
        m = ROW.match(line.strip()) if inside else None
        if m:
            rows[m.group(2)] = m.group(1)
    return rows


def sums_cover(root: Path, rev: str, base: str) -> bool:
    """Every SHA256SUMS line in `base` hashes to its committed file, and every file is listed."""
    text = blob(root, rev, f"{base}/SHA256SUMS")
    if text is None:
        return False
    listed = {}
    for line in text.decode(errors="replace").splitlines():
        digest, _, rel = line.partition("  ")
        listed[rel[2:] if rel.startswith("./") else rel] = digest
    out = git(root, "ls-tree", "-r", "--name-only", rev, base + "/")
    present = {p[len(base) + 1:] for p in out.stdout.decode().splitlines() if p and not p.endswith("/SHA256SUMS")}
    return bool(listed) and set(listed) == present and all(sha(blob(root, rev, f"{base}/{r}")) == d for r, d in listed.items())


def checkout(lane: Path, rev: str, dest: Path) -> Path:
    if dest.exists():
        shutil.rmtree(dest)
    proc = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", str(lane), str(dest)],
                          capture_output=True, timeout=300)
    if proc.returncode != 0 or git(dest, "-c", "advice.detachedHead=false", "checkout", "-q", rev).returncode != 0:
        raise CouldNotEvaluate("gate fixture checkout failed")
    if git(dest, "rev-parse", "--show-toplevel").stdout.decode().strip() != str(dest):
        raise CouldNotEvaluate("gate fixture toplevel mismatch")
    return dest


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


def new_row_defects(lane: Path, rev: str, work: Path) -> tuple[list[str], list[str], list[str]]:
    """(rows added after BASE, those the BASE anchor-digest gate flags, those the BASE line gate calls live)."""
    base_ids = set(ROWID.findall((blob(lane, BASE, SOURCES) or b"").decode(errors="replace")))
    rev_ids = set(ROWID.findall((blob(lane, rev, SOURCES) or b"").decode(errors="replace")))
    added = sorted(rev_ids - base_ids, key=lambda s: int(s[1:]))
    gate_bytes = blob(lane, BASE, GATE)
    line_bytes = blob(lane, BASE, LINE_GATE)
    if gate_bytes is None or line_bytes is None:
        raise CouldNotEvaluate("gate absent at BASE")
    gate = work / "gate-base.py"
    gate.write_bytes(gate_bytes)
    line_gate = work / "line-gate-base.py"
    line_gate.write_bytes(line_bytes)
    tree = checkout(lane, rev, work / "gate-tree")
    try:
        run = subprocess.run([sys.executable, "-I", "-B", str(gate), "--lane", str(tree)],
                             capture_output=True, text=True, timeout=1200, cwd=str(tree))
        lrun = subprocess.run([sys.executable, "-I", "-B", str(line_gate), "--lane", str(tree)],
                              capture_output=True, text=True, timeout=1200, cwd=str(tree))
    finally:
        shutil.rmtree(tree, ignore_errors=True)
    if run.returncode not in (0, 1) or lrun.returncode not in (0, 1):
        raise CouldNotEvaluate(f"gate rc={run.returncode} line-gate rc={lrun.returncode}")
    flagged = sorted({m.group(1) for m in map(DEFECT.match, run.stdout.splitlines()) if m and m.group(1) in added},
                     key=lambda s: int(s[1:]))
    live = sorted({m.group(1) for m in map(LIVE_ROW.match, lrun.stdout.splitlines()) if m and m.group(1) in added},
                  key=lambda s: int(s[1:]))
    return added, flagged, live


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
    print(f"REV {rev}")
    defects: list[str] = []

    table_bytes = blob(lane, rev, TABLE)
    table = json.loads(table_bytes.decode()) if table_bytes else {}
    ledger_bytes = blob(lane, rev, LEDGER)
    ledger = json.loads(ledger_bytes.decode()) if ledger_bytes else {}
    fcommit = freeze_commit(lane, rev)
    frozen = fenced(lane, fcommit, "frozen-instruments")
    candidates = fenced(lane, fcommit, "candidate-bytes")
    receipt_bytes = blob(lane, rev, RECEIPT)
    receipt = parse_receipt(receipt_bytes.decode(errors="replace")) if receipt_bytes else {"fields": {}, "cases": [], "obs": []}

    l1 = receipt_bytes is not None
    if not l1:
        defects.append(f"L1 receipt absent at revision: {RECEIPT}")

    cap = blob(lane, rev, CAP)
    l2 = (all(sha(blob(lane, rev, f"{CAPDIR}/{p}")) == want for p, want in PINS.items())
          and all(sha(blob(lane, rev, f"{FIXDIR}/{p}")) == want for p, want in FIX_PINS.items())
          and sums_cover(lane, rev, CAPDIR) and sums_cover(lane, rev, FIXDIR)
          and receipt["fields"].get("CAPTURE_SUMS_SHA") == CAPTURE_SUMS_SHA
          and receipt["fields"].get("FIXTURE_SUMS_SHA") == FIXTURE_SUMS_SHA
          and receipt["fields"].get("SUBJECT_SHA") == SUBJECT_SHA
          and receipt["fields"].get("SOLVE_SHA") == SOLVE_SHA
          and receipt["fields"].get("TEST_SH_SHA") == TEST_SH_SHA)
    if not l2:
        defects.append(f"L2 capture/receipt sha mismatch (cap={sha(cap)[:12]} receipt={receipt['fields'].get('SUBJECT_SHA', 'absent')[:12]})")

    tip = receipt["fields"].get("LANE_TIP", "")
    l3 = bool(tip) and bool(fcommit) and tip == fcommit
    if not l3:
        defects.append(f"L3 LANE_TIP {tip or 'absent'} is not the freeze commit {fcommit or 'absent'}")

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
        print("PREDICATE R100-C1 could-not-evaluate")
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
            print("PREDICATE R100-C1 could-not-evaluate")
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
    l7 = (member.get("status") == "executed" and member.get("round") == 100
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

    added, flagged, live_rows = new_row_defects(lane, rev, work)
    l10 = len(added) == NEW_ROWS and not flagged
    if not l10:
        defects.append(f"L10 new SOURCES rows={len(added)} want={NEW_ROWS} gate-flagged={','.join(flagged) or '-'}")

    self_at_rev = blob(lane, rev, SELF)
    l11 = bool(frozen.get(SELF)) and sha(self_at_rev) == frozen.get(SELF)
    if not l11:
        defects.append(f"L11 counter {sha(self_at_rev)[:12]} vs frozen {frozen.get(SELF, 'absent')[:12]}")

    if fcommit:
        diff = git(lane, "diff", "--name-only", "--no-renames", fcommit, rev)
        changed = set(diff.stdout.decode().split()) if diff.returncode == 0 else {"<diff-failed>"}
    else:
        changed = {"<no-freeze>"}
    outside_table = sorted(p for p in changed if p not in candidates and p != RECEIPT)
    own_bad = sorted(p for p in OWNED if p not in changed or candidates.get(p) != sha(blob(lane, rev, p)))
    l12 = bool(fcommit) and not outside_table and not own_bad
    if not l12:
        defects.append(f"L12 freeze={'yes' if fcommit else 'absent'} outside_table={outside_table or '-'} own_unbound={own_bad or '-'}")

    l13 = not live_rows
    if not l13:
        defects.append(f"L13 new rows live in the line gate={','.join(live_rows)}")

    legs = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13]
    ok = all(legs)
    print("LEGS " + " ".join(f"L{i + 1}={'pass' if v else 'fail'}" for i, v in enumerate(legs)))
    print("TARGET executed_rows=%d member=%s cells=%s set_equals_base_plus_member=%d located=%d executed=%d cases=%d legs=%d mismatches=%d new_rows=%d new_rows_flagged=%d new_rows_line_live=%d changed_outside_table=%d defects=%d"
          % (exec_total, MEMBER, ",".join(f"{k}:{v}" for k, v in cells.items()), 1 if set_ok else 0,
             1 if cap is not None else 0, 1 if ok else 0, len(predicted),
             len(receipt["cases"]) * len(table.get("leg_order", [])), mismatches, len(added), len(flagged),
             len(live_rows), len(outside_table), len(defects)))
    for d in defects:
        print("DEFECT " + d)
    print("PREDICATE R100-C1 " + ("pass" if ok else "fail"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R100-C1 could-not-evaluate")
        sys.exit(2)
