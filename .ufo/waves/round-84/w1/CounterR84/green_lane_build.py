#!/usr/bin/env python3
"""Fixture-only harness: build a green R84-C1 lane in scratch from BASE.

Not a production artifact. It constructs a git worktree of $S/lane at BASE, lands the
eight frozen vectors, a dummy instrument at both the tracked path and the reviewed draft
path, the executed ledger row and a receipt naming the minting tip, then leaves HEAD one
commit later with a clean worktree. The counter is then run against this lane.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r84/CounterR84")
LANE = S / "lane"
GREEN = S / "green"
BASE = "4087b2f8369fb0c317a8460725a607681ff2fd7f"
MEMBER = "gcode-to-text"
CAPTURE = "corpus/evidence/round52/graders/gcode-to-text/tests/test_outputs.py"
TABLE = "plans/round84-cases.json"
TOOL = "plans/round84_gcode_probe.py"
DRAFT = ".ufo/waves/round-84/w1/ProbeR84/round84_gcode_probe.py"
RECEIPT = "corpus/evidence/round84/gcode-to-text-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
VECTORS = (("missing", "F/F"), ("empty", "P/F"), ("exact", "P/P"), ("padded", "P/P"),
           ("uppercase", "P/F"), ("suffix", "P/F"), ("prefix-only", "P/F"),
           ("wrong-flag", "P/F"))

TOOL_SRC = '''import argparse
V = {vectors!r}
ap = argparse.ArgumentParser()
ap.add_argument("--lane")
ap.add_argument("--work")
a = ap.parse_args()
print("# tb2 gcode-to-text grader probe")
for cid, vec in V:
    print(f"CASE {{cid}} predicted={{vec}} observed={{vec}}")
print("cases=8 mismatches=0")
print("PREDICATE R84-PROBE pass")
'''.format(vectors=VECTORS)


def sh(*argv, cwd=None):
    proc = subprocess.run(argv, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"{argv} failed: {proc.stdout}{proc.stderr}")
    return proc.stdout


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def commit(message: str) -> str:
    sh("git", "-C", str(GREEN), "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
       "commit", "-q", "-m", message)
    return sh("git", "-C", str(GREEN), "rev-parse", "HEAD").strip()


def main() -> int:
    if GREEN.exists():
        sh("git", "-C", str(LANE), "worktree", "remove", "--force", str(GREEN))
    if GREEN.exists():
        import shutil
        shutil.rmtree(GREEN)
    sh("git", "-C", str(LANE), "worktree", "add", "--detach", str(GREEN), BASE)
    top = sh("git", "-C", str(GREEN), "rev-parse", "--show-toplevel").strip()
    if Path(top) != GREEN.resolve():
        raise SystemExit(f"worktree toplevel {top} != {GREEN}")
    (GREEN / TABLE).write_text(json.dumps(
        {"member": MEMBER,
         "cases": [{"id": cid, "content": None if cid == "missing" else cid, "predicted": vec}
                   for cid, vec in VECTORS]},
        indent=2, sort_keys=True) + "\n")
    (GREEN / TOOL).write_text(TOOL_SRC)
    (GREEN / DRAFT).parent.mkdir(parents=True)
    (GREEN / DRAFT).write_text(TOOL_SRC)
    (GREEN / RECEIPT).parent.mkdir(parents=True, exist_ok=True)
    doc = json.loads((GREEN / LEDGER).read_text())
    doc["members"][MEMBER] = {"classes": ["file-artifact"], "round": 84, "receipt": RECEIPT,
                              "status": "executed", "subject": "tb2-header",
                              "verdict": "predicate"}
    (GREEN / LEDGER).write_text(json.dumps(doc, indent=1) + "\n")
    sh("git", "-C", str(GREEN), "add", "-f", TABLE, TOOL, DRAFT, LEDGER, cwd=GREEN)
    mint = commit("fixture green lane: land frozen table, instrument and executed ledger")
    subject_sha = sha((GREEN / CAPTURE).read_bytes())
    table_sha = sha((GREEN / TABLE).read_bytes())
    tool_sha = sha((GREEN / TOOL).read_bytes())
    block = "\n".join([f"CASE {cid} predicted={vec} observed={vec}" for cid, vec in VECTORS]
                      + ["cases=8 mismatches=0", "PREDICATE R84-PROBE pass"]) + "\n"
    receipt = (
        f"# tb2 {MEMBER} grader probe\n"
        f"MEMBER {MEMBER}\n"
        f"SUBJECT_CAPTURE {CAPTURE}\n"
        f"SUBJECT_SHA {subject_sha}\n"
        f"CASE_TABLE_SHA {table_sha}\n"
        f"TOOL {TOOL}\n"
        f"TOOL_SHA {tool_sha}\n"
        f"HOST_PYTHON Python 3.14.8\n"
        f"HOST_OPENSSL OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)\n"
        f"LANE_TIP {mint}\n"
        f"WORKTREE clean\n"
        f"COMMAND python3 {TOOL} --lane . --work {S}/green-mint\n"
        f"EXIT 0\n"
        f"OBSERVATIONS_BEGIN\n{block}OBSERVATIONS_END\n")
    (GREEN / RECEIPT).write_text(receipt)
    sh("git", "-C", str(GREEN), "add", "-f", RECEIPT, cwd=GREEN)
    tip = commit("fixture green lane: land receipt naming the minting tip")
    status = sh("git", "-C", str(GREEN), "status", "--porcelain", "--untracked-files=normal")
    print(f"GREEN-LANE mint={mint} head={tip} subject={subject_sha} table={table_sha} "
          f"tool={tool_sha} clean={not status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
