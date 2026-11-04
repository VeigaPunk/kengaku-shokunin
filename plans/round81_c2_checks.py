#!/usr/bin/env python3
"""R81-C2 repair checks — one subcommand per routed defect from the round-80 spot-check.

Each check exits 0 exactly when its repair holds in the tree it is run in, and non-zero otherwise.
They are the `check` commands the `corpus/routed-findings.jsonl` rows R80-U1…R80-U6 carry, so they
must be runnable from the lane root (`bash -lc 'python3 plans/round81_c2_checks.py u1'`) and must
fail when the repair's evidence is reverted to the round-81 base `4e833e9f`.

    python3 plans/round81_c2_checks.py u1 … u6
    python3 plans/round81_c2_checks.py --all
    python3 plans/round81_c2_checks.py --selftest --work DIR

Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent.parent
SOURCES = "corpus/SOURCES.md"
LESSON81 = "corpus/lessons/round-81.md"
SCORECARD = "SCORECARD.md"
SKILL = "SKILL.md"
QUALITY = "corpus/QUALITY.md"
README = "corpus/README.md"
CENSUS_ROWS = "corpus/evidence/round81/census-rows.txt"
U4_RECEIPT = "corpus/evidence/round81/r80-u4-red-before.txt"
MEMBERS80 = ("cancel-async-tasks", "chess-best-move", "distribution-search", "largest-eigenval",
             "openssl-selfsigned-cert", "protein-assembly")
ROW_RE = re.compile(r"^\|[ \t]*S[0-9]{3,}[ \t]*\|")


def read(root: Path, rel: str) -> str:
    try:
        return (root / rel).read_text(errors="replace")
    except OSError:
        return ""


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def u1(root: Path) -> list[str]:
    """A superseding SOURCES row states the corrected round-80 receipt anchors (R80-U1)."""
    bad: list[str] = []
    rows = [ln for ln in read(root, SOURCES).splitlines() if ln.startswith("| S")]
    sup = [ln for ln in rows if "supersedes S258 —" in ln]
    if not sup:
        bad.append("SOURCES: no row whose teaches opens 'supersedes S258 —'")
    else:
        row = sup[-1]
        if "lines 2-12" not in row:
            bad.append("S259 anchor does not state the corrected stamp range (lines 2-12)")
        for m in MEMBERS80:
            p = root / f"corpus/evidence/round80/{m}-probe.txt"
            if not p.is_file():
                bad.append(f"receipt absent corpus/evidence/round80/{m}-probe.txt")
                continue
            pref = hashlib.sha256(p.read_bytes()).hexdigest()[:8]
            if pref not in row:
                bad.append(f"S259 anchor lacks {m} sha256 prefix {pref}")
    text = read(root, SOURCES) + read(root, LESSON81)
    if "7923b6dc" not in text:
        bad.append("the superseded anchor value 7923b6dc is named nowhere")
    if "R80-U1" not in read(root, LESSON81):
        bad.append("LESSON: corpus/lessons/round-81.md does not carry R80-U1")
    return bad


def u2(root: Path) -> list[str]:
    """The scorecard's dated erratum names the clean measurement and the dirty one (R80-U2)."""
    bad: list[str] = []
    text = read(root, SCORECARD)
    for tok, why in (("R80-U2", "erratum id"), ("gates-clean.txt", "clean receipt"),
                     ("e985e56a", "clean revision"), ("c1-after.txt", "the dirty receipt"),
                     ("WORKTREE dirty", "the defect it names")):
        if tok not in text:
            bad.append(f"SCORECARD: no {why} ({tok})")
    return bad


def u3(root: Path) -> list[str]:
    """The census row counts have a producing command, and it re-derives both values (R80-U3)."""
    bad: list[str] = []
    text = read(root, CENSUS_ROWS)
    if "R80-U3" not in text:
        return ["census-rows receipt absent or unmarked"]
    recorded = dict(re.findall(r"\b([0-9a-f]{8}) \([^)]*\): rows=(\d+)", text))
    for rev, want in (("dce7c275", "249"), ("507d249b", "250")):
        if recorded.get(rev) != want:
            bad.append(f"receipt does not state rows={want} for {rev}")
        proc = git(root, "show", f"{rev}:{SOURCES}")
        if proc.returncode != 0:
            bad.append(f"git show {rev} fails in this tree")
            continue
        got = sum(1 for ln in proc.stdout.splitlines() if ROW_RE.match(ln))
        if str(got) != want:
            bad.append(f"recomputed rows at {rev} = {got}, receipt says {want}")
    return bad


def u4(root: Path) -> list[str]:
    """The red-before run is committed and a QUALITY criterion cites it (R80-U4)."""
    bad: list[str] = []
    text = read(root, U4_RECEIPT)
    if "R80-U4" not in text:
        return ["r80-u4-red-before receipt absent or unmarked"]
    for tok in ("ModuleNotFoundError: No module named 'Bio'", "exit code: 1",
                "uv run --no-project --with biopython"):
        if tok not in text:
            bad.append(f"receipt lacks {tok!r}")
    q = read(root, QUALITY)
    if "R80-U4" not in q or "r80-u4-red-before.txt" not in q:
        bad.append("QUALITY: no criterion citing R80-U4 and its receipt")
    return bad


def u5(root: Path) -> list[str]:
    """Both round-80 gates and both round-81 gates have registry rows (R80-U5)."""
    bad: list[str] = []
    text = read(root, SKILL)
    if "R80-U5" not in text:
        bad.append("SKILL: registry block does not carry R80-U5")
    need = ("round80-c1-located-replay", "round80-c2-spotcheck-debt",
            "round81-c1-new-members", "round81-c2-spotcheck-debt")
    for name in need:
        rows = [ln for ln in text.splitlines() if ln.startswith("| `" + name + "`")]
        if not rows:
            bad.append(f"SKILL: no registry row for {name}")
            continue
        row = rows[0]
        for tok in ("--lane .", "--selftest"):
            if tok not in row:
                bad.append(f"{name} row lacks {tok!r}")
    return bad


def u6(root: Path) -> list[str]:
    """The lesson cites the six receipts instead of the uncommitted driver line (R80-U6)."""
    bad: list[str] = []
    lesson = read(root, LESSON81)
    if "R80-U6" not in lesson:
        bad.append("LESSON: no R80-U6 correction")
    if "REMINT minted=6" in lesson and "not a receipt" not in lesson:
        bad.append("LESSON: repeats the uncommitted driver line without the correction")
    cited = sum(1 for m in MEMBERS80 if f"{m}-probe.txt" in lesson)
    if cited < 6:
        bad.append(f"LESSON: cites {cited}/6 round-80 receipts")
    row = [ln for ln in read(root, README).splitlines()
           if "round-80.md" in ln and "lessons/" in ln]
    if not row:
        bad.append("README: no row for lessons/round-80.md")
    elif not ("M80-1" in row[0] and "M80-2" in row[0]):
        bad.append("README: the round-80 lesson row does not name both M80-1 and M80-2")
    return bad


CHECKS = {"u1": u1, "u2": u2, "u3": u3, "u4": u4, "u5": u5, "u6": u6}


def build_fixture(root: Path) -> None:
    """A green tree for all six checks: two tagged revisions carrying one and two registry rows,
    six committed round-80 receipts whose prefixes the superseding row carries, and every repair
    artifact."""
    root.mkdir(parents=True, exist_ok=True)
    for m in MEMBERS80:
        p = root / f"corpus/evidence/round80/{m}-probe.txt"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"# tb2 {m} grader probe\n")
    git(root, "init", "-q")
    git(root, "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
    (root / SOURCES).write_text("".join(f"| S{i:03d} | a |\n" for i in range(1, 250)))
    git(root, "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
    git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "one")
    git(root, "tag", "dce7c275")
    (root / SOURCES).write_text("".join(f"| S{i:03d} | a |\n" for i in range(1, 251)))
    git(root, "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
    git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "two")
    git(root, "tag", "507d249b")
    prefs = "".join(
        " " + hashlib.sha256((root / f"corpus/evidence/round80/{m}-probe.txt").read_bytes()
                             ).hexdigest()[:8] for m in MEMBERS80)
    (root / SOURCES).write_text(
        "| S259 | x | own-work | A | scope | lines 2-12 | supersedes S258 — anchored | mined | "
        "2026-11-04 | 2027-01-18 | corpus/lessons/round-81.md |" + prefs + "\n")
    (root / CENSUS_ROWS).parent.mkdir(parents=True, exist_ok=True)
    (root / CENSUS_ROWS).write_text(
        "R80-U3\ndce7c275 (a): rows=249\n507d249b (b): rows=250\n")
    (root / LESSON81).parent.mkdir(parents=True, exist_ok=True)
    (root / LESSON81).write_text(
        "R80-U1 superseded text 7923b6dc\nR80-U6 correction: the line is not a receipt\n"
        + "".join(f"{m}-probe.txt\n" for m in MEMBERS80))
    (root / SCORECARD).write_text("R80-U2 gates-clean.txt e985e56a c1-after.txt WORKTREE dirty\n")
    (root / U4_RECEIPT).write_text(
        "R80-U4\nuv run --no-project --with biopython\nModuleNotFoundError: No module named 'Bio'"
        "\nexit code: 1\n")
    (root / QUALITY).parent.mkdir(parents=True, exist_ok=True)
    (root / QUALITY).write_text("Q9 R80-U4 see corpus/evidence/round81/r80-u4-red-before.txt\n")
    (root / SKILL).write_text(
        "R80-U5\n"
        "| `round80-c1-located-replay` | gate | `python3 x --lane .` | 0 | `--selftest --work D` |\n"
        "| `round80-c2-spotcheck-debt` | gate | `python3 y --lane .` | 0 | `--selftest --work D` |\n"
        "| `round81-c1-new-members` | gate | `python3 z --lane .` | 0 | `--selftest --work D` |\n"
        "| `round81-c2-spotcheck-debt` | gate | `python3 w --lane .` | 0 | `--selftest --work D` |\n")
    (root / README).parent.mkdir(parents=True, exist_ok=True)
    (root / README).write_text("| `lessons/round-80.md` | M80-1/M80-2 |\n")


def selftest(work: Path) -> int:
    failures = 0
    cases = 0
    root = work / "green"
    if root.exists():
        shutil.rmtree(root)
    build_fixture(root)
    for name, fn in CHECKS.items():
        cases += 1
        bad = fn(root)
        if bad:
            failures += 1
            print(f"SELFTEST-FAIL green {name} {bad[:2]}")
    for name in CHECKS:
        r = work / f"drop-{name}"
        if r.exists():
            shutil.rmtree(r)
        shutil.copytree(root, r)
        rel = {"u1": SOURCES, "u2": SCORECARD, "u3": CENSUS_ROWS, "u4": U4_RECEIPT,
               "u5": SKILL, "u6": LESSON81}[name]
        (r / rel).unlink()
        cases += 1
        if not CHECKS[name](r):
            failures += 1
            print(f"SELFTEST-FAIL drop-{name} still passes")
        shutil.rmtree(r)
    shutil.rmtree(root)
    print(f"SELFTEST cases={cases} red={len(CHECKS)} failures={failures}")
    return 0 if failures == 0 else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name", nargs="?", choices=sorted(CHECKS))
    ap.add_argument("--lane", default=str(LANE))
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", default=None)
    a = ap.parse_args(argv)
    if a.selftest:
        work = Path(a.work) if a.work else Path("/fast/scratch/hyaku/kengaku-r81/c2checks")
        work.mkdir(parents=True, exist_ok=True)
        return selftest(work)
    root = Path(a.lane).resolve()
    names = sorted(CHECKS) if a.all or not a.name else [a.name]
    rc = 0
    for name in names:
        bad = CHECKS[name](root)
        if bad:
            for b in bad:
                print(f"FAIL {name} {b}")
            rc = 1
        else:
            print(f"OK {name}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
