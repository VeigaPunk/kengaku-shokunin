#!/usr/bin/env python3
"""R6RegistryCellAudit harness: per-row cell-truth audit of the five new SKILL.md rows.

Read-only. Parses the 5 new registry rows from the lane SKILL.md working tree, extracts each
cell, and checks:
  - entry cell: first backtick span starting with python3; referenced script exists in clone
  - pinned cell: claimed sha256 prefix vs actual script sha256
  - self-test cell: replicate plans/round52_c2_registry.py::selftest_unbacked + flag-in-body
  - verdict map / self-test cells carried verbatim for manual truth comparison
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

LANE = Path(sys.argv[1])   # lane working tree (for SKILL.md + script bytes)
CLONE = Path(sys.argv[2])  # scratch clone (for running entry commands)

NEW = ["round54-c1", "round54-c2", "round55-c2", "round55-c2-controls", "round55-c3"]
REGISTRY_HEADING = "## Gate/probe registry"
CMD = re.compile(r"python3 ((?:plans/[A-Za-z0-9_]+\.py|corpus/evidence/[A-Za-z0-9_]+/[A-Za-z0-9_]+\.py|grader\.py))")
FLAG = re.compile(r"(--[a-z][a-z0-9-]*)")


def registry_block(text):
    i = text.find(REGISTRY_HEADING)
    if i < 0:
        return ""
    j = text.find("\n## ", i + 1)
    return text[i:j] if j > 0 else text[i:]


def parse_rows(block):
    rows = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) != 8:
            continue
        if set(cells[0]) <= set("-: "):
            continue
        rows.append(cells)
    return rows


def first_python3_span(entry):
    m = re.search(r"`(python3 [^`]*)`", entry)
    return m.group(1) if m else None


def selftest_unbacked(cell, lane):
    if re.search(r"\bno\b.{0,24}--[a-z][a-z0-9-]*", cell):
        return False
    scripts = sorted(set(re.findall(r"(?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py", cell)))
    flags = sorted(set(FLAG.findall(cell)))
    if len(scripts) != 1 or not flags:
        return False
    path = lane / scripts[0]
    if not path.exists():
        return False
    body = path.read_text(errors="replace")
    return all(f not in body for f in flags)


def sha_prefix(path, n=12):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:n]


def main():
    skill = (LANE / "SKILL.md").read_text(errors="replace")
    rows = {r[0].strip("`"): r for r in parse_rows(registry_block(skill))}
    out = {}
    for name in NEW:
        if name not in rows:
            out[name] = {"present": False}
            continue
        r = rows[name]
        entry, vmap, st = r[2], r[3], r[4]
        pinned = r[5]
        m = CMD.search(entry)
        script = m.group(1) if m else None
        span = first_python3_span(entry)
        rec = {
            "present": True,
            "kind": r[1],
            "entry_cell": entry,
            "entry_span": span,
            "script": script,
            "script_in_lane": (LANE / script).exists() if script else None,
            "script_in_clone": (CLONE / script).exists() if script else None,
            "verdict_map": vmap,
            "selftest_cell": st,
            "pinned_cell": pinned,
            "scope_cell": r[6],
            "owner_cell": r[7],
        }
        # pinned sha check
        if script and (LANE / script).exists():
            actual = sha_prefix(LANE / script)
            rec["sha_actual"] = actual
            rec["sha_in_pinned"] = actual[:8] in pinned or actual[:12] in pinned or actual in pinned
        # selftest unbacked + flags in body
        rec["selftest_unbacked"] = selftest_unbacked(st, LANE)
        scripts_in_st = sorted(set(re.findall(r"(?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py", st)))
        flags_in_st = sorted(set(FLAG.findall(st)))
        rec["st_scripts"] = scripts_in_st
        rec["st_flags"] = flags_in_st
        if scripts_in_st and (LANE / scripts_in_st[0]).exists():
            body = (LANE / scripts_in_st[0]).read_text(errors="replace")
            rec["st_flags_in_body"] = {f: (f in body) for f in flags_in_st}
        out[name] = rec
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
