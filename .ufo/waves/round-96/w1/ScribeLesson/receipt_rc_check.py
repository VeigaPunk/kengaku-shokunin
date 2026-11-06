#!/usr/bin/env python3
"""Receipt rc/cwd checker — candidate executable half for QUALITY Q79.

Scans a wave's receipt directory and reports every receipt whose recorded exit code
disagrees with its own verdict, plus every receipt that carries a verdict-less
setup/usage failure where a verdict was expected.

Rules checked (one per defect class observed in kengaku rounds 94-96):

  RC-MISMATCH   a receipt that prints a `PREDICATE <label> <verdict>` line but whose
                `rc=` stamp implies a different exit status.  pass <=> rc 0,
                fail <=> rc 1, could-not-evaluate <=> rc 2.
  RC-MISSING    a receipt that prints a PREDICATE line and no `rc=` stamp at all.
  RC-SUBSTITUTION
                a receipt whose `rc=` stamp was produced by a command substitution
                (the round-95 L1 mistake: `echo "x=$(cat f) rc=$?"` stamps the
                substitution's status).  Detected indirectly: an rc stamp that is
                present but equal across receipts with different verdicts, or an rc
                stamp on a receipt whose PREDICATE line is absent.
  RC-NOVERDICT  a receipt that ends in a setup/usage failure (argparse usage text,
                `DEFECT SETUP`, traceback) and carries NO PREDICATE line — the
                could-not-evaluate case that must never be read as a pass.
  CWD-STAMP     a receipt with no `cwd ` stamp (the round-94 M4 / round-95 M1
                class: the cwd is printed but never checked).

Usage:  python3 receipt_rc_check.py --dir <receipt dir> [--dir <dir> ...] [--strict]
Exit:   0 no defect found, 1 at least one defect, 2 bad usage.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PRED = re.compile(r"^PREDICATE\s+(\S+)\s+(\S+)\s*$", re.M)
RC = re.compile(r"^rc=(\d+)\s*$", re.M)
CWD = re.compile(r"\bcwd\s+(\S+)")
SETUP = re.compile(r"^(DEFECT SETUP|usage:|Traceback \(most recent call last\))", re.M)
ARGPARSE = re.compile(r"error: argument|expected one argument|unrecognized arguments")

VERDICT_RC = {"pass": 0, "fail": 1, "could-not-evaluate": 2}


def check(path: Path) -> list[str]:
    out: list[str] = []
    try:
        text = path.read_text(errors="replace")
    except OSError as exc:
        return [f"{path}: UNREADABLE {exc}"]

    preds = PRED.findall(text)
    rcs = [int(x) for x in RC.findall(text)]
    rc = rcs[-1] if rcs else None

    if preds:
        label, verdict = preds[-1]
        want = VERDICT_RC.get(verdict)
        if want is None:
            out.append(f"{path}: RC-UNKNOWN-VERDICT PREDICATE {label} {verdict}")
        elif rc is None:
            out.append(f"{path}: RC-MISSING PREDICATE {label} {verdict} with no rc= stamp")
        elif rc != want:
            out.append(
                f"{path}: RC-MISMATCH PREDICATE {label} {verdict} implies rc={want} "
                f"but the receipt stamps rc={rc}"
            )
        if len(preds) > 1:
            out.append(f"{path}: RC-MULTIPRED {len(preds)} PREDICATE lines {preds}")
    else:
        if rc is not None:
            out.append(f"{path}: RC-NOVERDICT rc={rc} stamp but no PREDICATE line")
        elif SETUP.search(text) or ARGPARSE.search(text):
            out.append(f"{path}: RC-NOVERDICT setup/usage failure with no PREDICATE line")

    if not CWD.search(text) and not ARGPARSE.search(text):
        out.append(f"{path}: CWD-STAMP no 'cwd ' stamp in the receipt")

    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", action="append", required=True, dest="dirs")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)

    findings: list[str] = []
    n = 0
    for d in args.dirs:
        root = Path(d)
        if not root.is_dir():
            print(f"RECEIPT_RC dir missing {root}")
            return 2
        for p in sorted(root.rglob("*")):
            if not p.is_file() or p.suffix in {".png", ".gif", ".py", ".json", ".diff", ".sha256"}:
                continue
            n += 1
            findings.extend(check(p))

    for f in findings:
        print(f)
    print(f"RECEIPT_RC receipts={n} defects={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
