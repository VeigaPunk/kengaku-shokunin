#!/usr/bin/env python3
"""C2ChecksR81 — R81-C2 repair checks (seat C2ChecksR81, wave round-81/w1 deliverable).

One subcommand per routed defect (u1..u6) plus --all; each exits 0 exactly when its
repair holds in the tree it is run from (repo-relative: run from the lane root), and
non-zero otherwise. The integrated copy the routed-findings rows invoke is
plans/round81_c2_checks.py; this seat deliverable re-derives the same six contracts
independently so the two implementations can be diffed against each other.

    python3 .ufo/waves/round-81/w1/C2ChecksR81.py u1 … u6
    python3 .ufo/waves/round-81/w1/C2ChecksR81.py --all

Exit 0 pass, 1 fail.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

MEMBERS = ("cancel-async-tasks", "chess-best-move", "distribution-search",
           "largest-eigenval", "openssl-selfsigned-cert", "protein-assembly")
ROW = re.compile(r"^\|[ \t]*S[0-9]{3,}[ \t]*\|")


def rd(rel: str) -> str:
    try:
        return Path(rel).read_text(errors="replace")
    except OSError:
        return ""


def u1() -> list[str]:
    """A superseding SOURCES row states the corrected round-80 receipt anchors (R80-U1)."""
    bad: list[str] = []
    sup = [ln for ln in rd("corpus/SOURCES.md").splitlines() if "supersedes S258 —" in ln]
    if not sup:
        bad.append("no row whose teaches opens 'supersedes S258 —'")
    else:
        row = sup[-1]
        if "lines 2-12" not in row:
            bad.append("superseding row lacks the corrected stamp range (lines 2-12)")
        for m in MEMBERS:
            p = Path("corpus/evidence/round80") / f"{m}-probe.txt"
            if not p.is_file():
                bad.append(f"receipt absent {p}")
                continue
            pref = hashlib.sha256(p.read_bytes()).hexdigest()[:8]
            if pref not in row:
                bad.append(f"superseding row lacks {m} sha256 prefix {pref}")
    lesson = rd("corpus/lessons/round-81.md")
    if "R80-U1" not in lesson:
        bad.append("lesson does not carry R80-U1")
    if "7923b6dc" not in rd("corpus/SOURCES.md") + lesson:
        bad.append("superseded anchor value 7923b6dc named nowhere")
    return bad


def u2() -> list[str]:
    """The scorecard's dated erratum names the clean measurement and the dirty one (R80-U2)."""
    bad: list[str] = []
    text = rd("SCORECARD.md")
    for tok in ("R80-U2", "gates-clean.txt", "e985e56a", "c1-after.txt", "WORKTREE dirty"):
        if tok not in text:
            bad.append(f"SCORECARD lacks {tok}")
    return bad


def u3() -> list[str]:
    """The census receipt exists, carries the values, and the command re-derives them (R80-U3)."""
    text = rd("corpus/evidence/round81/census-rows.txt")
    if "R80-U3" not in text:
        return ["census-rows.txt absent or unmarked"]
    bad: list[str] = []
    recorded = dict(re.findall(r"\b([0-9a-f]{8}) \([^)]*\): rows=(\d+)", text))
    for rev, want in (("dce7c275", "249"), ("507d249b", "250")):
        if recorded.get(rev) != want:
            bad.append(f"receipt does not state rows={want} for {rev}")
        proc = subprocess.run(["git", "show", f"{rev}:corpus/SOURCES.md"],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            bad.append(f"git show {rev} unavailable in this tree")
            continue
        got = sum(1 for ln in proc.stdout.splitlines() if ROW.match(ln))
        if str(got) != want:
            bad.append(f"recomputed rows at {rev} = {got}, receipt says {want}")
    return bad


def u4() -> list[str]:
    """The red-before run is committed and a QUALITY criterion cites it (R80-U4)."""
    text = rd("corpus/evidence/round81/r80-u4-red-before.txt")
    if "R80-U4" not in text:
        return ["r80-u4-red-before.txt absent or unmarked"]
    bad: list[str] = []
    for tok in ("ModuleNotFoundError: No module named 'Bio'", "exit code: 1"):
        if tok not in text:
            bad.append(f"receipt lacks {tok!r}")
    quality = rd("corpus/QUALITY.md")
    if "R80-U4" not in quality or "r80-u4-red-before.txt" not in quality:
        bad.append("QUALITY has no criterion citing R80-U4 and its receipt")
    return bad


def u5() -> list[str]:
    """All four gates (two round-80, two round-81) have registry rows (R80-U5)."""
    bad: list[str] = []
    text = rd("SKILL.md")
    if "R80-U5" not in text:
        bad.append("SKILL registry block does not carry R80-U5")
    for name in ("round80-c1-located-replay", "round80-c2-spotcheck-debt",
                 "round81-c1-new-members", "round81-c2-spotcheck-debt"):
        rows = [ln for ln in text.splitlines() if ln.startswith("| `" + name + "`")]
        if not rows:
            bad.append(f"no registry row for {name}")
            continue
        for tok in ("--lane .", "--selftest"):
            if tok not in rows[0]:
                bad.append(f"{name} row lacks {tok!r}")
    return bad


def u6() -> list[str]:
    """The lesson cites the six receipts and the README row names M80-1/M80-2 (R80-U6)."""
    bad: list[str] = []
    lesson = rd("corpus/lessons/round-81.md")
    if "R80-U6" not in lesson:
        bad.append("lesson has no R80-U6 correction")
    cited = sum(1 for m in MEMBERS if f"{m}-probe.txt" in lesson)
    if cited < 6:
        bad.append(f"lesson cites {cited}/6 round-80 receipts")
    rows = [ln for ln in rd("corpus/README.md").splitlines()
            if "round-80.md" in ln and "lessons/" in ln]
    if not rows:
        bad.append("README has no row for lessons/round-80.md")
    elif "M80-1" not in rows[0] or "M80-2" not in rows[0]:
        bad.append("README round-80 lesson row does not name both M80-1 and M80-2")
    return bad


CHECKS = {"u1": u1, "u2": u2, "u3": u3, "u4": u4, "u5": u5, "u6": u6}


def main(argv: list[str]) -> int:
    names = [a for a in argv if a in CHECKS]
    if "--all" in argv or not names:
        names = sorted(CHECKS)
    rc = 0
    for name in names:
        bad = CHECKS[name]()
        if bad:
            for b in bad:
                print(f"FAIL {name} {b}")
            rc = 1
        else:
            print(f"OK {name}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
