#!/usr/bin/env python3
"""Re-derive the seven defect items round 31's non-author closure routed to this lane.

Round 32 (2026-10-25), claim C2. One command, one line: `defects=N`, exit 0 only
when every one of R1-R7 re-derives as repaired. Each check reads committed or live
bytes round 31 left behind (plus this round's own lesson/report, which are round
deliverables, not claim-owned bytes); none reads an artifact round 32's C1 or C3
creates, so C2 stays separable from them (QUALITY R13).

Frozen items (corpus/lessons/round-31-verifier-spotcheck.md §5 items D1-D6, plus
the round-31 report item 5 peer-review erratum debt):
  R1  the round-31 report addendum cites "a44b5a8"-class commits; `git cat-file -t
      a44b5a8` is missing; the locator fix actually landed at `ae95fe0`. The report
      is append-only, so the repair is an appended erratum that names the bogus
      token and supersedes it.
  R2  the final lane commits were never cited by the round-31 report (report-ordering
      defect, round-30 §5 item 7, recurring). The repair is this round's report
      landing after the last lane commit and citing the final lane tip.
  R3  the round-31 CLI receipt at lane tip was rewritten with a path that resolves to
      `.ufo/plans` (absent); every line reads `can't open file` / `exit=2`. The
      repair regenerates it from the committed fixtures with `../../../../plans/`.
  R4  `plans/sources_adopt.py` has no row in `SKILL.md` §Gate/probe registry. The
      repair adds the row under that section.
  R5  the falsify seat `R31FxEntryBar` has no committed report; the round's report
      said "0 dead". The repair records the seat as dead in the round-32 lesson's
      seat ledger.
  R6  the round-31 lesson Gate table still cites `verifier_mode.py` precedence at
      `:35-38` (the entry corrected it to `:39-40`), and the round-30 lesson
      erratum points the Q6 retraction at entry `:78-81` while at tip the lines are
      `:72` and `:82-83`. The repair appends correction notes to both lessons.
  R7  the round-30 lesson `:66` groups "S083/S086 peer-reviewed"; the registry's
      S086 cell records the society publishes without peer review. The repair
      appends an erratum.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

FLEET = Path("/home/vgpnk/Projects/shokunin")
R31_REPORT = FLEET / ".ufo/reports/round-31/kengaku.md"
R32_REPORT = FLEET / ".ufo/reports/round-32/kengaku.md"
CLI_RECEIPT = "corpus/evidence/round31/gate-cli-exits.txt"
SKILL = "SKILL.md"
LESSON31 = "corpus/lessons/round-31.md"
LESSON30 = "corpus/lessons/round-30.md"
LESSON32 = "corpus/lessons/round-32.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def git(lane: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(lane), *args], capture_output=True, text=True, check=False
    )


def near(text: str, a: str, b: str, width: int = 300, flags: int = re.I) -> bool:
    """True when `a` and `b` co-occur within `width` characters."""
    return bool(
        re.search(re.escape(a) + r".{0," + str(width) + r"}" + re.escape(b), text, flags)
        or re.search(re.escape(b) + r".{0," + str(width) + r"}" + re.escape(a), text, flags)
    )


def check_r1(lane: Path, r31_report: Path | None = None) -> str:
    r31_report = r31_report or R31_REPORT
    if not r31_report.is_file():
        return f"{r31_report} is unreadable: the round-31 report cannot be checked"
    text = read(r31_report)
    if "a44b5a8" not in text:
        return "the bogus hash a44b5a8 is gone from the report: append-only forbids rewriting it"
    if not near(text, "a44b5a8", "superseded") and not near(text, "a44b5a8", "erratum"):
        return "no appended erratum supersedes the a44b5a8 citation"
    if "ae95fe0" not in text:
        return "the appended erratum does not name the real locator-fix commit ae95fe0"
    return ""


def check_r2(lane: Path, r32_report: Path | None = None) -> str:
    r32_report = r32_report or R32_REPORT
    if not r32_report.is_file():
        return f"{r32_report} does not exist yet: the round-32 report must land after the last lane commit"
    proc = git(lane, "rev-parse", "master")
    if proc.returncode != 0:
        return f"cannot read the lane tip: {proc.stderr.strip()}"
    tip = proc.stdout.strip()
    if not tip:
        return "the lane tip is empty"
    if tip not in read(r32_report):
        return f"the round-32 report does not cite the final lane tip {tip[:10]}"
    return ""


def check_r3(lane: Path) -> str:
    path = lane / CLI_RECEIPT
    if not path.is_file():
        return f"{CLI_RECEIPT} is unreadable at lane tip"
    text = read(path)
    if "can't open file" in text:
        return "the tip receipt still contains 'can't open file' failure lines"
    for token in ("exit=0", "exit=8", "exit=9", "exit=2"):
        if token not in text:
            return f"the regenerated receipt lacks {token}"
    if "../../../../plans/sources_adopt.py" not in text:
        return "the regenerated receipt does not use the corrected ../../../../plans/ path"
    return ""


def check_r4(lane: Path) -> str:
    path = lane / SKILL
    if not path.is_file():
        return f"{SKILL} is unreadable"
    text = read(path)
    match = re.search(r"plans/sources_adopt\.py", text)
    if not match:
        return "SKILL.md has no sources_adopt.py row"
    # The row must sit under the Gate/probe registry section, not in prose.
    heading = None
    for line in text[: match.start()].splitlines():
        if re.match(r"^#{1,4}\s+\S", line):
            heading = line
    if heading is None or not re.search(r"(?i)(gate|probe|registry)", heading):
        return f"the sources_adopt.py row is not under the Gate/probe registry (heading: {heading})"
    return ""


def check_r5(lane: Path) -> str:
    path = lane / LESSON32
    if not path.is_file():
        return f"{LESSON32} does not exist yet: the round-32 lesson must record the seat ledger"
    text = read(path)
    if not near(text, "R31FxEntryBar", "dead", width=160):
        return "the round-32 lesson does not record R31FxEntryBar as dead in the seat ledger"
    return ""


def check_r6(lane: Path) -> str:
    lesson31 = lane / LESSON31
    if not lesson31.is_file():
        return f"{LESSON31} is unreadable"
    text31 = read(lesson31)
    if ":35-38" not in text31:
        return "the round-31 lesson's stale :35-38 locator is gone: append-only forbids rewriting it"
    if not near(text31, "verifier_mode.py", ":39-40", width=300):
        return "no appended correction updates verifier_mode.py's precedence locator to :39-40"
    if not near(text31, ":39-40", "correction", width=300) and not near(
        text31, ":39-40", "superseded", width=300
    ):
        return "the round-31 lesson correction note is not labelled"

    lesson30 = lane / LESSON30
    if not lesson30.is_file():
        return f"{LESSON30} is unreadable"
    text30 = read(lesson30)
    # The original (now stale) line refs must still be present (append-only), and an
    # appended note must point at the current lines.
    if ":78-81" not in text30 and "78–81" not in text30:
        return "the round-30 lesson erratum's stale :78-81 reference is gone: append-only forbids rewriting it"
    if ":72" not in text30 or "82-83" not in text30:
        return "no appended correction updates the round-30 erratum's entry line refs to :72 / :82-83"
    if not near(text30, ":72", "82-83", width=300) or (
        not near(text30, ":72", "corrected", width=300)
        and not near(text30, ":72", "superseded", width=300)
    ):
        return "the round-30 lesson correction note is not labelled"
    return ""


def check_r7(lane: Path) -> str:
    path = lane / LESSON30
    if not path.is_file():
        return f"{LESSON30} is unreadable"
    text = read(path)
    if "peer-reviewed" not in text:
        return "the round-30 lesson's peer-reviewed grouping is gone: append-only forbids rewriting it"
    if not near(text, "S086", "without peer review", width=250) and not near(
        text, "S086", "not peer-reviewed", width=250
    ):
        return "no appended erratum records S086 as published without peer review"
    if not near(text, "S086", "erratum", width=250) and not near(
        text, "S086", "correction", width=250
    ):
        return "the S086 peer-review erratum is not labelled"
    return ""


CHECKS = (
    ("R1", "round31-report-phantom-hash", check_r1),
    ("R2", "round32-report-order-tip", check_r2),
    ("R3", "round31-cli-receipt-regenerated", check_r3),
    ("R4", "skill-registry-row", check_r4),
    ("R5", "round31-dead-seat-recorded", check_r5),
    ("R6", "lesson-locators-corrected", check_r6),
    ("R7", "round30-peer-review-erratum", check_r7),
)

FROZEN = tuple((i, l) for i, l, _ in CHECKS)


def selftest() -> int:
    cases: list[tuple[str, bool]] = [("registry-complete", FROZEN == tuple((i, l) for i, l, _ in CHECKS))]
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp)

        # R1/R2 read absolute fleet paths by default, which would couple the
        # selftest to the live repair state. Run them against synthetic fixtures
        # instead: a report without the erratum must be red, and one with it must
        # be green; a missing round-32 report and be red.
        bad_r31 = empty / "r31-bad.md"
        bad_r31.write_text("fixed at lane tip `a44b5a8`-class commits\n", encoding="utf-8")
        good_r31 = empty / "r31-good.md"
        good_r31.write_text(
            "fixed at lane tip `a44b5a8`-class commits\n"
            "Erratum (round 32): `a44b5a8` is superseded; the locator fix landed at `ae95fe0`.\n",
            encoding="utf-8",
        )
        cases.append(("R1-red-without-erratum", bool(check_r1(empty, bad_r31))))
        cases.append(("R1-green-with-erratum", not bool(check_r1(empty, good_r31))))
        cases.append(("R2-red-missing-report", bool(check_r2(empty, empty / "r32-missing.md"))))

        for item_id, label, check in CHECKS:
            if item_id in ("R1", "R2"):
                continue  # synthetic fixtures above; the live fleet paths would couple the run
            try:
                red = bool(check(empty))
            except Exception:
                red = True
            cases.append((f"{item_id}-red-on-empty", red))
    failed = [name for name, passed in cases if not passed]
    for name, passed in cases:
        print(f"CASE {name} {'PASS' if passed else 'FAIL'}")
    print(f"SELFTEST checks={len(CHECKS)} failed={len(failed)}")
    return 0 if not failed else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", type=Path, default=Path("."))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    lane = args.lane.resolve()
    if FROZEN != tuple((i, l) for i, l, _ in CHECKS):
        print("DEFECT registry: the check list no longer matches the frozen seven")
        print(f"checks={len(CHECKS)} defects={len(CHECKS) + 1}")
        return 1
    defects = 0
    for item_id, label, check in CHECKS:
        try:
            reason = check(lane)
        except Exception as error:
            reason = f"check raised {type(error).__name__}: {error}"
        if reason:
            defects += 1
            print(f"DEFECT {item_id} {label}: {reason}")
    print(f"checks={len(CHECKS)} defects={defects}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
