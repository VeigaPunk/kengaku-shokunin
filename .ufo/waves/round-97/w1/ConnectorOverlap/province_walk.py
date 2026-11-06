#!/usr/bin/env python3
"""Read-only province walk for round 97: C1/C2 cell accounting and detector soundness.

Reads only `git show REV:path` from the lane. Writes nothing.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
BASE = "4992cd0e32b8db23ca20310deb7de12d485f8bcc"
T = "f1083da60e7ff6b88f7420aae7424f7762d14700"
F = "8d9d271306c4e7e2d586e51cd546652249d286cb"
SKILL = "SKILL.md"
HEADING = "## Gate/probe registry"
SPLIT = re.compile(r"(?<!\\)\|")
SCRIPT = re.compile(r"([\w./-]+\.(?:py|sh|mjs))")
SPELLING = [re.compile(p) for p in (
    r"add_argument\(\s*[\"']--self-?test[\"']",
    r"add_parser\(\s*[\"']self-?test[\"']",
    r"[\"']--self-?test[\"']\s*(?:in|==|not in)\b",
    r"(?:\bin|==)\s*\(?[\"']--self-?test[\"']",
    r"def run_selftest\b",
    r"(?:==|\bin)\s*\(?[\"']self-?test[\"']",
)]


def git(*args):
    return subprocess.run(["git", "-C", str(LANE), *args], capture_output=True, timeout=120)


def blob(rev, path):
    p = git("show", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None


def registry(rev):
    data = blob(rev, SKILL)
    lines = data.decode(errors="replace").split("\n")
    starts = [i for i, l in enumerate(lines) if l.startswith(HEADING)]
    assert len(starts) == 1, starts
    rows = []
    for i, line in enumerate(lines[starts[0] + 1:], start=starts[0] + 2):
        if line.startswith("## "):
            break
        if line.startswith("| `"):
            rows.append((i, [c.strip() for c in SPLIT.split(line.strip())[1:-1]]))
    return rows, starts[0] + 1


def script_of(row):
    m = SCRIPT.search(row[2]) if len(row) > 2 else None
    return m.group(1) if m else None


def classify_match(text, m):
    """Return 'code' or 'prose' for a spelling match by line context."""
    line_start = text.rfind("\n", 0, m.start()) + 1
    line_end = text.find("\n", m.end())
    line = text[line_start:line_end if line_end != -1 else len(text)]
    stripped = line.strip()
    if stripped.startswith("#"):
        return "prose"
    # triple-quote state: count unescaped triple quotes before the match
    before = text[:m.start()]
    for q in ('"""', "'''"):
        if before.count(q) % 2 == 1:
            return "prose"
    return "code"


def main():
    out = {}
    base_rows, _ = registry(BASE)
    rev_rows, reg_line = registry(T)
    by_base = {cells[0]: (lineno, cells) for lineno, cells in base_rows}
    by_rev = {cells[0]: (lineno, cells) for lineno, cells in rev_rows}
    out["rows_base"] = len(base_rows)
    out["rows_rev"] = len(rev_rows)
    out["registry_heading_line"] = reg_line
    kind_changed, other_changed, added = [], [], []
    for name, (_, bc) in by_base.items():
        if name not in by_rev:
            out.setdefault("removed", []).append(name)
            continue
        rc = by_rev[name][1]
        diffs = [i for i in range(max(len(bc), len(rc))) if (bc[i] if i < len(bc) else None) != (rc[i] if i < len(rc) else None)]
        if diffs == [1]:
            kind_changed.append((name, bc[1], rc[1]))
        elif diffs:
            other_changed.append((name, diffs, [bc[i] if i < len(bc) else None for i in diffs], [rc[i] if i < len(rc) else None for i in diffs]))
    for name in by_rev:
        if name not in by_base:
            added.append((name, by_rev[name][1][1], script_of(by_rev[name][1])))
    out["kind_changed_n"] = len(kind_changed)
    out["kind_changed"] = kind_changed
    out["other_changed"] = other_changed
    out["added_rows"] = added

    # base mismatch list from the L1 receipt
    receipt = (LANE / ".ufo/waves/round-97/L1/c2-base.txt").read_text()
    base_mismatch = [l.split("`")[1] for l in receipt.splitlines() if l.startswith("MISMATCH ")]
    out["base_mismatch_n"] = len(base_mismatch)
    out["kind_changed_set_equals_base_mismatch"] = sorted(n for n, _, _ in kind_changed) == sorted(base_mismatch)
    out["kind_changed_only_gate_to_probe"] = all(b == "gate" and r == "probe" for _, b, r in kind_changed)

    # detector soundness at T: gate rows whose only spelling is prose
    prose_only, code_only, both, no_match = [], [], [], []
    gate_rows = 0
    for lineno, cells in rev_rows:
        if len(cells) < 3 or cells[1] != "gate":
            continue
        gate_rows += 1
        s = script_of(cells)
        body = blob(T, s) if s else None
        text = (body or b"").decode(errors="replace")
        kinds = []
        for p in SPELLING:
            for m in p.finditer(text):
                kinds.append((classify_match(text, m), m.group(0)[:40]))
        has_code = any(k == "code" for k, _ in kinds)
        has_prose = any(k == "prose" for k, _ in kinds)
        rec = (cells[0], s, len(kinds), sorted({k for k, _ in kinds}))
        if has_code and has_prose:
            both.append(rec)
        elif has_code:
            code_only.append(rec)
        elif has_prose:
            prose_only.append(rec)
        else:
            no_match.append(rec)
    out["gates_at_T"] = gate_rows
    out["spelling_code_only_n"] = len(code_only)
    out["spelling_prose_only_n"] = len(prose_only)
    out["spelling_prose_only"] = prose_only
    out["spelling_both_n"] = len(both)
    out["spelling_none_n"] = len(no_match)

    # ledger accounting
    lb = json.loads(blob(BASE, "plans/grader-population-ledger.json").decode())["members"]
    lt = json.loads(blob(T, "plans/grader-population-ledger.json").decode())["members"]
    def counts(m):
        ex = {n: v for n, v in m.items() if v.get("status") == "executed"}
        fa = {n for n, v in ex.items() if "file-artifact" in v.get("classes", [])}
        return len(m), len(ex), len(fa), ex
    nb, eb, fb, exb = counts(lb)
    nt, et, ft, ext = counts(lt)
    out["ledger"] = {
        "members_base": nb, "executed_base": eb, "file_artifact_executed_base": fb,
        "members_T": nt, "executed_T": et, "file_artifact_executed_T": ft,
        "set_superset": set(ext) >= set(exb),
        "added": sorted(set(ext) - set(exb)),
        "removed": sorted(set(exb) - set(ext)),
        "sparql_row": lt.get("sparql-university"),
    }
    # class table row for file-artifact at T and its line
    lines = blob(T, SKILL).decode(errors="replace").split("\n")
    for i, l in enumerate(lines, 1):
        if l.startswith("| file-artifact |"):
            out["file_artifact_row_line"] = i
            out["file_artifact_row"] = l
            break
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
