#!/usr/bin/env python3
"""Build one fixture clone per single mutant of the R98-C1 counter's inputs.

Pristine clone at T is never touched; each mutant is a `git clone --shared` of it,
checked out detached at T, one edit, one commit.  Prints a JSON manifest.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path("/fast/scratch/hyaku/kengaku-r98/MutC1")
PRISTINE = ROOT / "clone"
T = "8e37fc65d5649bb37166fdd6b1657445a8cb55b9"
BASE = "49a1c4f1097db7c923da56d4213cad75772ed1c0"
RECEIPT = "corpus/evidence/round98/regexchess-probe.txt"
TABLE = "plans/round98-cases.json"
LEDGER = "plans/grader-population-ledger.json"
SOURCES = "corpus/SOURCES.md"
PROBE = "plans/round98_regexchess_probe.py"
COUNTER = "plans/round98_c1_replay.py"
CAP = "corpus/evidence/round98/tb2-regex-chess/instruction.md"

Z64 = "0" * 64
ONES = "1" * 64
CAP_SHA = "4983c44d21c56dd8191381eff0304afc8b87bb714527ea9036b3319c015a30b4"

# (name, target path, op, args, expected legs)
MUTANTS = [
    # ---- receipt edits -------------------------------------------------
    ("r1_lanetip_nonancestor", RECEIPT, "side_tip",
     ("LANE_TIP e1a3afd9069a19e38fd0bc3b015970231f303fc7",), "L3"),
    ("r2_detail_digest", RECEIPT, "replace",
     ("DETAIL C04 chars=2618175 pairs=40461 sha=5d122949b3c6816d built=- dup-first-drop-second",
      "DETAIL C04 chars=2618175 pairs=40461 sha=5d122949b3c6816e built=- dup-first-drop-second"), "L6"),
    ("r3_case_observed_flip", RECEIPT, "replace",
     ("CASE C08 predicted=F,F,F,P,0 observed=F,F,F,P,0 ok=True",
      "CASE C08 predicted=F,F,F,P,0 observed=P,P,P,P,1 ok=True"), "L5,L6"),
    ("r4_case_dropped", RECEIPT, "replace",
     ("CASE C12 predicted=P,P,P,F,0 observed=P,P,P,F,0 ok=True\n", ""), "L5,L6"),
    ("r6_subject_sha", RECEIPT, "replace",
     ("SUBJECT_SHA " + CAP_SHA, "SUBJECT_SHA " + Z64), "L2"),
    ("r7_tool_sha", RECEIPT, "replace",
     ("TOOL_SHA 871630782933871398922c510c5de1cebd2ace7fa081d014df90aeeff66d33db",
      "TOOL_SHA " + Z64), "L6,L9"),
    ("r8_host_bash", RECEIPT, "replace",
     ("HOST_BASH GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)",
      "HOST_BASH GNU bash, version 5.3.20(1)-release (mutant)"), "L9"),
    ("r10_receipt_absent", RECEIPT, "delete", (), "L1,L2,L3,L5,L6,L9"),
    # ---- case table edits ----------------------------------------------
    ("t1_predicted_flip", TABLE, "replace",
     ('"id": "C07",\n   "app": "invented-ep",\n   "predicted": "P,P,P,P,1"',
      '"id": "C07",\n   "app": "invented-ep",\n   "predicted": "F,F,F,P,0"'), "L4,L5,L6"),
    ("t2_app_swap", TABLE, "replace",
     ('"id": "C06",\n   "app": "extra-line"', '"id": "C06",\n   "app": "drop-last"'), "L4,L6"),
    ("t4_case_reorder", TABLE, "replace",
     ('  {\n   "id": "C01",\n   "app": "solve",\n   "predicted": "P,P,P,P,1",\n   "why": "positive control: captured solve.sh run unmodified (40460 pairs)"\n  },\n  {\n   "id": "C02",\n   "app": "absent",\n   "predicted": "E:FileNotFoundError,E:FileNotFoundError,E:FileNotFoundError,E:FileNotFoundError,0",\n   "why": "no /app/re.json: every test opens it"\n  },',
      '  {\n   "id": "C02",\n   "app": "absent",\n   "predicted": "E:FileNotFoundError,E:FileNotFoundError,E:FileNotFoundError,E:FileNotFoundError,0",\n   "why": "no /app/re.json: every test opens it"\n  },\n  {\n   "id": "C01",\n   "app": "solve",\n   "predicted": "P,P,P,P,1",\n   "why": "positive control: captured solve.sh run unmodified (40460 pairs)"\n  },'), "L4,L6"),
    ("t5_table_whitespace", TABLE, "replace",
     ('"member": "regex-chess",', '"member":  "regex-chess",'), "L4"),
    # ---- ledger edits ---------------------------------------------------
    ("g1_extra_executed_member", LEDGER, "replace",
     ('"evidence": "no-blocker: tests/test_outputs.py sha256=364069f893e336a0",\n   "reason": "unattempted",\n   "status": "unexecuted"',
      '"evidence": "no-blocker: tests/test_outputs.py sha256=364069f893e336a0",\n   "reason": "unattempted",\n   "status": "executed"'), "L7"),
    ("g2_removed_executed_member", LEDGER, "replace",
     ('"receipt": "corpus/evidence/round36/regex-log-probe.txt",\n   "round": 36,\n   "status": "executed"',
      '"receipt": "corpus/evidence/round36/regex-log-probe.txt",\n   "round": 36,\n   "status": "unexecuted"'), "L7"),
    ("g3_legacy_receipt", LEDGER, "replace",
     ('"receipt": "corpus/evidence/round98/regexchess-probe.txt",\n   "subject": "tb2-header"',
      '"receipt": "corpus/evidence/round97/other.txt",\n   "subject": "tb2-header"'), "L7"),
    ("g4_classes", LEDGER, "replace",
     ('"classes": [\n    "file-artifact",\n    "serialization-schema"\n   ],\n   "evidence": "no-blocker: tests/test_outputs.py sha256=4983c44d21c56dd8; receipt corpus/evidence/round98/regexchess-probe.txt"',
      '"classes": [\n    "file-artifact"\n   ],\n   "evidence": "no-blocker: tests/test_outputs.py sha256=4983c44d21c56dd8; receipt corpus/evidence/round98/regexchess-probe.txt"'), "L7"),
    # ---- SOURCES edits --------------------------------------------------
    ("s1_bad_anchor_row", SOURCES, "append",
     ("\n| S334 | mutant row with an unresolvable anchor | own-work | A | mutant scope | sha256 " + ONES +
      " | mutant | queued | 2026-11-06 | 90d | — |\n",), "L10"),
    ("s2_valid_anchor_row", SOURCES, "append",
     ("\n| S334 | mutant control row binding a committed capture — corpus/evidence/round98/tb2-regex-chess/test_outputs.py | own-work | A | mutant scope | sha256 " + CAP_SHA +
      " | mutant | queued | 2026-11-06 | 90d | — |\n",), "pass-control"),
    # ---- probe edit ------------------------------------------------------
    ("p1_probe_comment", PROBE, "replace",
     ('"""Replay the captured `regex-chess` grader', '"""Replay the captured `regex-chess` grader (mutant)'), "L6,L8,L9"),
    # ---- capture edit ----------------------------------------------------
    ("c1_capture_byte", CAP, "replace",
     ("You can look at the provided check.py", "You can look at the provided check.py!"), "setup-refusal"),
    # ---- counter code edits ---------------------------------------------
    ("k1_l10_ignore_flagged", COUNTER, "replace",
     ("l10 = bool(added) and not flagged", "l10 = bool(added)"), "pass (self-binding gap)"),
    ("k2_l7_superset", COUNTER, "replace",
     ("set_ok = bool(base_set) and MEMBER not in base_set and rev_set == base_set | {MEMBER}",
      "set_ok = bool(base_set) and MEMBER not in base_set and (base_set | {MEMBER}) <= rev_set"), "pass (round-97 defect 2)"),
    ("d1_k1_s1", None, "double", ("k1_l10_ignore_flagged", "s1_bad_anchor_row"), "pass (survivor pair)"),
    ("d2_k2_g1", None, "double", ("k2_l7_superset", "g1_extra_executed_member"), "pass (survivor pair)"),
]


def sh(*args, cwd=None, check=True):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit(f"FAILED {args}: {p.returncode}\n{p.stdout}\n{p.stderr}")
    return p


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "absent"


def apply_edit(root: Path, path: str, op: str, args) -> str:
    f = root / path
    before = sha(f)
    if op == "replace":
        old, new = args
        text = f.read_text()
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"{path}: old string occurs {n} times")
        f.write_text(text.replace(old, new))
    elif op == "delete":
        f.unlink()
    elif op == "append":
        with f.open("a") as fh:
            fh.write(args[0])
    elif op == "side_tip":
        (old,) = args
        tree = sh("git", "-C", str(root), "rev-parse", f"{BASE}^{{tree}}").stdout.strip()
        side = sh("git", "-C", str(root), "-c", "user.name=mut", "-c", "user.email=mut@example.invalid",
                  "commit-tree", tree, "-p", BASE, "-m", "mutant side commit").stdout.strip()
        text = f.read_text()
        if text.count(old) != 1:
            raise SystemExit(f"{path}: LANE_TIP line not unique")
        f.write_text(text.replace(old, f"LANE_TIP {side}"))
        return before + "|side=" + side
    else:
        raise SystemExit(f"bad op {op}")
    return before


def main() -> int:
    names = [m[0] for m in MUTANTS]
    by_name = {m[0]: m for m in MUTANTS}
    mdir = ROOT / "mutants"
    if mdir.exists():
        shutil.rmtree(mdir)
    mdir.mkdir()
    manifest = []
    for name, path, op, args, expected in MUTANTS:
        d = mdir / name
        sh("git", "clone", "-q", "--shared", str(PRISTINE), str(d))
        top = sh("git", "-C", str(d), "rev-parse", "--show-toplevel").stdout.strip()
        if top != str(d):
            raise SystemExit(f"toplevel mismatch for {d}: {top}")
        sh("git", "-C", str(d), "-c", "advice.detachedHead=false", "checkout", "-q", T)
        edits = []
        if op == "double":
            for sub in args:
                _, spath, sop, sargs, _ = by_name[sub]
                edits.append((spath, apply_edit(d, spath, sop, sargs)))
        else:
            edits.append((path, apply_edit(d, path, op, args)))
        sh("git", "-C", str(d), "add", "-A")
        sh("git", "-C", str(d), "-c", "user.name=mut", "-c", "user.email=mut@example.invalid",
           "commit", "-q", "-m", f"mutant {name}")
        commit = sh("git", "-C", str(d), "rev-parse", "HEAD").stdout.strip()
        after = {p: sha(d / p) for p, _ in edits}
        # restore exact bytes: reset the fixture to T and prove the tree is clean
        sh("git", "-C", str(d), "reset", "-q", "--hard", T)
        restored_clean = sh("git", "-C", str(d), "status", "--porcelain").stdout.strip() == ""
        restored = {p: sha(d / p) for p, _ in edits}
        manifest.append(dict(name=name, path=path, op=op, expected=expected, fixture=str(d),
                             commit=commit, before={p: b for p, b in edits}, after=after,
                             restored=restored, restored_clean=restored_clean))
        print(json.dumps(manifest[-1]), flush=True)
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
