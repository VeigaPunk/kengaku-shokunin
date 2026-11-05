#!/usr/bin/env python3
"""R87-C2 counter — live-document case-set wording against the round-86 table, at a measured revision.

Scope (current-state documents only): corpus/README.md, PROVINCE.md, SKILL.md. Append-only logs, filed
lessons and frozen claim files are out of scope by design.

Derived facts come from `plans/round86-cases.json` at the measured revision:
  total   = number of cases
  schema  = cases whose `why` text contains "schema drift"
  control = total - schema

  mismatch  — a scoped line asserting "<number word> [frozen] schema-drift case(s)" whose number word
              differs from `schema`
  defect    — mismatch, or the row `lessons/round-86.md` in corpus/README.md lacks the derived canonical
              sentence "<total> case shapes, <schema> schema-drift and <control> controls"

Prints one `DEFECT` line per finding, then `TARGET mismatches=<n> defects=<n>` and
`PREDICATE R87-C2 pass|fail`.

Usage:  python3 plans/round87_c2_wording.py --lane <repo> --rev <rev> --work <scratch dir>
Exit:   0 target reached, 1 at least one finding, 2 could not evaluate.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SCOPE = ("corpus/README.md", "PROVINCE.md", "SKILL.md")
TABLE = "plans/round86-cases.json"
CANON_ROW = "| `lessons/round-86.md` |"
CLAIM_RE = re.compile(r"\b([A-Za-z]+) (?:frozen )?schema-drift cases?\b")
NUMBERS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
           "eight": 8, "nine": 9, "ten": 10}
WORDS = {v: k for k, v in NUMBERS.items()}


def git_blob(root: Path, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{path}"], capture_output=True, timeout=120)
    return proc.stdout if proc.returncode == 0 else None


def derive(table_bytes: bytes) -> tuple[int, int, int]:
    doc = json.loads(table_bytes)
    cases = doc["cases"]
    schema = sum(1 for c in cases if "schema drift" in str(c.get("why", "")).lower())
    return len(cases), schema, len(cases) - schema


def run(root: Path, rev: str) -> int:
    resolved = subprocess.run(["git", "-C", str(root), "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}"],
                              capture_output=True, text=True, timeout=60)
    if resolved.returncode != 0:
        print(f"DEFECT SETUP unresolved-revision {rev}")
        print("PREDICATE R87-C2 could-not-evaluate")
        return 2
    table_bytes = git_blob(root, rev, TABLE)
    if table_bytes is None:
        print(f"DEFECT SETUP {TABLE} absent at {rev}")
        print("PREDICATE R87-C2 could-not-evaluate")
        return 2
    total, schema, control = derive(table_bytes)
    canon = (f"{WORDS[total]} case shapes, {WORDS[schema]} schema-drift and "
             f"{WORDS[control]} controls")
    mismatches = 0
    defects = 0
    for path in SCOPE:
        text = git_blob(root, rev, path)
        if text is None:
            print(f"DEFECT SETUP {path} absent at {rev}")
            print("PREDICATE R87-C2 could-not-evaluate")
            return 2
        for number, line in enumerate(text.decode("utf-8", errors="replace").splitlines(), start=1):
            for match in CLAIM_RE.finditer(line):
                word = match.group(1).lower()
                if NUMBERS.get(word) != schema:
                    mismatches += 1
                    defects += 1
                    print(f"DEFECT MISMATCH {path}:{number} asserts {word!r} schema-drift cases; derived {schema}")
    readme = git_blob(root, rev, "corpus/README.md") or b""
    rows = [ln for ln in readme.decode("utf-8", errors="replace").splitlines() if ln.startswith(CANON_ROW)]
    if not rows or canon not in rows[0]:
        defects += 1
        print(f"DEFECT CANON corpus/README.md lessons/round-86.md row lacks {canon!r}")
    print(f"TARGET mismatches={mismatches} defects={defects} total={total} schema={schema} control={control}")
    verdict = "pass" if defects == 0 else "fail"
    print(f"PREDICATE R87-C2 {verdict}")
    return 0 if defects == 0 else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--lane", default=".")
    parser.add_argument("--rev", required=True)
    parser.add_argument("--work", required=False, default="")
    args = parser.parse_args(argv)
    return run(Path(args.lane).resolve(), args.rev)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
