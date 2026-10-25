#!/usr/bin/env python3
"""Re-derive the eight round-34 C2 calibration defects, offline."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

R31_REPORT = Path(".ufo/reports/round-31/kengaku.md")
R32_REPORT = Path(".ufo/reports/round-32/kengaku.md")
WAVES = (".ufo/waves/round-32", ".ufo/waves/round-33")
SCORECARD = "SCORECARD.md"
LESSON31 = "corpus/lessons/round-31.md"
LESSON30 = "corpus/lessons/round-30.md"
LESSON33 = "corpus/lessons/round-33.md"
LEDGER33 = ".ufo/waves/round-33/falsify/swarm-registry.json"
INDEX = "corpus/README.md"
KNOWLEDGE = "corpus/knowledge"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def git(lane: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True, check=False)


def anchored(text: str, token: str) -> bool:
    """Match locator tokens on a line, permitting whitespace around punctuation."""
    nums = re.escape(token.lstrip(":"))
    return bool(re.search(r"(?m)^\s*[^\n]*?(?<!\w):?\s*" + nums + r"(?!\d)[^\n]*$", text))


def check_n1(lane: Path) -> str:
    for subtree in WAVES:
        path = lane / subtree
        if not path.is_dir():
            return f"{subtree} is missing or unreadable"
        proc = git(lane, "ls-files", "--", subtree)
        if proc.returncode:
            return f"git ls-files failed for {subtree}: {proc.stderr.strip()}"
        tracked = {x for x in proc.stdout.splitlines() if x}
        disk = {p.relative_to(lane).as_posix() for p in path.rglob("*") if p.is_file()}
        missing = sorted(disk - tracked)
        if missing:
            return f"{len(missing)} untracked files under {subtree}: {', '.join(missing[:3])}"
    return ""


def check_n2(lane: Path) -> str:
    path = lane / SCORECARD
    if not path.is_file(): return f"{SCORECARD} is unreadable"
    text = read(path)
    for n in (32, 33):
        m = re.search(rf"(?m)^## Round {n}\b[^\n]*(?:\n|$)", text)
        if not m: return f"missing ## Round {n} section"
        rest = text[m.end():]
        end = re.search(r"(?m)^## ", rest)
        section = rest[:end.start()] if end else rest
        content = [line for line in section.splitlines() if line.strip() and not line.lstrip().startswith("#")]
        if len(content) < 2: return f"Round {n} has fewer than two non-heading content lines"
    return ""


def check_n3(lane: Path, report: Path | None = None) -> str:
    path = report or lane / R31_REPORT
    if not path.is_file(): return f"{path} is unreadable"
    text = read(path)
    if "a44b5a8" not in text: return "round-31 report no longer retains a44b5a8 (append-only)"
    if not ("ae95fe0" in text and re.search(r"errat|correct|supersed", text, re.I)):
        return "no appended erratum after retained a44b5a8 names ae95fe0"
    return ""


def check_n4(lane: Path, report: Path | None = None) -> str:
    path = report or lane / R32_REPORT
    if not path.is_file(): return f"{path} is unreadable"
    if "112091c" not in read(path): return "round-32 report does not contain 112091c"
    return ""


def check_n5(lane: Path) -> str:
    path = lane / LESSON31
    if not path.is_file(): return f"{LESSON31} is unreadable"
    text = read(path)
    if not anchored(text, ":35-38"): return "round-31 lesson does not retain anchored :35-38 locator"
    if not re.search(r"(?im)^.*(?:correction|corrected|supersed).*(?:verifier_mode\.py|:39\s*-\s*40)|^.*(?:verifier_mode\.py|:39\s*-\s*40).*(?:correction|corrected|supersed).*$", text):
        return "round-31 lesson lacks anchored correction note for verifier_mode.py :39-40"
    return ""


def check_n6(lane: Path) -> str:
    path = lane / LESSON30
    if not path.is_file(): return f"{LESSON30} is unreadable"
    text = read(path)
    for token in (":78-81", ":72", "82-83"):
        if not anchored(text, token): return f"round-30 lesson lacks anchored retained locator {token}"
    if not re.search(r"(?im)^.*(?:S086|peer.review).*(?:erratum|correction|without peer review|not peer-reviewed)|^.*(?:erratum|correction).*(?:S086|peer.review).*$", text):
        return "round-30 lesson lacks anchored S086 erratum"
    return ""


def check_n7(lane: Path) -> str:
    lesson, ledger = lane / LESSON33, lane / LEDGER33
    if not lesson.is_file(): return f"{LESSON33} is unreadable"
    if not ledger.is_file(): return f"{LEDGER33} is unreadable"
    try:
        import json
        data = json.loads(read(ledger))
        members = data.get("members", [])
        count = len(members)
    except (ValueError, TypeError, AttributeError) as error:
        return f"cannot read seat ledger: {error}"
    text = read(lesson)
    if not re.search(r"(?im)^.*(?:36\s*\+\s*53\s*=\s*89|36 build.*53 falsify.*89).*$", text):
        return "round-33 lesson has no dated correction stating ledger sum 36+53=89"
    if count != 53: return f"seat ledger has {count} falsify members, expected 53"
    correction = re.search(r"(?im)^.*(?:correction|erratum).*(\d{4}-\d{2}-\d{2}).*$", text)
    if not correction: return "round-33 correction line is not dated"
    if not re.search(r"(?im)^.*(?:36\s*\+\s*53\s*=\s*89|36 build.*53 falsify.*89).*$", text):
        return "round-33 correction does not match seat ledger total"
    return ""


def check_n8(lane: Path) -> str:
    directory, index = lane / KNOWLEDGE, lane / INDEX
    if not directory.is_dir(): return f"{KNOWLEDGE} is unreadable"
    if not index.is_file(): return f"{INDEX} is unreadable"
    files = {p.stem for p in directory.glob("*.md")}
    rows = re.findall(r"(?m)^\|\s*`knowledge/([^`]+\.md)`\s*\|", read(index))
    stems = [Path(name).stem for name in rows]
    duplicate = sorted(name for name in set(stems) if stems.count(name) != 1)
    missing_rows, missing_files = sorted(files - set(stems)), sorted(set(stems) - files)
    if duplicate or missing_rows or missing_files:
        return f"knowledge/index parity failure; missing rows={missing_rows[:3]}, missing files={missing_files[:3]}, duplicate rows={duplicate[:3]}"
    return ""


CHECKS = (
    ("N1", "round32-round33-wave-tracking", check_n1),
    ("N2", "scorecard-round-sections", check_n2),
    ("N3", "round31-report-append-only-erratum", check_n3),
    ("N4", "round32-report-closure-hash", check_n4),
    ("N5", "round31-lesson-width-newline-locator", check_n5),
    ("N6", "round30-lesson-width-newline-errata", check_n6),
    ("N7", "round33-lesson-ledger-correction", check_n7),
    ("N8", "knowledge-readme-bidirectional-parity", check_n8),
)


def selftest() -> int:
    cases: list[tuple[str, bool]] = []
    with tempfile.TemporaryDirectory() as tmp:
        lane = Path(tmp)
        for sub in WAVES: (lane / sub).mkdir(parents=True)
        (lane / SCORECARD).write_text("## Round 32\none\ntwo\n## Round 33\none\ntwo\n")
        (lane / "corpus/lessons").mkdir(parents=True)
        (lane / LESSON31).write_text("old :35-38\nCorrection verifier_mode.py :39 - 40\n")
        (lane / LESSON30).write_text("old :78-81 and :72; 82-83\nErratum S086 without peer review\n")
        (lane / LESSON33).write_text("Correction (2026-10-25): 36 + 53 = 89\n")
        (lane / LEDGER33).parent.mkdir(parents=True)
        (lane / LEDGER33).write_text('{"members":[' + ','.join('{"id":%d}' % i for i in range(53)) + '] }')
        (lane / R31_REPORT).parent.mkdir(parents=True)
        (lane / R31_REPORT).write_text("a44b5a8\n\nErratum: correction ae95fe0\n")
        (lane / R32_REPORT).parent.mkdir(parents=True)
        (lane / R32_REPORT).write_text("112091c\n")
        (lane / KNOWLEDGE).mkdir(parents=True)
        (lane / KNOWLEDGE / "sample.md").write_text("x\n")
        (lane / INDEX).write_text("| `knowledge/sample.md` |\n")
        subprocess.run(["git", "-C", str(lane), "init", "-q"], check=False)
        subprocess.run(["git", "-C", str(lane), "add", "."], check=False)
        for item_id, label, check in CHECKS:
            try: ok = not check(lane)
            except Exception: ok = False
            cases.append((f"{item_id}-green", ok))
        # Red controls target the failure modes explicitly.
        (lane / SCORECARD).write_text("## Round 32\n## Round 33\n")
        cases.append(("N2-red-heading-only", bool(check_n2(lane))))
        (lane / KNOWLEDGE / "orphan.md").write_text("x\n")
        cases.append(("N8-red-unindexed-file", bool(check_n8(lane))))
        (lane / R31_REPORT).write_text("a44b5a8 " + "x\n"*30 + "Erratum: correction ae95fe0\n")
        cases.append(("N3-red-distant-tokens", bool(check_n3(lane))))
    failed = [name for name, ok in cases if not ok]
    for name, ok in cases: print(f"CASE {name} {'PASS' if ok else 'FAIL'}")
    print(f"SELFTEST cases={len(cases)} failed={len(failed)}")
    return 0 if not failed else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", type=Path, default=Path("."))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest: return selftest()
    lane = args.lane.resolve()
    defects = 0
    for item_id, label, check in CHECKS:
        try: reason = check(lane)
        except Exception as error: reason = f"check raised {type(error).__name__}: {error}"
        if reason:
            defects += 1
            print(f"DEFECT {item_id} {label}: {reason}")
    print(f"checks=8 defects={defects}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
