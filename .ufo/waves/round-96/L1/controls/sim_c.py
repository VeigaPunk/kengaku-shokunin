#!/usr/bin/env python3
"""Round-96 P2 control builder: clone the lane at REV into DEST and commit (clone-local fixture
identity) a simulated C step. Modes:
  full        C1 ledger flip + receipt + SKILL cells + counter edits + mteb subject re-pin
  c1-only     C1 flip only (do-nothing for C2 at a C1-landed tip)
  delete-l7   C1 flip + mteb re-pin + r90-r95 counters with L7 forced true (forgery)
usage: sim_c.py LANE REV DEST MODE EDITS RECEIPT
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

lane, rev, dest, mode, edits, receipt = sys.argv[1:7]
dest = Path(dest)
if dest.exists():
    shutil.rmtree(dest)
subprocess.run(["git", "clone", "-q", "--shared", lane, str(dest)], check=True)
assert subprocess.run(["git", "-C", str(dest), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() == str(dest)
subprocess.run(["git", "-C", str(dest), "checkout", "-q", "--detach", rev], check=True)
led = dest / "plans/grader-population-ledger.json"
d = json.loads(led.read_text())
if mode != "c2-only":
    row = d["members"]["multi-source-data-merger"]
    d["members"]["multi-source-data-merger"] = {"classes": row["classes"], "receipt": "corpus/evidence/round96/merger-probe.txt",
                                                "round": 96, "status": "executed", "subject": "tb2-header", "verdict": "cases"}
if mode in ("full", "delete-l7", "c2-only", "repin-abs"):
    d["members"]["mteb-retrieve"]["subject"] = "tb2-header"
led.write_text(json.dumps(d, indent=1, sort_keys=True) + "\n")
if mode != "c2-only":
    (dest / "corpus/evidence/round96").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(receipt, dest / "corpus/evidence/round96/merger-probe.txt")
    sk = dest / "SKILL.md"
    t = sk.read_text()
    t2 = t.replace("| file-artifact | 76 | executed 30 of 76 (", "| file-artifact | 76 | executed 31 of 76 (round 96 adds `multi-source-data-merger`; ", 1)
    t2 = t2.replace("| serialization-schema | 10 | executed 6 of 10 (", "| serialization-schema | 10 | executed 7 of 10 (round 96 adds `multi-source-data-merger`; ", 1)
    assert t2.count("executed 31 of 76") == 1 and t2.count("executed 7 of 10") == 1, "SKILL cells"
    sk.write_text(t2)
if mode == "full":
    for p in Path(edits, "plans").glob("*.py"):
        shutil.copyfile(p, dest / "plans" / p.name)
if mode in ("c2-only", "repin-abs"):
    for p in Path(edits, "plans").glob("*.py"):
        shutil.copyfile(p, dest / "plans" / p.name)
if mode == "repin-abs":
    for r in range(90, 96):
        p = dest / f"plans/round{r}_c1_replay.py"
        s = p.read_text()
        if r == 90:
            a = '            executed_rows = sum(1 for v in members.values() if v.get("status") == "executed")\n'
            s2 = s.replace(a, a + '            if executed_rows != 40:\n                defect("L7-ledger", "FORGERY absolute re-pin 40")\n', 1)
        else:
            s2 = re.sub(r"\n(    )l7 = \(", r"\n\1l7 = (exec_total == 40) and (", s, count=1)
        assert s2 != s, r
        p.write_text(s2)
if mode == "delete-l7":
    shutil.copyfile(Path(edits, "plans/round87_c1_replay.py"), dest / "plans/round87_c1_replay.py")
    for r in range(90, 96):
        p = dest / f"plans/round{r}_c1_replay.py"
        s = p.read_text()
        if r == 90:
            s2 = s.replace('defect("L7-ledger",', '(lambda *x: None)("L7-ledger",')
        else:
            s2 = re.sub(r"\n(    )l7 = \(", r"\n\1l7 = True or (", s, count=1)
        assert s2 != s, r
        p.write_text(s2)
g = ["git", "-c", "user.name=round96-fixture", "-c", "user.email=fixture@invalid", "-c", "commit.gpgsign=false", "-C", str(dest)]
subprocess.run(g + ["add", "-A"], check=True)
subprocess.run(g + ["commit", "-q", "-m", f"round96 P2 fixture {mode}"], check=True)
print(subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())
