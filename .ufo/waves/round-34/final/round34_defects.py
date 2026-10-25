#!/usr/bin/env python3
"""Round 34 defect counter N1–N8 (landed by KengakuR34).

Re-derives the round's calibration closure checks: wave-tree trackedness, SCORECARD
section substance (heading-only resistance), fleet-report token-co-occurrence anchors,
lesson line-range anchors in canonical form (width/newline resistance), and two-way
knowledge/index parity. Exit 0 iff defects=0; `--selftest` exercises green and red
fixture trees. N3/N4 read a fleet root supplied by `--fleet-root` (default: the real
fleet repo), so the mutation harness can test them on a sandbox copy.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
FLEET = Path("/home/vgpnk/Projects/shokunin")
WAVES = (".ufo/waves/round-32", ".ufo/waves/round-33")
SCORECARD = "SCORECARD.md"
LESSON31 = "corpus/lessons/round-31.md"
LESSON30 = "corpus/lessons/round-30.md"
CLOSURE_TIP = "112091c"
PHANTOM = "a44b5a8"
REAL = "ae95fe0"


def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def git(lane: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(lane), *args], capture_output=True, text=True, check=False
    )


def section_lines(text: str, heading: str) -> int:
    """Number of non-heading, non-blank lines under `heading` until next heading."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith(heading):
            start = i
            break
    if start is None:
        return 0
    n = 0
    for ln in lines[start + 1:]:
        if re.match(r"^#{1,6}\s", ln):
            break
        if ln.strip():
            n += 1
    return n

def tolerant_find(text: str, token: str) -> bool:
    pattern = r"\s*".join(re.escape(ch) for ch in token)
    return re.search(pattern, text) is not None


def check_n1(lane: Path) -> str:
    for w in WAVES:
        tree = lane / w
        if not tree.is_dir():
            return f"DEFECT N1 wave-tree-committed: missing {w}"
        files = [p for p in tree.rglob("*") if p.is_file()]
        tracked = git(lane, "ls-files", "--", w).stdout.splitlines()
        tracked_set = {(lane / t).resolve() for t in tracked}
        untracked = [str(p) for p in files if p.resolve() not in tracked_set]
        if untracked:
            return f"DEFECT N1 wave-tree-committed: untracked {untracked[:3]}"
    return ""


def check_n2(lane: Path) -> str:
    text = read(lane / SCORECARD)
    if section_lines(text, "## Round 32") < 2:
        return "DEFECT N2 scorecard-round32-section: heading present without section substance"
    return ""


def check_n3(lane: Path, fleet: Path) -> str:
    report = read(fleet / ".ufo/reports/round-31/kengaku.md")
    if not report:
        return f"DEFECT N3 round31-report-append-only-erratum: {fleet / '.ufo/reports/round-31/kengaku.md'} is unreadable"
    if PHANTOM not in report:
        return "DEFECT N3 round31-report-append-only-erratum: phantom token a44b5a8 missing"
    if REAL not in report:
        return "DEFECT N3 round31-report-append-only-erratum: real locator token ae95fe0 missing"
    chunks = re.split(
        r"(?i)(?m)^\s*(?:(?:##|###|####)\s*|\*\*)(?:Erratum|Addendum|supersedes)",
        report,
    )
    if len(chunks) < 2 or not any(PHANTOM in c and REAL in c for c in chunks[1:]):
        return "DEFECT N3 round31-report-append-only-erratum: tokens not co-located in an erratum chunk"
    return ""


def check_n4(lane: Path, fleet: Path) -> str:
    report = read(fleet / ".ufo/reports/round-32/kengaku.md")
    if not report:
        return f"DEFECT N4 round32-report-closure-hash: {fleet / '.ufo/reports/round-32/kengaku.md'} is unreadable"
    if CLOSURE_TIP not in report:
        return "DEFECT N4 round32-report-closure-hash: closure tip 112091c missing"
    if not re.search(r"(?i)(?:closure|round-32|kengaku).{0,80}112091c|112091c.{0,80}(?:closure|round-32|kengaku)", report):
        return "DEFECT N4 round32-report-closure-hash: closure token lacks nearby section context"
    return ""


def check_n5(lane: Path) -> str:
    text = read(lane / LESSON31)
    marker = "precedence docstring at `:35-"
    start = text.find(marker)
    if start < 0:
        return "DEFECT N5 lesson31-line-range: :35-38 locator missing"
    if "\n" in text[start:start + 40]:
        return "DEFECT N5 lesson31-line-range: locator wrapped across a newline"
    if ":35-38`" not in text[start:start + 40]:
        return "DEFECT N5 lesson31-line-range: exact locator value changed"
    if not re.search(r"verifier_mode\.py.{0,160}:39-40", text, re.S):
        return "DEFECT N5 lesson31-line-range: :39-40 correction locator missing"
    return ""

def check_n6(lane: Path) -> str:
    text = read(lane / LESSON30)
    for token in (":78-81", ":72", "82-83", "S086", "peer review"):
        if token not in text:
            return f"DEFECT N6 lesson30-line-range: {token} canonical form lost"
    return ""


def check_n7(lane: Path) -> str:
    text = read(lane / SCORECARD)
    if section_lines(text, "## Round 33") < 2:
        return "DEFECT N7 scorecard-round33-section: heading present without section substance"
    return ""


def check_n8(lane: Path) -> str:
    knowledge = lane / "corpus/knowledge"
    readme = read(lane / "corpus/README.md")
    files = {p.name for p in knowledge.glob("*.md") if p.is_file()}
    index_rows = set(re.findall(r"`knowledge/([^`]+\.md)`", readme))
    missing_file = sorted(index_rows - files)
    dangling_row = sorted(files - index_rows)
    if missing_file or dangling_row:
        return f"DEFECT N8 knowledge-index-parity: missing {missing_file[:2]} dangling {dangling_row[:2]}"
    return ""


CHECKS = (
    (1, "wave-tree-committed", check_n1),
    (2, "scorecard-round32-section", check_n2),
    (3, "round31-report-append-only-erratum", check_n3),
    (4, "round32-report-closure-hash", check_n4),
    (5, "lesson31-line-range", check_n5),
    (6, "lesson30-line-range", check_n6),
    (7, "scorecard-round33-section", check_n7),
    (8, "knowledge-index-parity", check_n8),
)


def run_all(lane: Path, fleet: Path) -> list[str]:
    defects = []
    for i, label, fn in CHECKS:
        msg = fn(lane, fleet) if i in (3, 4) else fn(lane)
        if msg:
            defects.append(f"DEFECT N{i} {label}: {msg}")
    return defects


def selftest() -> int:
    failed = 0
    with tempfile.TemporaryDirectory(prefix="r34-defects-") as tmp:
        root = Path(tmp)

        def seed(base: Path, green: bool) -> None:
            for d in ("corpus/knowledge", "corpus/lessons",
                      ".ufo/waves/round-32", ".ufo/waves/round-33",
                      ".ufo/reports/round-31", ".ufo/reports/round-32"):
                (base / d).mkdir(parents=True)
            if green:
                (base / "corpus/knowledge/a.md").write_text("x", encoding="utf-8")
                (base / "corpus/README.md").write_text(
                    "| `knowledge/a.md` | a | S000 |\n", encoding="utf-8")
                (base / "corpus/lessons/round-30.md").write_text(
                    ":78-81\n:72\n82-83\nS086 without peer review\n",
                    encoding="utf-8")
                (base / "corpus/lessons/round-31.md").write_text(
                    ":35-38\n:39-40\nverifier_mode\n", encoding="utf-8")
                (base / "SCORECARD.md").write_text(
                    "## Round 32\nline a\nline b\n## Round 33\nline c\nline d\n",
                    encoding="utf-8")
                (base / ".ufo/reports/round-31/kengaku.md").write_text(
                    "## Erratum\n\na44b5a8 ... ae95fe0\n", encoding="utf-8")
                (base / ".ufo/reports/round-32/kengaku.md").write_text(
                    "## Round 32\nclosure tip 112091c\n", encoding="utf-8")
                (base / ".ufo/waves/round-32/seat.md").write_text("x", encoding="utf-8")
                (base / ".ufo/waves/round-33/seat.md").write_text("x", encoding="utf-8")
            else:
                (base / "corpus/README.md").write_text("", encoding="utf-8")
                (base / "corpus/lessons/round-30.md").write_text("", encoding="utf-8")
                (base / "corpus/lessons/round-31.md").write_text("", encoding="utf-8")
                (base / "SCORECARD.md").write_text(
                    "## Round 32\n## Round 33\n", encoding="utf-8")
                (base / ".ufo/reports/round-31/kengaku.md").write_text(
                    "# Report\n\nplain\n", encoding="utf-8")
                (base / ".ufo/reports/round-32/kengaku.md").write_text(
                    "# Report\n\nplain\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(base), "init", "-q"], check=True)
            subprocess.run(["git", "-C", str(base), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(base), "commit", "-qm", "seed"], check=True)

        green = root / "green"
        red = root / "red"
        seed(green, True)
        seed(red, False)
        green_defects = run_all(green, green)
        red_defects = run_all(red, red)
        if green_defects:
            print(f"[selftest] GREEN unexpected: {green_defects[:3]}")
            failed += 1
        if len(red_defects) < 8:
            print(f"[selftest] RED too few: {len(red_defects)}")
            failed += 1
    if failed:
        return 1
    print("SELFTEST cases=10 failed=0")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", default=str(LANE))
    parser.add_argument("--fleet-root", default=str(FLEET))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    defects = run_all(Path(args.lane), Path(args.fleet_root))
    for d in defects:
        print(d)
    print(f"checks=8 defects={len(defects)}")
    return 0 if not defects else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
