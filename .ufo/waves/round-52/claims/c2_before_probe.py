#!/usr/bin/env python3
"""R52-C2 before-probe: advertised verdict instruments vs SKILL.md gate/probe registry.

Frozen before data (2026-10-28, L1 KengakuR52a3).  Reads only committed bytes of a
lane checkout; runs nothing it did not name; writes one receipt to stdout.

ADVERTISED universe = every `python3 <path>` command named in the lane's self-assessment
files (SCORECARD.md, SKILL.md, corpus/README.md, corpus/knowledge/*.md, LOG.md).
REGISTERED universe = every `python3 <path>` command named in the SKILL.md
"## Gate/probe registry (PROTOCOL §Gate standard)" table only.

Leg A (registry completeness): missing = ADVERTISED - REGISTERED ; incomplete rows, missing
files.  Leg B (runnability): each ADVERTISED script is invoked with `--selftest` when the
file declares that flag, else `--help`; a crash is a non-{0,1,2} exit or a Python
traceback on stderr.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

CMD = re.compile(r"python3 ([\w./-]+\.py)")
SELFTEST = re.compile(r"['\"]--selftest['\"]")


def advertised(lane: Path):
    files = ["SCORECARD.md", "SKILL.md", "LOG.md", "corpus/README.md"]
    files += [str(p.relative_to(lane)) for p in sorted((lane / "corpus" / "knowledge").glob("*.md"))]
    out = {}
    for rel in files:
        p = lane / rel
        if not p.exists():
            continue
        text = p.read_text(errors="replace")
        for m in CMD.finditer(text):
            out.setdefault(m.group(1), set()).add(rel)
    return out


def registered(lane: Path):
    text = (lane / "SKILL.md").read_text(errors="replace")
    m = re.search(r"^## Gate/probe registry.*?(?=^## )", text, re.S | re.M)
    if not m:
        return {}, []
    block = m.group(0)
    cmds = {x.group(1) for x in CMD.finditer(block)}
    rows = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            continue
        if cells[0].startswith("---") or set(cells[0]) <= set("-: "):
            continue
        rows.append(cells)
    return cmds, rows


def main() -> int:
    lane = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    adv = advertised(lane)
    reg, rows = registered(lane)
    missing = sorted(set(adv) - reg)
    absent_files = sorted(p for p in adv if not (lane / p).exists())
    incomplete = [r[0] for r in rows if not all(r)]
    print(f"REV {os.popen('git -C %s rev-parse HEAD' % lane).read().strip()}")
    print(f"ADVERTISED total={len(adv)}")
    print(f"REGISTERED total={len(reg)} rows={len(rows)}")
    print(f"MISSING rows={len(missing)}")
    for p in missing:
        print(f"  MISSING {p}  cited-in={','.join(sorted(adv[p]))}")
    print(f"ABSENT-FILE total={len(absent_files)}")
    for p in absent_files:
        print(f"  ABSENT {p}")
    print(f"INCOMPLETE-ROW total={len(incomplete)} {incomplete}")
    crashed = []
    ran = 0
    for p in sorted(adv):
        f = lane / p
        if not f.exists():
            continue
        args = ["python3", str(f), "--selftest"] if SELFTEST.search(f.read_text(errors="replace")) else ["python3", str(f), "--help"]
        try:
            r = subprocess.run(args, cwd=lane, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            crashed.append((p, "TIMEOUT", ""))
            ran += 1
            continue
        ran += 1
        tb = "Traceback (most recent call last)" in r.stderr
        if tb or r.returncode not in (0, 1, 2):
            crashed.append((p, f"exit={r.returncode}", "traceback" if tb else ""))
    print(f"RAN total={ran} crashed={len(crashed)}")
    for p, code, why in crashed:
        print(f"  CRASH {p} {code} {why}")
    print(f"LEG-A missing={len(missing)} absent_file={len(absent_files)} incomplete_row={len(incomplete)}")
    print(f"LEG-B crashed={len(crashed)} of {ran}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
