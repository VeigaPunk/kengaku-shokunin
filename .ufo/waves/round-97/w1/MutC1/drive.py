#!/usr/bin/env python3
"""Mutation driver for R97-C1 / R97-C2 counters. Private scratch only."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

T = "f1083da60e7ff6b88f7420aae7424f7762d14700"
BASE = "4992cd0e32b8db23ca20310deb7de12d485f8bcc"
ROOT = Path("/fast/scratch/hyaku/kengaku-r97/MutC1")
VENV = ROOT / "G"
SKILL = "SKILL.md"
RECEIPT = "corpus/evidence/round97/sparql-probe.txt"
TABLE = "plans/round97-cases.json"
PROBE = "plans/round97_sparql_probe.py"
LEDGER = "plans/grader-population-ledger.json"
CENSUS = "plans/round97_gate_selftest_census.py"


def git(tree: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(tree), *args], capture_output=True, text=True, timeout=300)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rd(tree: Path, rel: str) -> str:
    return (tree / rel).read_text()


def wr(tree: Path, rel: str, text: str) -> None:
    (tree / rel).write_text(text)


def sub(tree: Path, rel: str, old: str, new: str, n: int = 1) -> None:
    t = rd(tree, rel)
    got = t.count(old)
    assert got == n, f"{rel}: anchor {old[:50]!r} occurs {got}, want {n}"
    wr(tree, rel, t.replace(old, new))


# ------------------------------------------------------------------ C1 mutants
def c1_L1_receipt_absent(tree: Path, ctx: dict) -> None:
    (tree / RECEIPT).unlink()


def c1_L2_subject_forged(tree: Path, ctx: dict) -> None:
    sub(tree, RECEIPT, "SUBJECT_SHA ecf15840fc14f1eeff2f3b6317d7f0febc8fa81f688d24e3054205ba13207b39",
        "SUBJECT_SHA " + "0" * 64)


def c1_L2_capture_byte(tree: Path, ctx: dict) -> None:
    p = tree / "corpus/evidence/round97/graders/sparql-university/tests/test.sh"
    p.write_bytes(p.read_bytes() + b"# tampered\n")


def c1_L3_tip_orphan(tree: Path, ctx: dict) -> None:
    t = rd(tree, RECEIPT)
    t = re.sub(r"(?m)^LANE_TIP .*$", "LANE_TIP " + ctx["orphan"], t)
    wr(tree, RECEIPT, t)


def c1_L4_table_reformat(tree: Path, ctx: dict) -> None:
    t = rd(tree, TABLE)
    t2 = t.replace('"member": "sparql-university"', '"member":  "sparql-university"', 1)
    assert t2 != t
    wr(tree, TABLE, t2)
    t = rd(tree, RECEIPT)
    t = re.sub(r"(?m)^CASE_TABLE_SHA .*$", "CASE_TABLE_SHA " + sha(t2.encode()), t)
    wr(tree, RECEIPT, t)


def c1_L5_predicted_token(tree: Path, ctx: dict) -> None:
    sub(tree, RECEIPT, "CASE C07 predicted=P,P,F,0 observed=P,P,F,0",
        "CASE C07 predicted=P,P,P,1 observed=P,P,F,0")


def c1_L5_drop_case(tree: Path, ctx: dict) -> None:
    lines = [l for l in rd(tree, RECEIPT).split("\n")
             if not (l.startswith("CASE C18 ") or l.startswith("DETAIL C18 "))]
    wr(tree, RECEIPT, "\n".join(lines))


def c1_L6_detail_forge(tree: Path, ctx: dict) -> None:
    sub(tree, RECEIPT, "DETAIL C07 form=SELECT vars=professorName+countries rows=5 distinct=5",
        "DETAIL C07 form=SELECT vars=professorName+countries rows=4 distinct=4")


def c1_L6_graderside_forge(tree: Path, ctx: dict) -> None:
    sub(tree, RECEIPT, "GRADER_SIDE python,rdflib,pytest 3.13 7.1.4 8.4.1",
        "GRADER_SIDE python,rdflib,pytest 3.13 7.1.5 8.4.1")


def c1_L6_unpinned_forge(tree: Path, ctx: dict) -> None:
    sub(tree, RECEIPT, "GRADER_UNPINNED python,pyparsing 3.13.16 3.3.3",
        "GRADER_UNPINNED python,pyparsing 3.13.99 3.2.0")


def _ledger(tree: Path) -> dict:
    return json.loads(rd(tree, LEDGER))


def _put_ledger(tree: Path, led: dict) -> None:
    wr(tree, LEDGER, json.dumps(led, indent=2) + "\n")


def c1_L7_status_pending(tree: Path, ctx: dict) -> None:
    led = _ledger(tree)
    led["members"]["sparql-university"]["status"] = "pending"
    _put_ledger(tree, led)


def c1_L7_remove_base(tree: Path, ctx: dict) -> None:
    led = _ledger(tree)
    led["members"][ctx["victim"]]["status"] = "unexecuted"
    _put_ledger(tree, led)


def c1_L7_extra_executed(tree: Path, ctx: dict) -> None:
    led = _ledger(tree)
    led["members"]["zzz-calibration-ghost"] = {
        "classes": ["file-artifact"], "receipt": RECEIPT, "round": 97,
        "status": "executed", "subject": "tb2-header", "verdict": "cases"}
    _put_ledger(tree, led)


def c1_L7_classes(tree: Path, ctx: dict) -> None:
    led = _ledger(tree)
    led["members"]["sparql-university"]["classes"] = ["file-artifact", "subprocess-exec"]
    _put_ledger(tree, led)


def c1_L7_legacy_receipt(tree: Path, ctx: dict) -> None:
    led = _ledger(tree)
    led["members"]["sparql-university"]["receipt"] = "corpus/evidence/round97/other.txt"
    _put_ledger(tree, led)


def c1_L8_probe_comment(tree: Path, ctx: dict) -> None:
    p = tree / PROBE
    p.write_bytes(p.read_bytes() + b"\n# calibration probe comment\n")
    t = rd(tree, RECEIPT)
    t = re.sub(r"(?m)^TOOL_SHA .*$", "TOOL_SHA " + sha(p.read_bytes()), t)
    wr(tree, RECEIPT, t)


def c1_L9_bash(tree: Path, ctx: dict) -> None:
    t = re.sub(r"(?m)^HOST_BASH .*$",
               "HOST_BASH GNU bash, version 9.9.9(1)-release (x86_64-pc-linux-gnu)", rd(tree, RECEIPT))
    wr(tree, RECEIPT, t)


def c1_L9_toolsha(tree: Path, ctx: dict) -> None:
    t = re.sub(r"(?m)^TOOL_SHA .*$", "TOOL_SHA " + "0" * 64, rd(tree, RECEIPT))
    wr(tree, RECEIPT, t)


def c1_forged_receipt(tree: Path, ctx: dict) -> None:
    out = []
    for line in rd(tree, RECEIPT).split("\n"):
        if line.startswith("DETAIL "):
            line = re.sub(r"rows=\d+ distinct=\d+ names=\S*", "rows=4 distinct=4 names=-", line)
        out.append(line)
    wr(tree, RECEIPT, "\n".join(out))


def c1_ledger_only_base(tree: Path, ctx: dict) -> None:
    """BASE tree + ledger flip only: no receipt, no capture, no probe."""
    led = _ledger(tree)
    led["members"]["sparql-university"] = {
        "classes": ["file-artifact"], "evidence": "ledger-only control",
        "reason": "replayed", "receipt": RECEIPT, "round": 97,
        "status": "executed", "subject": "tb2-header", "verdict": "cases"}
    _put_ledger(tree, led)


C1 = {
    "c1-L1-receipt-absent": c1_L1_receipt_absent,
    "c1-L2-subject-forged": c1_L2_subject_forged,
    "c1-L2-capture-byte": c1_L2_capture_byte,
    "c1-L3-tip-orphan": c1_L3_tip_orphan,
    "c1-L4-table-reformat": c1_L4_table_reformat,
    "c1-L5-predicted-token": c1_L5_predicted_token,
    "c1-L5-drop-case": c1_L5_drop_case,
    "c1-L6-detail-forge": c1_L6_detail_forge,
    "c1-L6-graderside-forge": c1_L6_graderside_forge,
    "c1-L6-unpinned-forge": c1_L6_unpinned_forge,
    "c1-L7-status-pending": c1_L7_status_pending,
    "c1-L7-remove-base": c1_L7_remove_base,
    "c1-L7-extra-executed": c1_L7_extra_executed,
    "c1-L7-classes": c1_L7_classes,
    "c1-L7-legacy-receipt": c1_L7_legacy_receipt,
    "c1-L8-probe-comment": c1_L8_probe_comment,
    "c1-L9-bash": c1_L9_bash,
    "c1-L9-toolsha": c1_L9_toolsha,
    "c1-forged-receipt": c1_forged_receipt,
    "c1-ledger-only-base": c1_ledger_only_base,
}


def c1_L2_member_field(tree: Path, ctx: dict) -> None:
    sub(tree, RECEIPT, "MEMBER sparql-university", "MEMBER other-grader")


def c1_L6_legorder_field(tree: Path, ctx: dict) -> None:
    sub(tree, RECEIPT, "LEG_ORDER exists,runs,results,reward", "LEG_ORDER a,b,c,d")


C1["c1-L2-member-field"] = c1_L2_member_field
C1["c1-L6-legorder-field"] = c1_L6_legorder_field


# ------------------------------------------------------------------ C2 mutants
def skill_block(tree: Path) -> tuple[list[str], int]:
    lines = rd(tree, SKILL).split("\n")
    starts = [i for i, l in enumerate(lines) if l.startswith("## Gate/probe registry")]
    assert len(starts) == 1
    return lines, starts[0]


def find_row(lines: list[str], start: int, name: str) -> int:
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            break
        if lines[i].startswith("| `" + name + "`"):
            return i
    raise AssertionError(f"row {name} not found")


def cells_of(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def rebuild(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def set_cell(tree: Path, name: str, idx: int, value: str) -> None:
    lines, start = skill_block(tree)
    i = find_row(lines, start, name)
    cells = cells_of(lines[i])
    cells[idx] = value
    lines[i] = rebuild(cells)
    wr(tree, SKILL, "\n".join(lines))


def c2_M1_revert_kind(tree: Path, ctx: dict) -> None:
    set_cell(tree, "ledger-tip", 1, "gate")


def c2_M2_blanket(tree: Path, ctx: dict) -> None:
    set_cell(tree, "interval-reverdict", 1, "probe")


def c2_M3_cell_forge(tree: Path, ctx: dict) -> None:
    set_cell(tree, "ledger-tip", 4, "`--selftest`")


def c2_M4_delete_row(tree: Path, ctx: dict) -> None:
    lines, start = skill_block(tree)
    i = find_row(lines, start, "ledger-tip")
    del lines[i]
    wr(tree, SKILL, "\n".join(lines))


def c2_M5_duplicate_row(tree: Path, ctx: dict) -> None:
    lines, start = skill_block(tree)
    i = find_row(lines, start, "ledger-tip")
    lines.insert(i + 1, lines[i])
    wr(tree, SKILL, "\n".join(lines))


def c2_M6_script_forge(tree: Path, ctx: dict) -> None:
    p = tree / "plans/ledger_tip.py"
    p.write_bytes(p.read_bytes() + b'\nif "--selftest" in sys.argv:\n    pass\n')


def c2_M7_comment_forge(tree: Path, ctx: dict) -> None:
    set_cell(tree, "ledger-tip", 1, "gate")
    p = tree / "plans/ledger_tip.py"
    p.write_bytes(p.read_bytes() + b'\n# "--selftest" in sys.argv (comment)\n')


def _append_row(tree: Path, name: str, script_body: str) -> None:
    lines, start = skill_block(tree)
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    row = f"| `{name}` | gate | `python3 plans/{name}.py` | `0` clean · `1` failed | none | pins | read-only | kengaku |"
    lines.insert(end, row)
    wr(tree, SKILL, "\n".join(lines))
    (tree / f"plans/{name}.py").write_text(script_body)


def c2_M8_new_gate_plain(tree: Path, ctx: dict) -> None:
    _append_row(tree, "mut-new-gate", "import sys\nsys.exit(0)\n")


def c2_M9_dead_branch(tree: Path, ctx: dict) -> None:
    _append_row(tree, "mut-dead-branch",
                'import sys\nif False and "--selftest" in sys.argv:\n    pass\nsys.exit(0)\n')


def c2_M10_prose_mention(tree: Path, ctx: dict) -> None:
    _append_row(tree, "mut-prose",
                '# the parser accepts "--selftest" in prose only\nimport sys\nsys.exit(0)\n')


def c2_M11_kind_case(tree: Path, ctx: dict) -> None:
    set_cell(tree, "ledger-tip", 1, "Gate")


def c2_M12_no_script_entry(tree: Path, ctx: dict) -> None:
    set_cell(tree, "ledger-tip", 2, "`python3 -m ledger_tip`")


def _drop_pattern(tree: Path, pattern: str) -> None:
    t = rd(tree, CENSUS)
    assert t.count(pattern) == 1, (pattern, t.count(pattern))
    wr(tree, CENSUS, t.replace(pattern, ""))


def c2_M13_narrow_p3(tree: Path, ctx: dict) -> None:
    _drop_pattern(tree, 'r"[\\"\']--self-?test[\\"\']\\s*(?:in|==|not in)\\b",\n')


def c2_M14_always_true(tree: Path, ctx: dict) -> None:
    sub(tree, CENSUS, "    return any(p.search(text) for p in SPELLING)",
        "    return True")


def c2_M15_always_false(tree: Path, ctx: dict) -> None:
    sub(tree, CENSUS, "    return any(p.search(text) for p in SPELLING)",
        "    return False")


def c2_M16_narrow_p1(tree: Path, ctx: dict) -> None:
    _drop_pattern(tree, 'r"add_parser\\(\\s*[\\"\']self-?test[\\"\']",\n')


C2 = {
    "c2-M1-revert-kind": c2_M1_revert_kind,
    "c2-M2-blanket": c2_M2_blanket,
    "c2-M3-cell-forge": c2_M3_cell_forge,
    "c2-M4-delete-row": c2_M4_delete_row,
    "c2-M5-duplicate-row": c2_M5_duplicate_row,
    "c2-M6-script-forge": c2_M6_script_forge,
    "c2-M7-comment-forge": c2_M7_comment_forge,
    "c2-M8-new-gate-plain": c2_M8_new_gate_plain,
    "c2-M9-dead-branch": c2_M9_dead_branch,
    "c2-M10-prose-mention": c2_M10_prose_mention,
    "c2-M11-kind-case": c2_M11_kind_case,
    "c2-M12-no-script-entry": c2_M12_no_script_entry,
    "c2-M13-narrow-p3": c2_M13_narrow_p3,
    "c2-M14-always-true": c2_M14_always_true,
    "c2-M15-always-false": c2_M15_always_false,
    "c2-M16-narrow-p1": c2_M16_narrow_p1,
}


def c2_M17_narrow_p3(tree: Path, ctx: dict) -> None:
    _drop_pattern(tree, 'r"(?:\\bin|==)\\s*\\(?[\\"\']--self-?test[\\"\']",\n')


def c2_M18_new_gate_no_script(tree: Path, ctx: dict) -> None:
    lines, start = skill_block(tree)
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    lines.insert(end, "| `mut-no-script` | gate | `python3 -m mut_no_script` | `0` clean · `1` failed | none | pins | read-only | kengaku |")
    wr(tree, SKILL, "\n".join(lines))


C2["c2-M17-narrow-p3"] = c2_M17_narrow_p3
C2["c2-M18-new-gate-no-script"] = c2_M18_new_gate_no_script


def base_victim(tree: Path) -> str:
    base = json.loads(git(tree, "show", f"{BASE}:{LEDGER}").stdout)
    for name, v in base["members"].items():
        if v.get("status") == "executed" and name != "sparql-university":
            return name
    raise AssertionError("no base member")


def run_c1(tree: Path, mid: str, fn, ctx: dict, outdir: Path) -> dict:
    start = BASE if mid == "c1-ledger-only-base" else T
    assert git(tree, "rev-parse", "--show-toplevel").stdout.strip() == str(tree)
    git(tree, "checkout", "-q", "--detach", start)
    git(tree, "clean", "-fdq")
    fn(tree, ctx)
    git(tree, "add", "-A")
    c = git(tree, "-c", "user.name=mut", "-c", "user.email=mut@invalid",
            "commit", "-q", "--no-gpg-sign", "-m", mid)
    assert c.returncode == 0, c.stderr
    rev = git(tree, "rev-parse", "HEAD").stdout.strip()
    work = ROOT / "work" / mid
    p = subprocess.run([sys.executable, "plans/round97_c1_replay.py", "--lane", ".", "--rev", rev,
                        "--work", str(work), "--grader-venv", str(VENV)],
                       cwd=tree, capture_output=True, text=True, timeout=3600)
    out = p.stdout + p.stderr
    (outdir / f"{mid}.txt").write_text(f"# clone {tree}\n# rev {rev}\n# rc {p.returncode}\n{out}")
    git(tree, "checkout", "-q", "--detach", T)
    git(tree, "clean", "-fdq")
    st = git(tree, "status", "--porcelain").stdout.strip()
    head = git(tree, "rev-parse", "HEAD").stdout.strip()
    return {"id": mid, "rev": rev, "rc": p.returncode, "out": out,
            "restored": st == "" and head == T}


def run_c2(tree: Path, mid: str, fn, ctx: dict, outdir: Path) -> dict:
    assert git(tree, "rev-parse", "--show-toplevel").stdout.strip() == str(tree)
    git(tree, "checkout", "-q", "--detach", T)
    git(tree, "clean", "-fdq")
    fn(tree, ctx)
    git(tree, "add", "-A")
    c = git(tree, "-c", "user.name=mut", "-c", "user.email=mut@invalid",
            "commit", "-q", "--no-gpg-sign", "-m", mid)
    assert c.returncode == 0, c.stderr
    rev = git(tree, "rev-parse", "HEAD").stdout.strip()
    work = ROOT / "work" / mid
    work.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([sys.executable, str(tree / CENSUS), "--lane", str(tree), "--rev", rev],
                       capture_output=True, text=True, timeout=600)
    out = p.stdout + p.stderr
    (outdir / f"{mid}.census.txt").write_text(f"# clone {tree}\n# detector+target rev {rev}\n# rc {p.returncode}\n{out}")
    q = subprocess.run([sys.executable, str(tree / CENSUS), "--selftest", "--work", str(work)],
                       capture_output=True, text=True, timeout=900)
    out2 = q.stdout + q.stderr
    (outdir / f"{mid}.selftest.txt").write_text(f"# clone {tree}\n# detector rev {rev}\n# rc {q.returncode}\n{out2}")
    git(tree, "checkout", "-q", "--detach", T)
    git(tree, "clean", "-fdq")
    st = git(tree, "status", "--porcelain").stdout.strip()
    head = git(tree, "rev-parse", "HEAD").stdout.strip()
    return {"id": mid, "rev": rev, "rc": p.returncode, "out": out,
            "selftest_rc": q.returncode, "selftest": out2,
            "restored": st == "" and head == T}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", required=True)
    ap.add_argument("--kind", choices=("c1", "c2"), required=True)
    ap.add_argument("--ids", required=True)
    a = ap.parse_args()
    tree = ROOT / a.clone
    outdir = ROOT / "out"
    outdir.mkdir(parents=True, exist_ok=True)
    ids = [x for x in a.ids.split(",") if x]
    reg = C1 if a.kind == "c1" else C2
    ctx = {"orphan": "", "victim": ""}
    if a.kind == "c1":
        empty = git(tree, "hash-object", "-t", "tree", "/dev/null").stdout.strip()
        ctx["orphan"] = git(tree, "-c", "user.name=mut", "-c", "user.email=mut@invalid",
                            "commit-tree", empty, "-m", "orphan").stdout.strip()
        ctx["victim"] = base_victim(tree)
    summary = []
    for mid in ids:
        r = (run_c1 if a.kind == "c1" else run_c2)(tree, mid, reg[mid], ctx, outdir)
        summary.append(r)
        print(f"== {mid} rev={r['rev'][:12]} rc={r['rc']} restored={r['restored']}")
        for line in r["out"].splitlines():
            if line.startswith(("LEGS ", "TARGET ", "PREDICATE ", "ROWS ", "GATES ", "MISMATCH_TOTAL ",
                                "DEFECT ", "SELFTEST ")) or re.match(r"^(ROW-|CELL-|DEMOTED|SCRIPT-|MISMATCH )", line):
                print("   " + line)
        if a.kind == "c2":
            print(f"   selftest_rc={r['selftest_rc']} " +
                  " ".join(l for l in r["selftest"].splitlines() if l.startswith("SELFTEST ")))
    (outdir / f"summary-{a.clone}.json").write_text(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
