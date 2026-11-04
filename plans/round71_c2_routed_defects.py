#!/usr/bin/env python3
"""R71-C2 — the round-70 non-author closure's routed defects R70-D1 and R70-D2, re-derived.

R70-D1 (evidence standard): the round-70 lesson carries eight `## Mistakes` data rows, but three
sites disagreed — `LOG.md` said "five rows", `corpus/README.md` said "six Mistakes rows" in the
round-70 supporting block, and the lesson index row said "eight Mistakes rows" while naming only
six. Fix = an append-only `LOG.md` correction entry, both README mentions corrected to eight with
all eight row classes named, and an appended lesson erratum naming the under-sweep.

R70-D2 (citation): in `corpus/knowledge/tb2-nginx-request-logging-offline.md` the sentence that
cites `instruction.md:6-11` for the two HTTP bodies under-cites them (bodies are at `:15-18`).
Fix = an append-only erratum that quotes the superseded sentence and states the full range
`instruction.md:6-11,15-18`; the original sentence stays as written (corpus append-only norm).

Checks (each re-derives from the lane's committed bytes, no stored tally):
  E1a  the round-70 lesson's `## Mistakes` data-row count is 8 and the eight class keys are present
  E1b  `LOG.md` carries a dated correction entry naming R70-D1, quoting the superseded "five rows"
       and stating eight
  E1c  every `corpus/README.md` mention of round-70 Mistakes rows says eight and names all eight
       classes; no unsuperseded "five"/"six Mistakes rows" claim about round 70 remains
  E2a  the nginx entry keeps the superseded sentence verbatim and carries an `## Errata` block
       naming E-D2 with the corrected range `instruction.md:6-11,15-18`

Frozen predicate (R71-C2): `PREDICATE R71-C2 pass` iff all four checks print `ok`, `DEFECTS n=0`
and rc 0 at the round tip; `--selftest` shows `defects-in-fake=4 want=4 all-fail=True` plus the
append-only arm; `--mutants` shows 4/4 killed under single-check deletion.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

LESSON_REL = "corpus/lessons/round-70.md"
LOG_REL = "LOG.md"
README_REL = "corpus/README.md"
ENTRY_REL = "corpus/knowledge/tb2-nginx-request-logging-offline.md"

ROW_KEYS = (
    "staged-digest blind spot",
    "self-unreadable receipt",
    "argument-order",
    "exception-red",
    "speedy claim about isolation",
    "freeze-doc overclaim",
    "dead check clause",
    "unre-derived landing prose",
)
WANT_ROWS = len(ROW_KEYS)


def lane_root(arg):
    return Path(arg).resolve() if arg else Path(__file__).resolve().parent.parent


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def lesson_rows(text: str) -> list:
    """Data rows of the `## Mistakes` table(s): `|` lines that are neither header nor separator."""
    if "## Mistakes" not in text:
        return []
    section = text.split("## Mistakes", 1)[1]
    rows = []
    for line in section.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if rows and s and not s.startswith("|"):
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells or all(set(c) <= set("-: ") for c in cells):
            continue
        if cells[0].lower() == "class":
            continue
        rows.append(cells[0])
    return rows


def parse_count(phrase: str):
    m = re.search(r"\b(five|six|seven|eight|nine|ten|\d+)\s+Mistakes rows", phrase)
    if not m:
        return None
    word = m.group(1).lower()
    return {"five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}.get(word, word)


def check_e1_lesson(lane: Path, root: Path = None) -> list:
    text = read(lane / LESSON_REL)
    rows = lesson_rows(text)
    problems = []
    if len(rows) != WANT_ROWS:
        problems.append(f"row-count={len(rows)} want={WANT_ROWS}")
    for key in ROW_KEYS:
        if key not in text:
            problems.append(f"missing-row-class:{key}")
    return problems


def check_e1_log(lane: Path, root: Path = None) -> list:
    text = read(lane / LOG_REL)
    problems = []
    lines = text.splitlines()
    idx = [i for i, line in enumerate(lines) if "R70-D1" in line]
    if not idx:
        return ["no-R70-D1-correction-entry"]
    ok = False
    for i in idx:
        block = "\n".join(lines[max(0, i - 2):i + 24])
        if ("superseded" in block.lower() and "five" in block
                and re.search(r"\beight\b", block) and "2026-11-03" in block):
            ok = True
            break
    if not ok:
        problems.append("correction-entry-incomplete")
    return problems


def _readme_round70_lines(lines: list) -> dict:
    """The two sites: the lesson index row and the round-70 supporting-artifacts block."""
    sites = {}
    for i, line in enumerate(lines):
        if "`lessons/round-70.md`" in line and "Mistakes rows" in line:
            sites.setdefault("index-row", (i, line))
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## Round-70 supporting artifacts"):
            start = i
            break
    if start is not None:
        for i in range(start, min(start + 12, len(lines))):
            if "Mistakes rows" in lines[i]:
                sites.setdefault("support-block", (i, lines[i]))
                break
    return sites


def check_e1_readme(lane: Path, root: Path = None) -> list:
    lines = read(lane / README_REL).splitlines()
    problems = []
    sites = _readme_round70_lines(lines)
    if not sites:
        return ["no-round-70-readme-mention"]
    seen_idx = set()
    for name, (i, line) in sorted(sites.items()):
        seen_idx.add(i)
        n = parse_count(line)
        if n != WANT_ROWS:
            problems.append(f"{name}:count={n}")
        missing = [k for k in ROW_KEYS if k not in line]
        if missing:
            problems.append(f"{name}:missing={','.join(missing)}")
    # no other unsuperseded wrong count about round 70
    for i, line in enumerate(lines):
        if i in seen_idx:
            continue
        if "Mistakes rows" in line and ("round-70" in line or "round 70" in line):
            n = parse_count(line)
            if n is not None and n != WANT_ROWS:
                problems.append(f"line{i + 1}:count={n}")
    return problems


SUPERSEDED_SENTENCE = "states the same bodies"


def check_e2_entry(lane: Path, root: Path = None) -> list:
    text = read(lane / ENTRY_REL)
    flat = " ".join(text.split())
    problems = []
    if SUPERSEDED_SENTENCE not in flat:
        problems.append("superseded-sentence-missing")
    if "## Errata" not in text:
        return problems + ["no-errata-section"]
    errata = " ".join(text.split("## Errata", 1)[1].split())
    if "E-D2" not in errata:
        problems.append("no-E-D2")
    if "instruction.md:6-11,15-18" not in errata:
        problems.append("no-corrected-range")
    if "supersede" not in errata.lower():
        problems.append("no-supersedes-wording")
    if SUPERSEDED_SENTENCE not in errata:
        problems.append("erratum-does-not-quote-superseded-sentence")
    return problems


CHECKS = (
    ("E1a", check_e1_lesson),
    ("E1b", check_e1_log),
    ("E1c", check_e1_readme),
    ("E2a", check_e2_entry),
)


def run_checks(lane: Path, only=None) -> list:
    defects = []
    for code, fn in CHECKS:
        if only is not None and code not in only:
            continue
        problems = fn(lane)
        if problems:
            for p in problems:
                defects.append(f"DEFECT {code} {p}")
        else:
            print(f"{code} ok")
    return defects


def run_gate(lane: Path, quiet: bool = False) -> int:
    defects = run_checks(lane)
    if not quiet:
        for d in defects:
            print(d)
        print(f"DEFECTS n={len(defects)}")
        print(f"PREDICATE R71-C2 {'pass' if not defects else 'fail'}")
    return 0 if not defects else 1


# --------------------------------------------------------------------------- fixtures

FIXTURE_LESSON = """# Round 70 — fixture lesson

## Gate

- S242 admit.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
""" + "\n".join(f"| **{k}** | fixture | fixture | fixture |" for k in ROW_KEYS) + """

## Census

- fixture
"""

FIXTURE_LOG_RED = "# fixture log\n\n## Round 70\n\n- five rows of mistakes recorded.\n"
FIXTURE_LOG_GREEN = (
    "# fixture log\n\n## Round 70\n\n- five rows of mistakes recorded.\n"
    "- **Round-70 correction (R70-D1, round 71, 2026-11-03).** Append-only correction: the\n"
    "  line above is superseded — the lesson carries eight Mistakes rows. Old text kept as\n"
    "  written; the correct count is eight.\n")

FIXTURE_README_HEAD = "# fixture readme\n\n## Lessons\n\n| Entry | Covers |\n|---|---|\n"
FIXTURE_README_ROW_RED = (
    "| `lessons/round-70.md` | Gate, six Mistakes rows (staged-digest, self-unreadable receipt,"
    " argument order, exception-red, case-note isolation, freeze-doc overclaim) | fixture |\n")
FIXTURE_README_ROW_GREEN = (
    "| `lessons/round-70.md` | Gate, eight Mistakes rows (" + ", ".join(ROW_KEYS) +
    ") | fixture |\n")
FIXTURE_README_SUPPORT_RED = "\n## Round-70 supporting artifacts (2026-11-03)\n\n- Lesson: " \
    "`corpus/lessons/round-70.md` — Gate, six Mistakes rows, census 233 - 236.\n"
FIXTURE_README_SUPPORT_GREEN = "\n## Round-70 supporting artifacts (2026-11-03)\n\n- Lesson: " \
    "`corpus/lessons/round-70.md` — Gate, eight Mistakes rows (" + ", ".join(ROW_KEYS) + \
    "), census 233 - 236.\n"

FIXTURE_ENTRY_BASE = """source: S241 (fixture) — tests/test_outputs.py — anchor: instruction.md:6-11
verified-at: 2026-11-03
recheck: fixture

# fixture entry

The instruction at the same pin states the same bodies (`instruction.md:6-11`).
"""
FIXTURE_ENTRY_ERRATA = """

## Errata

- **E-D2 (round 71, 2026-11-03).** The sentence above is superseded: it does say the instruction
  `states the same bodies`, but the bodies are at `instruction.md:15-18`; the full range is
  `instruction.md:6-11,15-18`. Original sentence kept as written (append-only).
"""


def build_fixture(root: Path, green: bool, rows: int = WANT_ROWS) -> Path:
    root = Path(root)
    if root.exists():
        shutil.rmtree(root)
    (root / "corpus" / "lessons").mkdir(parents=True)
    (root / "corpus" / "knowledge").mkdir(parents=True)
    lesson = FIXTURE_LESSON
    if rows != WANT_ROWS:
        lesson = lesson.replace(
            "\n".join(f"| **{k}** | fixture | fixture | fixture |" for k in ROW_KEYS[rows:]),
            "")
    (root / LESSON_REL).write_text(lesson)
    (root / LOG_REL).write_text(FIXTURE_LOG_GREEN if green else FIXTURE_LOG_RED)
    row = FIXTURE_README_ROW_GREEN if green else FIXTURE_README_ROW_RED
    support = FIXTURE_README_SUPPORT_GREEN if green else FIXTURE_README_SUPPORT_RED
    (root / README_REL).write_text(FIXTURE_README_HEAD + row + support)
    (root / ENTRY_REL).write_text(
        FIXTURE_ENTRY_BASE + (FIXTURE_ENTRY_ERRATA if green else ""))
    return root


def run_selftest(work: Path) -> int:
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    red = build_fixture(work / "fake-red", green=False)
    green = build_fixture(work / "fake-green", green=True)
    stale = build_fixture(work / "fake-stale-lesson", green=False, rows=7)
    red_rc = run_gate(red, quiet=True)
    stale_rc = run_gate(stale, quiet=True)
    green_rc = run_gate(green, quiet=True)
    defects = run_checks(red) + run_checks(stale)
    codes_red = sorted({d.split()[1] for d in defects})
    want = sorted(code for code, _fn in CHECKS)
    all_fail = red_rc != 0 and stale_rc != 0 and green_rc == 0
    # append-only arm: rewriting the superseded sentence on GREEN bytes must turn E2a red
    rewritten = build_fixture(work / "fake-rewritten", green=True)
    entry = rewritten / ENTRY_REL
    entry.write_text(entry.read_text().replace("states the same bodies", "states the bodies"))
    hidden_codes = {d.split()[1] for d in run_checks(rewritten)}
    append_only_arm = "E2a" in hidden_codes
    ok = (all_fail and codes_red == want and append_only_arm)
    print(f"DEFECTS-RED n={len(defects)} codes={','.join(codes_red)} want={','.join(want)}")
    print(f"SELFTEST defects-in-fake={len(codes_red)} want={len(want)} all-fail={all_fail} "
          f"append-only-arm={append_only_arm} ok={ok}")
    return 0 if ok else 1


def run_mutants(work: Path) -> int:
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    red = build_fixture(work / "mutant-red", green=False, rows=7)
    src = Path(__file__).resolve().read_text()
    killed = 0
    total = 0
    for code, _fn in CHECKS:
        total += 1
        mutant_src = src.replace(f'    ("{code}", ', f'    # ({code} deleted) ("{code}"_x, ', 1)
        mutant_src = re.sub(rf'\s+\("{code}", (check_\w+)\),', "", mutant_src, count=1)
        mp = work / f"mutant-{code}.py"
        mp.write_text(mutant_src)
        out = subprocess.run([sys.executable, str(mp), "--lane", str(red)],
                             capture_output=True, text=True, timeout=120)
        absent = f"DEFECT {code} " not in out.stdout
        killed += 1 if absent else 0
        print(f"MUTANT {code} defect_absent={absent} killed={absent} rc={out.returncode}")
    print(f"MUTANTS total={total} killed={killed} survived={total - killed}")
    return 0 if killed == total else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    lane = lane_root(args.lane)
    if args.selftest:
        if not args.work:
            raise SystemExit("--selftest requires --work")
        return run_selftest(Path(args.work))
    if args.mutants:
        if not args.work:
            raise SystemExit("--mutants requires --work")
        return run_mutants(Path(args.work))
    if args.json:
        defects = run_checks(lane)
        print(json.dumps({"defects": defects, "n": len(defects)}))
        return 0 if not defects else 1
    return run_gate(lane)


if __name__ == "__main__":
    sys.exit(main())
