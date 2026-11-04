#!/usr/bin/env python3
"""R82-C2 repair checks — one subcommand per round-81 spot-check id (V1…V7).

Each check exits 0 exactly when its repair holds at the tree it is run in, and non-zero at the base
revision (a check that cannot fail is `CHECK-TRIVIAL` in the counter). Run from the lane root:

    python3 plans/round82_c2_checks.py u1     # V1 clean-tree C2 receipt
    python3 plans/round82_c2_checks.py u2     # V2 corrected counts/anchors (supersede rows)
    python3 plans/round82_c2_checks.py u3     # V3 provenance trio
    python3 plans/round82_c2_checks.py u4     # V4 docstring count == battery count
    python3 plans/round82_c2_checks.py u5     # V5 the stray --lane/ directory is gone
    python3 plans/round82_c2_checks.py u6     # V6 wave attack share + live mutation seat
    python3 plans/round82_c2_checks.py u7     # V7 determinism.txt carries COMMAND and REV
    python3 plans/round82_c2_checks.py --all  # every check, one line each
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

LANE = Path(".")

RECEIPT_V1 = "corpus/evidence/round81/c2-after.txt"
DET_V7 = "corpus/evidence/round81/determinism.txt"
SOURCES = "corpus/SOURCES.md"
LESSON81 = "corpus/lessons/round-81.md"
KNOW = "corpus/knowledge/tb2-file-artifact-replay-classes.md"
DEBT81 = "plans/round81_c2_spotcheck_debt.py"
RESULTS = ".ufo/waves/round-82/w1/w1-results.json"
RESULTS_ALT = ".ufo/waves/round-82/w1-results.json"


def read(rel: str) -> str | None:
    p = LANE / rel
    return p.read_text(errors="replace") if p.is_file() else None


def row(text: str, ident: str) -> str | None:
    for line in text.split("\n"):
        if line.startswith("| %s |" % ident):
            return line
    return None


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def u1() -> int:
    t = read(RECEIPT_V1)
    if t is None:
        print("CHECK u1 missing %s" % RECEIPT_V1)
        return 1
    clean = sum(1 for l in t.split("\n") if l.strip() == "WORKTREE clean")
    dirty = sum(1 for l in t.split("\n") if l.strip().startswith("WORKTREE dirty"))
    ok = clean == 1 and dirty == 0
    print("CHECK u1 clean=%d dirty=%d %s" % (clean, dirty, "ok" if ok else "fail"))
    return 0 if ok else 1


def u2() -> int:
    s = read(SOURCES)
    if s is None:
        print("CHECK u2 missing %s" % SOURCES)
        return 1
    probs = []
    # S260/S261 keep their bytes (Q34 immutability) and the correction lands as a supersede row.
    r260, r261 = row(s, "S260"), row(s, "S261")
    r265, r266 = row(s, "S265"), row(s, "S266")
    if not (r260 and r261):
        probs.append("frozen rows absent")
    if not r265 or "supersedes S260" not in r265:
        probs.append("no S265 supersedes S260")
    if not r266 or "supersedes S261" not in r266:
        probs.append("no S266 supersedes S261")
    if r265:
        c = cells(r265)
        anchor = c[5]
        quote = re.search(r"“([^”]+)”", anchor)
        m = re.search(r"\((\d+) words", anchor)
        if not quote or not m or len(quote.group(1).split()) != int(m.group(1)):
            probs.append("S265 quote count != %d" % (len(quote.group(1).split()) if quote else -1))
        if ":1-15" not in anchor or "stamp 2-14" not in anchor:
            probs.append("S265 anchor range")
    if r266:
        c = cells(r266)
        quotes = re.findall(r"“([^”]+)”\s*\((\d+) words", c[5])
        if len(quotes) != 2 or any(len(q.split()) != int(n) for q, n in quotes):
            probs.append("S266 quote counts")
    # the round-81 lesson's own counts recompute
    lesson = read(LESSON81)
    if lesson is None:
        probs.append("lesson absent")
    else:
        for frag in re.findall(r"“([^”]+)”\s*\((\d+) words", lesson):
            if len(frag[0].split()) != int(frag[1]):
                probs.append("lesson count %r" % (frag[0][:30],))
    ok = not probs
    print("CHECK u2 %s" % ("ok" if ok else "fail: " + "; ".join(probs)))
    return 0 if ok else 1


def u3() -> int:
    t = read(KNOW)
    if t is None:
        print("CHECK u3 missing %s" % KNOW)
        return 1
    head = t.split("\n")[:3]
    want = ("source:", "verified-at:", "recheck:")
    ok = all(h.startswith(w) for h, w in zip(head, want))
    print("CHECK u3 trio=%s %s" % ("yes" if ok else "no", "ok" if ok else "fail"))
    return 0 if ok else 1


def u4() -> int:
    src = read(DEBT81)
    if src is None:
        print("CHECK u4 missing %s" % DEBT81)
        return 1
    m = re.search(r'"?(Six|Four|Five|Seven|Eight|Nine|Ten)\b[^"]{0,40}mutations', src)
    words = {"Six": 6, "Four": 4, "Five": 5, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10}
    stated = words.get(m.group(1)) if m else None
    import tempfile
    work = tempfile.mkdtemp(prefix="r82-u4-")     # honours TMPDIR; never a hardcoded /tmp
    out = subprocess.run([sys.executable, DEBT81, "--mutants", "--work", work],
                         capture_output=True, text=True)
    import shutil
    shutil.rmtree(work, ignore_errors=True)
    real = re.search(r"MUTANTS real=(\d+)", out.stdout)
    n = int(real.group(1)) if real else None
    ok = stated is not None and n is not None and stated == n
    print("CHECK u4 docstring=%s battery=%s %s" % (stated, n, "ok" if ok else "fail"))
    return 0 if ok else 1


def u5() -> int:
    # the defect was an UNTRACKED directory, so a git-archive tree can never carry it: the repair is
    # "removed" and the removal is recorded where a reader of a tree can re-derive it.
    absent = not (LANE / "--lane").exists()
    lesson = read("corpus/lessons/round-82.md") or ""
    recorded = ("R81-V5" in lesson) and ("--lane/" in lesson)
    ok = absent and recorded
    print("CHECK u5 stray-dir=%s recorded=%s %s" % (
        "absent" if absent else "present", "yes" if recorded else "no", "ok" if ok else "fail"))
    return 0 if ok else 1


def u6() -> int:
    t = read(RESULTS)
    if t is None:
        t = read(RESULTS_ALT)
    if t is None:
        print("CHECK u6 missing %s" % RESULTS)
        return 1
    try:
        doc = json.loads(t)
    except Exception:
        print("CHECK u6 unreadable")
        return 1
    seats = doc.get("results") or doc.get("seats") or []
    if isinstance(seats, dict):
        seats = list(seats.values())
    roles = {}
    live_mut = 0
    for s in seats:
        if not isinstance(s, dict):
            continue
        role = s.get("role") or s.get("agent") or ""
        roles[role] = roles.get(role, 0) + 1
        status = str(s.get("status") or "").lower()
        if role == "mutation-tester":
            produced = bool((s.get("output") or "").strip()) or bool(str(s.get("note") or "").strip())
            if status not in ("dead", "failed", "error", "killed") and produced:
                live_mut += 1
    attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester", "labrat"))
    total = sum(roles.values())
    share = (attack / total) if total else 0.0
    ok = total > 0 and share >= 0.25 and live_mut > 0
    print("CHECK u6 seats=%d attack=%d share=%.3f mutation_seats=%d live=%d %s" % (
        total, attack, share, roles.get("mutation-tester", 0), live_mut, "ok" if ok else "fail"))
    return 0 if ok else 1


def u7() -> int:
    t = read(DET_V7)
    if t is None:
        print("CHECK u7 missing %s" % DET_V7)
        return 1
    cmds = [l for l in t.split("\n") if l.startswith("COMMAND ")]
    revs = [l for l in t.split("\n") if l.startswith("REV ")]
    ok = bool(cmds) and bool(revs) and all(len(c.split()) > 2 for c in cmds)
    print("CHECK u7 commands=%d revs=%d %s" % (len(cmds), len(revs), "ok" if ok else "fail"))
    return 0 if ok else 1


CHECKS = {"u1": u1, "u2": u2, "u3": u3, "u4": u4, "u5": u5, "u6": u6, "u7": u7}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("check", nargs="?", choices=sorted(CHECKS))
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args(argv)
    if a.all:
        rc = 0
        for k in sorted(CHECKS):
            rc = max(rc, CHECKS[k]())
        return rc
    if not a.check:
        print("SETUP one of %s or --all required" % ", ".join(sorted(CHECKS)))
        return 2
    return CHECKS[a.check]()


if __name__ == "__main__":
    sys.exit(main())
